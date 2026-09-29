from .resource import Resource


class DVD(Resource):
    def __init__(
        self,
        isbn,
        title,
        authors,
        publisher,
        year,
        genre,
        copies,
        director,
        runtime,
        rating,
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

        self.director = director
        self.runtime = runtime
        self.rating = rating