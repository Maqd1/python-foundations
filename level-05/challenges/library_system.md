'''
4️⃣ 📚 VERY HARD LIBRARY SYSTEM
The Complete Library Management System 📖

Build a comprehensive library system with books, members, borrowing, and digital resources!

Package Structure:
text

library_system/
    __init__.py
    resources/
        __init__.py
        book.py
        ebook.py
        audiobook.py
        journal.py
        dvd.py
    patrons/
        __init__.py
        member.py
        librarian.py
        admin.py
    borrowing/
        __init__.py
        loan.py
        hold.py
        fine.py
    catalog/
        __init__.py
        catalog.py
        search.py
    services/
        __init__.py
        recommendation.py
        notification.py
        reporting.py
    exceptions/
        __init__.py
        library_exceptions.py
    tests/
        __init__.py
        test_books.py
    main.py
    cli.py
    api.py
    setup.py

Requirements:

    Resource Hierarchy (Inheritance):

        Resource: ISBN, title, authors, publisher, year, genre, copies

        Book: Pages, edition, format

        EBook: File format, download link, DRM

        AudioBook: Narrator, duration, format

        Journal: Volume, issue, ISSN

        DVD: Director, runtime, rating

    Patron System:

        Member: Name, ID, contact, membership_type

        StudentMember: Student ID, school, borrow limit

        FacultyMember: Department, research area

        CommunityMember: Address, occupation

    Borrowing System (Strategy Pattern):

        Different loan periods based on membership

        Renewal policies

        Hold system for popular books

        Inter-library loans

    Fine System (Strategy Pattern):

        Daily overdue fines

        Different rates for different resources

        Fine exemption policies

        Payment processing

    Catalog System (HARD):

        Search by title, author, ISBN, subject

        Advanced filters

        Browse by category

        Recommendation engine

    Recommendation System (HARDEST):

        Collaborative filtering

        Content-based filtering

        Popularity-based suggestions

        Reading history analysis

    Inventory Management:

        Stock tracking

        Condition assessment

        Purchase suggestions

        Weeding/discarding

Sample Output:
text

📚 LAGOS CITY PUBLIC LIBRARY 📚

📖 LIBRARY STATISTICS
Total Resources: 45,678
Books: 32,456 (71%)
EBooks: 8,234 (18%)
AudioBooks: 3,456 (8%)
Journals: 987 (2%)
DVDs: 545 (1%)

Total Members: 12,345
Active Borrowers: 8,234
Total Loans: 2,345
Overdue Items: 234

=====================================
👤 MEMBER PROFILE
Name: Damilola Ogunleye
Member ID: MEM-2024-5678
Membership Type: Student (Premium)
University: University of Lagos
Department: Computer Science
Registered: 2024-01-15
Status: ACTIVE

📊 BORROWING STATISTICS
Currently Borrowed: 3/10
Currently On Hold: 1
Overdue Items: 0
Total Borrowed Lifetime: 45

=====================================
📚 CURRENT LOANS
1. "Introduction to Algorithms" (3rd Ed.)
   Author: Thomas Cormen
   ISBN: 978-0262033848
   Borrowed: 2026-08-25
   Due: 2026-09-25
   Status: On Loan (Days remaining: 20)

2. "Clean Code"
   Author: Robert Martin
   ISBN: 978-0132350884
   Borrowed: 2026-09-01
   Due: 2026-10-01
   Status: On Loan (Days remaining: 26)

3. "Design Patterns"
   Author: Erich Gamma
   ISBN: 978-0201633610
   Borrowed: 2026-09-05
   Due: 2026-10-05
   Status: On Loan (Days remaining: 30)

=====================================
🔍 SEARCH RESULTS
Search: "Python Programming"
Results: 28 items found

1. "Python Crash Course"
   Author: Eric Matthes
   ISBN: 978-1593279288
   Status: AVAILABLE
   Copies: 3/5 available

2. "Automate the Boring Stuff"
   Author: Al Sweigart
   ISBN: 978-1593279929
   Status: BORROWED
   Due: 2026-09-20
   Holds: 2

3. "Python for Data Analysis"
   Author: Wes McKinney
   ISBN: 978-1449319793
   Status: ON HOLD
   Available: 2026-09-25

=====================================
📚 PLACE HOLD
Book: "Design Patterns"
Hold Requested: 2026-09-05
Position in Queue: 1
Estimated Availability: 2026-10-05

Hold confirmed! You will be notified when available.
=====================================

=====================================
📝 RECOMMENDATIONS FOR YOU
Based on your borrowing history:

1. "Refactoring" by Martin Fowler
   Reason: You borrowed "Clean Code"
   Copies: 2 available

2. "The Pragmatic Programmer" by Andrew Hunt
   Reason: You borrowed "Design Patterns"
   Copies: 1 available (1 hold)

3. "Introduction to Machine Learning" by Peter Flach
   Reason: You borrowed "Python for Data Analysis"
   Copies: 3 available

=====================================
⚠️ NOTIFICATION: OVERDUE BOOK
Book: "Data Structures in Python"
Due Date: 2026-09-01
Days Overdue: 4
Fine: ₦200.00 (₦50.00/day)
Status: UNPAID

Please return or renew immediately!

=====================================
💰 FINE MANAGEMENT
Current Fines: ₦200.00
Total Paid: ₦0.00
Outstanding: ₦200.00

Payment Options:
1. Pay Now
2. Request Extension (1 renewal remaining)
3. Appeal Fine

Choose option: 1
✅ Payment received! Fine cleared.

=====================================
📊 LIBRARY STATISTICS (September 2026)
Most Borrowed Books:
1. "Introduction to Algorithms" - 45 loans
2. "Clean Code" - 38 loans
3. "Design Patterns" - 32 loans

Most Popular Genres:
1. Technology (35%)
2. Science (25%)
3. Fiction (20%)
4. History (10%)
5. Other (10%)

Peak Hours: 2PM - 5PM (45% of loans)
Average Loan Duration: 14.5 days

=====================================
📅 UPCOMING EVENTS
1. Book Club: "One Hundred Years of Solitude"
   Date: 2026-09-15
   Time: 18:00
   Location: Reading Room A

2. Author Talk: Chimamanda Ngozi Adichie
   Date: 2026-10-01
   Time: 17:00
   Location: Main Auditorium

3. Digital Library Workshop
   Date: 2026-10-05
   Time: 14:00
   Location: Computer Lab

=====================================
💳 ACCOUNT SUMMARY
Member: Damilola Ogunleye
Membership Fee (2026): ₦5,000.00
Paid: ₦5,000.00
Balance: ₦0.00

Benefits:
✅ Unlimited borrowing (10 items)
✅ Digital library access
✅ Free workshops
✅ Book club membership

Concepts Tested: Advanced inheritance, composition, strategy pattern, observer pattern, dataclasses, property decorators, search algorithms, recommendation algorithms, fine calculation, holds management
'''