"""
Personal Finance Manager - Database Configuration Module

A sophisticated Python-based personal finance management application that helps you track and manage your financial portfolio with advanced features for investments, inventory, and expenses.

Copyright (c) 2025 Mohit Saharan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

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