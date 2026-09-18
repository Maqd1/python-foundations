from dataclasses import dataclass
from datetime import date


@dataclass
class Medication:
    medication_id: str
    name: str
    dosage: str
    form: str
    unit_price: float
    expiry_date: date

    @property
    def is_expired(self) -> bool:
        return date.today() > self.expiry_date

    def days_until_expiry(self) -> int:
        return (self.expiry_date - date.today()).days

    def __str__(self) -> str:
        return (
            f"{self.name} | "
            f"{self.dosage} | "
            f"{self.form} | "
            f"₦{self.unit_price:.2f}"
        )