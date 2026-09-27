
inventory = {
    "electronics": [
        {"id": 1, "name": "Laptop", "price": 1200, "stock": 10},
        {"id": 2, "name": "Phone", "price": 800, "stock": 25},
        {"id": 3, "name": "Tablet", "price": 500, "stock": 15},
    ],
    "clothing": [
        {"id": 4, "name": "T-Shirt", "price": 25, "stock": 50},
        {"id": 5, "name": "Jeans", "price": 60, "stock": 30},
    ],
}

cart = {}  # item_id -> quantity reserved


def get_all_items():
    return [item for items in inventory.values() for item in items]


def get_items_by_category(category):
    return inventory.get(category.lower(), [])


def get_items_by_price_range(min_price, max_price):
    return [item for item in get_all_items() if min_price <= item["price"] <= max_price]


def get_low_stock_items(threshold):
    return [item for item in get_all_items() if item["stock"] < threshold]


def get_total_value():
    return sum(item["price"] * item["stock"] for item in get_all_items())


def get_category_summary():
    return {
        category: sum(item["price"] * item["stock"] for item in items)
        for category, items in inventory.items()
    }


def add_item(category, name, price, stock):
    new_id = max((item["id"] for item in get_all_items()), default=0) + 1
    new_item = {"id": new_id, "name": name, "price": price, "stock": stock}
    inventory.setdefault(category.lower(), []).append(new_item)
    return new_item


def find_item_by_id(item_id):
    return next((item for item in get_all_items() if item["id"] == item_id), None)


# --- SHOPPING CART ---

def add_to_cart(item_id, quantity):
    item = find_item_by_id(item_id)
    if item is None:
        return f"\u274c Item ID {item_id} not found."
    if quantity <= 0:
        return "\u274c Quantity must be positive."

    already_reserved = cart.get(item_id, 0)
    if already_reserved + quantity > item["stock"]:
        available = item["stock"] - already_reserved
        return f"\u274c Not enough stock. Only {available} more {item['name']} available."

    cart[item_id] = already_reserved + quantity
    return f"\u2705 Added {quantity}x {item['name']} to cart!"


def view_cart():
    if not cart:
        print("\n\U0001f6d2 Cart is empty.")
        return

    print("\n\U0001f6d2 YOUR CART:")
    total = 0
    for item_id, qty in cart.items():
        item = find_item_by_id(item_id)
        if item is None:
            continue
        line_total = item["price"] * qty
        total += line_total
        print(f"{qty}x {item['name']} - ${item['price']:.2f} \u00d7 {qty} = ${line_total:.2f}")
    print(f"Total: ${total:.2f}")


def checkout():
    if not cart:
        print("\n\U0001f6d2 Cart is empty. Nothing to checkout.")
        return

    print("\n\U0001f4cb CHECKOUT:")
    total = 0
    line_items = []
    for item_id, qty in cart.items():
        item = find_item_by_id(item_id)
        if item is None:
            continue
        # Re-check stock at checkout time in case it changed since the item was added to cart
        if qty > item["stock"]:
            print(f"\u274c Not enough stock for {item['name']} \u2014 only {item['stock']} left. Checkout cancelled.")
            return
        line_total = item["price"] * qty
        total += line_total
        line_items.append((item, qty))
        print(f"{qty}x {item['name']} - ${item['price']:.2f} \u00d7 {qty} = ${line_total:.2f}")

    print(f"Total: ${total:.2f}")
    confirm = input("Confirm purchase? (y/n): ").strip().lower()
    if confirm != "y":
        print("Purchase cancelled.")
        return

    for item, qty in line_items:
        item["stock"] -= qty
    cart.clear()
    print("\u2705 Purchase complete! Stock updated.")


def empty_cart():
    cart.clear()
    print("\U0001f6d2 Cart emptied.")


# --- DISPLAY / MENU HANDLERS ---

def print_all_items():
    print("\n\U0001f4cb ALL ITEMS:")
    for category, items in inventory.items():
        print(f"{category.title()}:")
        for item in items:
            print(f"  [{item['id']}] {item['name']} - ${item['price']:.2f} ({item['stock']} in stock)")

    print(f"\nTotal items: {len(get_all_items())}")
    print(f"Total value: ${get_total_value():,.2f}")


def print_by_category():
    category = input("Enter category: ").strip().lower()
    items = get_items_by_category(category)
    if not items:
        print(f"\u274c No items found in category '{category}'.")
        return

    print(f"\n\U0001f4cb {category.title()} ITEMS:")
    for item in items:
        print(f"  [{item['id']}] {item['name']} - ${item['price']:.2f} ({item['stock']} in stock)")


def handle_add_item():
    category = input("Enter category: ").strip().lower()
    name = input("Enter item name: ").strip()
    if not name:
        print("\u274c Item name cannot be empty.")
        return

    try:
        price = float(input("Enter price: "))
        stock = int(input("Enter stock: "))
    except ValueError:
        print("\u274c Price and stock must be numbers.")
        return

    if price < 0 or stock < 0:
        print("\u274c Price and stock cannot be negative.")
        return

    new_item = add_item(category, name, price, stock)
    print(f"\u2705 Added '{new_item['name']}' with ID {new_item['id']} to '{category}'.")


def handle_price_search():
    try:
        min_price = float(input("Enter min price: "))
        max_price = float(input("Enter max price: "))
    except ValueError:
        print("\u274c Please enter valid numbers.")
        return

    if min_price > max_price:
        print("\u274c Min price cannot be greater than max price.")
        return

    items = get_items_by_price_range(min_price, max_price)
    print(f"\n\U0001f4b0 ITEMS IN RANGE (${min_price:.0f}-${max_price:.0f}):")
    if not items:
        print("No items in this range.")
        return
    for i, item in enumerate(items, start=1):
        print(f"{i}. {item['name']} - ${item['price']:.2f}")


def handle_low_stock():
    try:
        threshold = int(input("Enter stock threshold: "))
    except ValueError:
        print("\u274c Please enter a valid number.")
        return

    items = get_low_stock_items(threshold)
    print(f"\n\u26a0\ufe0f  LOW STOCK ITEMS (below {threshold}):")
    if not items:
        print("No items are low on stock.")
        return
    for item in items:
        print(f"[{item['id']}] {item['name']} - {item['stock']} in stock")


def handle_total_value():
    print(f"\n\U0001f4b5 Total inventory value: ${get_total_value():,.2f}")
    print("\nBy category:")
    for category, value in get_category_summary().items():
        print(f"  {category.title()}: ${value:,.2f}")


def shopping_cart_menu():
    while True:
        print("\n\U0001f6d2 SHOPPING CART")
        print("1. Add item (by ID)")
        print("2. View cart")
        print("3. Checkout")
        print("4. Empty cart")
        print("5. Back")
        choice = input("Choice: ").strip()

        match choice:
            case "1":
                try:
                    item_id = int(input("Enter item ID: "))
                    quantity = int(input("Enter quantity: "))
                except ValueError:
                    print("\u274c ID and quantity must be whole numbers.")
                    continue
                print(add_to_cart(item_id, quantity))
            case "2":
                view_cart()
            case "3":
                checkout()
            case "4":
                empty_cart()
            case "5":
                break
            case _:
                print("\u274c Invalid choice.")
                continue


def print_menu():
    print("\n\U0001f4e6 INVENTORY MANAGEMENT \U0001f4e6")
    print("1. View All Items")
    print("2. View by Category")
    print("3. Add Item")
    print("4. Search by Price")
    print("5. Low Stock Report")
    print("6. Total Value")
    print("7. Shopping Cart")
    print("8. Exit")


def main():
    while True:
        print_menu()
        choice = input("Choice: ").strip()

        match choice:
            case "1":
                print_all_items()
            case "2":
                print_by_category()
            case "3":
                handle_add_item()
            case "4":
                handle_price_search()
            case "5":
                handle_low_stock()
            case "6":
                handle_total_value()
            case "7":
                shopping_cart_menu()
            case "8":
                print("Goodbye! \U0001f44b")
                break
            case _:
                print("\u274c Invalid choice.")
                continue


if __name__ == "__main__":
    main()