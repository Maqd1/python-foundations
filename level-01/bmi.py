"""
⚖️ HARD BMI CALCULATOR

The Health Risk Assessor 💪

Write a program that:

1. Asks for weight in kg (accept decimals)
2. Asks for height in either:
   · Meters (e.g., 1.75)
   · Centimeters (e.g., 175)
   · Feet and Inches (e.g., "5'10"")
   Let the user choose their input format!
3. Calculates BMI: weight / (height_in_meters ** 2)
4. Prints:
   · BMI value (rounded to 1 decimal place)
   · Category: Underweight, Normal, Overweight, Obese
   · 🚨 HARD PART: Calculate their "ideal weight range" based on height
   · For BMI 18.5–24.9: ideal range = 18.5 * height² to 24.9 * height²
5. Ask: "Would you like to save this data? (y/n)"
   · If 'y', save to a file bmi_history.txt
   · Include: date, weight, height, BMI, category

Concepts Tested:

· Multiple data types (float, string)
· Conditional logic (nested if statements)
· String methods (.split(), .strip())
· Type conversion (float(), int())
· File I/O (writing to .txt files)
· Date handling (needed for saving data)

Example Output:

```
Choose height input format:
1. Meters (e.g., 1.75)
2. Centimeters (e.g., 175)
3. Feet & Inches (e.g., 5'10")
Choice: 3
Enter height (feet'inches"): 5'10"
Enter weight (kg): 75

📊 RESULTS:
BMI: 22.8
Category: Normal
Ideal weight range: 58.5 kg - 78.8 kg
```

---
"""

weight = float(input("Enter weight (kg): "))

print("Choose height input format:")
print("1. Meters (e.g., 1.75)")
print("2. Centimeters (e.g., 175)")
print("3. Feet & Inches (e.g., 5'10\")")
choice = input("Choice: ")

if choice == "1":
    height_m = float(input("Enter height (meters): "))
elif choice == "2":
    height_cm = float(input("Enter height (centimeters): "))
    height_m = height_cm / 100
elif choice == "3":
    feet_inches = input("Enter height (feet'inches\"): ")
    feet_inches = feet_inches.replace('"', '')  # strip trailing "
    feet, inches = feet_inches.split("'")
    feet = int(feet)
    inches = int(inches)
    total_inches = (feet * 12) + inches
    height_m = total_inches * 0.0254
else:
    print("Invalid choice.")
    exit()

bmi = weight / (height_m ** 2)

if bmi < 18.5:
    category = "Underweight"
elif bmi < 25:
    category = "Normal"
elif bmi < 30:
    category = "Overweight"
else:
    category = "Obese"

print("\n📊 RESULTS:")
print(f"BMI: {bmi:.1f}")
print(f"Category: {category}")

ideal_min = 18.5 * (height_m ** 2)
ideal_max = 24.9 * (height_m ** 2)

print(f"Ideal weight range: {ideal_min:.1f} kg - {ideal_max:.1f} kg")

save = input("\nWould you like to save this data? (y/n): ").lower()

if save == "y":
    date_str = input("Enter today's date (DD/MM/YYYY): ")

    with open("bmi_history.txt", "a") as file:
        file.write(f"{date_str} | Weight: {weight}kg | Height: {height_m:.2f}m | BMI: {bmi:.1f} | Category: {category}\n")

    print("Saved to bmi_history.txt!")
else:
    print("Not saved.")