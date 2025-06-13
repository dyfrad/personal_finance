# ADR 003: GUI Design and Layout

## Status
Accepted

## Context
The application needs a modern, user-friendly interface that:
- Provides quick access to key information
- Supports both viewing and managing financial items
- Displays performance graphs and statistics
- Maintains consistency across different windows and dialogs
- Works well on different platforms (especially macOS)

## Decision
We will implement a GUI with:
1. **Four-Quadrant Main Dashboard**:
   - Top Left: Stock performance graph
   - Top Right: Action buttons (View Items, Add Item)
   - Bottom Left: Expenses graph
   - Bottom Right: Placeholder for future features

2. **Google Material Design Theme**:
   - Light and dark mode support
   - Consistent color scheme and typography
   - Modern, clean look
   - Responsive buttons and widgets
   - Custom message boxes for better platform compatibility

## Consequences
### Positive
- Clear organization of information and actions
- Modern, professional appearance
- Consistent user experience
- Better platform compatibility
- Easy to extend with new features

### Negative
- More complex layout management
- Need to maintain theme consistency across all windows
- Some platform-specific adjustments required

## Implementation Details
- Using Tkinter with ttk for modern widgets
- Custom `MainDashboard` class for the four-quadrant layout
- `set_theme()` function for consistent styling
- `CustomMessageBox` for platform-compatible dialogs
- Separate windows for detailed views (Add Item, View Items)
- Matplotlib integration for graphs
- Mplcursors for interactive graph features

## Related Decisions
- ADR 001: Flexible Item Model
- ADR 002: Database Schema Design 