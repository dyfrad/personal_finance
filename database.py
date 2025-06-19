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
        
        Creates four tables if they don't exist:
        1. investments: Stores investment items (stocks, bonds, etc.)
        2. inventory: Stores inventory items (appliances, electronics, etc.)
        3. expenses: Stores expense items
        4. purchases: Stores purchase records for investments
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Create investments table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS investments (
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
        
        # Create inventory table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
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
        
        # Create expenses table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
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
        
        # Create purchases table (for investment transactions)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY(item_id) REFERENCES investments(id)
        )
        ''')
        
        # Keep the old items table for now to allow migration
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
        
        conn.commit()
        conn.close()

    def _get_table_name(self, category):
        """Get the appropriate table name based on item category.
        
        Args:
            category (str): Item category
            
        Returns:
            str: Table name to use for this category
        """
        if category in ['Stocks', 'Bonds', 'Crypto', 'Real Estate', 'Gold']:
            return 'investments'
        elif category in ['Appliances', 'Electronics', 'Furniture', 'Transportation', 
                         'Home Improvement', 'Savings', 'Collectibles']:
            return 'inventory'
        elif category == 'Expense':
            return 'expenses'
        else:
            # Default fallback
            return 'items'

    def insert_base_item(self, name, purchase_price, date_of_purchase, current_value, profit_loss, category, created_at, updated_at):
        """Insert a base item into the appropriate table based on category.
        
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
        table_name = self._get_table_name(category)
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f'''
        INSERT INTO {table_name} (name, purchase_price, date_of_purchase, current_value, 
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
        """Retrieve an item by its ID from any table.
        
        Args:
            item_id (int): ID of the item to retrieve
            
        Returns:
            tuple: Row containing item data, or None if not found
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Search in all tables
        tables = ['investments', 'inventory', 'expenses', 'items']
        for table in tables:
            cursor.execute(f'SELECT * FROM {table} WHERE id = ?', (item_id,))
            row = cursor.fetchone()
            if row:
                conn.close()
                return row
        
        conn.close()
        return None

    def update_base_item(self, item_id, name, purchase_price, date_of_purchase, current_value, profit_loss, category, updated_at):
        """Update an existing item in the appropriate table.
        
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
        table_name = self._get_table_name(category)
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f'''
        UPDATE {table_name} 
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
        
        # Delete from all tables (only one will have the item)
        tables = ['investments', 'inventory', 'expenses', 'items']
        for table in tables:
            cursor.execute(f'DELETE FROM {table} WHERE id = ?', (item_id,))
        
        # Also delete any associated purchases
        cursor.execute('DELETE FROM purchases WHERE item_id = ?', (item_id,))
        
        conn.commit()
        conn.close()

    def clear_all_items(self):
        """Clear all items from all tables.
        
        This will remove all items and their associated purchases from all tables.
        Use with caution as this operation cannot be undone.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Clear all item tables
        tables = ['investments', 'inventory', 'expenses', 'items']
        for table in tables:
            cursor.execute(f'DELETE FROM {table}')
        
        # Clear purchases table
        cursor.execute('DELETE FROM purchases')
        
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
        """Retrieve all items from all tables.
        
        Returns:
            list: List of tuples containing all item data from all tables
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        all_items = []
        tables = ['investments', 'inventory', 'expenses', 'items']
        
        for table in tables:
            cursor.execute(f'SELECT * FROM {table}')
            rows = cursor.fetchall()
            all_items.extend(rows)
        
        conn.close()
        return all_items

    def get_items_by_category(self, category_type):
        """Retrieve items by category type (investments, inventory, or expenses).
        
        Args:
            category_type (str): Type of items to retrieve ('Investment', 'Inventory', or 'Expense')
            
        Returns:
            list: List of tuples containing item data for the specified category type
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        if category_type == "Investment":
            cursor.execute('SELECT * FROM investments')
        elif category_type == "Inventory":
            cursor.execute('SELECT * FROM inventory')
        elif category_type == "Expense":
            cursor.execute('SELECT * FROM expenses')
        else:
            # Return all items if category_type is not recognized
            return self.get_all_items()
            
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_table_items(self, table_name):
        """Retrieve all items from a specific table.
        
        Args:
            table_name (str): Name of the table to query
            
        Returns:
            list: List of tuples containing item data from the specified table
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {table_name}')
        rows = cursor.fetchall()
        conn.close()
        return rows

    def migrate_items_to_category_tables(self):
        """Migrate existing items from the items table to category-specific tables.
        
        This method moves items from the generic 'items' table to the appropriate
        category-specific tables (investments, inventory, expenses) based on their category.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Get all items from the old items table
        cursor.execute('SELECT * FROM items')
        items = cursor.fetchall()
        
        migrated_count = 0
        for item in items:
            # item structure: (id, name, purchase_price, date_of_purchase, current_value, profit_loss, category, created_at, updated_at)
            item_id, name, purchase_price, date_of_purchase, current_value, profit_loss, category, created_at, updated_at = item
            
            # Determine target table
            table_name = self._get_table_name(category)
            
            # Skip if it would go back to items table (unknown category)
            if table_name == 'items':
                continue
                
            # Insert into appropriate table
            cursor.execute(f'''
            INSERT INTO {table_name} (name, purchase_price, date_of_purchase, current_value, 
                             profit_loss, category, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, purchase_price, date_of_purchase, current_value, profit_loss, category, created_at, updated_at))
            
            new_item_id = cursor.lastrowid
            
            # For investments, migrate associated purchases
            if table_name == 'investments':
                cursor.execute('SELECT * FROM purchases WHERE item_id = ?', (item_id,))
                purchases = cursor.fetchall()
                for purchase in purchases:
                    # purchase structure: (id, item_id, date, amount, price)
                    _, _, date, amount, price = purchase
                    cursor.execute('''
                    INSERT INTO purchases (item_id, date, amount, price)
                    VALUES (?, ?, ?, ?)
                    ''', (new_item_id, date, amount, price))
                
                # Delete old purchase records
                cursor.execute('DELETE FROM purchases WHERE item_id = ?', (item_id,))
            
            # Delete the item from the old table
            cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
            migrated_count += 1
        
        conn.commit()
        conn.close()
        
        print(f"Migration completed: {migrated_count} items moved to category-specific tables.")
        return migrated_count 