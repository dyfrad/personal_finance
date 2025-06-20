# Troubleshooting Guide

## Common Issues

### GUI Problems

#### Windows don't appear
- **Solution**: Try running `python gui.py` directly
- **Check**: Ensure virtual environment is activated
- **Alternative**: Use `python main.py` for full version

#### Theme issues
- **Solution**: Reset theme in config.json to "dark" or "light"
- **Config location**: `config.json` → `"ui"` → `"theme"`
- **Valid values**: "dark", "light"

#### Performance issues
- **Check**: Large datasets may cause slowdowns
- **Solution**: Consider filtering portfolio view
- **Tip**: Use pagination for large portfolios (50+ items)

### Database Issues

#### Database locked
- **Cause**: Multiple instances of the application running
- **Solution**: Close all instances of the application
- **Check**: Look for background processes
- **Force quit**: Use task manager if needed

#### Corrupt database
- **Solution**: Check backups in the `backups/` directory
- **Command**: `python scripts/protect_database.py list-backups`
- **Restore**: `python scripts/protect_database.py restore backup_name --confirm`
- **Prevention**: Regular backups run automatically every 6 hours

#### Missing data
- **Check**: Verify the correct database file is being used
- **Location**: Default is `finance.db` in project root
- **Override**: Use `FINANCE_DB_PATH` environment variable
- **Verify**: Check database exists and has correct permissions

#### Database protection errors
- **Check status**: `python scripts/protect_database.py status`
- **Common cause**: File permissions or disk space
- **Solution**: Ensure write permissions in backup directory
- **Alternative**: Disable protection temporarily in config

#### Accidental deletion
- **Solution**: Restore from automatic backups
- **Command**: `python scripts/protect_database.py restore backup_name --confirm`
- **List backups**: `python scripts/protect_database.py list-backups`
- **Prevention**: Multiple confirmation layers prevent accidents

### Installation Issues

#### Module not found
- **Cause**: Virtual environment not activated or missing dependencies
- **Solution**: Ensure virtual environment is activated
- **Install**: `pip install -r requirements.txt`
- **Verify**: `python -c "import tkinter; print('GUI available')"`

#### Permission errors
- **Cause**: Insufficient write permissions
- **Solution**: Check write permissions in the installation directory
- **Alternative**: Install in user directory with `pip install --user`
- **Windows**: Run as administrator if needed

#### Python version
- **Requirement**: Python 3.7 or higher
- **Check**: `python --version`
- **Solution**: Upgrade Python or use pyenv/conda
- **Alternative**: Use Python 3.8+ for best compatibility

### Application Errors

#### Startup errors
- **Check logs**: Review `app.log` for detailed error information
- **Common causes**: Missing configuration files, database corruption
- **Solution**: Restore configuration from git or create fresh config

#### Import errors
- **Check**: All required packages installed
- **Solution**: `pip install -r requirements.txt`
- **Alternative**: Reinstall with `pip install -e .`

#### Data import/export issues
- **Format**: Ensure CSV files have correct headers
- **Encoding**: Use UTF-8 encoding for CSV files
- **Size**: Large files may take time to process

### Network and Data Issues

#### Stock data not updating
- **Cause**: Network connectivity or API limits
- **Check**: Internet connection active
- **Alternative**: Manual price entry for offline use
- **Retry**: Data fetching retries automatically

#### Chart display problems
- **Cause**: Matplotlib backend issues
- **Solution**: Update matplotlib: `pip install --upgrade matplotlib`
- **Alternative**: Use different backend in config

## Getting Help

### Diagnostic Steps
1. **Check logs**: Review `app.log` for error details
2. **Run tests**: `python -m pytest tests/` to verify system integrity
3. **Check config**: Verify `config.json` has valid settings
4. **Database status**: `python main.py --check-protection`

### Information to Collect
When reporting issues, include:
- Operating system and version
- Python version (`python --version`)
- Error messages from logs
- Steps to reproduce the problem
- Recent changes or updates

### Recovery Procedures

#### Complete application reset
```bash
# 1. Backup current database
python scripts/protect_database.py backup --name "before_reset"

# 2. Create fresh configuration
cp config.json config.json.backup
# Edit config.json with default values

# 3. Test with minimal setup
python gui.py  # Simple GUI without protection

# 4. Restore from backup if needed
python scripts/protect_database.py restore backup_name --confirm
```

#### Emergency database recovery
```bash
# List available backups
python scripts/protect_database.py list-backups

# Restore specific backup
python scripts/protect_database.py restore backup_name --confirm

# Verify data integrity
python -c "from database import Database; db = Database(); print(len(db.get_all_items()))"
```

### Additional Resources
- Check Architectural Decision Records in `docs/adr/`
- Review `PROTECTION_QUICK_START.md` for database protection
- See `DEVELOPMENT.md` for development-specific issues
- Consult `CONFIGURATION.md` for configuration problems 