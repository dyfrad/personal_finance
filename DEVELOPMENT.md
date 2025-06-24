# Development Guide

## Version Management

Version management is centralized in `config/version.py`. Use the update script for releases:

```bash
# Update version (updates config/version.py and CHANGELOG.md)
python scripts/update_version.py 0.3.0
```

**Manual updates**: Edit only `config/version.py` if needed.

**Import version info**:
```python
from config.version import __version__, __app_name__, __description__
```

## Development Workflow

```bash
# 1. Make changes
# 2. Update version for release
python scripts/update_version.py 0.3.0

# 3. Update CHANGELOG.md with actual changes
# 4. Commit and tag
git add .
git commit -m "feat: new feature in v0.3.0"
git tag v0.3.0
``` 