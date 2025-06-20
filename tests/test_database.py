import pytest
import sqlite3
from datetime import datetime
from services.database import Database, DatabaseError, DatabaseConnectionError, DatabaseQueryError
from models.item import Item

def test_init_db(temp_db):
    """Test database initialization."""
    # Database should be initialized with required tables
    with temp_db._get_connection() as conn:
        cursor = conn.cursor()
        
        # Check items table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='items'")
        assert cursor.fetchone() is not None
        
        # Check purchases table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='purchases'")
        assert cursor.fetchone() is not None

def test_insert_and_get_item(temp_db, sample_item):
    """Test inserting and retrieving an item."""
    # Insert item
    item_id = temp_db.insert_base_item(sample_item)
    assert item_id is not None
    
    # Retrieve item
    retrieved_item = temp_db.get_item_by_id(item_id)
    assert retrieved_item is not None
    assert retrieved_item.name == sample_item.name
    assert retrieved_item.category == sample_item.category
    assert retrieved_item.purchase_price == sample_item.purchase_price

def test_add_purchase(temp_db, sample_item, sample_purchase):
    """Test adding a purchase to an item."""
    # Insert item first
    item_id = temp_db.insert_base_item(sample_item)
    
    # Add purchase
    purchase_id = temp_db.add_purchase(item_id, sample_purchase)
    assert purchase_id is not None
    
    # Retrieve item and check purchase
    retrieved_item = temp_db.get_item_by_id(item_id)
    assert len(retrieved_item.purchases) == 1
    assert retrieved_item.purchases[0].date == sample_purchase.date
    assert retrieved_item.purchases[0].amount == sample_purchase.amount
    assert retrieved_item.purchases[0].price == sample_purchase.price

def test_update_item(temp_db, sample_item):
    """Test updating an item."""
    # Insert item
    item_id = temp_db.insert_base_item(sample_item)
    
    # Update item
    sample_item.id = item_id
    sample_item.name = "Updated Name"
    temp_db.update_item(sample_item)
    
    # Retrieve and check
    retrieved_item = temp_db.get_item_by_id(item_id)
    assert retrieved_item.name == "Updated Name"

def test_delete_item(temp_db, sample_item, sample_purchase):
    """Test deleting an item and its purchases."""
    # Insert item and purchase
    item_id = temp_db.insert_base_item(sample_item)
    temp_db.add_purchase(item_id, sample_purchase)
    
    # Delete item
    temp_db.delete_item(item_id)
    
    # Verify deletion
    retrieved_item = temp_db.get_item_by_id(item_id)
    assert retrieved_item is None

def test_get_all_items(temp_db, sample_item):
    """Test retrieving all items."""
    # Insert multiple items
    item1 = sample_item
    item2 = Item(
        name="Test Bond",
        category="Bonds",
        purchase_price=200.0,
        date_of_purchase="2024-01-01",
        current_value=250.0,
        profit_loss=50.0
    )
    
    temp_db.insert_base_item(item1)
    temp_db.insert_base_item(item2)
    
    # Get all items
    items = temp_db.get_all_items()
    assert len(items) == 2
    assert any(item.name == "Test Stock" for item in items)
    assert any(item.name == "Test Bond" for item in items)

def test_clear_all_data(temp_db, sample_item, sample_purchase):
    """Test clearing all data from the database."""
    # Insert item and purchase
    item_id = temp_db.insert_base_item(sample_item)
    temp_db.add_purchase(item_id, sample_purchase)
    
    # Clear all data
    temp_db.clear_all_data()
    
    # Verify everything is cleared
    items = temp_db.get_all_items()
    assert len(items) == 0

def test_database_connection_error():
    """Test database connection error handling."""
    # Try to connect to a non-existent directory
    from config.settings import ConfigManager
    test_config = ConfigManager()
    test_config.config.database.db_name = "/non/existent/path/db.sqlite"
    # This should raise an exception during initialization
    with pytest.raises((DatabaseConnectionError, sqlite3.OperationalError)):
        db = Database(config_manager=test_config)

def test_database_query_error(temp_db):
    """Test database query error handling."""
    with pytest.raises(DatabaseQueryError):
        # Try to insert invalid data
        invalid_item = Item(
            name=None,  # This should cause an error
            category="Stocks",
            purchase_price=100.0,
            date_of_purchase="2024-01-01",
            current_value=150.0,
            profit_loss=50.0
        )
        temp_db.insert_base_item(invalid_item) 