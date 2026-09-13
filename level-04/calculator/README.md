# Scientific Calculator

A calculator package with basic/scientific/statistical operations, calculation
history (with undo/redo), configurable precision and angle mode, a plugin
system, and both a CLI and a minimal GUI.

## Structure

```
calculator/
    __init__.py      # exposes the main Calculator class
    basic.py          # add, subtract, multiply, divide, power, modulus, floor_divide
    scientific.py      # sqrt, log, ln, sin/cos/tan (+ _deg variants), factorial, pi, e
    statistical.py      # mean, median, mode, variance, std_dev, correlation, linear_regression
    history.py          # CalculationHistory: undo/redo, JSON export/import, usage stats
    config.py            # precision, angle mode, history size, theme
    utils.py               # custom exceptions, logging, unit conversions
    evaluator.py             # safe AST-based expression parser (no eval() on raw input)
    plugins.py                 # register custom functions the evaluator can call by name
tests/
    test_basic.py
    test_scientific.py
cli.py      # interactive REPL — the primary interface
gui.py       # minimal tkinter GUI (basic arithmetic only)
```

## Usage

```bash
python3 cli.py
```

```
>> 15 + 7 * 3
= 36.0000
>> sin(45)
= 0.7071
>> history()
>> undo()
>> stats()
>> save history.json
>> quit
```

## Why not `eval()`?

Expressions are parsed with `ast.parse()` and walked through a small
whitelist of node types (numbers, `+ - * / // % **`, unary minus, and calls
to a fixed table of known functions). Raw `eval()` on arbitrary typed input
can execute arbitrary code — this avoids that entirely.

## Angle mode

`sin`, `cos`, and `tan` respect the current angle mode (`DEG` by default —
change with `calc.config.set_angle_mode("RAD")`). `sin_deg`/`cos_deg`/`tan_deg`
are always available regardless of mode.

## Running tests

```bash
pip install -r requirements.txt
python3 -m pytest tests/ -v
```

## Known deviation from the original spec

The spec's own sample transcript shows `15 + 7 * 3` evaluating to `36`
(correct precedence) but then logs it in history as two separate steps —
`15 + 7 = 22` then `22 * 3 = 66` — which is left-to-right, wrong-precedence
math that doesn't even match the `36` shown moments earlier. This
implementation logs the full expression as one history entry with its
correct result instead of reproducing that contradiction.
