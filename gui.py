import tkinter as tk
from tkinter import ttk, messagebox
from main import Item, save_portfolio, load_portfolio, mock_items
from database import Database
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import yfinance as yf
import ta
import mplcursors
import sqlite3
from tkinter import filedialog
import csv

def set_theme(root, light_mode=False):
    style = ttk.Style(root)
    style.theme_use('clam')

    if light_mode:
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

    else:
        # Google Material Design-inspired colors (Dark Theme - existing)
        google_primary = '#2196F3'  # Blue 500
        google_primary_dark = '#1976D2' # Blue 700
        google_accent = '#FFC107'   # Amber 500
        google_background_dark = '#424242' # Grey 800
        google_surface_dark = '#212121' # Grey 900 for deeper elements
        google_text_light = '#FFFFFF' # White text for dark backgrounds
        google_text_secondary = '#BDBDBD' # Grey 400 for secondary text

        # General colors
        dark_bg = google_background_dark
        dark_fg = google_text_light # Keep foreground light for dark theme
        accent = google_accent # Use Amber for accent

        style.configure('.', background=dark_bg, foreground=dark_fg)
        style.configure('TLabel', background=dark_bg, foreground=dark_fg)
        style.configure('TFrame', background=dark_bg)
        style.configure('TButton', background=google_primary, foreground=google_text_light, borderwidth=0)
        style.configure('TEntry', fieldbackground=google_surface_dark, foreground=google_text_light, insertcolor=google_text_light, borderwidth=0)
        style.configure('TMenubutton', background=google_primary, foreground=google_text_light)
        style.configure('TCheckbutton', background=dark_bg, foreground=dark_fg)
        style.configure('TLabelframe', background=dark_bg, foreground=dark_fg)
        style.configure('TLabelframe.Label', background=dark_bg, foreground=dark_fg)
        # Treeview
        style.configure('Treeview', background=google_surface_dark, foreground=google_text_light, fieldbackground=google_surface_dark, bordercolor=google_primary_dark, rowheight=25)
        style.configure('Treeview.Heading', background=google_primary_dark, foreground=google_text_light)
        style.map('TButton', background=[('active', google_primary_dark)])
        style.map('Treeview', background=[('selected', google_primary)]) # Highlight selected item
        root.configure(bg=dark_bg)

        # Update some styles for CustomMessageBox to fit new theme
        style.configure("Custom.TLabel", foreground=google_text_light, background=dark_bg)
        style.configure("Error.Custom.TLabel", foreground="#FF5252", background=dark_bg) # Red A200
        style.configure("Warning.Custom.TLabel", foreground="#FFD740", background=dark_bg) # Amber A200

class EditDialog:
    def __init__(self, parent, item):
        self.top = tk.Toplevel(parent)
        self.top.title(f"Edit Item: {item.name}")
        self.top.geometry("400x350")
        self.top.resizable(False, False)
        set_theme(self.top, light_mode=True)

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
                        entry.config(state='disabled') # Not directly editable for stocks
                elif field == 'Date of Purchase':
                    if self.item.category not in ['Stocks', 'Bonds']:
                        entry.insert(0, self.item.date_of_purchase)
                    else:
                        entry.config(state='disabled') # Not directly editable for stocks
                elif field == 'Current Value':
                    if self.item.category not in ['Stocks', 'Bonds']:
                        entry.insert(0, str(self.item.current_value))
                    else:
                        entry.config(state='disabled') # Not directly editable for stocks
        
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

            self.result = self.item # Return the updated item
            self.top.destroy()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for prices")
    
    def cancel(self):
        self.top.destroy()

class CustomMessageBox:
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

class PerformanceGraphDialog:
    def __init__(self, parent, item_data, db):
        self.top = tk.Toplevel(parent)
        self.top.title(f"Performance Graph - {item_data.name}")
        self.top.geometry("1000x800")
        set_theme(self.top, light_mode=True) # Apply light theme
        
        # Store database reference and item data
        self.db = db
        self.item_data = item_data
        self.comparison_items = []
        
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
        
        # Create main container
        main_container = ttk.Frame(self.top)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create control panel
        self.create_control_panel(main_container)
        
        # Create figure and axis
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[3, 1])
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=main_container)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add close button
        ttk.Button(main_container, text="Close", command=self.top.destroy).pack(pady=10)
        
        # Initial plot
        self.update_graph()
        
    def create_control_panel(self, parent):
        control_frame = ttk.LabelFrame(parent, text="Controls", padding="5")
        control_frame.pack(fill=tk.X, pady=5)
        
        # Time period selection
        ttk.Label(control_frame, text="Time Period:").pack(side=tk.LEFT, padx=5)
        self.period_var = tk.StringVar(value="1y")
        periods = [("1 Month", "1mo"), ("3 Months", "3mo"), ("6 Months", "6mo"), 
                  ("1 Year", "1y"), ("2 Years", "2y"), ("5 Years", "5y")]
        period_menu = ttk.OptionMenu(control_frame, self.period_var, "1y", *[p[1] for p in periods],
                                   command=lambda _: self.update_graph())
        period_menu.pack(side=tk.LEFT, padx=5)
        
        # Technical indicators
        ttk.Label(control_frame, text="Indicators:").pack(side=tk.LEFT, padx=5)
        self.indicator_vars = {
            "SMA": tk.BooleanVar(value=True),
            "EMA": tk.BooleanVar(value=False),
            "RSI": tk.BooleanVar(value=False),
            "MACD": tk.BooleanVar(value=False)
        }
        for indicator in self.indicator_vars:
            ttk.Checkbutton(control_frame, text=indicator, variable=self.indicator_vars[indicator],
                           command=self.update_graph).pack(side=tk.LEFT, padx=5)
        
        # Comparison section
        ttk.Label(control_frame, text="Compare with:").pack(side=tk.LEFT, padx=5)
        self.comparison_var = tk.StringVar()
        comparison_menu = ttk.OptionMenu(control_frame, self.comparison_var, "None", "None",
                                       command=self.add_comparison)
        comparison_menu.pack(side=tk.LEFT, padx=5)
        
        # Update comparison menu items
        comparison_menu['menu'].delete(0, 'end')
        for item_data in self.update_comparison_menu(): # Changed variable name to item_data for clarity
            comparison_menu['menu'].add_command(label=item_data, 
                                             command=lambda v=item_data: self.comparison_var.set(v))
        
    def update_comparison_menu(self):
        # Get all stocks and bonds from database
        rows = self.db.get_all_items()
        # Convert raw rows to Item objects for consistency
        from main import Item, Purchase
        all_items = []
        for row in rows:
            item_id, name, purchase_price, date_of_purchase, current_value, profit_loss, category, created_at, updated_at = row
            item = Item(name, category, purchase_price, date_of_purchase, current_value, profit_loss)
            item.id = item_id
            if category in ['Stocks', 'Bonds']:
                purchases_data = self.db.get_purchases_for_item(item_id)
                for p_date, p_amount, p_price in purchases_data:
                    item.add_purchase(Purchase(p_date, p_amount, p_price))
            all_items.append(item)

        self.comparison_items = [item for item in all_items if item.category in ['Stocks', 'Bonds'] 
                               and item.id != self.item_data.id] # Filter out the current item
        return ["None"] + [f"{item.name} ({item.category})" for item in self.comparison_items]
        
    def add_comparison(self, _):
        self.update_graph()
        
    def get_historical_data(self, item_data, period):
        """Fetches historical data for a given Item object (stock or bond)."""
        try:
            if item_data.category == 'Stocks':
                ticker_symbol = item_data.name.split()[0] if ' ' in item_data.name else item_data.name
                if ticker_symbol == 'VUSA':
                    exchanges = ['', '.L', '.AS', '.DE', '.PA']
                    for suffix in exchanges:
                        try:
                            ticker = yf.Ticker(ticker_symbol + suffix)
                            data = ticker.history(period=period)
                            if not data.empty:
                                return data
                        except:
                            continue
                    raise ValueError(f"No data found for VUSA on any exchange")
                else:
                    ticker = yf.Ticker(ticker_symbol)
                    data = ticker.history(period=period)
                if data.empty:
                    raise ValueError(f"No data found for ticker {ticker_symbol}")
                return data
            # For bonds, simulate data with less volatility
            dates = pd.date_range(end=datetime.now(), periods=365, freq='D')
            np.random.seed(42)
            daily_returns = np.random.normal(0.0002, 0.01, len(dates))  # Lower volatility for bonds
            cumulative_returns = (1 + daily_returns).cumprod()
            values = item_data.purchase_price * cumulative_returns
            return pd.DataFrame({'Close': values}, index=dates)
        except Exception as e:
            print(f"Error fetching data: {e}")
            messagebox.showerror("Error", f"Could not fetch data for {item_data.name}. Using simulated data instead.")
            # Fallback to simulated data
            dates = pd.date_range(end=datetime.now(), periods=365, freq='D')
            np.random.seed(42)
            daily_returns = np.random.normal(0.0005, 0.02, len(dates))
            cumulative_returns = (1 + daily_returns).cumprod()
            values = item_data.purchase_price * cumulative_returns
            return pd.DataFrame({'Close': values}, index=dates)
            
    def calculate_indicators(self, data):
        indicators = {}
        
        if self.indicator_vars["SMA"].get():
            indicators['SMA'] = ta.trend.sma_indicator(data['Close'], window=20)
            
        if self.indicator_vars["EMA"].get():
            indicators['EMA'] = ta.trend.ema_indicator(data['Close'], window=20)
            
        if self.indicator_vars["RSI"].get():
            indicators['RSI'] = ta.momentum.rsi(data['Close'], window=14)
            
        if self.indicator_vars["MACD"].get():
            macd = ta.trend.MACD(data['Close'])
            indicators['MACD'] = macd.macd()
            indicators['MACD Signal'] = macd.macd_signal()
            indicators['MACD Hist'] = macd.macd_diff()
            
        return indicators
        
    def update_graph(self):
        try:
            # Clear previous plots
            self.ax1.clear()
            self.ax2.clear()
            
            # Get data for main item
            data = self.get_historical_data(self.item_data, self.period_var.get())
            
            # Plot main item
            self.ax1.plot(data.index, data['Close'], label=self.item_data.name, linewidth=2)
            
            # Auto-scale y-axis based on price data
            min_price = data['Close'].min()
            max_price = data['Close'].max()
            y_margin = (max_price - min_price) * 0.1 if max_price > min_price else 1
            self.ax1.set_ylim(min_price - y_margin, max_price + y_margin)
            
            # Only plot purchase/current value lines if within 10% of min/max price
            # For PerformanceGraphDialog, purchase_price and current_value come from the Item object
            # which for stocks are placeholders, so we need to calculate them if purchases exist.
            purchase_price_for_display = self.item_data.get_total_invested() if self.item_data.category in ['Stocks', 'Bonds'] else self.item_data.purchase_price
            current_value_for_display = self.item_data.get_current_total_value({self.item_data.name: data['Close'].iloc[-1]}) if self.item_data.category in ['Stocks', 'Bonds'] else self.item_data.current_value

            if min_price - y_margin <= purchase_price_for_display <= max_price + y_margin:
                self.ax1.axhline(y=purchase_price_for_display, color='r', linestyle='--', label='Purchase Price')
            if min_price - y_margin <= current_value_for_display <= max_price + y_margin:
                self.ax1.axhline(y=current_value_for_display, color='g', linestyle='--', label='Current Value')
            
            # Add technical indicators
            indicators = self.calculate_indicators(data)
            for name, values in indicators.items():
                if name in ['MACD', 'MACD Signal', 'MACD Hist']:
                    self.ax2.plot(data.index, values, label=name)
                else:
                    self.ax1.plot(data.index, values, label=name, linestyle='--')
            
            # Add comparison if selected
            if self.comparison_var.get() != "None":
                # Find the comparison item object
                selected_comparison_name = self.comparison_var.get().split(' (')[0]
                comp_item = next((item for item in self.comparison_items if item.name == selected_comparison_name), None)
                if comp_item:
                    comp_data = self.get_historical_data(comp_item, self.period_var.get())
                    self.ax1.plot(comp_data.index, comp_data['Close'], label=f"{comp_item.name} (Comparison)",
                                linestyle=':', linewidth=2)
            
            # Customize the plot
            self.ax1.set_title(f'Performance Analysis: {self.item_data.name}')
            self.ax1.set_ylabel('Value (€)')
            self.ax1.grid(True)
            self.ax1.legend()
            
            if any(self.indicator_vars.values()):
                self.ax2.set_ylabel('Indicator Value')
                self.ax2.grid(True)
                if self.ax2.get_legend_handles_labels()[0]:
                    self.ax2.legend()
            
            # Rotate x-axis labels
            plt.xticks(rotation=45)
            
            # Adjust layout
            plt.tight_layout()
            
            # Redraw canvas
            self.canvas.draw()
            
            # Mark all purchases on the graph
            if hasattr(self.item_data, 'purchases') and self.item_data.purchases:
                data = self.get_historical_data(self.item_data, self.period_var.get())
                # Convert index to timezone-naive for comparison
                data.index = data.index.tz_localize(None)
                purchase_points = []
                for purchase in self.item_data.purchases:
                    purchase_date = pd.to_datetime(purchase.date)
                    # Find the closest date in the data
                    if purchase_date in data.index:
                        idx = data.index.get_loc(purchase_date)
                    else:
                        idx = data.index.get_indexer([purchase_date], method='nearest')[0]
                    price_at_purchase = data['Close'].iloc[idx]
                    point = self.ax1.scatter(data.index[idx], price_at_purchase, color='red', marker='o', label='Purchase' if purchase==self.item_data.purchases[0] else "")
                    purchase_points.append((point, purchase, data.index[idx], price_at_purchase))
                # Avoid duplicate legend entries
                handles, labels = self.ax1.get_legend_handles_labels()
                by_label = dict(zip(labels, handles))
                self.ax1.legend(by_label.values(), by_label.keys())
                # Add interactive tooltips
                if purchase_points:
                    scatter_objs = [pt[0] for pt in purchase_points]
                    cursor = mplcursors.cursor(scatter_objs, hover=True)
                    @cursor.connect("add")
                    def on_add(sel):
                        idx = scatter_objs.index(sel.artist)
                        purchase = purchase_points[idx][1]
                        sel.annotation.set(text=f"Date: {purchase.date}\nAmount: {purchase.amount}\nPrice: {purchase.price}")
                        sel.annotation.get_bbox_patch().set(fc="white")
            
        except Exception as e:
            print(f"Error updating graph: {e}")
            messagebox.showerror("Error", f"Error updating graph: {str(e)}")

class TechnicalIndicators:
    @staticmethod
    def sma(data, window=20):
        """Calculate Simple Moving Average"""
        return data.rolling(window=window).mean()
    
    @staticmethod
    def ema(data, window=20):
        """Calculate Exponential Moving Average"""
        return data.ewm(span=window, adjust=False).mean()
    
    @staticmethod
    def rsi(data, window=14):
        """Calculate Relative Strength Index"""
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    @staticmethod
    def macd(data, fast=12, slow=26, signal=9):
        """Calculate MACD, Signal, and Histogram"""
        exp1 = data.ewm(span=fast, adjust=False).mean()
        exp2 = data.ewm(span=slow, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        histogram = macd - signal_line
        return macd, signal_line, histogram

class PurchasesDialog:
    def __init__(self, parent, db, item_id, item_name):
        set_theme(parent, light_mode=True)
        self.db = db
        self.item_id = item_id
        self.top = tk.Toplevel(parent)
        set_theme(self.top, light_mode=True) # Apply light theme
        self.top.title(f"Purchases for {item_name}")
        self.top.geometry("500x400")
        self.purchases = self.db.get_purchases_for_item(item_id)

        # Purchases list
        self.tree = ttk.Treeview(self.top, columns=("Date", "Amount", "Price"), show='headings')
        for col in ("Date", "Amount", "Price"):
            self.tree.heading(col, text=col)
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
        ttk.Label(add_frame, text="Amount").grid(row=1, column=0, padx=5, pady=2)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=2)
        ttk.Label(add_frame, text="Price").grid(row=2, column=0, padx=5, pady=2)
        self.price_entry.grid(row=2, column=1, padx=5, pady=2)
        ttk.Button(add_frame, text="Add", command=self.add_purchase).grid(row=3, column=0, columnspan=2, pady=5)

        ttk.Button(self.top, text="Close", command=self.top.destroy).pack(pady=5)
        parent.wait_window(self.top)

    def refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for purchase in self.purchases:
            self.tree.insert('', tk.END, values=purchase)

    def add_purchase(self):
        date = self.date_entry.get()
        try:
            amount = float(self.amount_entry.get())
            price = float(self.price_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Amount and Price must be numbers.")
            return
        if not date:
            messagebox.showerror("Error", "Date is required.")
            return
        self.db.add_purchase(self.item_id, type('Purchase', (), {'date': date, 'amount': amount, 'price': price})())
        self.purchases = self.db.get_purchases_for_item(self.item_id)
        self.refresh_tree()
        self.date_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

class AddItemDialog:
    def __init__(self, parent, db, on_success):
        set_theme(parent, light_mode=True)
        self.db = db
        self.on_success = on_success
        self.top = tk.Toplevel(parent)
        set_theme(self.top, light_mode=True) # Apply light theme
        self.top.title("Add Item")
        self.top.geometry("400x350")
        self.top.resizable(False, False)
        # Fields
        ttk.Label(self.top, text="Name:").pack(pady=5)
        self.name_entry = ttk.Entry(self.top)
        self.name_entry.pack(pady=5, fill=tk.X, padx=20)
        ttk.Label(self.top, text="Category:").pack(pady=5)
        self.category_var = tk.StringVar(value="Stocks")
        categories = ["Stocks", "Bonds", "Appliances", "Electronics", "Furniture", "Transportation", "Home Improvement", "Savings", "Collectibles"]
        ttk.OptionMenu(self.top, self.category_var, self.category_var.get(), *categories).pack(pady=5, fill=tk.X, padx=20)
        # Optional initial purchase
        ttk.Label(self.top, text="Initial Purchase (optional)").pack(pady=10)
        frame = ttk.Frame(self.top)
        frame.pack(pady=2, fill=tk.X, padx=20)
        ttk.Label(frame, text="Date (YYYY-MM-DD)").grid(row=0, column=0, padx=2)
        self.date_entry = ttk.Entry(frame)
        self.date_entry.grid(row=0, column=1, padx=2)
        ttk.Label(frame, text="Amount").grid(row=1, column=0, padx=2)
        self.amount_entry = ttk.Entry(frame)
        self.amount_entry.grid(row=1, column=1, padx=2)
        ttk.Label(frame, text="Price").grid(row=2, column=0, padx=2)
        self.price_entry = ttk.Entry(frame)
        self.price_entry.grid(row=2, column=1, padx=2)
        ttk.Button(self.top, text="Add Item", command=self.add_item).pack(pady=15)
        ttk.Button(self.top, text="Cancel", command=self.top.destroy).pack()
        parent.wait_window(self.top)
    def add_item(self):
        name = self.name_entry.get().strip()
        category = self.category_var.get()
        if not name:
            messagebox.showerror("Error", "Name is required.")
            return

        # Get purchase details
        date = self.date_entry.get().strip()
        amount = self.amount_entry.get().strip()
        price = self.price_entry.get().strip()

        # Initialize values
        purchase_price = 0
        current_value = 0
        date_of_purchase = datetime.now().isoformat()
        profit_loss = 0

        # For non-stock items, use the entered values if provided
        if category not in ['Stocks', 'Bonds']:
            if date and amount and price:  # Only use values if all fields are provided
                try:
                    purchase_price = float(price)
                    current_value = float(price)  # Initially set current value same as purchase price
                    date_of_purchase = date
                    profit_loss = current_value - purchase_price
                except ValueError:
                    messagebox.showerror("Error", "Amount and Price must be numbers.")
                    return

        # Insert item
        now = datetime.now().isoformat()
        conn = sqlite3.connect(self.db.db_name)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO items (name, purchase_price, date_of_purchase, current_value, profit_loss, category, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, purchase_price, date_of_purchase, current_value, profit_loss, category, now, now))
        item_id = cursor.lastrowid

        # For stocks/bonds, add the purchase if provided
        if category in ['Stocks', 'Bonds'] and date and amount and price:
            try:
                amount = float(amount)
                price = float(price)
                cursor.execute('''
                INSERT INTO purchases (item_id, date, amount, price) VALUES (?, ?, ?, ?)
                ''', (item_id, date, amount, price))
            except ValueError:
                messagebox.showerror("Error", "Amount and Price must be numbers.")
                conn.commit()
                conn.close()
                return

        conn.commit()
        conn.close()
        self.top.destroy()
        self.on_success()

class MainDashboard:
    def __init__(self, root, db):
        set_theme(root, light_mode=True)
        self.root = root
        self.db = db
        self.root.title("Personal Finance Manager")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        self.create_layout()

    def create_layout(self):
        for i in range(2):
            self.root.rowconfigure(i, weight=1)
            self.root.columnconfigure(i, weight=1)
        # Top Left: Stock Performance Graph with controls
        self.frame_topleft = ttk.LabelFrame(self.root, text="Stock Performance", padding=10)
        self.frame_topleft.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        self.stock_controls_frame = ttk.Frame(self.frame_topleft)
        self.stock_controls_frame.pack(fill=tk.X, pady=(0, 10))
        self.show_stock_controls(self.stock_controls_frame)
        self.stock_graph_frame = ttk.Frame(self.frame_topleft)
        self.stock_graph_frame.pack(fill=tk.BOTH, expand=True)
        self.show_stock_performance_graph(self.stock_graph_frame)
        # Top Right: Controls
        self.frame_topright = ttk.LabelFrame(self.root, text="Controls", padding=10)
        self.frame_topright.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)
        self.show_topright_buttons(self.frame_topright)
        # Bottom Left: Expenses Graph with controls
        self.frame_bottomleft = ttk.LabelFrame(self.root, text="Expenses (Last Month)", padding=10)
        self.frame_bottomleft.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)
        self.expenses_controls_frame = ttk.Frame(self.frame_bottomleft)
        self.expenses_controls_frame.pack(fill=tk.X, pady=(0, 10))
        self.show_expenses_controls(self.expenses_controls_frame)
        self.expenses_graph_frame = ttk.Frame(self.frame_bottomleft)
        self.expenses_graph_frame.pack(fill=tk.BOTH, expand=True)
        self.show_expenses_graph(self.expenses_graph_frame)
        # Bottom Right: Placeholder
        self.frame_bottomright = ttk.LabelFrame(self.root, text="More Features Coming Soon", padding=10)
        self.frame_bottomright.grid(row=1, column=1, sticky="nsew", padx=8, pady=8)
        ttk.Label(self.frame_bottomright, text="(Reserved for future features)").pack(expand=True)

    def show_stock_controls(self, parent):
        # Dropdown for stock selection
        rows = self.db.get_all_items()
        stock_names = [row[1] for row in rows if row[6] == 'Stocks']
        self.selected_stock = tk.StringVar(value=stock_names[0] if stock_names else "")
        ttk.Label(parent, text="Stock:").pack(side=tk.LEFT, padx=5)
        stock_menu = ttk.OptionMenu(parent, self.selected_stock, self.selected_stock.get(), *stock_names, command=lambda _: self.update_stock_graph())
        stock_menu.pack(side=tk.LEFT, padx=5)
        # Time period selector
        self.stock_period = tk.StringVar(value="1y")
        ttk.Label(parent, text="Period:").pack(side=tk.LEFT, padx=5)
        period_menu = ttk.OptionMenu(parent, self.stock_period, "1y", "1mo", "3mo", "6mo", "1y", "2y", "5y", command=lambda _: self.update_stock_graph())
        period_menu.pack(side=tk.LEFT, padx=5)
        # Technical indicators
        self.indicators = {name: tk.BooleanVar(value=(name=="SMA")) for name in ["SMA", "EMA", "RSI", "MACD"]}
        for name in self.indicators:
            ttk.Checkbutton(parent, text=name, variable=self.indicators[name], command=self.update_stock_graph).pack(side=tk.LEFT, padx=2)

    def update_stock_graph(self):
        for widget in self.stock_graph_frame.winfo_children():
            widget.destroy()
        self.show_stock_performance_graph(self.stock_graph_frame)

    def show_stock_performance_graph(self, parent):
        rows = self.db.get_all_items()
        stock_item = next((item for item in self.get_loaded_items() if item.name == self.selected_stock.get()), None)
        if not stock_item:
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.text(0.5, 0.5, "No stock data", ha='center', va='center')
            canvas = FigureCanvasTkAgg(fig, master=parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            return

        period = self.stock_period.get()
        data = self.get_historical_data_for_stock(stock_item, period)
        data.index = data.index.tz_localize(None)
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(data.index, data['Close'], label=stock_item.name, linewidth=2)
        # Technical indicators
        indicators = self.calculate_indicators(data)
        for name, values in indicators.items():
            if name == 'MACD':
                continue  # Only plot MACD on a separate axis if needed
            ax.plot(data.index, values, label=name, linestyle='--')
        # Mark purchases
        if hasattr(stock_item, 'purchases') and stock_item.purchases:
            for purchase in stock_item.purchases:
                purchase_date = pd.to_datetime(purchase.date)
                if purchase_date in data.index:
                    idx = data.index.get_loc(purchase_date)
                else:
                    idx = data.index.get_indexer([purchase_date], method='nearest')[0]
                price_at_purchase = data['Close'].iloc[idx]
                point = ax.scatter(data.index[idx], price_at_purchase, color='red', marker='o')
        ax.set_title(f"Performance: {stock_item.name}")
        ax.set_ylabel('Value (€)')
        ax.grid(True)
        ax.legend()
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        mplcursors.cursor(ax.collections, hover=True)

    def get_loaded_items(self):
        """Helper to get all loaded items from the database as Item objects."""
        from main import load_portfolio
        return load_portfolio()

    def get_historical_data_for_stock(self, item_data, period):
        """Fetches historical data for a given stock Item object."""
        try:
            ticker_symbol = item_data.name.split()[0] if ' ' in item_data.name else item_data.name
            if ticker_symbol == 'VUSA':
                exchanges = ['', '.L', '.AS', '.DE', '.PA']
                for suffix in exchanges:
                    try:
                        ticker = yf.Ticker(ticker_symbol + suffix)
                        data = ticker.history(period=period)
                        if not data.empty:
                            return data
                    except:
                        continue
                raise ValueError(f"No data found for VUSA on any exchange")
            else:
                ticker = yf.Ticker(ticker_symbol)
                data = ticker.history(period=period)
            if data.empty:
                raise ValueError(f"No data found for ticker {ticker_symbol}")
            return data
        except Exception as e:
            print(f"Error fetching data: {e}")
            messagebox.showerror("Error", f"Could not fetch data for {item_data.name}. Using simulated data instead.")
            # Fallback to simulated data
            dates = pd.date_range(end=datetime.now(), periods=365, freq='D')
            np.random.seed(42)
            daily_returns = np.random.normal(0.0005, 0.02, len(dates))
            cumulative_returns = (1 + daily_returns).cumprod()
            values = item_data.purchase_price * cumulative_returns # This will use the Item's purchase_price for simulation
            return pd.DataFrame({'Close': values}, index=dates)

    def calculate_indicators(self, data):
        indicators = {}
        if self.indicators["SMA"].get():
            indicators['SMA'] = TechnicalIndicators.sma(data['Close'])
        if self.indicators["EMA"].get():
            indicators['EMA'] = TechnicalIndicators.ema(data['Close'])
        if self.indicators["RSI"].get():
            indicators['RSI'] = TechnicalIndicators.rsi(data['Close'])
        if self.indicators["MACD"].get():
            macd, signal, hist = TechnicalIndicators.macd(data['Close'])
            indicators['MACD'] = macd
        return indicators

    def show_expenses_controls(self, parent):
        # Date range selector
        self.expenses_period = tk.StringVar(value="1mo")
        ttk.Label(parent, text="Period:").pack(side=tk.LEFT, padx=5)
        period_menu = ttk.OptionMenu(parent, self.expenses_period, "1mo", "7d", "1mo", "3mo", command=lambda _: self.update_expenses_graph())
        period_menu.pack(side=tk.LEFT, padx=5)
        # (Optional) Category filter placeholder
        # ttk.Label(parent, text="Category:").pack(side=tk.LEFT, padx=5)
        # ttk.OptionMenu(parent, tk.StringVar(), "All").pack(side=tk.LEFT, padx=5)

    def update_expenses_graph(self):
        for widget in self.expenses_graph_frame.winfo_children():
            widget.destroy()
        self.show_expenses_graph(self.expenses_graph_frame)

    def show_expenses_graph(self, parent):
        import numpy as np
        import pandas as pd
        from datetime import datetime, timedelta
        today = datetime.now()
        period = self.expenses_period.get()
        if period == "7d":
            days = 7
        elif period == "3mo":
            days = 90
        else:
            days = 30
        dates = [today - timedelta(days=i) for i in range(days-1, -1, -1)]
        expenses = np.random.randint(10, 100, size=days)
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(dates, expenses, marker='o', color='purple')
        ax.set_title(f"Expenses (Last {days} Days)")
        ax.set_ylabel('Amount (€)')
        ax.set_xlabel('Date')
        ax.grid(True)
        fig.autofmt_xdate()
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_topright_buttons(self, parent):
        button_frame = ttk.Frame(parent)
        button_frame.pack(expand=True, fill=tk.BOTH, pady=20)
        ttk.Button(button_frame, text="View Items", command=self.open_portfolio_window).pack(pady=10, padx=20, fill=tk.X)
        ttk.Button(button_frame, text="Add Item", command=self.add_item_gui).pack(pady=10, padx=20, fill=tk.X)

    def open_portfolio_window(self):
        top = tk.Toplevel(self.root)
        app = PersonalFinanceApp(top)

    def add_item_gui(self):
        # Use the AddItemDialog for adding new items
        AddItemDialog(self.root, self.db, self.refresh_dashboard)

    def refresh_dashboard(self):
        # Redraw graphs and controls
        for widget in self.stock_graph_frame.winfo_children():
            widget.destroy()
        for widget in self.expenses_graph_frame.winfo_children():
            widget.destroy()
        for widget in self.stock_controls_frame.winfo_children():
            widget.destroy()
        for widget in self.expenses_controls_frame.winfo_children():
            widget.destroy()
        self.show_stock_controls(self.stock_controls_frame)
        self.show_stock_performance_graph(self.stock_graph_frame)
        self.show_expenses_controls(self.expenses_controls_frame)
        self.show_expenses_graph(self.expenses_graph_frame)

class PersonalFinanceApp:
    def __init__(self, root):
        set_theme(root, light_mode=True) # Apply theme to this window
        self.root = root
        self.root.title("Portfolio")
        self.root.geometry("1000x600")
        self.db = Database()
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

    def create_right_panel(self, parent):
        right_frame = ttk.LabelFrame(parent, text="Portfolio", padding="10")
        right_frame.pack(fill=tk.BOTH, expand=True)
        columns = ('ID', 'Name', 'Purchase Price', 'Date', 'Current Value', 'Profit/Loss', 'Category')
        self.tree = ttk.Treeview(right_frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.column('ID', width=0, stretch=False)
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        button_frame = ttk.Frame(right_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Export Portfolio", command=self.export_portfolio_gui).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load Portfolio", command=self.load_portfolio_gui).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit Selected", command=self.edit_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="View Performance", command=self.show_performance).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="View/Add Purchases", command=self.view_purchases).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset Demo Data", command=self.reset_demo_data).pack(side=tk.LEFT, padx=5)
        self.total_value_label = ttk.Label(right_frame, text="Total Value: €0.00")
        self.total_value_label.grid(row=2, column=0, columnspan=2, pady=5)

    def update_portfolio_display(self):
        # Clear existing items
        for item_in_tree in self.tree.get_children():
            self.tree.delete(item_in_tree)
            
        # Get items from main.py's load_portfolio, which returns rich Item objects
        from main import load_portfolio
        self.items = load_portfolio() # Store loaded items in self.items

        # Fetch current stock prices for calculation
        current_prices = {}
        stock_names_to_fetch = set()
        for item in self.items:
            if item.category in ['Stocks', 'Bonds']:
                stock_names_to_fetch.add(item.name) # Use the item name as ticker
        
        for stock_name in stock_names_to_fetch:
            ticker_symbol = stock_name.split()[0] if ' ' in stock_name else stock_name
            price = 0.0 # Default to 0
            # Try different exchange suffixes for VUSA or general tickers
            if ticker_symbol == 'VUSA':
                exchanges = ['', '.L', '.AS', '.DE', '.PA', '.MI']
            else:
                exchanges = [''] # For other tickers, try direct
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
        for item in self.items:
            display_purchase_price = ""
            display_current_value = ""
            display_profit_loss = ""
            display_date = ""

            if item.category in ['Stocks', 'Bonds']:
                total_invested = item.get_total_invested()
                current_total_value = item.get_current_total_value(current_prices) # Pass prices
                profit_loss = item.get_overall_profit_loss(current_prices)
                most_recent_purchase_date = max(p.date for p in item.purchases) if item.purchases else ""

                display_purchase_price = f"€{total_invested:.2f}" # Total invested
                display_current_value = f"€{current_total_value:.2f}" # Current aggregated value
                display_profit_loss = f"€{profit_loss:.2f}"
                display_date = most_recent_purchase_date

            else: # Household items and others
                display_purchase_price = f"€{item.purchase_price:.2f}"
                display_current_value = f"€{item.current_value:.2f}"
                display_profit_loss = f"€{item.profit_loss:.2f}"
                display_date = item.date_of_purchase
            
            # Store the actual Item object (or its ID) with the treeview row
            # For editing/deleting later, we need to retrieve the original Item object
            self.tree.insert('', tk.END, values=(
                item.id,  # ID
                item.name,  # Name
                display_purchase_price,  # Purchase Price (aggregated for stocks)
                display_date,  # Date (most recent for stocks)
                display_current_value,  # Current Value (aggregated for stocks)
                display_profit_loss,  # Profit/Loss (aggregated for stocks)
                item.category   # Category
            ), iid=item.id) # Use item.id as iid for easy lookup
            
        # Update total portfolio value across all items
        total_portfolio_value = 0
        for item in self.items:
            if item.category in ['Stocks', 'Bonds']:
                total_portfolio_value += item.get_current_total_value(current_prices)
            else:
                total_portfolio_value += item.current_value
        self.total_value_label.config(text=f"Total Value: €{total_portfolio_value:.2f}")

    def edit_selected(self):
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
                    # For stocks/bonds, only update name and category in base item table
                    self.db.update_base_item(
                        updated_item.id, updated_item.name, 0, "", 0, 0, # Placeholders for derived values
                        updated_item.category, datetime.now().isoformat()
                    )
                self.load_portfolio_gui() # Refresh the display

    def delete_selected(self):
        selected_item_id = self.tree.focus()
        if not selected_item_id:
            CustomMessageBox(self.root, "Error", "Please select an item to delete.", type="error")
            return
        # Confirm deletion
        if messagebox.askyesno("Delete Item", "Are you sure you want to delete the selected item?"):
            self.db.delete_item(selected_item_id) # Use the item ID directly
            self.load_portfolio_gui() # Refresh the display

    def show_performance(self):
        selected_item_id = self.tree.focus()
        if not selected_item_id:
            CustomMessageBox(self.root, "Error", "Please select an item to view performance.", type="error")
            return
        # Retrieve the Item object from self.items using its ID
        item_to_show_performance = next((item for item in self.items if str(item.id) == selected_item_id), None)
        if item_to_show_performance and item_to_show_performance.category in ['Stocks', 'Bonds']:
            PerformanceGraphDialog(self.root, item_to_show_performance, self.db)
        else:
            CustomMessageBox(self.root, "Info", "Performance graph is only available for Stocks and Bonds.", type="info")

    def view_purchases(self):
        selected_item_id = self.tree.focus()
        if not selected_item_id:
            CustomMessageBox(self.root, "Error", "Please select an item to view purchases.", type="error")
            return
        # Retrieve the Item object from self.items using its ID
        item_to_view_purchases = next((item for item in self.items if str(item.id) == selected_item_id), None)
        if item_to_view_purchases and item_to_view_purchases.category in ['Stocks', 'Bonds']:
            PurchasesDialog(self.root, self.db, item_to_view_purchases.id, item_to_view_purchases.name)
            self.load_portfolio_gui() # Refresh display after purchases are added/modified
        else:
            CustomMessageBox(self.root, "Info", "Purchase details are only available for Stocks and Bonds.", type="info")

    def reset_demo_data(self):
        if messagebox.askyesno("Reset Data", "Are you sure you want to reset all data to demo data?"):
            self.db.clear_all_items()
            self.db.clear_all_purchases()
            from main import mock_items # Import mock_items from main
            self.db.add_mock_data(mock_items)
            self.load_portfolio_gui()

    def save_portfolio_gui(self):
        from main import save_portfolio
        save_portfolio(self.items)
        CustomMessageBox(self.root, "Success", "Portfolio saved successfully!")

    def export_portfolio_gui(self):
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
                    # Write header
                    writer.writerow(['ID', 'Name', 'Purchase Price', 'Date', 'Current Value', 'Profit/Loss', 'Category'])
                    
                    # Write data
                    for item_id in self.tree.get_children():
                        values = self.tree.item(item_id)['values']
                        writer.writerow(values)
                        
                CustomMessageBox(self.root, "Success", "Portfolio exported successfully!")
            except Exception as e:
                CustomMessageBox(self.root, "Error", f"Error exporting portfolio: {str(e)}", type="error")        

    def load_portfolio_gui(self):
        self.update_portfolio_display()

if __name__ == "__main__":
    root = tk.Tk()
    db = Database()
    dashboard = MainDashboard(root, db)
    root.mainloop() 
