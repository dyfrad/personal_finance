# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/en/2.0.0/).

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

[Unreleased]: https://github.com/msaharan/dyfrad/compare/v0.1.0...HEAD 