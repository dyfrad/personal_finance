from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Purchase:
    """Represents a single purchase transaction for stocks or bonds.
    
    Attributes:
        id (Optional[int]): Database ID of the purchase
        date (str): The date of purchase in YYYY-MM-DD format
        amount (float): The quantity/shares purchased
        price (float): The price per unit at time of purchase
        created_at (datetime): Timestamp when the purchase was created
        updated_at (datetime): Timestamp when the purchase was last updated
    """
    id: Optional[int] = None
    date: str = ""
    amount: float = 0.0
    price: float = 0.0
    created_at: datetime = None
    updated_at: datetime = None

    def get_total_value(self) -> float:
        """Calculate the total value of the purchase.
        
        Returns:
            float: Total value (amount * price)
        """
        return self.amount * self.price

    def to_dict(self) -> dict:
        """Convert the purchase to a dictionary representation.
        
        Returns:
            dict: Dictionary representation of the purchase
        """
        return {
            'id': self.id,
            'date': self.date,
            'amount': self.amount,
            'price': self.price,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Purchase':
        """Create a Purchase instance from a dictionary.
        
        Args:
            data (dict): Dictionary containing purchase data
            
        Returns:
            Purchase: New Purchase instance
        """
        return cls(
            id=data.get('id'),
            date=data['date'],
            amount=data['amount'],
            price=data['price'],
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        ) 