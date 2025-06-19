# Personal Finance Manager

A Python-based personal finance management application that helps you track and manage your financial portfolio, including stocks, bonds, and other assets.

## Features

- Track stocks and bonds with multiple purchases
- Monitor regular items (appliances, electronics, etc.)
- Calculate profit/loss for each item
- View performance graphs and technical analysis
- Export/import portfolio data
- Modern, user-friendly GUI
- Dark/light theme support
- **NEW**: Separate database tables for investments, inventory, and expenses

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/personal_finance.git
cd personal_finance
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package:
```bash
pip install -e .
```

## Database Migration (Important!)

**If you're upgrading from a previous version or working with an existing database:**

The application has been updated to use separate tables for different item categories. If you have an existing `finance.db` file, you'll need to run the migration script:

### Check if migration is needed:
```bash
python migrate_database.py --check
```

### Run the migration:
```bash
python migrate_database.py
```

### For automated deployments:
```bash
python migrate_database.py --auto
```

The migration will:
- Create new tables: `investments`, `inventory`, and `expenses`
- Move existing items from the old `items` table to appropriate category tables
- Preserve all your data and purchase history
- Create a backup of your database before migration

**New Database Structure:**
- **Investments Table**: Stocks, Bonds, Crypto, Real Estate, Gold
- **Inventory Table**: Appliances, Electronics, Furniture, Transportation, Home Improvement, Savings, Collectibles
- **Expenses Table**: Expense category items

For detailed migration information, see `DATABASE_MIGRATION.md`.

## Usage

Run the application:
```bash
personal_finance
```

Or run directly:
```bash
python main.py
```

### First Time Setup

If this is your first time running the application:
1. The database will be automatically created with the new table structure
2. Start adding your financial items through the GUI
3. Items will be automatically categorized into the appropriate tables

## Development

### Project Structure

```
personal_finance/
├── models/             # Data models
├── services/          # Business logic
├── ui/               # GUI components
├── utils/            # Utility functions
├── config/           # Configuration
├── tests/            # Test files
├── docs/             # Documentation and ADRs
├── main.py           # Application entry point
├── database.py       # Database operations
├── gui.py            # Main GUI application
├── migrate_database.py  # Database migration script
├── setup.py          # Package setup
├── requirements.txt  # Dependencies
└── DATABASE_MIGRATION.md  # Migration guide
```

### Database Tables

The application uses SQLite with the following table structure:

- **investments**: For investment items (stocks, bonds, crypto, etc.)
- **inventory**: For physical items and savings
- **expenses**: For expense tracking
- **purchases**: Linked to all item types for transaction history

All tables maintain the same column structure for consistency while allowing category-specific optimizations.

### Running Tests

```bash
pytest
```

For coverage report:
```bash
pytest --cov=.
```

### Code Style

The project uses:
- Black for code formatting
- Flake8 for linting
- MyPy for type checking

Run all checks:
```bash
black .
flake8
mypy .
```

## Troubleshooting

### Migration Issues
- If migration fails, restore from the automatically created backup: `finance_backup_[timestamp].db`
- Check `DATABASE_MIGRATION.md` for detailed troubleshooting steps
- Ensure you have write permissions in the application directory

### GUI Issues
- If windows don't appear properly, try running with `python gui.py` directly
- Check that all dependencies are properly installed
- Verify your Python version is 3.7 or higher

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

### Database Changes
If you're making changes to the database schema:
1. Update the migration script if needed
2. Update tests to reflect the new structure
3. Document changes in `DATABASE_MIGRATION.md`

## Acknowledgments

- [yfinance](https://github.com/ranaroussi/yfinance) for stock data
- [ta](https://github.com/bukosabino/ta) for technical analysis
- [matplotlib](https://matplotlib.org/) for plotting
- [tkinter](https://docs.python.org/3/library/tkinter.html) for GUI
