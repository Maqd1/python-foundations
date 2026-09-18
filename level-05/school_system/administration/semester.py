from dataclasses import dataclass, field
from enum import Enum
from typing import List

from school_system.academics.course import Course


class SemesterPeriod(Enum):
    FALL = "FALL"
    SPRING = "SPRING"
    SUMMER = "SUMMER"


class EnrollmentStatus(Enum):
    ACTIVE = "ACTIVE"
    DROPPED = "DROPPED"
    COMPLETED = "COMPLETED"
    WAITLISTED = "WAITLISTED"


@dataclass
class Enrollment:
    student_id: str
    course: Course
    status: EnrollmentStatus = EnrollmentStatus.ACTIVE

    def drop(self) -> None:
        self.status = EnrollmentStatus.DROPPED

    def complete(self) -> None:
        self.status = EnrollmentStatus.COMPLETED

    def __str__(self) -> str:
        return (
            f"{self.student_id} -> "
            f"{self.course.course_code} "
            f"({self.status.value})"
        )


@dataclass
class Semester:
    year: int
    period: SemesterPeriod
    max_credits: int = 15
    courses_offered: List[Course] = field(
        default_factory=list
    )
    enrollments: List[Enrollment] = field(
        default_factory=list
    )

    def add_course(
        self,
        course: Course
    ) -> None:

        if course not in self.courses_offered:
            self.courses_offered.append(course)

    def find_course(
        self,
        course_code: str
    ) -> Course | None:

        for course in self.courses_offered:
            if course.course_code == course_code:
                return course

        return None

    def enroll(
        self,
        student_id: str,
        course_code: str
    ) -> Enrollment:

        course = self.find_course(course_code)

        if course is None:
            raise ValueError(
                f"Course {course_code} is not offered "
                f"in this semester."
            )

        for enrollment in self.enrollments:
            if (
                enrollment.student_id == student_id
                and enrollment.course.course_code
                == course_code
                and enrollment.status
                == EnrollmentStatus.ACTIVE
            ):
                raise ValueError(
                    "Student is already enrolled "
                    "in this course."
                )

        enrollment = Enrollment(
            student_id=student_id,
            course=course
        )

        self.enrollments.append(enrollment)

        return enrollment

    def get_student_enrollments(
        self,
        student_id: str
    ) -> List[Enrollment]:

        return [
            enrollment
            for enrollment in self.enrollments
            if enrollment.student_id == student_id
        ]

    def __str__(self) -> str:
        return (
            f"{self.period.value} {self.year}"
        )