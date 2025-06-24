"""
Personal Finance Manager - Database Package

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

import sqlite3
from typing import List, Optional, Tuple, Any

from .config import DatabaseConfig
from .exceptions import DatabaseError, DatabaseConnectionError, DatabaseQueryError
from .base import DatabaseManager
from .tables import TableManager
from .items import ItemOperations
from .purchases import PurchaseOperations
from .retrieval import DataRetrieval
from .maintenance import DataMaintenance
from utils.logging import get_logger

# Initialize logger for this module
logger = get_logger(__name__)


class Database:
    """
    Main database interface that combines all database operations.
    
    This class provides a unified interface for all database operations
    while maintaining backward compatibility with the existing API.
    """
    
    def __init__(self, db_name: str = "finance.db"):
        """Initialize the database with all operational modules."""
        self.db_name = db_name
        
        # Initialize all operational modules
        self._table_manager = TableManager(db_name)
        self._item_ops = ItemOperations(db_name)
        self._purchase_ops = PurchaseOperations(db_name)
        self._data_retrieval = DataRetrieval(db_name)
        self._data_maintenance = DataMaintenance(db_name)
        
        # Category mappings for backward compatibility
        self.INVESTMENT_CATEGORIES = DatabaseConfig.INVESTMENT_CATEGORIES
        self.INVENTORY_CATEGORIES = DatabaseConfig.INVENTORY_CATEGORIES
        self.EXPENSE_CATEGORIES = DatabaseConfig.EXPENSE_CATEGORIES
        
        logger.info("Database initialization completed successfully")
    
    def init_db(self) -> None:
        """Initialize the database (maintained for backward compatibility)."""
        # Tables are already initialized in TableManager
        pass
    
    def _get_table_name(self, category: str) -> str:
        """Get table name for category (backward compatibility)."""
        return DatabaseConfig.get_table_for_category(category)
    
    def _get_db_connection(self):
        """Get database connection (backward compatibility)."""
        return sqlite3.connect(self.db_name)
    
    # Item operations - delegate to ItemOperations
    def insert_base_item(self, name: str, purchase_price: float, date_of_purchase: str, 
                        current_value: float, profit_loss: float, category: str, 
                        created_at: str, updated_at: str) -> int:
        """Insert a base item (backward compatibility)."""
        return self._item_ops.insert_item(name, purchase_price, date_of_purchase, 
                                         current_value, profit_loss, category, 
                                         created_at, updated_at)
    
    def get_item_by_id(self, item_id: int) -> Optional[Tuple]:
        """Get item by ID (backward compatibility)."""
        return self._item_ops.get_item_by_id(item_id)
    
    def update_base_item(self, item_id: int, name: str, purchase_price: float, 
                        date_of_purchase: str, current_value: float, profit_loss: float, 
                        category: str, updated_at: str) -> None:
        """Update base item (backward compatibility)."""
        self._item_ops.update_item(item_id, name, purchase_price, date_of_purchase, 
                                  current_value, profit_loss, category, updated_at)
    
    def delete_item(self, item_id: int) -> None:
        """Delete item (backward compatibility)."""
        self._item_ops.delete_item(item_id)
    
    # Purchase operations - delegate to PurchaseOperations
    def add_purchase(self, item_id: int, purchase: Any, table_name: str = 'investments') -> None:
        """Add purchase (backward compatibility)."""
        self._purchase_ops.add_purchase(item_id, purchase, table_name)
    
    def get_purchases_for_item(self, item_id: int, table_name: str = 'investments') -> List[Tuple]:
        """Get purchases for item (backward compatibility)."""
        return self._purchase_ops.get_purchases_for_item(item_id, table_name)
    
    def clear_all_purchases(self) -> None:
        """Clear all purchases (backward compatibility)."""
        self._purchase_ops.clear_all_purchases()
    
    # Data retrieval - delegate to DataRetrieval
    def get_all_items(self) -> List[Tuple]:
        """Get all items (backward compatibility)."""
        return self._data_retrieval.get_all_items()
    
    def get_items_by_category(self, category_type: str) -> List[Tuple]:
        """Get items by category (backward compatibility)."""
        return self._data_retrieval.get_items_by_category(category_type)
    
    def get_table_items(self, table_name: str) -> List[Tuple]:
        """Get table items (backward compatibility)."""
        return self._data_retrieval.get_table_items(table_name)
    
    # Data maintenance - delegate to DataMaintenance
    def clear_all_items(self) -> None:
        """Clear all items (backward compatibility)."""
        self._data_maintenance.clear_all_items()
    
    def add_mock_data(self, mock_items: List[Any]) -> None:
        """Add mock data (backward compatibility)."""
        self._data_maintenance.add_mock_data(mock_items)


# Export main classes and exceptions for easy importing
__all__ = [
    'Database',
    'DatabaseError', 
    'DatabaseConnectionError',
    'DatabaseQueryError',
    'DatabaseConfig',
    'DatabaseManager',
    'TableManager',
    'ItemOperations',
    'PurchaseOperations',
    'DataRetrieval',
    'DataMaintenance'
] 