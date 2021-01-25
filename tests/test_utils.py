"""
Utility module for tests.
"""
import os

from networkx import Graph

from agh_graphs.utils import gen_name

visualize_tests = 'VISUALIZE_TESTS' in os.environ and os.environ['VISUALIZE_TESTS'] == 'true'
