# ADR 005: Database Protection Framework

## Status
Accepted

## Context
Personal finance applications handle critical financial data that users cannot afford to lose. Common risks include:

1. **Accidental Deletion**: User accidentally deletes database file or runs destructive operations
2. **Data Corruption**: Hardware failures, power outages, or software bugs corrupt the database
3. **Failed Operations**: Database operations that fail partway through, leaving data in inconsistent state
4. **Concurrent Access**: Multiple application instances accessing the database simultaneously
5. **Human Error**: Mistakes during maintenance, migrations, or manual database operations

Traditional SQLite applications provide minimal protection against these scenarios. Users often lose months or years of financial data due to accidents that could have been prevented with proper safeguards.

## Decision
We will implement a comprehensive **Database Protection Framework** that provides multiple layers of defense against data loss through automated protection, backup systems, and safe operation patterns.

### Core Architecture

#### 1. Protection Layers
```
┌─────────────────────────────────────┐
│         Application Layer           │
├─────────────────────────────────────┤
│      Safe Operation Contexts        │
├─────────────────────────────────────┤
│       Database Protection           │
│   ┌─────────────────────────────┐   │
│   │     File Permissions        │   │
│   │     Process Locking         │   │
│   │     Integrity Checks        │   │
│   └─────────────────────────────┘   │
├─────────────────────────────────────┤
│        Backup System               │
│   ┌─────────────────────────────┐   │
│   │   Automatic Backups         │   │
│   │   Event-driven Backups      │   │
│   │   Backup Verification       │   │
│   └─────────────────────────────┘   │
├─────────────────────────────────────┤
│         Database Layer              │
└─────────────────────────────────────┘
```

#### 2. Framework Components

**Core Protection Module** (`utils/database_protection.py`)
- `DatabaseProtection` class: Main protection orchestrator
- `SafeDatabaseOperation` context manager: Automatic protection during operations
- Backup creation, verification, and restoration
- Configuration management and status monitoring

**Command Line Interface** (`scripts/protect_database.py`)
- Complete CLI for all protection operations
- Status checking, backup management, restoration
- Configuration updates and emergency recovery

**Application Integration** (`main.py`, `services/database.py`)
- Automatic protection initialization
- Integration with database service layer
- Safe operation contexts for all database operations

### Protection Mechanisms

#### 1. File-Level Protection
```python
# Read-only protection
os.chmod(db_path, current_mode & ~0o222)  # Remove write permissions

# Process locking
with database_lock():
    # Critical database operations
    pass
```

#### 2. Automatic Backup System
```python
# Time-based backups (every 6 hours)
protection.auto_backup_if_needed()

# Event-driven backups
with protection.safe_database_operation("critical_operation"):
    # Pre-operation backup created automatically
    database.perform_operation()
    # Post-operation backup created automatically
```

#### 3. Integrity Verification
```python
# SQLite integrity checks
cursor.execute("PRAGMA integrity_check")

# Backup verification with checksums
backup_checksum = calculate_checksum(backup_file)
original_checksum = calculate_checksum(original_file)
```

#### 4. Safe Operation Contexts
```python
# Automatic protection management
with db.safe_operation_context("data_migration"):
    # Protection temporarily removed
    # Backup created before operation
    db.perform_migration()
    # Backup created after operation
    # Protection reapplied
```

### Backup Strategy

#### Backup Types
1. **Automatic Time-based**: Every 6 hours (configurable)
2. **Event-driven**: Before critical operations
3. **Manual**: User-initiated with custom names
4. **Safety**: Pre-restoration safety backups

#### Backup Naming Convention
```
{purpose}_{timestamp}.db

Examples:
- auto_20250619_150000.db           # Automatic backup
- pre_migration_20250619_180000.db  # Pre-operation backup
- manual_backup_20250619_190000.db  # User-initiated backup
- pre_restore_safety_20250619_200000.db  # Safety backup
```

#### Retention Policy
- **Default**: 10 backups maximum, 30 days retention
- **Configurable**: Through `database_protection.json`
- **Automatic Cleanup**: Old backups removed automatically

### Safety Features

#### Multiple Confirmation Layers
1. **Code-level**: `confirm=True` parameter required
2. **CLI-level**: `--confirm` flag required
3. **Interactive**: User must type 'yes' to confirm
4. **Safety Backups**: Automatic backup before dangerous operations

#### Error Recovery
- **Automatic Rollback**: Failed operations revert changes
- **Safety Backups**: Pre-operation backups for manual recovery
- **Protection Reapplication**: Automatic protection restoration after operations
- **Lock Cleanup**: Automatic cleanup of process locks

## Implementation Details

### Configuration Management
```json
{
    "auto_backup_enabled": true,
    "backup_interval_hours": 6,
    "max_backups": 10,
    "protection_enabled": true,
    "checksum_verification": true,
    "backup_retention_days": 30
}
```

### Directory Structure
```
personal_finance/
├── finance.db                    # Main database (protected)
├── backups/                      # Automatic backup storage
├── archive/                      # Historical backup storage
├── database_protection.json     # Protection configuration
└── .finance.lock                # Temporary lock file
```

### Integration Points

#### Application Startup
```python
# Automatic protection initialization
protection = DatabaseProtection(config.database.db_name)
protection.auto_backup_if_needed()
protection.protect_database()
```

#### Database Service Integration
```python
class Database:
    def __init__(self):
        self.protection = DatabaseProtection()
    
    def safe_operation_context(self, operation_name):
        return self.protection.safe_database_operation(operation_name)
    
    def add_item(self, ...):
        with self.safe_operation_context("add_item"):
            # Database operation with automatic protection
```

#### Application Shutdown
```python
def on_app_close():
    protection.create_backup("app_shutdown")
    protection.protect_database()
```

### CLI Interface
```bash
# Status and monitoring
python scripts/protect_database.py status
python scripts/protect_database.py list-backups

# Backup management
python scripts/protect_database.py backup --name "weekly_backup"
python scripts/protect_database.py auto-backup

# Protection management
python scripts/protect_database.py protect
python scripts/protect_database.py unprotect

# Emergency recovery
python scripts/protect_database.py restore backup_name --confirm

# Configuration
python scripts/protect_database.py config
python scripts/protect_database.py config --set backup_interval_hours=12
```

## Consequences

### Positive
- **Data Loss Prevention**: Multiple layers of protection against accidental deletion
- **Automatic Operation**: No manual intervention required for basic protection
- **Comprehensive Recovery**: Multiple backup types and restoration options
- **User Confidence**: Users can operate without fear of losing financial data
- **Error Resilience**: Graceful handling of protection system failures
- **Audit Trail**: All protection operations logged for troubleshooting

### Negative
- **Storage Overhead**: Backup files consume disk space (configurable)
- **Performance Impact**: Small overhead from protection operations
- **Complexity**: Additional system components to maintain
- **Dependencies**: Framework requires proper integration to function

### Neutral
- **User Experience**: Transparent operation with optional manual control
- **Maintenance**: Regular backup cleanup and monitoring

## Alternative Approaches

### Rejected: Database-level Protection Only
**Approach**: Rely solely on SQLite features like WAL mode and transactions
**Rejection Reason**: Insufficient protection against file-level deletion or corruption

### Rejected: Manual Backup System
**Approach**: Require users to manually create backups
**Rejection Reason**: Users forget to create backups, leading to data loss

### Rejected: Cloud-only Backup
**Approach**: Store all backups in cloud storage
**Rejection Reason**: Requires internet connectivity and external service dependencies

## Validation

### Testing Strategy
- **Protection Integration**: Verify protection is automatically applied
- **Backup Creation**: Test all backup types and scenarios
- **Restoration Process**: Validate backup restoration with multiple confirmation
- **Error Handling**: Test protection system failures and recovery
- **Configuration**: Test all configuration options and changes

### Success Metrics
- **Zero Data Loss**: No user reports of lost financial data
- **Automatic Operation**: Protection works without user intervention
- **Fast Recovery**: Users can recover from accidents within minutes
- **Reliable Backups**: All backups are valid and restorable

## Related Decisions
- ADR 002: Database Schema - Protection framework works with multi-table schema
- ADR 004: Testing Architecture - Protection features are tested comprehensively

## Future Enhancements
- **Cloud Backup Integration**: Automatic upload of backups to cloud storage
- **Encryption**: Encrypt backup files for enhanced security
- **Incremental Backups**: More efficient backup storage for large databases
- **Monitoring Dashboard**: GUI interface for protection status and backup management
- **Remote Backup**: Network-based backup to remote servers
- **Backup Compression**: Reduce backup file sizes

## Documentation
- **Complete Documentation**: `docs/DATABASE_PROTECTION.md`
- **Quick Reference**: `PROTECTION_QUICK_START.md`
- **CLI Help**: Built-in help for all commands
- **Error Messages**: Descriptive error messages with recovery suggestions 