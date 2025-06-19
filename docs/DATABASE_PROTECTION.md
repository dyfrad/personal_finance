# Database Protection Framework

## Overview

The Database Protection Framework provides comprehensive safeguards against accidental deletion, corruption, or data loss in your personal finance application. It implements multiple layers of protection including automatic backups, file permissions, integrity checks, and safe operation contexts.

## Features

### Core Protection
- **Read-only Protection**: Makes database file read-only to prevent accidental writes
- **File Locking**: Prevents concurrent access during critical operations
- **Integrity Verification**: SQLite PRAGMA integrity checks before operations
- **Checksum Validation**: SHA256 verification of backup files

### Automatic Backups
- **Time-based Backups**: Automatic backups every 6 hours (configurable)
- **Event-driven Backups**: Backups before critical operations
- **Retention Policy**: Automatic cleanup of old backups
- **Backup Verification**: Ensures backup integrity before use

### Safe Operations
- **Context Managers**: Safe database operation wrappers
- **Pre/Post Operation Backups**: Automatic backup creation around operations
- **Rollback Capability**: Easy restoration from backups
- **Error Recovery**: Automatic reversion on operation failures

## Quick Start

### Command Line Interface

```bash
# Check protection status
python scripts/protect_database.py status

# Create a manual backup
python scripts/protect_database.py backup --name "before_important_change"

# Apply database protection
python scripts/protect_database.py protect

# Remove protection temporarily
python scripts/protect_database.py unprotect

# List all backups
python scripts/protect_database.py list-backups

# Restore from backup (requires confirmation)
python scripts/protect_database.py restore backup_name --confirm
```

### Application Integration

```python
from utils.database_protection import DatabaseProtection, safe_operation

# Initialize protection
protection = DatabaseProtection("finance.db")

# Create manual backup
backup_path = protection.create_backup("before_migration")

# Safe operation context
with protection.safe_database_operation("data_migration"):
    # Your database operations here
    # Automatic backup created before and after
    pass

# Quick backup function
from utils.database_protection import create_backup
backup_path = create_backup()
```

## Application Startup Integration

The framework is automatically integrated into the main application:

```bash
# Start with automatic backup
python main.py --backup

# Check protection status
python main.py --check-protection

# Debug mode with protection
python main.py --debug
```

## Configuration

The protection framework uses `database_protection.json` for configuration:

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

### Configuration Options

| Setting | Default | Description |
|---------|---------|-------------|
| `auto_backup_enabled` | `true` | Enable automatic time-based backups |
| `backup_interval_hours` | `6` | Hours between automatic backups |
| `max_backups` | `10` | Maximum number of backups to keep |
| `protection_enabled` | `true` | Enable database protection features |
| `checksum_verification` | `true` | Verify backup integrity with checksums |
| `backup_retention_days` | `30` | Days to keep backups before cleanup |

### Modify Configuration

```bash
# View current configuration
python scripts/protect_database.py config

# Update settings
python scripts/protect_database.py config --set auto_backup_enabled=true
python scripts/protect_database.py config --set backup_interval_hours=12
python scripts/protect_database.py config --set max_backups=5
```

## Directory Structure

```
personal_finance/
├── finance.db                    # Main database (protected)
├── backups/                      # Automatic backups directory
│   ├── finance_backup_20250619_150000.db
│   ├── auto_20250619_160000.db
│   └── manual_startup_20250619_170000.db
├── archive/                      # Archived historical backups
├── database_protection.json     # Protection configuration
└── .finance.lock                # Lock file (temporary)
```

## Backup Types

### Automatic Backups
- **Time-based**: Created every N hours based on configuration
- **Event-driven**: Created before critical operations
- **Startup/Shutdown**: Created when application starts/stops

### Manual Backups
- **Named Backups**: Custom names for specific purposes
- **Quick Backups**: Timestamped backups for immediate use
- **Pre-operation**: Created before manual database operations

### Backup Naming Convention
```
{purpose}_{timestamp}.db

Examples:
- auto_20250619_150000.db           # Automatic backup
- manual_startup_20250619_170000.db # Manual startup backup
- pre_migration_20250619_180000.db  # Pre-operation backup
- before_update_20250619_190000.db  # Named backup
```

## Advanced Usage

### Safe Database Operations

```python
from utils.database_protection import DatabaseProtection

protection = DatabaseProtection()

# Context manager for safe operations
with protection.safe_database_operation("bulk_update"):
    # Database operations here are automatically protected
    # - Pre-operation backup created
    # - Protection temporarily removed
    # - Post-operation backup created
    # - Protection reapplied
    db.update_many_items(data)
```

### Custom Backup Strategies

```python
# Create backup with custom name
backup_path = protection.create_backup("before_data_import")

# Check if backup is needed
protection.auto_backup_if_needed()

# Get backup information
backups = protection.list_backups()
for backup in backups:
    print(f"{backup['name']}: {backup['size']} bytes")
```

### Restoration and Recovery

```python
# List available backups
backups = protection.list_backups()

# Restore from specific backup (creates safety backup first)
protection.restore_backup("backup_name.db", confirm=True)

# Restore from command line with confirmation
python scripts/protect_database.py restore backup_name --confirm --force
```

## Safety Features

### Multiple Confirmation Layers
1. **Explicit Confirmation**: Restoration requires `confirm=True` parameter
2. **Command Line Flags**: `--confirm` flag required for CLI restoration
3. **Interactive Prompts**: User must type 'yes' to confirm dangerous operations
4. **Safety Backups**: Automatic backup before restoration attempts

### Error Recovery
- **Automatic Rollback**: Failed operations automatically revert changes
- **Safety Backups**: Pre-operation backups for manual recovery
- **Integrity Checks**: Database validation before and after operations
- **Lock Management**: Automatic cleanup of file locks

### Protection Mechanisms
- **File Permissions**: Read-only database file protection
- **Process Locking**: Prevents concurrent dangerous operations
- **Checksum Verification**: Ensures backup file integrity
- **Atomic Operations**: All-or-nothing database changes

## Monitoring and Status

### Status Information
```bash
python scripts/protect_database.py status
```

Shows:
- Database path and size
- Protection status (enabled/disabled)
- Auto backup status
- Backup count and latest backup
- Last backup timestamp

### Backup Management
```bash
# List all backups with details
python scripts/protect_database.py list-backups

# Create manual backup
python scripts/protect_database.py backup --name "weekly_backup"

# Force automatic backup check
python scripts/protect_database.py auto-backup
```

## Troubleshooting

### Common Issues

#### Protection Not Available
```
Database protection not available
```
**Solution**: Install missing dependencies or check import paths

#### Database Locked
```
Database is locked by another process
```
**Solution**: Close other application instances or wait for lock to clear

#### Backup Verification Failed
```
Backup verification failed: checksums don't match
```
**Solution**: Check disk space and file permissions, retry backup

#### Permission Denied
```
Permission denied: Cannot write to database
```
**Solution**: Remove protection temporarily with `unprotect` command

### Recovery Procedures

#### Lost Database File
1. List available backups: `python scripts/protect_database.py list-backups`
2. Restore latest backup: `python scripts/protect_database.py restore latest --confirm`
3. Verify data integrity after restoration

#### Corrupted Database
1. Check integrity: Run application with `--debug` flag
2. Restore from backup: Use most recent valid backup
3. Re-import data if necessary

#### Configuration Issues
1. Reset configuration: Delete `database_protection.json`
2. Restart application to regenerate default config
3. Adjust settings as needed

## Security Considerations

### File Permissions
- Database files are set to read-only when protected
- Backup directory should have restricted access
- Configuration files contain no sensitive data

### Backup Security
- Backups contain full database copies
- Store backups in secure locations
- Consider encryption for sensitive financial data
- Regular cleanup of old backups

### Access Control
- Protection framework requires file system access
- Lock files prevent concurrent access
- Database operations are logged for audit

## Best Practices

### Regular Maintenance
1. **Monitor Backup Status**: Check backup count and dates regularly
2. **Test Restoration**: Periodically test backup restoration process
3. **Cleanup Old Backups**: Configure appropriate retention policies
4. **Update Configuration**: Adjust settings based on usage patterns

### Safe Operations
1. **Always Use Protection**: Keep protection enabled except during operations
2. **Create Named Backups**: Use descriptive names for important backups
3. **Verify After Changes**: Check data integrity after major operations
4. **Plan for Recovery**: Know your restoration procedures

### Performance Optimization
1. **Backup Frequency**: Balance protection vs. performance
2. **Retention Policies**: Keep only necessary backups
3. **Storage Location**: Use fast storage for backup directory
4. **Cleanup Schedule**: Regular cleanup of old files

## Integration with Application

The protection framework is seamlessly integrated:

- **Automatic Initialization**: Protection starts with the application
- **Safe Operation Contexts**: Database service uses protection automatically
- **Backup on Shutdown**: Automatic backup when application closes
- **Error Handling**: Protection reapplied even on application errors

This ensures your financial data is always protected without requiring manual intervention.

## Support

For issues with the database protection framework:

1. Check the application logs: `app.log`
2. Verify configuration: `python scripts/protect_database.py config`
3. Test with debug mode: `python main.py --debug`
4. Review backup status: `python scripts/protect_database.py status`

The framework is designed to fail safely - if protection fails, the application continues to work normally, just without the additional safety features. 