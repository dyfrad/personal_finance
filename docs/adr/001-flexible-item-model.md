# ADR 001: Flexible Item Model

## Status
Accepted

## Context
The application needs to handle two distinct types of financial items:
1. **Household Items**: Single purchase items (e.g., electronics, furniture) with a single purchase price, date, and current value.
2. **Financial Instruments**: Items like stocks and bonds that can have multiple purchases over time, each with its own date, amount, and price.

## Decision
We will implement a flexible `Item` class that can represent both types of items. The class will have:
- Core attributes common to all items (name, category, etc.)
- A `purchases` list to store multiple purchase entries
- Methods to calculate total invested amount, current value, and profit/loss that work for both single and multi-purchase items

## Consequences
### Positive
- Unified data model simplifies code and database schema
- Consistent interface for all items in the application
- Easy to extend for new item types in the future
- Simplified database operations and queries

### Negative
- Slightly more complex class structure
- Need to handle edge cases (e.g., items with no purchases)
- Database schema needs to support both types of items

## Implementation Details
- The `Item` class uses a `purchases` list to store `Purchase` objects
- For household items, the list will contain a single purchase
- For stocks/bonds, the list can contain multiple purchases
- The database uses two tables: `items` for base item data and `purchases` for purchase entries
- The `get_total_invested()`, `get_current_total_value()`, and `get_overall_profit_loss()` methods handle both cases

## Related Decisions
- ADR 002: Database Schema Design
- ADR 003: GUI Display and Interaction 