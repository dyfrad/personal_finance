#!/usr/bin/env python3
"""
Personal Finance Manager

A Python-based personal finance management application that helps you track investments, household inventory, and expenses.

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

import sys
import argparse
import logging
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import ConfigManager
from config.version import __version__, __app_name__, __description__, __author__
from utils.logging import setup_logging, get_logger

import pandas as pd
import numpy as np
import os 
from datetime import datetime, timedelta
from database import Database

class Purchase:
    """Represents a single purchase transaction for stocks or bonds.
    
    Attributes:
        date (str): The date of purchase in YYYY-MM-DD format
        amount (float): The quantity/shares purchased
        price (float): The price per unit at time of purchase
    """
    def __init__(self, date, amount, price):
        self.date = date
        self.amount = amount
        self.price = price

class Item:
    """Represents a financial item in the portfolio.
    
    This class can handle both regular items (like appliances) and financial instruments
    (like stocks and bonds). For stocks and bonds, it maintains a list of purchases.
    
    Attributes:
        name (str): Name of the item
        category (str): Category of the item (e.g., 'Stocks', 'Bonds', 'Appliances')
        purchase_price (float): Initial purchase price (for non-stock items)
        date_of_purchase (str): Date of purchase in YYYY-MM-DD format
        current_value (float): Current market value of the item
        profit_loss (float): Current profit/loss on the item
        purchases (list): List of Purchase objects (for stocks/bonds)
    """
    def __init__(self, name, category, purchase_price=0, date_of_purchase="", current_value=0, profit_loss=0):
        self.name = name
        self.category = category
        self.purchase_price = purchase_price
        self.date_of_purchase = date_of_purchase
        self.current_value = current_value
        self.profit_loss = profit_loss
        self.purchases = []  # List of Purchase objects, primarily for stocks/bonds

    def add_purchase(self, purchase):
        """Adds a new purchase to the item's purchase history.
        
        Args:
            purchase (Purchase): A Purchase object containing purchase details
        """
        self.purchases.append(purchase)

    def get_total_invested(self):
        """Calculates the total amount invested in the item.
        
        If purchases exist, sums up all purchase amounts (quantity × price).
        Otherwise, returns the initial purchase price.
        
        Returns:
            float: Total amount invested in the item
        """
        if self.purchases:
            return sum(p.amount * p.price for p in self.purchases)
        return self.purchase_price

    def get_current_total_value(self, current_price_lookup=None):
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

    def get_overall_profit_loss(self, current_price_lookup=None):
        """Calculates the overall profit/loss on the item.
        
        Args:
            current_price_lookup (dict, optional): Dictionary mapping item names to current prices
            
        Returns:
            float: Total profit/loss (positive for profit, negative for loss)
        """
        total_invested = self.get_total_invested()
        current_total_value = self.get_current_total_value(current_price_lookup)
        return current_total_value - total_invested

def add_item():
    """Interactive function to add a new item to the portfolio.
    
    Prompts user for item details and creates appropriate Item object.
    Handles both regular items and stocks/bonds differently.
    
    Returns:
        Item: A new Item object with the user-provided details
    """
    name = input("Enter the name of the item: ")
    category = input("Enter the category of the item (e.g., Stocks, Appliances): ")
    if category in ['Stocks', 'Bonds']:
        date = input("Enter purchase date (YYYY-MM-DD): ")
        amount = float(input("Enter amount/shares: "))
        price = float(input("Enter price per unit: "))
        item = Item(name, category)
        item.add_purchase(Purchase(date, amount, price))
    else:
        purchase_price = float(input("Enter the purchase price of the item: "))
        date_of_purchase = input("Enter the date of purchase of the item: ")
        current_value = float(input("Enter the current value of the item: "))
        profit_loss = current_value - purchase_price
        item = Item(name, category, purchase_price, date_of_purchase, current_value, profit_loss)
    return item

def save_portfolio(items):
    """Saves the entire portfolio to the database.
    
    Clears existing data and saves all items and their purchases.
    
    Args:
        items (list): List of Item objects to save
    """
    db = Database()
    db.clear_all_items()
    db.clear_all_purchases()
    for item in items:
        now = datetime.now().isoformat()
        item_id = db.insert_base_item(
            item.name, item.purchase_price, item.date_of_purchase,
            item.current_value, item.profit_loss, item.category, now, now
        )
        # Save purchases for all item types (not just Stocks and Bonds)
        if item.purchases:
            # Determine table name based on category
            if item.category in ['Stocks', 'Bonds', 'Crypto', 'Real Estate', 'Gold']:
                table_name = 'investments'
            else:
                table_name = 'inventory'
            for purchase in item.purchases:
                db.add_purchase(item_id, purchase, table_name)

def load_portfolio():
    """Loads the entire portfolio from the database.
    
    Retrieves all items and their associated purchases from the database
    and reconstructs the Item objects.
    
    Returns:
        list: List of Item objects representing the portfolio
    """
    db = Database()
    rows = db.get_all_items()
    items = []
    for row in rows:
        item_id, name, purchase_price, date_of_purchase, current_value, profit_loss, category, created_at, updated_at = row
        item = Item(name, category, purchase_price, date_of_purchase, current_value, profit_loss)
        item.id = item_id
        # Load purchases for all item types (not just Stocks and Bonds)
        # Determine table name based on category
        if category in ['Stocks', 'Bonds', 'Crypto', 'Real Estate', 'Gold']:
            table_name = 'investments'
        else:
            table_name = 'inventory'
        purchases_data = db.get_purchases_for_item(item_id, table_name)
        for p_date, p_amount, p_price in purchases_data:
            item.add_purchase(Purchase(p_date, p_amount, p_price))
        items.append(item)
    return items

def init_application():
    """Initialize the application."""
    # Initialize configuration
    config_manager = ConfigManager()
    config = config_manager.get_config()
    
    # Setup logging
    setup_logging(config_manager)
    logger = get_logger(__name__)
    logger.info(f"Starting {__app_name__} v{__version__}")
    
    return config_manager

def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description=__app_name__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Start GUI application
  python main.py --console          # Run in console mode (future feature)
        """
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    
    parser.add_argument(
        '--console',
        action='store_true',
        help='Run in console mode (future feature)'
    )
    
    args = parser.parse_args()
    
    # Initialize application
    config_manager = init_application()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Debug logging enabled")
    
    # Handle console mode (future feature)
    if args.console:
        print("Console mode not yet implemented")
        print("   Starting GUI application instead...")
    
    # Start GUI application
    try:
        from gui import MainDashboard
        from database import Database
        import tkinter as tk
        
        logger = logging.getLogger(__name__)
        logger.info("Starting GUI application")
        
        # Create and run the application
        root = tk.Tk()
        db = Database()
        dashboard = MainDashboard(root, db)
        
        # Set up close handler
        root.protocol("WM_DELETE_WINDOW", root.destroy)
        
        # Run the application
        root.mainloop()
        
    except ImportError as e:
        logger.error(f"Failed to import GUI module: {e}")
        print("Error: GUI module not found")
        print("   Please ensure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        print(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
# %%
