# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/en/2.0.0/).

## [0.2.1] - 2025-06-20
### Added
- **GNU Affero General Public License v3.0 (AGPL-3.0)**: Complete license implementation
  - Added comprehensive LICENSE file with full AGPL-3.0 text
  - Updated all source files with proper license headers and copyright notices
  - Added license information to setup.py and configuration files
  - Created license information script for easy access to license details
  - Updated README.md with detailed license section and requirements
- **License Compliance**: Full compliance with AGPL-3.0 requirements
  - Copyright notices on all source files (main.py, gui.py, database.py)
  - License information in package metadata (setup.py, config/version.py)
  - License headers following GNU standards
  - License documentation and user guidance
- **License Management Tools**: New utility for license information access
  - Created scripts/show_license.py with multiple output formats
  - Support for summary, full license text, copyright notice, and comprehensive display
  - User-friendly command-line interface with help documentation
  - Easy access to license information and user rights

### Documentation
- **License Documentation**: Comprehensive license information
  - Detailed license summary in README.md with user rights and requirements
  - License requirements and user rights explanation
  - Copyright notice and attribution
  - Links to full license text and official sources
  - Created LICENSE_IMPLEMENTATION_SUMMARY.md with complete implementation details
  - Updated docs/LICENSE_HEADER_TEMPLATE.txt with improved usage instructions

### Fixed
- **Test Infrastructure**: Complete test framework compatibility updates
  - Fixed Database constructor calls to use ConfigManager instead of direct db_name parameter
  - Updated test configuration to disable database protection features during testing
  - Fixed method signatures for add_purchase(), delete_item(), and update_item() methods
  - Added proper error handling for database connection and query operations
  - Updated database connection method calls to use private _get_connection()
  - Fixed exception handling tests to expect correct DatabaseError types
  - Ensured all 33 tests pass with updated Database service API
- **Database Service Compatibility**: Enhanced backward compatibility and consistency
  - Aligned purchases table schema with consistent field names (date, amount, price)
  - Updated add_purchase() method to accept Purchase objects for better type safety
  - Made delete_item() table_name parameter optional with automatic detection
  - Improved database protection configuration handling during testing
  - Fixed method signatures across Database service for consistency

### Changed
- Updated version to 0.2.1 to reflect license implementation
- Enhanced license header template with better usage instructions
- Improved documentation structure with dedicated license section

## [0.2.0] - 2025-06-19
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
- **Database Protection Framework**: Comprehensive safeguards against data loss
  - Automatic backups every 6 hours with configurable retention
  - Database file protection with read-only permissions
  - Integrity verification with checksum validation
  - Safe operation contexts with automatic backup creation
  - Emergency recovery with multiple confirmation layers
- **Performance Optimization**: Improved handling of large datasets
  - Efficient queries with proper indexing
  - Batch operations for bulk updates
  - Memory management and cleanup
  - Asynchronous data loading for UI responsiveness
- **User Experience**: Enhanced interface and usability
  - Google Material Design themes with light/dark mode
  - Responsive layout optimized for different screen sizes
  - Intuitive category-specific forms and validation
  - Real-time updates and interactive visualizations
- **Data Management**: Improved data handling and validation
  - Comprehensive input validation and error handling
  - Data migration tools for schema updates
  - Export/import functionality with CSV support
  - Backup and restore capabilities with integrity checks

### Fixed
- **Data Integrity**: Resolved issues with purchase tracking and calculations
  - Fixed cost basis calculation for multiple purchases
  - Corrected profit/loss calculations across all item types
  - Improved foreign key relationships and referential integrity
  - Enhanced data validation and error recovery
- **GUI Stability**: Fixed interface issues and improved responsiveness
  - Resolved window management and memory leaks
  - Fixed chart rendering and update issues
  - Improved error handling and user feedback
  - Enhanced theme switching and layout consistency
- **Database Operations**: Improved reliability and performance
  - Fixed connection management and pooling
  - Resolved transaction consistency issues
  - Improved query optimization and indexing
  - Enhanced backup and recovery procedures

### Documentation
- **Comprehensive Documentation**: Complete documentation suite
  - Detailed README with installation and usage guides
  - Feature documentation with examples and use cases
  - Configuration guide with all available options
  - Troubleshooting documentation with common solutions
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

## [0.1.0] - 2025-06-13
### Added
- Initial implementation of a Tkinter GUI for the Personal Finance Manager application.
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