#!/usr/bin/env python3

import sys
import math
from string import ascii_lowercase
from typing import Callable

"""
Provides a command-line calculator with support for arbitrarily extensible constants and single-parameter functions. Parenthetical logic (i.e., expression nested) is appropriately accounted for.

NOTE:
1. Functions names MUST be written in lowercase alphabetical script, and underscores are optional.
2. Constants MUST be written in uppercase alphabetical script.
3. Be way of how operator translations (e.g., "x" -> "*") can affect your constants and functions.
"""

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

FUNCTIONS: dict[str, Callable[[float | int], float]] = {
    "log": math.log,
    "log_two": math.log2,
    "log_ten": math.log10,
    "sqrt": math.sqrt,
    "ceil": math.ceil,
    "floor": math.floor,
    "fac": (lambda x: math.factorial(int(x)))
}

class StringBuilder:
    def __init__(self) -> None:
        self.strings: list[str] = []

    def build_string(self) -> str:
        return "".join(self.strings)

    def add(self, string: str) -> None:
        self.strings.append(string)

def verify_parentheses_use(exp: str) -> None:
    stack = 0
    for c in exp:
        if c == LEFT_PAREN:
            stack += 1
        elif c == RIGHT_PAREN:
            stack -= 1
            if stack < 0:
                raise Exception("Unmatched or poorly matched parentheses.")

    if stack != 0:
        raise Exception("Unmatched parentheses.")

def replace_with_dict(exp: str, d) -> str:
    for to_replace, replacement in d.items():
        exp = exp.replace(to_replace, replacement)
    return exp

def replace_constants_and_operators(exp: str) -> str:
    exp = replace_with_dict(exp, OPERATORS)
    exp = replace_with_dict(exp, CONSTANTS)
    return exp

def make_implicit_multiplication_explicit(exp: str) -> str:
    exp = exp.replace(")(", ")*(")

    new_exp: StringBuilder = StringBuilder()
    for i, c in enumerate(exp):
        if i > 0 and ((exp[i-1].isdigit() and c == LEFT_PAREN) or
                      (exp[i-1] == RIGHT_PAREN and c.isdigit())):
            new_exp.add("*")
        new_exp.add(c)

    return new_exp.build_string()
                
def remove_syntactic_sugar(exp: str) -> str:
    exp = replace_constants_and_operators(exp)
    exp = make_implicit_multiplication_explicit(exp)
    return exp

def get_function(fn_name: str) -> Callable[[float|int], float]:
    for c in fn_name:
        if c not in FN_ALPHABET:
            raise Exception(f"Expected function name with only lowercase, alphabetical letters and underscores but found {c} in {fn_name}.")
    
    if fn_name not in FUNCTIONS:
        raise Exception(f"{fn_name} not found in FUNCTIONS keys: {list(FUNCTIONS.keys())}.")
    else:
        return FUNCTIONS[fn_name]

def advance_to_function_end(exp: str, i: int) -> int:
    if exp[i] not in FN_ALPHABET:
       raise Exception(f"Expected function name start at index {i} of expression but instead found {exp[i]} in {exp}.")

    while exp[i] in FN_ALPHABET:
        i += 1

    if exp[i] != LEFT_PAREN:
        raise Exception(f"Expected \"(\" to border end of function name but instead found {exp[i]}.")

    return i

def advance_to_closed_parenthesis(exp: str, i: int) -> int:
    if exp[i] != LEFT_PAREN:
        raise Exception(f"Expected index {i} to point to left parenthesis but index {i} points to {exp[i]} in {exp}.")

    stack: list[str] = [exp[i]]
    while stack and i < len(exp):
        i += 1
        if exp[i] == RIGHT_PAREN:
            stack.pop()
        elif exp[i] == LEFT_PAREN:
            stack.append(LEFT_PAREN)

    if i >= len(exp) and stack:
        raise Exception(f"Non-exhausted initial left-parenthesis in {exp[i:]}.")

    return i

def evaluate(exp: str, fn_to_apply=(lambda x: x)) -> str:
    new_exp: StringBuilder = StringBuilder()
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
            e: int =  advance_to_closed_parenthesis(exp, i)
            to_add = evaluate(exp[i+1:e])
            i: int = e
        else:
            to_add = exp[i]

        new_exp.add(to_add)
        i += 1
  
    x: int | float = eval(new_exp.build_string())
    y: int | float = fn_to_apply(x)
    return str(y)

def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] == "":
        print("Usage: mcal \"<expression>\"")
        return
    exp: str = "".join(sys.argv[1:])
    exp: str = remove_syntactic_sugar(exp) 
    result: str = evaluate(exp)
    print(result)

if __name__ == "__main__":
    main()
