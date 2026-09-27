# 📱 Phone Book Organizer

## Q3 — The Phone Book Organizer (Mid)

Create a phone book system using **nested dictionaries**.

The program should allow users to add, find, list, and delete contacts through a menu-driven interface.

---

# 📞 1. Phone Book Structure

Create a phone book using a nested dictionary:

```python
phone_book = {
    "Damilola": {
        "mobile": "080-1234-5678",
        "work": "01-2345-6789",
        "email": "dami@email.com"
    },

    # Add 3–4 more contacts
}
```

Each person's name is the main dictionary key.

The value is another dictionary containing their contact information.

---

# ⚙️ 2. Required Functions

Implement the following functions.

### `add_contact(name, phone, email)`

Add a new contact to the phone book.

The contact should contain the person's:

* Name
* Phone number
* Email address

---

### `find_contact(name)`

Search for a contact by name.

If the contact exists, return or display their information.

If the contact does not exist, return:

```text
Not found
```

---

### `list_contacts()`

Display all contacts alphabetically.

Each contact should show relevant information such as their name and phone number.

---

### `delete_contact(name)`

Remove a contact from the phone book.

The program should handle the case where the requested contact does not exist.

---

# 🖥️ 3. Main Menu

Create a menu that repeatedly gives the user these options:

```text
📱 PHONE BOOK 📱

1. Add Contact
2. Find Contact
3. List All Contacts
4. Delete Contact
5. Exit
```

The program should continue displaying the menu until the user chooses **Exit**.

---

# ⭐ 4. Extra Challenge — Multiple Phone Numbers

Allow contacts to have multiple types of phone numbers.

For example:

```python
{
    "mobile": "080-1234-5678",
    "work": "01-2345-6789",
    "home": "080-9876-5432",
    "email": "dami@email.com"
}
```

Possible phone types include:

* Mobile
* Work
* Home

---

# 💾 5. Harder Challenge — File Persistence

Save contacts to a file so that the phone book is not lost when the program closes.

The program should:

1. Load saved contacts when it starts.
2. Allow the user to modify the phone book.
3. Save the updated contacts when changes are made or when the program exits.

---

# 🖥️ Sample Output

```text
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
```

---

# 🧠 Concepts Tested

This exercise focuses on:

* Nested dictionaries
* Dictionary access
* Functions
* Function parameters
* Return values
* `while` loops
* Conditional logic
* String formatting
* Alphabetical sorting
* Menu-driven programs
* File persistence
