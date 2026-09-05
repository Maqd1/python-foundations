'''
5️⃣ 📚 HARD LIBRARY MANAGEMENT SYSTEM
The Complete Library System with Checkouts 📖

Build a full library management system with borrowing, returns, and fines.

Data Structure:
python

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
            "locations": ["Aisle 2, Shelf 3", "Aisle 2, Shelf 4"],
            "tags": ["python", "programming", "beginner"],
            "rating": 4.5,
            "reviews": [
                {"user": "user1", "rating": 5, "comment": "Great book!"}
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
            "preferences": ["Technology", "Fiction"],
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
    "fines": 0.50  # Per day overdue
}

Requirements:

    Book Management:

        add_book(title, author, genre, copies, publisher) → Add new book

        search_books(query) → Search by title, author, genre, ISBN, tag

        get_book_details(isbn) → Show full book info

        update_copies(isbn, change) → Add/remove copies

        get_available_books() → Books with copies available

        get_books_by_genre(genre) → All books in genre

    Member Management:

        register_member(name, email, phone) → Add new member

        get_member_details(member_id) → Show member info

        update_member(member_id, **kwargs) → Update info

        deactivate_member(member_id) → Suspend account

        get_member_history(member_id) → Complete borrowing history

    Borrowing System (HARD):

        borrow_book(member_id, isbn) → Check out book

        return_book(member_id, isbn) → Return book

        renew_book(member_id, isbn) → Extend due date (once allowed)

        reserve_book(member_id, isbn) → Place hold on book

        check_availability(isbn) → Check current availability

    Fine System (HARDER):

        calculate_fines(member_id) → Calculate overdue fines

        pay_fines(member_id, amount) → Process payment

        get_overdue_books() → All overdue books

        send_overdue_notices() → Simulate sending emails

    Analytics and Reports (HARDEST):

        get_popular_books(n) → Top n most borrowed books

        get_active_members() → Members with active borrows

        get_genre_popularity() → Most popular genres

        get_borrowing_trends() → Borrowing over time

        get_member_statistics() → Active vs inactive, average borrows

    Advanced Features (VERY HARD):

        get_recommendations(member_id) → Based on reading history

        get_most_reviewed_books() → Books with most reviews

        get_author_ranking() → Most borrowed authors

        generate_library_report() → Full library statistics

Sample Output:
text

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

Concepts Tested: Complex nested dictionaries with multiple relationships, list comprehensions with multiple conditions, sorting with custom keys, statistical analysis, date handling, search algorithms, recommendation algorithms, complex filtering, data aggregation
'''


from datetime import datetime, timedelta
import math

# ==========================================
# GLOBAL STATE & DATA STRUCTURE
# ==========================================

library = {
    "books": {
        "ISBN001": {
            "title": "Python Programming",
            "author": "John Smith",
            "genre": "Technology",
            "year": 2025,
            "publisher": "TechBooks",
            "copies": {"total": 5, "available": 3, "borrowed": 2},
            "locations": ["Aisle 2, Shelf 3", "Aisle 2, Shelf 4"],
            "tags": ["python", "programming", "beginner"],
            "rating": 4.5,
            "reviews": [
                {"user": "user1", "rating": 5, "comment": "Great book!"}
            ],
            "borrow_count": 45,
            "holds": [],  # List of member_ids
        },
        "ISBN002": {
            "title": "Data Science 101",
            "author": "Jane Doe",
            "genre": "Technology",
            "year": 2024,
            "publisher": "DataPress",
            "copies": {"total": 4, "available": 2, "borrowed": 2},
            "locations": ["Aisle 2, Shelf 5"],
            "tags": ["data", "science", "python"],
            "rating": 4.8,
            "reviews": [],
            "borrow_count": 38,
            "holds": [],
        },
        "ISBN003": {
            "title": "Web Development",
            "author": "John Smith",
            "genre": "Technology",
            "year": 2023,
            "publisher": "TechBooks",
            "copies": {"total": 3, "available": 3, "borrowed": 0},
            "locations": ["Aisle 2, Shelf 1"],
            "tags": ["web", "html", "javascript"],
            "rating": 4.2,
            "reviews": [],
            "borrow_count": 32,
            "holds": [],
        },
        "ISBN004": {
            "title": "African History & Culture",
            "author": "Chinua Achebe",
            "genre": "History",
            "year": 2020,
            "publisher": "Heritage Books",
            "copies": {"total": 2, "available": 2, "borrowed": 0},
            "locations": ["Aisle 5, Shelf 2"],
            "tags": ["history", "africa", "culture"],
            "rating": 4.9,
            "reviews": [],
            "borrow_count": 12,
            "holds": [],
        },
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
                    "returned": None,
                    "renewed": False,
                }
            ],
            "fines": 0.00,
            "active": True,
            "preferences": ["Technology", "Fiction"],
            "reading_history": ["ISBN001", "ISBN002"],
        }
    },
    "transactions": [
        {
            "id": "TRN001",
            "member_id": "MEM001",
            "isbn": "ISBN001",
            "action": "borrow",
            "date": "2026-03-01",
            "due_date": "2026-03-15",
        }
    ],
    "fines_rate": 0.50,  # Fines per day overdue in ₦
    "next_isbn_id": 5,
    "next_member_id": 2,
    "next_transaction_id": 2,
    "fines_collected_month": 12450.00,
}

# ==========================================
# 1. BOOK MANAGEMENT
# ==========================================


def add_book(
    title,
    author,
    genre,
    total_copies,
    publisher,
    year=2026,
    tags=None,
    locations=None,
):
    """Adds a new book record to the library catalog."""
    isbn = f"ISBN{library['next_isbn_id']:03d}"
    library["next_isbn_id"] += 1

    library["books"][isbn] = {
        "title": title,
        "author": author,
        "genre": genre,
        "year": year,
        "publisher": publisher,
        "copies": {
            "total": total_copies,
            "available": total_copies,
            "borrowed": 0,
        },
        "locations": locations or ["General Shelf"],
        "tags": tags or [],
        "rating": 0.0,
        "reviews": [],
        "borrow_count": 0,
        "holds": [],
    }
    return isbn


def search_books(query):
    """Searches catalog by title, author, genre, ISBN, or tags."""
    q = query.lower()
    results = {}
    for isbn, b in library["books"].items():
        if (
            q in isbn.lower()
            or q in b["title"].lower()
            or q in b["author"].lower()
            or q in b["genre"].lower()
            or any(q in tag.lower() for tag in b["tags"])
        ):
            results[isbn] = b
    return results


def get_book_details(isbn):
    """Retrieves record details for a target ISBN."""
    return library["books"].get(isbn)


def update_copies(isbn, change):
    """Increases or decreases total/available stock for a book."""
    book = library["books"].get(isbn)
    if not book:
        return False
    new_total = book["copies"]["total"] + change
    new_avail = book["copies"]["available"] + change
    if new_total < book["copies"]["borrowed"] or new_avail < 0:
        return False
    book["copies"]["total"] = new_total
    book["copies"]["available"] = new_avail
    return True


def get_available_books():
    """Returns dictionary of books that currently have stock on hand."""
    return {
        isbn: b
        for isbn, b in library["books"].items()
        if b["copies"]["available"] > 0
    }


def get_books_by_genre(genre):
    """Filters library catalog by genre."""
    return {
        isbn: b
        for isbn, b in library["books"].items()
        if b["genre"].lower() == genre.lower()
    }


# ==========================================
# 2. MEMBER MANAGEMENT
# ==========================================


def register_member(name, email, phone, preferences=None):
    """Registers a new library member."""
    mem_id = f"MEM{library['next_member_id']:03d}"
    library["next_member_id"] += 1

    library["members"][mem_id] = {
        "name": name,
        "email": email,
        "phone": phone,
        "joined": datetime.now().strftime("%Y-%m-%d"),
        "borrowed": [],
        "fines": 0.00,
        "active": True,
        "preferences": preferences or [],
        "reading_history": [],
    }
    return mem_id


def get_member_details(member_id):
    """Retrieves account record for a member."""
    return library["members"].get(member_id)


def update_member(member_id, **kwargs):
    """Updates demographic or preference fields for a member."""
    member = library["members"].get(member_id)
    if not member:
        return False
    for key, val in kwargs.items():
        if key in member and val is not None:
            member[key] = val
    return True


def deactivate_member(member_id):
    """Suspends account activity for a member."""
    member = library["members"].get(member_id)
    if member:
        member["active"] = False
        return True
    return False


def get_member_history(member_id):
    """Retrieves complete borrowing history across active and returned records."""
    member = library["members"].get(member_id)
    return member["borrowed"] if member else []


# ==========================================
# 3. BORROWING SYSTEM
# ==========================================


def check_availability(isbn):
    """Checks stock counts and hold lists for a book."""
    book = library["books"].get(isbn)
    if not book:
        return None
    return {
        "title": book["title"],
        "available": book["copies"]["available"],
        "total": book["copies"]["total"],
        "holds_count": len(book["holds"]),
    }


def record_transaction(member_id, isbn, action, due_date=None):
    """Logs system activity transactions."""
    t_id = f"TRN{library['next_transaction_id']:03d}"
    library["next_transaction_id"] += 1
    library["transactions"].append(
        {
            "id": t_id,
            "member_id": member_id,
            "isbn": isbn,
            "action": action,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "due_date": due_date,
        }
    )


def borrow_book(member_id, isbn):
    """Executes checkout logic for a member and book."""
    member = library["members"].get(member_id)
    book = library["books"].get(isbn)

    if not member or not book:
        return False, "Member or Book not found."
    if not member["active"]:
        return False, "Member account is suspended."
    if member["fines"] > 0:
        return False, f"Unpaid fines balance: ₦{member['fines']:.2f}."

    active_borrows = [b for b in member["borrowed"] if b["returned"] is None]
    if len(active_borrows) >= 5:
        return False, "Borrowing limit reached (max 5 books)."

    if book["copies"]["available"] <= 0:
        return False, "No copies available. Consider placing a hold."

    # Process checkout
    book["copies"]["available"] -= 1
    book["copies"]["borrowed"] += 1
    book["borrow_count"] += 1

    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=14)

    borrow_record = {
        "isbn": isbn,
        "borrowed": borrow_date.strftime("%Y-%m-%d"),
        "due": due_date.strftime("%Y-%m-%d"),
        "returned": None,
        "renewed": False,
    }

    member["borrowed"].append(borrow_record)
    if isbn not in member["reading_history"]:
        member["reading_history"].append(isbn)

    record_transaction(
        member_id, isbn, "borrow", due_date.strftime("%Y-%m-%d")
    )
    return True, f"Successfully borrowed! Due date: {due_date.strftime('%Y-%m-%d')}"


def return_book(member_id, isbn):
    """Executes return operations and calculates overdue penalties."""
    member = library["members"].get(member_id)
    book = library["books"].get(isbn)

    if not member or not book:
        return False, "Member or Book not found.", 0.0

    borrow_record = None
    for rec in member["borrowed"]:
        if rec["isbn"] == isbn and rec["returned"] is None:
            borrow_record = rec
            break

    if not borrow_record:
        return False, "Active borrow record not found.", 0.0

    today_str = datetime.now().strftime("%Y-%m-%d")
    borrow_record["returned"] = today_str

    # Inventory adjustments
    book["copies"]["available"] += 1
    book["copies"]["borrowed"] -= 1

    # Overdue fine calculation
    due_date = datetime.strptime(borrow_record["due"], "%Y-%m-%d")
    today_date = datetime.strptime(today_str, "%Y-%m-%d")
    days_overdue = (today_date - due_date).days

    fine_amount = 0.0
    if days_overdue > 0:
        fine_amount = days_overdue * library["fines_rate"]
        member["fines"] += fine_amount

    record_transaction(member_id, isbn, "return")
    return True, f"Book returned. Days overdue: {max(0, days_overdue)}", fine_amount


def renew_book(member_id, isbn):
    """Extends due date by 14 days if allowed."""
    member = library["members"].get(member_id)
    if not member:
        return False, "Member not found."

    for rec in member["borrowed"]:
        if rec["isbn"] == isbn and rec["returned"] is None:
            if rec["renewed"]:
                return False, "Book has already been renewed once."

            cur_due = datetime.strptime(rec["due"], "%Y-%m-%d")
            new_due = cur_due + timedelta(days=14)
            rec["due"] = new_due.strftime("%Y-%m-%d")
            rec["renewed"] = True

            record_transaction(
                member_id, isbn, "renew", new_due.strftime("%Y-%m-%d")
            )
            return True, f"Extended due date to {rec['due']}."

    return False, "Active borrowing record not found."


def reserve_book(member_id, isbn):
    """Places hold on a book when out of stock."""
    book = library["books"].get(isbn)
    if not book:
        return False, "Book not found."
    if member_id in book["holds"]:
        return False, "Member already in hold queue."

    book["holds"].append(member_id)
    return True, f"Hold placed. Position in queue: {len(book['holds'])}"


# ==========================================
# 4. FINE SYSTEM
# ==========================================


def calculate_fines(member_id):
    """Evaluates total pending fines including accrued overdue charges."""
    member = library["members"].get(member_id)
    if not member:
        return 0.0

    accrued = 0.0
    today = datetime.now()
    for rec in member["borrowed"]:
        if rec["returned"] is None:
            due = datetime.strptime(rec["due"], "%Y-%m-%d")
            if today > due:
                accrued += (today - due).days * library["fines_rate"]

    return member["fines"] + accrued


def pay_fines(member_id, amount):
    """Processes payment towards member fines balance."""
    member = library["members"].get(member_id)
    if not member:
        return False, "Member not found."

    if amount <= 0:
        return False, "Invalid payment amount."

    paid = min(member["fines"], amount)
    member["fines"] -= paid
    library["fines_collected_month"] += paid
    return True, f"Paid ₦{paid:.2f}. Remaining balance: ₦{member['fines']:.2f}"


def get_overdue_books():
    """Identifies all active borrows past their due date."""
    overdue_list = []
    today_str = datetime.now().strftime("%Y-%m-%d")

    for m_id, member in library["members"].items():
        for rec in member["borrowed"]:
            if rec["returned"] is None and rec["due"] < today_str:
                due_d = datetime.strptime(rec["due"], "%Y-%m-%d")
                now_d = datetime.strptime(today_str, "%Y-%m-%d")
                days_late = (now_d - due_d).days
                overdue_list.append(
                    {
                        "member_id": m_id,
                        "member_name": member["name"],
                        "isbn": rec["isbn"],
                        "book_title": library["books"][rec["isbn"]]["title"],
                        "due_date": rec["due"],
                        "days_overdue": days_late,
                        "fine": days_late * library["fines_rate"],
                    }
                )
    return overdue_list


def send_overdue_notices():
    """Simulates sending email notifications for overdue items."""
    overdue = get_overdue_books()
    notifications = []
    for item in overdue:
        msg = f"NOTICE: '{item['book_title']}' is {item['days_overdue']} days overdue. Fine: ₦{item['fine']:.2f}."
        notifications.append((item["member_id"], item["member_name"], msg))
    return notifications


# ==========================================
# 5. ANALYTICS AND REPORTS
# ==========================================


def get_popular_books(n=5):
    """Returns top N most borrowed books."""
    sorted_books = sorted(
        library["books"].items(),
        key=lambda item: item[1]["borrow_count"],
        reverse=True,
    )
    return sorted_books[:n]


def get_active_members():
    """Identifies members currently holding unreturned books."""
    active = {}
    for m_id, member in library["members"].items():
        unreturned = [r for r in member["borrowed"] if r["returned"] is None]
        if unreturned:
            active[m_id] = {
                "name": member["name"],
                "active_borrows_count": len(unreturned),
            }
    return active


def get_genre_popularity():
    """Calculates percentage distribution of total borrows by genre."""
    totals = {}
    grand_total = 0
    for b in library["books"].values():
        genre = b["genre"]
        count = b["borrow_count"]
        totals[genre] = totals.get(genre, 0) + count
        grand_total += count

    if grand_total == 0:
        return {}

    return {
        genre: round((cnt / grand_total) * 100, 1)
        for genre, cnt in sorted(
            totals.items(), key=lambda x: x[1], reverse=True
        )
    }


def get_borrowing_trends():
    """Aggregates borrowing transaction counts by month."""
    monthly_counts = {}
    for t in library["transactions"]:
        if t["action"] == "borrow":
            month = t["date"][:7]  # YYYY-MM
            monthly_counts[month] = monthly_counts.get(month, 0) + 1
    return monthly_counts


def get_member_statistics():
    """Calculates activity counts and borrowing averages across membership."""
    total_m = len(library["members"])
    if total_m == 0:
        return {"total": 0, "active": 0, "inactive": 0, "avg_borrows": 0.0}

    active_count = sum(
        1 for m in library["members"].values() if m["active"]
    )
    inactive_count = total_m - active_count
    total_borrows = sum(
        len(m["borrowed"]) for m in library["members"].values()
    )

    return {
        "total": total_m,
        "active": active_count,
        "active_pct": round((active_count / total_m) * 100, 1),
        "inactive": inactive_count,
        "inactive_pct": round((inactive_count / total_m) * 100, 1),
        "avg_borrows": round(total_borrows / total_m, 1),
    }


# ==========================================
# 6. ADVANCED RECOMMENDATIONS & METRICS
# ==========================================


def get_recommendations(member_id):
    """Generates personalized book recommendations based on history and co-borrowing patterns."""
    member = library["members"].get(member_id)
    if not member:
        return [], []

    history = member["reading_history"]
    pref_genres = member["preferences"]

    # Genre & tag-based recommendations
    recommendations_genre = []
    for isbn, book in library["books"].items():
        if isbn not in history:
            if book["genre"] in pref_genres:
                recommendations_genre.append(
                    (book["title"], f"Based on genre: {book['genre']}")
                )

    # Co-borrowing algorithm (collaborative filtering pattern)
    co_borrow_counts = {}
    for m_id, other_mem in library["members"].items():
        if m_id != member_id:
            other_hist = set(other_mem["reading_history"])
            # Check overlap
            if any(b in other_hist for b in history):
                for isbn in other_hist:
                    if isbn not in history:
                        co_borrow_counts[isbn] = (
                            co_borrow_counts.get(isbn, 0) + 1
                        )

    collaborative_recs = []
    total_similar = max(1, len(library["members"]) - 1)
    for isbn, count in sorted(
        co_borrow_counts.items(), key=lambda x: x[1], reverse=True
    ):
        b_title = library["books"][isbn]["title"]
        pct = int((count / total_similar) * 100)
        collaborative_recs.append((b_title, f"{pct}% match"))

    return recommendations_genre[:3], collaborative_recs[:3]


def get_most_reviewed_books():
    """Ranks books by number of submitted reviews."""
    return sorted(
        library["books"].items(),
        key=lambda item: len(item[1]["reviews"]),
        reverse=True,
    )


def get_author_ranking():
    """Ranks authors by aggregate total borrowings."""
    authors = {}
    for b in library["books"].values():
        author = b["author"]
        authors[author] = authors.get(author, 0) + b["borrow_count"]
    return sorted(authors.items(), key=lambda x: x[1], reverse=True)


def generate_library_report():
    """Displays comprehensive analytical breakdown of library operations."""
    total_books = sum(b["copies"]["total"] for b in library["books"].values())
    borrowed_books = sum(
        b["copies"]["borrowed"] for b in library["books"].values()
    )
    available_books = sum(
        b["copies"]["available"] for b in library["books"].values()
    )

    avail_pct = (
        round((available_books / total_books) * 100) if total_books else 0
    )
    borr_pct = (
        round((borrowed_books / total_books) * 100) if total_books else 0
    )

    mem_stats = get_member_statistics()
    popular = get_popular_books(5)
    genre_pop = get_genre_popularity()

    print("\n📊 LIBRARY REPORT")
    print("=" * 45)
    print(f"Total Books: {total_books:,}")
    print(f"Available: {available_books:,} ({avail_pct}%)")
    print(f"Borrowed: {borrowed_books:,} ({borr_pct}%)")

    print("\n📈 POPULAR BOOKS (Top 5):")
    for idx, (isbn, b) in enumerate(popular, 1):
        print(f"{idx}. {b['title']} ({b['borrow_count']} borrows)")

    print("\n👥 MEMBER STATISTICS:")
    print(f"Total Members: {mem_stats['total']}")
    print(f"Active: {mem_stats['active']} ({mem_stats['active_pct']}%)")
    print(f"Inactive: {mem_stats['inactive']} ({mem_stats['inactive_pct']}%)")
    print(f"Average Borrows/Member: {mem_stats['avg_borrows']}")

    print("\n🏷️ GENRE POPULARITY:")
    for idx, (genre, pct) in enumerate(genre_pop.items(), 1):
        print(f"{idx}. {genre} ({pct}%)")

    print("\n💸 FINES COLLECTED (This Month):")
    print(f"Total: ₦{library['fines_collected_month']:,.2f}")
    avg_fine = (
        library["fines_collected_month"] / mem_stats["total"]
        if mem_stats["total"]
        else 0
    )
    print(f"Average fine per member: ₦{avg_fine:,.2f}")
    print("=" * 45)


# ==========================================
# CLI USER INTERFACE
# ==========================================


def main():
    while True:
        print("\n📚 PYTHON LIBRARY SYSTEM 📚\n")
        print("1. Book Management")
        print("2. Member Management")
        print("3. Borrow/Return")
        print("4. Fines")
        print("5. Reports & Analytics")
        print("6. Search")
        print("7. Recommendations")
        print("8. Exit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            print("\n📖 BOOK MANAGEMENT")
            print("1. Add Book")
            print("2. View All Books")
            print("3. Update Copies")
            sub = input("Choice: ").strip()
            if sub == "1":
                t = input("Title: ").strip()
                a = input("Author: ").strip()
                g = input("Genre: ").strip()
                c = int(input("Total Copies: ").strip() or "1")
                p = input("Publisher: ").strip()
                isbn = add_book(t, a, g, c, p)
                print(f"✅ Book added with ISBN: {isbn}")
            elif sub == "2":
                for isbn, b in library["books"].items():
                    print(
                        f"[{isbn}] {b['title']} by {b['author']} - Avail: {b['copies']['available']}/{b['copies']['total']}"
                    )
            elif sub == "3":
                isbn = input("ISBN: ").strip()
                chg = int(
                    input("Change count (+ or - number): ").strip() or "0"
                )
                if update_copies(isbn, chg):
                    print("✅ Stock updated.")
                else:
                    print("❌ Failed to update stock.")

        elif choice == "2":
            print("\n👥 MEMBER MANAGEMENT")
            print("1. Register Member")
            print("2. View Member Details")
            print("3. Deactivate Member")
            sub = input("Choice: ").strip()
            if sub == "1":
                n = input("Name: ").strip()
                e = input("Email: ").strip()
                p = input("Phone: ").strip()
                mid = register_member(n, e, p)
                print(f"✅ Member registered with ID: {mid}")
            elif sub == "2":
                mid = input("Member ID: ").strip()
                m = get_member_details(mid)
                if m:
                    print(
                        f"Name: {m['name']} | Email: {m['email']} | Active: {m['active']} | Fines: ₦{m['fines']:.2f}"
                    )
                else:
                    print("Member not found.")
            elif sub == "3":
                mid = input("Member ID: ").strip()
                if deactivate_member(mid):
                    print("✅ Account deactivated.")

        elif choice == "3":
            print("\n📖 BORROW/RETURN MENU")
            print("1. Borrow Book")
            print("2. Return Book")
            print("3. Renew Book")
            print("4. View My Borrowings")
            print("5. Check Availability")

            sub = input("\nChoice: ").strip()
            if sub == "1":
                mid = input("Enter Member ID: ").strip()
                isbn = input("Enter ISBN: ").strip()
                success, msg = borrow_book(mid, isbn)
                if success:
                    m = library["members"][mid]
                    b = library["books"][isbn]
                    print(f"\n✅ Book borrowed successfully!")
                    print(f"Member: {m['name']}")
                    print(f"Book: {b['title']}")
                    active_count = len(
                        [x for x in m["borrowed"] if x["returned"] is None]
                    )
                    print(f"{msg}")
                    print(f"Total books borrowed: {active_count}/5 allowed")
                else:
                    print(f"\n❌ Borrowing failed: {msg}")

            elif sub == "2":
                mid = input("Enter Member ID: ").strip()
                isbn = input("Enter ISBN: ").strip()

                # Check if overdue before executing
                member = library["members"].get(mid)
                borrow_rec = next(
                    (
                        r
                        for r in member["borrowed"]
                        if r["isbn"] == isbn and r["returned"] is None
                    ),
                    None,
                ) if member else None

                if borrow_rec:
                    due_date = datetime.strptime(borrow_rec["due"], "%Y-%m-%d")
                    today_date = datetime.now()
                    days_overdue = (today_date - due_date).days

                    if days_overdue > 0:
                        est_fine = days_overdue * library["fines_rate"]
                        print(
                            f"\n⚠️ This book is {days_overdue} days overdue!"
                        )
                        print(
                            f"Fine: ₦{est_fine:.2f} (₦{library['fines_rate']:.2f} per day)"
                        )
                        pay = (
                            input("\nReturn book and pay fine? (y/n): ")
                            .strip()
                            .lower()
                        )
                        if pay == "y":
                            ok, msg, fine = return_book(mid, isbn)
                            pay_fines(mid, fine)
                            print(f"✅ Book returned!")
                            print(f"Fine paid: ₦{fine:.2f}")
                            print(f"New balance: ₦{member['fines']:.2f}")
                        continue

                ok, msg, fine = return_book(mid, isbn)
                if ok:
                    print(f"✅ {msg}")
                else:
                    print(f"❌ {msg}")

            elif sub == "3":
                mid = input("Member ID: ").strip()
                isbn = input("ISBN: ").strip()
                ok, msg = renew_book(mid, isbn)
                print(f"{'✅' if ok else '❌'} {msg}")

            elif sub == "4":
                mid = input("Member ID: ").strip()
                hist = get_member_history(mid)
                print(f"\nBorrowing History for {mid}:")
                for r in hist:
                    status = (
                        f"Returned on {r['returned']}"
                        if r["returned"]
                        else f"Due on {r['due']}"
                    )
                    print(
                        f"  • ISBN: {r['isbn']} | Borrowed: {r['borrowed']} | {status}"
                    )

            elif sub == "5":
                isbn = input("ISBN: ").strip()
                avail = check_availability(isbn)
                if avail:
                    print(
                        f"\nAvailability for '{avail['title']}': {avail['available']}/{avail['total']} available ({avail['holds_count']} holds)"
                    )

        elif choice == "4":
            print("\n💸 FINES MANAGEMENT")
            print("1. View Member Fine")
            print("2. Pay Fines")
            print("3. Send Overdue Notices")
            sub = input("Choice: ").strip()
            if sub == "1":
                mid = input("Member ID: ").strip()
                fine = calculate_fines(mid)
                print(f"Total calculated fine for {mid}: ₦{fine:.2f}")
            elif sub == "2":
                mid = input("Member ID: ").strip()
                amt = float(input("Amount to pay: ₦").strip() or "0")
                ok, msg = pay_fines(mid, amt)
                print(f"{'✅' if ok else '❌'} {msg}")
            elif sub == "3":
                notices = send_overdue_notices()
                print(f"\nSent {len(notices)} overdue notices:")
                for mid, name, msg in notices:
                    print(f"  📩 [{name} - {mid}]: {msg}")

        elif choice == "5":
            generate_library_report()

        elif choice == "6":
            q = input("\nEnter search query (title, author, genre, tag, ISBN): ").strip()
            results = search_books(q)
            print(f"\n🔍 Found {len(results)} matching books:")
            for isbn, b in results.items():
                print(
                    f"  [{isbn}] {b['title']} by {b['author']} ({b['genre']}) - Avail: {b['copies']['available']}"
                )

        elif choice == "7":
            mid = input("\nEnter Member ID: ").strip()
            member = library["members"].get(mid)
            if member:
                g_recs, c_recs = get_recommendations(mid)
                print(f"\n📚 RECOMMENDATIONS FOR {member['name']}")
                print("Based on your reading history:")
                for idx, (title, reason) in enumerate(g_recs, 1):
                    print(f"{idx}. {title} ({reason})")

                print(
                    f"\nMembers who borrowed similar books also borrowed:"
                )
                for idx, (title, pct) in enumerate(c_recs, 1):
                    print(f"{idx}. {title} ({pct})")
            else:
                print("Member not found.")

        elif choice == "8":
            print("\nGoodbye! Thank you for using the Library System. 👋")
            break


if __name__ == "__main__":
    main()