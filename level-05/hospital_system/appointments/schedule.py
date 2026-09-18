from abc import ABC, abstractmethod
from datetime import datetime

from hospital_system.appointments.appointment import Appointment


class SchedulingStrategy(ABC):

    @abstractmethod
    def schedule(
        self,
        appointments: list[Appointment],
        appointment: Appointment
    ) -> Appointment:
        pass


class StandardScheduling(SchedulingStrategy):

    def schedule(
        self,
        appointments: list[Appointment],
        appointment: Appointment
    ) -> Appointment:

        for existing in appointments:
            if (
                existing.doctor_id == appointment.doctor_id
                and existing.appointment_time
                == appointment.appointment_time
                and existing.is_active
            ):
                raise ValueError(
                    "Doctor already has an appointment "
                    "at this time."
                )

        appointment.confirm()
        appointments.append(appointment)

        return appointment


class PriorityScheduling(SchedulingStrategy):

    def schedule(
        self,
        appointments: list[Appointment],
        appointment: Appointment
    ) -> Appointment:

        for existing in appointments:
            if (
                existing.doctor_id == appointment.doctor_id
                and existing.appointment_time
                == appointment.appointment_time
                and existing.is_active
            ):
                if appointment.priority < existing.priority:
                    existing.cancel()
                    break

                raise ValueError(
                    "A higher or equal priority appointment "
                    "already occupies this time."
                )

        appointment.confirm()
        appointments.append(appointment)

        return appointment


class EmergencyScheduling(SchedulingStrategy):

    def schedule(
        self,
        appointments: list[Appointment],
        appointment: Appointment
    ) -> Appointment:

        appointment.priority = 1

        for existing in appointments:
            if (
                existing.doctor_id == appointment.doctor_id
                and existing.appointment_time
                == appointment.appointment_time
                and existing.is_active
            ):
                existing.cancel()

        appointment.confirm()
        appointments.append(appointment)

        return appointment


class AppointmentScheduler:

    def __init__(
        self,
        strategy: SchedulingStrategy
    ):
        self.strategy = strategy
        self.appointments: list[Appointment] = []

    def set_strategy(
        self,
        strategy: SchedulingStrategy
    ) -> None:
        self.strategy = strategy

    def schedule(
        self,
        appointment: Appointment
    ) -> Appointment:
        return self.strategy.schedule(
            self.appointments,
            appointment
        )

    def cancel(self, appointment_id: str) -> None:
        for appointment in self.appointments:
            if appointment.appointment_id == appointment_id:
                appointment.cancel()
                return

        raise ValueError(
            f"Appointment {appointment_id} not found."
        )

    def get_active_appointments(self) -> list[Appointment]:
        return [
            appointment
            for appointment in self.appointments
            if appointment.is_active
        ]