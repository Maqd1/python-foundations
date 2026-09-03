def greetings(id, name):
    return f"Welcome, {name}!\nYour ID has been verified."


def show_special_alert(birthday, restaurant_class):
    if birthday == "yes":
        birth_hurray = ("🎂 HAPPY BIRTHDAY!\nYou receive a ₦1,000 birthday discount.")
        birth_discount = 1000
    else:
        birth_hurray = ""
        birth_discount = 0

    if restaurant_class == "VIP":
        vip_hail = ("⭐ VIP CUSTOMER\nThank you for choosing our VIP service.")
    else:
        vip_hail = ""

    return birth_discount, vip_hail, birth_hurray


def choose_class(choice):
    match choice:
        case "1":
            print("\nWelcome to Normal Class.")
            print("Please follow me to your table.")
            return "Normal"
        case "2":
            print("\nWelcome to the VIP section.")
            print("Please proceed to the VIP chamber.")
            return "VIP"
        case _:
            return "Invalid choice"


def goto_normal():
    while True:
        eat = int(input("How many people are eating?\nInput a number between 1-6: "))

        if 1 <= eat <= 6:
            return eat

        print("Invalid number.")
        print("A table can have between 1 and 6 people.")


def goto_vip():
    while True:
        seat = int(input("\nHow many seats do you need?\nChoose between 2 and 6: "))

        if 2 <= seat <= 6:
            return seat

        print("Invalid number.")
        print("A VIP table can have between 2 and 6 people.")


def show_menu():
    menu = {
        "rice": 2500,
        "chicken": 4000,
        "drink": 1000,
        "dessert": 1500,
        "fish": 3500,
        "salad": 2000,
    }

    return menu


def order_food(menu):
    cart = {}
    while True:
        if len(cart) > 0:
            make_choice = input("Would you like to order another item? (yes/no): ").lower()

            if make_choice == "no":
                break

        item = input("What would you like to order: ").lower()
        # Check whether the item exists.
        if item not in menu:
            print(f"Sorry, {item} is not available.")
            print("Please choose an item from the menu.")

            continue

        quantity = int(input("How many? "))
        # Add to existing quantity if the
        # customer orders the same item again.
        if item in cart:
            cart[item] += quantity
        else:
            cart[item] = quantity

    return cart


def calculate_quantity_discount(cart, menu):
    quantity_discounts = {}

    for item, quantity in cart.items():
        price = menu[item]
        # If customer orders 5 or more
        # of the same item, give 5% discount.
        if quantity >= 5:
            normal_price = price * quantity
            discount = 0.05 * normal_price
            quantity_discounts[item] = discount

        else:
            quantity_discounts[item] = 0

    return quantity_discounts


def calculate_food_subtotal(cart, menu, quantity_discounts):
    subtotal = 0

    for item, quantity in cart.items():
        price = menu[item]
        normal_price = price * quantity
        discount = quantity_discounts[item]
        final_item_price = normal_price - discount
        subtotal += final_item_price

    return subtotal


def check_free_drink(subtotal):
    return subtotal >= 20000


def order_summary(cart, menu):
    different_items = len(cart)
    total_items = sum(cart.values())
    # Find the most expensive item.
    most_expensive_item = max(cart, key=lambda item: menu[item])

    # Find the cheapest item.
    cheapest_item = min(cart, key=lambda item: menu[item])

    print("\n")
    print("================================")
    print("         ORDER SUMMARY")
    print("================================")

    print(f"You ordered {different_items} different items.")

    print(f"Total number of items: {total_items}")

    print(f"Most expensive item ordered: {most_expensive_item.title()}")

    print(f"Cheapest item ordered: {cheapest_item.title()}")

    print("================================")


def calculate_class_charge(restaurant_class):

    class_charge = 5000

    if restaurant_class == "VIP":
        return class_charge

    return 0


def calculate_discount_system( restaurant_class, subtotal):
    # Normal:
    # 10% discount if subtotal >= ₦10,000
    if restaurant_class == "Normal" and subtotal >= 10000:
        return 0.10 * subtotal

    # VIP:
    # 5% discount if subtotal >= ₦15,000
    elif restaurant_class == "VIP" and subtotal >= 15000:
        return 0.05 * subtotal

    return 0


def calculate_id_discount(id, subtotal):
    # Even ID number → 5% discount
    if int(id[-1]) % 2 == 0:
        return 0.05 * subtotal

    return 0


def calculate_tax(amount_after_discount):
    return 0.075 * amount_after_discount


def print_receipt(customer,cart,menu,subtotal,quantity_discounts,class_charge,class_discount,birthday_discount,id_discount,tax,total,free_drink):

    print("\n")
    print("=" * 55)
    print("             MAQD RESTAURANT")
    print("                  RECEIPT")
    print("=" * 55)

    print(f"Customer: {customer['name']}")
    print(f"ID:       {customer['id']}")
    print(f"Class:    {customer['class']}")
    print(f"Seats:    {customer['seats']}")

    print("-" * 55)
    print("ORDER")
    print("-" * 55)

    for item, quantity in cart.items():

        price = menu[item]
        normal_price = price * quantity
        quantity_discount = quantity_discounts.get(item, 0)
        final_price = normal_price - quantity_discount

        print(f"{item.title():<15}x {quantity:<3}₦{final_price:>12,.2f}")

        # Show quantity discount when applicable.
        if quantity_discount > 0:
            print(f"{'  Quantity Discount':<25}-₦{quantity_discount:>11,.2f}")


    if free_drink:
        print("\n🎁 Congratulations!")
        print("You received one free drink.")

    print("-" * 55)
    print(f"{'Food Subtotal:':<32} ₦{subtotal:>12,.2f}")
    print(f"{'VIP Charge:':<32}₦{class_charge:>12,.2f}")

    if class_discount > 0:
        print(f"{'Class Discount:':<32}-₦{class_discount:>11,.2f}")

    if birthday_discount > 0:
        print(f"{'Birthday Discount:':<32}-₦{birthday_discount:>11,.2f}")

    if id_discount > 0:
        print(f"{'ID Discount:':<32}-₦{id_discount:>11,.2f}")

    print(f"{'Tax (7.5%):':<32}₦{tax:>12,.2f}")

    print("-" * 55)
    print(f"{'TOTAL:':<32}₦{total:>12,.2f}")

    print("=" * 55)
    print("        THANK YOU FOR VISITING!")
    print("=" * 55)













# ============================================
#           MAQD RESTAURANT
# ============================================

# ============================================
#           RESTAURANT PROGRAM
# ============================================

customers_served = 0
normal_customers = 0
vip_customers = 0
total_money_collected = 0

# ============================================
# EXTREME CHALLENGE:
# SERVE CUSTOMERS REPEATEDLY
# ============================================

while True:

    new_customer = input("\nNew customer? (yes/no): ").lower()
    if new_customer == "no":
        break

    # ----------------------------------------
    # CUSTOMER INFORMATION
    # ----------------------------------------
    print("\n")
    print("================================")
    print("      WELCOME TO MAQD RESTAURANT")
    print("================================")

    name = input("What is your name: ")
    id = input("What is your ID number: ")

    customer = {}
    customer["name"] = name
    customer["id"] = id

    print(greetings(id, name))

    # ----------------------------------------
    # CHOOSE CLASS
    # ----------------------------------------

    while True:

        print("\nWhich class would you like?\n1. Normal\n2. VIP")
        choice = input("Make a choice by typing 1 or 2: ")
        restaurant_class = choose_class(choice)

        if restaurant_class != "Invalid choice":
            break

        print("Invalid choice. Please try again.")

    customer["class"] = restaurant_class
    customers_served += 1

    if restaurant_class == "Normal":
        normal_customers += 1
    else:
        vip_customers += 1

    # ----------------------------------------
    # BIRTHDAY
    # ----------------------------------------

    birthday = input("Is today your birthday? (yes/no): ").lower()

    (birthday_discount,hail_message,hurray) = show_special_alert(birthday,restaurant_class)

    print(hurray)
    print(hail_message)

    # ----------------------------------------
    # SEATING
    # ----------------------------------------

    if restaurant_class == "Normal":
        seats = goto_normal()
    else:
        seats = goto_vip()

    customer["seats"] = seats

    # ----------------------------------------
    # SHOW MENU
    # ----------------------------------------

    menu = show_menu()

    print("\nThese are the available items")
    print(f"{'Item':<12} | {'Price':>10}")
    print("-" * 26)

    for key, value in menu.items():
        print(f"{key.title():<12} | ₦{value:>9,.2f}")

    # ----------------------------------------
    # ORDER FOOD
    # ----------------------------------------

    cart = order_food(menu)

    # ----------------------------------------
    # QUANTITY DISCOUNT
    # ----------------------------------------

    quantity_discounts = calculate_quantity_discount(cart,menu)

    # ----------------------------------------
    # FOOD SUBTOTAL
    # ----------------------------------------

    subtotal = calculate_food_subtotal(cart,menu,quantity_discounts)

    # ----------------------------------------
    # FREE DRINK
    # ----------------------------------------

    free_drink = check_free_drink(subtotal)

    # ----------------------------------------
    # ORDER SUMMARY
    # ----------------------------------------

    order_summary(cart,menu)

    # ----------------------------------------
    # CLASS CHARGE
    # ----------------------------------------

    class_charge = calculate_class_charge(restaurant_class)

    # ----------------------------------------
    # CLASS DISCOUNT
    # ----------------------------------------

    class_discount = calculate_discount_system(restaurant_class,subtotal)

    # ----------------------------------------
    # ID DISCOUNT
    # ----------------------------------------

    id_discount = calculate_id_discount(id,subtotal)

    # ----------------------------------------
    # TOTAL DISCOUNT
    # ----------------------------------------

    total_discount = (class_discount + birthday_discount + id_discount
    )

    # ----------------------------------------
    # AMOUNT AFTER DISCOUNT
    # ----------------------------------------

    amount_after_discount = (subtotal - total_discount)

    # ----------------------------------------
    # TAX
    # ----------------------------------------

    tax = calculate_tax(amount_after_discount)

    # ----------------------------------------
    # FINAL TOTAL
    # ----------------------------------------

    total = (amount_after_discount + class_charge + tax)

    # ----------------------------------------
    # RECEIPT
    # ----------------------------------------

    print_receipt(
        customer,
        cart,
        menu,
        subtotal,
        quantity_discounts,
        class_charge,
        class_discount,
        birthday_discount,
        id_discount,
        tax,
        total,
        free_drink
    )


    # ----------------------------------------
    # SMALL ORDER ALERT
    # ----------------------------------------

    if subtotal < 5000:
        print("\n⚠️ Small order alert:")
        print("Orders below ₦5,000 do not qualify for restaurant discounts.")

    # ----------------------------------------
    # UPDATE RESTAURANT MONEY
    # ----------------------------------------

    total_money_collected += total

# ============================================
# RESTAURANT SUMMARY
# ============================================

print("\n")

print("================================")
print("       RESTAURANT SUMMARY")
print("================================")

print(f"Customers served: {customers_served}")
print(f"Normal customers: {normal_customers}")
print(f"VIP customers:    {vip_customers}")
print(f"Total money collected: ₦{total_money_collected:,.2f}")

print("================================")
print("Thank you!")
print("================================")


'''
"""
MAQD RESTAURANT — Smart Restaurant Management System (with bonus challenges)

DESIGN DECISIONS (documented as the spec requires):

1. DISCOUNT ORDER OF OPERATIONS:
   a) Quantity Discount (Bonus 3, per-item, 5% if that item's qty >= 5) is
      applied FIRST, item by item, to produce "subtotal_after_quantity".
      Reason: it's a per-item pricing rule, conceptually part of what an
      item "costs" before any order-level or customer-level discount.
   b) Large Order Discount, VIP Discount, and Loyalty Discount (Bonus 1)
      are then each calculated independently from subtotal_after_quantity
      (NOT compounded on each other) and summed together — same approach
      as the original decision: independent, not sequential/compounding.
   c) Tax (7.5%) is calculated on the subtotal AFTER all percentage
      discounts above, but does not include the VIP service charge.
   d) Birthday Discount and Repeat Customer Discount (Bonus 2) are flat
      amounts subtracted at the very end, after tax — they're loyalty
      perks, not pricing adjustments on the food itself.

2. FREE DRINK (Bonus 4):
   Eligibility is checked against subtotal_after_quantity (the same
   number the other discounts use) BEFORE those discounts are applied,
   so a free drink can't be earned or lost because of a discount that
   comes later in the calculation. The free drink is added to the cart
   (so it shows in "order data" as the spec asks) but its cost is
   excluded from the subtotal — it's a reward, not a purchase.

3. ORDER SUMMARY (Bonus 5):
   "Most expensive" / "cheapest" item ordered is based on each item's
   MENU UNIT PRICE (not total spent), since the spec's own example
   picks Chicken (the priciest item on the menu) and Drink (the
   cheapest), not whichever item the customer happened to spend most
   on.
"""

RESTAURANT_NAME = "MAQD RESTAURANT"


def get_customer_info():
    while True:
        name = input("Enter your name: ").strip().upper()
        if not name or len(name) < 3:
            print("Invalid name. Please enter your name.")
            continue
        break

    while True:
        raw_id = input("Enter your ID number: ").strip()
        try:
            id_number = int(raw_id)
            break
        except ValueError:
            print("Invalid ID. Please enter numbers only.")

    return {"name": name, "id": id_number}


def print_welcome(customer):
    print(f"\nWelcome, {customer['name']}!\nYour ID has been verified.\n")


def choose_class():
    while True:
        choice = input("Please choose Normal or VIP: ").strip().lower()
        if choice in ("normal", "vip"):
            return choice
        print("\nInvalid choice.")


def get_seat_count(customer_class):
    if customer_class == "normal":
        print("\nWelcome to Normal Class.\nPlease follow me to your table.")
        low, high, prompt = 1, 6, "How many people are eating? "
    else:
        print("\nWelcome to the VIP section.\nPlease proceed to the VIP chamber.")
        print("You will be charged a service fee of \u20a65,000.")
        low, high, prompt = 2, 6, "How many seats do you need? "

    while True:
        raw = input(prompt).strip()
        try:
            count = int(raw)
        except ValueError:
            print(f"Invalid number.\nPlease enter a number between {low} and {high}.")
            continue
        if count < low or count > high:
            print(f"Invalid number.\nA table can have between {low} and {high} people.")
            continue
        return count


def build_menu():
    return {
        "rice": 2500,
        "chicken": 4000,
        "drink": 1000,
        "dessert": 1500,
        "fish": 3500,
        "salad": 2000,
    }


def display_menu(menu):
    print("\n===============\nMENU\n===============")
    print(f"{'Item':<12} | Price")
    print("-" * 25)
    for item, price in menu.items():
        print(f"{item.title():<12} | \u20a6{price}")


def take_order(menu):
    cart = {}
    while True:
        item = input("\nWhat would you like to order? ").strip().lower()
        if item not in menu:
            print(f"Sorry, {item} is not available. Please choose an item from the menu.")
            continue

        while True:
            raw_qty = input("How many? ").strip()
            try:
                qty = int(raw_qty)
            except ValueError:
                print("Please enter a valid whole number.")
                continue
            if qty <= 0:
                print("Quantity must be at least 1.")
                continue
            break

        cart[item] = cart.get(item, 0) + qty
        print(f"{item.title()} x{qty} = \u20a6{menu[item] * qty}")

        again = input("Would you like to order another item? (yes/no) ").strip().lower()
        if again != "yes":
            break

    return cart


def print_order_summary(cart, menu):
    """Bonus 5 — summary derived from cart/menu data, not typed manually."""
    num_different = len(cart)
    total_items = sum(cart.values())
    most_expensive = max(cart, key=lambda item: menu[item])
    cheapest = min(cart, key=lambda item: menu[item])

    print(f"\nYou ordered {num_different} different items.")
    print(f"Total number of items: {total_items}")
    print(f"Most expensive item ordered: {most_expensive.title()}")
    print(f"Cheapest item ordered: {cheapest.title()}")


def calculate_costs(cart, menu):
    """Returns (raw_subtotal, quantity_discount_total, subtotal_after_quantity)."""
    raw_subtotal = 0
    quantity_discount_total = 0
    for item, qty in cart.items():
        item_cost = menu[item] * qty
        raw_subtotal += item_cost
        if qty >= 5:  # Bonus 3 — quantity discount
            quantity_discount_total += 0.05 * item_cost
    subtotal_after_quantity = raw_subtotal - quantity_discount_total
    return raw_subtotal, quantity_discount_total, subtotal_after_quantity


def service_charge(customer_class):
    return 5000 if customer_class == "vip" else 0


def large_order_discount(subtotal):
    return 0.10 * subtotal if subtotal >= 10000 else 0


def vip_discount(customer_class, subtotal):
    if customer_class == "vip" and subtotal >= 15000:
        return 0.05 * subtotal
    return 0


def loyalty_discount(customer_id, subtotal):
    """Bonus 1 — 5% off if the customer's ID ends in an even digit."""
    if customer_id % 2 == 0:
        return 0.05 * subtotal
    return 0


def small_order_alert(raw_subtotal):
    if raw_subtotal < 5000:
        return "\u26a0\ufe0f Orders below \u20a65,000 do not qualify for restaurant discounts."
    return ""


def birthday_discount():
    answer = input("\nIs today your birthday? (yes/no) ").strip().lower()
    if answer == "yes":
        print("\U0001f382 HAPPY BIRTHDAY! You receive a \u20a61,000 birthday discount.")
        return 1000
    return 0


def repeat_customer_discount():
    """Bonus 2 — flat ₦500 off for returning customers."""
    answer = input("Are you a returning customer? (yes/no) ").strip().lower()
    if answer == "yes":
        print("Thank you for being a returning customer! You receive a \u20a6500 discount.")
        return 500
    return 0


def check_free_drink(cart, menu, subtotal_after_quantity):
    """Bonus 4 — free drink if food subtotal (post quantity discount) >= ₦20,000."""
    if subtotal_after_quantity >= 20000:
        cart["drink"] = cart.get("drink", 0) + 1
        print("\n\U0001f381 Congratulations! You receive one free drink.")
        return True
    return False


def calculate_tax(amount_after_discount):
    return 0.075 * amount_after_discount


def print_receipt(customer, customer_class, seats, cart, menu, bill, free_drink_awarded):
    print(f"\n{'=' * 40}")
    print(f"{RESTAURANT_NAME:^40}")
    print(f"{'RECEIPT':^40}")
    print("=" * 40)
    print(f"Customer: {customer['name']}")
    print(f"ID:       {customer['id']}")
    print(f"Class:    {customer_class.title()}")
    print(f"Seats:    {seats}")

    print("\n" + "-" * 40)
    print("ORDER")
    print("-" * 40)
    for item, qty in cart.items():
        if item == "drink" and free_drink_awarded:
            paid_qty = qty - 1
            cost = paid_qty * menu[item]
            note = " (1 FREE)"
        else:
            cost = qty * menu[item]
            note = ""
        print(f"{item.title():<12} x{qty:<3}{note:<10} \u20a6{cost}")

    print("-" * 40)
    print(f"Food Subtotal:        \u20a6{bill['raw_subtotal']:.2f}")
    if bill["quantity_discount"]:
        print(f"Quantity Discount:    -\u20a6{bill['quantity_discount']:.2f}")
    if bill["vip_charge"]:
        print(f"VIP Charge:           \u20a6{bill['vip_charge']:.2f}")
    if bill["large_discount"]:
        print(f"Large Order Discount: -\u20a6{bill['large_discount']:.2f}")
    if bill["vip_discount"]:
        print(f"VIP Discount:         -\u20a6{bill['vip_discount']:.2f}")
    if bill["loyalty_discount"]:
        print(f"Loyalty Discount:     -\u20a6{bill['loyalty_discount']:.2f}")

    alert = small_order_alert(bill["raw_subtotal"])
    if alert:
        print(alert)

    print(f"Tax:                  \u20a6{bill['tax']:.2f}")
    if bill["birthday_discount"]:
        print(f"Birthday Discount:    -\u20a6{bill['birthday_discount']:.2f}")
    if bill["repeat_discount"]:
        print(f"Repeat Customer:      -\u20a6{bill['repeat_discount']:.2f}")

    print("-" * 40)
    print(f"TOTAL:                \u20a6{bill['total']:.2f}")
    print("=" * 40)
    print(f"{'THANK YOU FOR VISITING!':^40}")
    print("=" * 40)


def run_customer_session():
    """Runs one full customer visit and returns their class + total paid."""
    print("\nPlease scan your ID card.")
    customer = get_customer_info()
    print_welcome(customer)

    customer_class = choose_class()
    if customer_class == "vip":
        print("\n\u2b50 VIP CUSTOMER\nThank you for choosing our VIP service.")

    seats = get_seat_count(customer_class)

    menu = build_menu()
    display_menu(menu)

    cart = take_order(menu)
    print_order_summary(cart, menu)  # Bonus 5

    raw_subtotal, quantity_discount_total, subtotal_after_quantity = calculate_costs(cart, menu)

    free_drink_awarded = check_free_drink(cart, menu, subtotal_after_quantity)  # Bonus 4

    vip_charge = service_charge(customer_class)
    discount_large = large_order_discount(subtotal_after_quantity)
    discount_vip = vip_discount(customer_class, subtotal_after_quantity)
    discount_loyalty = loyalty_discount(customer["id"], subtotal_after_quantity)  # Bonus 1

    amount_after_percent_discounts = (
        subtotal_after_quantity - discount_large - discount_vip - discount_loyalty
    )
    tax_amount = calculate_tax(amount_after_percent_discounts)

    bday_discount = birthday_discount()
    repeat_discount = repeat_customer_discount()  # Bonus 2

    total = (
        amount_after_percent_discounts
        + vip_charge
        + tax_amount
        - bday_discount
        - repeat_discount
    )

    bill = {
        "raw_subtotal": raw_subtotal,
        "quantity_discount": quantity_discount_total,
        "vip_charge": vip_charge,
        "large_discount": discount_large,
        "vip_discount": discount_vip,
        "loyalty_discount": discount_loyalty,
        "tax": tax_amount,
        "birthday_discount": bday_discount,
        "repeat_discount": repeat_discount,
        "total": total,
    }

    print_receipt(customer, customer_class, seats, cart, menu, bill, free_drink_awarded)

    return {"class": customer_class, "total": total}


def main():
    print(f"{'=' * 32}\n{RESTAURANT_NAME:^32}\n{'=' * 32}")

    customers_served = 0
    normal_count = 0
    vip_count = 0
    total_collected = 0

    while True:
        result = run_customer_session()
        customers_served += 1
        if result["class"] == "normal":
            normal_count += 1
        else:
            vip_count += 1
        total_collected += result["total"]

        again = input("\nNew customer? (yes/no) ").strip().lower()
        if again != "yes":
            break

    print(f"\n{'=' * 32}\nRESTAURANT SUMMARY\n{'=' * 32}")
    print(f"Customers served: {customers_served}")
    print(f"Normal customers: {normal_count}")
    print(f"VIP customers:    {vip_count}")
    print(f"Total money collected: \u20a6{total_collected:.2f}")
    print("Thank you!")


if __name__ == "__main__":
    main()
'''