from datetime import date

import pytest

from hospital_system.billing.insurance import Insurance
from hospital_system.billing.invoice import Invoice
from hospital_system.billing.payment import Payment


def make_insurance():
    return Insurance(
        insurance_id="INS001",
        provider="HealthCare Insurance",
        policy_number="POL001",
        coverage_percentage=80,
    )


def make_invoice():
    return Invoice(
        invoice_id="INV001",
        patient_id="PAT001",
        consultation_cost=10_000,
    )


def test_insurance_creation():
    insurance = make_insurance()

    assert insurance.provider == "HealthCare Insurance"
    assert insurance.coverage_percentage == 80
    assert insurance.active is True


def test_insurance_calculates_coverage():
    insurance = make_insurance()

    assert insurance.calculate_coverage(10_000) == 8_000
    assert insurance.calculate_patient_amount(10_000) == 2_000


def test_inactive_insurance_provides_no_coverage():
    insurance = make_insurance()
    insurance.deactivate()

    assert insurance.calculate_coverage(10_000) == 0
    assert insurance.calculate_patient_amount(10_000) == 10_000


def test_invalid_insurance_percentage():
    with pytest.raises(ValueError):
        Insurance(
            insurance_id="INS001",
            provider="HealthCare Insurance",
            policy_number="POL001",
            coverage_percentage=120,
        )


def test_invoice_creation():
    invoice = make_invoice()

    assert invoice.subtotal == 10_000
    assert invoice.balance == 10_000
    assert invoice.status == "UNPAID"


def test_invoice_procedure_and_medication_costs():
    invoice = make_invoice()

    invoice.add_procedure(
        "X-Ray",
        5_000,
    )

    invoice.add_medication(
        "Paracetamol",
        2_000,
    )

    assert invoice.procedure_total == 5_000
    assert invoice.medication_total == 2_000
    assert invoice.subtotal == 17_000


def test_invoice_with_insurance():
    invoice = make_invoice()

    invoice.add_procedure(
        "Laboratory Test",
        5_000,
    )

    invoice.apply_insurance(
        make_insurance()
    )

    assert invoice.subtotal == 15_000
    assert invoice.insurance_coverage == 12_000
    assert invoice.patient_amount == 3_000
    assert invoice.balance == 3_000


def test_payment_creation():
    payment = Payment(
        payment_id="PAY001",
        invoice_id="INV001",
        amount=5_000,
        payment_date=date.today(),
        method="CASH",
    )

    assert payment.amount == 5_000
    assert payment.is_completed is True


def test_invalid_payment_amount():
    with pytest.raises(ValueError):
        Payment(
            payment_id="PAY001",
            invoice_id="INV001",
            amount=0,
            payment_date=date.today(),
            method="CASH",
        )


def test_invoice_payment():
    invoice = make_invoice()

    payment = Payment(
        payment_id="PAY001",
        invoice_id="INV001",
        amount=4_000,
        payment_date=date.today(),
        method="CASH",
    )

    invoice.add_payment(payment)

    assert invoice.total_paid == 4_000
    assert invoice.balance == 6_000
    assert invoice.status == "PARTIALLY_PAID"


def test_invoice_fully_paid():
    invoice = make_invoice()

    payment = Payment(
        payment_id="PAY001",
        invoice_id="INV001",
        amount=10_000,
        payment_date=date.today(),
        method="CARD",
    )

    invoice.add_payment(payment)

    assert invoice.total_paid == 10_000
    assert invoice.balance == 0
    assert invoice.status == "PAID"


def test_payment_must_belong_to_invoice():
    invoice = make_invoice()

    payment = Payment(
        payment_id="PAY001",
        invoice_id="INV999",
        amount=5_000,
        payment_date=date.today(),
        method="CASH",
    )

    with pytest.raises(ValueError):
        invoice.add_payment(payment)


def test_refund_payment():
    payment = Payment(
        payment_id="PAY001",
        invoice_id="INV001",
        amount=5_000,
        payment_date=date.today(),
        method="CASH",
    )

    payment.refund()

    assert payment.status == "REFUNDED"
    assert payment.is_completed is False
