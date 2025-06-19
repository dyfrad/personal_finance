# ADR 002: Database Schema Design

## Status
Accepted

## Context
The personal finance application needs a robust database schema that can handle:
1. **Multiple Item Categories**: Investments, inventory items, and expenses with different data requirements
2. **Purchase Tracking**: Multiple purchases per item with detailed transaction history
3. **Table Separation**: Logical separation of different item types while maintaining consistency
4. **Data Integrity**: Foreign key relationships and referential integrity
5. **Performance**: Efficient queries and indexing for portfolio operations

## Decision
We will implement a multi-table SQLite database schema with:

### Core Tables
1. **Investments Table**: For investment items (stocks, bonds, crypto, real estate, gold)
2. **Inventory Table**: For physical items and savings (appliances, electronics, furniture, etc.)
3. **Expenses Table**: For expense tracking and management
4. **Purchases Table**: Transaction history linked to all item types with table context
5. **Items Table**: Legacy table maintained for backward compatibility

### Schema Structure
```sql
-- Investments table for financial instruments
CREATE TABLE investments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    purchase_price REAL NOT NULL,
    date_of_purchase TEXT NOT NULL,
    current_value REAL NOT NULL,
    profit_loss REAL NOT NULL,
    category TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- Inventory table for physical items and savings
CREATE TABLE inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    purchase_price REAL NOT NULL,
    date_of_purchase TEXT NOT NULL,
    current_value REAL NOT NULL,
    profit_loss REAL NOT NULL,
    category TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- Expenses table for expense tracking
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    purchase_price REAL NOT NULL,
    date_of_purchase TEXT NOT NULL,
    current_value REAL NOT NULL,
    profit_loss REAL NOT NULL,
    category TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- Purchases table for transaction history
CREATE TABLE purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    table_name TEXT NOT NULL DEFAULT 'investments',
    date TEXT NOT NULL,
    amount REAL NOT NULL,
    price REAL NOT NULL,
    FOREIGN KEY (item_id) REFERENCES items (id)
);

-- Legacy items table for backward compatibility
CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    purchase_price REAL NOT NULL,
    date_of_purchase TEXT NOT NULL,
    current_value REAL NOT NULL,
    profit_loss REAL NOT NULL,
    category TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

### Category Routing Logic
Items are automatically routed to appropriate tables based on category:
- **Investments**: 'Stocks', 'Bonds', 'Crypto', 'Real Estate', 'Gold'
- **Inventory**: 'Appliances', 'Electronics', 'Furniture', 'Transportation', 'Home Improvement', 'Savings', 'Collectibles'
- **Expenses**: 'Expense'
- **Legacy**: All other categories fallback to 'items' table

### Purchase Context System
The `purchases` table includes a `table_name` field to distinguish which table an item belongs to:
- `table_name = 'investments'` for investment items
- `table_name = 'inventory'` for inventory items
- No expenses use the purchases table (single transaction model)

## Consequences

### Positive
- **Logical Separation**: Clear organization of different item types
- **Consistent Schema**: All item tables have identical structure for unified operations
- **Flexible Purchase Tracking**: Supports both single and multi-purchase items
- **Data Integrity**: Foreign key relationships prevent orphaned purchases
- **Query Performance**: Smaller tables enable faster category-specific queries
- **Backward Compatibility**: Legacy table supports existing data

### Negative
- **Schema Complexity**: Multiple tables require more complex query logic
- **Code Duplication**: Similar operations across multiple tables
- **Migration Overhead**: Moving between category tables if items change type
- **Testing Complexity**: Need to test operations across all table types

### Neutral
- **Database Size**: Multiple tables vs. single table has minimal impact on SQLite
- **Maintenance**: Standard SQL operations work consistently across all tables

## Implementation Details

### Database Operations
- **Insert**: `_get_table_name(category)` determines target table
- **Update**: Items can change categories, requiring table migration
- **Delete**: Cascading delete removes purchases when items are deleted
- **Query**: Union operations combine results from multiple tables

### Purchase Management
- Investment items support multiple purchases with detailed tracking
- Inventory items can have purchases for bulk buying scenarios
- Expenses use single-transaction model (no purchases table)
- Purchase context (`table_name`) ensures proper association

### Data Access Patterns
- `get_all_items()`: Combines results from all tables
- `get_table_items(table_name)`: Category-specific queries
- `get_purchases_for_item(item_id, table_name)`: Context-aware purchase retrieval

## Validation and Testing
The schema design is validated through comprehensive tests:
- **33 total tests** covering all database operations
- **Table separation tests** verify correct category routing
- **Purchase assignment tests** ensure proper table context
- **Data integrity tests** validate foreign key relationships
- **Migration tests** (when applicable) ensure data preservation

## Related Decisions
- ADR 001: Flexible Item Model - Defines the unified Item class interface
- ADR 003: GUI Design - Determines how the schema is presented to users

## Future Considerations
- **Performance Optimization**: Consider indexing on frequently queried columns
- **Schema Evolution**: Plan for adding new item categories or fields
- **Data Archival**: Strategy for handling large transaction histories
- **Reporting**: Optimized views for portfolio analysis and reporting 