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
import logging
from utils.logging import get_logger

# Initialize logger for this module
logger = get_logger(__name__)

class Database:
    """
    Database management class for the Personal Finance Manager application.

    This module provides a comprehensive database interface for managing
    financial items including investments, inventory, and expenses.
    
    Handles all database operations including creating tables, inserting/updating/deleting
    items and purchases, and retrieving data. Uses SQLite as the backend database.
    
    Attributes:
        db_name (str): Name of the SQLite database file
    """
    
    # Category mappings for table selection
    INVESTMENT_CATEGORIES = ['Stocks', 'Bonds', 'Crypto', 'Real Estate', 'Gold']
    INVENTORY_CATEGORIES = ['Appliances', 'Electronics', 'Furniture', 'Transportation', 
                           'Home Improvement', 'Savings', 'Collectibles']
    EXPENSE_CATEGORIES = ['Expense']
    
    def __init__(self, db_name="finance.db"):
        """Initialize the database connection.
        
        Args:
            db_name (str): Name of the SQLite database file. Defaults to "finance.db"
        """
        self.db_name = db_name
        logger.info(f"Initializing database with file: {db_name}")
        try:
            self.init_db()
            logger.info("Database initialization completed successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    def init_db(self):
        """Initialize the database with required tables.
        
        Creates three category-specific tables:
        1. investments: Stores investment items (stocks, bonds, etc.)
        2. inventory: Stores inventory items (appliances, electronics, etc.)
        3. expenses: Stores expense items
        4. purchases: Stores purchase records for investments
        """
        logger.debug("Starting database table initialization")
        try:
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
            logger.debug("Created/verified investments table")
            
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
            logger.debug("Created/verified inventory table")
            
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
            logger.debug("Created/verified expenses table")
            
            # Create purchases table for stocks/bonds
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS purchases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER NOT NULL,
                table_name TEXT NOT NULL DEFAULT 'investments',
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                price REAL NOT NULL
            )
            ''')
            logger.debug("Created/verified purchases table")
            
            conn.commit()
            conn.close()
            logger.info("All database tables created/verified successfully")
            
        except sqlite3.Error as e:
            logger.error(f"SQLite error during table initialization: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during table initialization: {e}")
            raise

    def _get_table_name(self, category):
        """Get the appropriate table name based on item category.
        
        Args:
            category (str): Item category
            
        Returns:
            str: Table name to use for this category
        """
        logger.debug(f"Determining table name for category: {category}")
        if category in self.INVESTMENT_CATEGORIES:
            table_name = 'investments'
        elif category in self.INVENTORY_CATEGORIES:
            table_name = 'inventory'
        elif category in self.EXPENSE_CATEGORIES:
            table_name = 'expenses'
        else:
            logger.error(f"Unknown category: {category}")
            raise ValueError(f"Unknown category: {category}")
        
        logger.debug(f"Category '{category}' mapped to table '{table_name}'")
        return table_name

    def _get_db_connection(self):
        """Get a database connection with automatic commit and close.
        
        Returns:
            sqlite3.Connection: Database connection
        """
        try:
            conn = sqlite3.connect(self.db_name)
            logger.debug(f"Database connection established to {self.db_name}")
            return conn
        except sqlite3.Error as e:
            logger.error(f"Failed to connect to database {self.db_name}: {e}")
            raise

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
        logger.info(f"Inserting new item: {name} (category: {category})")
        try:
            table_name = self._get_table_name(category)
            conn = self._get_db_connection()
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
            logger.info(f"Successfully inserted item '{name}' with ID {item_id} in table '{table_name}'")
            return item_id
        except sqlite3.Error as e:
            logger.error(f"SQLite error inserting item '{name}': {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error inserting item '{name}': {e}")
            raise

    def get_item_by_id(self, item_id):
        """Retrieve an item by its ID from any table.
        
        Args:
            item_id (int): ID of the item to retrieve
            
        Returns:
            tuple: Row containing item data, or None if not found
        """
        logger.debug(f"Retrieving item with ID: {item_id}")
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor()
            
            # Search in all category-specific tables
            tables = ['investments', 'inventory', 'expenses']
            for table in tables:
                logger.debug(f"Searching for item ID {item_id} in table '{table}'")
                cursor.execute(f'SELECT * FROM {table} WHERE id = ?', (item_id,))
                row = cursor.fetchone()
                if row:
                    conn.close()
                    logger.info(f"Found item ID {item_id} in table '{table}'")
                    return row
            
            conn.close()
            logger.warning(f"Item with ID {item_id} not found in any table")
            return None
        except sqlite3.Error as e:
            logger.error(f"SQLite error retrieving item ID {item_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error retrieving item ID {item_id}: {e}")
            raise

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
        logger.info(f"Updating item ID {item_id}: {name} (category: {category})")
        try:
            table_name = self._get_table_name(category)
            conn = self._get_db_connection()
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
            conn.close()
            
            if rows_affected > 0:
                logger.info(f"Successfully updated item ID {item_id} in table '{table_name}'")
            else:
                logger.warning(f"No rows affected when updating item ID {item_id}")
        except sqlite3.Error as e:
            logger.error(f"SQLite error updating item ID {item_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error updating item ID {item_id}: {e}")
            raise

    def delete_item(self, item_id):
        """Delete an item and its associated purchases from the database.
        
        Args:
            item_id (int): ID of the item to delete
        """
        logger.info(f"Deleting item ID {item_id} and associated purchases")
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor()
            
            # Delete from all category-specific tables (only one will have the item)
            tables = ['investments', 'inventory', 'expenses']
            item_deleted = False
            for table in tables:
                cursor.execute(f'DELETE FROM {table} WHERE id = ?', (item_id,))
                if cursor.rowcount > 0:
                    logger.debug(f"Deleted item ID {item_id} from table '{table}'")
                    item_deleted = True
            
            # Also delete any associated purchases
            cursor.execute('DELETE FROM purchases WHERE item_id = ?', (item_id,))
            purchases_deleted = cursor.rowcount
            if purchases_deleted > 0:
                logger.debug(f"Deleted {purchases_deleted} purchase records for item ID {item_id}")
            
            conn.commit()
            conn.close()
            
            if item_deleted:
                logger.info(f"Successfully deleted item ID {item_id} and {purchases_deleted} associated purchases")
            else:
                logger.warning(f"No item found with ID {item_id} to delete")
        except sqlite3.Error as e:
            logger.error(f"SQLite error deleting item ID {item_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error deleting item ID {item_id}: {e}")
            raise

    def clear_all_items(self):
        """Clear all items from all tables.
        
        This will remove all items and their associated purchases from all tables.
        Use with caution as this operation cannot be undone.
        """
        logger.warning("Clearing ALL items from database - this cannot be undone")
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor()
            
            # Clear all category-specific tables
            tables = ['investments', 'inventory', 'expenses']
            total_items_deleted = 0
            for table in tables:
                cursor.execute(f'SELECT COUNT(*) FROM {table}')
                count = cursor.fetchone()[0]
                cursor.execute(f'DELETE FROM {table}')
                total_items_deleted += count
                logger.debug(f"Cleared {count} items from table '{table}'")
            
            # Clear purchases table
            cursor.execute('SELECT COUNT(*) FROM purchases')
            purchases_count = cursor.fetchone()[0]
            cursor.execute('DELETE FROM purchases')
            logger.debug(f"Cleared {purchases_count} purchase records")
            
            conn.commit()
            conn.close()
            logger.warning(f"Database cleared: {total_items_deleted} items and {purchases_count} purchases deleted")
        except sqlite3.Error as e:
            logger.error(f"SQLite error clearing database: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error clearing database: {e}")
            raise

    def add_purchase(self, item_id, purchase, table_name='investments'):
        """Add a purchase record for an item.
        
        Args:
            item_id (int): ID of the item this purchase belongs to
            purchase (object): Purchase object with date, amount, and price attributes
            table_name (str): Name of the table the item belongs to ('investments' or 'inventory')
        """
        logger.info(f"Adding purchase for item ID {item_id}: {purchase.amount} units at ${purchase.price} on {purchase.date}")
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO purchases (item_id, table_name, date, amount, price)
            VALUES (?, ?, ?, ?, ?)
            ''', (item_id, table_name, purchase.date, purchase.amount, purchase.price))
            purchase_id = cursor.lastrowid
            conn.commit()
            conn.close()
            logger.info(f"Successfully added purchase with ID {purchase_id} for item {item_id}")
        except sqlite3.Error as e:
            logger.error(f"SQLite error adding purchase for item ID {item_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error adding purchase for item ID {item_id}: {e}")
            raise

    def get_purchases_for_item(self, item_id, table_name='investments'):
        """Retrieve all purchase records for a specific item.
        
        Args:
            item_id (int): ID of the item to get purchases for
            table_name (str): Name of the table the item belongs to ('investments' or 'inventory')
            
        Returns:
            list: List of tuples containing (date, amount, price) for each purchase
        """
        logger.debug(f"Retrieving purchases for item ID {item_id} from table '{table_name}'")
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT date, amount, price FROM purchases WHERE item_id = ? AND table_name = ?', (item_id, table_name))
            rows = cursor.fetchall()
            conn.close()
            logger.debug(f"Retrieved {len(rows)} purchase records for item ID {item_id}")
            return rows
        except sqlite3.Error as e:
            logger.error(f"SQLite error retrieving purchases for item ID {item_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error retrieving purchases for item ID {item_id}: {e}")
            raise

    def add_mock_data(self, mock_items):
        """Add mock data to the database for testing purposes.
        
        Args:
            mock_items (list): List of Item objects to add to the database
        """
        logger.info(f"Adding {len(mock_items)} mock items to database")
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            items_added = 0
            purchases_added = 0
            
            for item in mock_items:
                # For simple items, use their direct attributes
                if item.category not in ['Stocks', 'Bonds']:
                    item_id = self.insert_base_item(
                        item.name, item.purchase_price, item.date_of_purchase,
                        item.current_value, item.profit_loss, item.category, now, now
                    )
                    items_added += 1
                else: # For stocks/bonds, insert a base item first, then add purchases
                    # Placeholder values for main item table
                    item_id = self.insert_base_item(
                        item.name, 0.0, "", 0.0, 0.0, item.category, now, now
                    )
                    items_added += 1
                    # Insert purchases if present
                    if hasattr(item, 'purchases'):
                        for purchase in item.purchases:
                            cursor.execute('''
                            INSERT INTO purchases (item_id, table_name, date, amount, price)
                            VALUES (?, ?, ?, ?, ?)
                            ''', (item_id, 'investments', purchase.date, purchase.amount, purchase.price))
                            purchases_added += 1
            conn.commit()
            conn.close()
            logger.info(f"Successfully added {items_added} mock items and {purchases_added} purchase records")
        except sqlite3.Error as e:
            logger.error(f"SQLite error adding mock data: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error adding mock data: {e}")
            raise

    def clear_all_purchases(self):
        """Clear all purchase records from the database.
        
        This will remove all purchase records while keeping the items table intact.
        Use with caution as this operation cannot be undone.
        """
        logger.warning("Clearing ALL purchase records from database")
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM purchases')
            count = cursor.fetchone()[0]
            cursor.execute('DELETE FROM purchases')
            conn.commit()
            conn.close()
            logger.warning(f"Cleared {count} purchase records from database")
        except sqlite3.Error as e:
            logger.error(f"SQLite error clearing purchases: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error clearing purchases: {e}")
            raise

    def get_all_items(self):
        """Retrieve all items from all category-specific tables.
        
        Returns:
            list: List of tuples containing all item data from all tables
        """
        logger.debug("Retrieving all items from all tables")
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor()
            
            all_items = []
            tables = ['investments', 'inventory', 'expenses']
            
            for table in tables:
                cursor.execute(f'SELECT * FROM {table}')
                rows = cursor.fetchall()
                all_items.extend(rows)
                logger.debug(f"Retrieved {len(rows)} items from table '{table}'")
            
            conn.close()
            logger.info(f"Retrieved total of {len(all_items)} items from all tables")
            return all_items
        except sqlite3.Error as e:
            logger.error(f"SQLite error retrieving all items: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error retrieving all items: {e}")
            raise

    def get_items_by_category(self, category_type):
        """Retrieve items by category type (investments, inventory, or expenses).
        
        Args:
            category_type (str): Type of items to retrieve ('Investment', 'Inventory', or 'Expense')
            
        Returns:
            list: List of tuples containing item data for the specified category type
        """
        logger.debug(f"Retrieving items by category type: {category_type}")
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor()
            
            if category_type == "Investment":
                cursor.execute('SELECT * FROM investments')
                table_name = 'investments'
            elif category_type == "Inventory":
                cursor.execute('SELECT * FROM inventory')
                table_name = 'inventory'
            elif category_type == "Expense":
                cursor.execute('SELECT * FROM expenses')
                table_name = 'expenses'
            else:
                logger.warning(f"Unknown category type '{category_type}', returning all items")
                # Return all items if category_type is not recognized
                return self.get_all_items()
                
            rows = cursor.fetchall()
            conn.close()
            logger.info(f"Retrieved {len(rows)} items from '{table_name}' table")
            return rows
        except sqlite3.Error as e:
            logger.error(f"SQLite error retrieving items by category '{category_type}': {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error retrieving items by category '{category_type}': {e}")
            raise

    def get_table_items(self, table_name):
        """Retrieve all items from a specific table.
        
        Args:
            table_name (str): Name of the table to query
            
        Returns:
            list: List of tuples containing item data from the specified table
        """
        logger.debug(f"Retrieving all items from table: {table_name}")
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM {table_name}')
            rows = cursor.fetchall()
            conn.close()
            logger.info(f"Retrieved {len(rows)} items from table '{table_name}'")
            return rows
        except sqlite3.Error as e:
            logger.error(f"SQLite error retrieving items from table '{table_name}': {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error retrieving items from table '{table_name}': {e}")
            raise 