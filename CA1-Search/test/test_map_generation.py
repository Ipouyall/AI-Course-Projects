import unittest
import search


class TestGraph(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = search.initialize_from_file("sample1.txt")

    def test_start(self):
        self.assertEqual(self.graph.start_node, 0)

    def test_nodes(self):
        self.assertEqual(self.graph.node_count, 11)

    def test_edges(self):
        self.assertEqual(self.graph.edges[0], [2])
        self.assertEqual(self.graph.edges[1], [2, 3])
        self.assertEqual(self.graph.edges[2], [0, 1, 3, 9])
        self.assertEqual(self.graph.edges[3], [1, 2, 4, 7])
        self.assertEqual(self.graph.edges[4], [3, 5, 6])
        self.assertEqual(self.graph.edges[5], [4, 6])
        self.assertEqual(self.graph.edges[6], [4, 5, 7, 9])
        self.assertEqual(self.graph.edges[7], [3, 6, 8])
        self.assertEqual(self.graph.edges[8], [7, 10])
        self.assertEqual(self.graph.edges[9], [2, 6, 10])
        self.assertEqual(self.graph.edges[10], [8, 9])

    def test_morid(self):
        self.assertEqual(self.graph.recipes[7], [4, 10], "testing morid's recipes")

    def test_hard_nodes(self):
        self.assertEqual(self.graph.hard_nodes, [9])


if __name__ == '__main__':
    unittest.main()
