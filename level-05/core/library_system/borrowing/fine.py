from datetime import datetime


class Fine:
    def __init__(
        self,
        loan,
        daily_rate=1.0,
        exempt=False,
    ):
        self.loan = loan
        self.daily_rate = daily_rate
        self.exempt = exempt
        self.paid = False
        self.paid_at = None

    @property
    def overdue_days(self):
        if self.exempt or not self.loan.due_date:
            return 0

        end_time = (
            self.loan.returned_at
            if self.loan.returned_at
            else datetime.now()
        )

        overdue_seconds = (
            end_time - self.loan.due_date
        ).total_seconds()

        if overdue_seconds <= 0:
            return 0

        return (overdue_seconds // 86400) + 1

    @property
    def amount(self):
        if self.exempt:
            return 0.0

        return self.overdue_days * self.daily_rate

    def pay(self):
        if self.paid:
            raise ValueError("Fine has already been paid.")

        self.paid = True
        self.paid_at = datetime.now()