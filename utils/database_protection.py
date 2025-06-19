import os
import shutil
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
import json
import fcntl
import tempfile
from contextlib import contextmanager

class DatabaseProtection:
    """
    Comprehensive database protection framework to prevent accidental deletion
    and provide automated backup capabilities.
    """
    
    def __init__(self, db_path: str = "finance.db", backup_dir: str = "backups"):
        """
        Initialize database protection.
        
        Args:
            db_path (str): Path to the main database file
            backup_dir (str): Directory for automated backups
        """
        self.db_path = Path(db_path)
        self.backup_dir = Path(backup_dir)
        self.lock_file = Path(f".{self.db_path.stem}.lock")
        self.protection_config = Path("database_protection.json")
        
        # Ensure backup directory exists
        self.backup_dir.mkdir(exist_ok=True)
        
        # Initialize protection config
        self._init_protection_config()
    
    def _init_protection_config(self):
        """Initialize or load protection configuration."""
        default_config = {
            "auto_backup_enabled": True,
            "backup_interval_hours": 6,
            "max_backups": 10,
            "protection_enabled": True,
            "checksum_verification": True,
            "last_backup": None,
            "backup_retention_days": 30
        }
        
        if not self.protection_config.exists():
            with open(self.protection_config, 'w') as f:
                json.dump(default_config, f, indent=4)
        
        with open(self.protection_config, 'r') as f:
            self.config = json.load(f)
    
    def _save_config(self):
        """Save current protection configuration."""
        with open(self.protection_config, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate SHA256 checksum of a file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    @contextmanager
    def database_lock(self):
        """Context manager for database file locking."""
        lock_fd = None
        try:
            lock_fd = os.open(self.lock_file, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            yield
        except (OSError, IOError) as e:
            raise RuntimeError(f"Database is locked by another process: {e}")
        finally:
            if lock_fd:
                fcntl.flock(lock_fd, fcntl.LOCK_UN)
                os.close(lock_fd)
                try:
                    os.unlink(self.lock_file)
                except OSError:
                    pass
    
    def create_backup(self, backup_name: Optional[str] = None) -> Path:
        """
        Create a backup of the main database.
        
        Args:
            backup_name (str, optional): Custom backup name
            
        Returns:
            Path: Path to the created backup file
        """
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database file not found: {self.db_path}")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if backup_name:
            backup_filename = f"{backup_name}_{timestamp}.db"
        else:
            backup_filename = f"{self.db_path.stem}_backup_{timestamp}.db"
        
        backup_path = self.backup_dir / backup_filename
        
        # Use database lock for safe backup
        with self.database_lock():
            # Verify database integrity before backup
            self._verify_database_integrity()
            
            # Create backup
            shutil.copy2(self.db_path, backup_path)
            
            # Verify backup integrity
            if self.config["checksum_verification"]:
                original_checksum = self._calculate_checksum(self.db_path)
                backup_checksum = self._calculate_checksum(backup_path)
                
                if original_checksum != backup_checksum:
                    backup_path.unlink()  # Remove corrupted backup
                    raise RuntimeError("Backup verification failed: checksums don't match")
        
        # Update config
        self.config["last_backup"] = datetime.now().isoformat()
        self._save_config()
        
        print(f"Database backup created: {backup_path}")
        return backup_path
    
    def _verify_database_integrity(self):
        """Verify database integrity using SQLite's PRAGMA integrity_check."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("PRAGMA integrity_check")
                result = cursor.fetchone()[0]
                if result != "ok":
                    raise RuntimeError(f"Database integrity check failed: {result}")
        except sqlite3.Error as e:
            raise RuntimeError(f"Database integrity verification failed: {e}")
    
    def auto_backup_if_needed(self):
        """Create automatic backup if needed based on configured interval."""
        if not self.config["auto_backup_enabled"]:
            return
        
        last_backup = self.config.get("last_backup")
        if last_backup:
            last_backup_time = datetime.fromisoformat(last_backup)
            hours_since_backup = (datetime.now() - last_backup_time).total_seconds() / 3600
            
            if hours_since_backup < self.config["backup_interval_hours"]:
                return
        
        # Create automatic backup
        self.create_backup("auto")
        self._cleanup_old_backups()
    
    def _cleanup_old_backups(self):
        """Remove old backups beyond retention policy."""
        backup_files = list(self.backup_dir.glob("*.db"))
        backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Keep only max_backups files
        max_backups = self.config["max_backups"]
        if len(backup_files) > max_backups:
            for old_backup in backup_files[max_backups:]:
                old_backup.unlink()
                print(f"Removed old backup: {old_backup}")
        
        # Remove backups older than retention period
        retention_days = self.config["backup_retention_days"]
        cutoff_time = datetime.now().timestamp() - (retention_days * 24 * 3600)
        
        for backup_file in backup_files:
            if backup_file.stat().st_mtime < cutoff_time:
                backup_file.unlink()
                print(f"Removed expired backup: {backup_file}")
    
    def protect_database(self):
        """Apply protection mechanisms to the database file."""
        if not self.config["protection_enabled"]:
            print("Database protection is disabled")
            return
        
        # Make database read-only for additional protection
        current_mode = self.db_path.stat().st_mode
        os.chmod(self.db_path, current_mode & ~0o222)  # Remove write permissions
        print(f"Database protection applied: {self.db_path}")
    
    def unprotect_database(self):
        """Remove protection mechanisms from the database file."""
        # Restore write permissions
        current_mode = self.db_path.stat().st_mode
        os.chmod(self.db_path, current_mode | 0o644)  # Restore write permissions
        print(f"Database protection removed: {self.db_path}")
    
    def safe_database_operation(self, operation_name: str = "database_operation"):
        """
        Context manager for safe database operations with automatic backup.
        
        Args:
            operation_name (str): Name of the operation for backup naming
        """
        return SafeDatabaseOperation(self, operation_name)
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """
        List all available backups with metadata.
        
        Returns:
            List[Dict]: List of backup information
        """
        backups = []
        for backup_file in self.backup_dir.glob("*.db"):
            stat = backup_file.stat()
            backups.append({
                "name": backup_file.name,
                "path": str(backup_file),
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "checksum": self._calculate_checksum(backup_file) if self.config["checksum_verification"] else None
            })
        
        return sorted(backups, key=lambda x: x["created"], reverse=True)
    
    def restore_backup(self, backup_path: str, confirm: bool = False):
        """
        Restore database from backup.
        
        Args:
            backup_path (str): Path to backup file
            confirm (bool): Confirmation flag to prevent accidental restoration
        """
        if not confirm:
            raise ValueError("Restoration requires explicit confirmation (confirm=True)")
        
        backup_file = Path(backup_path)
        if not backup_file.exists():
            raise FileNotFoundError(f"Backup file not found: {backup_path}")
        
        # Create safety backup of current database
        safety_backup = self.create_backup("pre_restore_safety")
        
        try:
            with self.database_lock():
                # Verify backup integrity
                with sqlite3.connect(backup_file) as conn:
                    cursor = conn.execute("PRAGMA integrity_check")
                    result = cursor.fetchone()[0]
                    if result != "ok":
                        raise RuntimeError(f"Backup file is corrupted: {result}")
                
                # Restore backup
                shutil.copy2(backup_file, self.db_path)
                print(f"Database restored from: {backup_path}")
                print(f"Safety backup created: {safety_backup}")
        
        except Exception as e:
            # Restore from safety backup if restoration fails
            shutil.copy2(safety_backup, self.db_path)
            raise RuntimeError(f"Restoration failed, reverted to original: {e}")
    
    def status(self) -> Dict[str, Any]:
        """Get protection status and statistics."""
        backups = self.list_backups()
        
        return {
            "database_path": str(self.db_path),
            "database_exists": self.db_path.exists(),
            "database_size": self.db_path.stat().st_size if self.db_path.exists() else 0,
            "protection_enabled": self.config["protection_enabled"],
            "auto_backup_enabled": self.config["auto_backup_enabled"],
            "backup_count": len(backups),
            "last_backup": self.config.get("last_backup"),
            "backup_dir": str(self.backup_dir),
            "latest_backup": backups[0] if backups else None
        }


class SafeDatabaseOperation:
    """Context manager for safe database operations with automatic backup."""
    
    def __init__(self, protection: DatabaseProtection, operation_name: str):
        self.protection = protection
        self.operation_name = operation_name
        self.pre_operation_backup = None
    
    def __enter__(self):
        # Create pre-operation backup
        self.pre_operation_backup = self.protection.create_backup(f"pre_{self.operation_name}")
        
        # Remove database protection temporarily
        self.protection.unprotect_database()
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                # Operation succeeded, create post-operation backup
                self.protection.create_backup(f"post_{self.operation_name}")
                print(f"Safe operation completed: {self.operation_name}")
            else:
                # Operation failed, consider restoring from backup
                print(f"Operation failed: {self.operation_name}")
                print(f"Pre-operation backup available: {self.pre_operation_backup}")
        finally:
            # Always reapply protection
            self.protection.protect_database()


# Convenience functions for easy usage
def init_protection(db_path: str = "finance.db") -> DatabaseProtection:
    """Initialize database protection for the given database."""
    return DatabaseProtection(db_path)

def create_backup(db_path: str = "finance.db", backup_name: str = None) -> Path:
    """Create a quick backup of the database."""
    protection = DatabaseProtection(db_path)
    return protection.create_backup(backup_name)

def safe_operation(operation_name: str = "operation", db_path: str = "finance.db"):
    """Context manager for safe database operations."""
    protection = DatabaseProtection(db_path)
    return protection.safe_database_operation(operation_name) 