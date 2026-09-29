from dataclasses import dataclass


@dataclass
class Grade:
    student_id: str
    course_code: str
    score: float

    def __post_init__(self):
        if not 0 <= self.score <= 100:
            raise ValueError(
                "Score must be between 0 and 100."
            )

    @property
    def letter_grade(self) -> str:
        if self.score >= 70:
            return "A"
        elif self.score >= 60:
            return "B"
        elif self.score >= 50:
            return "C"
        elif self.score >= 45:
            return "D"
        elif self.score >= 40:
            return "E"
        else:
            return "F"

    def grade_point(
        self,
        scale: float = 4.0
    ) -> float:

        if scale == 4.0:
            points = {
                "A": 4.0,
                "B": 3.0,
                "C": 2.0,
                "D": 1.0,
                "E": 0.0,
                "F": 0.0,
            }

            return points[self.letter_grade]

        if scale == 5.0:
            points = {
                "A": 5.0,
                "B": 4.0,
                "C": 3.0,
                "D": 2.0,
                "E": 1.0,
                "F": 0.0,
            }

            return points[self.letter_grade]

        raise ValueError(
            "Unsupported grading scale."
        )

    def __str__(self) -> str:
        return (
            f"{self.course_code}: "
            f"{self.score}% "
            f"({self.letter_grade})"
        )