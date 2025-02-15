#!/usr/bin/env python3

import re
import sys
import math
from string import ascii_lowercase
from typing import Callable


CLEAR_TOKENS = ["c", "clear", "clean", "wipe"]
QUIT_TOKENS = ["q", "quit", "exit"]

FN_ALPHABET = set(ascii_lowercase).union(set(["_"]))
LEFT_PAREN = "("
RIGHT_PAREN = ")"

CONSTANTS: dict[str, str] = {
    "E": str(math.e),
    "PI": str(math.pi)
}

OPERATORS: dict[str, str] = {
    "^": "**",
    "X": "*",
}

"""
1. Functions names must be written in lowercase alphabetical script, and underscores are optional.
2. Constants must be written in uppercase alphabetical script.
3. Be aware of how syntactic-sugar translations (e.g., "x" -> "*") can affect your constants and functions.
"""
FUNCTIONS: dict[str, Callable[[float | int], float]] = {
    "log": math.log,
    "log_two": math.log2,
    "log_ten": math.log10,
    "sqrt": math.sqrt,
    "ceil": math.ceil,
    "floor": math.floor,
    "fac": (lambda x: math.factorial(int(x)))
}

def verify_parentheses_use(exp: str) -> None:
    """Checks for balanced parentheses in the expression."""
    msg = "Unbalanced parentheses."
    stack = 0
    for c in exp:
        if c == LEFT_PAREN:
            stack += 1
        elif c == RIGHT_PAREN:
            stack -= 1
            if stack < 0:
                raise Exception(msg)

    if stack != 0:
        raise Exception(msg)

def replace_with_dict(exp: str, d) -> str:
    """Replaces substrings in the expression based on a dictionary."""
    for to_replace, replacement in d.items():
        exp = exp.replace(to_replace, replacement)
    return exp

def replace_constants_and_operators(exp: str) -> str:
    """Replaces constants and operators in the expression."""
    exp = replace_with_dict(exp, OPERATORS)
    exp = replace_with_dict(exp, CONSTANTS)
    return exp

def make_implicit_multiplication_explicit(exp: str) -> str:
    """Adds explicit multiplication for cases like '2(3)' or ')3'."""
    exp = exp.replace(")(", ")*(")

    new_exp: list[str] = []
    for i, c in enumerate(exp):
        if i > 0 and ((exp[i-1].isdigit() and c == LEFT_PAREN) or
                      (exp[i-1] == RIGHT_PAREN and c.isdigit())):
            new_exp.append("*")
        new_exp.append(c)

    return "".join(new_exp)
                
def remove_syntactic_sugar(exp: str) -> str:
    """Applies replacements and formatting to normalize the expression."""
    exp = replace_constants_and_operators(exp)
    exp = make_implicit_multiplication_explicit(exp)
    return exp

def get_function(fn_name: str) -> Callable[[float|int], float]:
    """Returns a function by name, ensuring it only contains valid characters."""
    for c in fn_name:
        if c not in FN_ALPHABET:
            raise Exception(f"Invalid character {c} in function name {fn_name}.")
    
    if fn_name not in FUNCTIONS:
        raise Exception(f"Function {fn_name} not found.")

    return FUNCTIONS[fn_name]

def advance_to_function_end(exp: str, i: int) -> int:
    """Advances to the end of the function name and checks for '('."""
    if exp[i] not in FN_ALPHABET:
       raise Exception(f"Expected function name at index {i}.")
    while exp[i] in FN_ALPHABET:
        i += 1
    if exp[i] != LEFT_PAREN:
        raise Exception(f"Expected '(' after function name at index {i}.")
    return i

def advance_to_closed_parenthesis(exp: str, i: int) -> int:
    """Advances to the closing parenthesis, ensuring matching parentheses."""
    if exp[i] != LEFT_PAREN:
        raise Exception(f"Expected '(' at index {i}.")
    stack: list[str] = [exp[i]]
    while stack and i < len(exp):
        i += 1
        if exp[i] == RIGHT_PAREN:
            stack.pop()
        elif exp[i] == LEFT_PAREN:
            stack.append(LEFT_PAREN)
    if i >= len(exp) and stack:
        raise Exception("Unmatched left parenthesis.")
    return i

def evaluate(exp: str, fn_to_apply=(lambda x: x)) -> str:
    """Evaluates the expression recursively, applying functions if found."""
    new_exp: list[str] = []
    to_add: str | None = None

    i: int = 0
    while i < len(exp):
        function_start: bool = exp[i] in FN_ALPHABET
        vanilla_parentheses: bool = exp[i] == LEFT_PAREN

        if function_start:
            j: int = advance_to_function_end(exp, i)
            fn = get_function(exp[i:j])
            e: int = advance_to_closed_parenthesis(exp, j)
            to_add = evaluate(exp[j+1:e], fn)
            i: int = e
        elif vanilla_parentheses:
            e: int = advance_to_closed_parenthesis(exp, i)
            to_add = evaluate(exp[i+1:e])
            i: int = e
        else:
            to_add = exp[i]

        new_exp.append(to_add)
        i += 1
  
    x: int | float = eval("".join(new_exp))
    y: int | float = fn_to_apply(x)
    return str(y)

def substitute_registers(exp: str) -> str:
    def _substitute_registers(match):
        n: int = int(match.group(1))
        value: str = registers[n-1]
        return value
    return re.sub(r"\$(\d+)", _substitute_registers, exp)

def evaluate_prime(exp: str) -> str:
    desugared_exp: str = remove_syntactic_sugar(exp)
    deregistered_exp: str = substitute_registers(desugared_exp)
    return evaluate(deregistered_exp)

def process_line() -> None:
    exp: str = "".join(sys.argv[1:])
    result = evaluate_prime(exp)
    print(result)

def clear_screen() -> None:
    print("\033[H\033[J", end="")

def repl() -> None:
    clear_screen()
    print("Enter 'q' to quit.")

    count: int = 1
    while True:
        user_input = input(f"[{count}] ~ ")
        if not user_input:
            print("Please enter a non-empty expression.")
            continue
        elif user_input.lower() in CLEAR_TOKENS:
            clear_screen()
            continue
        elif user_input.lower() in QUIT_TOKENS:
            clear_screen()
            break
        
        try:
            result: str = evaluate_prime(user_input)
            registers.append(result)
            prefix: str = (len(str(count)) + 1) * " "
            count += 1
            print(prefix + " = " + result) 
        except:
            print("Error calculating.")

registers: list[str] = []

def main() -> None:
    """Main entry point for the calculator. Processes command-line input."""
    if len(sys.argv) >= 2:
        process_line()
    else:
        repl()

if __name__ == "__main__":
    main()

