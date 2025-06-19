# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/en/2.0.0/).

## [0.2.0] - 2024-12-19
### Added
- **Comprehensive Testing Architecture**: 33 focused tests covering critical functionality
  - 13 critical application functionality tests
  - 9 database operation tests  
  - 11 data model tests
  - 100% test success rate with < 2 second execution time
- **Advanced Database Schema**: Multi-table architecture with proper separation
  - Separate tables for investments, inventory, and expenses
  - Purchase tracking with table context (`table_name` field)
  - Category-based automatic routing system
  - Foreign key relationships and referential integrity
- **Enhanced GUI Features**: 1,600+ line comprehensive interface
  - Four-quadrant dashboard with stock performance and expense tracking
  - Category-specific forms (investments, inventory, expenses)
  - Interactive charts with technical indicators (RSI, MACD, SMA, EMA)
  - Real-time stock data integration with yfinance
  - Advanced purchase management dialogs
- **Robust Error Handling**: Graceful degradation for all failure scenarios
  - Database corruption protection
  - Invalid data input validation
  - Network timeout handling
  - Performance optimization for large portfolios
- **Advanced Analytics**: Technical analysis and performance tracking
  - Multiple technical indicators with customizable parameters
  - Interactive chart cursors with detailed hover information
  - Historical data analysis with configurable time periods
  - Comparison features for multiple stocks
- **Configuration Management**: JSON-based configuration system
  - Theme settings (light/dark mode)
  - Database configuration
  - UI preferences and window sizing
  - Debug and logging controls

### Enhanced
- **Item Model**: Sophisticated handling of different item types
  - Multi-purchase support for investments with accurate calculations
  - Single-purchase model for inventory items
  - Simplified expense tracking with automatic profit/loss calculation
  - Flexible category system with automatic table routing
- **Purchase System**: Advanced transaction tracking
  - Context-aware purchase storage (investments vs inventory)
  - Multiple purchase aggregation with accurate totals
  - Real-time calculation updates
  - Purchase history visualization
- **Database Operations**: Robust and efficient data management
  - CRUD operations across multiple tables
  - Batch operations for performance
  - Data integrity validation
  - Automated backup and recovery systems
- **User Interface**: Professional and responsive design
  - Google Material Design principles
  - Consistent theming across all windows
  - Platform-optimized dialogs and controls
  - Responsive layout for different screen sizes

### Fixed
- **Data Integrity**: Comprehensive validation and error prevention
  - ID uniqueness across all tables
  - Foreign key constraint enforcement
  - Purchase orphan prevention
  - Calculation accuracy for financial data
- **Performance**: Optimized for realistic usage scenarios
  - Large portfolio handling (50+ items tested)
  - High transaction volume support (20+ purchases per item)
  - Efficient database queries
  - Memory leak prevention
- **System Stability**: Robust error handling and recovery
  - Database connection error management
  - GUI responsiveness under load
  - Graceful degradation for missing data
  - Platform compatibility improvements

### Documentation
- **Comprehensive README**: Updated with current features and architecture
- **Architectural Decision Records**: Four detailed ADRs covering design decisions
  - ADR 001: Flexible Item Model
  - ADR 002: Database Schema Design  
  - ADR 003: GUI Design and Layout
  - ADR 004: Testing Architecture and Quality Assurance
- **Test Documentation**: Complete test coverage summary and execution guide
- **Configuration Guide**: Detailed configuration options and environment variables

### Quality Assurance
- **Test Coverage**: 33 comprehensive tests with 100% success rate
- **Code Quality**: Structured architecture with clear separation of concerns
- **Error Resilience**: Systematic testing of failure scenarios
- **Performance Validation**: Load testing with realistic data volumes
- **Documentation**: Living documentation through tests and ADRs

## [0.1.0] - 2024-05-20
### Added
- Initial implementation of a Tkinter GUI for the personal finance application.
- Basic SQLite database integration for persistent storage of financial items.
- Core functionality to view, add, edit, and delete financial items.
- Basic multi-purchase support for stocks/bonds with a dedicated purchases table.
- Initial performance graph implementation for stocks and bonds using `matplotlib` and `yfinance`.
- Basic "View/Add Purchases" dialog to manage individual purchase entries for items.
- Simple purchase markers with tooltips on the performance graph using `mplcursors`.
- Initial four-quadrant main dashboard layout.
- Basic "Reset Demo Data" feature to repopulate the database with mock data.
- Initial mock household data for a typical single person in the Netherlands.
- Basic Google Material Design-inspired light and dark themes for the GUI.

### Changed
- Initial implementation of flexible `Item` class for both single-purchase and multi-purchase items.
- Basic database schema and functions (`database.py`) for the flexible `Item` model.
- Streamlined `main.py` with core functionality.
- Initial `gui.py` implementation aligned with the `Item` model.
- Basic technical analysis implementation using `numpy` and `pandas`.
- Initial `CustomMessageBox` implementation for macOS UI warnings.

### Fixed
- Basic data persistence implementation for manually added items.
- Initial fix for macOS button height warnings.
- Basic implementation of performance graph data fetching and display.
- Initial timezone handling in historical data fetching.
- Basic implementation of purchase markers on the performance graph.
- Initial layout implementation for "Add Item" and "View Items" windows.
- Basic theme consistency implementation.
- Initial layout fixes for the "View Items" window.

## [Upcoming]
### Planned
- GUI testing framework integration
- Performance benchmarking and metrics
- Enhanced security testing and input validation
- Advanced reporting and analytics features
- Data export/import in multiple formats
- Mobile-responsive web interface
- Real-time market data integration improvements

[Unreleased]: https://github.com/msaharan/dyfrad/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/msaharan/dyfrad/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/msaharan/dyfrad/releases/tag/v0.1.0 