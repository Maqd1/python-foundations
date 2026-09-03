'''
4.

🌡️ HARD TEMPERATURE CONVERTER

The Thermal Master 🔥❄️

Write a program that:

1. Shows a menu:
  
   1. Celsius to Fahrenheit
   2. Fahrenheit to Celsius
   3. Celsius to Kelvin
   4. Kelvin to Celsius
   5. Fahrenheit to Kelvin
   6. Kelvin to Fahrenheit
   7. Convert multiple values
   
2. Option 7: Let the user enter multiple temperatures:
   · User enters: 25, 30, 35, 40
   · Output: 25°C = 77°F, 30°C = 86°F, ...
   · For any conversion chosen!
3. 🚨 HARD PART: Add error handling:
   · If user enters text, print: "Invalid input! Please enter a number."
· If user chooses Kelvin, ensure temperature isn't below 0K (-273.15°C) and print error if so
   · Ask to retry or exit
4. Keep a conversion history:
   · After each conversion, ask: "Add to history? (y/n)"
   · If 'y', store in memory (list)
   · At the end, print all conversions in history

Formulas:

· °F = (°C × 9/5) + 32
· K = °C + 273.15
· °C = K - 273.15
· °F = (K - 273.15) × 9/5 + 32
· K = (°F - 32) × 5/9 + 273.15

Concepts Tested:

· Nested conditionals
· Lists (for storing history)
· Loops (for multiple values)
· String methods (.split(), .strip() for parsing "25, 30, 35")
· Error handling (check if input is numeric)
· Boolean logic for validation

Example Output:

Option: 7 (convert multiple)
Convert from (C/F/K): C
Convert to (C/F/K): F
Enter temperatures (separated by commas): 0, 25, 37, 100

Results:
0°C = 32.0°F
25°C = 77.0°F
37°C = 98.6°F
100°C = 212.0°F

Add to history? (y/n): y
History saved!
'''

def c_to_f(c):
    return (c * 9/5) + 32

def f_to_c(f):
    return (f - 32) * 5/9

def c_to_k(c):
    return c + 273.15

def k_to_c(k):
    return k - 273.15

def f_to_k(f):
    return (f - 32) * 5/9 + 273.15

def k_to_f(k):
    return (k - 273.15) * 9/5 + 32

def get_temperature():
    while True:
        raw = input("Enter temperature: ")
        try:
            return float(raw)
        except ValueError:
            print("Invalid input! Please enter a number.")

def get_kelvin():
    while True:
        value = get_temperature()
        if value < 0:
            print("Invalid! Kelvin cannot be below 0K.")
        else:
            return value

history = []

while True:
    print("\n1. Celsius to Fahrenheit")
    print("2. Fahrenheit to Celsius")
    print("3. Celsius to Kelvin")
    print("4. Kelvin to Celsius")
    print("5. Fahrenheit to Kelvin")
    print("6. Kelvin to Fahrenheit")
    print("7. Convert multiple values")
    print("8. Show history")
    print("9. Exit")
    option = input("Option: ")

    if option == "9":
        break

    elif option == "1":
        c = get_temperature()
        result = c_to_f(c)
        entry = f"{c}°C = {result:.1f}°F"
        print(entry)
        if input("Add to history? (y/n): ").lower() == "y":
            history.append(entry)

    elif option == "2":
        f = get_temperature()
        result = f_to_c(f)
        entry = f"{f}°F = {result:.1f}°C"
        print(entry)
        if input("Add to history? (y/n): ").lower() == "y":
            history.append(entry)

    elif option == "3":
        c = get_temperature()
        result = c_to_k(c)
        entry = f"{c}°C = {result:.1f}K"
        print(entry)
        if input("Add to history? (y/n): ").lower() == "y":
            history.append(entry)

    elif option == "4":
        k = get_kelvin()
        result = k_to_c(k)
        entry = f"{k}K = {result:.1f}°C"
        print(entry)
        if input("Add to history? (y/n): ").lower() == "y":
            history.append(entry)

    elif option == "5":
        f = get_temperature()
        result = f_to_k(f)
        entry = f"{f}°F = {result:.1f}K"
        print(entry)
        if input("Add to history? (y/n): ").lower() == "y":
            history.append(entry)

    elif option == "6":
        k = get_kelvin()
        result = k_to_f(k)
        entry = f"{k}K = {result:.1f}°F"
        print(entry)
        if input("Add to history? (y/n): ").lower() == "y":
            history.append(entry)

    elif option == "8":
        if not history:
            print("No history yet.")
        else:
            print("\n--- History ---")
            for entry in history:
                print(entry)

    elif option == "7":
        from_unit = input("Convert from (C/F/K): ").upper()
        to_unit = input("Convert to (C/F/K): ").upper()
        raw_values = input("Enter temperatures (separated by commas): ")

        raw_list = raw_values.split(",")
        results = []

        for raw in raw_list:
            raw = raw.strip()
            try:
                value = float(raw)
            except ValueError:
                print(f"Skipping invalid value: {raw}")
                continue
            if from_unit == "C" and to_unit == "F":
                result = c_to_f(value)
                results.append(f"{value}°C = {result:.1f}°F")
            elif from_unit == "F" and to_unit == "C":
                result = f_to_c(value)
                results.append(f"{value}°F = {result:.1f}°C")
            elif from_unit == "C" and to_unit == "K":
                result = c_to_k(value)
                results.append(f"{value}°C = {result:.1f}K")
            elif from_unit == "K" and to_unit == "C":
                result = k_to_c(value)
                results.append(f"{value}K = {result:.1f}°C")
            elif from_unit == "F" and to_unit == "K":
                result = f_to_k(value)
                results.append(f"{value}°F = {result:.1f}K")
            elif from_unit == "K" and to_unit == "F":
                result = k_to_f(value)
                results.append(f"{value}K = {result:.1f}°F")
            else:
                print("Invalid unit combination.")
                continue
        print("\nResults:")
        for r in results:
            print(r)

        if input("Add to history? (y/n): ").lower() == "y":
            history.extend(results)