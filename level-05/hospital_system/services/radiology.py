from dataclasses import dataclass, field
from datetime import date


@dataclass
class RadiologyScan:
    scan_id: str
    patient_id: str
    scan_type: str
    body_part: str
    requested_by: str
    requested_date: date
    status: str = "REQUESTED"
    findings: str = ""
    report: str = ""

    def start(self) -> None:
        self.status = "IN_PROGRESS"

    def complete(
        self,
        findings: str,
        report: str,
    ) -> None:
        self.findings = findings
        self.report = report
        self.status = "COMPLETED"

    def cancel(self) -> None:
        self.status = "CANCELLED"

    @property
    def is_completed(self) -> bool:
        return self.status == "COMPLETED"


@dataclass
class RadiologyDepartment:
    scans: list[RadiologyScan] = field(
        default_factory=list
    )

    def request_scan(
        self,
        scan: RadiologyScan,
    ) -> None:
        self.scans.append(scan)

    def start_scan(
        self,
        scan_id: str,
    ) -> None:
        scan = self._get_scan(scan_id)
        scan.start()

    def complete_scan(
        self,
        scan_id: str,
        findings: str,
        report: str,
    ) -> None:
        scan = self._get_scan(scan_id)
        scan.complete(findings, report)

    def cancel_scan(
        self,
        scan_id: str,
    ) -> None:
        scan = self._get_scan(scan_id)
        scan.cancel()

    def get_pending_scans(self) -> list[RadiologyScan]:
        return [
            scan
            for scan in self.scans
            if scan.status in {
                "REQUESTED",
                "IN_PROGRESS",
            }
        ]

    def get_patient_scans(
        self,
        patient_id: str,
    ) -> list[RadiologyScan]:
        return [
            scan
            for scan in self.scans
            if scan.patient_id == patient_id
        ]

    def _get_scan(
        self,
        scan_id: str,
    ) -> RadiologyScan:
        for scan in self.scans:
            if scan.scan_id == scan_id:
                return scan

        raise ValueError(
            f"Radiology scan {scan_id} not found."
        )