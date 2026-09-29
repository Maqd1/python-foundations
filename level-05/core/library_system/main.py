from core.library_system.api import LibraryAPI


def create_library():
    return LibraryAPI()


def main():
    library = create_library()

    print("LIBRARY SYSTEM")
    print("=" * 40)
    print(
        f"Resources in catalog: "
        f"{len(library.catalog.resources)}"
    )


if __name__ == "__main__":
    main()