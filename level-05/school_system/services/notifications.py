from abc import ABC, abstractmethod


class RegistrationObserver(ABC):

    @abstractmethod
    def update(
        self,
        event: str,
        student_id: str,
        course_code: str
    ) -> None:
        pass


class StudentNotification(RegistrationObserver):

    def update(
        self,
        event: str,
        student_id: str,
        course_code: str
    ) -> None:
        print(
            f"[NOTIFICATION] "
            f"{student_id}: {event} "
            f"{course_code}"
        )
