"""
you can run this module in following format:
python -m sim <depth> <prune> <gui> <rounds>
"""
import argparse
from tqdm import tqdm

from sim import *

parser = argparse.ArgumentParser(description="Optional configs to run a simulation of the game.")
parser.add_argument("--depth", type=int, nargs="?", default=3, help="depth of minimax algorithm")
parser.add_argument("--prune", action='store_true', help="whether to prune the minimax tree")
parser.add_argument("--gui", action='store_true', help="whether to show the gui")
parser.add_argument("--r", type=int, nargs="?", default=10, help="number of rounds to play")

args = parser.parse_args()

game = Sim(
    minimax_depth=args.depth,
    prune=args.prune,
    gui=args.gui
)

results = {"red": 0, "blue": 0}

for bar in tqdm(range(args.r)):
    results[game.play_game()] += 1

print(results)
