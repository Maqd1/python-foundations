from dataclasses import dataclass
from school_system.users.student import Student
from school_system.administration.semester import (
    Semester,
    Enrollment,
    EnrollmentStatus,
)
from school_system.exceptions.school_exceptions import (
    PrerequisiteError,
    EnrollmentError,
    ScheduleConflictError,
    CreditLimitError,
)
from school_system.users.staff import AdminStaff




@dataclass
class RegistrationOverride:
    student_id: str
    course_code: str
    reason: str
    status: str = "PENDING"

    def approve(self) -> None:
        if self.status != "PENDING":
            raise EnrollmentError(
                "Only pending override requests "
                "can be approved."
            )

        self.status = "APPROVED"

    def reject(self) -> None:
        if self.status != "PENDING":
            raise EnrollmentError(
                "Only pending override requests "
                "can be rejected."
            )

        self.status = "REJECTED"

class RegistrationService:

    def __init__(
        self,
        semester: Semester
    ):
        self.semester = semester
        self.students = {}
        self.overrides = []
        self.observers = []

    def add_observer(
        self,
        observer: RegistrationObserver
    ) -> None:
        if observer not in self.observers:
            self.observers.append(observer)
 
    def remove_observer(
        self,
        observer: RegistrationObserver
    ) -> None:
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(
        self,
        event: str,
        student_id: str,
        course_code: str
    ) -> None:
        for observer in self.observers:
            observer.update(
                event,
                student_id,
                course_code
            )

    def check_prerequisites(
        self,
        student: Student,
        course_code: str
    ) -> bool:
    
        course = self.semester.find_course(course_code)
    
        if course is None:
            raise EnrollmentError(
                f"Course {course_code} is not offered "
                f"in this semester."
            )
    
        for prerequisite in course.prerequisites:
        
            if prerequisite not in student.grades:
            
                for override in self.overrides:
                    if (
                        override.student_id
                        == student.student_id
                        and override.course_code
                        == course_code
                        and override.status == "APPROVED"
                    ):
                        break
                else:
                    raise PrerequisiteError(
                        f"Student has not completed "
                        f"prerequisite {prerequisite}."
                    )
    
        return True

    def check_schedule_conflicts(
        self,
        student: Student,
        course_code: str
    ) -> bool:

        new_course = self.semester.find_course(
            course_code
        )

        if new_course is None:
            raise EnrollmentError(
                f"Course {course_code} is not offered "
                f"in this semester."
            )

        if new_course.schedule is None:
            return True

        for enrolled_course_code in student.enrolled_courses:

            enrolled_course = self.semester.find_course(
                enrolled_course_code
            )

            if enrolled_course is None:
                continue

            if enrolled_course.schedule is None:
                continue

            if new_course.schedule.conflicts_with(
                enrolled_course.schedule
            ):
                raise ScheduleConflictError(
                    f"{course_code} conflicts with "
                    f"{enrolled_course_code}."
                )

        return True

    def check_capacity(
        self,
        course_code: str
    ) -> bool:

        course = self.semester.find_course(
            course_code
        )

        if course is None:
            raise EnrollmentError(
                f"Course {course_code} is not offered "
                f"in this semester."
            )

        active_enrollments = 0

        for enrollment in self.semester.enrollments:

            if (
                enrollment.course.course_code
                == course_code
                and enrollment.status
                == EnrollmentStatus.ACTIVE
            ):
                active_enrollments += 1

        return active_enrollments < course.capacity

    def register(
        self,
        student: Student,
        course_code: str
    ) -> Enrollment:

        self.students[student.student_id] = student

        course = self.semester.find_course(course_code)

        if course is None:
            raise EnrollmentError(
                f"Course {course_code} is not offered."
            )

        # Prevent duplicate active/waitlist registration
        for enrollment in self.semester.enrollments:
            if (
                enrollment.student_id
                == student.student_id
                and enrollment.course.course_code
                == course_code
                and enrollment.status
                in (
                    EnrollmentStatus.ACTIVE,
                    EnrollmentStatus.WAITLISTED,
                )
            ):
                raise EnrollmentError(
                    f"Student already has an active "
                    f"registration or waitlist entry "
                    f"for {course_code}."
                )

        # Academic requirements still apply to waitlisting
        self.check_prerequisites(
            student,
            course_code
        )

        # Schedule conflicts still apply
        self.check_schedule_conflicts(
            student,
            course_code
        )

        # If the course is full, place the student
        # on the waitlist without checking credit limit.
        if not self.check_capacity(course_code):
            enrollment = Enrollment(
                student_id=student.student_id,
                course=course,
                status=EnrollmentStatus.WAITLISTED
            )

            self.semester.enrollments.append(
                enrollment
            )

            self.notify_observers(
                "WAITLISTED",
                student.student_id,
                course_code
            )

            return enrollment

        # Only active registration must respect
        # the semester credit limit.
        self.check_credit_limit(
            student,
            course_code
        )

        enrollment = self.semester.enroll(
            student.student_id,
            course_code
        )

        student.enroll_course(course_code)

        self.notify_observers(
            "REGISTERED",
            student.student_id,
            course_code
        )

        return enrollment

    def promote_waitlisted(
        self,
        course_code: str
    ) -> Enrollment | None:

        course = self.semester.find_course(
            course_code
        )

        if course is None:
            return None

        for enrollment in self.semester.enrollments:

            if (
                enrollment.course.course_code
                == course_code
                and enrollment.status
                == EnrollmentStatus.WAITLISTED
            ):

                student = self.students.get(
                    enrollment.student_id
                )

                if student is None:
                    continue

                try:
                    self.check_credit_limit(
                        student,
                        course_code
                    )
                except CreditLimitError:
                    continue

                enrollment.status = (
                    EnrollmentStatus.ACTIVE
                )

                student.enroll_course(
                    course_code
                )

                self.notify_observers(
                    "PROMOTED_FROM_WAITLIST",
                    student.student_id,
                    course_code
                )

                return enrollment

        return None

    def drop(
        self,
        student: Student,
        course_code: str
    ) -> None:

        if course_code not in student.enrolled_courses:
            raise EnrollmentError(
                f"Student is not registered "
                f"for {course_code}."
            )

        student.drop_course(course_code)

        for enrollment in self.semester.enrollments:
        
            if (
                enrollment.student_id
                == student.student_id
                and enrollment.course.course_code
                == course_code
                and enrollment.status
                == EnrollmentStatus.ACTIVE
            ):
                enrollment.drop()

                self.notify_observers(
                    "DROPPED",
                    student.student_id,
                    course_code
                )

                self.promote_waitlisted(
                    course_code
                )

                return

    def cancel_waitlist(
        self,
        student: Student,
        course_code: str
    ) -> None:

        for enrollment in self.semester.enrollments:

            if (
                enrollment.student_id
                == student.student_id
                and enrollment.course.course_code
                == course_code
                and enrollment.status
                == EnrollmentStatus.WAITLISTED
            ):
                enrollment.drop()
                return

        raise EnrollmentError(
            f"Student is not waitlisted "
            f"for {course_code}."
        )

    def request_override(
        self,
        student: Student,
        course_code: str,
        reason: str
    ) -> RegistrationOverride:

        course = self.semester.find_course(
            course_code
        )

        if course is None:
            raise EnrollmentError(
                f"Course {course_code} is not offered "
                f"in this semester."
            )

        override = RegistrationOverride(
            student_id=student.student_id,
            course_code=course_code,
            reason=reason
        )

        self.overrides.append(override)

        return override

    def approve_override(
        self,
        override: RegistrationOverride,
        approver: AdminStaff
    ) -> None:

        if not approver.can_access(2):
            raise EnrollmentError(
                "Staff member does not have permission "
                "to approve registration overrides."
            )

        override.approve()

    def reject_override(
        self,
        override: RegistrationOverride,
        approver: AdminStaff
    ) -> None:

        if not approver.can_access(2):
            raise EnrollmentError(
                "Staff member does not have permission "
                "to reject registration overrides."
            )

        override.reject()

    def check_credit_limit(
        self,
        student: Student,
        course_code: str
    ) -> bool:

        course = self.semester.find_course(
            course_code
        )

        if course is None:
            raise EnrollmentError(
                f"Course {course_code} is not offered "
                f"in this semester."
            )

        current_credits = 0

        for enrollment in self.semester.enrollments:

            if (
                enrollment.student_id
                == student.student_id
                and enrollment.status
                == EnrollmentStatus.ACTIVE
            ):
                current_credits += (
                    enrollment.course.credits
                )

        total_credits = (
            current_credits + course.credits
        )

        if total_credits > self.semester.max_credits:
            raise CreditLimitError(
                f"Registering for {course_code} would "
                f"exceed the semester credit limit of "
                f"{self.semester.max_credits} credits."
            )

        return True
