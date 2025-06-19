# Database Migration Guide

## Overview
This guide covers the migration from a single `items` table to category-specific tables (`investments`, `inventory`, `expenses`).

## When Migration is Needed
- When pulling this branch for the first time
- When deploying to production
- When team members have existing data in the old format

## Migration Process

### 1. Check if Migration is Needed
```bash
python migrate_database.py --check
```

**Exit codes:**
- `0`: No migration needed (already using new structure)
- `1`: Migration needed (old data found)

### 2. Run Migration

**Interactive Mode (Recommended for Development):**
```bash
python migrate_database.py
```

**Automated Mode (For CI/CD):**
```bash
python migrate_database.py --auto
```

### 3. Verify Migration
The script will show a summary of items in each table after migration.

## Database Structure Changes

### Before (Single Table)
```
items (all categories mixed)
├── id, name, purchase_price, date_of_purchase
├── current_value, profit_loss, category
└── created_at, updated_at
```

### After (Category-Specific Tables)
```
investments (Stocks, Bonds, Crypto, Real Estate, Gold)
├── Same columns as original items table
└── Linked to purchases table for transaction history

inventory (Appliances, Electronics, Furniture, etc.)
├── Same columns as original items table
└── Physical items and collectibles

expenses (Expense category)
├── Same columns as original items table
└── Expenditure tracking
```

## Deployment Checklist

### For Team Members
- [ ] Pull the latest branch
- [ ] Run `python migrate_database.py --check`
- [ ] If migration needed, run `python migrate_database.py`
- [ ] Verify data in GUI (check Investment/Inventory/Expense categories)

### For CI/CD Pipeline
- [ ] Add migration check to deployment script
- [ ] Run `python migrate_database.py --auto` during deployment
- [ ] Verify exit code (0 = success)

### For Production Deployment
- [ ] Backup existing database
- [ ] Test migration on staging environment
- [ ] Run migration during maintenance window
- [ ] Verify all data migrated correctly
- [ ] Test application functionality

## Rollback Plan
If issues occur, restore from the database backup taken before migration.

## Support
If migration fails or data appears incorrect, check:
1. Database file permissions
2. Sufficient disk space
3. No conflicting database connections

The migration preserves all original data and adds it to appropriate category-specific tables. 