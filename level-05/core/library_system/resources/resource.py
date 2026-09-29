from core.library_system.exceptions.library_exceptions import ResourceUnavailableError


class Resource:
    def __init__(
        self,
        isbn,
        title,
        authors,
        publisher,
        year,
        genre,
        copies,
        subject=None,
    ):
        self.isbn = isbn
        self.title = title
        self.authors = authors
        self.publisher = publisher
        self.year = year
        self.genre = genre
        self.subject = subject
        self.copies = copies
        self.available_copies = copies


    @property
    def copies(self):
        return self._copies

    @copies.setter
    def copies(self, value):
        if not isinstance(value, int):
            raise TypeError("Copies must be an integer.")

        if value < 0:
            raise ValueError("Copies cannot be negative.")

        self._copies = value

    def borrow(self):
        if self.available_copies <= 0:
            raise ResourceUnavailableError(
                f'"{self.title}" has no available copies.'
            )

        self.available_copies -= 1

    def return_copy(self):
        if self.available_copies >= self.copies:
            raise ValueError(
                f'All copies of "{self.title}" are already available.'
            )

        self.available_copies += 1

    @property
    def is_available(self):
        return self.available_copies > 0

    @property
    def borrowed_copies(self):
        return self.copies - self.available_copies