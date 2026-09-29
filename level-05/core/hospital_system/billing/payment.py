from dataclasses import dataclass
from datetime import date


@dataclass
class Payment:
    payment_id: str
    invoice_id: str
    amount: float
    payment_date: date
    method: str
    status: str = "COMPLETED"

    def __post_init__(self):
        if self.amount <= 0:
            raise ValueError(
                "Payment amount must be greater than zero."
            )

    def refund(self) -> None:
        self.status = "REFUNDED"

    @property
    def is_completed(self) -> bool:
        return self.status == "COMPLETED"
    