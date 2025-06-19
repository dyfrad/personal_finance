# Personal Finance Manager

A sophisticated Python-based personal finance management application that helps you track and manage your financial portfolio with advanced features for investments, inventory, and expenses.

## ✨ Key Features

### 📊 Portfolio Management
- **Investment Tracking**: Manage stocks, bonds, crypto, real estate, and gold with multiple purchase tracking
- **Inventory Management**: Track appliances, electronics, furniture, transportation, home improvements, savings, and collectibles
- **Expense Tracking**: Record and monitor expenses with simplified entry forms
- **Multi-Purchase Support**: Track multiple purchases for investment items with detailed transaction history

### 📈 Advanced Analytics
- **Performance Graphs**: Real-time stock performance visualization with technical indicators
- **Technical Analysis**: Moving averages (SMA, EMA), RSI, MACD indicators
- **Interactive Charts**: Hover details, comparison features, and historical data analysis
- **Profit/Loss Calculations**: Accurate financial calculations for all item types

### 🎨 Modern User Interface
- **Four-Quadrant Dashboard**: Organized layout with stock performance, expenses, and action buttons
- **Google Material Design**: Professional theme with light/dark mode support
- **Category-Specific Forms**: Tailored input forms for investments, inventory, and expenses
- **Responsive Design**: Optimized for different screen sizes and platforms

### 🔧 Data Management
- **Multiple Database Tables**: Separate tables for investments, inventory, and expenses
- **Purchase History**: Detailed transaction tracking with table-specific context
- **Export/Import**: CSV export functionality for data portability
- **Data Integrity**: Comprehensive validation and error handling

### 🛡️ Quality Assurance
- **33 Comprehensive Tests**: Complete test coverage for critical functionality
- **Error Handling**: Graceful degradation for database and network issues
- **Data Validation**: Input validation to prevent data corruption
- **Performance Testing**: Verified with large portfolios (50+ items, 20+ purchases per item)

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Quick Start
```bash
# Clone the repository
git clone https://github.com/yourusername/personal_finance.git
cd personal_finance

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the application
pip install -e .

# Run the application
personal_finance
```

### Alternative Installation
```bash
# Install dependencies directly
pip install -r requirements.txt

# Run from source
python main.py
```

## 📋 Usage Guide

### Getting Started
1. **Launch the Application**: Run `personal_finance` or `python main.py`
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

## 🏗️ Architecture

### Project Structure
```
personal_finance/
├── models/                 # Data models (Item, Purchase)
│   ├── item.py            # Core Item class
│   └── purchase.py        # Purchase tracking
├── services/              # Business logic layer
│   └── database.py        # Database service (clean API)
├── config/                # Configuration management
│   └── settings.py        # Application settings
├── utils/                 # Utility functions
│   └── logging.py         # Logging configuration
├── tests/                 # Comprehensive test suite
│   ├── test_app_critical.py      # Critical functionality tests
│   ├── test_database.py          # Database operation tests
│   ├── test_models.py             # Data model tests
│   └── TEST_COVERAGE_SUMMARY.md  # Test documentation
├── docs/                  # Documentation and ADRs
│   └── adr/              # Architectural Decision Records
├── main.py               # Application entry point and core logic
├── gui.py                # Complete GUI application (1,600+ lines)
├── database.py           # Legacy database operations
└── config.json           # Runtime configuration
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

## 🧪 Testing

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

## 🔧 Configuration

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

## 🐛 Troubleshooting

### Common Issues

#### GUI Problems
- **Windows don't appear**: Try running `python gui.py` directly
- **Theme issues**: Reset theme in config.json to "dark" or "light"
- **Performance issues**: Check if you have large datasets, consider filtering

#### Database Issues
- **Database locked**: Close all instances of the application
- **Corrupt database**: Check backups in the `backups/` directory
- **Missing data**: Verify the correct database file is being used

#### Installation Issues
- **Module not found**: Ensure virtual environment is activated
- **Permission errors**: Check write permissions in the installation directory
- **Python version**: Verify Python 3.7+ is installed

### Getting Help
1. Check the logs in `app.log` for detailed error information
2. Run tests to verify system integrity: `python -m pytest tests/`
3. Review the Architectural Decision Records in `docs/adr/`

## 🤝 Contributing

### Development Setup
```bash
# Clone and setup
git clone https://github.com/yourusername/personal_finance.git
cd personal_finance
python -m venv venv
source venv/bin/activate
pip install -e .[dev]

# Run tests
python -m pytest tests/ -v

# Code formatting
black .
flake8 .
```

### Contribution Guidelines
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Add tests** for new functionality
4. **Ensure** all tests pass (`python -m pytest`)
5. **Update** documentation as needed
6. **Commit** changes (`git commit -m 'Add amazing feature'`)
7. **Push** to branch (`git push origin feature/amazing-feature`)
8. **Create** a Pull Request

### Code Standards
- **Testing**: All new features must include tests
- **Documentation**: Update ADRs for architectural changes
- **Style**: Follow Black formatting and Flake8 linting
- **Commits**: Use conventional commit messages

## 📚 Documentation

### Architectural Decision Records
- [ADR 001: Flexible Item Model](docs/adr/001-flexible-item-model.md)
- [ADR 002: Database Schema](docs/adr/002-database-schema.md)
- [ADR 003: GUI Design](docs/adr/003-gui-design.md)

### Additional Resources
- `tests/TEST_COVERAGE_SUMMARY.md`: Comprehensive test documentation
- `DATABASE_MIGRATION.md`: Database migration guide (if applicable)
- `CHANGELOG.md`: Version history and updates

## 🙏 Acknowledgments

- **[yfinance](https://github.com/ranaroussi/yfinance)**: Real-time stock data
- **[ta](https://github.com/bukosabino/ta)**: Technical analysis indicators
- **[matplotlib](https://matplotlib.org/)**: Advanced plotting and visualization
- **[tkinter](https://docs.python.org/3/library/tkinter.html)**: Cross-platform GUI framework
- **[pytest](https://pytest.org/)**: Comprehensive testing framework

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for personal finance management**
