from dataclasses import dataclass


@dataclass
class Insurance:
    insurance_id: str
    provider: str
    policy_number: str
    coverage_percentage: float
    active: bool = True

    def __post_init__(self):
        if not 0 <= self.coverage_percentage <= 100:
            raise ValueError(
                "Coverage percentage must be between 0 and 100."
            )

    def calculate_coverage(self, amount: float) -> float:
        if not self.active:
            return 0.0

        return amount * (
            self.coverage_percentage / 100
        )

    def calculate_patient_amount(self, amount: float) -> float:
        return amount - self.calculate_coverage(amount)

    def deactivate(self) -> None:
        self.active = False

    def activate(self) -> None:
        self.active = True