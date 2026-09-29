from .staff import Staff


class Librarian(Staff):
    def add_resource(self, catalog, resource):
        catalog.add_resource(resource)
        