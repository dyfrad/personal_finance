"""
Personal Finance Manager - Database Purchases Module

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

from typing import List, Tuple, Any

from .base import DatabaseManager
from utils.logging import get_logger

# Initialize logger for this module
logger = get_logger(__name__)


class PurchaseOperations(DatabaseManager):
    """Handles purchase-related operations."""
    
    def add_purchase(self, item_id: int, purchase: Any, table_name: str = 'investments') -> None:
        """Add a purchase record for an item."""
        logger.info(f"Adding purchase for item ID {item_id}: {purchase.amount} units at ${purchase.price} on {purchase.date}")
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO purchases (item_id, table_name, date, amount, price)
            VALUES (?, ?, ?, ?, ?)
            ''', (item_id, table_name, purchase.date, purchase.amount, purchase.price))
            purchase_id = cursor.lastrowid
            conn.commit()
            
        logger.info(f"Successfully added purchase with ID {purchase_id} for item {item_id}")
    
    def get_purchases_for_item(self, item_id: int, table_name: str = 'investments') -> List[Tuple]:
        """Retrieve all purchase records for a specific item."""
        logger.debug(f"Retrieving purchases for item ID {item_id} from table '{table_name}'")
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT date, amount, price FROM purchases WHERE item_id = ? AND table_name = ?', 
                          (item_id, table_name))
            rows = cursor.fetchall()
        
        logger.debug(f"Retrieved {len(rows)} purchase records for item ID {item_id}")
        return rows
    
    def clear_all_purchases(self) -> int:
        """Clear all purchase records from the database."""
        logger.warning("Clearing ALL purchase records from database")
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM purchases')
            count = cursor.fetchone()[0]
            cursor.execute('DELETE FROM purchases')
            conn.commit()
        
        logger.warning(f"Cleared {count} purchase records from database")
        return count 