'''
2️⃣ 📦 HARD INVENTORY MANAGEMENT SYSTEM
The Smart Inventory with Reorder Alerts 🏪

Build a professional inventory system with automatic reorder alerts and sales tracking.

Data Structure:
python

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
            "sales": [  # Monthly sales
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
            "lead_time": 3  # Days
        }
    }
}

Requirements:

    Core Inventory Operations:

        add_product(name, category, price, cost, stock, reorder_level) → Add new product

        update_stock(product_id, quantity) → Update stock (positive for restock, negative for sale)

        search_products(query) → Search by name, category, or ID

        get_product_details(product_id) → Show full product info

    Inventory Management (HARD):

        get_low_stock_items() → Products below reorder_level

        get_out_of_stock_items() → Products with 0 stock

        calculate_inventory_value() → Total value (cost × stock)

        calculate_sales_value() → Total sales value (price × units sold)

        generate_reorder_report() → What needs reordering

        apply_markdown(category, percentage) → Apply discount to all products in category

    Sales Analytics (HARDER):

        record_sale(product_id, quantity) → Record sale, update stock, record revenue

        get_top_selling_products(n) → Top n by units sold

        get_sales_by_category() → Sales grouped by category

        get_profit_analysis() → Calculate profit per product and category

        generate_sales_report(start_date, end_date) → Sales in date range

    Advanced Features (HARDEST):

        get_recommended_reorder() → Based on sales trends, suggest reorder quantities

        get_abc_analysis() → Classify items as A (high value), B (medium), C (low)

        get_inventory_turnover() → How quickly inventory sells

    Data Export (SUPER HARD):

        Export to JSON for backup

        Generate PDF report (bonus)

Sample Output:
text

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

Choice: 6

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

📊 CATEGORY SUMMARY:
Electronics: $42,000.00 (47% of sales)
Food: $25,600.00 (29% of sales)
Clothing: $21,600.00 (24% of sales)

📈 TOP SELLING PRODUCTS:
1. Laptop Pro X - 45 units
2. Coffee Beans - 120 units
3. T-Shirt - 200 units

Concepts Tested: Nested dictionaries, lists, complex sorting, comprehensions, functions with multiple returns, file I/O, statistical calculations, data aggregation

'''


import json
import os
from datetime import date

INVENTORY_FILE = "inventory.json"
MONTH_ORDER = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

inventory = {
    "categories": ["Electronics", "Clothing", "Food", "Books"],
    "products": {},
    "suppliers": {},
}


# --- PERSISTENCE ---

def load_inventory():
    global inventory
    if os.path.exists(INVENTORY_FILE):
        try:
            with open(INVENTORY_FILE, "r") as f:
                inventory = json.load(f)
        except (json.JSONDecodeError, OSError):
            print("\u26a0\ufe0f  Could not read inventory.json \u2014 starting with an empty inventory.")


def export_to_json(filename=INVENTORY_FILE):
    with open(filename, "w") as f:
        json.dump(inventory, f, indent=2)
    return f"\u2705 Exported inventory to {filename}."


def _autosave():
    export_to_json()


# --- CORE INVENTORY OPERATIONS ---

def _generate_product_id():
    existing_nums = [int(pid[3:]) for pid in inventory["products"] if pid.startswith("PRD") and pid[3:].isdigit()]
    return f"PRD{max(existing_nums, default=0) + 1:03d}"


def add_product(name, category, price, cost, stock, reorder_level,
                 reorder_quantity=None, supplier=None, location=None, barcode=None):
    if category not in inventory["categories"]:
        inventory["categories"].append(category)

    product_id = _generate_product_id()
    today = date.today().isoformat()

    inventory["products"][product_id] = {
        "name": name,
        "category": category,
        "price": price,
        "cost": cost,
        "stock": stock,
        "reorder_level": reorder_level,
        "reorder_quantity": reorder_quantity if reorder_quantity is not None else reorder_level * 2,
        "supplier": supplier,
        "location": location,
        "barcode": barcode,
        "sales": [],
        "date_added": today,
        "last_updated": today,
    }
    _autosave()
    return product_id


def update_stock(product_id, quantity):
    """quantity: positive to restock, negative for a manual stock reduction."""
    if product_id not in inventory["products"]:
        return f"\u274c Product '{product_id}' not found."

    product = inventory["products"][product_id]
    new_stock = product["stock"] + quantity
    if new_stock < 0:
        return f"\u274c Cannot reduce stock below 0 (current: {product['stock']}, requested change: {quantity})."

    product["stock"] = new_stock
    product["last_updated"] = date.today().isoformat()
    _autosave()
    return f"\u2705 Stock updated. {product['name']} now at {new_stock} units."


def search_products(query):
    q = query.lower()
    return {
        pid: p for pid, p in inventory["products"].items()
        if q in pid.lower() or q in p["name"].lower() or q in p["category"].lower()
    }


def get_product_details(product_id):
    return inventory["products"].get(product_id)


# --- INVENTORY MANAGEMENT ---

def get_low_stock_items():
    """Per the written spec: products where stock is below reorder_level.
    (Note: the spec's own sample transcript lists a product safely ABOVE its
    reorder level under 'Low Stock Report' too — that's inconsistent with
    the function's own stated definition, so this follows the definition,
    not the sample.)"""
    return {pid: p for pid, p in inventory["products"].items() if p["stock"] < p["reorder_level"]}


def get_out_of_stock_items():
    return {pid: p for pid, p in inventory["products"].items() if p["stock"] == 0}


def calculate_inventory_value():
    return sum(p["cost"] * p["stock"] for p in inventory["products"].values())


def _total_units_sold(product):
    return sum(entry["units"] for entry in product["sales"])


def calculate_sales_value():
    return sum(p["price"] * _total_units_sold(p) for p in inventory["products"].values())


def generate_reorder_report():
    low_stock = get_low_stock_items()
    return {
        pid: {
            "name": p["name"],
            "current_stock": p["stock"],
            "reorder_level": p["reorder_level"],
            "suggested_order": p["reorder_quantity"],
        }
        for pid, p in low_stock.items()
    }


def apply_markdown(category, percentage):
    affected = [p for p in inventory["products"].values() if p["category"] == category]
    for product in affected:
        product["price"] = round(product["price"] * (1 - percentage / 100), 2)
        product["last_updated"] = date.today().isoformat()
    _autosave()
    return f"\u2705 Applied {percentage}% markdown to {len(affected)} product(s) in '{category}'."


# --- SALES ANALYTICS ---

def record_sale(product_id, quantity, month=None):
    if product_id not in inventory["products"]:
        return f"\u274c Product '{product_id}' not found."

    product = inventory["products"][product_id]
    if quantity > product["stock"]:
        return f"\u274c Not enough stock. Only {product['stock']} {product['name']} available."

    month = month or MONTH_ORDER[date.today().month - 1]

    existing_entry = next((s for s in product["sales"] if s["month"] == month), None)
    if existing_entry:
        existing_entry["units"] += quantity
    else:
        product["sales"].append({"month": month, "units": quantity})

    product["stock"] -= quantity
    product["last_updated"] = date.today().isoformat()
    revenue = quantity * product["price"]
    _autosave()
    return f"\u2705 Sold {quantity}x {product['name']} for ${revenue:,.2f}. Stock now {product['stock']}."


def get_top_selling_products(n):
    ranked = sorted(
        inventory["products"].items(),
        key=lambda item: _total_units_sold(item[1]),
        reverse=True,
    )
    return [(pid, p["name"], _total_units_sold(p)) for pid, p in ranked[:n]]


def get_sales_by_category():
    by_category = {}
    for p in inventory["products"].values():
        value = p["price"] * _total_units_sold(p)
        by_category[p["category"]] = by_category.get(p["category"], 0) + value
    return by_category


def get_profit_analysis():
    analysis = {}
    for pid, p in inventory["products"].items():
        unit_profit = p["price"] - p["cost"]
        margin = (unit_profit / p["price"] * 100) if p["price"] else 0
        units_sold = _total_units_sold(p)
        analysis[pid] = {
            "name": p["name"],
            "unit_profit": unit_profit,
            "margin_pct": margin,
            "units_sold": units_sold,
            "total_profit": unit_profit * units_sold,
        }
    return analysis


def generate_sales_report(start_month, end_month):
    """NOTE: the given data only records sales by month NAME (e.g. 'Jan'),
    with no year — so this filters by month order within a single assumed
    year rather than true calendar dates. A real date-range report would
    need actual dates stored per sale, which the spec's data structure
    doesn't provide."""
    if start_month not in MONTH_ORDER or end_month not in MONTH_ORDER:
        return None

    start_idx = MONTH_ORDER.index(start_month)
    end_idx = MONTH_ORDER.index(end_month)

    report = {}
    for pid, p in inventory["products"].items():
        units_in_range = sum(
            s["units"] for s in p["sales"]
            if start_idx <= MONTH_ORDER.index(s["month"]) <= end_idx
        )
        if units_in_range > 0:
            report[pid] = {"name": p["name"], "units": units_in_range, "revenue": units_in_range * p["price"]}
    return report


# --- ADVANCED FEATURES ---

def get_recommended_reorder():
    """Simplified trend-based suggestion: average monthly sales x 2 months
    of buffer stock, minus what's currently on hand. Only surfaced for
    items already at or below their reorder level."""
    recommendations = {}
    for pid, p in get_low_stock_items().items():
        months_tracked = len(p["sales"]) or 1
        avg_monthly_sales = _total_units_sold(p) / months_tracked
        suggested = max(round(avg_monthly_sales * 2) - p["stock"], p["reorder_quantity"])
        recommendations[pid] = {"name": p["name"], "suggested_quantity": suggested}
    return recommendations


def get_abc_analysis():
    """Classic Pareto classification by sales value: A = top ~80% of
    cumulative value, B = next ~15%, C = remaining ~5%."""
    values = [(pid, p["price"] * _total_units_sold(p)) for pid, p in inventory["products"].items()]
    values.sort(key=lambda item: item[1], reverse=True)

    total_value = sum(v for _, v in values)
    if total_value == 0:
        return {pid: "C" for pid, _ in values}

    classification = {}
    running_total = 0
    for pid, value in values:
        running_total += value
        cumulative_pct = running_total / total_value * 100
        if cumulative_pct <= 80:
            classification[pid] = "A"
        elif cumulative_pct <= 95:
            classification[pid] = "B"
        else:
            classification[pid] = "C"
    return classification


def get_inventory_turnover():
    """Simplified turnover: units sold / current stock. Higher = sells faster.
    (A textbook version uses average inventory over a period, which isn't
    tracked here — this is a reasonable approximation given the data available.)"""
    turnover = {}
    for pid, p in inventory["products"].items():
        units_sold = _total_units_sold(p)
        turnover[pid] = (units_sold / p["stock"]) if p["stock"] > 0 else float("inf") if units_sold > 0 else 0
    return turnover


# --- DISPLAY / MENU HANDLERS ---

def print_low_stock_report():
    low_stock = get_low_stock_items()
    out_of_stock = get_out_of_stock_items()

    print("\n\u26a0\ufe0f  LOW STOCK ALERT!")
    print("=" * 36)
    if not low_stock:
        print("No products are below their reorder level.")
    for pid, p in low_stock.items():
        print(f"Product: {p['name']} ({pid})")
        print(f"Category: {p['category']}")
        print(f"Current Stock: {p['stock']}")
        print(f"Reorder Level: {p['reorder_level']}")
        if p["stock"] == 0:
            print("\U0001f6d1 OUT OF STOCK! Immediate action required!")
        else:
            print(f"\U0001f6a8 BELOW REORDER LEVEL! Suggested order: {p['reorder_quantity']} units")
        print()

    print("=" * 36)
    print(f"Total items below reorder: {len(low_stock)}")
    print(f"Total out of stock: {len(out_of_stock)}")


def print_profit_analysis():
    analysis = get_profit_analysis()
    print("\n\U0001f4ca PROFIT ANALYSIS")
    print("=" * 36)
    total_inventory_value = calculate_inventory_value()
    total_sales_value = calculate_sales_value()
    total_profit = 0

    for pid, a in analysis.items():
        if a["units_sold"] == 0:
            continue
        print(f"Product: {a['name']}")
        print(f"Unit Profit: ${a['unit_profit']:.2f} ({a['margin_pct']:.1f}% margin)")
        print(f"Units Sold: {a['units_sold']}")
        print(f"Total Profit: ${a['total_profit']:,.2f}\n")
        total_profit += a["total_profit"]

    print("=" * 36)
    print(f"Total Inventory Value: ${total_inventory_value:,.2f}")
    print(f"Total Sales Value: ${total_sales_value:,.2f}")
    print(f"Total Profit: ${total_profit:,.2f}")

    by_category = get_sales_by_category()
    if total_sales_value > 0:
        print("\n\U0001f4ca CATEGORY SUMMARY:")
        for category, value in sorted(by_category.items(), key=lambda item: item[1], reverse=True):
            pct = value / total_sales_value * 100
            print(f"{category}: ${value:,.2f} ({pct:.0f}% of sales)")


def print_top_sellers(n=3):
    top = get_top_selling_products(n)
    print(f"\n\U0001f4c8 TOP SELLING PRODUCTS:")
    if not top:
        print("No sales recorded yet.")
        return
    for i, (pid, name, units) in enumerate(top, start=1):
        print(f"{i}. {name} - {units} units")


def print_menu():
    print("\n\U0001f4e6 INVENTORY MANAGEMENT SYSTEM \U0001f4e6")
    print("1. Add Product")
    print("2. Update Stock")
    print("3. Search Products")
    print("4. Low Stock Report")
    print("5. Record Sale")
    print("6. Analytics")
    print("7. Generate Reports")
    print("8. Exit")


def handle_add_product():
    name = input("Name: ").strip()
    category = input("Category: ").strip()
    try:
        price = float(input("Price: "))
        cost = float(input("Cost: "))
        stock = int(input("Initial stock: "))
        reorder_level = int(input("Reorder level: "))
    except ValueError:
        print("\u274c Price, cost, stock, and reorder level must be numbers.")
        return
    product_id = add_product(name, category, price, cost, stock, reorder_level)
    print(f"\u2705 Added '{name}' with ID {product_id}.")


def handle_update_stock():
    product_id = input("Product ID: ").strip()
    try:
        quantity = int(input("Quantity change (+ restock / - reduce): "))
    except ValueError:
        print("\u274c Quantity must be a whole number.")
        return
    print(update_stock(product_id, quantity))


def handle_search():
    query = input("Search by name, category, or ID: ").strip()
    results = search_products(query)
    if not results:
        print("No matches found.")
        return
    print(f"\n\U0001f50d {len(results)} match(es):")
    for pid, p in results.items():
        print(f"  {pid} - {p['name']} ({p['category']}) - ${p['price']:.2f} - {p['stock']} in stock")


def handle_record_sale():
    product_id = input("Product ID: ").strip()
    try:
        quantity = int(input("Quantity sold: "))
    except ValueError:
        print("\u274c Quantity must be a whole number.")
        return
    print(record_sale(product_id, quantity))


def handle_analytics_menu():
    while True:
        print("\n\U0001f4c8 ANALYTICS MENU:")
        print("1. Profit Analysis")
        print("2. Top Selling Products")
        print("3. Sales by Category")
        print("4. ABC Analysis")
        print("5. Inventory Turnover")
        print("6. Recommended Reorders")
        print("7. Back")
        choice = input("Choice: ").strip()

        if choice == "1":
            print_profit_analysis()
        elif choice == "2":
            try:
                n = int(input("How many? "))
            except ValueError:
                n = 3
            print_top_sellers(n)
        elif choice == "3":
            for category, value in get_sales_by_category().items():
                print(f"{category}: ${value:,.2f}")
        elif choice == "4":
            classification = get_abc_analysis()
            for pid, grade in classification.items():
                print(f"{pid} ({inventory['products'][pid]['name']}): Class {grade}")
        elif choice == "5":
            for pid, ratio in get_inventory_turnover().items():
                display_ratio = f"{ratio:.2f}" if ratio != float("inf") else "N/A (no stock left)"
                print(f"{pid} ({inventory['products'][pid]['name']}): {display_ratio}")
        elif choice == "6":
            recs = get_recommended_reorder()
            if not recs:
                print("No reorder recommendations right now.")
            for pid, r in recs.items():
                print(f"{r['name']} ({pid}): suggest ordering {r['suggested_quantity']} units")
        elif choice == "7":
            break
        else:
            print("\u274c Invalid choice.")
            continue


def handle_reports_menu():
    while True:
        print("\n\U0001f4cb REPORTS MENU:")
        print("1. Reorder Report")
        print("2. Sales Report (by month range)")
        print("3. Export to JSON")
        print("4. Back")
        choice = input("Choice: ").strip()

        if choice == "1":
            report = generate_reorder_report()
            if not report:
                print("Nothing needs reordering.")
            for pid, r in report.items():
                print(f"{r['name']} ({pid}): {r['current_stock']}/{r['reorder_level']} \u2192 order {r['suggested_order']}")
        elif choice == "2":
            start = input("Start month (e.g. Jan): ").strip().title()
            end = input("End month (e.g. Mar): ").strip().title()
            report = generate_sales_report(start, end)
            if report is None:
                print("\u274c Invalid month name(s).")
            elif not report:
                print("No sales in that range.")
            else:
                for pid, r in report.items():
                    print(f"{r['name']}: {r['units']} units - ${r['revenue']:,.2f}")
        elif choice == "3":
            filename = input("Filename (blank for default): ").strip() or INVENTORY_FILE
            print(export_to_json(filename))
        elif choice == "4":
            break
        else:
            print("\u274c Invalid choice.")
            continue


def main():
    load_inventory()
    while True:
        print_menu()
        choice = input("Choice: ").strip()

        if choice == "1":
            handle_add_product()
        elif choice == "2":
            handle_update_stock()
        elif choice == "3":
            handle_search()
        elif choice == "4":
            print_low_stock_report()
        elif choice == "5":
            handle_record_sale()
        elif choice == "6":
            handle_analytics_menu()
        elif choice == "7":
            handle_reports_menu()
        elif choice == "8":
            print("Goodbye! \U0001f44b")
            break
        else:
            print("\u274c Invalid choice.")
            continue


if __name__ == "__main__":
    main()