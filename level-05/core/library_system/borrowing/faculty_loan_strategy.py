from .loan_strategy import LoanStrategy


class FacultyLoanStrategy(LoanStrategy):
    def get_loan_period(self):
        return 30

    def get_max_loans(self):
        return 10

    def can_renew(self):
        return True
