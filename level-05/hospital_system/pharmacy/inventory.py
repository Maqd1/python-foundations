from dataclasses import dataclass, field
from datetime import date

from hospital_system.exceptions.medical_exceptions import (
    InventoryError,
)
from hospital_system.pharmacy.medication import Medication


@dataclass
class InventoryItem:
    medication: Medication
    quantity: int
    reorder_level: int = 10

    def __post_init__(self):
        if self.quantity < 0:
            raise InventoryError(
                "Inventory quantity cannot be negative."
            )

        if self.reorder_level < 0:
            raise InventoryError(
                "Reorder level cannot be negative."
            )

    @property
    def needs_reorder(self) -> bool:
        return self.quantity <= self.reorder_level

    @property
    def is_expired(self) -> bool:
        return self.medication.is_expired


@dataclass
class Inventory:
    items: dict[str, InventoryItem] = field(
        default_factory=dict
    )

    def add_medication(
        self,
        medication: Medication,
        quantity: int,
        reorder_level: int = 10,
    ) -> None:
        if quantity < 0:
            raise InventoryError(
                "Quantity cannot be negative."
            )

        if medication.medication_id in self.items:
            self.items[
                medication.medication_id
            ].quantity += quantity
        else:
            self.items[
                medication.medication_id
            ] = InventoryItem(
                medication=medication,
                quantity=quantity,
                reorder_level=reorder_level,
            )

    def remove_medication(
        self,
        medication_id: str,
        quantity: int,
    ) -> None:
        if quantity <= 0:
            raise InventoryError(
                "Quantity must be greater than zero."
            )

        item = self._get_item(medication_id)

        if item.is_expired:
            raise InventoryError(
                "Cannot dispense expired medication."
            )

        if quantity > item.quantity:
            raise InventoryError(
                "Insufficient medication stock."
            )

        item.quantity -= quantity

    def restock(
        self,
        medication_id: str,
        quantity: int,
    ) -> None:
        if quantity <= 0:
            raise InventoryError(
                "Restock quantity must be greater than zero."
            )

        item = self._get_item(medication_id)
        item.quantity += quantity

    def get_quantity(
        self,
        medication_id: str,
    ) -> int:
        return self._get_item(medication_id).quantity

    def get_reorder_alerts(self) -> list[InventoryItem]:
        return [
            item
            for item in self.items.values()
            if item.needs_reorder
        ]

    def get_expired_medications(self) -> list[InventoryItem]:
        return [
            item
            for item in self.items.values()
            if item.is_expired
        ]

    def get_expiring_soon(
        self,
        days: int = 30,
    ) -> list[InventoryItem]:
        today = date.today()

        return [
            item
            for item in self.items.values()
            if 0
            <= (item.medication.expiry_date - today).days
            <= days
        ]

    def _get_item(
        self,
        medication_id: str,
    ) -> InventoryItem:
        if medication_id not in self.items:
            raise InventoryError(
                f"Medication {medication_id} not found."
            )

        return self.items[medication_id]