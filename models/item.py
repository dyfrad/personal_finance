"""Financial item data models and portfolio management."""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from .purchase import Purchase

@dataclass
class Item:
    """Represents a financial item in the portfolio.
    
    This class can handle both regular items (like appliances) and financial instruments
    (like stocks and bonds). For stocks and bonds, it maintains a list of purchases.
    
    Attributes:
        id (Optional[int]): Database ID of the item
        name (str): Name of the item
        category (str): Category of the item (e.g., 'Stocks', 'Bonds', 'Appliances')
        purchase_price (float): Initial purchase price (for non-stock items)
        date_of_purchase (str): Date of purchase in YYYY-MM-DD format
        current_value (float): Current market value of the item
        profit_loss (float): Current profit/loss on the item
        purchases (List[Purchase]): List of Purchase objects (for stocks/bonds)
        created_at (datetime): Timestamp when the item was created
        updated_at (datetime): Timestamp when the item was last updated
    """
    id: Optional[int] = None
    name: str = ""
    category: str = ""
    purchase_price: float = 0.0
    date_of_purchase: str = ""
    current_value: float = 0.0
    profit_loss: float = 0.0
    purchases: List[Purchase] = None
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        """Initialize the purchases list if it's None."""
        if self.purchases is None:
            self.purchases = []

    def add_purchase(self, purchase: Purchase) -> None:
        """Adds a new purchase to the item's purchase history.
        
        Args:
            purchase (Purchase): A Purchase object containing purchase details
        """
        self.purchases.append(purchase)

    def get_total_invested(self) -> float:
        """Calculates the total amount invested in the item.
        
        If purchases exist, sums up all purchase amounts (quantity × price).
        Otherwise, returns the initial purchase price.
        
        Returns:
            float: Total amount invested in the item
        """
        if self.purchases:
            return sum(p.amount * p.price for p in self.purchases)
        return self.purchase_price

    def get_current_total_value(self, current_price_lookup: Optional[dict] = None) -> float:
        """Calculates the current total value of the item.
        
        If purchases exist and current prices are available for investments,
        calculates total value using current market prices. For inventory items
        with purchases, uses the most recent purchase price as current value.
        Otherwise, returns the stored current value.
        
        Args:
            current_price_lookup (dict, optional): Dictionary mapping item names to current prices
            
        Returns:
            float: Current total value of the item
        """
        if self.purchases:
            # For investments with current price lookup, use market prices
            if self.category in ['Stocks', 'Bonds', 'Crypto', 'Real Estate', 'Gold'] and current_price_lookup:
                if self.name in current_price_lookup:
                    price_per_unit = current_price_lookup[self.name]
                else:
                    price_per_unit = self.purchases[-1].price if self.purchases else 1
                return sum(p.amount * price_per_unit for p in self.purchases)
            else:
                # For inventory items or investments without market data, use purchase prices
                return sum(p.amount * p.price for p in self.purchases)
        return self.current_value

    def get_overall_profit_loss(self, current_price_lookup: Optional[dict] = None) -> float:
        """Calculates the overall profit/loss on the item.
        
        Args:
            current_price_lookup (dict, optional): Dictionary mapping item names to current prices
            
        Returns:
            float: Total profit/loss (positive for profit, negative for loss)
        """
        total_invested = self.get_total_invested()
        current_total_value = self.get_current_total_value(current_price_lookup)
        return current_total_value - total_invested

    def to_dict(self) -> dict:
        """Convert the item to a dictionary representation.
        
        Returns:
            dict: Dictionary representation of the item
        """
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'purchase_price': self.purchase_price,
            'date_of_purchase': self.date_of_purchase,
            'current_value': self.current_value,
            'profit_loss': self.profit_loss,
            'purchases': [p.to_dict() for p in self.purchases],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Item':
        """Create an Item instance from a dictionary.
        
        Args:
            data (dict): Dictionary containing item data
            
        Returns:
            Item: New Item instance
        """
        item = cls(
            id=data.get('id'),
            name=data['name'],
            category=data['category'],
            purchase_price=data['purchase_price'],
            date_of_purchase=data['date_of_purchase'],
            current_value=data['current_value'],
            profit_loss=data['profit_loss'],
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        )
        
        if 'purchases' in data:
            item.purchases = [Purchase.from_dict(p) for p in data['purchases']]
            
        return item 