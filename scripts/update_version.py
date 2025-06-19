#!/usr/bin/env python3
"""
Version update utility for Personal Finance Manager.

This script helps update the version number in the centralized location.
Usage: python scripts/update_version.py <new_version>
"""

import sys
import re
from pathlib import Path

def update_version(new_version):
    """Update version in config/version.py and CHANGELOG.md."""
    
    # Validate version format (semantic versioning)
    if not re.match(r'^\d+\.\d+\.\d+$', new_version):
        print(f"Error: Invalid version format '{new_version}'. Use format: X.Y.Z")
        sys.exit(1)
    
    # Update config/version.py
    version_file = Path("config/version.py")
    if not version_file.exists():
        print(f"Error: {version_file} not found")
        sys.exit(1)
    
    with open(version_file, 'r') as f:
        content = f.read()
    
    # Update version in version.py
    content = re.sub(
        r'__version__ = "[^"]*"',
        f'__version__ = "{new_version}"',
        content
    )
    
    with open(version_file, 'w') as f:
        f.write(content)
    
    print(f"✅ Updated version to {new_version} in config/version.py")
    
    # Update CHANGELOG.md
    changelog_file = Path("CHANGELOG.md")
    if changelog_file.exists():
        with open(changelog_file, 'r') as f:
            content = f.read()
        
        # Add new version entry at the top
        new_entry = f"""## [{new_version}] - {Path.cwd().name}
### Added
- Version update to {new_version}

### Changed
- Updated version number

"""
        
        # Insert after the header
        lines = content.split('\n')
        insert_index = 0
        for i, line in enumerate(lines):
            if line.startswith('## ['):
                insert_index = i
                break
        
        lines.insert(insert_index, new_entry.rstrip())
        
        with open(changelog_file, 'w') as f:
            f.write('\n'.join(lines))
        
        print(f"✅ Added version {new_version} entry to CHANGELOG.md")
    
    print(f"\n🎉 Version updated to {new_version}!")
    print("📝 Don't forget to:")
    print("   - Update CHANGELOG.md with actual changes")
    print("   - Commit your changes")
    print("   - Tag the release if needed")

def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/update_version.py <new_version>")
        print("Example: python scripts/update_version.py 0.3.0")
        sys.exit(1)
    
    new_version = sys.argv[1]
    update_version(new_version)

if __name__ == "__main__":
    main() 