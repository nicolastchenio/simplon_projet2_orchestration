"""Business logic module containing basic mathematical operations.

DataFrame utilities.
"""

from typing import Union

import pandas as pd

Number = Union[int, float]


def add(a: Number, b: Number) -> Number:
    """Add two numbers.

    Args:
        a (Number): First number.
        b (Number): Second number.

    Returns:
        Number: Sum of a and b.

    """
    return a + b


def sub(a: Number, b: Number) -> Number:
    """Subtract two numbers.

    Args:
        a (Number): First number.
        b (Number): Second number.

    Returns:
        Number: Result of a minus b.

    """
    return a - b


def square(a: Number) -> Number:
    """Return the square of a number.

    Args:
        a (Number): Input number.

    Returns:
        Number: Square of a.

    """
    return a * a


def print_data(df: pd.DataFrame) -> int:
    """Print a DataFrame and return the number of rows.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        int: Number of rows in the DataFrame.

    """
    print(df)
    return len(df)
