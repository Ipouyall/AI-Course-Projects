from dataclasses import dataclass


def makes_triangle(point: tuple[int, int], points: tuple[tuple[int, int]]):
    for p in points:
        if point[0] in p or point[1] in p:
            other_ep = point[0] if point[1] in p else point[1], p[0] if p[1] in point else p[1]
            for p2 in points:
                if other_ep[0] in p2 and other_ep[1] in p2:
                    return True
    return False


def is_triangle(p1, p2, p3):
    return p1[0] == p2[0] and ((p1[1] == p3[0] and p2[1] == p3[1]) or (p1[1] == p3[1] and p2[1] == p3[0]))


def has_triangle(points: set[tuple[int, int]]):
    if len(points) < 3:
        return False
    sorted_points = [sorted(p) for p in points]
    for i in range(len(sorted_points) - 2):
        for j in range(i + 1, len(sorted_points) - 1):
            for k in range(j + 1, len(sorted_points)):
                if is_triangle(sorted_points[i], sorted_points[j], sorted_points[k]):
                    return True
    return False


def game_overed(red_points: set[tuple[int, int]], blue_points: set[tuple[int, int]]):
    if has_triangle(red_points):
        return 'blue'
    if has_triangle(blue_points):
        return 'red'
    return ''


@dataclass
class State:
    available_moves: set[tuple[int, int]]
    red_moves: set[tuple[int, int]]
    blue_moves: set[tuple[int, int]]
    compiled: str = ''

    @staticmethod
    def _get_valid_moves(moves, available_moves: set[tuple[int, int]]) -> set[tuple[int, int]]:
        valid_moves = set()
        for move in available_moves:
            if not makes_triangle(move, moves):
                valid_moves.add(move)
        return valid_moves

    def _compile_red(self):
        if 'r' in self.compiled:
            return
        self.compiled = "red," + self.compiled
        valid_red_moves = self._get_valid_moves(self.red_moves, self.available_moves)
        self.red_greedy_moves = self._get_valid_moves(self.blue_moves, valid_red_moves)
        self.red_helper_moves = valid_red_moves - self.red_greedy_moves

    def _compile_blue(self):
        if 'b' in self.compiled:
            return
        self.compiled = "blue," + self.compiled
        valid_blue_moves = self._get_valid_moves(self.blue_moves, self.available_moves)
        self.blue_greedy_moves = self._get_valid_moves(self.red_moves, valid_blue_moves)
        self.blue_helper_moves = valid_blue_moves - self.blue_greedy_moves

    def compile(self):
        self._compile_red()
        self._compile_blue()

    def _next_state(self, turn='r', greedy=True):
        if 'r' == turn:
            self._compile_red()
            if greedy:
                moves = self.red_greedy_moves
            else:
                moves = self.red_helper_moves
        elif 'b' == turn:
            self._compile_blue()
            if greedy:
                moves = self.blue_greedy_moves
            else:
                moves = self.blue_helper_moves
        else:
            raise ValueError(f"Invalid turn {turn}")
        for move in moves:
            if turn == 'r':
                yield move, State(
                    available_moves=self.available_moves - {move},
                    red_moves=self.red_moves.union({move}),
                    blue_moves=self.blue_moves,
                )
            else:
                yield move, State(
                    available_moves=self.available_moves - {move},
                    red_moves=self.red_moves,
                    blue_moves=self.blue_moves.union({move}),
                )

    def next_state(self, turn='r'):
        for item in self._next_state(turn, True):
            yield item
        for item in self._next_state(turn, False):
            yield item
