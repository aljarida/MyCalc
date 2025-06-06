# MyCalc: Minimal CLI Calculator

**MyCalc** is a minimal command-line calculator for evaluating math. expressions instantly, with zero learning curve.

## Philosophy

**MyCalc** is designed for users who:
- Want calculations now—no GUIs and no noise.
- Prefer as little friction as possible to jot down, evaluate, and experiment with math. expressions.

## Quickstart

> Ensure you have Python 3 installed on your system.

If not already made executable, run:
```bash
chmod +x mcal.py
```

Then use:
```bash
./mcal.py "expression"
```
; or,
```bash
python3 mcal.py "expression"
```

You can also run the program without arguments to enter an interactive REPL mode:
```bash
./mcal.py
```

## Usage

mcal works in two main ways:
1. **Single-shot expression**—Give it a math. expression as an argument.
2. **REPL mode**—Invoke it with no arguments and interactively enter as many expressions as you want.

### Single-Shot Expressions

Calculate directly from the command line:

```bash
$ mcal.py "(3^4)/5"
16.2
```
```bash
$ mcal.py "log(100) + PI"
7.746762839577885
```

- The caret `^` is interpreted as exponentiation (i.e., `**`).
- The constants `PI` and `E` are available.

### REPL Mode

Run with no arguments for an interactive session:
```bash
$ mcal.py
Enter 'q' to quit.
[1] ~ 10 + 5 * 3
      = 25
[2] ~ sqrt(81)
      = 9.0
[3] ~ log(E)
      = 1.0
[4] ~ q
# MyCalc exits
```

**Added Usage in the REPL:**
- **Register variables:**
  - Each result is saved as `$1`, `$2`, ... for that session.
  - Use `$N` in later calculations. Example:
      ```bash
      [1] ~ 7 + 2
            = 9
      [2] ~ $1 * 3
            = 27
      ```    
- **Clear screen:** Enter `c`, `clear`, `clean`, or `wipe`.
- **Quit:** Enter `q`, `quit`, or `exit`.


## Supported Syntax

- **Standard math. operations**: `+`, `-`, `x` (product), `*`, `/`, `^` (exponent), parentheses
- **Implicit multiplication:** `2(3+4)` → `2*(3+4)`, `(3)4` → `(3)*4`
- **Constants:** `PI`, `E`
- **Functions:** (always lowercase, underscores allowed)
    - `sqrt(x)` — square root
    - `log(x)` — natural logarithm (base e)
    - `log_two(x)` — logarithm base 2
    - `log_ten(x)` — logarithm base 10
    - `ceil(x)` — ceiling
    - `floor(x)` — floor
    - `fac(x)` — factorial (for integer `x`)
