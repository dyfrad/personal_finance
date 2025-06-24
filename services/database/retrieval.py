"""Data retrieval and query operations."""

from typing import List, Tuple

from .base import DatabaseManager
from utils.logging import get_logger

# Initialize logger for this module
logger = get_logger(__name__)


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