from dataclasses import dataclass, field
from datetime import date

from hospital_system.patients.medical_record import LabResult


@dataclass
class LabTest:
    test_id: str
    patient_id: str
    test_name: str
    requested_by: str
    requested_date: date
    status: str = "REQUESTED"
    result: LabResult | None = None

    def start(self) -> None:
        self.status = "IN_PROGRESS"

    def complete(self, result: LabResult) -> None:
        self.result = result
        self.status = "COMPLETED"

    def cancel(self) -> None:
        self.status = "CANCELLED"

    @property
    def is_completed(self) -> bool:
        return self.status == "COMPLETED"


@dataclass
class Laboratory:
    tests: list[LabTest] = field(default_factory=list)

    def request_test(self, test: LabTest) -> None:
        self.tests.append(test)

    def start_test(self, test_id: str) -> None:
        test = self._get_test(test_id)
        test.start()

    def complete_test(
        self,
        test_id: str,
        result: LabResult,
    ) -> None:
        test = self._get_test(test_id)
        test.complete(result)

    def cancel_test(self, test_id: str) -> None:
        test = self._get_test(test_id)
        test.cancel()

    def get_pending_tests(self) -> list[LabTest]:
        return [
            test
            for test in self.tests
            if test.status in {"REQUESTED", "IN_PROGRESS"}
        ]

    def get_patient_tests(
        self,
        patient_id: str,
    ) -> list[LabTest]:
        return [
            test
            for test in self.tests
            if test.patient_id == patient_id
        ]

    def _get_test(self, test_id: str) -> LabTest:
        for test in self.tests:
            if test.test_id == test_id:
                return test

        raise ValueError(
            f"Lab test {test_id} not found."
        )