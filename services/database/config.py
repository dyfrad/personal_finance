"""Database configuration and category mappings."""

from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """Configuration class for database settings."""
    
    INVESTMENT_CATEGORIES = ['Stocks', 'Bonds', 'Crypto', 'Real Estate', 'Gold']
    INVENTORY_CATEGORIES = ['Appliances', 'Electronics', 'Furniture', 'Transportation', 
                           'Home Improvement', 'Savings', 'Collectibles']
    EXPENSE_CATEGORIES = ['Expense']
    
    TABLES = {
        'investments': 'investments',
        'inventory': 'inventory', 
        'expenses': 'expenses',
        'purchases': 'purchases'
    }
    
    @classmethod
    def get_table_for_category(cls, category: str) -> str:
        """Get the appropriate table name based on item category."""
        if category in cls.INVESTMENT_CATEGORIES:
            return cls.TABLES['investments']
        elif category in cls.INVENTORY_CATEGORIES:
            return cls.TABLES['inventory']
        elif category in cls.EXPENSE_CATEGORIES:
            return cls.TABLES['expenses']
        else:
            raise ValueError(f"Unknown category: {category}") 