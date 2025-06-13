import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="finance.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        """Initialize the database with required tables"""
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
        """Insert a base item into the items table and return its ID"""
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
        """Get the ID of the last inserted item"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT last_insert_rowid()")
        item_id = cursor.fetchone()[0]
        conn.close()
        return item_id

    def get_item_by_id(self, item_id):
        """Retrieve an item by its ID"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,))
        row = cursor.fetchone()
        conn.close()
        return row

    def update_base_item(self, item_id, name, purchase_price, date_of_purchase, current_value, profit_loss, category, updated_at):
        """Update an existing item in the database's items table"""
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
        """Delete an item from the database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
        
        conn.commit()
        conn.close()

    def clear_all_items(self):
        """Clear all items from the database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM items')
        conn.commit()
        conn.close()

    def add_purchase(self, item_id, purchase):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO purchases (item_id, date, amount, price)
        VALUES (?, ?, ?, ?)
        ''', (item_id, purchase.date, purchase.amount, purchase.price))
        conn.commit()
        conn.close()

    def get_purchases_for_item(self, item_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT date, amount, price FROM purchases WHERE item_id = ?', (item_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def add_mock_data(self, mock_items):
        conn = sqlite3.connect(self.db_name) # Open connection once
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
                        cursor.execute(''' # Use the same cursor for batch insert
                        INSERT INTO purchases (item_id, date, amount, price)
                        VALUES (?, ?, ?, ?)
                        ''', (item_id, purchase.date, purchase.amount, purchase.price))
        conn.commit() # Commit once after all inserts
        conn.close() # Close once after all inserts

    def clear_all_purchases(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM purchases')
        conn.commit()
        conn.close()

    def get_all_items(self):
        """Retrieve all items from the database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items')
        rows = cursor.fetchall()
        conn.close()
        return rows 