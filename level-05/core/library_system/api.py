from core.library_system.borrowing.loan import Loan
from core.library_system.catalog.catalog import Catalog
from core.library_system.catalog.search import CatalogSearch
from core.library_system.services.notification import NotificationService
from core.library_system.services.recommendation import RecommendationService
from core.library_system.services.reporting import ReportingService


class LibraryAPI:
    def __init__(self):
        self.catalog = Catalog()
        self.search = CatalogSearch(self.catalog)
        self.notifications = NotificationService()
        self.recommendations = RecommendationService()
        self.reporting = ReportingService()
        self.loans = []

    def add_resource(self, resource):
        self.catalog.add_resource(resource)

    def remove_resource(self, resource):
        self.catalog.remove_resource(resource)

    def borrow(self, member, resource):
        loan = Loan(member, resource)
        loan.activate()

        self.loans.append(loan)

        self.notifications.notify(
            "borrowed",
            member,
            resource,
        )

        return loan

    def return_resource(self, loan):
        loan.mark_returned()

        self.notifications.notify(
            "returned",
            loan.member,
            loan.resource,
        )

    def get_active_loans(self):
        return [
            loan
            for loan in self.loans
            if loan.is_active
        ]

    def get_overdue_loans(self):
        return [
            loan
            for loan in self.loans
            if loan.is_overdue
        ]