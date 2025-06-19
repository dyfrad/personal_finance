import pytest
import sqlite3
import tempfile
import os
from services.database import Database, DatabaseError
from main import Item, Purchase

class TestCriticalAppFunctionality:
    """Test the most critical functionality that could cause app failures."""
    
    def test_database_item_insertion_and_retrieval(self, temp_db):
        """Test that items can be inserted and retrieved correctly."""
        # Create test item
        item = Item("Test Stock", "Stocks", 100.0, "2024-01-01", 150.0, 50.0)
        
        # Insert item
        item_id = temp_db.insert_base_item(item)
        assert item_id is not None, "Should return item ID"
        
        # Retrieve item
        retrieved_item = temp_db.get_item_by_id(item_id)
        assert retrieved_item is not None, "Should retrieve item"
        assert retrieved_item.name == "Test Stock", "Should retrieve correct item"
        assert retrieved_item.category == "Stocks", "Should preserve category"
    
    def test_purchase_system_integrity(self, temp_db):
        """Test that the purchase system works correctly for investments."""
        # Create investment item
        item = Item("AAPL", "Stocks", 0.0, "2024-01-01", 0.0, 0.0)
        item_id = temp_db.insert_base_item(item)
        
        # Add purchases
        purchase1 = Purchase("2024-01-01", 10.0, 100.0)
        purchase2 = Purchase("2024-01-02", 5.0, 110.0)
        
        temp_db.add_purchase(item_id, purchase1)
        temp_db.add_purchase(item_id, purchase2)
        
        # Retrieve item with purchases
        item_with_purchases = temp_db.get_item_by_id(item_id)
        assert len(item_with_purchases.purchases) == 2, "Should have 2 purchases"
        
        # Test calculations
        total_invested = item_with_purchases.get_total_invested()
        assert total_invested == 1550.0, "Total invested should be correct (10*100 + 5*110)"
    
    def test_item_deletion_integrity(self, temp_db):
        """Test that item deletion removes associated purchases."""
        # Create item with purchases
        item = Item("Test Delete", "Stocks", 100.0, "2024-01-01", 100.0, 0.0)
        item_id = temp_db.insert_base_item(item)
        
        purchase = Purchase("2024-01-01", 10.0, 100.0)
        temp_db.add_purchase(item_id, purchase)
        
        # Verify item and purchase exist
        retrieved_item = temp_db.get_item_by_id(item_id)
        assert retrieved_item is not None, "Item should exist"
        assert len(retrieved_item.purchases) == 1, "Should have purchase"
        
        # Delete item
        temp_db.delete_item(item_id)
        
        # Verify item is deleted
        deleted_item = temp_db.get_item_by_id(item_id)
        assert deleted_item is None, "Item should be deleted"
    
    def test_data_persistence(self, temp_db):
        """Test that data persists across database operations."""
        # Create and save data
        items = [
            Item("Stock 1", "Stocks", 100.0, "2024-01-01", 150.0, 50.0),
            Item("Appliance 1", "Appliances", 500.0, "2024-01-01", 450.0, -50.0),
            Item("Expense 1", "Expense", 50.0, "2024-01-01", 0.0, -50.0)
        ]
        
        item_ids = []
        for item in items:
            item_id = temp_db.insert_base_item(item)
            item_ids.append(item_id)
        
        # Get all items
        all_items = temp_db.get_all_items()
        assert len(all_items) == 3, "Should have 3 items"
        
        # Verify each item type exists
        categories = [item.category for item in all_items]
        assert "Stocks" in categories, "Should have stock item"
        assert "Appliances" in categories, "Should have appliance item"
        assert "Expense" in categories, "Should have expense item"

class TestErrorHandling:
    """Test error handling for critical failure scenarios."""
    
    def test_invalid_database_file(self):
        """Test handling of invalid database files."""
        # Create a corrupted database file
        fd, path = tempfile.mkstemp()
        os.close(fd)
        
        try:
            # Write garbage data to file
            with open(path, 'wb') as f:
                f.write(b'This is not a valid SQLite database')
            
            # Attempt to open - should handle gracefully
            with pytest.raises(DatabaseError):
                db = Database(db_name=path)
                
        finally:
            os.unlink(path)
    
    def test_database_query_error_handling(self, temp_db):
        """Test that database query errors are handled properly."""
        # Test invalid item ID
        result = temp_db.get_item_by_id(99999)
        assert result is None, "Should return None for non-existent item"
        
        # Test deletion of non-existent item should not crash
        temp_db.delete_item(99999)  # Should not raise exception

class TestBusinessLogicCritical:
    """Test critical business logic calculations."""
    
    def test_investment_calculations_accuracy(self):
        """Test that investment calculations are accurate."""
        item = Item("Test Investment", "Stocks")
        
        # Add purchases
        item.add_purchase(Purchase("2024-01-01", 10.0, 100.0))  # $1000
        item.add_purchase(Purchase("2024-01-02", 5.0, 120.0))   # $600
        
        # Test total invested
        total_invested = item.get_total_invested()
        assert total_invested == 1600.0, "Total invested calculation should be accurate"
        
        # Test current value calculation
        current_prices = {"Test Investment": 150.0}
        current_value = item.get_current_total_value(current_prices)
        expected_value = (10.0 + 5.0) * 150.0  # 15 shares * $150
        assert current_value == expected_value, "Current value calculation should be accurate"
        
        # Test profit/loss calculation
        profit_loss = item.get_overall_profit_loss(current_prices)
        expected_profit = expected_value - total_invested  # $2250 - $1600 = $650
        assert profit_loss == expected_profit, "Profit/loss calculation should be accurate"
    
    def test_inventory_item_handling(self):
        """Test that inventory items work correctly."""
        item = Item("MacBook", "Electronics", 2000.0, "2024-01-01", 1800.0, -200.0)
        
        assert item.get_total_invested() == 2000.0, "Should return purchase price"
        assert item.get_current_total_value() == 1800.0, "Should return current value"
        assert item.get_overall_profit_loss() == -200.0, "Should calculate loss correctly"
    
    def test_expense_item_handling(self):
        """Test that expense items work correctly."""
        expense = Item("Dinner", "Expense", 50.0, "2024-01-01", 0.0, -50.0)
        
        assert expense.get_total_invested() == 50.0, "Should track expense amount"
        assert expense.get_current_total_value() == 0.0, "Expenses have no current value"
        assert expense.get_overall_profit_loss() == -50.0, "Expenses are always losses"

class TestDataIntegrity:
    """Test data integrity across operations."""
    
    def test_item_id_uniqueness(self, temp_db):
        """Test that item IDs are unique."""
        # Create multiple items
        items = [
            Item(f"Item {i}", "Stocks", 100.0, "2024-01-01", 100.0, 0.0)
            for i in range(10)
        ]
        
        item_ids = []
        for item in items:
            item_id = temp_db.insert_base_item(item)
            item_ids.append(item_id)
        
        # All IDs should be unique
        assert len(item_ids) == len(set(item_ids)), "All item IDs should be unique"
    
    def test_data_consistency_after_operations(self, temp_db):
        """Test that data remains consistent after multiple operations."""
        # Create item
        item = Item("Consistency Test", "Stocks", 100.0, "2024-01-01", 100.0, 0.0)
        item_id = temp_db.insert_base_item(item)
        
        # Add purchase
        purchase = Purchase("2024-01-01", 10.0, 100.0)
        temp_db.add_purchase(item_id, purchase)
        
        # Update item
        updated_item = temp_db.get_item_by_id(item_id)
        updated_item.current_value = 150.0
        updated_item.profit_loss = 50.0
        temp_db.update_item(updated_item)
        
        # Verify consistency
        final_item = temp_db.get_item_by_id(item_id)
        assert final_item.current_value == 150.0, "Update should persist"
        assert len(final_item.purchases) == 1, "Purchases should be preserved"
        assert final_item.get_total_invested() == 1000.0, "Calculations should remain correct"

class TestSystemLimits:
    """Test system limits and performance."""
    
    def test_large_portfolio_handling(self, temp_db):
        """Test that the system can handle a reasonably large portfolio."""
        # Create 50 items (reasonable portfolio size)
        num_items = 50
        
        for i in range(num_items):
            item = Item(f"Item {i}", "Stocks", 100.0, "2024-01-01", 100.0, 0.0)
            temp_db.insert_base_item(item)
        
        # Verify all items were created
        all_items = temp_db.get_all_items()
        assert len(all_items) == num_items, f"Should handle {num_items} items"
        
        # Test that retrieval still works efficiently
        first_item = temp_db.get_item_by_id(1)
        assert first_item is not None, "Should still retrieve items efficiently"
    
    def test_many_purchases_per_item(self, temp_db):
        """Test that an item can handle many purchases."""
        # Create item
        item = Item("High Volume Stock", "Stocks", 0.0, "2024-01-01", 0.0, 0.0)
        item_id = temp_db.insert_base_item(item)
        
        # Add 20 purchases (reasonable for active trading)
        num_purchases = 20
        for i in range(num_purchases):
            purchase = Purchase(f"2024-01-{i+1:02d}", 10.0, 100.0 + i)
            temp_db.add_purchase(item_id, purchase)
        
        # Verify all purchases are recorded
        item_with_purchases = temp_db.get_item_by_id(item_id)
        assert len(item_with_purchases.purchases) == num_purchases, f"Should handle {num_purchases} purchases"
        
        # Verify calculations still work
        total_invested = item_with_purchases.get_total_invested()
        expected_total = sum(10.0 * (100.0 + i) for i in range(num_purchases))
        assert total_invested == expected_total, "Calculations should work with many purchases" 