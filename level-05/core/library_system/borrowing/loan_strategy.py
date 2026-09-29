class LoanStrategy:
    def get_loan_period(self):
        raise NotImplementedError

    def get_max_loans(self):
        raise NotImplementedError

    def can_renew(self):
        raise NotImplementedError