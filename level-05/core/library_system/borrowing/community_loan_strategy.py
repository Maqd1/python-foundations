from .loan_strategy import LoanStrategy


class CommunityLoanStrategy(LoanStrategy):
    def get_loan_period(self):
        return 21

    def get_max_loans(self):
        return 3

    def can_renew(self):
        return False
