# Library Book System

A simple interactive library management system built with Python and Object-Oriented Programming (OOP).

## Features

The system supports:

- Adding books
- Removing books
- Searching books by title
- Searching books by author
- Listing all books
- Borrowing books
- Returning books
- Displaying detailed book information
- Preventing a borrowed book from being borrowed again
- Preventing an available book from being returned
- Comparing books using ISBN

## OOP Concepts

This project demonstrates:

- Classes
- Objects
- Constructors
- Attributes
- Methods
- Lists
- Encapsulation
- Inheritance of behavior through object relationships
- Magic methods
- Error handling

## Classes

### Book

The `Book` class represents an individual book.

Attributes:

- `title`
- `author`
- `isbn`
- `year`
- `is_borrowed`

Methods:

- `borrow()`
- `return_book()`
- `display_info()`

Magic methods:

- `__str__()` - provides a readable representation of a book
- `__eq__()` - compares two books using their ISBN

### Library

The `Library` class manages a collection of books.

It maintains a list of `Book` objects.

Methods:

- `add_book()`
- `remove_book()`
- `search_by_title()`
- `search_by_author()`
- `list_books()`

## Magic Methods

### `__str__()`

The `__str__()` method controls what is displayed when a `Book` object is converted to a string.

For example:

```text
Python Programming by Damilola (Available)