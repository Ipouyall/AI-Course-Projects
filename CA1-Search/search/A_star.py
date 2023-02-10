"""A* algorithm implementation and some heuristic functions"""
from .types import *
from heapq import heappush, heappop, heapify


def a_star(start_state: State, goal_test: callable, transition_function: callable, heuristic: callable):
    frontier = []
    heapify(frontier)
    heappush(frontier, (start_state.time + heuristic(start_state), start_state))
    explored = set()
    path = {path_label(start_state): (start_state.current_node,)}

    while frontier:
        current_state = heappop(frontier)[1]
        explored.add(current_state)
        if goal_test(current_state):
            return current_state, len(explored), normalize_path(path[path_label(current_state)])
        for moved, next_state in transition_function(current_state):
            if next_state in explored:
                continue
            labeled_state = (next_state.time + heuristic(next_state), next_state)
            if moved:
                path[path_label(next_state)] = path[path_label(current_state)] + (next_state.current_node,)
            else:
                path[path_label(next_state)] = path[path_label(current_state)]
            heappush(frontier, labeled_state)

    print("couldn't find any answer")
    return None, len(explored), None


def _union_aryan_and_recipes(graph):
    u_recipes = graph.get_nodes_have_recipe()
    aryans = set(graph.recipes.keys())
    return u_recipes.union(aryans)


def generate_satisfaction_base_heuristic(graph, w = 1):
    """
    generate heuristic function for a graph
    this heuristic function is based on path and satisfying consumers
    """
    max_h = len(graph.get_nodes_have_recipe()) + graph.number_of_consumers

    def heuristic(state):
        return (max_h - len(set(state.satisfied_consumer).union(state.collected_recipes))) * w

    return heuristic


def _dist_from_other(graph, node) -> dict:
    """
    calculate distance from node to other nodes
    :param graph: graph
    :param node: node
    :return: distances
    """
    distances = {n: float('inf') for n in range(graph.node_count)}
    distances[node] = 0
    frontier = [node]
    while frontier:
        current_node = frontier.pop()
        for neighbor in graph.edges[current_node]:
            c_cost = distances[current_node] + 1
            if c_cost < distances[neighbor]:
                distances[neighbor] = c_cost
                frontier.append(neighbor)

    return distances


def _satisfiable(unknown_recipes, consumer, recipes):
    return all(recipe not in unknown_recipes for recipe in recipes[consumer])


def generate_path_base_heuristic(graph: Graph, weight: int = 1):
    """
    generate heuristic function for a graph
    this heuristic function is based on path and satisfying consumers
    """
    distances = {}
    for node in range(graph.node_count):
        distances[node] = _dist_from_other(graph, node)

    all_recipes = graph.get_nodes_have_recipe()
    all_consumers = graph.get_nodes_have_consumer()

    def heuristic(state):
        remained_recipes = all_recipes - set(state.collected_recipes)
        remained_consumers = all_consumers - set(state.satisfied_consumer)
        should_visit = remained_recipes.union(remained_consumers)
        current_node = state.current_node

        return weight * _path_cost_helper(
            should_v=should_visit,
            r_recipes=remained_recipes,
            r_consumers=remained_consumers,
            t_recipes=graph.recipes,
            dists=distances,
            c_code=current_node
        )

    return heuristic


def _path_cost_helper(should_v: set, r_recipes: set, r_consumers: set, t_recipes: dict,
                      dists: dict, c_code: int):
    if not should_v:
        return 0

    min_cost = float('inf')

    targets = r_recipes.union(
        {
            consumer for consumer in r_consumers if
            _satisfiable(r_recipes, consumer, t_recipes)
        }
    )
    for node in targets:
        res = dists[c_code][node] + _path_cost_helper(
            should_v - {node},
            r_recipes - {node} if node in r_recipes else r_recipes,
            r_consumers - {node} if node in r_consumers else r_consumers,
            t_recipes,
            dists,
            node,
        )
        if res < min_cost:
            min_cost = res
    return min_cost
