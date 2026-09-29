from .staff import Staff


class Admin(Staff):
    def remove_resource(self, catalog, resource):
        catalog.remove_resource(resource)
        