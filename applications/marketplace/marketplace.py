from datetime import date, timedelta
from pathlib import Path

import random
import re
import string


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# ============================================================
# STAGE 3 — MARKETPLACE DATE
# ============================================================

def check_3day_range():

    start_date_input = input(
        "Enter marketplace start date (YYYY-MM-DD): "
    ).strip()

    try:
        start_date = date.fromisoformat(start_date_input)

    except ValueError:
        print("Invalid format. Please use YYYY-MM-DD.")
        return None, False

    day1 = start_date
    day2 = start_date + timedelta(days=1)
    day3 = start_date + timedelta(days=2)

    today = date.today()

    print(f"\nMarketplace opening period: {day1} to {day3}")
    print(f"Today is: {today}")

    if today == day1:
        print("Today is Day 1.")
        return start_date_input, True

    elif today == day2:
        print("Today is Day 2.")
        return start_date_input, True

    elif today == day3:
        print("Today is Day 3.")
        return start_date_input, True

    else:
        return start_date_input, False


def market_status(start_date_input, run):

    if run:

        print(
            f"\n{'=' * 30}\n"
            "MARKETPLACE IS OPEN\n"
            f"{'=' * 30}\n\n"
            "Welcome!\n"
            "You may continue shopping.\n"
        )

    else:

        print(
            f"\n{'=' * 30}\n"
            "MARKETPLACE CLOSED\n"
            f"{'=' * 30}\n\n"
            "The marketplace is currently closed.\n"
            f"Please come back during the opening period "
            f"starting {start_date_input}.\n"
        )


# ============================================================
# ONBOARDING PAGE
# ============================================================

def show_onboarding_page(name):

    print(
        f"\n{'=' * 40}\n"
        f"        {name} MARKETPLACE\n"
        f"{'=' * 40}\n"
        "1. Sign Up\n"
        "2. Login\n"
        "3. Exit\n"
    )


# ============================================================
# STAGE 1 — VALIDATION
# ============================================================

def valid_username(username):

    if username == "":
        print("Username must not be empty.")
        return False

    return True


def valid_email(email):

    # Example:
    # maqd@gmail.com     -> valid
    # maqd.com           -> invalid
    # maqd@              -> invalid

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not re.match(pattern, email):

        print("Invalid email.")
        return False

    return True


# ============================================================
# FILE CHECKING
# ============================================================

def username_exists(username):

    try:

        with open("passwords.txt", "r") as file:

            for line in file:

                line_words = [
                    word.strip()
                    for word in line.split(",")
                ]

                if len(line_words) < 3:
                    continue

                saved_username = line_words[0]

                if username == saved_username:
                    return True

    except FileNotFoundError:

        return False

    return False


def email_exists(email):

    try:

        with open("passwords.txt", "r") as file:

            for line in file:

                line_words = [
                    word.strip()
                    for word in line.split(",")
                ]

                if len(line_words) < 3:
                    continue

                saved_email = line_words[1]

                if email == saved_email:
                    return True

    except FileNotFoundError:

        return False

    return False


# ============================================================
# PASSWORD GENERATION
# ============================================================

def generate_password():

    upper_rand = random.choices(
        string.ascii_uppercase,
        k=2
    )

    lower_rand = random.choices(
        string.ascii_lowercase,
        k=4
    )


    digit_rand = random.choices(
        string.digits,
        k=4
    )

    specials_rand = random.choices(
        "!@#$%^&_",
        k=3
    )

    password_list = (
        upper_rand
        + lower_rand
        + digit_rand
        + specials_rand
    )

    # Mix the characters so they don't always
    # appear in the same order.

    random.shuffle(password_list)

    return "".join(password_list)


# ============================================================
# SAVE USER
# ============================================================

def save_user(username, email):

    with open("users.txt", "a") as file:

        file.write(
            f"{username},{email}\n"
        )


def save_password(username, email, password):

    with open("passwords.txt", "a") as file:

        file.write(
            f"{username},{email},{password}\n"
        )


# ============================================================
# ACCOUNT CREATED
# ============================================================

def account_generated(username, email, password):

    print(
        f"\n{'=' * 30}\n"
        "ACCOUNT CREATED\n"
        f"{'=' * 30}\n\n"
        f"Username: {username}\n"
        f"Email: {email}\n\n"
        "Your generated password is:\n"
        f"{password}\n"
    )


# ============================================================
# SIGN UP
# ============================================================

def sign_up():

    print(
        f"\n{'=' * 30}\n"
        "SIGN UP\n"
        f"{'=' * 30}\n"
    )

    # --------------------------------------------------------
    # USERNAME
    # --------------------------------------------------------

    while True:

        username = input(
            "Enter your username: "
        ).strip()

        if not valid_username(username):
            continue

        if username_exists(username):

            print(
                "That username already exists. "
                "Please choose another."
            )

            continue

        break

    # --------------------------------------------------------
    # EMAIL
    # --------------------------------------------------------

    while True:

        email = input(
            "Enter your email: "
        ).strip()

        if not valid_email(email):
            continue

        if email_exists(email):

            print(
                "That email already exists. "
                "Please use another email."
            )

            continue

        break

    # --------------------------------------------------------
    # GENERATE PASSWORD
    # --------------------------------------------------------

    password = generate_password()

    # --------------------------------------------------------
    # SAVE ACCOUNT
    # --------------------------------------------------------

    save_user(
        username,
        email
    )

    save_password(
        username,
        email,
        password
    )

    # --------------------------------------------------------
    # SHOW GENERATED ACCOUNT DETAILS
    # --------------------------------------------------------

    account_generated(
        username,
        email,
        password
    )

    return username, email, password


# ============================================================
# LOCKED ACCOUNTS
# ============================================================

def is_locked(username):

    try:

        with open("locked_accounts.txt","r") as file:

            for line in file:

                saved_username = line.strip()

                if saved_username == username:
                    return True

    except FileNotFoundError:

        return False

    return False


def lock_account(username):

    # Prevent the same username from being
    # added repeatedly.

    if not is_locked(username):

        with open("locked_accounts.txt","a") as file:

            file.write(
                f"{username}\n"
            )

    # Keep a separate restriction log.

    with open("restricted.txt","a") as file:

        file.write(
            f"{username} is restricted\n"
        )


# ============================================================
# LOGIN AUTHENTICATION
# ============================================================

def confirm_login_details(
    username,
    email,
    password
):

    try:

        with open("passwords.txt", "r") as file:

            for line in file:

                line_words = [
                    word.strip()
                    for word in line.split(",")
                ]

                if len(line_words) < 3:
                    continue

                saved_username = line_words[0]
                saved_email = line_words[1]
                saved_password = line_words[2]

                # ------------------------------------------------
                # FIRST CHECK USERNAME
                # ------------------------------------------------

                if username == saved_username:

                    if email != saved_email:

                        return (
                            "Username and email "
                            "do not match."
                        )

                    if password != saved_password:

                        return "Incorrect password."

                    return "Login successful."

    except FileNotFoundError:

        return (
            "No user accounts have "
            "been created yet."
        )

    return "Username not found."


# ============================================================
# LOGIN
# ============================================================

def login():

    print(
        f"\n{'=' * 30}\n"
        "LOGIN\n"
        f"{'=' * 30}\n"
    )

    username = input(
        "Enter your username: "
    ).strip()

    email = input(
        "Enter your email: "
    ).strip()

    # --------------------------------------------------------
    # CHECK WHETHER ACCOUNT IS LOCKED
    # --------------------------------------------------------

    if is_locked(username):

        print(
            "\nYour account is locked.\n"
            "Please contact support."
        )

        return False

    # --------------------------------------------------------
    # THREE PASSWORD ATTEMPTS
    # --------------------------------------------------------

    attempts_left = 3

    while attempts_left > 0:

        password = input(
            "Enter password: "
        )

        result = confirm_login_details(
            username,
            email,
            password
        )

        print(result)

        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        if result == "Login successful.":

            print(
                f"\nWelcome, {username}!"
            )

            return username

        # ----------------------------------------------------
        # USERNAME / EMAIL PROBLEM
        # ----------------------------------------------------

        if result == "Username not found.":

            return False

        if result == "Username and email do not match.":

            return False

        # ----------------------------------------------------
        # WRONG PASSWORD
        # ----------------------------------------------------

        if result == "Incorrect password.":

            attempts_left -= 1

            if attempts_left > 0:

                print(
                    f"Wrong password.\n"
                    f"Attempts remaining: "
                    f"{attempts_left}"
                )

            else:

                print(
                    "\nYour account has been locked.\n"
                    "Please try again later."
                )

                lock_account(username)

                return False

    return False


# ============================================================
# STAGE 4 — ANIMALS
# ============================================================


def read_animals():

    animals = []

    try:

        with open(
            DATA_DIR / "animals.txt",
            "r"
        ) as file:

            for line in file:

                # Remove whitespace and split
                # the line using commas.

                animal = [
                    item.strip()
                    for item in line.split(",")
                ]

                # Expected format:
                #
                # type,name,price,stock,category
                #
                # Therefore we need 5 values.

                if len(animal) < 5:
                    continue

                animals.append(animal)

    except FileNotFoundError:

        print(
            "\nanimals.txt does not exist."
        )

    return animals


# ------------------------------------------------------------
# DISPLAY ANIMALS
# ------------------------------------------------------------

def view_animals():

    animals = read_animals()

    if not animals:

        print(
            "\nNo animals are available."
        )

        return

    print(
        f"\n{'=' * 60}\n"
        "                 AVAILABLE ANIMALS\n"
        f"{'=' * 60}"
    )

    for number, animal in enumerate(
        animals,
        start=1
    ):

        animal_type = animal[0]
        name = animal[1]
        price = animal[2]
        stock = animal[3]
        category = animal[4]

        print(
            f"\n{number}. {name}"
            f"\n   Type: {animal_type}"
            f"\n   Price: ₦{price}"
            f"\n   Stock: {stock}"
            f"\n   Category: {category}"
        )


# ------------------------------------------------------------
# CHOOSE ANIMAL
# ------------------------------------------------------------

def choose_animal():

    animals = read_animals()

    if not animals:

        print(
            "\nNo animals are available."
        )

        return None

    print(
        f"\n{'=' * 50}\n"
        "                 CHOOSE ANIMAL\n"
        f"{'=' * 50}"
    )

    for number, animal in enumerate(
        animals,
        start=1
    ):

        print(
            f"{number}. "
            f"{animal[1]} - "
            f"₦{animal[2]} "
            f"(Stock: {animal[3]})"
        )

    while True:

        choice = input(
            "\nChoose an animal: "
        ).strip()

        if not choice.isdigit():

            print(
                "Please enter a number."
            )

            continue

        choice = int(choice)

        if choice < 1 or choice > len(animals):

            print(
                "Invalid animal choice."
            )

            continue

        # Lists start from index 0.
        #
        # Therefore:
        #
        # choice 1 -> animals[0]
        # choice 2 -> animals[1]
        #
        return animals[choice - 1]


# ============================================================
# STAGE 5 — CLOTHING
# ============================================================


def read_clothes():

    clothes = []

    try:

        with open(
            DATA_DIR / "clothes.txt",
            "r"
        ) as file:

            for line in file:

                # Expected:
                #
                # category,gender,age,type,price,stock

                clothing = [
                    item.strip()
                    for item in line.split(",")
                ]

                if len(clothing) < 6:
                    continue

                clothes.append(clothing)

    except FileNotFoundError:

        print(
            "\nclothes.txt does not exist."
        )

    return clothes


# ------------------------------------------------------------
# DISPLAY ALL CLOTHES
# ------------------------------------------------------------

def view_clothes():

    clothes = read_clothes()

    if not clothes:

        print(
            "\nNo clothing products are available."
        )

        return

    print(
        f"\n{'=' * 60}\n"
        "                 AVAILABLE CLOTHES\n"
        f"{'=' * 60}"
    )

    for number, clothing in enumerate(
        clothes,
        start=1
    ):

        category = clothing[0]
        gender = clothing[1]
        age = clothing[2]
        clothing_type = clothing[3]
        price = clothing[4]
        stock = clothing[5]

        print(
            f"\n{number}. {clothing_type}"
            f"\n   Category: {category}"
            f"\n   Gender: {gender}"
            f"\n   Age: {age}"
            f"\n   Price: ₦{price}"
            f"\n   Stock: {stock}"
        )


# ------------------------------------------------------------
# CHOOSE GENDER
# ------------------------------------------------------------

def choose_gender():

    print(
        f"\n{'=' * 40}\n"
        "             CLOTHING SECTION\n"
        f"{'=' * 40}\n"
        "1. Men\n"
        "2. Women\n"
        "3. Children\n"
        "4. Back\n"
    )

    while True:

        choice = input(
            "Choose an option: "
        ).strip()

        if choice == "1":

            return "Men"

        elif choice == "2":

            return "Women"

        elif choice == "3":

            return "Children"

        elif choice == "4":

            return None

        else:

            print(
                "Invalid choice."
            )


# ------------------------------------------------------------
# GET CLOTHES BY GENDER
# ------------------------------------------------------------

def get_clothes_by_gender(gender):

    clothes = read_clothes()

    filtered_clothes = []

    for clothing in clothes:

        # clothing[1] is the gender field.

        if clothing[1].lower() == gender.lower():

            filtered_clothes.append(
                clothing
            )

    return filtered_clothes


# ------------------------------------------------------------
# CHOOSE CLOTHING
# ------------------------------------------------------------

def choose_clothing(gender):

    clothes = get_clothes_by_gender(
        gender
    )

    if not clothes:

        print(
            f"\nNo clothing available "
            f"for {gender}."
        )

        return None

    print(
        f"\n{'=' * 50}\n"
        f"             {gender.upper()} CLOTHES\n"
        f"{'=' * 50}"
    )

    for number, clothing in enumerate(
        clothes,
        start=1
    ):

        print(
            f"{number}. "
            f"{clothing[3]} - "
            f"₦{clothing[4]} "
            f"(Stock: {clothing[5]})"
        )

    while True:

        choice = input(
            "\nChoose clothing: "
        ).strip()

        if not choice.isdigit():

            print(
                "Please enter a number."
            )

            continue

        choice = int(choice)

        if choice < 1 or choice > len(clothes):

            print(
                "Invalid clothing choice."
            )

            continue

        return clothes[choice - 1]


# ============================================================
# QUANTITY
# ============================================================
# This function is shared by BOTH:
#
# Stage 4 — Animals
# Stage 5 — Clothes
#
# That means we don't need two separate
# choose_quantity() functions.
# ============================================================

def choose_quantity(stock):

    stock = int(stock)

    while True:

        quantity = input(
            f"Enter quantity "
            f"(Available: {stock}): "
        ).strip()

        if not quantity.isdigit():

            print(
                "Please enter a valid number."
            )

            continue

        quantity = int(quantity)

        if quantity <= 0:

            print(
                "Quantity must be greater than 0."
            )

            continue

        if quantity > stock:

            print(
                f"Not enough stock. "
                f"Only {stock} available."
            )

            continue

        return quantity


# ============================================================
# CART
# ============================================================
# The cart is a Python list.
#
# Example:
#
# cart = []
#
# After buying an animal:
#
# cart = [
#     {
#         "name": "White Ram",
#         "price": 150000,
#         "quantity": 2
#     }
# ]
#
# We will use this cart for both animals
# and clothes.
# ============================================================

def add_to_cart(cart, name, price, quantity):

    item = {
        "name": name,
        "price": float(price),
        "quantity": quantity
    }

    cart.append(item)

    print(
        f"\n{quantity} x {name} "
        "has been added to your cart."
    )


# ============================================================
# VIEW CART
# ============================================================

def view_cart(cart):

    if not cart:

        print(
            "\nYour cart is empty."
        )

        return 0

    print(
        f"\n{'=' * 60}\n"
        "                    YOUR CART\n"
        f"{'=' * 60}"
    )

    total = 0

    for number, item in enumerate(
        cart,
        start=1
    ):

        name = item["name"]
        price = item["price"]
        quantity = item["quantity"]

        subtotal = price * quantity

        total += subtotal

        print(
            f"\n{number}. {name}"
            f"\n   Price: ₦{price:,.2f}"
            f"\n   Quantity: {quantity}"
            f"\n   Subtotal: ₦{subtotal:,.2f}"
        )

    print(
        f"\n{'-' * 60}\n"
        f"TOTAL: ₦{total:,.2f}"
    )

    return total


# ============================================================
# PAYMENT
# ============================================================
# IMPORTANT:
#
# This is where card details belong.
#
# NOT in sign_up()
#
# The user has already created an account and
# selected products before reaching this function.
# ============================================================

def payment(username, total):

    print(
        f"\n{'=' * 50}\n"
        "                    PAYMENT\n"
        f"{'=' * 50}\n"
        f"Amount to pay: ₦{total:,.2f}\n"
    )

    card_number = input(
        "Enter card number: "
    ).strip()

    expiry = input(
        "Enter card expiry (MM/YY): "
    ).strip()

    cvv = input(
        "Enter CVV: "
    ).strip()

    # For the assignment, we save the payment
    # information separately.
    #
    # In a real application, NEVER store CVV
    # in plain text like this.

    with open(
        "payments.txt",
        "a"
    ) as file:

        file.write(
            f"{username},{card_number},"
            f"{expiry},{cvv},{total}\n"
        )

    print(
        "\nPayment successful!"
    )

    print(
        f"Thank you, {username}."
    )


# ============================================================
# CHECKOUT
# ============================================================

def checkout(username, cart):

    if not cart:

        print(
            "\nYour cart is empty."
        )

        return False

    total = view_cart(cart)

    while True:

        choice = input(
            "\nProceed to payment? (yes/no): "
        ).strip().lower()

        if choice == "yes":

            payment(
                username,
                total
            )

            return True

        elif choice == "no":

            print(
                "Returning to marketplace."
            )

            return False

        else:

            print(
                "Please enter yes or no."
            )


# ============================================================
# MARKETPLACE MENU
# ============================================================
# This is where Stages 4 and 5 are connected
# to the successful login.
# ============================================================

def marketplace_menu(username):

    # The cart belongs to this shopping session.

    cart = []

    while True:

        print(
            f"\n{'=' * 45}\n"
            "                MARKETPLACE\n"
            f"{'=' * 45}\n"
            f"Welcome, {username}!\n\n"
            "1. Animals\n"
            "2. Clothes\n"
            "3. View Cart\n"
            "4. Checkout\n"
            "5. Logout\n"
        )

        choice = input(
            "Choose an option: "
        ).strip()

        # ====================================================
        # STAGE 4 — ANIMALS
        # ====================================================

        if choice == "1":

            animal = choose_animal()

            if animal:

                # animal[3] is the stock.

                quantity = choose_quantity(
                    animal[3]
                )

                # animal[1] is the animal name.
                # animal[2] is the price.

                add_to_cart(
                    cart,
                    animal[1],
                    animal[2],
                    quantity
                )

        # ====================================================
        # STAGE 5 — CLOTHES
        # ====================================================

        elif choice == "2":

            gender = choose_gender()

            if gender:

                clothing = choose_clothing(
                    gender
                )

                if clothing:

                    # clothing[5] is the stock.

                    quantity = choose_quantity(
                        clothing[5]
                    )

                    # clothing[3] is the clothing type.
                    # clothing[4] is the price.

                    add_to_cart(
                        cart,
                        clothing[3],
                        clothing[4],
                        quantity
                    )

        # ====================================================
        # VIEW CART
        # ====================================================

        elif choice == "3":

            view_cart(cart)

        # ====================================================
        # CHECKOUT
        # ====================================================

        elif choice == "4":

            checkout(
                username,
                cart
            )

        # ====================================================
        # LOGOUT
        # ====================================================

        elif choice == "5":

            print(
                "\nLogging out..."
            )

            return

        else:

            print(
                "\nInvalid choice."
            )
















# ============================================================
# MAIN PROGRAM
# ============================================================

start_date_input, run = check_3day_range()

market_status(
    start_date_input,
    run
)


if run:

    while True:

        # ----------------------------------------------------
        # MARKETPLACE NAME
        # ----------------------------------------------------

        name = input(
            "\nWhat name would you like "
            "the marketplace to be? "
        ).strip().upper()

        # ----------------------------------------------------
        # SHOW ONBOARDING PAGE
        # ----------------------------------------------------

        show_onboarding_page(name)

        onboard_choice = input(
            "Choose an option: "
        ).strip()

        # ====================================================
        # SIGN UP
        # ====================================================

        if onboard_choice == "1":

            username, email, password = sign_up()

            print(
                "\nYour account has been created."
            )

            # ------------------------------------------------
            # AUTOMATIC LOGIN AFTER SIGN UP
            # ------------------------------------------------

            print(
                "\nLogging you in..."
            )

            logged_in = confirm_login_details(
                username,
                email,
                password
            )

            if logged_in == "Login successful.":

                print(
                    f"\nWelcome, {username}!"
                )

                # ------------------------------------------------
                # ENTER THE ACTUAL MARKETPLACE
                # ------------------------------------------------

                marketplace_menu(
                    username
                )

                # After logout, return to onboarding.

            else:

                print(
                    "\nAutomatic login failed."
                )

        # ====================================================
        # LOGIN
        # ====================================================

        elif onboard_choice == "2":

            logged_in = login()

            if logged_in:

                # ------------------------------------------------
                # SUCCESSFUL LOGIN
                # ------------------------------------------------

                # Enter Stages 4 and 5.

                marketplace_menu(
                    logged_in
                )

        # ====================================================
        # EXIT
        # ====================================================

        elif onboard_choice == "3":

            print(
                "Goodbye!"
            )

            break

        # ====================================================
        # INVALID OPTION
        # ====================================================

        else:

            print(
                "\nInvalid choice.\n"
                "Enter 1 for Sign Up, "
                "2 for Login, "
                "or 3 to Exit."
            )

else:

    print(
        "\nToday is NOT within the "
        "3-day marketplace range."
    )
