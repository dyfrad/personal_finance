import sqlite3
from datetime import datetime

class Database:
    """Database management class for the personal finance application.
    
    Handles all database operations including creating tables, inserting/updating/deleting
    items and purchases, and retrieving data. Uses SQLite as the backend database.
    
    Attributes:
        db_name (str): Name of the SQLite database file
    """
    
    def __init__(self, db_name="finance.db"):
        """Initialize the database connection.
        
        Args:
            db_name (str): Name of the SQLite database file. Defaults to "finance.db"
        """
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        """Initialize the database with required tables.
        
        Creates two tables if they don't exist:
        1. items: Stores basic item information
        2. purchases: Stores purchase records for stocks and bonds
        """
        conn = sqlite3.connect(self.db_name)
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
            FOREIGN KEY(item_id) REFERENCES items(id)
        )
        ''')
        conn.commit()
        conn.close()

    def insert_base_item(self, name, purchase_price, date_of_purchase, current_value, profit_loss, category, created_at, updated_at):
        """Insert a base item into the items table.
        
        Args:
            name (str): Name of the item
            purchase_price (float): Initial purchase price
            date_of_purchase (str): Date of purchase in ISO format
            current_value (float): Current market value
            profit_loss (float): Current profit/loss amount
            category (str): Item category (e.g., 'Stocks', 'Bonds', 'Appliances')
            created_at (str): Creation timestamp in ISO format
            updated_at (str): Last update timestamp in ISO format
            
        Returns:
            int: ID of the newly inserted item
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO items (name, purchase_price, date_of_purchase, current_value, 
                         profit_loss, category, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, purchase_price, date_of_purchase, 
              current_value, profit_loss, category, created_at, updated_at))
        item_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return item_id

    def get_last_inserted_item_id(self):
        """Get the ID of the last inserted item.
        
        Returns:
            int: ID of the most recently inserted item
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT last_insert_rowid()")
        item_id = cursor.fetchone()[0]
        conn.close()
        return item_id

    def get_item_by_id(self, item_id):
        """Retrieve an item by its ID.
        
        Args:
            item_id (int): ID of the item to retrieve
            
        Returns:
            tuple: Row containing item data, or None if not found
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,))
        row = cursor.fetchone()
        conn.close()
        return row

    def update_base_item(self, item_id, name, purchase_price, date_of_purchase, current_value, profit_loss, category, updated_at):
        """Update an existing item in the database.
        
        Args:
            item_id (int): ID of the item to update
            name (str): New name of the item
            purchase_price (float): New purchase price
            date_of_purchase (str): New purchase date in ISO format
            current_value (float): New current value
            profit_loss (float): New profit/loss amount
            category (str): New category
            updated_at (str): Update timestamp in ISO format
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE items 
        SET name = ?, purchase_price = ?, date_of_purchase = ?, 
            current_value = ?, profit_loss = ?, category = ?, updated_at = ?
        WHERE id = ?
        ''', (name, purchase_price, date_of_purchase,
              current_value, profit_loss, category, updated_at, item_id))
        conn.commit()
        conn.close()

    def delete_item(self, item_id):
        """Delete an item and its associated purchases from the database.
        
        Args:
            item_id (int): ID of the item to delete
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
        
        conn.commit()
        conn.close()

    def clear_all_items(self):
        """Clear all items from the database.
        
        This will remove all items and their associated purchases.
        Use with caution as this operation cannot be undone.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM items')
        conn.commit()
        conn.close()

    def add_purchase(self, item_id, purchase):
        """Add a purchase record for a stock or bond.
        
        Args:
            item_id (int): ID of the item this purchase belongs to
            purchase (object): Purchase object with date, amount, and price attributes
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO purchases (item_id, date, amount, price)
        VALUES (?, ?, ?, ?)
        ''', (item_id, purchase.date, purchase.amount, purchase.price))
        conn.commit()
        conn.close()

    def get_purchases_for_item(self, item_id):
        """Retrieve all purchase records for a specific item.
        
        Args:
            item_id (int): ID of the item to get purchases for
            
        Returns:
            list: List of tuples containing (date, amount, price) for each purchase
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT date, amount, price FROM purchases WHERE item_id = ?', (item_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def add_mock_data(self, mock_items):
        """Add mock data to the database for testing purposes.
        
        Args:
            mock_items (list): List of Item objects to add to the database
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        for item in mock_items:
            # For simple items, use their direct attributes
            if item.category not in ['Stocks', 'Bonds']:
                item_id = self.insert_base_item(
                    item.name, item.purchase_price, item.date_of_purchase,
                    item.current_value, item.profit_loss, item.category, now, now
                )
            else: # For stocks/bonds, insert a base item first, then add purchases
                # Placeholder values for main item table
                item_id = self.insert_base_item(
                    item.name, 0.0, "", 0.0, 0.0, item.category, now, now
                )
                # Insert purchases if present
                if hasattr(item, 'purchases'):
                    for purchase in item.purchases:
                        cursor.execute('''
                        INSERT INTO purchases (item_id, date, amount, price)
                        VALUES (?, ?, ?, ?)
                        ''', (item_id, purchase.date, purchase.amount, purchase.price))
        conn.commit()
        conn.close()

    def clear_all_purchases(self):
        """Clear all purchase records from the database.
        
        This will remove all purchase records while keeping the items table intact.
        Use with caution as this operation cannot be undone.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM purchases')
        conn.commit()
        conn.close()

    def get_all_items(self):
        """Retrieve all items from the database.
        
        Returns:
            list: List of tuples containing all item data
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items')
        rows = cursor.fetchall()
        conn.close()
        return rows 