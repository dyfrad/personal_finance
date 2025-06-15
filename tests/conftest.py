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
    
    # Create database instance
    db = Database(db_name=path)
    
    yield db
    
    # Clean up
    os.unlink(path)

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