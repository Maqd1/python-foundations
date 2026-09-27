
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