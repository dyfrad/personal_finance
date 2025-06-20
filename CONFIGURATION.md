# Configuration Guide

## Application Settings (`config.json`)
```json
{
    "database": {
        "db_name": "finance.db",
        "backup_dir": "backups",
        "max_connections": 5
    },
    "ui": {
        "theme": "dark",
        "window_size": [1024, 768],
        "refresh_interval": 60,
        "max_items_per_page": 50
    },
    "debug": false,
    "log_level": "INFO",
    "log_file": "app.log"
}
```

## Environment Variables
- `FINANCE_DB_PATH`: Override default database location
- `FINANCE_CONFIG_PATH`: Custom configuration file path
- `FINANCE_DEBUG`: Enable debug mode

## Version Configuration (`config/version.py`)
The application uses centralized version management. All version information is stored in `config/version.py`:

```python
__version__ = "0.2.0"                    # Current version
__app_name__ = "Personal Finance Manager" # Application name
__author__ = "Mohit Saharan"             # Author name
__author_email__ = "mohit@msaharan.com"  # Author email
__github_url__ = "https://github.com/msaharan/personal_finance"
__package_name__ = "personal-finance-manager"  # PyPI package name
__entry_point__ = "personal-finance-manager"   # Console script name
__description__ = "A sophisticated Python-based..."  # App description
```

**Important**: Only edit `config/version.py` directly if you need to change version information. For version updates, use the automated script: `python scripts/update_version.py <new_version>`.

## Database Protection Configuration

### Protection Settings (`database_protection.json`)
```json
{
    "protection_enabled": true,
    "auto_backup_enabled": true,
    "backup_interval_hours": 6,
    "max_backups": 10,
    "backup_on_startup": true,
    "backup_on_shutdown": true
}
```

### Protection Commands
```bash
# Check protection status
python main.py --check-protection
python scripts/protect_database.py status

# Create manual backup before important changes
python scripts/protect_database.py backup --name "before_important_change"

# Emergency recovery (if needed)
python scripts/protect_database.py list-backups
python scripts/protect_database.py restore backup_name --confirm
```

## UI Configuration

### Theme Settings
- **Available themes**: "dark", "light"
- **Default**: "dark"
- **Change**: Edit `theme` in `config.json`

### Window Settings
- **Default size**: 1024x768
- **Resizable**: Yes
- **Minimum size**: 800x600

### Display Settings
- **Refresh interval**: 60 seconds (stock data)
- **Items per page**: 50 (portfolio view)
- **Chart update**: Real-time on data change

## Logging Configuration

### Log Levels
- **DEBUG**: Detailed debugging information
- **INFO**: General application information
- **WARNING**: Warning messages
- **ERROR**: Error messages
- **CRITICAL**: Critical errors

### Log File Settings
- **Default location**: `app.log`
- **Rotation**: Automatic when file exceeds 10MB
- **Retention**: Last 5 log files kept
- **Format**: Timestamp, level, module, message

### Enable Debug Logging
```bash
# Command line
python main.py --debug

# Environment variable
export FINANCE_DEBUG=1

# Config file
{
    "debug": true,
    "log_level": "DEBUG"
}
``` 