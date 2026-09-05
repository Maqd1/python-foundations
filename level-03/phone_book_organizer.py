'''
🟡 Mid Level (2 Questions)
Q3: The Phone Book Organizer (Mid)

Create a phone book system using nested dictionaries.

Requirements:

    Create a phone book structure:
    python

    phone_book = {
        "Damilola": {
            "mobile": "080-1234-5678",
            "work": "01-2345-6789",
            "email": "dami@email.com"
        },
        # Add 3-4 more contacts
    }

    Implement these functions:

        add_contact(name, phone, email) → Adds new contact

        find_contact(name) → Returns contact info or "Not found"

        list_contacts() → Prints all contacts alphabetically

        delete_contact(name) → Removes contact

    Main menu:
    text

    1. Add Contact
    2. Find Contact
    3. List All Contacts
    4. Delete Contact
    5. Exit

    Extra challenge: Allow multiple phone numbers (mobile, work, home)

    Harder: Save contacts to a file and load on start

Sample Output:
text

📱 PHONE BOOK 📱
1. Add Contact
2. Find Contact
3. List All Contacts
4. Delete Contact
5. Exit
Choice: 2
Enter name: Damilola

📞 Contact found:
Name: Damilola
Mobile: 080-1234-5678
Work: 01-2345-6789
Email: dami@email.com

Choice: 3
📇 All Contacts:
1. Alice - 080-1111-1111
2. Bob - 080-2222-2222
3. Damilola - 080-1234-5678

Concepts: Nested dictionaries, functions, while loops, conditional logic, string formatting
'''

import json
import os

CONTACTS_FILE = "contacts.json"

# Starter contacts — pre-populated so the book isn't empty on first run
phone_book = {
    "Damilola": {"mobile": "080-1234-5678", "work": "01-2345-6789", "email": "dami@email.com"},
    "Alice": {"mobile": "080-1111-1111", "email": "alice@email.com"},
    "Bob": {"mobile": "080-2222-2222", "work": "01-9876-5432", "home": "01-5555-0000", "email": "bob@email.com"},
    "Zainab": {"mobile": "080-3333-3333", "email": "zainab@email.com"},
}


def load_contacts():
    """Loads contacts.json if it exists, otherwise keeps the starter contacts above."""
    global phone_book
    if os.path.exists(CONTACTS_FILE):
        try:
            with open(CONTACTS_FILE, "r") as f:
                phone_book = json.load(f)
        except (json.JSONDecodeError, OSError):
            print("\u26a0\ufe0f  Could not read contacts.json — starting with default contacts.")


def save_contacts():
    with open(CONTACTS_FILE, "w") as f:
        json.dump(phone_book, f, indent=2)


def add_contact(name, phone, email, work=None, home=None):
    """Adds a new contact. 'phone' is stored as the mobile number.
    work/home are optional, satisfying the 'multiple numbers' extra challenge."""
    entry = {"mobile": phone, "email": email}
    if work:
        entry["work"] = work
    if home:
        entry["home"] = home

    phone_book[name] = entry
    save_contacts()
    return f"\u2705 Contact '{name}' added."


def find_contact(name):
    """Case-insensitive lookup. Returns the contact dict, or None if not found."""
    for stored_name, info in phone_book.items():
        if stored_name.lower() == name.lower():
            return stored_name, info
    return None


def list_contacts():
    if not phone_book:
        print("\nNo contacts saved yet.")
        return

    print("\n\U0001f4c7 All Contacts:")
    for i, name in enumerate(sorted(phone_book.keys(), key=str.lower), start=1):
        mobile = phone_book[name].get("mobile", "N/A")
        print(f"{i}. {name} - {mobile}")


def delete_contact(name):
    match = find_contact(name)
    if match is None:
        return "\u274c Not found."

    stored_name, _ = match
    del phone_book[stored_name]
    save_contacts()
    return f"\U0001f5d1\ufe0f  Contact '{stored_name}' deleted."


def print_contact_details(stored_name, info):
    print("\n\U0001f4de Contact found:")
    print(f"Name: {stored_name}")
    if "mobile" in info:
        print(f"Mobile: {info['mobile']}")
    if "work" in info:
        print(f"Work: {info['work']}")
    if "home" in info:
        print(f"Home: {info['home']}")
    if "email" in info:
        print(f"Email: {info['email']}")


def print_menu():
    print("\n\U0001f4f1 PHONE BOOK \U0001f4f1")
    print("1. Add Contact")
    print("2. Find Contact")
    print("3. List All Contacts")
    print("4. Delete Contact")
    print("5. Exit")


def handle_add():
    name = input("Enter name: ").strip()
    if not name:
        print("\u274c Name cannot be empty.")
        return
    if find_contact(name):
        print(f"\u26a0\ufe0f  '{name}' already exists. Use a different name or delete the old entry first.")
        return

    mobile = input("Enter mobile number: ").strip()
    email = input("Enter email: ").strip()

    add_work = input("Add a work number too? (y/n): ").strip().lower()
    work = input("Enter work number: ").strip() if add_work == "y" else None

    add_home = input("Add a home number too? (y/n): ").strip().lower()
    home = input("Enter home number: ").strip() if add_home == "y" else None

    print(add_contact(name, mobile, email, work=work, home=home))


def handle_find():
    name = input("Enter name: ").strip()
    match = find_contact(name)
    if match is None:
        print("\u274c Not found.")
        return
    stored_name, info = match
    print_contact_details(stored_name, info)


def handle_delete():
    name = input("Enter name: ").strip()
    print(delete_contact(name))


def main():
    load_contacts()

    while True:
        print_menu()
        choice = input("Choice: ").strip()

        match choice:
            case "1":
                handle_add()
            case "2":
                handle_find()
            case "3":
                list_contacts()
            case "4":
                handle_delete()
            case "5":
                print("Goodbye! \U0001f44b")
                break
            case _:
                print("Invalid choice! Try again.")
                continue


if __name__ == "__main__":
    main()