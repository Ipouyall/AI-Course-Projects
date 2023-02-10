from .types import *
from queue import Queue


def bfs(start_state: State, goal_test: callable, transition_function: callable):
    explored = set()
    frontier = Queue()
    frontier.put(start_state)
    path = {path_label(start_state): (start_state.current_node,)}

    while not frontier.empty():
        current_state = frontier.get()
        if current_state in explored:
            continue
        explored.add(current_state)
        for moved, next_state in transition_function(current_state):
            if next_state in explored:
                continue
            frontier.put(next_state)
            if moved:
                path[path_label(next_state)] = path[path_label(current_state)] + (next_state.current_node,)
                if goal_test(current_state):
                    return current_state, len(explored), normalize_path(path[path_label(current_state)])
                continue
            path[path_label(next_state)] = path[path_label(current_state)]

    print("Error: couldn't find answer")
    return None, len(explored), None
