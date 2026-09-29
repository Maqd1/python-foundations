class Catalog:
    def __init__(self):
        self.resources = []

    def add_resource(self, resource):
        self.resources.append(resource)

    def remove_resource(self, resource):
        self.resources.remove(resource)

    def get_by_isbn(self, isbn):
        for resource in self.resources:
            if resource.isbn == isbn:
                return resource

        return None

    def get_by_title(self, title):
        matches = []

        for resource in self.resources:
            if resource.title == title:
                matches.append(resource)

        return matches

    def get_by_author(self, author):
        matches = []

        for resource in self.resources:
            if author in resource.authors:
                matches.append(resource)

        return matches

    def get_by_genre(self, genre):
        matches = []

        for resource in self.resources:
            if resource.genre == genre:
                matches.append(resource)

        return matches

    def get_all(self):
        return self.resources.copy()
