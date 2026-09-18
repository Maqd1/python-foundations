from datetime import datetime

import pytest

from hospital_system.appointments import (
    Appointment,
    AppointmentScheduler,
    StandardScheduling,
    PriorityScheduling,
    EmergencyScheduling,
)


def make_appointment(
    appointment_id,
    doctor_id="DOC001",
    priority=3,
):
    return Appointment(
        appointment_id=appointment_id,
        patient_id="PAT001",
        doctor_id=doctor_id,
        appointment_time=datetime(2026, 9, 20, 10, 0),
        reason="Consultation",
        priority=priority,
    )


def test_standard_scheduling():
    scheduler = AppointmentScheduler(
        StandardScheduling()
    )

    appointment = make_appointment("APT001")

    scheduler.schedule(appointment)

    assert appointment.status == "CONFIRMED"
    assert len(scheduler.appointments) == 1


def test_duplicate_appointment_is_rejected():
    scheduler = AppointmentScheduler(
        StandardScheduling()
    )

    scheduler.schedule(make_appointment("APT001"))

    with pytest.raises(ValueError):
        scheduler.schedule(make_appointment("APT002"))


def test_priority_appointment_replaces_lower_priority():
    scheduler = AppointmentScheduler(
        PriorityScheduling()
    )

    normal = make_appointment(
        "APT001",
        priority=3,
    )

    urgent = make_appointment(
        "APT002",
        priority=2,
    )

    scheduler.schedule(normal)
    scheduler.schedule(urgent)

    assert normal.status == "CANCELLED"
    assert urgent.status == "CONFIRMED"


def test_emergency_appointment_overrides_existing():
    scheduler = AppointmentScheduler(
        EmergencyScheduling()
    )

    normal = make_appointment("APT001")

    emergency = make_appointment("APT002")

    scheduler.schedule(normal)
    scheduler.schedule(emergency)

    assert normal.status == "CANCELLED"
    assert emergency.status == "CONFIRMED"
    assert emergency.priority == 1


def test_cancel_appointment():
    scheduler = AppointmentScheduler(
        StandardScheduling()
    )

    appointment = make_appointment("APT001")

    scheduler.schedule(appointment)
    scheduler.cancel("APT001")

    assert appointment.status == "CANCELLED"
    assert scheduler.get_active_appointments() == []


def test_strategy_can_be_changed_at_runtime():
    scheduler = AppointmentScheduler(
        StandardScheduling()
    )

    assert isinstance(
        scheduler.strategy,
        StandardScheduling,
    )

    scheduler.set_strategy(
        EmergencyScheduling()
    )

    assert isinstance(
        scheduler.strategy,
        EmergencyScheduling,
    )
