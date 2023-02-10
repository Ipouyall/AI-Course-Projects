"""search algorithms for graphs"""

from .types import *
from .BFS import *
from .IDS import *
from .A_star import *


def initialize_from_file(filename) -> Graph:
    """
    read information from a file
    :returns: graph, start_node
    """

    with open(filename, 'r') as f:
        vertices_c, edges_c = map(int, f.readline().split())
        graph = Graph(vertices_c)
        # read edges
        for _ in range(edges_c):
            v1, v2 = map(int, f.readline().split())
            graph.add_edge(v1, v2)

        hard_nodes_c = int(f.readline().strip())
        # read hard nodes
        for h_node in list(map(int, f.readline().split())):
            graph.add_hard_node(int(h_node))

        number_of_ary = int(f.readline().strip())
        # read ary
        for _ in range(number_of_ary):
            nodes = list(map(int, f.readline().split()))
            graph.add_consumer(nodes[0], nodes[2:])

        start_node = int(f.readline().strip()) - 1
        graph.set_start(start_node)

    return graph
