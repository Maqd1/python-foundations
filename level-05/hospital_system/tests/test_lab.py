from datetime import date

from hospital_system.patients.medical_record import LabResult
from hospital_system.services.lab import LabTest, Laboratory


def test_lab_test_creation():
    test = LabTest(
        test_id="LAB001",
        patient_id="P001",
        test_name="Full Blood Count",
        requested_by="D001",
        requested_date=date.today(),
    )

    assert test.test_id == "LAB001"
    assert test.status == "REQUESTED"
    assert not test.is_completed


def test_start_lab_test():
    test = LabTest(
        test_id="LAB002",
        patient_id="P002",
        test_name="Blood Glucose",
        requested_by="D001",
        requested_date=date.today(),
    )

    test.start()

    assert test.status == "IN_PROGRESS"


def test_complete_lab_test():
    test = LabTest(
        test_id="LAB003",
        patient_id="P003",
        test_name="Blood Glucose",
        requested_by="D001",
        requested_date=date.today(),
    )

    result = LabResult(
        test_name="Blood Glucose",
        result="5.2",
        reference_range="3.9-5.5",
        test_date=date.today(),
        unit="mmol/L",
    )

    test.complete(result)

    assert test.status == "COMPLETED"
    assert test.is_completed
    assert test.result == result


def test_cancel_lab_test():
    test = LabTest(
        test_id="LAB004",
        patient_id="P004",
        test_name="X",
        requested_by="D001",
        requested_date=date.today(),
    )

    test.cancel()

    assert test.status == "CANCELLED"


def test_laboratory_requests_test():
    laboratory = Laboratory()

    test = LabTest(
        test_id="LAB005",
        patient_id="P005",
        test_name="Malaria Test",
        requested_by="D001",
        requested_date=date.today(),
    )

    laboratory.request_test(test)

    assert len(laboratory.tests) == 1
    assert laboratory.tests[0] == test


def test_laboratory_starts_test():
    laboratory = Laboratory()

    test = LabTest(
        test_id="LAB006",
        patient_id="P006",
        test_name="Urinalysis",
        requested_by="D001",
        requested_date=date.today(),
    )

    laboratory.request_test(test)
    laboratory.start_test("LAB006")

    assert test.status == "IN_PROGRESS"


def test_laboratory_completes_test():
    laboratory = Laboratory()

    test = LabTest(
        test_id="LAB007",
        patient_id="P007",
        test_name="Full Blood Count",
        requested_by="D001",
        requested_date=date.today(),
    )

    result = LabResult(
        test_name="Full Blood Count",
        result="Normal",
        reference_range="Normal",
        test_date=date.today(),
    )

    laboratory.request_test(test)
    laboratory.complete_test("LAB007", result)

    assert test.status == "COMPLETED"
    assert test.result == result


def test_get_pending_tests():
    laboratory = Laboratory()

    test1 = LabTest(
        test_id="LAB008",
        patient_id="P008",
        test_name="Test A",
        requested_by="D001",
        requested_date=date.today(),
    )

    test2 = LabTest(
        test_id="LAB009",
        patient_id="P009",
        test_name="Test B",
        requested_by="D001",
        requested_date=date.today(),
    )

    laboratory.request_test(test1)
    laboratory.request_test(test2)
    laboratory.start_test("LAB009")

    pending = laboratory.get_pending_tests()

    assert len(pending) == 2


def test_get_patient_tests():
    laboratory = Laboratory()

    test1 = LabTest(
        test_id="LAB010",
        patient_id="P010",
        test_name="Malaria Test",
        requested_by="D001",
        requested_date=date.today(),
    )

    test2 = LabTest(
        test_id="LAB011",
        patient_id="P011",
        test_name="Blood Test",
        requested_by="D001",
        requested_date=date.today(),
    )

    laboratory.request_test(test1)
    laboratory.request_test(test2)

    patient_tests = laboratory.get_patient_tests("P010")

    assert len(patient_tests) == 1
    assert patient_tests[0].test_id == "LAB010"


def test_missing_lab_test_raises_error():
    laboratory = Laboratory()

    try:
        laboratory.start_test("DOES_NOT_EXIST")
        assert False
    except ValueError:
        assert True
