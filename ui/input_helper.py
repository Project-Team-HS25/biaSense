from __future__ import annotations

import sys
from enum import Enum


class YesOrNo(Enum):
    YES = 1
    NO = 0


class EmptyInputError(ValueError):
    """Custom exception for empty input."""
    pass


class OutOfRangeError(ValueError):
    """Custom exception for values outside the allowed range."""

    def __init__(self, value, min_value, max_value):
        super().__init__(f"Input {value} is out of range ({min_value} to {max_value}).")
        self.value = value
        self.min_value = min_value
        self.max_value = max_value


class StringLengthError(ValueError):
    """Custom exception for strings that are too short or too long."""

    def __init__(self, value, min_length, max_length):
        super().__init__(f"Input '{value}' must be between {min_length} and {max_length} characters long.")
        self.value = value
        self.min_length = min_length
        self.max_length = max_length

# Geänderte Inputhelper, die bei bedarf auch None (leere Eingaben) erlauben

def input_valid_string(prompt: str, min_length: int = 0, max_length: int = sys.maxsize, allow_empty: bool = False) -> str | None:
    """Function to get a valid string input, enforcing length constraints."""
    user_input = input(prompt).strip()
    if user_input == "":
        if allow_empty:
            return None
        else:
            raise EmptyInputError("Input cannot be empty.")
    if not (min_length <= len(user_input) <= max_length):
        raise StringLengthError(user_input, min_length, max_length)
    return user_input

def input_valid_int(prompt: str, min_value: int = -sys.maxsize, max_value: int = sys.maxsize, allow_empty: bool = False) -> int | None:
    user_input = input(prompt).strip()
    if user_input == "":
        if allow_empty:
            return None
        else:
            raise EmptyInputError("Input cannot be empty.")
    try:
        value = int(user_input)
    except ValueError as err:
        raise ValueError("Invalid input. Please enter a valid number.") from err
    if value < min_value or value > max_value:
        raise OutOfRangeError(value, min_value, max_value)
    return value

def input_valid_float(prompt: str, min_value: float = -float('inf'), max_value: float = float('inf'), allow_empty: bool = False) -> float | None:
    user_input = input(prompt).strip()
    if user_input == "":
        if allow_empty:
            return None
        else:
            raise EmptyInputError("Input cannot be empty.")
    try:
        value = float(user_input)
    except ValueError as err:
        raise ValueError("Invalid input. Please enter a valid float number.") from err
    if value < min_value or value > max_value:
        raise OutOfRangeError(value, min_value, max_value)
    return value

def input_y_n(prompt: str, default: YesOrNo = None) -> bool:
    y = ['y', 'yes']
    n = ['n', 'no']

    while True:
        user_input = input(prompt).strip().lower()

        if user_input in y:
            return True
        elif user_input in n:
            return False
        elif user_input == "":
            if default is not None:
                return bool(default.value)
            else:
                print("Eingabe darf nicht leer sein. Bitte geben Sie 'y' oder 'n' ein.")
        else:
            print("Ungültige Eingabe. Bitte geben Sie 'y' oder 'n' ein.")
