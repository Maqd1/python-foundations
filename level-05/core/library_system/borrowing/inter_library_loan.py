from dataclasses import dataclass
from datetime import datetime


@dataclass
class InterLibraryLoan:
    request_id: str
    member_id: str
    isbn: str
    source_library: str
    status: str = "REQUESTED"
    requested_at: datetime | None = None

    def __post_init__(self):
        if self.requested_at is None:
            self.requested_at = datetime.now()

    def approve(self) -> None:
        if self.status != "REQUESTED":
            raise ValueError("Only requested loans can be approved.")
        self.status = "APPROVED"

    def receive(self) -> None:
        if self.status != "APPROVED":
            raise ValueError("Only approved loans can be received.")
        self.status = "RECEIVED"

    def complete(self) -> None:
        if self.status != "RECEIVED":
            raise ValueError("Only received loans can be completed.")
        self.status = "COMPLETED"

    def cancel(self) -> None:
        if self.status == "COMPLETED":
            raise ValueError("Completed loans cannot be cancelled.")
        self.status = "CANCELLED"

    @property
    def is_active(self) -> bool:
        return self.status in {"REQUESTED", "APPROVED", "RECEIVED"}
