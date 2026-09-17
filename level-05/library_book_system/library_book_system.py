class Book:
    def __init__(self, title, author, isbn, year):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.is_borrowed = False

    def borrow(self):
        if self.is_borrowed:
            print(f"❌ '{self.title}' is already borrowed.")
            return False

        self.is_borrowed = True
        print(f"✅ Successfully borrowed '{self.title}'.")
        return True

    def return_book(self):
        if not self.is_borrowed:
            print(f"❌ '{self.title}' is not currently borrowed.")
            return False

        self.is_borrowed = False
        print(f"✅ Successfully returned '{self.title}'.")
        return True

    def display_info(self):
        status = "Borrowed" if self.is_borrowed else "Available"

        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"ISBN: {self.isbn}")
        print(f"Year: {self.year}")
        print(f"Status: {status}")

    def __str__(self):
        status = "Borrowed" if self.is_borrowed else "Available"
        return f"{self.title} by {self.author} ({status})"

    def __eq__(self, other):
        if not isinstance(other, Book):
            return NotImplemented

        return self.isbn == other.isbn


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        if book in self.books:
            print(f"❌ A book with ISBN {book.isbn} already exists.")
            return False

        self.books.append(book)
        print(f"📖 Book added: {book}")
        return True

    def remove_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                if book.is_borrowed:
                    print("❌ Cannot remove a borrowed book.")
                    return False

                self.books.remove(book)
                print(f"🗑️ Book removed: {book.title}")
                return True

        print(f"❌ No book found with ISBN {isbn}.")
        return False

    def search_by_title(self, title):
        results = []

        for book in self.books:
            if title.lower() in book.title.lower():
                results.append(book)

        return results

    def search_by_author(self, author):
        results = []

        for book in self.books:
            if author.lower() in book.author.lower():
                results.append(book)

        return results

    def list_books(self):
        if not self.books:
            print("📚 The library is empty.")
            return

        print(f"\nCurrent books ({len(self.books)}):")

        for number, book in enumerate(self.books, start=1):
            print(f"{number}. {book}")


def display_search_results(results):
    if not results:
        print("❌ No books found.")
        return

    print(f"Found {len(results)} book(s):")

    for book in results:
        print(f"📖 {book}")


def find_book_by_isbn(library):
    isbn = input("Enter ISBN: ")

    for book in library.books:
        if book.isbn == isbn:
            return book

    print(f"❌ No book found with ISBN {isbn}.")
    return None


def create_book(library):
    print("\n--- Add Book ---")

    title = input("Title: ")
    author = input("Author: ")
    isbn = input("ISBN: ")

    try:
        year = int(input("Year: "))
    except ValueError:
        print("❌ Year must be a number.")
        return

    book = Book(title, author, isbn, year)
    library.add_book(book)


def borrow_book(library):
    book = find_book_by_isbn(library)

    if book:
        print(f"\n📖 Borrowing: {book}")
        book.borrow()


def return_book(library):
    book = find_book_by_isbn(library)

    if book:
        print(f"\n📖 Returning: {book}")
        book.return_book()


def search_books(library):
    print("\n1. Search by title")
    print("2. Search by author")

    choice = input("Choice: ")

    if choice == "1":
        title = input("Enter title: ")
        results = library.search_by_title(title)
        display_search_results(results)

    elif choice == "2":
        author = input("Enter author: ")
        results = library.search_by_author(author)
        display_search_results(results)

    else:
        print("❌ Invalid choice.")


def main():
    library = Library()

    # Sample books
    library.add_book(
        Book(
            "Python Programming",
            "Damilola",
            "978-001",
            2024
        )
    )

    library.add_book(
        Book(
            "Data Science",
            "John",
            "978-002",
            2023
        )
    )

    library.add_book(
        Book(
            "Web Development",
            "Alice",
            "978-003",
            2025
        )
    )

    print("\n📚 LIBRARY MANAGEMENT SYSTEM 📚")

    while True:
        print("\n1. Add Book")
        print("2. Remove Book")
        print("3. Search Books")
        print("4. List Books")
        print("5. Borrow Book")
        print("6. Return Book")
        print("7. Display Book Info")
        print("8. Exit")

        choice = input("\nChoice: ")

        if choice == "1":
            create_book(library)

        elif choice == "2":
            book = find_book_by_isbn(library)

            if book:
                library.remove_book(book.isbn)

        elif choice == "3":
            search_books(library)

        elif choice == "4":
            library.list_books()

        elif choice == "5":
            borrow_book(library)

        elif choice == "6":
            return_book(library)

        elif choice == "7":
            book = find_book_by_isbn(library)

            if book:
                print("\n📋 BOOK DETAILS")
                book.display_info()

        elif choice == "8":
            print("\nThank you for using the Library Management System! 👋")
            break

        else:
            print("❌ Invalid choice. Please select 1–8.")


if __name__ == "__main__":
    main()