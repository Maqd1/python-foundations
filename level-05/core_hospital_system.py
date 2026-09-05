'''
3️⃣ 🏥 VERY HARD HOSPITAL SYSTEM
The Complete Healthcare Management System 🏥

Build a comprehensive hospital system with patients, doctors, appointments, and medical records!

Package Structure:
text

hospital_system/
    __init__.py
    patients/
        __init__.py
        patient.py
        medical_record.py
        visit.py
    staff/
        __init__.py
        doctor.py
        nurse.py
        admin.py
    appointments/
        __init__.py
        appointment.py
        schedule.py
    pharmacy/
        __init__.py
        medication.py
        prescription.py
        inventory.py
    billing/
        __init__.py
        invoice.py
        payment.py
        insurance.py
    services/
        __init__.py
        emergency.py
        lab.py
        radiology.py
    exceptions/
        __init__.py
        medical_exceptions.py
    tests/
        __init__.py
        test_patients.py
    main.py
    cli.py
    setup.py

Requirements:

    Patient System (Inheritance):

        Patient: Personal info, medical history, allergies

        Inpatient: Room assignment, admission/discharge

        Outpatient: Clinic visits, referrals

        EmergencyPatient: Emergency info, triage

    Medical Records (Composition):

        MedicalRecord: Patient, diagnoses, treatments, outcomes

        VitalSigns: Blood pressure, heart rate, temperature

        LabResult: Tests, results, reference ranges

        Prescription: Medication, dosage, duration

    Staff Hierarchy:

        Doctor: Specialty, certifications, schedule

        Nurse: Department, shift, certifications

        Admin: Role, department, access level

    Appointment System (Strategy Pattern):

        Different scheduling strategies

        Priority-based scheduling

        Emergency overrides

        Cancellation management

    Billing System (HARD):

        Consultation fees

        Procedure costs

        Medication costs

        Insurance coverage

        Payment plans

    Inventory System (HARDEST):

        Medication inventory

        Medical supplies

        Expiry tracking

        Reorder alerts

    Emergency Response (Observer Pattern):

        Emergency alerts

        Staff notification

        Resource allocation

        Patient tracking

Sample Output:
text

🏥 LAGOS UNIVERSITY TEACHING HOSPITAL 🏥

👤 PATIENT PROFILE
Name: Damilola Ogunleye
Patient ID: P2024-5678
DOB: 1996-03-15 (Age: 30)
Blood Group: O+
Allergies: Penicillin, Latex
Emergency Contact: John Ogunleye (080-1234-5678)

📋 MEDICAL HISTORY
1. Diagnosis: Malaria (2024-05-15)
   Treatment: Artemether-Lumefantrine
   Outcome: Resolved

2. Diagnosis: Hypertension (2025-08-10)
   Treatment: Amlodipine 5mg daily
   Outcome: Stable

3. Diagnosis: Diabetes Type 2 (2026-01-20)
   Treatment: Metformin 500mg BD
   Outcome: Under management

=====================================
🏥 CURRENT ADMISSION
Admission Number: ADM-2026-09-05-001
Ward: General Medicine (Ward B)
Room: 304-B
Admitted: 2026-09-05 14:30
Condition: Stable
Attending Doctor: Dr. Adaobi Okonkwo (Cardiology)

VITAL SIGNS (Last Update):
BP: 130/85 mmHg (Elevated)
HR: 78 bpm (Normal)
Temp: 37.2°C (Normal)
SpO2: 98% (Normal)
Glucose: 5.6 mmol/L (Normal)

=====================================
📋 CURRENT TREATMENT PLAN
1. Medication:
   - Amlodipine 5mg (Once daily)
   - Metformin 500mg (Twice daily)
   - Insulin 10 units (Before meals)

2. Procedures:
   - ECG (Scheduled: Tomorrow 10:00)
   - Echocardiogram (Scheduled: Tomorrow 14:00)
   - Blood Work (Daily morning)

3. Diet:
   - Low sodium diet
   - Diabetic diet
   - Fluid restriction: 1.5L/day

=====================================
📋 LAB RESULTS (2026-09-05)
1. CBC:
   WBC: 5.2 x10^9/L (Normal)
   RBC: 4.8 x10^12/L (Normal)
   Platelets: 150 x10^9/L (Normal)

2. Chemistry:
   Sodium: 135 mmol/L (Normal)
   Potassium: 4.2 mmol/L (Normal)
   Creatinine: 1.0 mg/dL (Normal)
   Glucose: 5.6 mmol/L (Normal)
   HbA1c: 7.2% (Elevated - Poor control)

=====================================
💊 MEDICATION ORDER
1. Amlodipine 5mg
   - Dosage: 1 tablet daily
   - Route: Oral
   - Start: 2026-09-05
   - End: 2026-10-05
   - Prescribed by: Dr. Adaobi Okonkwo
   - Pharmacy: In-patient pharmacy
   - Status: Active

2. Metformin 500mg
   - Dosage: 1 tablet twice daily
   - Route: Oral
   - Start: 2026-09-05
   - End: 2026-12-05
   - Prescribed by: Dr. Adaobi Okonkwo
   - Pharmacy: In-patient pharmacy
   - Status: Active

=====================================
💰 BILLING SUMMARY
Patient: Damilola Ogunleye
Admission: 2026-09-05
Insurance: NHIS (75% coverage)

Current Charges:
1. Admission Fee: ₦25,000.00
2. Bed Fee (Ward B): ₦15,000.00/day
3. Consultation: ₦50,000.00
4. Lab Tests: ₦35,000.00
5. Medications: ₦12,500.00
6. Procedures: ₦45,000.00
-------------------------------------------------
Subtotal: ₦182,500.00
Insurance (75%): -₦136,875.00
Balance: ₦45,625.00

=====================================
⚠️ MEDICATION ALERT!
Medication: Penicillin
Patient: Damilola Ogunleye
Allergy: Penicillin (Documented)

Prescription Error Detected!
Doctor: Dr. John Smith
Prescribed: Amoxicillin (Penicillin-based)

⚠️ Alert sent to attending doctor!
Action: Prescription blocked - Changed to Azithromycin
=====================================

=====================================
📊 DAILY ROUND NOTES
Date: 2026-09-05
Time: 08:00
Doctor: Dr. Adaobi Okonkwo

Patient: Damilola Ogunleye
Chief Complaint: Chest pain, Shortness of breath
Assessment: Hypertensive crisis, Type 2 DM

Plan:
1. Adjust Amlodipine to 10mg
2. Start IV fluids
3. Cardiology consult
4. Echocardiogram
5. Monitor blood pressure q4h

=====================================
⏰ SCHEDULED APPOINTMENTS
1. Cardiology Consultation
   - Doctor: Dr. Adaobi Okonkwo
   - Date: 2026-09-06
   - Time: 10:00
   - Location: Outpatient Clinic B
   - Status: Confirmed

2. Ophthalmology (Diabetic Eye Check)
   - Doctor: Dr. Chidi Okafor
   - Date: 2026-09-12
   - Time: 14:00
   - Location: Eye Clinic
   - Status: Pending Confirmation

=====================================
📊 HOSPITAL STATISTICS (Today)
Patients Admitted: 12
Emergency Visits: 45
Surgeries: 8
Discharges: 15
Occupancy Rate: 87%
Wait Time (ER): 15 minutes

Concepts Tested: Advanced inheritance, composition, strategy pattern, observer pattern, dataclasses, property decorators, complex validation, medical data management, inventory management, real-time alerts
'''