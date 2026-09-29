from datetime import datetime, timedelta


class Loan:
    def __init__(self, member, resource):
        self.member = member
        self.resource = resource
        self.borrowed_at = None
        self.due_date = None
        self.returned_at = None
        self.renewal_count = 0
        self.activated = False


    @property
    def is_returned(self):
        return self.returned_at is not None

    @property
    def is_active(self):
        return self.activated and not self.is_returned

    @property
    def is_overdue(self):
        if self.is_returned:
            return self.returned_at > self.due_date

        return datetime.now() > self.due_date


    
    def activate(self):
        if self.activated:
            raise ValueError("Loan is already active.")

        if self.member.loan_count >= self.member.loan_strategy.get_max_loans():
            raise ValueError("Member has reached the maximum number of loans.")

        self.resource.borrow()

        self.borrowed_at = datetime.now()
        loan_period = self.member.loan_strategy.get_loan_period()
        self.due_date = self.borrowed_at + timedelta(days=loan_period)

        self.member.add_borrowed_resource(self.resource)
        self.activated = True


    def mark_returned(self):
        if not self.activated:
            raise ValueError("Loan has not been activated.")

        if self.is_returned:
            raise ValueError("Loan has already been returned.")

        self.resource.return_copy()
        self.member.remove_borrowed_resource(self.resource)
        self.returned_at = datetime.now()

    def renew(self):
        if not self.is_active:
            raise ValueError("Only active loans can be renewed.")
    
        if not self.member.loan_strategy.can_renew():
            raise ValueError("Member is not allowed to renew this loan.")
    
        self.due_date += timedelta(
            days=self.member.loan_strategy.get_loan_period()
        )
    
        self.renewal_count += 1