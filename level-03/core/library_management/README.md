# 📚 Library Management System

## The Complete Library System with Checkouts 📖

Build a full library management system with **book management, members, borrowing, returns, fines, analytics, and recommendations**.

This project combines complex nested dictionaries, lists, relationships between records, date handling, searching, filtering, sorting, statistical analysis, and data aggregation.

---

## 📊 Data Structure

The main `library` structure contains books, members, transactions, and the fine rate.

```python
library = {
    "books": {
        "ISBN001": {
            "title": "Python Programming",
            "author": "John Smith",
            "genre": "Technology",
            "year": 2025,
            "publisher": "TechBooks",
            "copies": {
                "total": 5,
                "available": 3,
                "borrowed": 2
            },
            "locations": [
                "Aisle 2, Shelf 3",
                "Aisle 2, Shelf 4"
            ],
            "tags": [
                "python",
                "programming",
                "beginner"
            ],
            "rating": 4.5,
            "reviews": [
                {
                    "user": "user1",
                    "rating": 5,
                    "comment": "Great book!"
                }
            ]
        }
    },

    "members": {
        "MEM001": {
            "name": "Damilola Ogunleye",
            "email": "dami@email.com",
            "phone": "080-1234-5678",
            "joined": "2025-01-15",
            "borrowed": [
                {
                    "isbn": "ISBN001",
                    "borrowed": "2026-03-01",
                    "due": "2026-03-15",
                    "returned": None
                }
            ],
            "fines": 0.00,
            "active": True,
            "preferences": [
                "Technology",
                "Fiction"
            ],
            "reading_history": []
        }
    },

    "transactions": [
        {
            "id": "TRN001",
            "member_id": "MEM001",
            "isbn": "ISBN001",
            "action": "borrow",
            "date": "2026-03-01",
            "due_date": "2026-03-15"
        }
    ],

    "fines": 0.50
}
```

The `fines` value represents the **fine charged per day for an overdue book**.

---

# 📚 1. Book Management

### `add_book(title, author, genre, copies, publisher)`

Add a new book to the library.

### `search_books(query)`

Search books by:

* Title
* Author
* Genre
* ISBN
* Tag

### `get_book_details(isbn)`

Display the complete information for a specific book.

### `update_copies(isbn, change)`

Add or remove copies of an existing book.

### `get_available_books()`

Return books that currently have available copies.

### `get_books_by_genre(genre)`

Return all books belonging to a specific genre.

---

# 👥 2. Member Management

### `register_member(name, email, phone)`

Register a new library member.

### `get_member_details(member_id)`

Display complete information about a member.

### `update_member(member_id, **kwargs)`

Update a member's information.

### `deactivate_member(member_id)`

Suspend or deactivate a member's account.

### `get_member_history(member_id)`

Display the member's complete borrowing history.

---

# 📖 3. Borrowing System — HARD

### `borrow_book(member_id, isbn)`

Check out a book to a member.

The system should check relevant conditions such as:

* Whether the member exists
* Whether the member is active
* Whether the book exists
* Whether a copy is available
* Whether the member has reached the borrowing limit

### `return_book(member_id, isbn)`

Return a borrowed book and update the relevant records.

### `renew_book(member_id, isbn)`

Extend the due date.

A book can only be renewed **once**.

### `reserve_book(member_id, isbn)`

Allow a member to place a hold on a book.

### `check_availability(isbn)`

Check the current availability of a book.

---

# 💸 4. Fine System — HARDER

### `calculate_fines(member_id)`

Calculate fines resulting from overdue books.

The system uses:

```text
₦0.50 per day overdue
```

### `pay_fines(member_id, amount)`

Process payment toward a member's outstanding fines.

### `get_overdue_books()`

Return all currently overdue books.

### `send_overdue_notices()`

Simulate sending overdue notices to members.

---

# 📊 5. Analytics and Reports — HARDEST

### `get_popular_books(n)`

Return the top `n` most borrowed books.

### `get_active_members()`

Find members who currently have active borrowed books.

### `get_genre_popularity()`

Calculate which genres are most popular.

### `get_borrowing_trends()`

Analyse borrowing activity over time.

### `get_member_statistics()`

Generate statistics such as:

* Active vs inactive members
* Average number of borrows per member
* Total members
* Borrowing activity

---

# 🤖 6. Advanced Features — VERY HARD

### `get_recommendations(member_id)`

Recommend books to a member based on their reading history and preferences.

### `get_most_reviewed_books()`

Find books with the highest number of reviews.

### `get_author_ranking()`

Rank authors according to borrowing activity.

### `generate_library_report()`

Generate a complete library statistics report.

The report should combine information from books, members, borrowing activity, genres, fines, and other library data.

---

# 🖥️ Sample Output

```text
📚 PYTHON LIBRARY SYSTEM 📚

1. Book Management
2. Member Management
3. Borrow/Return
4. Fines
5. Reports & Analytics
6. Search
7. Recommendations
8. Exit

Choice: 3

📖 BORROW/RETURN MENU
1. Borrow Book
2. Return Book
3. Renew Book
4. View My Borrowings
5. Check Availability

Choice: 1
Enter Member ID: MEM001
Enter ISBN: ISBN001

✅ Book borrowed successfully!
Member: Damilola Ogunleye
Book: Python Programming
Due Date: 2026-07-15 (14 days)
Total books borrowed: 1/5 allowed

====================================
Choice: 2 (Return Book)
Enter Member ID: MEM001
Enter ISBN: ISBN001

⚠️ This book is 3 days overdue!
Fine: ₦1.50 (₦0.50 per day)

Return book and pay fine? (y/n): y
✅ Book returned!
Fine paid: ₦1.50
New balance: ₦0.00

====================================
Choice: 5

📊 LIBRARY REPORT
====================================
Total Books: 1,250
Available: 875 (70%)
Borrowed: 375 (30%)

📈 POPULAR BOOKS (Top 5):
1. Python Programming (45 borrows)
2. Data Science 101 (38 borrows)
3. Web Development (32 borrows)
4. Machine Learning (28 borrows)
5. AI Fundamentals (25 borrows)

👥 MEMBER STATISTICS:
Total Members: 325
Active: 280 (86%)
Inactive: 45 (14%)
Average Borrows/Member: 4.2

🏷️ GENRE POPULARITY:
1. Technology (40%)
2. Fiction (25%)
3. Science (15%)
4. History (10%)
5. Business (10%)

💸 FINES COLLECTED (This Month):
Total: ₦12,450.00
Average fine per member: ₦38.30

====================================
Choice: 7
Enter Member ID: MEM001

📚 RECOMMENDATIONS FOR Damilola Ogunleye
Based on your reading history:
1. Advanced Python (You liked Python Programming)
2. Django Web Framework (Based on genre: Technology)
3. Algorithms Unlocked (Recommended for programmers)

Members who borrowed Python Programming also borrowed:
1. Data Science 101 (85%)
2. Web Development (72%)
3. Machine Learning (65%)
```

---

# 🧠 Concepts Tested

This project tests advanced use of Python data structures and algorithms, including:

* Complex nested dictionaries
* Multiple relationships between data
* Lists inside dictionaries
* Dictionaries inside lists
* List comprehensions
* List comprehensions with multiple conditions
* Custom sorting with `key=`
* Statistical analysis
* Date handling
* Searching algorithms
* Filtering
* Data aggregation
* Recommendation algorithms
* Borrowing and transaction tracking
* Fine calculations
* Report generation

---

# 🎯 Main Goal

The goal is to build a complete library system where different pieces of information are connected.

For example:

```text
Member
   │
   ├── borrows ──────► Book
   │                     │
   │                     ├── Author
   │                     ├── Genre
   │                     ├── Copies
   │                     └── Reviews
   │
   ├── fines
   │
   └── reading history
```

The challenge is not just storing the data. The challenge is **using relationships between the data to perform real operations and produce useful information**.
