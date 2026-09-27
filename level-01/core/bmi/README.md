# ⚖️ HARD BMI CALCULATOR - The Health Risk Assessor

## Difficulty

Core

## Task

Write a program that:

1. Asks for weight in kilograms. Decimals should be accepted.
2. Asks for height using one of three input formats:

   * Meters (e.g., `1.75`)
   * Centimeters (e.g., `175`)
   * Feet and inches (e.g., `5'10"`)
3. Allows the user to choose their preferred height input format.
4. Calculates BMI using:

```text
BMI = weight / (height_in_meters ** 2)
```

5. Prints:

   * BMI rounded to 1 decimal place
   * BMI category
   * Ideal weight range based on the user's height
6. Asks:

```text
Would you like to save this data? (y/n)
```

If the user chooses `y`, save the following information to `bmi_history.txt`:

* Date
* Weight
* Height
* BMI
* Category

### BMI Categories

* Underweight: BMI below 18.5
* Normal: BMI from 18.5 to 24.9
* Overweight: BMI from 25.0 to 29.9
* Obese: BMI 30.0 or above

### Ideal Weight Range

For a BMI between 18.5 and 24.9:

```text
Minimum ideal weight = 18.5 * height²
Maximum ideal weight = 24.9 * height²
```

The height used in the calculation must be in meters.

## Example

```text
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

## Goal

Build a program that combines user input, multiple data types, conditional logic, string processing, type conversion, calculations, file handling, and date handling.

## Concepts Tested

* Multiple data types (`float`, `string`)
* `input()`
* Conditional logic
* Nested `if` statements
* String methods (`.split()`, `.strip()`)
* Type conversion (`float()`, `int()`)
* Arithmetic
* File I/O
* Writing to `.txt` files
* Date handling
* Formatted output
