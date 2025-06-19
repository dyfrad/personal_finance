import sqlite3
import os
from datetime import datetime
from typing import List, Optional, Tuple, Any, Dict
from contextlib import contextmanager
import logging
from models.item import Item
from models.purchase import Purchase
from config.settings import ConfigManager
from utils.logging import get_logger

# Import the database protection framework
try:
    from utils.database_protection import DatabaseProtection, safe_operation
    PROTECTION_AVAILABLE = True
except ImportError:
    PROTECTION_AVAILABLE = False
    print("Database protection not available")

logger = get_logger(__name__)

class DatabaseError(Exception):
    """Base exception for database-related errors."""
    pass

class DatabaseConnectionError(DatabaseError):
    """Raised when there's an error connecting to the database."""
    pass

class DatabaseQueryError(DatabaseError):
    """Raised when there's an error executing a database query."""
    pass

class Database:
    """Enhanced database service with integrated protection framework."""
    
    def __init__(self, config_manager: Optional[ConfigManager] = None):
        """Initialize database with protection framework."""
        self.config_manager = config_manager or ConfigManager()
        self.config = self.config_manager.get_config()
        self.db_path = self.config.database.db_name
        
        # Initialize database protection
        if PROTECTION_AVAILABLE:
            self.protection = DatabaseProtection(self.db_path)
            # Run auto backup check on initialization
            try:
                self.protection.auto_backup_if_needed()
            except Exception as e:
                logger.warning(f"Auto backup check failed: {e}")
        else:
            self.protection = None
        
        # Initialize database
        self._init_database()

    def _init_database(self):
        """Initialize database tables if they don't exist."""
        with self._get_connection() as conn:
            # Create investments table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS investments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    purchase_price REAL NOT NULL,
                    date_of_purchase TEXT NOT NULL,
                    current_value REAL,
                    profit_loss REAL,
                    category TEXT DEFAULT 'Investment',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create inventory table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    purchase_price REAL NOT NULL,
                    date_of_purchase TEXT NOT NULL,
                    current_value REAL,
                    profit_loss REAL,
                    category TEXT DEFAULT 'Inventory',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create expenses table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    purchase_price REAL NOT NULL,
                    date_of_purchase TEXT NOT NULL,
                    current_value REAL,
                    profit_loss REAL,
                    category TEXT DEFAULT 'Expense',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create purchases table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS purchases (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id INTEGER NOT NULL,
                    table_name TEXT NOT NULL,
                    purchase_price REAL NOT NULL,
                    date_of_purchase TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Legacy items table (kept for migration compatibility)
            conn.execute('''
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    purchase_price REAL NOT NULL,
                    date_of_purchase TEXT NOT NULL,
                    current_value REAL,
                    profit_loss REAL,
                    category TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            logger.info("Database initialized successfully")

    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection with protection considerations."""
        if not os.path.exists(self.db_path):
            logger.warning(f"Database file not found: {self.db_path}")
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def safe_operation_context(self, operation_name: str = "database_operation"):
        """Get a safe operation context manager for database operations."""
        if self.protection and PROTECTION_AVAILABLE:
            return self.protection.safe_database_operation(operation_name)
        else:
            # Fallback context manager that does nothing
            from contextlib import nullcontext
            return nullcontext()

    def create_backup(self, backup_name: Optional[str] = None) -> Optional[str]:
        """Create a manual backup of the database."""
        if self.protection and PROTECTION_AVAILABLE:
            try:
                backup_path = self.protection.create_backup(backup_name)
                logger.info(f"Manual backup created: {backup_path}")
                return str(backup_path)
            except Exception as e:
                logger.error(f"Manual backup failed: {e}")
                return None
        else:
            logger.warning("Database protection not available - backup skipped")
            return None

    def get_protection_status(self) -> Dict[str, Any]:
        """Get database protection status."""
        if self.protection and PROTECTION_AVAILABLE:
            return self.protection.status()
        else:
            return {
                "protection_available": False,
                "database_path": self.db_path,
                "message": "Database protection framework not available"
            }

    def insert_base_item(self, item: Item) -> int:
        """Insert a base item into the items table.
        
        Args:
            item (Item): The item to insert
            
        Returns:
            int: ID of the newly inserted item
            
        Raises:
            DatabaseQueryError: If insertion fails
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                now = datetime.now().isoformat()
                
                cursor.execute('''
                INSERT INTO items (name, purchase_price, date_of_purchase, current_value, 
                                 profit_loss, category, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (item.name, item.purchase_price, item.date_of_purchase,
                      item.current_value, item.profit_loss, item.category, now, now))
                
                item_id = cursor.lastrowid
                conn.commit()
                return item_id
        except sqlite3.Error as e:
            logger.error(f"Error inserting item: {e}")
            raise DatabaseQueryError(f"Failed to insert item: {e}")

    def add_purchase(self, item_id: int, table_name: str, purchase_price: float, 
                     date_of_purchase: str) -> int:
        """Add purchase with protection framework."""
        with self.safe_operation_context("add_purchase"):
            with self._get_connection() as conn:
                cursor = conn.execute('''
                    INSERT INTO purchases (item_id, table_name, purchase_price, date_of_purchase)
                    VALUES (?, ?, ?, ?)
                ''', (item_id, table_name, purchase_price, date_of_purchase))
                
                purchase_id = cursor.lastrowid
                conn.commit()
                
                logger.info(f"Added purchase for {table_name} item {item_id}: ${purchase_price}")
                return purchase_id

    def get_item_by_id(self, item_id: int) -> Optional[Item]:
        """Retrieve an item by its ID.
        
        Args:
            item_id (int): ID of the item to retrieve
            
        Returns:
            Optional[Item]: Item object if found, None otherwise
            
        Raises:
            DatabaseQueryError: If query fails
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,))
                row = cursor.fetchone()
                
                if not row:
                    return None
                    
                item = Item(
                    id=row['id'],
                    name=row['name'],
                    category=row['category'],
                    purchase_price=row['purchase_price'],
                    date_of_purchase=row['date_of_purchase'],
                    current_value=row['current_value'],
                    profit_loss=row['profit_loss'],
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at'])
                )
                
                # Get purchases for this item
                cursor.execute('SELECT * FROM purchases WHERE item_id = ?', (item_id,))
                for purchase_row in cursor.fetchall():
                    purchase = Purchase(
                        id=purchase_row['id'],
                        date=purchase_row['date'],
                        amount=purchase_row['amount'],
                        price=purchase_row['price'],
                        created_at=datetime.fromisoformat(purchase_row['created_at']),
                        updated_at=datetime.fromisoformat(purchase_row['updated_at'])
                    )
                    item.add_purchase(purchase)
                
                return item
        except sqlite3.Error as e:
            logger.error(f"Error retrieving item: {e}")
            raise DatabaseQueryError(f"Failed to retrieve item: {e}")

    def get_all_items(self) -> List[Item]:
        """Retrieve all items from the database.
        
        Returns:
            List[Item]: List of all items
            
        Raises:
            DatabaseQueryError: If query fails
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM items')
                items = []
                
                for row in cursor.fetchall():
                    item = Item(
                        id=row['id'],
                        name=row['name'],
                        category=row['category'],
                        purchase_price=row['purchase_price'],
                        date_of_purchase=row['date_of_purchase'],
                        current_value=row['current_value'],
                        profit_loss=row['profit_loss'],
                        created_at=datetime.fromisoformat(row['created_at']),
                        updated_at=datetime.fromisoformat(row['updated_at'])
                    )
                    
                    # Get purchases for this item
                    cursor.execute('SELECT * FROM purchases WHERE item_id = ?', (item.id,))
                    for purchase_row in cursor.fetchall():
                        purchase = Purchase(
                            id=purchase_row['id'],
                            date=purchase_row['date'],
                            amount=purchase_row['amount'],
                            price=purchase_row['price'],
                            created_at=datetime.fromisoformat(purchase_row['created_at']),
                            updated_at=datetime.fromisoformat(purchase_row['updated_at'])
                        )
                        item.add_purchase(purchase)
                    
                    items.append(item)
                
                return items
        except sqlite3.Error as e:
            logger.error(f"Error retrieving items: {e}")
            raise DatabaseQueryError(f"Failed to retrieve items: {e}")

    def update_item(self, table_name: str, item_id: int, **kwargs) -> bool:
        """Update item with protection framework."""
        with self.safe_operation_context("update_item"):
            with self._get_connection() as conn:
                # Build SET clause dynamically
                set_clauses = []
                values = []
                
                for key, value in kwargs.items():
                    if key in ['name', 'purchase_price', 'date_of_purchase', 'current_value', 'category']:
                        set_clauses.append(f"{key} = ?")
                        values.append(value)
                
                if not set_clauses:
                    return False
                
                # Always update the updated_at timestamp
                set_clauses.append("updated_at = ?")
                values.append(datetime.now().isoformat())
                
                # Recalculate profit_loss if current_value or purchase_price changed
                if 'current_value' in kwargs or 'purchase_price' in kwargs:
                    # Get current values
                    cursor = conn.execute(f"SELECT purchase_price, current_value FROM {table_name} WHERE id = ?", (item_id,))
                    row = cursor.fetchone()
                    if row:
                        current_purchase_price = kwargs.get('purchase_price', row['purchase_price'])
                        current_current_value = kwargs.get('current_value', row['current_value'])
                        profit_loss = current_current_value - current_purchase_price
                        set_clauses.append("profit_loss = ?")
                        values.append(profit_loss)
                
                values.append(item_id)
                
                query = f"UPDATE {table_name} SET {', '.join(set_clauses)} WHERE id = ?"
                cursor = conn.execute(query, values)
                conn.commit()
                
                success = cursor.rowcount > 0
                if success:
                    logger.info(f"Updated item in {table_name}: ID {item_id}")
                else:
                    logger.warning(f"No item found to update in {table_name}: ID {item_id}")
                
                return success

    def delete_item(self, table_name: str, item_id: int) -> bool:
        """Delete item with protection framework."""
        with self.safe_operation_context("delete_item"):
            with self._get_connection() as conn:
                # First delete related purchases
                conn.execute("DELETE FROM purchases WHERE item_id = ? AND table_name = ?", (item_id, table_name))
                
                # Then delete the item
                cursor = conn.execute(f"DELETE FROM {table_name} WHERE id = ?", (item_id,))
                conn.commit()
                
                success = cursor.rowcount > 0
                if success:
                    logger.info(f"Deleted item from {table_name}: ID {item_id}")
                else:
                    logger.warning(f"No item found to delete in {table_name}: ID {item_id}")
                
                return success

    def add_item(self, table_name: str, name: str, purchase_price: float, 
                 date_of_purchase: str, current_value: Optional[float] = None,
                 category: str = None) -> int:
        """Add item with protection framework."""
        with self.safe_operation_context("add_item"):
            with self._get_connection() as conn:
                if current_value is None:
                    current_value = purchase_price
                
                profit_loss = current_value - purchase_price
                
                if category is None:
                    category_map = {
                        'investments': 'Investment',
                        'inventory': 'Inventory', 
                        'expenses': 'Expense'
                    }
                    category = category_map.get(table_name, 'Unknown')
                
                cursor = conn.execute(f'''
                    INSERT INTO {table_name} 
                    (name, purchase_price, date_of_purchase, current_value, profit_loss, category, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (name, purchase_price, date_of_purchase, current_value, profit_loss, category, datetime.now().isoformat()))
                
                item_id = cursor.lastrowid
                conn.commit()
                
                logger.info(f"Added item to {table_name}: {name} (ID: {item_id})")
                return item_id

    def clear_all_data(self) -> None:
        """Clear all data from the database.
        
        This will remove all items and their associated purchases.
        Use with caution as this operation cannot be undone.
        
        Raises:
            DatabaseQueryError: If clearing fails
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM purchases')
                cursor.execute('DELETE FROM items')
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error clearing database: {e}")
            raise DatabaseQueryError(f"Failed to clear database: {e}") 