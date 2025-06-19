#!/usr/bin/env python3
"""
Database Protection Management Script

This script provides command-line interface for managing database protection,
backups, and recovery operations.

Usage:
    python scripts/protect_database.py backup
    python scripts/protect_database.py protect
    python scripts/protect_database.py status
    python scripts/protect_database.py list-backups
    python scripts/protect_database.py restore <backup_name> --confirm
"""

import sys
import argparse
from pathlib import Path
import json
from datetime import datetime

# Add parent directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.database_protection import DatabaseProtection, init_protection

def format_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

def format_datetime(iso_string: str) -> str:
    """Format ISO datetime string for display."""
    try:
        dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return iso_string

def cmd_backup(args):
    """Create a database backup."""
    protection = init_protection(args.database)
    
    try:
        backup_path = protection.create_backup(args.name)
        print(f"✅ Backup created successfully!")
        print(f"   Path: {backup_path}")
        print(f"   Size: {format_size(backup_path.stat().st_size)}")
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        sys.exit(1)

def cmd_protect(args):
    """Apply database protection."""
    protection = init_protection(args.database)
    
    try:
        protection.protect_database()
        print("🔒 Database protection applied successfully!")
        print("   Database is now read-only protected")
        print("   Use 'unprotect' command to remove protection for operations")
    except Exception as e:
        print(f"❌ Protection failed: {e}")
        sys.exit(1)

def cmd_unprotect(args):
    """Remove database protection."""
    protection = init_protection(args.database)
    
    try:
        protection.unprotect_database()
        print("🔓 Database protection removed successfully!")
        print("   Database is now writable")
        print("   Remember to reapply protection after operations")
    except Exception as e:
        print(f"❌ Unprotection failed: {e}")
        sys.exit(1)

def cmd_status(args):
    """Show database protection status."""
    protection = init_protection(args.database)
    
    try:
        status = protection.status()
        
        print("📊 Database Protection Status")
        print("=" * 40)
        print(f"Database: {status['database_path']}")
        print(f"Exists: {'✅ Yes' if status['database_exists'] else '❌ No'}")
        
        if status['database_exists']:
            print(f"Size: {format_size(status['database_size'])}")
        
        print(f"Protection: {'🔒 Enabled' if status['protection_enabled'] else '🔓 Disabled'}")
        print(f"Auto Backup: {'✅ Enabled' if status['auto_backup_enabled'] else '❌ Disabled'}")
        print(f"Backup Count: {status['backup_count']}")
        print(f"Backup Directory: {status['backup_dir']}")
        
        if status['last_backup']:
            print(f"Last Backup: {format_datetime(status['last_backup'])}")
        else:
            print("Last Backup: Never")
        
        if status['latest_backup']:
            latest = status['latest_backup']
            print(f"Latest Backup: {latest['name']} ({format_size(latest['size'])})")
    
    except Exception as e:
        print(f"❌ Status check failed: {e}")
        sys.exit(1)

def cmd_list_backups(args):
    """List all available backups."""
    protection = init_protection(args.database)
    
    try:
        backups = protection.list_backups()
        
        if not backups:
            print("📂 No backups found")
            return
        
        print(f"📂 Available Backups ({len(backups)})")
        print("=" * 80)
        print(f"{'Name':<40} {'Size':<10} {'Created':<20}")
        print("-" * 80)
        
        for backup in backups:
            name = backup['name']
            size = format_size(backup['size'])
            created = format_datetime(backup['created'])
            print(f"{name:<40} {size:<10} {created:<20}")
    
    except Exception as e:
        print(f"❌ Listing backups failed: {e}")
        sys.exit(1)

def cmd_restore(args):
    """Restore database from backup."""
    if not args.confirm:
        print("❌ Restoration requires --confirm flag for safety")
        print("   This operation will overwrite your current database!")
        sys.exit(1)
    
    protection = init_protection(args.database)
    
    try:
        # Find backup file
        backup_path = None
        if Path(args.backup).exists():
            backup_path = args.backup
        else:
            # Look in backup directory
            backup_dir = protection.backup_dir
            possible_path = backup_dir / args.backup
            if possible_path.exists():
                backup_path = str(possible_path)
            else:
                # Try to find by partial name
                matches = list(backup_dir.glob(f"*{args.backup}*"))
                if len(matches) == 1:
                    backup_path = str(matches[0])
                elif len(matches) > 1:
                    print(f"❌ Multiple backups match '{args.backup}':")
                    for match in matches:
                        print(f"   {match.name}")
                    sys.exit(1)
        
        if not backup_path:
            print(f"❌ Backup not found: {args.backup}")
            sys.exit(1)
        
        print(f"⚠️  About to restore database from: {backup_path}")
        print(f"   This will overwrite: {protection.db_path}")
        
        if not args.force:
            response = input("   Are you sure? (type 'yes' to confirm): ")
            if response.lower() != 'yes':
                print("❌ Restoration cancelled")
                sys.exit(0)
        
        protection.restore_backup(backup_path, confirm=True)
        print("✅ Database restored successfully!")
    
    except Exception as e:
        print(f"❌ Restoration failed: {e}")
        sys.exit(1)

def cmd_auto_backup(args):
    """Run automatic backup if needed."""
    protection = init_protection(args.database)
    
    try:
        protection.auto_backup_if_needed()
        print("✅ Auto backup check completed")
    except Exception as e:
        print(f"❌ Auto backup failed: {e}")
        sys.exit(1)

def cmd_config(args):
    """Show or update configuration."""
    protection = init_protection(args.database)
    
    if args.set:
        # Set configuration value
        key, value = args.set.split('=', 1)
        
        # Convert string values to appropriate types
        if value.lower() == 'true':
            value = True
        elif value.lower() == 'false':
            value = False
        elif value.isdigit():
            value = int(value)
        
        protection.config[key] = value
        protection._save_config()
        print(f"✅ Configuration updated: {key} = {value}")
    else:
        # Show current configuration
        print("⚙️  Database Protection Configuration")
        print("=" * 40)
        for key, value in protection.config.items():
            print(f"{key}: {value}")

def main():
    parser = argparse.ArgumentParser(
        description="Database Protection Management Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--database', '-d',
        default='finance.db',
        help='Database file path (default: finance.db)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Backup command
    backup_parser = subparsers.add_parser('backup', help='Create database backup')
    backup_parser.add_argument('--name', '-n', help='Custom backup name')
    backup_parser.set_defaults(func=cmd_backup)
    
    # Protect command
    protect_parser = subparsers.add_parser('protect', help='Apply database protection')
    protect_parser.set_defaults(func=cmd_protect)
    
    # Unprotect command
    unprotect_parser = subparsers.add_parser('unprotect', help='Remove database protection')
    unprotect_parser.set_defaults(func=cmd_unprotect)
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show protection status')
    status_parser.set_defaults(func=cmd_status)
    
    # List backups command
    list_parser = subparsers.add_parser('list-backups', help='List available backups')
    list_parser.set_defaults(func=cmd_list_backups)
    
    # Restore command
    restore_parser = subparsers.add_parser('restore', help='Restore from backup')
    restore_parser.add_argument('backup', help='Backup file name or path')
    restore_parser.add_argument('--confirm', action='store_true', 
                               help='Confirm restoration (required)')
    restore_parser.add_argument('--force', action='store_true',
                               help='Skip confirmation prompt')
    restore_parser.set_defaults(func=cmd_restore)
    
    # Auto backup command
    auto_parser = subparsers.add_parser('auto-backup', help='Run automatic backup check')
    auto_parser.set_defaults(func=cmd_auto_backup)
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Show or update configuration')
    config_parser.add_argument('--set', help='Set configuration value (key=value)')
    config_parser.set_defaults(func=cmd_config)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Run the selected command
    args.func(args)

if __name__ == '__main__':
    main() 