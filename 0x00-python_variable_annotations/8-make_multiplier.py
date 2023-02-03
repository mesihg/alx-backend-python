#!/usr/bin/env python3
"""Task 8 return a multiplier function module"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """returns a multiplier function"""
    return lambda x: x * multiplier
