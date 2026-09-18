from datetime import date, time

import pytest

from school_system.users.student import Student
from school_system.users.staff import AdminStaff
from school_system.academics.course import Course
from school_system.academics.schedule import Schedule
from school_system.administration.semester import (
    Semester,
    SemesterPeriod,
    EnrollmentStatus,
)
from school_system.services.registration import (
    RegistrationService,
)
from school_system.exceptions.school_exceptions import (
    PrerequisiteError,
    ScheduleConflictError,
    CreditLimitError,
    EnrollmentError,
)


def create_student(
    student_id: str
) -> Student:
    return Student(
        name=f"Student {student_id}",
        date_of_birth=date(2000, 1, 1),
        contact="08000000000",
        address="Lagos",
        student_id=student_id,
        program="Computer Science",
        level=400
    )


def create_semester(
    max_credits: int = 15
) -> Semester:
    return Semester(
        year=2026,
        period=SemesterPeriod.FALL,
        max_credits=max_credits
    )


def create_course(
    code: str,
    credits: int = 3,
    capacity: int = 30,
    prerequisites=None,
    schedule=None
) -> Course:
    return Course(
        course_code=code,
        title=f"Course {code}",
        description="Test course",
        credits=credits,
        department="Computer Science",
        capacity=capacity,
        prerequisites=prerequisites or [],
        schedule=schedule
    )


def test_successful_registration():
    semester = create_semester()
    course = create_course("CSC301")

    semester.add_course(course)

    student = create_student("STU001")
    service = RegistrationService(semester)

    enrollment = service.register(
        student,
        "CSC301"
    )

    assert enrollment.status == EnrollmentStatus.ACTIVE
    assert "CSC301" in student.enrolled_courses


def test_prerequisite_is_required():
    semester = create_semester()

    course = create_course(
        "CSC401",
        prerequisites=["CSC301"]
    )

    semester.add_course(course)

    student = create_student("STU001")
    service = RegistrationService(semester)

    with pytest.raises(PrerequisiteError):
        service.register(
            student,
            "CSC401"
        )


def test_completed_prerequisite_allows_registration():
    semester = create_semester()

    prerequisite = create_course("CSC301")
    advanced = create_course(
        "CSC401",
        prerequisites=["CSC301"]
    )

    semester.add_course(prerequisite)
    semester.add_course(advanced)

    student = create_student("STU001")

    student.add_grade(
        "CSC301",
        75
    )

    service = RegistrationService(semester)

    enrollment = service.register(
        student,
        "CSC401"
    )

    assert enrollment.status == EnrollmentStatus.ACTIVE


def test_schedule_conflict_is_rejected():
    semester = create_semester()

    first = create_course(
        "CSC301",
        schedule=Schedule(
            day="Monday",
            start_time=time(9, 0),
            end_time=time(11, 0),
            room="Room A",
            instructor="Teacher A"
        )
    )

    second = create_course(
        "CSC401",
        schedule=Schedule(
            day="Monday",
            start_time=time(10, 0),
            end_time=time(12, 0),
            room="Room B",
            instructor="Teacher B"
        )
    )

    semester.add_course(first)
    semester.add_course(second)

    student = create_student("STU001")
    service = RegistrationService(semester)

    service.register(
        student,
        "CSC301"
    )

    with pytest.raises(ScheduleConflictError):
        service.register(
            student,
            "CSC401"
        )


def test_credit_limit_is_enforced():
    semester = create_semester(
        max_credits=6
    )

    course1 = create_course("CSC301")
    course2 = create_course("CSC401")
    course3 = create_course("CSC501")

    semester.add_course(course1)
    semester.add_course(course2)
    semester.add_course(course3)

    student = create_student("STU001")
    service = RegistrationService(semester)

    service.register(student, "CSC301")
    service.register(student, "CSC401")

    with pytest.raises(CreditLimitError):
        service.register(
            student,
            "CSC501"
        )


def test_full_course_creates_waitlist():
    semester = create_semester()

    course = create_course(
        "CSC501",
        capacity=1
    )

    semester.add_course(course)

    student1 = create_student("STU001")
    student2 = create_student("STU002")

    service = RegistrationService(semester)

    service.register(
        student1,
        "CSC501"
    )

    enrollment = service.register(
        student2,
        "CSC501"
    )

    assert (
        enrollment.status
        == EnrollmentStatus.WAITLISTED
    )


def test_waitlisted_student_is_promoted():
    semester = create_semester()

    course = create_course(
        "CSC501",
        capacity=1
    )

    semester.add_course(course)

    student1 = create_student("STU001")
    student2 = create_student("STU002")

    service = RegistrationService(semester)

    service.register(
        student1,
        "CSC501"
    )

    service.register(
        student2,
        "CSC501"
    )

    service.drop(
        student1,
        "CSC501"
    )

    assert (
        "CSC501"
        in student2.enrolled_courses
    )


def test_duplicate_registration_is_rejected():
    semester = create_semester()

    course = create_course("CSC301")
    semester.add_course(course)

    student = create_student("STU001")
    service = RegistrationService(semester)

    service.register(
        student,
        "CSC301"
    )

    with pytest.raises(EnrollmentError):
        service.register(
            student,
            "CSC301"
        )


def test_override_allows_missing_prerequisite():
    semester = create_semester()

    course = create_course(
        "CSC401",
        prerequisites=["CSC301"]
    )

    semester.add_course(course)

    student = create_student("STU001")

    service = RegistrationService(semester)

    override = service.request_override(
        student,
        "CSC401",
        "Approved academic exception"
    )

    admin = AdminStaff(
        name="Admin",
        date_of_birth=date(1980, 1, 1),
        contact="08000000000",
        address="Lagos",
        employee_id="ADM001",
        role="Registrar",
        access_level=2
    )

    service.approve_override(
        override,
        admin
    )

    enrollment = service.register(
        student,
        "CSC401"
    )

    assert (
        enrollment.status
        == EnrollmentStatus.ACTIVE
    )
