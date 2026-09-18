from hospital_system.services.emergency import (
    EmergencyAlert,
    EmergencyResponseSystem,
    EmergencyService,
    PatientTracker,
    ResourceAllocator,
    StaffNotifier,
)

def test_emergency_alert_creation():
    alert = EmergencyAlert(
        alert_id="E001",
        patient_id="P001",
        emergency_type="Cardiac Arrest",
        severity=1,
        message="Patient requires immediate intervention.",
    )

    assert alert.alert_id == "E001"
    assert alert.patient_id == "P001"
    assert alert.severity == 1
    assert not alert.resolved


def test_invalid_emergency_severity():
    try:
        EmergencyAlert(
            alert_id="E002",
            patient_id="P002",
            emergency_type="Accident",
            severity=6,
            message="Critical injury.",
        )
        assert False
    except ValueError:
        assert True


def test_alert_resolution():
    alert = EmergencyAlert(
        alert_id="E003",
        patient_id="P003",
        emergency_type="Severe Bleeding",
        severity=2,
        message="Immediate treatment required.",
    )

    alert.resolve()

    assert alert.resolved


def test_staff_notifier_receives_alert():
    notifier = StaffNotifier()

    alert = EmergencyAlert(
        alert_id="E004",
        patient_id="P004",
        emergency_type="Breathing Difficulty",
        severity=2,
        message="Patient needs urgent attention.",
    )

    notifier.update(alert)

    assert len(notifier.notifications) == 1
    assert "E004" in notifier.notifications[0]
    assert "P004" in notifier.notifications[0]


def test_resource_allocator_allocates_critical_resources():
    allocator = ResourceAllocator()

    alert = EmergencyAlert(
        alert_id="E005",
        patient_id="P005",
        emergency_type="Cardiac Arrest",
        severity=1,
        message="Resuscitation required.",
    )

    allocator.update(alert)

    assert "Emergency Doctor" in allocator.resources["E005"]
    assert "Emergency Nurse" in allocator.resources["E005"]
    assert "Resuscitation Equipment" in allocator.resources["E005"]


def test_patient_tracker_tracks_patient():
    tracker = PatientTracker()

    alert = EmergencyAlert(
        alert_id="E006",
        patient_id="P006",
        emergency_type="Trauma",
        severity=3,
        message="Trauma patient.",
    )

    tracker.update(alert)

    assert "P006" in tracker.active_patients


def test_patient_tracker_removes_patient():
    tracker = PatientTracker()

    alert = EmergencyAlert(
        alert_id="E007",
        patient_id="P007",
        emergency_type="Trauma",
        severity=3,
        message="Trauma patient.",
    )

    tracker.update(alert)
    tracker.remove_patient("P007")

    assert "P007" not in tracker.active_patients


def test_emergency_system_notifies_all_observers():
    system = EmergencyResponseSystem()

    notifier = StaffNotifier()
    allocator = ResourceAllocator()
    tracker = PatientTracker()

    system.subscribe(notifier)
    system.subscribe(allocator)
    system.subscribe(tracker)

    alert = EmergencyAlert(
        alert_id="E008",
        patient_id="P008",
        emergency_type="Severe Injury",
        severity=2,
        message="Patient requires emergency care.",
    )

    system.create_alert(alert)

    assert len(notifier.notifications) == 1
    assert "E008" in allocator.resources
    assert "P008" in tracker.active_patients


def test_unsubscribe_stops_notifications():
    system = EmergencyResponseSystem()

    notifier = StaffNotifier()

    system.subscribe(notifier)
    system.unsubscribe(notifier)

    alert = EmergencyAlert(
        alert_id="E009",
        patient_id="P009",
        emergency_type="Fall",
        severity=4,
        message="Patient fell.",
    )

    system.create_alert(alert)

    assert len(notifier.notifications) == 0


def test_get_active_alerts():
    system = EmergencyResponseSystem()

    alert1 = EmergencyAlert(
        alert_id="E010",
        patient_id="P010",
        emergency_type="Trauma",
        severity=2,
        message="Urgent.",
    )

    alert2 = EmergencyAlert(
        alert_id="E011",
        patient_id="P011",
        emergency_type="Fever",
        severity=4,
        message="Requires attention.",
    )

    system.create_alert(alert1)
    system.create_alert(alert2)

    system.resolve_alert("E010")

    active_alerts = system.get_active_alerts()

    assert len(active_alerts) == 1
    assert active_alerts[0].alert_id == "E011"

def test_emergency_service_registers_case():
    response_system = EmergencyResponseSystem()
    notifier = StaffNotifier()

    response_system.subscribe(notifier)

    service = EmergencyService(response_system)

    alert = EmergencyAlert(
        alert_id="E100",
        patient_id="P100",
        emergency_type="Cardiac Arrest",
        severity=1,
        message="Immediate intervention required.",
    )

    service.register_emergency(alert)

    assert service.get_emergency("E100") == alert
    assert len(notifier.notifications) == 1


def test_emergency_service_resolves_case():
    response_system = EmergencyResponseSystem()
    service = EmergencyService(response_system)

    alert = EmergencyAlert(
        alert_id="E101",
        patient_id="P101",
        emergency_type="Trauma",
        severity=2,
        message="Patient requires treatment.",
    )

    service.register_emergency(alert)
    service.resolve_emergency("E101")

    assert alert.resolved
    assert service.get_active_emergencies() == []


def test_duplicate_emergency_is_rejected():
    response_system = EmergencyResponseSystem()
    service = EmergencyService(response_system)

    alert = EmergencyAlert(
        alert_id="E102",
        patient_id="P102",
        emergency_type="Fall",
        severity=3,
        message="Patient fell.",
    )

    service.register_emergency(alert)

    try:
        service.register_emergency(alert)
        assert False
    except ValueError:
        assert True
