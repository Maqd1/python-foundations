from .resource import Resource


class Book(Resource):
    def __init__(
        self,
        isbn,
        title,
        authors,
        publisher,
        year,
        genre,
        copies,
        pages,
        edition,
        format,
    ):
        super().__init__(
            isbn,
            title,
            authors,
            publisher,
            year,
            genre,
            copies,
        )

        self.pages = pages
        self.edition = edition
        self.format = format
