class SchoolError(Exception):
    """Base exception for the school management system."""


class PersonError(SchoolError):
    """Base exception for person-related errors."""


class InvalidPersonError(PersonError):
    """Raised when person information is invalid."""


class StudentError(PersonError):
    """Base exception for student-related errors."""


class StudentNotFoundError(StudentError):
    """Raised when a student cannot be found."""


class CourseError(SchoolError):
    """Base exception for course-related errors."""


class CourseNotFoundError(CourseError):
    """Raised when a course cannot be found."""


class RegistrationError(SchoolError):
    """Base exception for registration-related errors."""


class PrerequisiteError(RegistrationError):
    """Raised when prerequisites have not been completed."""


class ScheduleConflictError(RegistrationError):
    """Raised when courses have conflicting schedules."""


class EnrollmentError(RegistrationError):
    """Raised when enrollment fails."""


class CreditLimitError(RegistrationError):
    """Raised when a student exceeds the semester credit limit."""


class GradeError(SchoolError):
    """Base exception for grade-related errors."""


class InvalidGradeError(GradeError):
    """Raised when a grade or score is invalid."""


class AttendanceError(SchoolError):
    """Base exception for attendance-related errors."""


class InvalidAttendanceError(AttendanceError):
    """Raised when attendance information is invalid."""


class SemesterError(SchoolError):
    """Base exception for semester-related errors."""


class FeeError(SchoolError):
    """Base exception for fee-related errors."""