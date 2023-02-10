import random

from .state import *


class PlayerAgent:
    enemy_lose = 100000
    enemy_win = -100000
    bonus_score = 1000
    harassment = False

    def __init__(self, available_moves: list[tuple[int, int]], red_moves, blue_moves):
        self.available_moves = available_moves
        self.state = State(
            available_moves=set(available_moves),
            red_moves=set(red_moves),
            blue_moves=set(blue_moves),
        )

    def minimax(self, depth: int, turn: str):
        if turn == 'red':
            results = self.maximizer(
                self.state,
                depth=depth,
                alpha=-1*float('inf'),
                beta=float('inf'),
            )
        else:
            results = self.minimizer(
                self.state,
                depth=depth,
                alpha=-1*float('inf'),
                beta=float('inf'),
            )
        if results[1] is None:
            return results[0], random.choice(self.available_moves)
        return results

    def maximizer(self, state: State, depth: int, **pruning) -> [int, tuple]:
        go = game_overed(state.red_moves, state.blue_moves)
        if go == 'red':
            return PlayerAgent.enemy_lose, None
        elif go == 'blue':
            return PlayerAgent.enemy_win, None

        if len(state.available_moves) == 0:
            return 0, None

        if depth <= 0:
            return PlayerAgent._estimate_score(state), None

        max_score = PlayerAgent.enemy_win
        max_movement = None

        for move, next_state in state.next_state('r'):
            score, _ = self.minimizer(next_state, depth - 1, **pruning)
            if score > max_score:
                max_score = score
                max_movement = move
                if self.harassment:
                    if max_score >= pruning['beta']:
                        break
                    pruning['alpha'] = max(pruning['alpha'], max_score)
        return max_score, max_movement

    def minimizer(self, state: State, depth: int, **pruning) -> [int, tuple]:
        go = game_overed(state.red_moves, state.blue_moves)
        if go == 'red':
            return PlayerAgent.enemy_lose, None
        elif go == 'blue':
            return PlayerAgent.enemy_win, None

        if len(state.available_moves) == 0:
            return 0, None

        if depth <= 0:
            return PlayerAgent._estimate_score(state), None

        min_score = PlayerAgent.enemy_lose
        min_movement = None

        for move, next_state in state.next_state('b'):
            score, _ = self.maximizer(next_state, depth - 1, **pruning)
            if score < min_score:
                min_score = score
                min_movement = move
                if self.harassment:
                    if min_score <= pruning['alpha']:
                        break
                    pruning['beta'] = min(pruning['beta'], min_score)
        return min_score, min_movement

    @staticmethod
    def _estimate_score(state: State) -> int:
        state.compile()
        valid_moves_for_blue = len(state.blue_greedy_moves) + len(state.blue_helper_moves)
        perfect_blue_moves = len(state.blue_greedy_moves)
        valid_moves_for_red = len(state.red_greedy_moves) + len(state.red_helper_moves)
        perfect_red_moves = len(state.red_greedy_moves)
        return \
            valid_moves_for_red - valid_moves_for_blue + \
            (perfect_red_moves - perfect_blue_moves) * PlayerAgent.bonus_score

    def enable_harassment(self):
        self.harassment = True

    def disable_harassment(self):
        self.harassment = False
