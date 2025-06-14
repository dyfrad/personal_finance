#%%
import pandas as pd
import numpy as np
import os 
from datetime import datetime, timedelta
from database import Database

# add a class for an item that has the following attributes:
# - name
# - purchase_price
# - date_of_purchase
# - current_value           
class Purchase:
    def __init__(self, date, amount, price):
        self.date = date
        self.amount = amount
        self.price = price

class Item:
    def __init__(self, name, category, purchase_price=0, date_of_purchase="", current_value=0, profit_loss=0):
        self.name = name
        self.category = category
        self.purchase_price = purchase_price
        self.date_of_purchase = date_of_purchase
        self.current_value = current_value
        self.profit_loss = profit_loss
        self.purchases = []  # List of Purchase objects, primarily for stocks/bonds

    def add_purchase(self, purchase):
        self.purchases.append(purchase)

    def get_total_invested(self):
        if self.category in ['Stocks', 'Bonds'] and self.purchases:
            return sum(p.amount for p in self.purchases)
        return self.purchase_price # For non-stock items

    def get_current_total_value(self, current_price_lookup=None):
        if self.category in ['Stocks', 'Bonds'] and self.purchases:
            if current_price_lookup:
                # Attempt to get current price for the stock
                # This requires fetching from yfinance, which we can't do synchronously here easily
                # For now, let's use the last known price from purchases if available or a mock
                if self.name in current_price_lookup:
                    price_per_unit = current_price_lookup[self.name]
                else: # Fallback for initial load or if no real-time price
                    price_per_unit = self.purchases[-1].price if self.purchases else 1 # Default to 1 if no purchases
                return sum(p.amount * price_per_unit for p in self.purchases)
            else:
                # If no lookup, just return sum of initial purchase values
                return sum(p.amount * p.price for p in self.purchases)
        return self.current_value # For non-stock items

    def get_overall_profit_loss(self, current_price_lookup=None):
        total_invested = self.get_total_invested()
        current_total_value = self.get_current_total_value(current_price_lookup)
        return current_total_value - total_invested

# add functionality to add an item when user runs the program
def add_item():
    name = input("Enter the name of the item: ")
    category = input("Enter the category of the item (e.g., Stocks, Appliances): ")
    if category in ['Stocks', 'Bonds']:
        # For stocks/bonds, capture first purchase data
        date = input("Enter purchase date (YYYY-MM-DD): ")
        amount = float(input("Enter amount/shares: "))
        price = float(input("Enter price per unit: "))
        item = Item(name, category)
        item.add_purchase(Purchase(date, amount, price))
    else:
        # For other items, use single purchase attributes
        purchase_price = float(input("Enter the purchase price of the item: "))
        date_of_purchase = input("Enter the date of purchase of the item: ")
        current_value = float(input("Enter the current value of the item: "))
        profit_loss = current_value - purchase_price
        item = Item(name, category, purchase_price, date_of_purchase, current_value, profit_loss)
    return item

# add functionality to save the portfolio to the database
def save_portfolio(items):
    db = Database()
    db.clear_all_items()
    db.clear_all_purchases() # Clear purchases too
    for item in items:
        now = datetime.now().isoformat()
        # Add item to items table
        item_id = db.insert_base_item(
            item.name, item.purchase_price, item.date_of_purchase,
            item.current_value, item.profit_loss, item.category, now, now
        )
        # Add purchases if it's a stock/bond
        if item.category in ['Stocks', 'Bonds'] and item.purchases:
            for purchase in item.purchases:
                db.add_purchase(item_id, purchase)

# add functionality to load the portfolio from the database
def load_portfolio():
    db = Database()
    rows = db.get_all_items() # This now just returns base item rows
    items = []
    for row in rows:
        item_id, name, purchase_price, date_of_purchase, current_value, profit_loss, category, created_at, updated_at = row
        item = Item(name, category, purchase_price, date_of_purchase, current_value, profit_loss)
        item.id = item_id # Store the ID for later updates/deletes
        # If it's a stock/bond, load purchases from the separate table
        if category in ['Stocks', 'Bonds']:
            purchases_data = db.get_purchases_for_item(item_id)
            for p_date, p_amount, p_price in purchases_data:
                item.add_purchase(Purchase(p_date, p_amount, p_price))
        items.append(item)
    return items
# %%
