from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List

from school_system.users.person import Person
from school_system.academics.grade import Grade


@dataclass
class TranscriptEntry:
    semester: str
    course_code: str
    course_title: str
    credits: int
    grade: Grade

    @property
    def grade_point(self) -> float:
        return self.grade.grade_point()

    def __str__(self) -> str:
        return (
            f"{self.course_code} - "
            f"{self.course_title}: "
            f"{self.grade.letter_grade} "
            f"({self.grade_point})"
        )


@dataclass
class Transcript:
    student_id: str
    entries: List[TranscriptEntry] = field(
        default_factory=list
    )

    def add_entry(
        self,
        entry: TranscriptEntry
    ) -> None:

        self.entries.append(entry)

    @property
    def total_credits(self) -> int:
        return sum(
            entry.credits
            for entry in self.entries
        )

    @property
    def cumulative_gpa(self) -> float:

        if not self.entries:
            return 0.0

        total_quality_points = sum(
            entry.grade_point * entry.credits
            for entry in self.entries
        )

        return (
            total_quality_points
            / self.total_credits
        )

    def get_semester_entries(
        self,
        semester: str
    ) -> List[TranscriptEntry]:

        return [
            entry
            for entry in self.entries
            if entry.semester == semester
        ]

    def __str__(self) -> str:
        return (
            f"Transcript for {self.student_id} | "
            f"GPA: {self.cumulative_gpa:.2f}"
        )


@dataclass
class Student(Person):
    student_id: str
    program: str
    level: int
    status: str = "ACTIVE"

    enrolled_courses: List[str] = field(
        default_factory=list
    )

    grades: Dict[str, float] = field(
        default_factory=dict
    )

    attendance: Dict[str, float] = field(
        default_factory=dict
    )

    transcript: Transcript = field(
        init=False
    )

    def __post_init__(self):
        self.transcript = Transcript(
            student_id=self.student_id
        )

    def get_role(self) -> str:
        return "STUDENT"

    def enroll_course(
        self,
        course_code: str
    ) -> None:

        if course_code not in self.enrolled_courses:
            self.enrolled_courses.append(
                course_code
            )

    def drop_course(
        self,
        course_code: str
    ) -> None:

        if course_code in self.enrolled_courses:
            self.enrolled_courses.remove(
                course_code
            )

    def add_grade(
        self,
        course_code: str,
        score: float
    ) -> None:

        if not 0 <= score <= 100:
            raise ValueError(
                "Score must be between 0 and 100."
            )

        self.grades[course_code] = score

    def record_attendance(
        self,
        course_code: str,
        percentage: float
    ) -> None:

        if not 0 <= percentage <= 100:
            raise ValueError(
                "Attendance must be between 0 and 100."
            )

        self.attendance[course_code] = percentage

    def add_transcript_entry(
        self,
        semester: str,
        course_code: str,
        course_title: str,
        credits: int,
        score: float
    ) -> None:
        grade = Grade(
            student_id=self.student_id,
            course_code=course_code,
            score=score
        )
    
        self.grades[course_code] = score
    
        entry = TranscriptEntry(
            semester=semester,
            course_code=course_code,
            course_title=course_title,
            credits=credits,
            grade=grade
        )
    
        self.transcript.add_entry(entry)

    def get_transcript(self) -> Transcript:
        return self.transcript

    def __str__(self) -> str:
        return (
            f"{self.name} "
            f"({self.student_id})"
        )