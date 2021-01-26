import unittest

from networkx import Graph

from agh_graphs.utils import sort_segments_by_angle, angle_with_x_axis


class UtilsTest(unittest.TestCase):
    def test_angle_with_x_axis(self):
        self.assertEqual(45, angle_with_x_axis((0, 0), (1, 1)))
        self.assertEqual(45, angle_with_x_axis((1, 0), (2, 1)))
        self.assertEqual(45, angle_with_x_axis((1, 1), (2, 2)))
        self.assertEqual(0, angle_with_x_axis((1, 1), (1, 1)))
        self.assertEqual(90, angle_with_x_axis((0, 0), (0, 10)))
        self.assertEqual(90, angle_with_x_axis((0, 0), (0, -10)))
        self.assertEqual(90, angle_with_x_axis((0, -10), (0, 0)))
        self.assertEqual(135, angle_with_x_axis((2, -2), (-10, 10)))
        self.assertEqual(135, angle_with_x_axis((5, 5), (6, 4)))
        self.assertEqual(135, angle_with_x_axis((6, 4), (5, 5)))

    def test_sort_segments_by_angle(self):
        graph = Graph()
        graph.add_node('a', layer=0, position=(3, 3), label='x')
        graph.add_node('b', layer=0, position=(2, 3), label='x')
        graph.add_node('c', layer=0, position=(2, 2), label='x')

        sorted_segments = sort_segments_by_angle(graph, [('a', 'b'), ('b', 'c'), ('c', 'a')])
        self.assertEqual(('a', 'b'), sorted_segments[0])
        self.assertEqual(('c', 'a'), sorted_segments[1])
        self.assertEqual(('b', 'c'), sorted_segments[2])

        sorted_segments = sort_segments_by_angle(graph, [('b', 'a'), ('b', 'c'), ('a', 'c')])
        self.assertEqual(('b', 'a'), sorted_segments[0])
        self.assertEqual(('a', 'c'), sorted_segments[1])
        self.assertEqual(('b', 'c'), sorted_segments[2])
