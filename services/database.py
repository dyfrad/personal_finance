"""
Personal Finance Manager - Database Module

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
from datetime import datetime
from typing import List, Optional, Tuple, Union, Any
from contextlib import contextmanager
from dataclasses import dataclass
from utils.logging import get_logger

# Initialize logger for this module
logger = get_logger(__name__)


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


class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass


class DatabaseManager:
    """Base database manager for common operations."""
    
    def __init__(self, db_name: str = "finance.db"):
        self.db_name = db_name
        self.config = DatabaseConfig()
        logger.info(f"Initializing database manager with file: {db_name}")
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            logger.debug(f"Database connection established to {self.db_name}")
            yield conn
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            if conn:
                conn.rollback()
            raise DatabaseError(f"Database operation failed: {e}")
        finally:
            if conn:
                conn.close()
                logger.debug("Database connection closed")


class TableManager(DatabaseManager):
    """Handles table creation and schema management."""
    
    def __init__(self, db_name: str = "finance.db"):
        super().__init__(db_name)
        self._initialize_tables()
    
    def _initialize_tables(self) -> None:
        """Initialize all required database tables."""
        logger.debug("Starting database table initialization")
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                self._create_item_tables(cursor)
                self._create_purchases_table(cursor)
                conn.commit()
            logger.info("All database tables created/verified successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database tables: {e}")
            raise
    
    def _create_item_tables(self, cursor: sqlite3.Cursor) -> None:
        """Create item tables (investments, inventory, expenses)."""
        item_table_sql = '''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            purchase_price REAL NOT NULL,
            date_of_purchase TEXT NOT NULL,
            current_value REAL NOT NULL,
            profit_loss REAL NOT NULL,
            category TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        '''
        
        for table_name in ['investments', 'inventory', 'expenses']:
            cursor.execute(item_table_sql.format(table_name=table_name))
            logger.debug(f"Created/verified {table_name} table")
    
    def _create_purchases_table(self, cursor: sqlite3.Cursor) -> None:
        """Create purchases table."""
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            table_name TEXT NOT NULL DEFAULT 'investments',
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (item_id) REFERENCES investments(id)
        )
        ''')
        logger.debug("Created/verified purchases table")


class ItemOperations(DatabaseManager):
    """Handles CRUD operations for items."""
    
    def insert_item(self, name: str, purchase_price: float, date_of_purchase: str, 
                   current_value: float, profit_loss: float, category: str, 
                   created_at: str, updated_at: str) -> int:
        """Insert a new item into the appropriate table."""
        logger.info(f"Inserting new item: {name} (category: {category})")
        
        table_name = self.config.get_table_for_category(category)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
            INSERT INTO {table_name} (name, purchase_price, date_of_purchase, current_value, 
                             profit_loss, category, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, purchase_price, date_of_purchase, 
                  current_value, profit_loss, category, created_at, updated_at))
            item_id = cursor.lastrowid
            conn.commit()
            
        logger.info(f"Successfully inserted item '{name}' with ID {item_id} in table '{table_name}'")
        return item_id
    
    def get_item_by_id(self, item_id: int) -> Optional[Tuple]:
        """Retrieve an item by its ID from any table."""
        logger.debug(f"Retrieving item with ID: {item_id}")
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            for table in ['investments', 'inventory', 'expenses']:
                logger.debug(f"Searching for item ID {item_id} in table '{table}'")
                cursor.execute(f'SELECT * FROM {table} WHERE id = ?', (item_id,))
                row = cursor.fetchone()
                if row:
                    logger.info(f"Found item ID {item_id} in table '{table}'")
                    return row
        
        logger.warning(f"Item with ID {item_id} not found in any table")
        return None
    
    def update_item(self, item_id: int, name: str, purchase_price: float, 
                   date_of_purchase: str, current_value: float, profit_loss: float, 
                   category: str, updated_at: str) -> bool:
        """Update an existing item."""
        logger.info(f"Updating item ID {item_id}: {name} (category: {category})")
        
        table_name = self.config.get_table_for_category(category)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
            UPDATE {table_name} 
            SET name = ?, purchase_price = ?, date_of_purchase = ?, 
                current_value = ?, profit_loss = ?, category = ?, updated_at = ?
            WHERE id = ?
            ''', (name, purchase_price, date_of_purchase,
                  current_value, profit_loss, category, updated_at, item_id))
            rows_affected = cursor.rowcount
            conn.commit()
        
        success = rows_affected > 0
        if success:
            logger.info(f"Successfully updated item ID {item_id} in table '{table_name}'")
        else:
            logger.warning(f"No rows affected when updating item ID {item_id}")
        
        return success
    
    def delete_item(self, item_id: int) -> bool:
        """Delete an item and its associated purchases."""
        logger.info(f"Deleting item ID {item_id} and associated purchases")
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Delete from item tables
            item_deleted = False
            for table in ['investments', 'inventory', 'expenses']:
                cursor.execute(f'DELETE FROM {table} WHERE id = ?', (item_id,))
                if cursor.rowcount > 0:
                    logger.debug(f"Deleted item ID {item_id} from table '{table}'")
                    item_deleted = True
            
            # Delete associated purchases
            cursor.execute('DELETE FROM purchases WHERE item_id = ?', (item_id,))
            purchases_deleted = cursor.rowcount
            
            conn.commit()
        
        if item_deleted:
            logger.info(f"Successfully deleted item ID {item_id} and {purchases_deleted} associated purchases")
        else:
            logger.warning(f"No item found with ID {item_id} to delete")
        
        return item_deleted


class PurchaseOperations(DatabaseManager):
    """Handles purchase-related operations."""
    
    def add_purchase(self, item_id: int, purchase: Any, table_name: str = 'investments') -> None:
        """Add a purchase record for an item."""
        logger.info(f"Adding purchase for item ID {item_id}: {purchase.amount} units at ${purchase.price} on {purchase.date}")
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO purchases (item_id, table_name, date, amount, price)
            VALUES (?, ?, ?, ?, ?)
            ''', (item_id, table_name, purchase.date, purchase.amount, purchase.price))
            purchase_id = cursor.lastrowid
            conn.commit()
            
        logger.info(f"Successfully added purchase with ID {purchase_id} for item {item_id}")
    
    def get_purchases_for_item(self, item_id: int, table_name: str = 'investments') -> List[Tuple]:
        """Retrieve all purchase records for a specific item."""
        logger.debug(f"Retrieving purchases for item ID {item_id} from table '{table_name}'")
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT date, amount, price FROM purchases WHERE item_id = ? AND table_name = ?', 
                          (item_id, table_name))
            rows = cursor.fetchall()
        
        logger.debug(f"Retrieved {len(rows)} purchase records for item ID {item_id}")
        return rows
    
    def clear_all_purchases(self) -> int:
        """Clear all purchase records from the database."""
        logger.warning("Clearing ALL purchase records from database")
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM purchases')
            count = cursor.fetchone()[0]
            cursor.execute('DELETE FROM purchases')
            conn.commit()
        
        logger.warning(f"Cleared {count} purchase records from database")
        return count


class DataRetrieval(DatabaseManager):
    """Handles data retrieval operations."""
    
    def get_all_items(self) -> List[Tuple]:
        """Retrieve all items from all tables."""
        logger.debug("Retrieving all items from all tables")
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            all_items = []
            
            for table in ['investments', 'inventory', 'expenses']:
                cursor.execute(f'SELECT * FROM {table}')
                rows = cursor.fetchall()
                all_items.extend(rows)
                logger.debug(f"Retrieved {len(rows)} items from table '{table}'")
        
        logger.info(f"Retrieved total of {len(all_items)} items from all tables")
        return all_items
    
    def get_items_by_category(self, category_type: str) -> List[Tuple]:
        """Retrieve items by category type."""
        logger.debug(f"Retrieving items by category type: {category_type}")
        
        table_mapping = {
            "Investment": 'investments',
            "Inventory": 'inventory', 
            "Expense": 'expenses'
        }
        
        table_name = table_mapping.get(category_type)
        if not table_name:
            logger.warning(f"Unknown category type '{category_type}', returning all items")
            return self.get_all_items()
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM {table_name}')
            rows = cursor.fetchall()
        
        logger.info(f"Retrieved {len(rows)} items from '{table_name}' table")
        return rows
    
    def get_table_items(self, table_name: str) -> List[Tuple]:
        """Retrieve all items from a specific table."""
        logger.debug(f"Retrieving all items from table: {table_name}")
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM {table_name}')
            rows = cursor.fetchall()
        
        logger.info(f"Retrieved {len(rows)} items from table '{table_name}'")
        return rows


class DataMaintenance(DatabaseManager):
    """Handles data maintenance operations."""
    
    def clear_all_items(self) -> Tuple[int, int]:
        """Clear all items from all tables."""
        logger.warning("Clearing ALL items from database - this cannot be undone")
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Clear all item tables
            total_items_deleted = 0
            for table in ['investments', 'inventory', 'expenses']:
                cursor.execute(f'SELECT COUNT(*) FROM {table}')
                count = cursor.fetchone()[0]
                cursor.execute(f'DELETE FROM {table}')
                total_items_deleted += count
                logger.debug(f"Cleared {count} items from table '{table}'")
            
            # Clear purchases table
            cursor.execute('SELECT COUNT(*) FROM purchases')
            purchases_count = cursor.fetchone()[0]
            cursor.execute('DELETE FROM purchases')
            
            conn.commit()
        
        logger.warning(f"Database cleared: {total_items_deleted} items and {purchases_count} purchases deleted")
        return total_items_deleted, purchases_count
    
    def add_mock_data(self, mock_items: List[Any]) -> Tuple[int, int]:
        """Add mock data to the database for testing purposes."""
        logger.info(f"Adding {len(mock_items)} mock items to database")
        
        now = datetime.now().isoformat()
        items_added = 0
        purchases_added = 0
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            for item in mock_items:
                # For simple items, use their direct attributes
                if item.category not in ['Stocks', 'Bonds']:
                    item_id = self._insert_mock_item(item, now)
                    items_added += 1
                else:
                    # For stocks/bonds, insert a base item first, then add purchases
                    item_id = self._insert_mock_item_with_purchases(item, now, cursor)
                    items_added += 1
                    if hasattr(item, 'purchases'):
                        purchases_added += len(item.purchases)
            
            conn.commit()
        
        logger.info(f"Successfully added {items_added} mock items and {purchases_added} purchase records")
        return items_added, purchases_added
    
    def _insert_mock_item(self, item: Any, timestamp: str) -> int:
        """Insert a simple mock item."""
        item_ops = ItemOperations(self.db_name)
        return item_ops.insert_item(
            item.name, item.purchase_price, item.date_of_purchase,
            item.current_value, item.profit_loss, item.category, timestamp, timestamp
        )
    
    def _insert_mock_item_with_purchases(self, item: Any, timestamp: str, cursor: sqlite3.Cursor) -> int:
        """Insert a mock item with purchases."""
        item_ops = ItemOperations(self.db_name)
        # Placeholder values for main item table
        item_id = item_ops.insert_item(
            item.name, 0.0, "", 0.0, 0.0, item.category, timestamp, timestamp
        )
        
        # Insert purchases if present
        if hasattr(item, 'purchases'):
            for purchase in item.purchases:
                cursor.execute('''
                INSERT INTO purchases (item_id, table_name, date, amount, price)
                VALUES (?, ?, ?, ?, ?)
                ''', (item_id, 'investments', purchase.date, purchase.amount, purchase.price))
        
        return item_id


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