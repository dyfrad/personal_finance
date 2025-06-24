"""
Personal Finance Manager - Database Maintenance Module

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
from typing import List, Tuple, Any

from .base import DatabaseManager
from .items import ItemOperations
from utils.logging import get_logger

# Initialize logger for this module
logger = get_logger(__name__)


class DataMaintenance(DatabaseManager):
    """Handles data maintenance operations."""
    
    def clear_all_items(self) -> Tuple[int, int]:
        """Clear all items from all tables."""
        logger.warning("Clearing ALL items from database - this cannot be undone")
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Clear all item tables
            total_items_deleted = 0
            for table in ['investments', 'inventory', 'expenses']:
                cursor.execute(f'SELECT COUNT(*) FROM {table}')
                count = cursor.fetchone()[0]
                cursor.execute(f'DELETE FROM {table}')
                total_items_deleted += count
                logger.debug(f"Cleared {count} items from table '{table}'")
            
            # Clear purchases table
            cursor.execute('SELECT COUNT(*) FROM purchases')
            purchases_count = cursor.fetchone()[0]
            cursor.execute('DELETE FROM purchases')
            
            conn.commit()
        
        logger.warning(f"Database cleared: {total_items_deleted} items and {purchases_count} purchases deleted")
        return total_items_deleted, purchases_count
    
    def add_mock_data(self, mock_items: List[Any]) -> Tuple[int, int]:
        """Add mock data to the database for testing purposes."""
        logger.info(f"Adding {len(mock_items)} mock items to database")
        
        now = datetime.now().isoformat()
        items_added = 0
        purchases_added = 0
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            for item in mock_items:
                # For simple items, use their direct attributes
                if item.category not in ['Stocks', 'Bonds']:
                    item_id = self._insert_mock_item(item, now)
                    items_added += 1
                else:
                    # For stocks/bonds, insert a base item first, then add purchases
                    item_id = self._insert_mock_item_with_purchases(item, now, cursor)
                    items_added += 1
                    if hasattr(item, 'purchases'):
                        purchases_added += len(item.purchases)
            
            conn.commit()
        
        logger.info(f"Successfully added {items_added} mock items and {purchases_added} purchase records")
        return items_added, purchases_added
    
    def _insert_mock_item(self, item: Any, timestamp: str) -> int:
        """Insert a simple mock item."""
        item_ops = ItemOperations(self.db_name)
        return item_ops.insert_item(
            item.name, item.purchase_price, item.date_of_purchase,
            item.current_value, item.profit_loss, item.category, timestamp, timestamp
        )
    
    def _insert_mock_item_with_purchases(self, item: Any, timestamp: str, cursor: sqlite3.Cursor) -> int:
        """Insert a mock item with purchases."""
        item_ops = ItemOperations(self.db_name)
        # Placeholder values for main item table
        item_id = item_ops.insert_item(
            item.name, 0.0, "", 0.0, 0.0, item.category, timestamp, timestamp
        )
        
        # Insert purchases if present
        if hasattr(item, 'purchases'):
            for purchase in item.purchases:
                cursor.execute('''
                INSERT INTO purchases (item_id, table_name, date, amount, price)
                VALUES (?, ?, ?, ?, ?)
                ''', (item_id, 'investments', purchase.date, purchase.amount, purchase.price))
        
        return item_id 