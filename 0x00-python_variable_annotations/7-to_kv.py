#!/usr/bin/env python3
"""Task 7 to tuple module"""
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """returns a tuple"""
    return (k, float(v**2))
