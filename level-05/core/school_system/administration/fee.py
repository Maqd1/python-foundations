from dataclasses import dataclass, field
from typing import List


@dataclass
class Fee:
    name: str
    amount: float
    paid: float = 0.0

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("Fee amount cannot be negative.")

        if self.paid < 0:
            raise ValueError("Paid amount cannot be negative.")

        if self.paid > self.amount:
            raise ValueError(
                "Paid amount cannot exceed the fee amount."
            )

    @property
    def balance(self) -> float:
        return self.amount - self.paid

    @property
    def is_paid(self) -> bool:
        return self.balance == 0

    def make_payment(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError(
                "Payment amount must be greater than zero."
            )

        if self.paid + amount > self.amount:
            raise ValueError(
                "Payment cannot exceed the outstanding balance."
            )

        self.paid += amount


@dataclass
class StudentAccount:
    student_id: str
    fees: List[Fee] = field(default_factory=list)

    def add_fee(self, fee: Fee) -> None:
        self.fees.append(fee)

    @property
    def total_fees(self) -> float:
        return sum(fee.amount for fee in self.fees)

    @property
    def total_paid(self) -> float:
        return sum(fee.paid for fee in self.fees)

    @property
    def outstanding_balance(self) -> float:
        return sum(fee.balance for fee in self.fees)

    @property
    def is_cleared(self) -> bool:
        return self.outstanding_balance == 0

    def make_payment(self, fee_name: str, amount: float) -> None:
        for fee in self.fees:
            if fee.name == fee_name:
                fee.make_payment(amount)
                return

        raise ValueError(f"Fee '{fee_name}' not found.")