#!/usr/bin/env python3
"""Parameterized unit test module
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """ A parameterized unit test class """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected_output):
        """ '' """
        self.assertEqual(access_nested_map(nested_map, path), expected_output)

    @parameterized.expand([
        ({}, ("a",), "KeyError('a',)"),
        ({"a": 1}, ("a", "b"), "KeyError('b',)"),
    ])
    def test_access_nested_map_exception(
            self,
            nested_map,
            path,
            expected_output
            ):
        """ '' """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), expected_output)
