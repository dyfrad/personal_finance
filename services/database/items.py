"""
Personal Finance Manager - Database Items Module

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

from typing import Optional, Tuple

from .base import DatabaseManager
from utils.logging import get_logger

# Initialize logger for this module
logger = get_logger(__name__)


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