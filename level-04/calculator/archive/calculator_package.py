'''
🎯 HARD PROJECTS USING FUNCTIONS & MODULES
1️⃣ 🧮 HARD CALCULATOR PACKAGE
The Scientific Calculator Package with History 📐

Build a complete calculator package with scientific functions, history, and plugin support!

Package Structure:
text

calculator/
    __init__.py
    basic.py
    scientific.py
    statistical.py
    history.py
    config.py
    utils.py
tests/
    test_basic.py
    test_scientific.py
cli.py
gui.py
setup.py
requirements.txt
README.md

Data Structure:
python

# calculator/history.py
class CalculationHistory:
    def __init__(self, max_size=100):
        self.history = []
        self.max_size = max_size
        self.current = 0
        
    def add(self, operation, a, b, result):
        entry = {
            "id": len(self.history) + 1,
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "a": a,
            "b": b,
            "result": result
        }
        self.history.append(entry)
        if len(self.history) > self.max_size:
            self.history.pop(0)
            
    def undo(self):
        if len(self.history) > 0:
            return self.history.pop()
        return None
        
    def get_last(self, n=1):
        return self.history[-n:] if n <= len(self.history) else self.history
        
    def clear(self):
        self.history = []

Requirements:

    Basic Operations (calculator/basic.py):

        add(a, b) → a + b

        subtract(a, b) → a - b

        multiply(a, b) → a * b

        divide(a, b) → a / b (handle division by zero)

        power(a, b) → a ** b

        modulus(a, b) → a % b

        floor_divide(a, b) → a // b

    Scientific Operations (calculator/scientific.py):

        sqrt(x) → Square root

        log(x, base=10) → Logarithm

        ln(x) → Natural log

        sin(x), cos(x), tan(x) → Trig functions (radians)

        sin_deg(x), cos_deg(x), tan_deg(x) → Trig functions (degrees)

        factorial(x) → x!

        pi() → π constant

        e() → e constant

    Statistical Operations (calculator/statistical.py):

        mean(*args) → Average

        median(*args) → Middle value

        mode(*args) → Most frequent

        variance(*args) → Population variance

        std_dev(*args) → Standard deviation

        correlation(x_list, y_list) → Pearson correlation

        linear_regression(x_list, y_list) → Slope and intercept

    History System (calculator/history.py):

        Store every calculation with timestamp

        undo() → Remove last calculation

        redo() → Re-add undone calculation

        export_history(filename) → Save to JSON

        import_history(filename) → Load from JSON

        get_statistics() → Most used operations, average results, etc.

    Configuration (calculator/config.py):

        Set precision (decimal places)

        Set angle mode (DEG/RAD)

        Set history size

        Theme/color settings

        Load/Save config to JSON

    Package Features (HARD):

        Plugin System: Allow custom functions via plugins

        Error Handling: Custom exceptions for math errors

        Logging: Log all calculations to file

        Unit Conversion: Add length, weight, temperature conversions

    CLI Interface (cli.py):
    python

    def main():
        calc = Calculator()
        while True:
            expr = input(">> ")
            if expr == "quit": break
            try:
                result = calc.evaluate(expr)
                print(f"= {result}")
            except Exception as e:
                print(f"Error: {e}")

Sample Output:
text

🧮 PYTHON SCIENTIFIC CALCULATOR v2.0 🧮

Mode: Scientific | Precision: 4 | Angle: DEG

>> 15 + 7 * 3
= 36.0000

>> sin(45)
= 0.7071

>> log(100)
= 2.0000

>> factorial(10)
= 3628800.0000

>> mean(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
= 5.5000

>> history()
📜 Calculation History:
1: 15 + 7 = 22.0000
2: 22 * 3 = 66.0000  [undo available]
3: sin(45) = 0.7071
4: log(100) = 2.0000
5: factorial(10) = 3628800.0000
6: mean(...) = 5.5000

>> undo()
✅ Undone: 22 * 3 = 66.0000

>> history()
1: 15 + 7 = 22.0000
2: sin(45) = 0.7071
3: log(100) = 2.0000
4: factorial(10) = 3628800.0000
5: mean(...) = 5.5000

>> stats()
📊 Usage Statistics:
Most used operations:
1. Addition (32%)
2. Multiplication (25%)
3. Sin (15%)

Average result: 124.5
Total calculations: 1,247

>> save history.txt
✅ History saved to history.txt

>> quit
Goodbye! 👋

Concepts Tested: Package structure, modules, functions with decorators, error handling, file I/O, JSON serialization, logging, plugin architecture, CLI design
'''