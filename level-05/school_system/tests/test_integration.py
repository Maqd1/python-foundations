from datetime import date

from school_system.users.student import Student
from school_system.academics.course import Course
from school_system.administration.semester import (
    Semester,
    SemesterPeriod,
    EnrollmentStatus,
)
from school_system.services.registration import (
    RegistrationService,
)
from school_system.services.reporting import (
    ReportingService,
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


def test_complete_school_workflow():
    # Create semester
    semester = Semester(
        year=2026,
        period=SemesterPeriod.FALL,
        max_credits=6
    )

    # Create courses
    course1 = Course(
        course_code="CSC301",
        title="Database Systems",
        description="Database fundamentals",
        credits=3,
        department="Computer Science",
        capacity=1
    )

    course2 = Course(
        course_code="CSC401",
        title="Software Engineering",
        description="Software engineering principles",
        credits=3,
        department="Computer Science",
        prerequisites=["CSC301"],
        capacity=1
    )

    semester.add_course(course1)
    semester.add_course(course2)

    # Create students
    student1 = create_student("STU001")
    student2 = create_student("STU002")

    # Registration service
    service = RegistrationService(semester)

    # Student 1 registers for CSC301
    enrollment1 = service.register(
        student1,
        "CSC301"
    )

    assert enrollment1.status == EnrollmentStatus.ACTIVE
    assert "CSC301" in student1.enrolled_courses

    # Student 2 attempts CSC301 but course is full
    enrollment2 = service.register(
        student2,
        "CSC301"
    )

    assert (
        enrollment2.status
        == EnrollmentStatus.WAITLISTED
    )

    # Student 1 completes CSC301
    student1.add_transcript_entry(
        semester="FALL 2026",
        course_code="CSC301",
        course_title="Database Systems",
        credits=3,
        score=75
    )

    # Student 1 can now register for CSC401
    enrollment3 = service.register(
        student1,
        "CSC401"
    )

    assert enrollment3.status == EnrollmentStatus.ACTIVE
    assert "CSC401" in student1.enrolled_courses

    # Student 1 drops CSC301
    service.drop(
        student1,
        "CSC301"
    )

    # Student 2 is promoted from waitlist
    assert "CSC301" in student2.enrolled_courses

    # Add CSC301 grade for student 2
    student2.add_transcript_entry(
        semester="FALL 2026",
        course_code="CSC301",
        course_title="Database Systems",
        credits=3,
        score=65
    )

    # Generate student report
    reporting = ReportingService()

    report = reporting.generate_student_report(
        student1
    )

    assert "STUDENT ACADEMIC REPORT" in report
    assert "CSC301" in report
    assert "Cumulative GPA: 4.00" in report
