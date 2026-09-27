# 📦 Inventory Management System

## Q5 — The Inventory Management System (Hard)

Create a full inventory system using **nested data structures, comprehensions, functions, filtering, searching, and error handling**.

The system should allow users to manage products, search inventory, calculate inventory value, identify low-stock products, and optionally process purchases through a shopping cart.

---

# 📊 1. Inventory Structure

Create an inventory using categories containing lists of product dictionaries:

```python
inventory = {
    "electronics": [
        {
            "id": 1,
            "name": "Laptop",
            "price": 1200,
            "stock": 10
        },
        {
            "id": 2,
            "name": "Phone",
            "price": 800,
            "stock": 25
        },
        {
            "id": 3,
            "name": "Tablet",
            "price": 500,
            "stock": 15
        }
    ],

    "clothing": [
        {
            "id": 4,
            "name": "T-Shirt",
            "price": 25,
            "stock": 50
        },
        {
            "id": 5,
            "name": "Jeans",
            "price": 60,
            "stock": 30
        }
    ]
}
```

Each product contains:

* ID
* Name
* Price
* Stock quantity

---

# ⚙️ 2. Required Functions

Where appropriate, use **list or dictionary comprehensions** to implement these functions.

### `get_all_items()`

Return a flattened list containing every item from every category.

---

### `get_items_by_category(category)`

Return all products belonging to the specified category.

---

### `get_items_by_price_range(min_price, max_price)`

Return all products whose prices fall within the specified range.

---

### `get_low_stock_items(threshold)`

Return all products whose stock is below the given threshold.

---

### `get_total_value()`

Calculate the total value of the inventory.

For each product:

```text
value = price × stock
```

Then calculate the total value across all products.

---

### `get_category_summary()`

Return a dictionary containing each category and its total inventory value.

For example:

```python
{
    "electronics": 31500,
    "clothing": 3050
}
```

---

### `add_item(category, name, price, stock)`

Add a new product to a category.

The product should receive an automatically generated ID.

---

### `find_item_by_id(item_id)`

Search the entire inventory for a product with the specified ID.

Return the item if found.

Return `None` if it does not exist.

---

# 🖥️ 3. Main Menu

Create a menu that allows the user to:

```text
📦 INVENTORY MANAGEMENT 📦

1. View All Items
2. View by Category
3. Add Item
4. Search by Price
5. Low Stock Report
6. Total Value
7. Shopping Cart
8. Exit
```

The program should continue running until the user chooses **Exit**.

---

# 🛒 4. Super Hard Challenge — Shopping Cart

Add a shopping cart feature to the inventory system.

The user should be able to:

### Add products to the cart

The user selects a product by ID and specifies the quantity.

For example:

```text
Enter item ID: 1
Enter quantity: 3
```

The system should add the requested quantity to the cart.

### View the cart

Display:

* Product name
* Quantity
* Price
* Item subtotal
* Cart total

### Checkout

Calculate the total cost of the purchase.

When the purchase is confirmed:

* Reduce the product's stock.
* Complete the transaction.
* Clear the cart if appropriate.

### Insufficient stock

If the requested quantity is greater than the available stock, display an error instead of completing the purchase.

---

# 🖥️ Sample Output

```text
📦 INVENTORY MANAGEMENT 📦

1. View All Items
2. View by Category
3. Add Item
4. Search by Price
5. Low Stock Report
6. Total Value
7. Shopping Cart
8. Exit

Choice: 1

📋 ALL ITEMS:

Electronics:
  [1] Laptop - $1200.00 (10 in stock)
  [2] Phone - $800.00 (25 in stock)
  [3] Tablet - $500.00 (15 in stock)

Clothing:
  [4] T-Shirt - $25.00 (50 in stock)
  [5] Jeans - $60.00 (30 in stock)

Total items: 5
Total value: $36,550.00

Choice: 4

Enter min price: 50
Enter max price: 1000

💰 ITEMS IN RANGE (50-1000):

1. Phone - $800.00
2. Tablet - $500.00
3. Jeans - $60.00

Choice: 7

🛒 SHOPPING CART

1. Add item (by ID)
2. View cart
3. Checkout
4. Empty cart
5. Back

Choice: 1
Enter item ID: 1
Enter quantity: 3

✅ Added 3x Laptop to cart!

Choice: 3

📋 CHECKOUT:

1x Laptop - $1200.00 × 1 = $1200.00

Total: $1200.00

Confirm purchase? (y/n): y

✅ Purchase complete! Stock updated.
```

---

# 🧠 Concepts Tested

This project focuses on:

* Nested lists
* Nested dictionaries
* List comprehensions
* Dictionary comprehensions
* Functions
* Function parameters
* Return values
* Complex loops
* Searching and matching
* Filtering
* Error handling
* Automatic ID generation
* Inventory calculations
* Shopping cart logic
* Updating nested data structures
