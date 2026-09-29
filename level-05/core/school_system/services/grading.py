from abc import ABC, abstractmethod
from typing import Iterable

from core.school_system.academics.grade import Grade


class GradingStrategy(ABC):

    @abstractmethod
    def calculate_grade_point(self, grade: Grade) -> float:
        pass


class FourPointGradingStrategy(GradingStrategy):

    def calculate_grade_point(self, grade: Grade) -> float:
        return grade.grade_point(scale=4.0)


class FivePointGradingStrategy(GradingStrategy):

    def calculate_grade_point(self, grade: Grade) -> float:
        return grade.grade_point(scale=5.0)


class PercentageGradingStrategy(GradingStrategy):

    def calculate_grade_point(self, grade: Grade) -> float:
        return grade.score


class GradingService:

    def __init__(
        self,
        strategy: GradingStrategy | None = None
    ) -> None:
        self.strategy = (
            strategy
            if strategy is not None
            else FourPointGradingStrategy()
        )

    def calculate_grade_point(
        self,
        grade: Grade
    ) -> float:
        return self.strategy.calculate_grade_point(grade)

    def calculate_average(
        self,
        grades: Iterable[Grade]
    ) -> float:

        grades = list(grades)

        if not grades:
            return 0.0

        total = sum(
            self.calculate_grade_point(grade)
            for grade in grades
        )

        return total / len(grades)