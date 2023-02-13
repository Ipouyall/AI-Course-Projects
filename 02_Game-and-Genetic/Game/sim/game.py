import turtle
import math
import random
from time import sleep

from .agent import PlayerAgent


class Sim:
    GUI = False
    screen = None
    selection = []
    turn = ''
    dots = []
    red = []
    blue = []
    available_moves = []
    minimax_depth = 0
    wait_time = 0.3

    def __init__(self, minimax_depth, prune=False, gui=False):
        self.GUI = gui
        self.prune = prune
        self.minimax_depth = minimax_depth
        if self.GUI:
            self._setup_screen()

    def _setup_screen(self):
        self.screen = turtle.Screen()
        self.screen.setup(800, 800)
        self.screen.title("Game of SIM")
        self.screen.setworldcoordinates(-1.5, -1.5, 1.5, 1.5)
        self.screen.tracer(0, 0)
        turtle.hideturtle()

    @staticmethod
    def _draw_dot(x, y, color):
        turtle.up()
        turtle.goto(x, y)
        turtle.color(color)
        turtle.dot(15)

    @staticmethod
    def _gen_dots():
        return [
            (math.cos(math.radians(angle)), math.sin(math.radians(angle)))
            for angle in range(0, 360, 60)
        ]

    def _initialize_game(self):
        self.selection = []
        self.available_moves = []
        for i in range(0, 6):
            for j in range(i, 6):
                if i != j:
                    self.available_moves.append((i, j))
        if random.randint(0, 2) == 1:
            self.turn = 'red'
        else:
            self.turn = 'blue'
        self.dots = self._gen_dots()
        self.red = []
        self.blue = []
        if self.GUI:
            turtle.clear()
        self._draw()

    @staticmethod
    def _draw_line(p1, p2, color):
        turtle.up()
        turtle.pensize(3)
        turtle.goto(p1)
        turtle.down()
        turtle.color(color)
        turtle.goto(p2)

    def _draw_board(self):
        for i in range(len(self.dots)):
            if i in self.selection:
                self._draw_dot(self.dots[i][0], self.dots[i][1], self.turn)
            else:
                self._draw_dot(self.dots[i][0], self.dots[i][1], 'dark gray')

    def _show_triangle_point(self, winner, *triangle_points):
        if not self.GUI:
            return
        color = 'dark ' + self._swap_turn(winner)
        dots = set()
        for point in triangle_points:
            dots.add(point[0])
            dots.add(point[1])
            self._draw_line(
                (math.cos(math.radians(point[0] * 60)), math.sin(math.radians(point[0] * 60))),
                (math.cos(math.radians(point[1] * 60)), math.sin(math.radians(point[1] * 60))),
                color,
            )
        for dot in dots:
            self._draw_dot(
                math.cos(math.radians(dot * 60)),
                math.sin(math.radians(dot * 60)),
                color)
        self.screen.update()
        sleep(Sim.wait_time)

    def _draw(self):
        if not self.GUI:
            return

        self._draw_board()
        for i in range(len(self.red)):
            self._draw_line(
                (math.cos(math.radians(self.red[i][0] * 60)), math.sin(math.radians(self.red[i][0] * 60))),
                (math.cos(math.radians(self.red[i][1] * 60)), math.sin(math.radians(self.red[i][1] * 60))),
                'red',
            )
        for i in range(len(self.blue)):
            self._draw_line(
                (math.cos(math.radians(self.blue[i][0] * 60)), math.sin(math.radians(self.blue[i][0] * 60))),
                (math.cos(math.radians(self.blue[i][1] * 60)), math.sin(math.radians(self.blue[i][1] * 60))),
                'blue',
            )
        self.screen.update()
        if Sim.wait_time:
            sleep(Sim.wait_time)

    def minimax(self, depth, player_turn):
        agent = PlayerAgent(
            available_moves=self.available_moves,
            red_moves=self.red,
            blue_moves=self.blue,
        )
        if self.prune:
            agent.enable_harassment()
        else:
            agent.disable_harassment()
        return agent.minimax(depth, player_turn)[1]

    def _blue_agent(self):
        return random.choice(self.available_moves)

    def _play(self):
        if self.turn == 'red':
            selection = self.minimax(depth=self.minimax_depth, player_turn=self.turn)
        else:
            selection = self._blue_agent()

        if selection[1] < selection[0]:
            selection = (selection[1], selection[0])
        if selection in self.red or selection in self.blue:
            raise Exception("Duplicate Move!!!")

        return selection

    def play_game(self):
        self._initialize_game()
        while True:
            selection = self._play()
            if self.turn == 'red':
                self.red.append(selection)
            else:
                self.blue.append(selection)
            self.available_moves.remove(selection)
            self.turn = self._swap_turn(self.turn)
            self._draw()
            r = self._game_over(self.red, self.blue)
            if r != 0:
                return r

    @staticmethod
    def _swap_turn(turn):
        return 'red' if turn == 'blue' else 'blue'

    def _game_over(self, r, b):
        r.sort()
        for i in range(len(r) - 2):
            for j in range(i + 1, len(r) - 1):
                for k in range(j + 1, len(r)):
                    if r[i][0] == r[j][0] and r[i][1] == r[k][0] and r[j][1] == r[k][1]:
                        self._show_triangle_point('blue', r[i], r[j], r[k])
                        return 'blue'
        b.sort()
        for i in range(len(b) - 2):
            for j in range(i + 1, len(b) - 1):
                for k in range(j + 1, len(b)):
                    if b[i][0] == b[j][0] and b[i][1] == b[k][0] and b[j][1] == b[k][1]:
                        self._show_triangle_point('red', b[i], b[j], b[k])
                        return 'red'
        return 0
