from typing import Dict

from school_system.users.student import Student
from school_system.academics.course import Course


class StudentRepository:

    def __init__(self):
        self.students: Dict[str, Student] = {}

    def add(
        self,
        student: Student
    ) -> None:
        self.students[student.student_id] = student

    def get(
        self,
        student_id: str
    ) -> Student | None:
        return self.students.get(student_id)

    def remove(
        self,
        student_id: str
    ) -> None:
        self.students.pop(student_id, None)

    def all(self) -> list[Student]:
        return list(self.students.values())


class CourseRepository:

    def __init__(self):
        self.courses: Dict[str, Course] = {}

    def add(
        self,
        course: Course
    ) -> None:
        self.courses[course.course_code] = course

    def get(
        self,
        course_code: str
    ) -> Course | None:
        return self.courses.get(course_code)

    def remove(
        self,
        course_code: str
    ) -> None:
        self.courses.pop(course_code, None)

    def all(self) -> list[Course]:
        return list(self.courses.values())
