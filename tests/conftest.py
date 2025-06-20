import pytest
import os
import tempfile
from services.database import Database
from models.item import Item
from models.purchase import Purchase
from config.settings import ConfigManager
from utils.logging import setup_logging
import logging

@pytest.fixture
def temp_db():
    """Create a temporary database for testing.
    
    Yields:
        Database: Database instance connected to temporary database
    """
    # Create a temporary file for the database
    fd, path = tempfile.mkstemp()
    os.close(fd)
    
    # Create a test config manager with the temporary database path
    test_config = ConfigManager()
    test_config.config.database.db_name = path
    
    # Create database instance with config manager
    db = Database(config_manager=test_config)
    
    # Disable protection features for testing
    if hasattr(db, 'protection') and db.protection:
        db.protection.config["protection_enabled"] = False
        db.protection.config["auto_backup_enabled"] = False
    
    yield db
    
    # Clean up
    try:
        os.unlink(path)
    except FileNotFoundError:
        pass

@pytest.fixture
def sample_item():
    """Create a sample item for testing.
    
    Returns:
        Item: Sample item instance
    """
    return Item(
        name="Test Stock",
        category="Stocks",
        purchase_price=100.0,
        date_of_purchase="2024-01-01",
        current_value=150.0,
        profit_loss=50.0
    )

@pytest.fixture
def sample_purchase():
    """Create a sample purchase for testing.
    
    Returns:
        Purchase: Sample purchase instance
    """
    return Purchase(
        date="2024-01-01",
        amount=10.0,
        price=10.0
    )

@pytest.fixture
def config_manager():
    """Create a configuration manager for testing.
    
    Returns:
        ConfigManager: Configuration manager instance
    """
    return ConfigManager(config_file="test_config.json")

@pytest.fixture(autouse=True)
def setup_test_logging():
    """Set up logging for tests.
    
    This fixture runs automatically for all tests.
    """
    setup_logging()
    yield
    # Clean up logging handlers after test
    logging.getLogger().handlers = [] 