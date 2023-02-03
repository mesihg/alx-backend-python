#!/usr/bin/env python3
"""Task 6 sum of integers and floats module"""
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """sum of a list of integers and floating numbers"""
    return float(sum(mxd_lst))
