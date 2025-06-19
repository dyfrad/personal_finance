# 🔒 Database Protection Quick Start

## Essential Commands

### Check Status
```bash
python scripts/protect_database.py status
python main.py --check-protection
```

### Create Backup
```bash
# Quick backup
python scripts/protect_database.py backup

# Named backup  
python scripts/protect_database.py backup --name "before_important_change"

# Backup before starting app
python main.py --backup
```

### Protection Management
```bash
# Apply protection (makes database read-only)
python scripts/protect_database.py protect

# Remove protection (for operations)
python scripts/protect_database.py unprotect

# List all backups
python scripts/protect_database.py list-backups
```

### Emergency Recovery
```bash
# List available backups
python scripts/protect_database.py list-backups

# Restore from backup (REQUIRES CONFIRMATION)
python scripts/protect_database.py restore backup_name --confirm
```

## 🚨 CRITICAL SAFETY FEATURES

1. **Database is automatically protected (read-only) to prevent accidental deletion**
2. **Automatic backups every 6 hours** 
3. **Manual backup creation before risky operations**
4. **Multiple confirmation required for restoration**
5. **Safety backups created before restoration attempts**

## 🛡️ What's Protected

- ✅ **Main database (`finance.db`)** - Your financial data
- ✅ **Automatic time-based backups** (every 6 hours)
- ✅ **Operation-triggered backups** (before major changes)
- ✅ **Application startup/shutdown backups**

## 📁 File Locations

```
personal_finance/
├── finance.db                    # Main database (PROTECTED)
├── backups/                      # Auto backups (PRESERVED)
│   ├── auto_20250619_120000.db
│   └── manual_backup_20250619_150000.db
├── archive/                      # Historical backups
└── database_protection.json     # Protection settings
```

## ⚡ Quick Recovery

If you lose your database:

1. **Check backups**: `python scripts/protect_database.py list-backups`
2. **Pick latest**: Look for most recent backup
3. **Restore**: `python scripts/protect_database.py restore latest_backup --confirm`
4. **Verify**: Start app and check your data

## 🔧 Configuration

View/change settings:
```bash
# View current settings
python scripts/protect_database.py config

# Change backup frequency (hours)
python scripts/protect_database.py config --set backup_interval_hours=12

# Change max backup count
python scripts/protect_database.py config --set max_backups=20
```

## ⚠️ Important Notes

- **Protection is AUTOMATIC** - your database is protected by default
- **Backups happen AUTOMATICALLY** - no manual intervention needed
- **Restoration requires CONFIRMATION** - prevents accidents
- **Application handles protection** - works seamlessly with GUI

## 💡 Best Practices

1. **Let protection run automatically** - don't disable unless necessary
2. **Create named backups before major changes**: 
   `python scripts/protect_database.py backup --name "before_data_import"`
3. **Check status regularly**: 
   `python scripts/protect_database.py status`
4. **Test restoration occasionally** to ensure backups work

## 🆘 Emergency Contacts

- Check logs: `app.log`
- Debug mode: `python main.py --debug`
- Protection status: `python main.py --check-protection`

**Your financial data is now AUTOMATICALLY PROTECTED against accidental deletion!** 🛡️ 