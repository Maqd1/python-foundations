'''
3️⃣ 🛒 HARD SHOPPING CART SYSTEM
The E-Commerce Cart with Promotions 🛍️

Build a full-featured shopping cart with discounts, coupons, and wishlists.

Data Structure:
python

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
            "weight": 2.5,  # kg
            "free_shipping": True
        },
        # More products...
    }
    
    # Coupons database
    coupons = {
        "SAVE10": {"type": "percentage", "value": 10, "min_order": 100},
        "SAVE50": {"type": "fixed", "value": 50, "min_order": 200},
        "FREESHIP": {"type": "shipping", "value": 0, "min_order": 50}
    }

Requirements:

    Cart Operations:

        add_to_cart(product_id, quantity) → Add item to cart

        remove_from_cart(product_id) → Remove item

        update_quantity(product_id, quantity) → Change quantity

        view_cart() → Display all items with totals

        clear_cart() → Empty cart

    Discount System (HARD):

        apply_coupon(code) → Apply coupon code with validation

        calculate_discount(subtotal) → Calculate total discount

        get_available_coupons() → List all valid coupons

        Bulk discount: Buy X get Y% off (e.g., buy 3 get 10% off)

        Category discount: 15% off electronics on weekends

    Checkout with Multiple Payment Methods (HARDER):

        checkout(payment_method) → Process order

        calculate_total() → Subtotal + tax + shipping - discounts

        calculate_shipping() → Based on weight and location

        calculate_tax() → Based on location (use Nigerian VAT: 7.5%)

        Validate stock before checkout

        Reduce inventory after purchase

    User Experience (HARDEST):

        add_to_wishlist(product_id) → Save for later

        move_wishlist_to_cart(product_id) → Move to cart

        get_recommendations() → "Customers who bought this also bought..."

        apply_loyalty_points() → Use points for discounts

    Order Management (SUPER HARD):

        view_order_history() → List all past orders

        get_order_details(order_id) → Full order details

        cancel_order(order_id) → Cancel within 24 hours

        generate_invoice(order_id) → Print receipt

    Data Persistence:

        Save cart state to file

        Load on startup

Sample Output:
text

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

Available coupons:
1. SAVE10 (10% off, min $100)
2. SAVE50 ($50 off, min $200)
3. FREESHIP (Free shipping, min $50)
4. ELECTRO15 (15% off electronics)

====================================
1. Apply Coupon
2. Add to Wishlist
3. View Wishlist
4. Proceed to Checkout
5. Continue Shopping

Choice: 4

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

🛒 RECOMMENDATIONS:
Customers who bought Laptop also bought:
1. Laptop Bag ($45.00)
2. USB Hub ($35.00)
3. Wireless Mouse ($30.00)

Continue shopping? (y/n): n
Total spent today: $1,209.38
Loyalty points: 60 (rewards earned)

Concepts Tested: Dictionaries with complex nested structures, list comprehensions, set operations (for recommendations), complex calculations, conditional logic, file I/O, sorting, searching
'''

from datetime import datetime, timedelta
import json
import os
import random

# ==========================================
# PRODUCT CATALOG & COUPON DATABASE
# ==========================================

PRODUCTS = {
    "PRD001": {
        "name": "Laptop",
        "price": 1200.00,
        "category": "Electronics",
        "stock": 10,
        "weight": 2.5,
        "free_shipping": True,
    },
    "PRD002": {
        "name": "Mouse",
        "price": 25.00,
        "category": "Electronics",
        "stock": 25,
        "weight": 0.2,
        "free_shipping": False,
    },
    "PRD003": {
        "name": "Laptop Bag",
        "price": 45.00,
        "category": "Accessories",
        "stock": 15,
        "weight": 0.8,
        "free_shipping": False,
    },
    "PRD004": {
        "name": "USB Hub",
        "price": 35.00,
        "category": "Electronics",
        "stock": 20,
        "weight": 0.3,
        "free_shipping": False,
    },
    "PRD005": {
        "name": "Wireless Mouse",
        "price": 30.00,
        "category": "Electronics",
        "stock": 12,
        "weight": 0.2,
        "free_shipping": False,
    },
}

COUPONS = {
    "SAVE10": {"type": "percentage", "value": 10, "min_order": 100},
    "SAVE50": {"type": "fixed", "value": 50, "min_order": 200},
    "FREESHIP": {"type": "shipping", "value": 0, "min_order": 50},
    "ELECTRO15": {
        "type": "category",
        "category": "Electronics",
        "value": 15,
        "min_order": 100,
    },
}

# Cross-sell mapping using item co-occurrence sets
CO_PURCHASE_GRAPH = {
    "PRD001": {"PRD003", "PRD004", "PRD005"},
    "PRD002": {"PRD001", "PRD004"},
}


# ==========================================
# SHOPPING CART SYSTEM CLASS
# ==========================================

import datetime
import json
import os
import random

# ==========================================
# GLOBAL STATE & DATABASES
# ==========================================

# Application State
cart = {}  # { product_id: quantity }
wishlist = []  # [ product_id ]
order_history = []  # [ {order_dict} ]
loyalty_points = 0
active_coupon = None

PRODUCTS_FILE = "products.json"
STATE_FILE = "cart_state.json"

# Products Database
products = {
    "PRD001": {
        "name": "Laptop",
        "price": 1200.00,
        "category": "Electronics",
        "stock": 10,
        "weight": 2.5,  # kg
        "free_shipping": True,
    },
    "PRD002": {
        "name": "Mouse",
        "price": 25.00,
        "category": "Electronics",
        "stock": 25,
        "weight": 0.2,
        "free_shipping": False,
    },
    "PRD003": {
        "name": "Laptop Bag",
        "price": 45.00,
        "category": "Accessories",
        "stock": 15,
        "weight": 0.8,
        "free_shipping": False,
    },
    "PRD004": {
        "name": "USB Hub",
        "price": 35.00,
        "category": "Electronics",
        "stock": 20,
        "weight": 0.3,
        "free_shipping": False,
    },
    "PRD005": {
        "name": "Wireless Mouse",
        "price": 30.00,
        "category": "Electronics",
        "stock": 12,
        "weight": 0.2,
        "free_shipping": False,
    },
}

# Coupons Database
coupons = {
    "SAVE10": {"type": "percentage", "value": 10, "min_order": 100},
    "SAVE50": {"type": "fixed", "value": 50, "min_order": 200},
    "FREESHIP": {"type": "shipping", "value": 0, "min_order": 50},
    "ELECTRO15": {"type": "category", "category": "Electronics", "value": 15, "min_order": 100},
}


# ==========================================
# DATA PERSISTENCE (FILE I/O)
# ==========================================

def save_state():
    """Saves cart, wishlist, loyalty points, and order history to JSON file."""
    state = {
        "cart": cart,
        "wishlist": wishlist,
        "order_history": order_history,
        "loyalty_points": loyalty_points,
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)


def load_state():
    """Loads state from file on startup if available."""
    global cart, wishlist, order_history, loyalty_points
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                state = json.load(f)
                cart = state.get("cart", {})
                wishlist = state.get("wishlist", [])
                order_history = state.get("order_history", [])
                loyalty_points = state.get("loyalty_points", 0)
        except Exception:
            pass


# ==========================================
# CART OPERATIONS
# ==========================================

def add_to_cart(product_id, quantity=1):
    if product_id not in products:
        print("❌ Invalid product code.")
        return False

    current_in_cart = cart.get(product_id, 0)
    available_stock = products[product_id]["stock"]

    if current_in_cart + quantity > available_stock:
        print(f"❌ Not enough stock! Only {available_stock - current_in_cart} remaining.")
        return False

    cart[product_id] = current_in_cart + quantity
    print(f"✅ Added {quantity}x {products[product_id]['name']} to cart.")
    save_state()
    return True


def remove_from_cart(product_id):
    if product_id in cart:
        removed_item = products[product_id]["name"]
        del cart[product_id]
        print(f"🗑️ Removed {removed_item} from cart.")
        save_state()
    else:
        print("❌ Item not found in cart.")


def update_quantity(product_id, quantity):
    if product_id not in cart:
        print("❌ Item not in cart.")
        return

    if quantity <= 0:
        remove_from_cart(product_id)
        return

    if quantity > products[product_id]["stock"]:
        print(f"❌ Exceeds available stock ({products[product_id]['stock']}).")
        return

    cart[product_id] = quantity
    print(f"🔄 Updated {products[product_id]['name']} quantity to {quantity}.")
    save_state()


def clear_cart():
    global cart, active_coupon
    cart.clear()
    active_coupon = None
    save_state()


# ==========================================
# CALCULATIONS & DISCOUNTS
# ==========================================

def calculate_subtotal():
    return sum(products[pid]["price"] * qty for pid, qty in cart.items())


def calculate_discount(subtotal):
    global active_coupon
    total_discount = 0.0

    # 1. Bulk Discount: Buy 3+ total items, get 10% off subtotal
    total_items = sum(cart.values())
    if total_items >= 3:
        total_discount += subtotal * 0.10

    # 2. Category Discount: Weekend 15% off Electronics
    is_weekend = datetime.datetime.now().weekday() >= 5
    if is_weekend:
        elec_subtotal = sum(
            products[pid]["price"] * qty
            for pid, qty in cart.items()
            if products[pid]["category"] == "Electronics"
        )
        total_discount += elec_subtotal * 0.15

    # 3. Coupon Discount
    if active_coupon and active_coupon in coupons:
        c_info = coupons[active_coupon]
        if subtotal >= c_info.get("min_order", 0):
            if c_info["type"] == "percentage":
                total_discount += subtotal * (c_info["value"] / 100.0)
            elif c_info["type"] == "fixed":
                total_discount += min(c_info["value"], subtotal)
            elif c_info["type"] == "category":
                cat = c_info["category"]
                cat_subtotal = sum(
                    products[pid]["price"] * qty
                    for pid, qty in cart.items()
                    if products[pid]["category"] == cat
                )
                total_discount += cat_subtotal * (c_info["value"] / 100.0)

    return round(total_discount, 2)


def calculate_shipping():
    if not cart:
        return 0.0

    if active_coupon and coupons.get(active_coupon, {}).get("type") == "shipping":
        return 0.0

    # Check if all items have free shipping
    all_free = all(products[pid]["free_shipping"] for pid in cart)
    if all_free:
        return 0.0

    # Base weight calculation: $5 per kg for non-free items
    billable_weight = sum(
        products[pid]["weight"] * qty
        for pid, qty in cart.items()
        if not products[pid]["free_shipping"]
    )
    return round(billable_weight * 5.0, 2)


def calculate_tax(taxable_amount):
    # Nigerian VAT: 7.5%
    return round(taxable_amount * 0.075, 2)


def calculate_total():
    subtotal = calculate_subtotal()
    discount = calculate_discount(subtotal)
    discounted_subtotal = max(0.0, subtotal - discount)

    shipping = calculate_shipping()
    tax = calculate_tax(discounted_subtotal)

    total = discounted_subtotal + shipping + tax
    return {
        "subtotal": subtotal,
        "discount": discount,
        "shipping": shipping,
        "tax": tax,
        "total": round(total, 2),
    }


def apply_coupon(code):
    global active_coupon
    code = code.upper().strip()
    if code not in coupons:
        print("❌ Invalid coupon code.")
        return False

    subtotal = calculate_subtotal()
    if subtotal < coupons[code]["min_order"]:
        print(f"❌ Minimum order of ${coupons[code]['min_order']:.2f} required for this coupon.")
        return False

    active_coupon = code
    print(f"✅ Coupon '{code}' applied successfully!")
    return True


def apply_loyalty_points():
    global loyalty_points
    if loyalty_points <= 0:
        print("❌ You have no loyalty points to redeem.")
        return 0.0

    # 100 points = $10 discount
    point_discount = (loyalty_points // 100) * 10.0
    if point_discount == 0:
        print("❌ Minimum 100 points required to redeem ($10 value).")
        return 0.0

    subtotal = calculate_subtotal()
    redeemed_discount = min(point_discount, subtotal)
    used_points = int((redeemed_discount / 10.0) * 100)

    loyalty_points -= used_points
    print(f"✅ Redeemed {used_points} points for a ${redeemed_discount:.2f} discount!")
    save_state()
    return redeemed_discount


# ==========================================
# USER EXPERIENCE & RECOMMENDATIONS
# ==========================================

def add_to_wishlist(product_id):
    if product_id not in products:
        print("❌ Invalid product.")
        return
    if product_id not in wishlist:
        wishlist.append(product_id)
        print(f"⭐ Added {products[product_id]['name']} to Wishlist.")
        save_state()
    else:
        print("ℹ️ Item is already in your wishlist.")


def move_wishlist_to_cart(product_id):
    if product_id in wishlist:
        if add_to_cart(product_id, 1):
            wishlist.remove(product_id)
            save_state()
    else:
        print("❌ Item not in wishlist.")


def get_recommendations():
    """Generates recommendations based on co-occurrence in order history or category matches."""
    cart_pids = set(cart.keys())
    if not cart_pids:
        return []

    recommended = set()

    # 1. Check past orders using set intersection logic
    for order in order_history:
        order_pids = set(order["items"].keys())
        if cart_pids.intersection(order_pids):
            recommended.update(order_pids - cart_pids)

    # 2. Fallback: Suggest items from same categories
    if not recommended:
        cart_categories = {products[pid]["category"] for pid in cart_pids}
        for pid, pdata in products.items():
            if pid not in cart_pids and pdata["category"] in cart_categories:
                recommended.add(pid)

    return list(recommended)[:3]


# ==========================================
# VIEW & DISPLAY FUNCTIONS
# ==========================================

def view_cart():
    print("\n🛒 DASHMART SHOPPING CART 🛒")
    print("CURRENT CART:")
    print("====================================")

    if not cart:
        print("Your cart is empty.")
        print("====================================")
        return

    for pid, qty in cart.items():
        p = products[pid]
        sub = p["price"] * qty
        print(f"Item: {p['name']} ({pid})")
        print(f"Price: ${p['price']:,.2f}")
        print(f"Quantity: {qty}")
        print(f"Subtotal: ${sub:,.2f}\n")

    print("====================================")
    totals = calculate_total()

    print(f"Subtotal: ${totals['subtotal']:,.2f}")
    ship_str = "Free shipping!" if totals['shipping'] == 0.0 else f"${totals['shipping']:,.2f}"
    print(f"Shipping: {ship_str}")

    if totals['discount'] > 0:
        coupon_label = f" ({active_coupon})" if active_coupon else ""
        print(f"Discount: -${totals['discount']:,.2f}{coupon_label}")

    print(f"Tax: ${totals['tax']:,.2f} (7.5% VAT)")
    print(f"TOTAL: ${totals['total']:,.2f}")

    print("\nAvailable coupons:")
    for idx, (code, info) in enumerate(coupons.items(), 1):
        print(f"{idx}. {code} ({info['value']}{'%' if info['type'] in ['percentage', 'category'] else '$'} off, min ${info['min_order']})")
    print("====================================")


def view_wishlist():
    print("\n⭐ YOUR WISHLIST ⭐")
    if not wishlist:
        print("Wishlist is empty.")
        return

    for idx, pid in enumerate(wishlist, 1):
        p = products[pid]
        print(f"{idx}. {p['name']} ({pid}) - ${p['price']:,.2f}")


# ==========================================
# CHECKOUT & ORDER MANAGEMENT
# ==========================================

def checkout():
    if not cart:
        print("❌ Cart is empty! Add items before checking out.")
        return

    # Validate Stock
    for pid, qty in cart.items():
        if qty > products[pid]["stock"]:
            print(f"❌ Cannot checkout. {products[pid]['name']} exceeds available stock!")
            return

    totals = calculate_total()

    print("\n💳 CHECKOUT:")
    print("Payment methods:")
    print("1. Credit Card")
    print("2. PayPal")
    print("3. Bank Transfer")
    print("4. Cash on Delivery")

    method_choice = input("Choice: ").strip()
    methods = {"1": "Credit Card", "2": "PayPal", "3": "Bank Transfer", "4": "Cash on Delivery"}
    payment_method = methods.get(method_choice, "Credit Card")

    if method_choice == "1":
        input("Enter card details: ")

    # Process Order
    now = datetime.datetime.now()
    order_id = f"ORD-{now.strftime('%Y-%m-%d')}-{random.randint(100, 999)}"

    # Loyalty Points earned: 1 point for every $20 spent
    earned_points = int(totals["total"] // 20)
    global loyalty_points
    loyalty_points += earned_points

    # Deduct stock
    for pid, qty in cart.items():
        products[pid]["stock"] -= qty

    order_record = {
        "order_id": order_id,
        "date": now.strftime("%Y-%m-%d %H:%M"),
        "timestamp": now.timestamp(),
        "items": dict(cart),
        "totals": totals,
        "payment_method": payment_method,
        "coupon_used": active_coupon,
        "points_earned": earned_points,
        "status": "Completed",
    }

    order_history.append(order_record)

    print("\n✅ ORDER COMPLETE!")
    print(f"Order ID: {order_id}")
    print(f"Total: ${totals['total']:,.2f}")
    print(f"Loyalty points earned: {earned_points}")

    generate_invoice(order_id)
    clear_cart()

    # Show Recommendations
    recs = get_recommendations()
    if recs:
        print("\n🛒 RECOMMENDATIONS:")
        print("Customers who bought these items also bought:")
        for idx, r_pid in enumerate(recs, 1):
            rp = products[r_pid]
            print(f"{idx}. {rp['name']} (${rp['price']:,.2f})")

    print(f"\nTotal spent today: ${totals['total']:,.2f}")
    print(f"Loyalty points: {loyalty_points} (rewards earned)")


def generate_invoice(order_id):
    order = next((o for o in order_history if o["order_id"] == order_id), None)
    if not order:
        print("❌ Order not found.")
        return

    print("\n====================================")
    print("📝 INVOICE:")
    print("DASHMART E-COMMERCE")
    print(f"Order #{order['order_id']}")
    print(f"Date: {order['date']}")

    for pid, qty in order["items"].items():
        p = products[pid]
        sub = p["price"] * qty
        print(f"{qty}x {p['name']} @ ${p['price']:,.2f} = ${sub:,.2f}")

    print("------------------------------------")
    t = order["totals"]
    print(f"Subtotal: ${t['subtotal']:,.2f}")
    if t["discount"] > 0:
        c_label = f" ({order['coupon_used']})" if order["coupon_used"] else ""
        print(f"Discount: -${t['discount']:,.2f}{c_label}")
    print(f"Tax: ${t['tax']:,.2f} (7.5%)")
    print("------------------------------------")
    print(f"TOTAL: ${t['total']:,.2f}")
    print(f"Payment: {order['payment_method']}")
    print(f"Status: {order['status']}")
    print("Thank you for shopping!")
    print("====================================")


def view_order_history():
    print("\n📜 ORDER HISTORY:")
    if not order_history:
        print("No past orders found.")
        return

    for idx, order in enumerate(order_history, 1):
        print(
            f"{idx}. ID: {order['order_id']} | Date: {order['date']} | "
            f"Total: ${order['totals']['total']:,.2f} | Status: {order['status']}"
        )


def cancel_order(order_id):
    order = next((o for o in order_history if o["order_id"] == order_id), None)
    if not order:
        print("❌ Order not found.")
        return

    if order["status"] == "Cancelled":
        print("ℹ️ Order is already cancelled.")
        return

    # Check 24-hour limit (86,400 seconds)
    current_time = datetime.datetime.now().timestamp()
    if current_time - order["timestamp"] > 86400:
        print("❌ Cannot cancel order. More than 24 hours have elapsed since placement.")
        return

    # Restock inventory
    for pid, qty in order["items"].items():
        products[pid]["stock"] += qty

    order["status"] = "Cancelled"
    print(f"✅ Order {order_id} has been successfully cancelled and inventory restocked.")
    save_state()


# ==========================================
# MAIN INTERACTIVE MENU
# ==========================================

def print_menu():
    print("\n" + "=" * 40)
    print("1. View Cart & Checkout Options")
    print("2. Browse Products & Add to Cart")
    print("3. Apply Coupon")
    print("4. Redeem Loyalty Points")
    print("5. Wishlist Management")
    print("6. Order History & Invoices")
    print("7. Cancel Order")
    print("8. Exit DashMart")
    print("=" * 40)


def browse_products():
    print("\n🛍️ PRODUCT CATALOG:")
    for pid, p in products.items():
        print(f"[{pid}] {p['name']} - ${p['price']:,.2f} | Stock: {p['stock']} | Category: {p['category']}")

    pid = input("\nEnter Product ID to add (or press Enter to skip): ").strip().upper()
    if pid in products:
        qty_str = input("Enter quantity: ").strip()
        if qty_str.isdigit():
            add_to_cart(pid, int(qty_str))


def main():
    load_state()

    while True:
        view_cart()
        print_menu()
        choice = input("Choice: ").strip()

        if choice == "1":
            print("\n1. Proceed to Checkout")
            print("2. Update Quantity / Remove Item")
            print("3. Clear Cart")
            sub_c = input("Select option: ").strip()
            if sub_c == "1":
                checkout()
            elif sub_c == "2":
                pid = input("Enter Product ID: ").strip().upper()
                qty = int(input("Enter new quantity (0 to remove): ").strip())
                update_quantity(pid, qty)
            elif sub_c == "3":
                clear_cart()

        elif choice == "2":
            browse_products()

        elif choice == "3":
            code = input("Enter Coupon Code: ").strip()
            apply_coupon(code)

        elif choice == "4":
            apply_loyalty_points()

        elif choice == "5":
            view_wishlist()
            print("\n1. Add Product to Wishlist")
            print("2. Move Wishlist Item to Cart")
            w_choice = input("Choice: ").strip()
            if w_choice == "1":
                pid = input("Enter Product ID: ").strip().upper()
                add_to_wishlist(pid)
            elif w_choice == "2":
                pid = input("Enter Product ID: ").strip().upper()
                move_wishlist_to_cart(pid)

        elif choice == "6":
            view_order_history()
            oid = input("\nEnter Order ID to view invoice (or press Enter to back): ").strip()
            if oid:
                generate_invoice(oid)

        elif choice == "7":
            view_order_history()
            oid = input("Enter Order ID to cancel: ").strip()
            if oid:
                cancel_order(oid)

        elif choice == "8":
            save_state()
            print("\nThank you for shopping at DashMart! 👋")
            break
        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()