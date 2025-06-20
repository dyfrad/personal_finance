# Personal Finance Manager

A sophisticated Python-based personal finance management application that helps you track and manage your financial portfolio with advanced features for investments, inventory, and expenses.

**PRIVATE PROJECT**: This is a personal finance application designed for individual use. All data is stored locally and privately.

## Application Overview
![Personal Finance Manager Dashboard](docs/images/dashboard_0.2.0.png)

The dashboard provides a comprehensive view of your financial portfolio with:
- Real-time stock performance tracking with technical indicators
- Expense monitoring with detailed visualization
- Quick access controls for portfolio management
- Reserved space for future feature expansion

## Key Features

### Portfolio Management
- **Investment Tracking**: Manage stocks, bonds, crypto, real estate, and gold with multiple purchase tracking
- **Inventory Management**: Track appliances, electronics, furniture, transportation, home improvements, savings, and collectibles
- **Expense Tracking**: Record and monitor expenses with simplified entry forms
- **Multi-Purchase Support**: Track multiple purchases for investment items with detailed transaction history

### Advanced Analytics
- **Performance Graphs**: Real-time stock performance visualization with technical indicators
- **Technical Analysis**: Moving averages (SMA, EMA), RSI, MACD indicators
- **Interactive Charts**: Hover details, comparison features, and historical data analysis
- **Profit/Loss Calculations**: Accurate financial calculations for all item types

### Modern User Interface
- **Four-Quadrant Dashboard**: Organized layout with stock performance, expenses, and action buttons
- **Google Material Design**: Professional theme with light/dark mode support
- **Category-Specific Forms**: Tailored input forms for investments, inventory, and expenses
- **Responsive Design**: Optimized for different screen sizes and platforms

### Data Management
- **Multiple Database Tables**: Separate tables for investments, inventory, and expenses
- **Purchase History**: Detailed transaction tracking with table-specific context
- **Export/Import**: CSV export functionality for data portability
- **Data Integrity**: Comprehensive validation and error handling
- **Database Protection**: Automatic protection against accidental deletion with read-only permissions
- **Automatic Backups**: Every 6 hours + event-driven backups with configurable retention
- **Emergency Recovery**: Multiple confirmation layers and safety backups for restoration

### Quality Assurance
- **33 Comprehensive Tests**: Complete test coverage for critical functionality
- **Database Protection Framework**: Comprehensive safeguards against accidental data loss
- **Automatic Backup System**: Time-based and event-driven backups with integrity verification
- **Error Handling**: Graceful degradation for database and network issues
- **Data Validation**: Input validation to prevent data corruption
- **Performance Testing**: Verified with large portfolios (50+ items, 20+ purchases per item)

## Development

### Version Management
The application uses centralized version management to eliminate inconsistencies. All version information is stored in `config/version.py`:

#### Quick Version Update
```bash
# Update version (updates config/version.py and CHANGELOG.md)
python scripts/update_version.py 0.3.0
```

#### What Gets Updated Automatically
- **`config/version.py`** - Central version information
- **`CHANGELOG.md`** - New version entry with template
- **`setup.py`** - Package version (imported from config/version.py)
- **`main.py`** - Application startup version (imported from config/version.py)

#### Manual Version Update (if needed)
If you need to update version manually, only edit `config/version.py`:
```python
__version__ = "0.3.0"
__app_name__ = "Personal Finance Manager"
__author__ = "Mohit Saharan"
__author_email__ = "mohit@msaharan.com"
```

#### Version Information Available
```python
from config.version import (
    __version__, __app_name__, __description__, 
    __author__, __author_email__, __github_url__,
    __package_name__, __entry_point__
)
```

#### Benefits
- **Single Source of Truth**: Version only exists in one place
- **No Inconsistencies**: Impossible to have different versions in different files
- **Automated Updates**: One command updates everything
- **Validation**: Ensures proper semantic versioning format (X.Y.Z)
- **Documentation**: Automatically updates changelog

### Development Workflow
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

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Quick Start
```bash
# Clone the repository (private)
git clone <your-private-repo-url>
cd personal_finance

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the application
pip install -e .

# Run the application (choose one):
personal-finance-manager

# DEVELOPER: Run from source with CLI options
python main.py --help

# SIMPLE: GUI only (no protection, for testing)
python gui.py
```

### Alternative Installation
```bash
# Install dependencies directly
pip install -r requirements.txt

# Run from source (choose one):
python main.py             # Full version with database protection
python gui.py              # Simple GUI only
```

### Database Protection (Automatic)
Your database is automatically protected against accidental deletion:

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

**Note**: The protection framework runs automatically - no manual setup required! See [PROTECTION_QUICK_START.md](PROTECTION_QUICK_START.md) for details.

## Usage Guide

### Getting Started
1. **Launch the Application**: Choose your preferred method:
   - **Full Version**: `personal-finance-manager` or `python main.py` (includes database protection)
   - **Simple Version**: `python gui.py` (GUI only, no protection features)
2. **Dashboard Overview**: The main dashboard shows four key areas:
   - **Top Left**: Stock performance graph with technical indicators
   - **Top Right**: Quick action buttons (View Portfolio, Add Items)
   - **Bottom Left**: Expenses tracking and visualization
   - **Bottom Right**: Additional controls and features

### Managing Your Portfolio

#### Adding Items
- **Investments** (Stocks, Bonds, Crypto): Multiple purchase tracking with shares/units and price per unit
- **Inventory** (Electronics, Furniture, etc.): Single or multiple purchase tracking
- **Expenses**: Simplified form with amount and date only

#### Viewing and Editing
- **Portfolio View**: Comprehensive table with category-specific columns
- **Edit Items**: Update item details with category-appropriate forms
- **Purchase History**: View and add purchases for investment items
- **Performance Analysis**: Interactive graphs with technical indicators

#### Advanced Features
- **Technical Analysis**: RSI, MACD, moving averages for stock performance
- **Data Export**: Export portfolio data to CSV format
- **Theme Switching**: Toggle between light and dark modes
- **Real-time Updates**: Live stock data integration (when available)

## Architecture

### Project Structure
```
personal_finance/
├── models/                 # Data models (Item, Purchase)
│   ├── item.py            # Core Item class
│   └── purchase.py        # Purchase tracking
├── services/              # Business logic layer
│   └── database.py        # Database service (clean API)
├── config/                # Configuration management
│   ├── settings.py        # Application settings
│   └── version.py         # Centralized version information
├── utils/                 # Utility functions
│   ├── logging.py         # Logging configuration
│   └── database_protection.py  # Database protection framework
├── scripts/               # Command-line utilities
│   ├── protect_database.py     # Database protection CLI
│   └── update_version.py       # Version management utility
├── tests/                 # Comprehensive test suite
│   ├── test_app_critical.py      # Critical functionality tests
│   ├── test_database.py          # Database operation tests
│   ├── test_models.py             # Data model tests
│   └── TEST_COVERAGE_SUMMARY.md  # Test documentation
├── docs/                  # Documentation and ADRs
│   ├── adr/              # Architectural Decision Records
│   └── DATABASE_PROTECTION.md   # Protection framework docs
├── backups/               # Automatic database backups
├── archive/               # Historical backup storage
├── main.py               # Application entry point and core logic
├── gui.py                # Complete GUI application (1,600+ lines)
├── database.py           # Legacy database operations
├── config.json           # Runtime configuration
├── database_protection.json    # Protection framework config
└── PROTECTION_QUICK_START.md   # Protection quick reference
```

### Database Schema
- **Investments Table**: Stocks, bonds, crypto, real estate, gold
- **Inventory Table**: Physical items and savings accounts
- **Expenses Table**: Expense tracking and management
- **Purchases Table**: Transaction history with table context (`table_name` field)

### Technology Stack
- **GUI Framework**: Tkinter with ttk for modern widgets
- **Database**: SQLite with multiple table architecture
- **Charting**: Matplotlib with TkAgg backend
- **Data Analysis**: yfinance for stock data, ta for technical analysis
- **Testing**: pytest with 33 comprehensive tests
- **Configuration**: JSON-based config management

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

## Configuration

### Application Settings (`config.json`)
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

### Environment Variables
- `FINANCE_DB_PATH`: Override default database location
- `FINANCE_CONFIG_PATH`: Custom configuration file path
- `FINANCE_DEBUG`: Enable debug mode

### Version Configuration (`config/version.py`)
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

## Troubleshooting

### Common Issues

#### GUI Problems
- **Windows don't appear**: Try running `python gui.py` directly
- **Theme issues**: Reset theme in config.json to "dark" or "light"
- **Performance issues**: Check if you have large datasets, consider filtering

#### Database Issues
- **Database locked**: Close all instances of the application
- **Corrupt database**: Check backups in the `backups/` directory with `python scripts/protect_database.py list-backups`
- **Missing data**: Verify the correct database file is being used
- **Database protection errors**: Check `python scripts/protect_database.py status`
- **Accidental deletion**: Restore from automatic backups with `python scripts/protect_database.py restore backup_name --confirm`

#### Installation Issues
- **Module not found**: Ensure virtual environment is activated
- **Permission errors**: Check write permissions in the installation directory
- **Python version**: Verify Python 3.7+ is installed

### Getting Help
1. Check the logs in `app.log` for detailed error information
2. Run tests to verify system integrity: `python -m pytest tests/`
3. Review the Architectural Decision Records in `docs/adr/`

## Documentation

### Architectural Decision Records
- [ADR 001: Flexible Item Model](docs/adr/001-flexible-item-model.md)
- [ADR 002: Database Schema](docs/adr/002-database-schema.md)
- [ADR 003: GUI Design](docs/adr/003-gui-design.md)
- [ADR 004: Testing Architecture](docs/adr/004-testing-architecture.md)
- [ADR 005: Database Protection Framework](docs/adr/005-database-protection-framework.md)

### Additional Resources
- `docs/DATABASE_PROTECTION.md`: Complete database protection framework documentation
- `PROTECTION_QUICK_START.md`: Essential database protection commands
- `tests/TEST_COVERAGE_SUMMARY.md`: Comprehensive test documentation
- `DATABASE_MIGRATION.md`: Database migration guide (if applicable)
- `CHANGELOG.md`: Version history and updates
- `scripts/update_version.py`: Version management utility for automated version updates

## License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

### License Summary
- **Freedom to Use**: You can use this software for any purpose
- **Freedom to Study**: You can examine the source code and understand how it works
- **Freedom to Modify**: You can modify the software to suit your needs
- **Freedom to Share**: You can distribute copies of the original or modified software
- **Network Use**: If you run a modified version on a server, you must provide the source code to users

### Key Requirements
- **Source Code Availability**: If you distribute this software, you must provide the complete source code
- **Network Server Provision**: If you run a modified version on a network server, you must provide the source code to users who interact with it
- **License Preservation**: Any modified versions must also be licensed under AGPL-3.0
- **Copyright Notice**: You must preserve all copyright notices and license information

### Full License Text
The complete license text is available in the [LICENSE](LICENSE) file and online at [https://www.gnu.org/licenses/agpl-3.0.html](https://www.gnu.org/licenses/agpl-3.0.html).

### Copyright
Copyright (c) 2025 Mohit Saharan

## Acknowledgments

- **[yfinance](https://github.com/ranaroussi/yfinance)**: Real-time stock data
- **[ta](https://github.com/bukosabino/ta)**: Technical analysis indicators
- **[matplotlib](https://matplotlib.org/)**: Advanced plotting and visualization
- **[tkinter](https://docs.python.org/3/library/tkinter.html)**: Cross-platform GUI framework
- **[pytest](https://pytest.org/)**: Comprehensive testing framework

## Privacy & Security

This is a **private personal finance application** designed for individual use:

- **Local Data Storage**: All financial data is stored locally on your device
- **No Cloud Services**: No data is transmitted to external servers
- **Privacy First**: Your financial information remains completely private
- **Data Sovereignty**: You maintain full control over your data
- **Automatic Backups**: Local backup system protects against data loss

---

**Built with love for personal finance management**
