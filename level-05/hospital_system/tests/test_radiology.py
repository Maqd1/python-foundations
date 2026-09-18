from datetime import date

from hospital_system.services.radiology import (
    RadiologyDepartment,
    RadiologyScan,
)


def make_scan(scan_id="RAD001", patient_id="P001"):
    return RadiologyScan(
        scan_id=scan_id,
        patient_id=patient_id,
        scan_type="X-Ray",
        body_part="Chest",
        requested_by="D001",
        requested_date=date.today(),
    )


def test_radiology_scan_creation():
    scan = make_scan()

    assert scan.scan_id == "RAD001"
    assert scan.patient_id == "P001"
    assert scan.status == "REQUESTED"
    assert not scan.is_completed


def test_start_scan():
    scan = make_scan()

    scan.start()

    assert scan.status == "IN_PROGRESS"


def test_complete_scan():
    scan = make_scan()

    scan.complete(
        findings="No abnormality detected.",
        report="Chest X-Ray is normal.",
    )

    assert scan.status == "COMPLETED"
    assert scan.is_completed
    assert scan.findings == "No abnormality detected."
    assert scan.report == "Chest X-Ray is normal."


def test_cancel_scan():
    scan = make_scan()

    scan.cancel()

    assert scan.status == "CANCELLED"


def test_request_scan():
    department = RadiologyDepartment()
    scan = make_scan()

    department.request_scan(scan)

    assert len(department.scans) == 1
    assert department.scans[0] == scan


def test_start_scan_through_department():
    department = RadiologyDepartment()
    scan = make_scan()

    department.request_scan(scan)
    department.start_scan("RAD001")

    assert scan.status == "IN_PROGRESS"


def test_complete_scan_through_department():
    department = RadiologyDepartment()
    scan = make_scan()

    department.request_scan(scan)

    department.complete_scan(
        "RAD001",
        "Clear lungs.",
        "No acute findings.",
    )

    assert scan.status == "COMPLETED"
    assert scan.findings == "Clear lungs."


def test_get_pending_scans():
    department = RadiologyDepartment()

    scan1 = make_scan("RAD002", "P002")
    scan2 = make_scan("RAD003", "P003")

    department.request_scan(scan1)
    department.request_scan(scan2)

    department.start_scan("RAD003")

    pending = department.get_pending_scans()

    assert len(pending) == 2


def test_get_patient_scans():
    department = RadiologyDepartment()

    scan1 = make_scan("RAD004", "P004")
    scan2 = make_scan("RAD005", "P005")

    department.request_scan(scan1)
    department.request_scan(scan2)

    scans = department.get_patient_scans("P004")

    assert len(scans) == 1
    assert scans[0].scan_id == "RAD004"


def test_missing_scan_raises_error():
    department = RadiologyDepartment()

    try:
        department.start_scan("DOES_NOT_EXIST")
        assert False
    except ValueError:
        assert True
