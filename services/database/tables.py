"""Database table management and schema operations."""

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