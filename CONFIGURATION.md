# Configuration Guide

## Settings (`config.json`)

```json
{
    "database": {"db_name": "finance.db"},
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

- `FINANCE_DB_PATH`: Override database location
- `FINANCE_CONFIG_PATH`: Custom config file path  
- `FINANCE_DEBUG`: Enable debug mode

## Version Management

Version info is centralized in `config/version.py`. For updates, use:
```bash
python scripts/update_version.py <new_version>
```

## UI Options

- **Themes**: "dark" (default), "light"
- **Window size**: 1024x768 (default), resizable, minimum 800x600
- **Refresh interval**: 60 seconds for stock data
- **Items per page**: 50 in portfolio view

## Logging

**Log levels**: DEBUG, INFO (default), WARNING, ERROR, CRITICAL

**Enable debug mode**:
```bash
python main.py --debug              # Command line
export FINANCE_DEBUG=1              # Environment
{"debug": true, "log_level": "DEBUG"} # Config file
```

**Log file**: `app.log` (auto-rotates at 10MB, keeps 5 files) 