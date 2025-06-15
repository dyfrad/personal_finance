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

## Usage

Run the application:
```bash
personal_finance
```

Or run directly:
```bash
python main.py
```

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
├── main.py           # Application entry point
├── setup.py          # Package setup
└── requirements.txt  # Dependencies
```

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

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Acknowledgments

- [yfinance](https://github.com/ranaroussi/yfinance) for stock data
- [ta](https://github.com/bukosabino/ta) for technical analysis
- [matplotlib](https://matplotlib.org/) for plotting
- [tkinter](https://docs.python.org/3/library/tkinter.html) for GUI
