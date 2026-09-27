# 📦 Core Project: Inventory Management System

## The Smart Inventory with Reorder Alerts 🏪

Build a professional inventory management system with **automatic reorder alerts, stock management, sales tracking, profit analysis, inventory analytics, and data export**.

The system should manage products, suppliers, stock levels, sales history, and inventory performance.

---

## 📊 Data Structure

The system uses nested dictionaries and lists to represent products, categories, suppliers, stock, and sales information.

```python
inventory = {
    "categories": ["Electronics", "Clothing", "Food", "Books"],

    "products": {
        "PRD001": {
            "name": "Laptop Pro X",
            "category": "Electronics",
            "price": 1200.00,
            "cost": 800.00,
            "stock": 10,
            "reorder_level": 5,
            "reorder_quantity": 20,
            "supplier": "TechDistributors",
            "location": "Aisle 3, Shelf 2",
            "barcode": "1234567890123",
            "sales": [
                {"month": "Jan", "units": 15},
                {"month": "Feb", "units": 12},
                {"month": "Mar", "units": 18}
            ],
            "date_added": "2026-01-15",
            "last_updated": "2026-03-20"
        }
    },

    "suppliers": {
        "TechDistributors": {
            "contact": "080-1234-5678",
            "email": "orders@techdist.com",
            "lead_time": 3
        }
    }
}
```

---

# 📋 Requirements

## 1. Core Inventory Operations

Implement the fundamental inventory operations.

### `add_product(name, category, price, cost, stock, reorder_level)`

Add a new product to the inventory.

### `update_stock(product_id, quantity)`

Update the stock quantity.

* Positive quantity → Restock
* Negative quantity → Reduce stock / sale

### `search_products(query)`

Search products by:

* Product name
* Category
* Product ID

### `get_product_details(product_id)`

Display complete information about a product.

---

# 📦 2. Inventory Management — HARD

The system must monitor stock levels and inventory value.

### `get_low_stock_items()`

Return products whose stock is below their reorder level.

### `get_out_of_stock_items()`

Return products whose stock is `0`.

### `calculate_inventory_value()`

Calculate the total inventory value using:

```text
cost × stock
```

### `calculate_sales_value()`

Calculate the total sales value using:

```text
price × units sold
```

### `generate_reorder_report()`

Generate a report showing products that need to be reordered.

### `apply_markdown(category, percentage)`

Apply a percentage discount to all products within a specified category.

---

# 📊 3. Sales Analytics — HARDER

The system must track and analyze sales.

### `record_sale(product_id, quantity)`

Record a sale by:

* Updating stock
* Recording the sale
* Tracking revenue

### `get_top_selling_products(n)`

Return the top `n` products based on units sold.

### `get_sales_by_category()`

Group sales according to product category.

### `get_profit_analysis()`

Calculate:

* Profit per product
* Profit per category
* Unit profit
* Total profit
* Profit margins

### `generate_sales_report(start_date, end_date)`

Generate a sales report for a specified date range.

---

# 🧠 4. Advanced Features — HARDEST

Implement more advanced inventory analysis.

### `get_recommended_reorder()`

Analyze sales trends and recommend appropriate reorder quantities.

### `get_abc_analysis()`

Classify inventory items according to their value:

* **A** — High-value items
* **B** — Medium-value items
* **C** — Low-value items

### `get_inventory_turnover()`

Calculate how quickly inventory is being sold and replaced.

---

# 💾 5. Data Export — SUPER HARD

The system should support data export and reporting.

Requirements:

* Export inventory data to JSON for backup.
* Generate a PDF inventory report as a bonus feature.

---

# 🖥️ Sample Interface

```text
📦 INVENTORY MANAGEMENT SYSTEM 📦

1. Add Product
2. Update Stock
3. Search Products
4. Low Stock Report
5. Record Sale
6. Analytics
7. Generate Reports
8. Exit

Choice: 4
```

### Low Stock Report

```text
⚠️ LOW STOCK ALERT!
====================================

Product: Laptop Pro X (PRD001)
Category: Electronics
Current Stock: 10
Reorder Level: 5
⚠️ Above reorder level

Product: Coffee Beans (PRD005)
Category: Food
Current Stock: 3
Reorder Level: 10
🚨 BELOW REORDER LEVEL!
Suggested order: 20 units

Product: T-Shirt (PRD008)
Category: Clothing
Current Stock: 0
🛑 OUT OF STOCK!
Immediate action required!

====================================
Total items below reorder: 5
Total out of stock: 3
```

---

# 📈 Profit Analysis

```text
📊 PROFIT ANALYSIS
====================================

Product: Laptop Pro X
Unit Profit: $400.00 (33.3% margin)
Units Sold: 45
Total Profit: $18,000.00

Product: Coffee Beans
Unit Profit: $5.00 (20.0% margin)
Units Sold: 120
Total Profit: $600.00

====================================

Total Inventory Value: $125,450.00
Total Sales Value: $89,200.00
Total Profit: $32,500.00
```

### Category Summary

```text
📊 CATEGORY SUMMARY:

Electronics: $42,000.00 (47% of sales)
Food: $25,600.00 (29% of sales)
Clothing: $21,600.00 (24% of sales)
```

### Top-Selling Products

```text
📈 TOP SELLING PRODUCTS:

1. Laptop Pro X - 45 units
2. Coffee Beans - 120 units
3. T-Shirt - 200 units
```

---

# 🧠 Concepts Tested

This project tests the ability to work with:

* Nested dictionaries
* Lists
* Nested data structures
* Complex sorting
* List and dictionary comprehensions
* Functions with multiple return values
* File I/O
* JSON data
* Statistical calculations
* Data aggregation
* Stock management
* Sales tracking
* Profit calculations
* Search and filtering
* Inventory analytics
* Reorder logic
* Data export
