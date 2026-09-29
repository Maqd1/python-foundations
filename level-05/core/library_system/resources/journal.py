from .resource import Resource


class Journal(Resource):
    def __init__(
        self,
        isbn,
        title,
        authors,
        publisher,
        year,
        genre,
        copies,
        volume,
        issue,
        issn,
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

        self.volume = volume
        self.issue = issue
        self.issn = issn