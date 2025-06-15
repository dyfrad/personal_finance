import sqlite3
from datetime import datetime
from typing import List, Optional, Tuple, Any
from contextlib import contextmanager
import logging
from models.item import Item
from models.purchase import Purchase

logger = logging.getLogger(__name__)

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
    """Database management class for the personal finance application.
    
    Handles all database operations including creating tables, inserting/updating/deleting
    items and purchases, and retrieving data. Uses SQLite as the backend database.
    
    Attributes:
        db_name (str): Name of the SQLite database file
    """
    
    def __init__(self, db_name: str = "finance.db"):
        """Initialize the database connection.
        
        Args:
            db_name (str): Name of the SQLite database file. Defaults to "finance.db"
        """
        self.db_name = db_name
        self.init_db()

    @contextmanager
    def get_connection(self):
        """Context manager for database connections.
        
        Yields:
            sqlite3.Connection: Database connection
            
        Raises:
            DatabaseConnectionError: If connection cannot be established
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            conn.row_factory = sqlite3.Row
            yield conn
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            raise DatabaseConnectionError(f"Could not connect to database: {e}")
        finally:
            if conn:
                conn.close()

    def init_db(self) -> None:
        """Initialize the database with required tables.
        
        Creates two tables if they don't exist:
        1. items: Stores basic item information
        2. purchases: Stores purchase records for stocks and bonds
        
        Raises:
            DatabaseError: If table creation fails
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Create items table
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS items (
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
                ''')
                
                # Create purchases table
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS purchases (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    amount REAL NOT NULL,
                    price REAL NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY(item_id) REFERENCES items(id)
                )
                ''')
                
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {e}")
            raise DatabaseError(f"Failed to initialize database: {e}")

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
            with self.get_connection() as conn:
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

    def add_purchase(self, item_id: int, purchase: Purchase) -> int:
        """Add a purchase record for a stock or bond.
        
        Args:
            item_id (int): ID of the item this purchase belongs to
            purchase (Purchase): Purchase object to add
            
        Returns:
            int: ID of the newly inserted purchase
            
        Raises:
            DatabaseQueryError: If insertion fails
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                now = datetime.now().isoformat()
                
                cursor.execute('''
                INSERT INTO purchases (item_id, date, amount, price, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (item_id, purchase.date, purchase.amount, purchase.price, now, now))
                
                purchase_id = cursor.lastrowid
                conn.commit()
                return purchase_id
        except sqlite3.Error as e:
            logger.error(f"Error adding purchase: {e}")
            raise DatabaseQueryError(f"Failed to add purchase: {e}")

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
            with self.get_connection() as conn:
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
            with self.get_connection() as conn:
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

    def update_item(self, item: Item) -> None:
        """Update an existing item in the database.
        
        Args:
            item (Item): The updated item
            
        Raises:
            DatabaseQueryError: If update fails
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                now = datetime.now().isoformat()
                
                cursor.execute('''
                UPDATE items 
                SET name = ?, purchase_price = ?, date_of_purchase = ?, 
                    current_value = ?, profit_loss = ?, category = ?, updated_at = ?
                WHERE id = ?
                ''', (item.name, item.purchase_price, item.date_of_purchase,
                      item.current_value, item.profit_loss, item.category, now, item.id))
                
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error updating item: {e}")
            raise DatabaseQueryError(f"Failed to update item: {e}")

    def delete_item(self, item_id: int) -> None:
        """Delete an item and its associated purchases from the database.
        
        Args:
            item_id (int): ID of the item to delete
            
        Raises:
            DatabaseQueryError: If deletion fails
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Delete associated purchases first
                cursor.execute('DELETE FROM purchases WHERE item_id = ?', (item_id,))
                
                # Delete the item
                cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
                
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error deleting item: {e}")
            raise DatabaseQueryError(f"Failed to delete item: {e}")

    def clear_all_data(self) -> None:
        """Clear all data from the database.
        
        This will remove all items and their associated purchases.
        Use with caution as this operation cannot be undone.
        
        Raises:
            DatabaseQueryError: If clearing fails
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM purchases')
                cursor.execute('DELETE FROM items')
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error clearing database: {e}")
            raise DatabaseQueryError(f"Failed to clear database: {e}") 