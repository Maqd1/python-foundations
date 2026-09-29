from .loan_strategy import LoanStrategy


class StudentLoanStrategy(LoanStrategy):
    def get_loan_period(self):
        return 14

    def get_max_loans(self):
        return 5

    def can_renew(self):
        return True