"""Scratch file."""

import numpy as np
import pandas as pd


def to_number(obj):
    """Convert an object to a float64."""
    try:
        return float(obj)
    except ValueError:
        return obj


def convert_column_to_float(arr):
    """Convert a numpy array to float64."""
    result = [to_number(x) for x in arr]
    problems = []
    for ind, val in enumerate(result):
        if not isinstance(val, float):
            problems.append((ind, val))

    return result, problems
