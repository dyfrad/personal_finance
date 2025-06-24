"""Base database management functionality."""

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