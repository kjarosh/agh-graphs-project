"""
Utility module for tests.
"""
import os

visualize_tests = 'VISUALIZE_TESTS' in os.environ and os.environ['VISUALIZE_TESTS'] == 'true'
