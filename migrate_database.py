#!/usr/bin/env python3
"""
Database Migration Script - Single Items Table to Category-Specific Tables

This script migrates existing data from the old single 'items' table 
to the new category-specific tables (investments, inventory, expenses).

Usage:
    python migrate_database.py                    # Interactive mode
    python migrate_database.py --auto             # Auto-migrate if needed
    python migrate_database.py --check            # Check migration status only
"""

import sys
from database import Database

def check_migration_needed():
    """Check if migration is needed"""
    db = Database()
    try:
        old_items = db.get_table_items('items')
        return len(old_items) > 0
    except:
        return False

def main():
    """Run the database migration."""
    auto_mode = '--auto' in sys.argv
    check_only = '--check' in sys.argv
    
    print("=== Personal Finance Database Migration ===")
    print("Moving items from 'items' table to category-specific tables...")
    
    # Check if migration is needed
    migration_needed = check_migration_needed()
    
    if check_only:
        if migration_needed:
            print("Migration needed: Old 'items' table contains data")
            sys.exit(1)
        else:
            print("Migration not needed: Database already using new structure")
            sys.exit(0)
    
    if not migration_needed:
        print("Database already migrated or no migration needed.")
        print("   All items are already in category-specific tables.")
        return
    
    if not auto_mode:
        # Ask for confirmation in interactive mode
        print("This will move items from 'items' table to:")
        print("   • investments (Stocks, Bonds, Crypto, etc.)")
        print("   • inventory (Appliances, Electronics, etc.)")  
        print("   • expenses (Expense category)")
        print()
        confirm = input("Do you want to proceed with the migration? (y/N): ").lower()
        if confirm != 'y':
            print("Migration cancelled.")
            return
    
    # Create database instance
    db = Database()
    
    # Run migration
    try:
        migrated_count = db.migrate_items_to_category_tables()
        print(f"Migration successful! {migrated_count} items migrated.")
        
        # Show summary of items in each table
        print("\nSummary after migration:")
        investments = db.get_table_items('investments')
        inventory = db.get_table_items('inventory')
        expenses = db.get_table_items('expenses')
        remaining_items = db.get_table_items('items')
        
        print(f"   Investments: {len(investments)} items")
        print(f"   Inventory: {len(inventory)} items")
        print(f"   Expenses: {len(expenses)} items")
        if remaining_items:
            print(f"   Remaining in items table: {len(remaining_items)} items")
        
        print("\nDatabase migration completed successfully!")
        
    except Exception as e:
        print(f"Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 