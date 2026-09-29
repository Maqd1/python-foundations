from abc import ABC, abstractmethod


class FineStrategy(ABC):
    @abstractmethod
    def calculate(self, overdue_days: int) -> float:
        pass


class StandardFineStrategy(FineStrategy):
    def __init__(self, daily_rate: float = 1.0):
        if daily_rate < 0:
            raise ValueError("Daily rate cannot be negative.")
        self.daily_rate = daily_rate

    def calculate(self, overdue_days: int) -> float:
        return max(0, overdue_days) * self.daily_rate


class StudentFineStrategy(StandardFineStrategy):
    def __init__(self):
        super().__init__(daily_rate=0.50)


class FacultyFineStrategy(StandardFineStrategy):
    def __init__(self):
        super().__init__(daily_rate=0.25)


class ExemptFineStrategy(FineStrategy):
    def calculate(self, overdue_days: int) -> float:
        return 0.0
