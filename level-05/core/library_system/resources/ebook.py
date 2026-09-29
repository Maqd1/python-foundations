from .resource import Resource


class EBook(Resource):
    def __init__(
        self,
        isbn,
        title,
        authors,
        publisher,
        year,
        genre,
        copies,
        file_format,
        download_link,
        drm,
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

        self.file_format = file_format
        self.download_link = download_link
        self.drm = drm
