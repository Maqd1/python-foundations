# 🛒 Core Project: Shopping Cart System

## The E-Commerce Cart with Promotions 🛍️

Build a full-featured shopping cart system with **product management, discounts, coupons, wishlists, checkout, multiple payment methods, recommendations, loyalty points, order history, invoices, and data persistence**.

This project simulates the logic behind an e-commerce shopping system.

---

# 📊 Data Structure

The system uses a `ShoppingCart` class together with nested dictionaries and lists to represent the cart, wishlist, order history, products, and coupons.

```python
class ShoppingCart:
    def __init__(self):
        self.cart = {}
        self.wishlist = []
        self.order_history = []
        self.loyalty_points = 0

    # Products catalog
    products = {
        "PRD001": {
            "name": "Laptop",
            "price": 1200.00,
            "category": "Electronics",
            "stock": 10,
            "weight": 2.5,
            "free_shipping": True
        }
    }

    # Coupons database
    coupons = {
        "SAVE10": {
            "type": "percentage",
            "value": 10,
            "min_order": 100
        },
        "SAVE50": {
            "type": "fixed",
            "value": 50,
            "min_order": 200
        },
        "FREESHIP": {
            "type": "shipping",
            "value": 0,
            "min_order": 50
        }
    }
```

---

# 🛒 1. Cart Operations

Implement the basic shopping cart functionality.

### `add_to_cart(product_id, quantity)`

Add a product and quantity to the cart.

### `remove_from_cart(product_id)`

Remove a product from the cart.

### `update_quantity(product_id, quantity)`

Change the quantity of an existing cart item.

### `view_cart()`

Display all items in the cart together with their prices, quantities, subtotals, and overall totals.

### `clear_cart()`

Empty the shopping cart.

---

# 🏷️ 2. Discount System — HARD

Implement different types of promotions and discounts.

### `apply_coupon(code)`

Apply a coupon after validating:

* Coupon exists
* Minimum order requirement
* Coupon type
* Other applicable conditions

### `calculate_discount(subtotal)`

Calculate the total discount applicable to the current order.

### `get_available_coupons()`

Display all currently valid coupons.

### Bulk Discount

Support promotions such as:

```text
Buy 3 → Get 10% Off
```

### Category Discount

Support category-specific promotions, such as:

```text
15% off Electronics on weekends
```

---

# 💳 3. Checkout & Payment — HARDER

Implement the complete checkout process.

### `checkout(payment_method)`

Process an order using the selected payment method.

### `calculate_total()`

Calculate the final order total:

```text
Subtotal + Tax + Shipping - Discounts
```

### `calculate_shipping()`

Calculate shipping based on:

* Product weight
* Location
* Free-shipping eligibility

### `calculate_tax()`

Calculate tax based on location.

For the Nigerian scenario, use:

```text
VAT = 7.5%
```

### Stock Validation

Before checkout:

* Confirm sufficient stock.
* Prevent purchases that exceed available stock.
* Reduce inventory after a successful purchase.

---

# ❤️ 4. User Experience — HARDEST

Implement additional shopping features.

### `add_to_wishlist(product_id)`

Save a product to the user's wishlist.

### `move_wishlist_to_cart(product_id)`

Move a wishlist item into the shopping cart.

### `get_recommendations()`

Recommend related products based on purchasing patterns.

Example:

```text
Customers who bought this also bought...
```

### `apply_loyalty_points()`

Allow customers to use accumulated loyalty points for discounts.

---

# 📦 5. Order Management — SUPER HARD

Implement order history and order management.

### `view_order_history()`

Display previous orders.

### `get_order_details(order_id)`

Display complete information about a specific order.

### `cancel_order(order_id)`

Allow an order to be cancelled within 24 hours.

### `generate_invoice(order_id)`

Generate a formatted receipt/invoice for an order.

---

# 💾 6. Data Persistence

The application must preserve its state between sessions.

Requirements:

* Save cart state to a file.
* Load cart state when the application starts.

---

# 🖥️ Sample Interface

```text
🛒 DASHMART SHOPPING CART 🛒

CURRENT CART:
====================================
Item: Laptop (PRD001)
Price: $1,200.00
Quantity: 1
Subtotal: $1,200.00

Item: Mouse (PRD002)
Price: $25.00
Quantity: 2
Subtotal: $50.00

====================================
Subtotal: $1,250.00
Shipping: $0.00 (Free shipping!)
Discount: -$125.00 (10% coupon SAVE10)
Tax: $84.38 (7.5% VAT)
TOTAL: $1,209.38
```

### Available Coupons

```text
Available coupons:

1. SAVE10 (10% off, min $100)
2. SAVE50 ($50 off, min $200)
3. FREESHIP (Free shipping, min $50)
4. ELECTRO15 (15% off electronics)
```

### Shopping Menu

```text
====================================
1. Apply Coupon
2. Add to Wishlist
3. View Wishlist
4. Proceed to Checkout
5. Continue Shopping

Choice: 4
```

---

# 💳 Checkout

```text
💳 CHECKOUT:

Payment methods:
1. Credit Card
2. PayPal
3. Bank Transfer
4. Cash on Delivery

Choice: 1
Enter card details: ****

✅ ORDER COMPLETE!

Order ID: ORD-2026-03-20-001
Total: $1,209.38
Loyalty points earned: 60
```

---

# 📝 Invoice

```text
====================================
📝 INVOICE:

DASHMART E-COMMERCE
Order #ORD-2026-03-20-001
Date: 2026-03-20 14:30

1x Laptop @ $1,200.00 = $1,200.00
2x Mouse @ $25.00 = $50.00

------------------------------------
Subtotal: $1,250.00
Discount: -$125.00 (SAVE10)
Tax: $84.38 (7.5%)

------------------------------------
TOTAL: $1,209.38

Payment: Credit Card
Status: Completed

Thank you for shopping!
====================================
```

---

# 🛍️ Recommendations

The system should be able to recommend related products.

```text
🛒 RECOMMENDATIONS:

Customers who bought Laptop also bought:

1. Laptop Bag ($45.00)
2. USB Hub ($35.00)
3. Wireless Mouse ($30.00)
```

After shopping:

```text
Continue shopping? (y/n): n

Total spent today: $1,209.38
Loyalty points: 60 (rewards earned)
```

---

# 🧠 Concepts Tested

This project tests the ability to work with:

* Classes and objects
* Dictionaries
* Complex nested structures
* Lists
* List comprehensions
* Set operations
* Recommendation logic
* Complex calculations
* Conditional logic
* File I/O
* Data persistence
* Sorting
* Searching
* Filtering
* Discounts and promotions
* Shopping cart calculations
* Inventory validation
* Order management
* Invoice generation
