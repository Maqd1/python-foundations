from core.library_system.catalog.catalog import Catalog
from core.library_system.catalog.search import CatalogSearch
from core.library_system.resources.book import Book


def make_books():
    return [
        Book(
            "978-1",
            "Clean Code",
            ["Robert Martin"],
            "Prentice Hall",
            2008,
            "Programming",
            3,
            464,
            1,
            "Hardcover",
        ),
        Book(
            "978-2",
            "Python Crash Course",
            ["Eric Matthes"],
            "No Starch Press",
            2023,
            "Programming",
            2,
            544,
            3,
            "Paperback",
        ),
        Book(
            "978-3",
            "Clean Architecture",
            ["Robert Martin"],
            "Prentice Hall",
            2017,
            "Programming",
            2,
            432,
            1,
            "Hardcover",
        ),
    ]


def test_catalog_add_and_find():
    catalog = Catalog()
    book = make_books()[0]

    catalog.add_resource(book)

    assert catalog.get_by_isbn("978-1") is book


def test_catalog_title_search():
    catalog = Catalog()

    for book in make_books():
        catalog.add_resource(book)

    results = catalog.get_by_title("Clean Code")

    assert len(results) == 1
    assert results[0].isbn == "978-1"


def test_search_by_author():
    catalog = Catalog()

    for book in make_books():
        catalog.add_resource(book)

    search = CatalogSearch(catalog)

    results = search.by_author("Robert Martin")

    assert len(results) == 2


def test_search_by_genre():
    catalog = Catalog()

    for book in make_books():
        catalog.add_resource(book)

    search = CatalogSearch(catalog)

    results = search.by_genre("programming")

    assert len(results) == 3


def test_resource_borrow_and_return():
    book = make_books()[0]

    assert book.available_copies == 3

    book.borrow()

    assert book.available_copies == 2
    assert book.borrowed_copies == 1

    book.return_copy()

    assert book.available_copies == 3