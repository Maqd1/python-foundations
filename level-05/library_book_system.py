'''
Q2: The Library Book System (Easy)

Create an OOP system for managing library books.

Requirements:

    Create a Book class with:

        Attributes: title, author, isbn, year, is_borrowed

        Methods: borrow(), return_book(), display_info()

    Create a Library class that:

        Maintains a list of books

        Methods: add_book(), remove_book(), search_by_title(), search_by_author(), list_books()

    Add proper error handling:

        Can't borrow already borrowed book

        Can't return book that's not borrowed

    Use magic methods:

        __str__() for book display

        __eq__() to compare books by ISBN

Sample Output:
text

📚 LIBRARY MANAGEMENT SYSTEM 📚

📖 Book added: Python Programming by Damilola
📖 Book added: Data Science by John
📖 Book added: Web Development by Alice

Current books (3):
1. Python Programming by Damilola (Available)
2. Data Science by John (Available)
3. Web Development by Alice (Available)

🔍 Search by title: Python
Found: Python Programming by Damilola (Available)

📖 Borrowing: Python Programming by Damilola
✅ Successfully borrowed!

Current books:
1. Python Programming by Damilola (Borrowed)
2. Data Science by John (Available)
3. Web Development by Alice (Available)

📖 Returning: Python Programming by Damilola
✅ Successfully returned!

Current books:
1. Python Programming by Damilola (Available)
2. Data Science by John (Available)
3. Web Development by Alice (Available)

Concepts: Classes, objects, lists, constructors, magic methods, encapsulation
'''