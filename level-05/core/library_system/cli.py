from core.library_system.api import LibraryAPI


def run_cli():
    library = LibraryAPI()

    print("LIBRARY SYSTEM")
    print("=" * 40)

    while True:
        print("\n1. List resources")
        print("2. Search by title")
        print("3. Search by author")
        print("4. Search by ISBN")
        print("5. Search by genre")
        print("6. Inventory report")
        print("7. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            for resource in library.catalog.get_all():
                print(
                    f"{resource.title} "
                    f"({resource.isbn})"
                )

        elif choice == "2":
            title = input("Title: ")
            results = library.search.by_title(title)

            for resource in results:
                print(resource.title)

        elif choice == "3":
            author = input("Author: ")
            results = library.search.by_author(author)

            for resource in results:
                print(resource.title)

        elif choice == "4":
            isbn = input("ISBN: ")
            results = library.search.by_isbn(isbn)

            for resource in results:
                print(resource.title)

        elif choice == "5":
            genre = input("Genre: ")
            results = library.search.by_genre(genre)

            for resource in results:
                print(resource.title)

        elif choice == "6":
            print(
                library.reporting.inventory_report(
                    library.catalog
                )
            )

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    run_cli()