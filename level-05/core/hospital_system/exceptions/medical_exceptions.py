class HospitalError(Exception):
    """Base exception for the hospital system."""


class PatientError(HospitalError):
    """Base exception for patient-related errors."""


class InvalidPatientError(PatientError):
    """Raised when patient information is invalid."""


class AdmissionError(PatientError):
    """Raised when an admission operation fails."""


class MedicalRecordError(HospitalError):
    """Raised when a medical record operation fails."""


class AppointmentError(HospitalError):
    """Raised when an appointment operation fails."""


class PrescriptionError(HospitalError):
    """Raised when a prescription operation fails."""


class BillingError(HospitalError):
    """Raised when a billing operation fails."""


class InventoryError(HospitalError):
    """Raised when an inventory operation fails."""


class EmergencyError(HospitalError):
    """Raised when an emergency operation fails."""