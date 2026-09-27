# 🌡️ HARD TEMPERATURE CONVERTER - The Thermal Master

## Difficulty

Core

## Task

Write a temperature conversion program that displays a menu with these options:

1. Celsius to Fahrenheit
2. Fahrenheit to Celsius
3. Celsius to Kelvin
4. Kelvin to Celsius
5. Fahrenheit to Kelvin
6. Kelvin to Fahrenheit
7. Convert multiple values

### Multiple Values

For option 7, allow the user to enter multiple temperatures separated by commas.

For example:

```text
25, 30, 35, 40
```

The program should convert every value using the conversion selected by the user.

For example:

```text
0°C = 32.0°F
25°C = 77.0°F
37°C = 98.6°F
100°C = 212.0°F
```

### Error Handling

The program must handle invalid input.

If the user enters text instead of a number, print:

```text
Invalid input! Please enter a number.
```

If Kelvin is involved, ensure that the temperature does not go below absolute zero:

```text
0 K = -273.15°C
```

If the input is below the valid Kelvin limit, display an error.

After an error, ask the user whether they want to retry or exit.

### Conversion History

After each conversion, ask:

```text
Add to history? (y/n)
```

If the user chooses `y`, store the conversion in a history list.

At the end of the program, print all conversions stored in the history.

## Formulas

### Celsius → Fahrenheit

```text
°F = (°C × 9/5) + 32
```

### Fahrenheit → Celsius

```text
°C = (°F - 32) × 5/9
```

### Celsius → Kelvin

```text
K = °C + 273.15
```

### Kelvin → Celsius

```text
°C = K - 273.15
```

### Fahrenheit → Kelvin

```text
K = (°F - 32) × 5/9 + 273.15
```

### Kelvin → Fahrenheit

```text
°F = (K - 273.15) × 9/5 + 32
```

## Example

```text
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
```

## Goal

Build a temperature converter that combines menus, calculations, loops, lists, string parsing, input validation, error handling, and conversion history.

## Concepts Tested

* Nested conditionals
* Lists
* Loops
* String methods (`.split()`, `.strip()`)
* Parsing comma-separated input
* Numeric input validation
* Error handling
* Boolean logic
* Type conversion
* Arithmetic
* Formatted output
