from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date


@dataclass
class Person(ABC):
    name: str
    date_of_birth: date
    contact: str
    address: str

    @abstractmethod
    def get_role(self) -> str:
        """Return the person's role in the school."""
        pass

    def display_info(self) -> None:
        print(f"Name: {self.name}")
        print(f"Date of Birth: {self.date_of_birth}")
        print(f"Contact: {self.contact}")
        print(f"Address: {self.address}")
        print(f"Role: {self.get_role()}")

    def __str__(self) -> str:
        return f"{self.name} ({self.get_role()})"