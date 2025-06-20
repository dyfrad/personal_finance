# Personal Finance Manager

A sophisticated Python-based personal finance management application that helps you track and manage your financial portfolio with advanced features for investments, inventory, and expenses.

A sophisticated personal finance application designed for individual use with local data storage and privacy protection.

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

### Data Protection
- **Database Protection**: Automatic protection against accidental deletion with read-only permissions
- **Automatic Backups**: Every 6 hours + event-driven backups with configurable retention
- **Emergency Recovery**: Multiple confirmation layers and safety backups for restoration
- **Local Storage**: All data stored privately on your device

## Quick Start

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd personal_finance

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the application
pip install -e .

# Run the application
personal-finance-manager
```

### Alternative - Run from Source
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application (choose one):
python main.py              # Full version with database protection
python main.py --help       # See all available options
python gui.py               # Simple GUI only (for testing)
```

## Basic Usage

### Getting Started
1. **Launch**: Run `personal-finance-manager` or `python main.py`
2. **Dashboard**: Four-quadrant view with stocks, expenses, and controls
3. **Add Items**: Use category-specific forms for investments, inventory, or expenses
4. **View Portfolio**: Comprehensive table with detailed financial information
5. **Analyze**: Interactive charts with technical indicators

### Managing Your Portfolio
- **Investments**: Track multiple purchases with shares/units and price per unit
- **Inventory**: Single or multiple purchase tracking for physical items
- **Expenses**: Simplified forms with amount and date
- **Export**: CSV export for data portability

### Key Features
- **Technical Analysis**: RSI, MACD, moving averages for stock performance
- **Theme Switching**: Toggle between light and dark modes
- **Real-time Updates**: Live stock data integration (when available)
- **Data Export**: Export portfolio data to CSV format

## Database Protection

Your database is automatically protected:
- **Automatic backups** every 6 hours
- **Protection status**: `python main.py --check-protection`
- **Manual backup**: `python scripts/protect_database.py backup --name "my_backup"`
- **Emergency recovery**: Available if needed

See [PROTECTION_QUICK_START.md](PROTECTION_QUICK_START.md) for details.

## Documentation

### User Guides
- **[Configuration Guide](CONFIGURATION.md)**: Settings, themes, and environment variables
- **[Troubleshooting Guide](TROUBLESHOOTING.md)**: Common issues and solutions

### Developer Resources
- **[Development Guide](DEVELOPMENT.md)**: Version management, testing, and workflow
- **[Architecture Guide](ARCHITECTURE.md)**: Technical architecture and design decisions
- **[Changelog](CHANGELOG.md)**: Version history and updates

### Additional Resources
- `PROTECTION_QUICK_START.md`: Database protection commands
- `docs/`: Architectural Decision Records and detailed documentation
- `tests/`: Comprehensive test suite (33 tests, 100% passing)

## Quality Assurance
- **33 Comprehensive Tests**: Complete test coverage for critical functionality
- **Database Protection Framework**: Comprehensive safeguards against accidental data loss
- **Error Handling**: Graceful degradation for database and network issues
- **Performance Testing**: Verified with large portfolios (50+ items, 20+ purchases per item)

## License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

- **Freedom to use, study, modify, and share**
- **Network server provision**: Modified versions on servers must provide source code
- **Source code availability**: Distributed software must include complete source code

See [LICENSE](LICENSE) for complete details.

## Privacy & Security

This is a **personal finance application** designed for individual use:
- **Local Data Storage**: All financial data stored locally on your device
- **No Cloud Services**: No data transmitted to external servers
- **Privacy First**: Your financial information remains completely private
- **Data Sovereignty**: You maintain full control over your data

---

**Built for personal finance management**
