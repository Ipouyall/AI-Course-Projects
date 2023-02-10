from .types import *
from sys import getrecursionlimit, setrecursionlimit

setrecursionlimit(1_000_000_000)


def _dls(test_goal: callable, state: State, transition_function: callable,
         remaining_depth: int, explored: set, path: tuple = ()):
    if remaining_depth <= 0:
        return None
    if (remaining_depth, state) in explored:
        return None

    explored.add((remaining_depth, state))
    if test_goal(state):
        return state, path

    for moved, next_state in transition_function(state):
        if next_state not in explored:
            t_path = path
            if moved:
                t_path = path + (next_state.current_node,)
            result = _dls(test_goal, next_state, transition_function, remaining_depth - 1, explored, t_path)
            if result is not None:
                return result[0], result[1]
    return None


def ids(start_state: State, goal_test: callable, transition_function: callable):
    explored = set()
    for depth in range(1, getrecursionlimit()):
        visited_state = set()
        result = _dls(goal_test, start_state, transition_function,
                      depth, visited_state, (start_state.current_node,))
        explored.update(visited_state)
        if result is not None:
            return result[0], len(explored), normalize_path(result[1])

    print(f"sorry, we can't find a solution for this graph, please try another graph...")
    print(f"the maximum depth we can search is {getrecursionlimit()} and we have searched all of them")
    return None, len(explored), None
