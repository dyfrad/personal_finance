# Architecture Guide

## Project Structure
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

## Database Schema
- **Investments Table**: Stocks, bonds, crypto, real estate, gold
- **Inventory Table**: Physical items and savings accounts
- **Expenses Table**: Expense tracking and management
- **Purchases Table**: Transaction history with table context (`table_name` field)

## Technology Stack
- **GUI Framework**: Tkinter with ttk for modern widgets
- **Database**: SQLite with multiple table architecture
- **Charting**: Matplotlib with TkAgg backend
- **Data Analysis**: yfinance for stock data, ta for technical analysis
- **Testing**: pytest with 33 comprehensive tests
- **Configuration**: JSON-based config management

## Architectural Decision Records

### ADR Documents
- [ADR 001: Flexible Item Model](docs/adr/001-flexible-item-model.md)
- [ADR 002: Database Schema](docs/adr/002-database-schema.md)
- [ADR 003: GUI Design](docs/adr/003-gui-design.md)
- [ADR 004: Testing Architecture](docs/adr/004-testing-architecture.md)
- [ADR 005: Database Protection Framework](docs/adr/005-database-protection-framework.md)

## Design Principles

### Data Layer
- Multiple specialized tables (investments, inventory, expenses)
- Purchase history tracking with table context
- SQLite for local data storage and privacy

### Business Logic
- Centralized in services layer
- Clean separation of concerns
- Comprehensive error handling

### User Interface
- Four-quadrant dashboard design
- Google Material Design principles
- Theme support (light/dark mode)
- Responsive layout design

### Data Protection
- Automatic database protection framework
- Time-based and event-driven backups
- Multiple confirmation layers for destructive operations
- Read-only database protection when not in use 