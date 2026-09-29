from .resource import Resource


class AudioBook(Resource):
    def __init__(
        self,
        isbn,
        title,
        authors,
        publisher,
        year,
        genre,
        copies,
        narrator,
        duration,
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

        self.narrator = narrator
        self.duration = duration
        self.format = format