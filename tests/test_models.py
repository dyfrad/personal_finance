"""Unit tests for data models."""

import pytest
from datetime import datetime
from models.item import Item
from models.purchase import Purchase

def test_item_creation():
    """Test creating an Item instance."""
    item = Item(
        name="Test Stock",
        category="Stocks",
        purchase_price=100.0,
        date_of_purchase="2024-01-01",
        current_value=150.0,
        profit_loss=50.0
    )
    
    assert item.name == "Test Stock"
    assert item.category == "Stocks"
    assert item.purchase_price == 100.0
    assert item.date_of_purchase == "2024-01-01"
    assert item.current_value == 150.0
    assert item.profit_loss == 50.0
    assert item.purchases == []

def test_item_add_purchase():
    """Test adding a purchase to an item."""
    item = Item(name="Test Stock", category="Stocks")
    purchase = Purchase(date="2024-01-01", amount=10.0, price=10.0)
    
    item.add_purchase(purchase)
    assert len(item.purchases) == 1
    assert item.purchases[0] == purchase

def test_item_get_total_invested():
    """Test calculating total invested amount."""
    # Test for regular item
    regular_item = Item(
        name="Test Appliance",
        category="Appliances",
        purchase_price=500.0
    )
    assert regular_item.get_total_invested() == 500.0
    
    # Test for stock with purchases
    stock_item = Item(name="Test Stock", category="Stocks")
    stock_item.add_purchase(Purchase(date="2024-01-01", amount=10.0, price=10.0))
    stock_item.add_purchase(Purchase(date="2024-01-02", amount=5.0, price=12.0))
    assert stock_item.get_total_invested() == 160.0  # Total invested: (10*10) + (5*12) = 160

def test_item_get_current_total_value():
    """Test calculating current total value."""
    # Test for regular item
    regular_item = Item(
        name="Test Appliance",
        category="Appliances",
        current_value=450.0
    )
    assert regular_item.get_current_total_value() == 450.0
    
    # Test for stock with purchases and current price
    stock_item = Item(name="Test Stock", category="Stocks")
    stock_item.add_purchase(Purchase(date="2024-01-01", amount=10.0, price=10.0))
    current_prices = {"Test Stock": 15.0}
    assert stock_item.get_current_total_value(current_prices) == 150.0  # 10 shares * $15

def test_item_get_overall_profit_loss():
    """Test calculating overall profit/loss."""
    # Test for regular item
    regular_item = Item(
        name="Test Appliance",
        category="Appliances",
        purchase_price=500.0,
        current_value=450.0
    )
    assert regular_item.get_overall_profit_loss() == -50.0  # Loss of $50
    
    # Test for stock with purchases and current price
    stock_item = Item(name="Test Stock", category="Stocks")
    stock_item.add_purchase(Purchase(date="2024-01-01", amount=10.0, price=10.0))
    current_prices = {"Test Stock": 15.0}
    assert stock_item.get_overall_profit_loss(current_prices) == 50.0  # Profit of $50

def test_item_to_dict():
    """Test converting item to dictionary."""
    item = Item(
        id=1,
        name="Test Stock",
        category="Stocks",
        purchase_price=100.0,
        date_of_purchase="2024-01-01",
        current_value=150.0,
        profit_loss=50.0,
        created_at=datetime(2024, 1, 1),
        updated_at=datetime(2024, 1, 1)
    )
    
    data = item.to_dict()
    assert data['id'] == 1
    assert data['name'] == "Test Stock"
    assert data['category'] == "Stocks"
    assert data['purchase_price'] == 100.0
    assert data['date_of_purchase'] == "2024-01-01"
    assert data['current_value'] == 150.0
    assert data['profit_loss'] == 50.0
    assert data['created_at'] == "2024-01-01T00:00:00"
    assert data['updated_at'] == "2024-01-01T00:00:00"

def test_item_from_dict():
    """Test creating item from dictionary."""
    data = {
        'id': 1,
        'name': "Test Stock",
        'category': "Stocks",
        'purchase_price': 100.0,
        'date_of_purchase': "2024-01-01",
        'current_value': 150.0,
        'profit_loss': 50.0,
        'created_at': "2024-01-01T00:00:00",
        'updated_at': "2024-01-01T00:00:00",
        'purchases': [
            {
                'date': "2024-01-01",
                'amount': 10.0,
                'price': 10.0
            }
        ]
    }
    
    item = Item.from_dict(data)
    assert item.id == 1
    assert item.name == "Test Stock"
    assert item.category == "Stocks"
    assert item.purchase_price == 100.0
    assert item.date_of_purchase == "2024-01-01"
    assert item.current_value == 150.0
    assert item.profit_loss == 50.0
    assert len(item.purchases) == 1
    assert item.purchases[0].date == "2024-01-01"
    assert item.purchases[0].amount == 10.0
    assert item.purchases[0].price == 10.0

def test_purchase_creation():
    """Test creating a Purchase instance."""
    purchase = Purchase(
        date="2024-01-01",
        amount=10.0,
        price=10.0
    )
    
    assert purchase.date == "2024-01-01"
    assert purchase.amount == 10.0
    assert purchase.price == 10.0

def test_purchase_get_total_value():
    """Test calculating total value of a purchase."""
    purchase = Purchase(
        date="2024-01-01",
        amount=10.0,
        price=10.0
    )
    
    assert purchase.get_total_value() == 100.0  # 10 shares * $10

def test_purchase_to_dict():
    """Test converting purchase to dictionary."""
    purchase = Purchase(
        id=1,
        date="2024-01-01",
        amount=10.0,
        price=10.0,
        created_at=datetime(2024, 1, 1),
        updated_at=datetime(2024, 1, 1)
    )
    
    data = purchase.to_dict()
    assert data['id'] == 1
    assert data['date'] == "2024-01-01"
    assert data['amount'] == 10.0
    assert data['price'] == 10.0
    assert data['created_at'] == "2024-01-01T00:00:00"
    assert data['updated_at'] == "2024-01-01T00:00:00"

def test_purchase_from_dict():
    """Test creating purchase from dictionary."""
    data = {
        'id': 1,
        'date': "2024-01-01",
        'amount': 10.0,
        'price': 10.0,
        'created_at': "2024-01-01T00:00:00",
        'updated_at': "2024-01-01T00:00:00"
    }
    
    purchase = Purchase.from_dict(data)
    assert purchase.id == 1
    assert purchase.date == "2024-01-01"
    assert purchase.amount == 10.0
    assert purchase.price == 10.0
    assert purchase.created_at == datetime(2024, 1, 1)
    assert purchase.updated_at == datetime(2024, 1, 1) 