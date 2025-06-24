"""
Personal Finance Manager - Database Base Module

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
from contextlib import contextmanager

from .config import DatabaseConfig
from .exceptions import DatabaseError
from utils.logging import get_logger

# Initialize logger for this module
logger = get_logger(__name__)


class DatabaseManager:
    """Base database manager for common operations."""
    
    def __init__(self, db_name: str = "finance.db"):
        self.db_name = db_name
        self.config = DatabaseConfig()
        logger.info(f"Initializing database manager with file: {db_name}")
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            logger.debug(f"Database connection established to {self.db_name}")
            yield conn
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            if conn:
                conn.rollback()
            raise DatabaseError(f"Database operation failed: {e}")
        finally:
            if conn:
                conn.close()
                logger.debug("Database connection closed") 