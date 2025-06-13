# Personal Finance Manager

A Python-based personal finance management application that helps you track your assets, investments, and household items. The application provides both a command-line interface and a graphical user interface (GUI) for managing your financial portfolio.

## Features

- Track various types of assets:
  - Household items
  - Investments (stocks, bonds)
  - Personal assets
  - Savings accounts
- Calculate profit/loss for each item
- View total portfolio value
- Save and load portfolio data
- Modern GUI interface with:
  - Easy item addition
  - Tabular view of all items
  - Delete functionality
  - Automatic calculations
  - Data persistence
- SQLite database for reliable data storage:
  - Automatic data persistence
  - Transaction support
  - Data integrity with timestamps
  - Efficient querying

## Requirements

- Python 3.x
- Required Python packages:
  - tkinter (usually comes with Python)
  - pandas
  - numpy
  - sqlite3 (comes with Python)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd personal_finance
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### GUI Version

To run the graphical user interface:

```bash
python gui.py
```

The GUI provides the following features:
- Add new items with details like name, purchase price, date, current value, and category
- View all items in a sortable table
- Save and load your portfolio
- Delete items
- See total portfolio value
- Automatic data persistence using SQLite

### Command Line Version

To run the command-line interface:

```bash
python main.py
```

The CLI provides the following options:
1. Add Item
2. Display Portfolio
3. Save Portfolio
4. Load Portfolio
5. Exit

## Data Storage

The application uses SQLite database (`finance.db`) for data storage, which includes:
- Item name
- Purchase price
- Date of purchase
- Current value
- Profit/Loss
- Category
- Creation timestamp
- Last update timestamp

The database provides:
- Automatic data persistence
- Transaction support
- Data integrity
- Efficient querying
- Backup and restore capabilities

## Example Categories

The application supports various categories of items:
- Appliances
- Electronics
- Furniture
- Stocks
- Bonds
- Transportation
- Home Improvement
- Savings
- Collectibles

## Project Structure

```
personal_finance/
├── main.py           # Core functionality and CLI
├── gui.py           # Graphical user interface
├── database.py      # SQLite database operations
├── finance.db       # SQLite database file (created automatically)
├── requirements.txt # Python package dependencies
└── README.md        # This file
```

## Contributing

Feel free to submit issues and enhancement requests!
