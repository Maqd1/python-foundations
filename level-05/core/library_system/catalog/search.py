class CatalogSearch:
    def __init__(self, catalog):
        self.catalog = catalog

    def by_title(self, title):
        title = title.lower()

        return [
            resource
            for resource in self.catalog.resources
            if title in resource.title.lower()
        ]

    def by_author(self, author):
        author = author.lower()

        return [
            resource
            for resource in self.catalog.resources
            if any(
                author in item.lower()
                for item in resource.authors
            )
        ]

    def by_isbn(self, isbn):
        return [
            resource
            for resource in self.catalog.resources
            if resource.isbn == isbn
        ]

    def by_subject(self, subject):
        subject = subject.lower()

        return [
            resource
            for resource in self.catalog.resources
            if resource.subject
            and subject in resource.subject.lower()
        ]

    def by_genre(self, genre):
        genre = genre.lower()

        return [
            resource
            for resource in self.catalog.resources
            if resource.genre.lower() == genre
        ]

    def available_only(self):
        return [
            resource
            for resource in self.catalog.resources
            if resource.is_available
        ]

    def filter(
        self,
        title=None,
        author=None,
        genre=None,
        subject=None,
        year=None,
        available=None,
    ):
        results = self.catalog.resources

        if title is not None:
            title = title.lower()
            results = [
                resource
                for resource in results
                if title in resource.title.lower()
            ]

        if author is not None:
            author = author.lower()
            results = [
                resource
                for resource in results
                if any(
                    author in item.lower()
                    for item in resource.authors
                )
            ]

        if genre is not None:
            genre = genre.lower()
            results = [
                resource
                for resource in results
                if resource.genre.lower() == genre
            ]
            
        if subject is not None:
            subject = subject.lower()
            results = [
                resource
                for resource in results
                if resource.subject
                and subject in resource.subject.lower()
            ]

        if year is not None:
            results = [
                resource
                for resource in results
                if resource.year == year
            ]

        if available is not None:
            results = [
                resource
                for resource in results
                if resource.is_available == available
            ]

        return results