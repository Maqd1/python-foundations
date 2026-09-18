from datetime import date

from school_system.users.student import Student
from school_system.academics.course import Course
from school_system.database.repository import (
    StudentRepository,
    CourseRepository,
)


def create_student(
    student_id: str
) -> Student:
    return Student(
        name="Test Student",
        date_of_birth=date(2000, 1, 1),
        contact="08000000000",
        address="Lagos",
        student_id=student_id,
        program="Computer Science",
        level=400
    )


def create_course(
    course_code: str
) -> Course:
    return Course(
        course_code=course_code,
        title="Test Course",
        description="Test description",
        credits=3,
        department="Computer Science"
    )


def test_student_repository_add_and_get():
    repository = StudentRepository()
    student = create_student("STU001")

    repository.add(student)

    assert repository.get("STU001") is student


def test_student_repository_remove():
    repository = StudentRepository()
    student = create_student("STU001")

    repository.add(student)
    repository.remove("STU001")

    assert repository.get("STU001") is None


def test_course_repository_add_and_get():
    repository = CourseRepository()
    course = create_course("CSC301")

    repository.add(course)

    assert repository.get("CSC301") is course


def test_course_repository_remove():
    repository = CourseRepository()
    course = create_course("CSC301")

    repository.add(course)
    repository.remove("CSC301")

    assert repository.get("CSC301") is None
