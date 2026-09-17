'''
5️⃣ 🚗 VERY HARD CAR RENTAL SYSTEM
The Complete Car Rental Management System 🚗

Build a comprehensive car rental system with vehicles, customers, reservations, and fleet management!

Package Structure:
text

car_rental/
    __init__.py
    vehicles/
        __init__.py
        vehicle.py
        car.py
        suv.py
        truck.py
        van.py
        luxury.py
    customers/
        __init__.py
        customer.py
        driver.py
    reservations/
        __init__.py
        reservation.py
        rental.py
    payments/
        __init__.py
        payment.py
        invoice.py
    fleet/
        __init__.py
        fleet.py
        maintenance.py
    services/
        __init__.py
        pricing.py
        insurance.py
        notification.py
    exceptions/
        __init__.py
        rental_exceptions.py
    tests/
        __init__.py
        test_vehicles.py
    main.py
    cli.py
    api.py
    setup.py

Requirements:

    Vehicle Hierarchy (Inheritance):

        Vehicle: VIN, model, brand, year, mileage, fuel_type, transmission, color

        Car: Seats, fuel_efficiency, features

        SUV: Seats, 4WD, towing_capacity, cargo_space

        Truck: Payload, bed_length, cab_type

        Van: Passenger_capacity, cargo_volume, sliding_doors

        Luxury: Premium_features, interior_material, engine_type

    Customer System:

        Customer: Name, ID, contact, license_info, payment_method

        IndividualCustomer: Driver license, insurance

        BusinessCustomer: Company_name, tax_id, PO_number

        PremiumCustomer: Membership_level, discounts

    Reservation System (Strategy Pattern):

        Different pricing strategies: Daily, Weekly, Monthly, Mileage-based

        Dynamic pricing: Peak season, demand-based

        Deposit calculation

        Cancellation policies

    Rental Management:

        Check-in/check-out process

        Vehicle condition inspection

        Damage reporting

        Fuel policy (Full-to-Full, Pre-paid)

        Additional drivers

    Fleet Management (HARD):

        Vehicle availability

        Maintenance scheduling

        Insurance tracking

        Location tracking

    Pricing System (HARDEST):

        Base rates by vehicle category

        Seasonal pricing

        Long-term discounts

        Insurance add-ons

        Additional driver charges

        One-way rental fees

    Insurance System (Observer Pattern):

        Different insurance tiers

        Damage liability

        Theft protection

        Roadside assistance

        Claims processing

Sample Output:
text

🚗 PREMIUM CAR RENTALS 🚗

📊 FLEET OVERVIEW
Total Vehicles: 45
Available: 28
Rented: 17
Under Maintenance: 0

Fleet Composition:
- Economy: 12
- Standard: 15
- SUV: 8
- Luxury: 5
- Truck: 3
- Van: 2

=====================================
👤 CUSTOMER PROFILE
Name: Damilola Ogunleye
Customer ID: CUST-2024-5678
Membership: GOLD
Driver License: LAG-2024-1234
Credit Card: **** 1234
Joined: 2024-01-15

📊 RENTAL HISTORY
Total Rentals: 23
Total Spend: ₦2,345,678.00
Days Rented: 128
Average Rating: 4.8/5

=====================================
🚗 CURRENT RESERVATION
Reservation ID: RES-20260905-001
Vehicle: Toyota Camry (Standard)
Plate Number: LAG 123 AB
Pickup: 2026-09-05 14:00 (MM Airport)
Return: 2026-09-10 14:00 (MM Airport)
Duration: 5 days

Rental Details:
Daily Rate: ₦45,000.00
Base Rate (5 days): ₦225,000.00
Insurance (Premium): ₦50,000.00
Additional Driver: ₦15,000.00
GPS Rental: ₦10,000.00
----------------------------------------
Subtotal: ₦300,000.00
Loyalty Discount (10%): -₦30,000.00
----------------------------------------
Total: ₦270,000.00

Deposit: ₦100,000.00
Total to Pay Today: ₦370,000.00

=====================================
🚗 VEHICLE DETAILS
Vehicle: Toyota Camry
Year: 2023
Color: Silver
Transmission: Automatic
Fuel Type: Petrol
Features:
- AC
- Power Steering
- Keyless Entry
- Cruise Control
- Bluetooth
- USB Port
- GPS Navigation
- Backup Camera

Mileage: 45,678 km
Condition: EXCELLENT
Last Service: 2026-08-15

=====================================
📋 RENTAL AGREEMENT
Rental Period: Sep 05 - Sep 10, 2026
Pickup Location: MM Airport
Return Location: MM Airport

Terms and Conditions:
1. Returning: Full to Full
2. Miles: Unlimited
3. Insurance: Premium Coverage
4. Additional Driver: D. Ogunleye (Approved)
5. Late Return: ₦5,000.00/day
6. Damage: Excess ₦50,000.00

Confirmation Code: 48293
Signature: ___________________

=====================================
🚗 CHECK-OUT PROCESS
Pre-Rental Inspection:
[] Exterior condition
[] Interior condition
[] Fuel level (FULL)
[] Mileage reading
[] Damage report
[] Accessories check

Mileage: 45,678 km
Fuel Level: 100%

Vehicle Condition:
Exterior: Excellent
Interior: Excellent
No damage noted.

Inspection completed by: John

Customer Signature: ___________________

🔑 Keys handed over: 14:30
Vehicle dispatched: 14:35

=====================================
🚗 ACTIVE RENTALS
Customer: Damilola Ogunleye
Vehicle: Toyota Camry
Due Return: 2026-09-10 14:00
Days Remaining: 2
Mileage Used: 345 km
Fuel Used: 45%

Usage Status: ON SCHEDULE

⚠️ Low Fuel Alert!
Fuel Level: 45%
Please refuel before return.

=====================================
💵 INVOICE
Rental #RENT-20260905-001
Customer: Damilola Ogunleye
Vehicle: Toyota Camry

Invoice Date: 2026-09-10
Payment Due: 2026-09-10

Rental Charges:
5 days @ ₦45,000.00: ₦225,000.00
Excess Mileage: ₦0.00
Fuel (Pre-paid): ₦0.00
Damage: ₦0.00

Adjustments:
Loyalty Discount: -₦30,000.00
----------------------------------------
Total Due: ₦195,000.00

Paid: ₦370,000.00 (Deposit ₦100,000.00 + Rental ₦270,000.00)
Refund: ₦100,000.00
Balance: ₦0.00

=====================================
📊 FLEET UTILIZATION REPORT
Week: Sep 05 - Sep 11, 2026
Total Revenue: ₦1,245,000.00
Utilization Rate: 75%

Top Performing Vehicles:
1. Toyota Camry: 5 rentals (₦450,000.00)
2. Toyota Hilux: 3 rentals (₦285,000.00)
3. Mercedes-Benz: 2 rentals (₦240,000.00)

Lowest Performing:
1. Hyundai Grandeur: 1 rental
2. Ford Ranger: 2 rentals

=====================================
⚠️ MAINTENANCE ALERTS
1. Toyota Camry (LAG 123 AB)
   Mileage: 52,345 km
   Next Service: 55,000 km
   Status: DUE SOON

2. Toyota Hilux (LAG 456 CD)
   Annual Inspection Due: 2026-09-15
   Status: SCHEDULE

=====================================
📋 DAMAGE REPORT
Rental: RENT-20260905-001
Vehicle: Toyota Camry
Return Date: 2026-09-10

Damage Report:
[] Scratches on rear bumper (5cm)
[] Dent on driver side door
[] Missing floor mats

Estimated Repair Cost: ₦35,000.00
Excess: ₦50,000.00
Customer Liability: ₦0.00 (Insurance covers)

Insurance Claim Filed: Claim #CLM-2026-001

=====================================
⭐ CUSTOMER FEEDBACK
Customer: Damilola Ogunleye
Vehicle: Toyota Camry
Rating: 5/5

Feedback:
"Excellent service! The car was well-maintained and clean. Will definitely rent again."

Thank you for choosing Premium Car Rentals!
See you next time!

=====================================
📈 MONTHLY REVENUE REPORT
Month: September 2026
Total Revenue: ₦3,245,000.00
Total Rentals: 145

Revenue Breakdown:
1. Daily Rentals: ₦2,100,000.00 (65%)
2. Insurance: ₦450,000.00 (14%)
3. Add-ons: ₦345,000.00 (11%)
4. Other: ₦350,000.00 (11%)

Projected Revenue (October): ₦3,500,000.00 (↑8%)

Concepts Tested: Advanced inheritance, composition, strategy pattern, observer pattern, dataclasses, property decorators, complex business logic, fleet management, dynamic pricing, insurance handling, damage claims

'''