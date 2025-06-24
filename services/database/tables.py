"""
Personal Finance Manager - Database Tables Module

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

from .base import DatabaseManager
from utils.logging import get_logger

# Initialize logger for this module
logger = get_logger(__name__)


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