from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class EmergencyAlert:
    alert_id: str
    patient_id: str
    emergency_type: str
    severity: int
    message: str
    created_at: datetime = field(
        default_factory=datetime.now
    )
    resolved: bool = False

    def __post_init__(self):
        if not 1 <= self.severity <= 5:
            raise ValueError(
                "Severity must be between 1 and 5."
            )

    def resolve(self) -> None:
        self.resolved = True


class EmergencyObserver(ABC):

    @abstractmethod
    def update(
        self,
        alert: EmergencyAlert,
    ) -> None:
        pass


class StaffNotifier(EmergencyObserver):

    def __init__(self):
        self.notifications: list[str] = []

    def update(
        self,
        alert: EmergencyAlert,
    ) -> None:
        notification = (
            f"Emergency {alert.alert_id}: "
            f"Patient {alert.patient_id} | "
            f"{alert.emergency_type} | "
            f"Severity {alert.severity}"
        )

        self.notifications.append(notification)


class ResourceAllocator(EmergencyObserver):

    def __init__(self):
        self.resources: dict[str, list[str]] = {}

    def update(
        self,
        alert: EmergencyAlert,
    ) -> None:
        resources = []

        if alert.severity <= 2:
            resources.extend([
                "Emergency Doctor",
                "Emergency Nurse",
                "Resuscitation Equipment",
            ])
        else:
            resources.extend([
                "Emergency Nurse",
                "Monitoring Equipment",
            ])

        self.resources[alert.alert_id] = resources


class PatientTracker(EmergencyObserver):

    def __init__(self):
        self.active_patients: set[str] = set()

    def update(
        self,
        alert: EmergencyAlert,
    ) -> None:
        self.active_patients.add(alert.patient_id)

    def remove_patient(
        self,
        patient_id: str,
    ) -> None:
        self.active_patients.discard(patient_id)


class EmergencyResponseSystem:

    def __init__(self):
        self.observers: list[EmergencyObserver] = []
        self.alerts: list[EmergencyAlert] = []

    def subscribe(
        self,
        observer: EmergencyObserver,
    ) -> None:
        if observer not in self.observers:
            self.observers.append(observer)

    def unsubscribe(
        self,
        observer: EmergencyObserver,
    ) -> None:
        if observer in self.observers:
            self.observers.remove(observer)

    def create_alert(
        self,
        alert: EmergencyAlert,
    ) -> None:
        self.alerts.append(alert)

        for observer in self.observers:
            observer.update(alert)

    def resolve_alert(
        self,
        alert_id: str,
    ) -> None:
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.resolve()
                return

        raise ValueError(
            f"Emergency alert {alert_id} not found."
        )

    def get_active_alerts(
        self,
    ) -> list[EmergencyAlert]:
        return [
            alert
            for alert in self.alerts
            if not alert.resolved
        ]


@dataclass
class EmergencyService:

    def __init__(
        self,
        response_system: EmergencyResponseSystem,
    ):
        self.response_system = response_system
        self.cases: dict[str, EmergencyAlert] = {}

    def register_emergency(
        self,
        alert: EmergencyAlert,
    ) -> None:
        if alert.alert_id in self.cases:
            raise ValueError(
                f"Emergency {alert.alert_id} already exists."
            )

        self.cases[alert.alert_id] = alert
        self.response_system.create_alert(alert)

    def resolve_emergency(
        self,
        alert_id: str,
    ) -> None:
        if alert_id not in self.cases:
            raise ValueError(
                f"Emergency {alert_id} not found."
            )

        self.response_system.resolve_alert(alert_id)

    def get_emergency(
        self,
        alert_id: str,
    ) -> EmergencyAlert:
        if alert_id not in self.cases:
            raise ValueError(
                f"Emergency {alert_id} not found."
            )

        return self.cases[alert_id]

    def get_active_emergencies(
        self,
    ) -> list[EmergencyAlert]:
        return self.response_system.get_active_alerts()

    def subscribe(
        self,
        observer: EmergencyObserver,
    ) -> None:
        if observer not in self.observers:
            self.observers.append(observer)

    def unsubscribe(
        self,
        observer: EmergencyObserver,
    ) -> None:
        if observer in self.observers:
            self.observers.remove(observer)

    def create_alert(
        self,
        alert: EmergencyAlert,
    ) -> None:
        self.alerts.append(alert)

        for observer in self.observers:
            observer.update(alert)

    def resolve_alert(
        self,
        alert_id: str,
    ) -> None:
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.resolve()
                return

        raise ValueError(
            f"Emergency alert {alert_id} not found."
        )

    def get_active_alerts(
        self,
    ) -> list[EmergencyAlert]:
        return [
            alert
            for alert in self.alerts
            if not alert.resolved
        ]