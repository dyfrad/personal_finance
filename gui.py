"""Graphical user interface implementation with tkinter."""

import tkinter as tk
from tkinter import ttk, messagebox
from main import Item, save_portfolio, load_portfolio
from services.database import Database
import pandas as pd
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('TkAgg')  # Ensure TkAgg backend is used
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import yfinance as yf
import ta
import mplcursors
import sqlite3
from tkinter import filedialog
import csv

def set_theme(root):
    """Configure the application's visual theme.
    """
    style = ttk.Style(root)
    style.theme_use('clam')

    # Google Material Design Light Theme colors
    primary_color = '#2196F3'  # Blue 500
    primary_dark_color = '#1976D2' # Blue 700
    accent_color = '#FFC107'   # Amber 500
    background_color = '#FFFFFF' # White
    surface_color = '#FAFAFA' # Grey 50 for surfaces like cards, entry backgrounds
    text_primary_color = '#212121' # Grey 900 for primary text
    text_secondary_color = '#757575' # Grey 600 for secondary text
    text_hint_color = '#BDBDBD' # Grey 400 for hint text / disabled text

    style.configure('.', background=background_color, foreground=text_primary_color)
    style.configure('TLabel', background=background_color, foreground=text_primary_color)
    style.configure('TFrame', background=background_color)
    style.configure('TButton', background=primary_color, foreground='#FFFFFF', borderwidth=0)
    style.configure('TEntry', fieldbackground=surface_color, foreground=text_primary_color, insertcolor=text_primary_color, borderwidth=1, relief="solid", bordercolor=text_hint_color)
    style.configure('TMenubutton', background=primary_color, foreground='#FFFFFF')
    style.configure('TCheckbutton', background=background_color, foreground=text_primary_color)
    style.configure('TLabelframe', background=background_color, foreground=text_primary_color)
    style.configure('TLabelframe.Label', background=background_color, foreground=text_primary_color)
    # Treeview
    style.configure('Treeview', background=surface_color, foreground=text_primary_color, fieldbackground=surface_color, bordercolor=primary_dark_color, rowheight=25)
    style.configure('Treeview.Heading', background=primary_dark_color, foreground='#FFFFFF')
    style.map('TButton', background=[('active', primary_dark_color)])
    style.map('Treeview', background=[('selected', primary_color)])
    root.configure(bg=background_color)

    # CustomMessageBox styles for light theme
    style.configure("Custom.TLabel", foreground=text_primary_color, background=background_color)
    style.configure("Error.Custom.TLabel", foreground="#D32F2F", background=background_color) # Red 700
    style.configure("Warning.Custom.TLabel", foreground="#F57C00", background=background_color) # Orange 700
class EditDialog:
    """Dialog window for editing item details.
    
    Provides a modal dialog window with fields to edit an item's properties.
    Handles both regular items and financial instruments (stocks/bonds) differently.
    
    Attributes:
        top (tk.Toplevel): The dialog window
        item (Item): The item being edited
        entries (dict): Dictionary of entry widgets for item properties
        category_var (tk.StringVar): Variable holding the selected category
        result (Item): The updated item after editing
    """
    def __init__(self, parent, item):
        self.top = tk.Toplevel(parent)
        self.top.title(f"Edit Item: {item.name}")
        self.top.geometry("400x350")
        self.top.resizable(False, False)
        set_theme(self.top)

        self.item = item # Store the actual Item object
        
        # Make it modal
        self.top.transient(parent)
        self.top.grab_set()
        
        # Center the window
        self.top.update_idletasks()
        width = self.top.winfo_width()
        height = self.top.winfo_height()
        x = (self.top.winfo_screenwidth() // 2) - (width // 2)
        y = (self.top.winfo_screenheight() // 2) - (height // 2)
        self.top.geometry(f'{width}x{height}+{x}+{y}')
        
        # Create entry fields
        fields = ['Name', 'Category', 'Purchase Price', 'Date of Purchase', 'Current Value']
        self.entries = {}
        
        for i, field in enumerate(fields):
            ttk.Label(self.top, text=field).grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
            
            if field == 'Category':
                self.category_var = tk.StringVar(value=self.item.category)
                categories = ["Stocks", "Bonds", "Appliances", "Electronics", "Furniture", "Transportation", "Home Improvement", "Savings", "Collectibles"]
                category_menu = ttk.OptionMenu(self.top, self.category_var, self.category_var.get(), *categories)
                category_menu.grid(row=i, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
                self.entries[field] = category_menu # Store menu for value retrieval
            else:
                entry = ttk.Entry(self.top)
                entry.grid(row=i, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
                self.entries[field] = entry
                # Set initial values based on item type
                if field == 'Name':
                    entry.insert(0, self.item.name)
                elif field == 'Purchase Price':
                    if self.item.category not in ['Stocks', 'Bonds']:
                        entry.insert(0, str(self.item.purchase_price))
                    else:
                        # For stocks/bonds, show total invested amount but make it read-only
                        total_invested = self.item.get_total_invested() if hasattr(self.item, 'get_total_invested') else 0
                        entry.insert(0, str(total_invested))
                        entry.config(state='disabled')
                elif field == 'Date of Purchase':
                    # Always show the date from the main item record
                    entry.insert(0, self.item.date_of_purchase)
                elif field == 'Current Value':
                    if self.item.category not in ['Stocks', 'Bonds']:
                        entry.insert(0, str(self.item.current_value))
                    else:
                        # For stocks/bonds, show calculated current value but make it read-only
                        current_total = self.item.get_current_total_value({}) if hasattr(self.item, 'get_current_total_value') else 0
                        entry.insert(0, str(current_total))
                        entry.config(state='disabled')
        
        # Add buttons
        button_frame = ttk.Frame(self.top)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Save", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.LEFT, padx=5)
        
        # Initialize result
        self.result = None
        
        # Wait for window to be closed
        parent.wait_window(self.top)
    
    def save(self):
        try:
            # Update the item object directly
            self.item.name = self.entries['Name'].get()
            self.item.category = self.category_var.get()

            if self.item.category not in ['Stocks', 'Bonds']:
                self.item.purchase_price = float(self.entries['Purchase Price'].get())
                self.item.date_of_purchase = self.entries['Date of Purchase'].get()
                self.item.current_value = float(self.entries['Current Value'].get())
                self.item.profit_loss = self.item.current_value - self.item.purchase_price
            else:
                # For stocks/bonds, allow editing of name, category, and date of purchase
                self.item.date_of_purchase = self.entries['Date of Purchase'].get()

            self.result = self.item # Return the updated item
            self.top.destroy()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for prices")
    
    def cancel(self):
        self.top.destroy()

class CustomMessageBox:
    """Custom message box dialog with themed styling.
    
    Provides a modal dialog window for displaying messages with different styles
    (info, warning, error) and consistent theming.
    
    Attributes:
        top (tk.Toplevel): The dialog window
    """
    def __init__(self, parent, title, message, type="info"):
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.top.geometry("300x150")
        self.top.resizable(False, False)
        
        # Make it modal
        self.top.transient(parent)
        self.top.grab_set()
        
        # Center the window
        self.top.update_idletasks()
        width = self.top.winfo_width()
        height = self.top.winfo_height()
        x = (self.top.winfo_screenwidth() // 2) - (width // 2)
        y = (self.top.winfo_screenheight() // 2) - (height // 2)
        self.top.geometry(f'{width}x{height}+{x}+{y}')
        
        # Configure style
        style = ttk.Style()
        if type == "error":
            style.configure("Custom.TLabel", foreground="#D32F2F") # Red 700
        elif type == "warning":
            style.configure("Custom.TLabel", foreground="#F57C00") # Orange 700
        else:
            style.configure("Custom.TLabel", foreground="#212121") # Grey 900
        
        # Add message
        ttk.Label(self.top, text=message, style="Custom.TLabel", wraplength=250).pack(pady=20)
        
        # Add button
        ttk.Button(self.top, text="OK", command=self.top.destroy).pack(pady=10)
        
        # Wait for window to be closed
        parent.wait_window(self.top)

class PurchasesDialog:
    """Dialog window for managing item purchases.
    
    Provides a modal dialog window for viewing, adding, and managing
    purchase records for investments and inventory items.
    
    Attributes:
        top (tk.Toplevel): The dialog window
        db (Database): Database connection for data operations
        item_id (int): ID of the item being managed
        item_name (str): Name of the item being managed
        item_category (str): Category of the item being managed
        tree (ttk.Treeview): Treeview widget displaying purchases
    """
    def __init__(self, top_level_root, parent_for_modality, db, item_id, item_name, item_category):
        self.db = db
        self.item_id = item_id
        self.item_category = item_category
        self.top = top_level_root # Use the Toplevel provided by show_window
        set_theme(self.top)
        self.top.title(f"Purchases for {item_name}")
        self.top.geometry("500x400")
        # Determine table name based on category
        if self.item_category in ['Stocks', 'Bonds', 'Crypto', 'Real Estate', 'Gold']:
            table_name = 'investments'
        else:
            table_name = 'inventory'
        self.purchases = self.db.get_purchases_for_item(item_id, table_name)

        # Make it modal
        self.top.transient(parent_for_modality) # parent_for_modality is PersonalFinanceApp's root
        self.top.grab_set()

        # Center the window
        self.top.update_idletasks()
        width = self.top.winfo_width()
        height = self.top.winfo_height()
        x = (self.top.winfo_screenwidth() // 2) - (width // 2)
        y = (self.top.winfo_screenheight() // 2) - (height // 2)
        self.top.geometry(f'{width}x{height}+{x}+{y}')

        # Determine labels based on item category
        if self.item_category in ['Stocks', 'Bonds', 'Crypto', 'Real Estate', 'Gold']:
            # For investments
            amount_label = "Shares/Units"
            price_label = "Price per Unit"
        else:
            # For inventory items
            amount_label = "Quantity"
            price_label = "Unit Price"

        # Purchases list
        self.tree = ttk.Treeview(self.top, columns=("Date", "Amount", "Price"), show='headings') # master is self.top
        self.tree.heading("Date", text="Date")
        self.tree.heading("Amount", text=amount_label)
        self.tree.heading("Price", text=price_label)
        for col in ("Date", "Amount", "Price"):
            self.tree.column(col, width=120)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.refresh_tree()

        # Add purchase section
        add_frame = ttk.LabelFrame(self.top, text="Add Purchase", padding="10")
        add_frame.pack(fill=tk.X, padx=10, pady=5)
        self.date_entry = ttk.Entry(add_frame)
        self.amount_entry = ttk.Entry(add_frame)
        self.price_entry = ttk.Entry(add_frame)
        ttk.Label(add_frame, text="Date (YYYY-MM-DD)").grid(row=0, column=0, padx=5, pady=2)
        self.date_entry.grid(row=0, column=1, padx=5, pady=2)
        ttk.Label(add_frame, text=amount_label).grid(row=1, column=0, padx=5, pady=2)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=2)
        ttk.Label(add_frame, text=price_label).grid(row=2, column=0, padx=5, pady=2)
        self.price_entry.grid(row=2, column=1, padx=5, pady=2)
        ttk.Button(add_frame, text="Add", command=self.add_purchase).grid(row=3, column=0, columnspan=2, pady=5)

        ttk.Button(self.top, text="Close", command=self.top.destroy).pack(pady=5)

    def refresh_tree(self):
        """Refresh the purchases treeview with current data."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for purchase in self.purchases:
            self.tree.insert('', tk.END, values=purchase)

    def add_purchase(self):
        """Add a new purchase record for the item."""
        date = self.date_entry.get()
        try:
            amount = float(self.amount_entry.get())
            price = float(self.price_entry.get())
        except ValueError:
            if self.item_category in ['Stocks', 'Bonds', 'Crypto', 'Real Estate', 'Gold']:
                messagebox.showerror("Error", "Shares/Units and Price per Unit must be numbers.")
            else:
                messagebox.showerror("Error", "Quantity and Unit Price must be numbers.")
            return
        if not date:
            messagebox.showerror("Error", "Date is required.")
            return
        # Determine table name based on category
        if self.item_category in ['Stocks', 'Bonds', 'Crypto', 'Real Estate', 'Gold']:
            table_name = 'investments'
        else:
            table_name = 'inventory'
        self.db.add_purchase(self.item_id, type('Purchase', (), {'date': date, 'amount': amount, 'price': price})(), table_name)
        self.purchases = self.db.get_purchases_for_item(self.item_id, table_name)
        self.refresh_tree()
        self.date_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

class AddItemDialog:
    """Dialog for adding new items to the portfolio."""
    
    def __init__(self, top_level_root, parent_for_modality, db, on_success, category=None):
        self.db = db
        self.on_success = on_success
        self.category = category
        
        self.top = top_level_root  # Use the Toplevel provided by show_window
        set_theme(self.top)
        self.top.title("Add New Item")
        self.top.geometry("400x500")
        self.top.transient(parent_for_modality)
        self.top.grab_set()
        
        # Create form
        ttk.Label(self.top, text="Name:").pack(pady=5)
        self.name_entry = ttk.Entry(self.top)
        self.name_entry.pack(pady=5, fill=tk.X, padx=20)
        
        ttk.Label(self.top, text="Category:").pack(pady=5)
        self.category_var = tk.StringVar()
        
        # Set categories based on item type
        if category == "Investment":
            categories = ["Stocks", "Bonds", "Crypto", "Real Estate", "Gold"]
        elif category == "Inventory":
            categories = ["Appliances", "Electronics", "Furniture", "Transportation", "Home Improvement", "Savings", "Collectibles"]
        elif category == "Expense":
            categories = ["Expense"]
        else:
            categories = ["Stocks", "Bonds", "Crypto", "Real Estate", "Gold",
                         "Appliances", "Electronics", "Furniture", "Transportation",
                         "Home Improvement", "Savings", "Collectibles", "Expense"]
        
        self.category_var.set(categories[0])
        ttk.OptionMenu(self.top, self.category_var, self.category_var.get(), *categories).pack(pady=5, fill=tk.X, padx=20)
        
        # Create different forms based on category
        if category == "Expense":
            # For expenses: only show Date and Amount
            ttk.Label(self.top, text="Date:").pack(pady=5)
            self.date_entry = ttk.Entry(self.top)
            self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
            self.date_entry.pack(pady=5, fill=tk.X, padx=20)
            
            ttk.Label(self.top, text="Amount (€):").pack(pady=5)
            self.amount_entry = ttk.Entry(self.top)
            self.amount_entry.pack(pady=5, fill=tk.X, padx=20)
            
            # Set unused entries to None for expenses
            self.price_entry = None
            self.value_entry = None
            
        else:
            # For Investment and Inventory items: show price-related fields
            if category == "Investment":
                ttk.Label(self.top, text="Price per Share/Unit (€):").pack(pady=5)
            else:
                ttk.Label(self.top, text="Purchase Price (€):").pack(pady=5)
            self.price_entry = ttk.Entry(self.top)
            self.price_entry.pack(pady=5, fill=tk.X, padx=20)
            
            ttk.Label(self.top, text="Date of Purchase:").pack(pady=5)
            self.date_entry = ttk.Entry(self.top)
            self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
            self.date_entry.pack(pady=5, fill=tk.X, padx=20)
            
            if category == "Investment":
                ttk.Label(self.top, text="Number of Shares/Units:").pack(pady=5)
                self.amount_entry = ttk.Entry(self.top)
                self.amount_entry.pack(pady=5, fill=tk.X, padx=20)
            else:
                # For inventory items, amount/quantity is not stored, so don't show the field
                self.amount_entry = None
            
            if category != "Investment":
                ttk.Label(self.top, text="Current Value (€):").pack(pady=5)
                self.value_entry = ttk.Entry(self.top)
                self.value_entry.pack(pady=5, fill=tk.X, padx=20)
            else:
                # For investments, current value will be calculated automatically
                self.value_entry = None
        
        # Add buttons
        button_frame = ttk.Frame(self.top)
        button_frame.pack(pady=20, fill=tk.X, padx=20)
        ttk.Button(button_frame, text="Add", command=self.add_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.top.destroy).pack(side=tk.RIGHT, padx=5)

    def add_item(self):
        """Add a new item to the portfolio."""
        name = self.name_entry.get().strip()
        category = self.category_var.get()
        if not name:
            messagebox.showerror("Error", "Name is required.")
            return

        # Get form data
        date = self.date_entry.get().strip()
        amount = self.amount_entry.get().strip() if self.amount_entry else ""
        price = self.price_entry.get().strip() if self.price_entry else ""

        # Initialize values
        purchase_price = 0
        current_value = 0
        date_of_purchase = datetime.now().isoformat()
        profit_loss = 0

        # Handle form data based on category
        if category == "Expense":
            # For expenses: validate date and amount only
            if not date:
                messagebox.showerror("Error", "Date is required.")
                return
            if not amount:
                messagebox.showerror("Error", "Amount is required.")
                return
            try:
                expense_amount = float(amount)
                purchase_price = expense_amount  # Store expense amount as purchase_price
                current_value = 0  # Expenses don't have current value
                date_of_purchase = date
                profit_loss = -expense_amount  # Expenses are always negative profit
            except ValueError:
                messagebox.showerror("Error", "Amount must be a valid number.")
                return
        elif category not in ['Stocks', 'Bonds']:
            # For inventory items, use the entered values if provided
            if date and price:  # Only date and price needed for non-stock items
                try:
                    purchase_price = float(price)
                    current_value = float(self.value_entry.get()) if self.value_entry and self.value_entry.get().strip() else purchase_price
                    date_of_purchase = date
                    profit_loss = current_value - purchase_price
                except ValueError:
                    messagebox.showerror("Error", "Price and Current Value must be numbers.")
                    return
        else:
            # For stocks/bonds, we'll store basic info and use purchases table for detailed data
            if date:
                date_of_purchase = date

        # Use the Database class methods to insert items properly
        now = datetime.now().isoformat()
        
        if category in ['Stocks', 'Bonds']:
            # Validate required fields for investments
            if not date:
                messagebox.showerror("Error", "Date is required for investments.")
                return
            if not amount:
                messagebox.showerror("Error", "Number of shares/units is required for investments.")
                return
            if not price:
                messagebox.showerror("Error", "Price per share/unit is required for investments.")
                return
            
            try:
                amount = float(amount)
                price = float(price)
            except ValueError:
                messagebox.showerror("Error", "Amount and Price must be valid numbers.")
                return
            
            # Check if investment with same name and category already exists
            existing_items = self.db.get_items_by_category(category)
            existing_item = next((item for item in existing_items if item[1] == name), None)
            
            if existing_item:
                # Add purchase to existing item
                item_id = existing_item[0]
                self.db.add_purchase(item_id, type('Purchase', (), {'date': date, 'amount': amount, 'price': price})())
                print(f"DEBUG: Added purchase to existing item - Item ID: {item_id}, Date: {date}, Amount: {amount}, Price: {price}")
                
                # Update the item's date to the most recent purchase date
                self.db.update_base_item(item_id, name, 0, date, 0, 0, category, now)
            else:
                # Create new investment item
                item_id = self.db.insert_base_item(name, purchase_price, date_of_purchase, current_value, profit_loss, category, now, now)
                
                # Add purchase record
                self.db.add_purchase(item_id, type('Purchase', (), {'date': date, 'amount': amount, 'price': price})())
                print(f"DEBUG: Created new investment item with purchase - Item ID: {item_id}, Date: {date}, Amount: {amount}, Price: {price}")
        else:
            # For non-investment items (inventory and expenses), always create new item
            item_id = self.db.insert_base_item(name, purchase_price, date_of_purchase, current_value, profit_loss, category, now, now)
            print(f"DEBUG: Created new {category.lower()} item - Item ID: {item_id}, Name: {name}, Amount: {purchase_price}")
        self.top.destroy()
        self.on_success()

class MainDashboard:
    """Main dashboard window of the application.
    
    Provides the primary interface for viewing financial data, including
    stock performance, expenses, and portfolio overview.
    
    Attributes:
        root (tk.Tk): The root window
        db (Database): Database connection for data operations
        open_windows (dict): Dictionary of active window instances
        controls_frame (ttk.LabelFrame): Frame containing centered control buttons
    """
    def __init__(self, root, db):
        set_theme(root)
        self.root = root
        self.db = db
        self.root.title("Personal Finance Manager")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        # Track open windows
        self.open_windows = {}
        self.create_layout()

    def create_layout(self):
        """Create the main dashboard layout."""
        # Configure single row and column to center the controls
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        
        # Create centered controls frame
        self.controls_frame = ttk.LabelFrame(self.root, text="Controls", padding=20)
        self.controls_frame.grid(row=0, column=0, padx=50, pady=50)
        self.show_topright_buttons(self.controls_frame)

    def show_window(self, window_type, window_class, *args, **kwargs):
        """Show a new window of the specified type.
        
        Args:
            window_type (str): Type of window to show
            window_class (class): Class of the window to instantiate
            *args: Additional positional arguments for window initialization
            **kwargs: Additional keyword arguments for window initialization
        """
        print(f"show_window called for type: {window_type}")
        print(f"Current open_windows: {self.open_windows.keys()}")

        # Get the actual Toplevel window from the stored object if it exists
        top_level_window = self.open_windows.get(window_type)
        print(f"Retrieved top_level_window: {top_level_window}")

        if top_level_window:
            print(f"top_level_window exists in dict. Checking winfo_exists(): {top_level_window.winfo_exists()}")

        if top_level_window and top_level_window.winfo_exists():
            # Window exists, focus it
            print(f"FOCUSED existing window: {window_type}")
            top_level_window.lift()
            top_level_window.focus_force()
        else:
            # Create new window
            print(f"CREATING new window: {window_type}")
            new_toplevel = tk.Toplevel(self.root)
            # Pass the new Toplevel window as the first argument to the window_class
            window_instance = window_class(new_toplevel, *args, **kwargs) # window_instance will be the dialog object

            # Store the Toplevel window itself, not the dialog class instance
            self.open_windows[window_type] = new_toplevel 
            
            # Set the protocol for closing the Toplevel window
            new_toplevel.protocol("WM_DELETE_WINDOW", lambda: self.on_window_close(window_type))
            print(f"New window created and stored: {new_toplevel}")

    def on_window_close(self, window_type):
        """Handle window close event.
        
        Args:
            window_type (str): Type of window being closed
        """
        if window_type in self.open_windows:
            self.open_windows[window_type].destroy()
            del self.open_windows[window_type]

    def show_topright_buttons(self, parent):
        """Create top-right control buttons organized by category.
        
        Args:
            parent (ttk.Frame): Parent frame for the buttons
        """
        button_frame = ttk.Frame(parent)
        button_frame.pack(expand=True, fill=tk.BOTH, pady=10)

        # Investments Section
        investments_frame = ttk.LabelFrame(button_frame, text="Investments", padding="5")
        investments_frame.pack(fill=tk.X, padx=10, pady=5)
        investments_buttons = ttk.Frame(investments_frame)
        investments_buttons.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(investments_buttons, text="View", 
                  command=lambda: self.open_portfolio_window("Investment")).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        ttk.Button(investments_buttons, text="Add", 
                  command=lambda: self.add_item_gui("Investment")).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        # Inventory Section
        inventory_frame = ttk.LabelFrame(button_frame, text="Inventory", padding="5")
        inventory_frame.pack(fill=tk.X, padx=10, pady=5)
        inventory_buttons = ttk.Frame(inventory_frame)
        inventory_buttons.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(inventory_buttons, text="View", 
                  command=lambda: self.open_portfolio_window("Inventory")).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        ttk.Button(inventory_buttons, text="Add", 
                  command=lambda: self.add_item_gui("Inventory")).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        # Expenses Section
        expenses_frame = ttk.LabelFrame(button_frame, text="Expenses", padding="5")
        expenses_frame.pack(fill=tk.X, padx=10, pady=5)
        expenses_buttons = ttk.Frame(expenses_frame)
        expenses_buttons.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(expenses_buttons, text="View", 
                  command=lambda: self.open_portfolio_window("Expense")).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        ttk.Button(expenses_buttons, text="Add", 
                  command=lambda: self.add_item_gui("Expense")).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

    def open_portfolio_window(self, category=None):
        """Open the portfolio management window.
        
        Args:
            category (str, optional): Category of items to display. Defaults to None.
        """
        # Pass only the Toplevel to PersonalFinanceApp
        self.show_window('portfolio', PersonalFinanceApp, category)

    def add_item_gui(self, category=None):
        """Open the add item dialog.
        
        Args:
            category (str, optional): Category of item to add. Defaults to None.
        """
        # Create unique window type based on category to prevent window conflicts
        window_type = f'add_item_{category}' if category else 'add_item'
        # Pass MainDashboard's root as the parent_for_modality
        self.show_window(window_type, AddItemDialog, self.root, self.db, self.refresh_dashboard, category)

    def refresh_dashboard(self):
        """Refresh all dashboard components."""        
        # With the simplified centered layout, there's nothing dynamic to refresh
        pass

class PersonalFinanceApp:
    """Main application class for the personal finance manager.
    
    Manages the main application window and coordinates between different
    components of the application.
    
    Attributes:
        root (tk.Tk): The root window
        db (Database): Database connection for data operations
        open_windows (dict): Dictionary of active window instances
        portfolio_tree (ttk.Treeview): Treeview widget displaying portfolio items
        right_panel (ttk.Frame): Frame containing right panel controls
    """
    def __init__(self, top_level_root, category=None):
        set_theme(top_level_root)
        self.root = top_level_root
        self.root.title(f"{category if category else 'All'} Portfolio")
        self.root.geometry("1000x600")
        self.db = Database()
        self.category = category
        
        # Create main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=3)
        self.main_frame.rowconfigure(0, weight=1)
        
        # Create right panel for displaying portfolio
        self.right_panel = ttk.Frame(self.main_frame)
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.create_right_panel(self.right_panel)
        
        # Load initial data
        self.load_portfolio_gui()
        
        # Track open windows specific to PersonalFinanceApp
        self.open_windows = {}

    def show_window(self, window_type, window_class, *args, **kwargs):
        """Show a new window of the specified type.
        
        Args:
            window_type (str): Type of window to show
            window_class (class): Class of the window to instantiate
            *args: Additional positional arguments for window initialization
            **kwargs: Additional keyword arguments for window initialization
        """
        # Get the actual Toplevel window from the stored object if it exists
        top_level_window = self.open_windows.get(window_type)

        if top_level_window and top_level_window.winfo_exists():
            # Window exists, focus it
            top_level_window.lift()
            top_level_window.focus_force()
        else:
            # Create new window
            new_toplevel = tk.Toplevel(self.root)
            # Pass the new Toplevel window as the first argument to the window_class
            window_instance = window_class(new_toplevel, self.root, *args, **kwargs)

            # Store the Toplevel window itself, not the dialog class instance
            self.open_windows[window_type] = new_toplevel 
            
            # Set the protocol for closing the Toplevel window
            new_toplevel.protocol("WM_DELETE_WINDOW", lambda: self.on_window_close(window_type))

    def create_right_panel(self, parent):
        """Create the right panel with action buttons.
        
        Args:
            parent (ttk.Frame): Parent frame for the panel
        """
        right_frame = ttk.LabelFrame(parent, text=f"{self.category if self.category else 'All'} Portfolio", padding="10")
        right_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview with different columns based on category
        if self.category == "Expense":
            columns = ('ID', 'Name', 'Category', 'Date', 'Amount')
            column_widths = {'ID': 0, 'Name': 200, 'Category': 100, 'Date': 120, 'Amount': 100}
        else:
            columns = ('ID', 'Name', 'Purchase Price', 'Date', 'Current Value', 'Profit/Loss', 'Category')
            column_widths = {'ID': 0, 'Name': 150, 'Purchase Price': 100, 'Date': 120, 'Current Value': 100, 'Profit/Loss': 100, 'Category': 100}
        
        self.tree = ttk.Treeview(right_frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 100))
        self.tree.column('ID', width=0, stretch=False)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Add buttons
        button_frame = ttk.Frame(right_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Export", command=self.export_portfolio_gui).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load", command=self.load_portfolio_gui).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit Selected", command=self.edit_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="View/Add Purchases", command=self.view_purchases).pack(side=tk.LEFT, padx=5)
        
        # Add total value label
        self.total_value_label = ttk.Label(right_frame, text="Total Value: €0.00")
        self.total_value_label.grid(row=2, column=0, columnspan=2, pady=5)

    def load_portfolio_gui(self):
        """Load portfolio data from the database."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Get items from main.py's load_portfolio, which returns rich Item objects
        from main import load_portfolio
        self.items = load_portfolio()  # Store loaded items in self.items
        
        # Filter items based on category if specified
        if self.category:
            if self.category == "Investment":
                self.items = [item for item in self.items if item.category in ['Stocks', 'Bonds', 'Crypto', 'Real Estate', 'Gold']]
            elif self.category == "Inventory":
                self.items = [item for item in self.items if item.category in ['Appliances', 'Electronics', 'Furniture', 'Transportation', 'Home Improvement', 'Savings', 'Collectibles']]
            elif self.category == "Expense":
                self.items = [item for item in self.items if item.category == "Expense"]

        # Fetch current stock prices for calculation
        current_prices = {}
        stock_names_to_fetch = set()
        for item in self.items:
            if item.category in ['Stocks', 'Bonds']:
                stock_names_to_fetch.add(item.name)  # Use the item name as ticker
        
        for stock_name in stock_names_to_fetch:
            ticker_symbol = stock_name.split()[0] if ' ' in stock_name else stock_name
            price = 0.0  # Default to 0
            # Try different exchange suffixes for VUSA or general tickers
            if ticker_symbol == 'VUSA':
                exchanges = ['', '.L', '.AS', '.DE', '.PA', '.MI']
            else:
                exchanges = ['']  # For other tickers, try direct
            for suffix in exchanges:
                try:
                    ticker_data = yf.Ticker(ticker_symbol + suffix).history(period="1d")
                    if not ticker_data.empty:
                        price = ticker_data['Close'].iloc[-1]
                        break
                except Exception:
                    continue
            current_prices[stock_name] = price

        # Add items to treeview
        total_portfolio_value = 0
        for item in self.items:
            if self.category == "Expense":
                # For expenses: show only Name, Category, Date, Amount
                self.tree.insert('', tk.END, values=(
                    item.id,  # ID (hidden)
                    item.name,  # Name
                    item.category,  # Category
                    item.date_of_purchase,  # Date
                    f"€{item.purchase_price:.2f}"  # Amount (stored as purchase_price)
                ), iid=item.id)
                # For expenses, don't add to total portfolio value (they're costs)
            else:
                # For investments and inventory: show all columns
                display_purchase_price = ""
                display_current_value = ""
                display_profit_loss = ""
                display_date = ""

                if item.category in ['Stocks', 'Bonds']:
                    total_invested = item.get_total_invested()
                    current_total_value = item.get_current_total_value(current_prices)
                    profit_loss = item.get_overall_profit_loss(current_prices)
                    # Show date from main item record, not purchases (more reliable)
                    display_date = item.date_of_purchase

                    display_purchase_price = f"€{total_invested:.2f}"
                    display_current_value = f"€{current_total_value:.2f}"
                    display_profit_loss = f"€{profit_loss:.2f}"
                    total_portfolio_value += current_total_value

                else:  # Inventory items
                    display_purchase_price = f"€{item.purchase_price:.2f}"
                    display_current_value = f"€{item.current_value:.2f}"
                    display_profit_loss = f"€{item.profit_loss:.2f}"
                    display_date = item.date_of_purchase
                    total_portfolio_value += item.current_value

                # Store the actual Item object (or its ID) with the treeview row
                self.tree.insert('', tk.END, values=(
                    item.id,  # ID
                    item.name,  # Name
                    display_purchase_price,  # Purchase Price
                    display_date,  # Date
                    display_current_value,  # Current Value
                    display_profit_loss,  # Profit/Loss
                    item.category  # Category
                ), iid=item.id)

        # Update total value label
        if self.category == "Expense":
            total_expenses = sum(item.purchase_price for item in self.items)
            self.total_value_label.config(text=f"Total Expenses: €{total_expenses:.2f}")
        else:
            self.total_value_label.config(text=f"Total Value: €{total_portfolio_value:.2f}")

    def edit_selected(self):
        """Edit the selected portfolio item."""
        selected_item_id = self.tree.focus()
        if not selected_item_id:
            CustomMessageBox(self.root, "Error", "Please select an item to edit.", type="error")
            return
        # Retrieve the Item object from self.items using its ID
        item_to_edit = next((item for item in self.items if str(item.id) == selected_item_id), None)
        if item_to_edit:
            edit_dialog = EditDialog(self.root, item_to_edit)
            updated_item = edit_dialog.result
            if updated_item: # If user clicked Save
                # Update the database
                if updated_item.category not in ['Stocks', 'Bonds']:
                    self.db.update_base_item(
                        updated_item.id, updated_item.name, updated_item.purchase_price,
                        updated_item.date_of_purchase, updated_item.current_value,
                        updated_item.profit_loss, updated_item.category, datetime.now().isoformat()
                    )
                else:
                    # For stocks/bonds, update name, category, and date_of_purchase in base item table
                    self.db.update_base_item(
                        updated_item.id, updated_item.name, 0, updated_item.date_of_purchase, 0, 0, # Keep date, use placeholders for calculated values
                        updated_item.category, datetime.now().isoformat()
                    )
                self.load_portfolio_gui() # Refresh the display

    def delete_selected(self):
        """Delete the selected portfolio item."""
        selected_item_id = self.tree.focus()
        if not selected_item_id:
            CustomMessageBox(self.root, "Error", "Please select an item to delete.", type="error")
            return
        # Confirm deletion
        if messagebox.askyesno("Delete Item", "Are you sure you want to delete the selected item?"):
            self.db.delete_item(selected_item_id) # Use the item ID directly
            self.load_portfolio_gui() # Refresh the display

    def view_purchases(self):
        """View purchases for selected item."""
        selected_item_id = self.tree.focus()
        if not selected_item_id:
            CustomMessageBox(self.root, "Error", "Please select an item to view purchases.", type="error")
            return
        # Retrieve the Item object from self.items using its ID
        item_to_view_purchases = next((item for item in self.items if str(item.id) == selected_item_id), None)
        if item_to_view_purchases:
            # Allow purchases for both investments and inventory items
            if item_to_view_purchases.category in ['Stocks', 'Bonds', 'Crypto', 'Real Estate', 'Gold', 'Appliances', 'Electronics', 'Furniture', 'Transportation', 'Home Improvement', 'Savings', 'Collectibles']:
                # Create a unique key for this purchases window
                window_key = f'purchases_{selected_item_id}'
                # Use the new show_window method - don't pass self.root as extra arg
                self.show_window(window_key, PurchasesDialog, self.db, item_to_view_purchases.id, item_to_view_purchases.name, item_to_view_purchases.category)
                self.load_portfolio_gui() # Refresh display after purchases are added/modified
            else:
                CustomMessageBox(self.root, "Info", "Purchase details are only available for Investment and Inventory items.", type="info")
        else:
            CustomMessageBox(self.root, "Error", "Item not found.", type="error")

    def on_window_close(self, window_key):
        """Handle window close event.
        
        Args:
            window_key (str): Key of the window being closed
        """
        if window_key in self.open_windows:
            self.open_windows[window_key].destroy()
            del self.open_windows[window_key]

    def export_portfolio_gui(self):
        """Export portfolio data to a CSV file."""
        # Get the file path from user
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Portfolio"
        )
        
        if file_path:  # If user didn't cancel
            try:
                with open(file_path, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    # Write header based on category
                    if self.category == "Expense":
                        writer.writerow(['ID', 'Name', 'Category', 'Date', 'Amount'])
                    else:
                        writer.writerow(['ID', 'Name', 'Purchase Price', 'Date', 'Current Value', 'Profit/Loss', 'Category'])
                    
                    # Write data
                    for item_id in self.tree.get_children():
                        values = self.tree.item(item_id)['values']
                        writer.writerow(values)
                        
                CustomMessageBox(self.root, "Success", "Portfolio exported successfully!")
            except Exception as e:
                CustomMessageBox(self.root, "Error", f"Error exporting portfolio: {str(e)}", type="error")                 

if __name__ == "__main__":
    root = tk.Tk()
    db = Database()
    dashboard = MainDashboard(root, db)
    root.mainloop() 
