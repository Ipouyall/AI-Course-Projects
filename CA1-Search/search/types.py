"""contains the types used in the search module"""
from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class State:
    current_node: int
    remaining_time: int
    collected_recipes: tuple
    satisfied_consumer: tuple
    impassible_nodes_visits: tuple
    time: int

    def __eq__(self, other):
        return (self.current_node, self.remaining_time, self.collected_recipes, self.satisfied_consumer) \
               == \
               (other.current_node, other.remaining_time, other.collected_recipes, other.satisfied_consumer)

    def __hash__(self):
        return hash((
            self.current_node,
            self.remaining_time,
            self.collected_recipes,
            self.satisfied_consumer))


def _additional_impassible_node_cost(n: int):
    if n <= 1:
        return 0
    return (n * (n - 1)) / 2


class Graph:
    """graph class"""

    def __init__(self, nodes_count: int):
        self.node_count = nodes_count
        self.edges = defaultdict(list)
        self.hard_nodes = []
        self.number_of_consumers = None
        self.recipes = defaultdict(list)
        self.start_node = None
        self._aggregated_recipes = set()

    def add_edge(self, from_node: int, to_node: int):
        """add edge to graph"""
        from_node, to_node = from_node - 1, to_node - 1
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)

    def add_hard_node(self, node: int):
        """add hard node to graph"""
        self.hard_nodes.append(node - 1)

    def add_consumer(self, node: int, recipes: list):
        """morid(consumer) exists in node"""
        self.recipes[node - 1] = [int(recipe) - 1 for recipe in recipes]
        self._aggregated_recipes = self._aggregated_recipes.union(set(self.recipes[node - 1]))
        if self.number_of_consumers is None:
            self.number_of_consumers = 1
        else:
            self.number_of_consumers += 1

    def set_start(self, node: int):
        self.start_node = node

    def get_start_state(self):
        visited_hard_nodes = [0] * len(self.hard_nodes)
        if self.start_node in self.hard_nodes:
            visited_hard_nodes[self.start_node] = 1
        return State(
            current_node=self.start_node,
            remaining_time=0,
            collected_recipes=tuple(),
            satisfied_consumer=tuple(),
            impassible_nodes_visits=tuple(visited_hard_nodes),
            time=0
        )

    def get_transition_function(self):
        """get transition function"""
        return self._transition_function

    def _transition_function(self, state):
        """using generator function to get next states"""
        if state.remaining_time > 0:
            yield False, State(
                current_node=state.current_node,
                remaining_time=state.remaining_time - 1,
                collected_recipes=state.collected_recipes,
                satisfied_consumer=state.satisfied_consumer,
                impassible_nodes_visits=state.impassible_nodes_visits,
                time=state.time + 1
            )
        else:
            for node in self.edges[state.current_node]:
                times_visited = state.impassible_nodes_visits
                wait_time = 0
                collected_recipes = state.collected_recipes
                satisfied_consumer = state.satisfied_consumer
                if node in self.hard_nodes:
                    index = self.hard_nodes.index(node)
                    times_visited = list(times_visited)
                    wait_time = times_visited[index]
                    times_visited[index] += 1
                    times_visited = tuple(times_visited)
                if node in self._aggregated_recipes and node not in collected_recipes:
                    collected_recipes = collected_recipes + (node,)
                if node in self.recipes.keys() and node not in satisfied_consumer:
                    if all(recipe in collected_recipes for recipe in self.recipes[node]):
                        satisfied_consumer = satisfied_consumer + (node,)
                yield True, State(
                    current_node=node,
                    remaining_time=wait_time,
                    collected_recipes=collected_recipes,
                    satisfied_consumer=satisfied_consumer,
                    impassible_nodes_visits=times_visited,
                    time=state.time + 1
                )

    def calculate_path_cost(self, path: list):
        """generate transition cost function"""
        total_cost = len(path)
        for node in self.hard_nodes:
            total_cost += _additional_impassible_node_cost(path.count(node))
        return total_cost - 1

    def generate_goal_tester(self):
        """generate goal test function"""

        def goal_test(state: State):
            """is this state a goal?"""
            for node in self._aggregated_recipes:
                if node not in state.collected_recipes:
                    return False
            for node in self.recipes.keys():
                if node not in state.satisfied_consumer:
                    return False
            return True

        return goal_test

    def get_nodes_have_recipe(self) -> set:
        return self._aggregated_recipes

    def get_nodes_have_consumer(self) -> set:
        return set(self.recipes.keys())

    def __str__(self):
        return f"Graph with {self.node_count} nodes and {len(self.edges)} edges\n" + \
               f"Hard nodes: {self.hard_nodes}\n" + \
               f"Recipes: {dict(self.recipes)}\n" + \
               f"Consumers: {list(self.recipes.keys())}\n" + \
               f"Start node: {self.start_node}"

    def __getitem__(self, item: str):
        if item == "start state":
            return self.get_start_state()
        if item == "transition function":
            return self.get_transition_function()
        if item == "goal tester":
            return self.generate_goal_tester()
        if item == "impassible cost":
            return self.calculate_path_cost
        if item == "nodes have recipe":
            return self.get_nodes_have_recipe()
        if item == "nodes have consumer":
            return self.get_nodes_have_consumer()
        raise KeyError(f"item {item} not found")


def path_label(state: State):
    return state.time, state


def normalize_path(path: tuple):
    return tuple(node + 1 for node in path)