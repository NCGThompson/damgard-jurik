#!/usr/bin/env python3
"""
test.py
Boucher, Govedič, Saowakon, Swanson 2019

Runs all unit tests.

"""
import unittest

if __name__ == "__main__":
    test_suite = unittest.TestLoader().discover(start_dir='.')
    unittest.TextTestRunner(verbosity=1).run(test_suite)
