# Development Guide

## Version Management

The application uses centralized version management to eliminate inconsistencies. All version information is stored in `config/version.py`:

### Quick Version Update
```bash
# Update version (updates config/version.py and CHANGELOG.md)
python scripts/update_version.py 0.3.0
```

### What Gets Updated Automatically
- **`config/version.py`** - Central version information
- **`CHANGELOG.md`** - New version entry with template
- **`setup.py`** - Package version (imported from config/version.py)
- **`main.py`** - Application startup version (imported from config/version.py)

### Manual Version Update (if needed)
If you need to update version manually, only edit `config/version.py`:
```python
__version__ = "0.3.0"
__app_name__ = "Personal Finance Manager"
__author__ = "Mohit Saharan"
__author_email__ = "mohit@msaharan.com"
```

### Version Information Available
```python
from config.version import (
    __version__, __app_name__, __description__, 
    __author__, __author_email__, __github_url__,
    __package_name__, __entry_point__
)
```

### Benefits
- **Single Source of Truth**: Version only exists in one place
- **No Inconsistencies**: Impossible to have different versions in different files
- **Automated Updates**: One command updates everything
- **Validation**: Ensures proper semantic versioning format (X.Y.Z)
- **Documentation**: Automatically updates changelog

## Development Workflow
```bash
# 1. Make your changes
# 2. Update version when ready for release
python scripts/update_version.py 0.3.0

# 3. Update CHANGELOG.md with actual changes (not just version bump)
# 4. Test the application
python -m pytest tests/ -v

# 5. Commit changes
git add .
git commit -m "feat: new feature in v0.3.0"

# 6. Tag release (optional)
git tag v0.3.0
```

## Testing

### Test Coverage
The application includes **33 comprehensive tests** covering:

- **Critical App Functionality** (13 tests): Database operations, purchase system, data persistence
- **Database Layer** (9 tests): CRUD operations, error handling, data integrity
- **Data Models** (11 tests): Item/Purchase objects, calculations, serialization

### Running Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test categories
python -m pytest tests/test_app_critical.py -v
python -m pytest tests/test_database.py -v
python -m pytest tests/test_models.py -v

# Quick test summary
python -m pytest tests/ -q
```

### Test Results
Current status: **33/33 tests passing (100% success rate)**

For detailed test coverage information, see `tests/TEST_COVERAGE_SUMMARY.md`. 