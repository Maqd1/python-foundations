class InventoryService:
    VALID_CONDITIONS = {"NEW", "GOOD", "FAIR", "POOR", "DAMAGED"}

    def __init__(self):
        self.conditions = {}
        self.purchase_requests = set()
        self.weeded_resources = set()

    def set_condition(self, resource, condition: str) -> None:
        condition = condition.upper()

        if condition not in self.VALID_CONDITIONS:
            raise ValueError(f"Invalid condition: {condition}")

        self.conditions[resource.isbn] = condition

    def get_condition(self, resource):
        return self.conditions.get(resource.isbn, "GOOD")

    def suggest_purchase(self, resource) -> bool:
        if resource.available_copies == 0:
            self.purchase_requests.add(resource.isbn)
            return True

        return False

    def purchase_suggestions(self):
        return set(self.purchase_requests)

    def weed(self, resource) -> None:
        self.weeded_resources.add(resource.isbn)

    def is_weeded(self, resource) -> bool:
        return resource.isbn in self.weeded_resources
