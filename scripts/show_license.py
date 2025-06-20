#!/usr/bin/env python3
"""
License Information Script

This script displays license information for the Personal Finance Manager application
and helps users understand their rights under the GNU Affero General Public License v3.0.

Copyright (c) 2025 Mohit Saharan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import sys
import argparse
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.version import __version__, __app_name__, __author__, __license__, __license_url__

def show_license_summary():
    """Display a summary of the license information."""
    print(f"{__app_name__} v{__version__}")
    print("=" * 50)
    print(f"Author: {__author__}")
    print(f"License: {__license__}")
    print(f"License URL: {__license_url__}")
    print()
    
    print("LICENSE SUMMARY")
    print("-" * 20)
    print("This software is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).")
    print()
    
    print("YOUR RIGHTS UNDER THIS LICENSE:")
    print("• Freedom to Use: You can use this software for any purpose")
    print("• Freedom to Study: You can examine the source code and understand how it works")
    print("• Freedom to Modify: You can modify the software to suit your needs")
    print("• Freedom to Share: You can distribute copies of the original or modified software")
    print("• Network Use: If you run a modified version on a server, you must provide the source code to users")
    print()
    
    print("KEY REQUIREMENTS:")
    print("• Source Code Availability: If you distribute this software, you must provide the complete source code")
    print("• Network Server Provision: If you run a modified version on a network server, you must provide the source code to users who interact with it")
    print("• License Preservation: Any modified versions must also be licensed under AGPL-3.0")
    print("• Copyright Notice: You must preserve all copyright notices and license information")
    print()
    
    print("For the complete license text, see the LICENSE file or visit:")
    print(__license_url__)

def show_full_license():
    """Display the full license text."""
    license_file = project_root / "LICENSE"
    if license_file.exists():
        with open(license_file, 'r', encoding='utf-8') as f:
            print(f.read())
    else:
        print("LICENSE file not found.")
        print("Please visit:", __license_url__)

def show_copyright_notice():
    """Display copyright information."""
    print("COPYRIGHT NOTICE")
    print("=" * 20)
    print(f"Copyright (c) 2025 {__author__}")
    print()
    print("All files in this repository are licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).")
    print()
    print("This program is free software: you can redistribute it and/or modify")
    print("it under the terms of the GNU Affero General Public License as published by")
    print("the Free Software Foundation, either version 3 of the License, or")
    print("(at your option) any later version.")
    print()
    print("This program is distributed in the hope that it will be useful,")
    print("but WITHOUT ANY WARRANTY; without even the implied warranty of")
    print("MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the")
    print("GNU Affero General Public License for more details.")
    print()
    print("You should have received a copy of the GNU Affero General Public License")
    print("along with this program.  If not, see <https://www.gnu.org/licenses/>.")

def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(
        description="Display license information for Personal Finance Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/show_license.py                    # Show license summary
  python scripts/show_license.py --full            # Show full license text
  python scripts/show_license.py --copyright       # Show copyright notice
  python scripts/show_license.py --all             # Show all license information
        """
    )
    
    parser.add_argument(
        '--full', '-f',
        action='store_true',
        help='Display the full license text'
    )
    
    parser.add_argument(
        '--copyright', '-c',
        action='store_true',
        help='Display copyright notice'
    )
    
    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Display all license information (summary, copyright, and full license)'
    )
    
    args = parser.parse_args()
    
    if args.all:
        show_license_summary()
        print("\n" + "=" * 80 + "\n")
        show_copyright_notice()
        print("\n" + "=" * 80 + "\n")
        show_full_license()
    elif args.full:
        show_full_license()
    elif args.copyright:
        show_copyright_notice()
    else:
        show_license_summary()

if __name__ == "__main__":
    main() 