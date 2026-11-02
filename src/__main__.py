from src.game_engine import GameEngine
from src.player import Player
import sys


class Pacman:
    def __init__(self):
        pass

    def main_loop(self):
        if len(sys.argv) < 1:
            return "Config file not found"

        config_file = sys.argv[1]
        obj_maze = GameEngine(config_file)
        print(obj_maze.draw_maze())


if __name__ == "__main__":
    pac_obj = Pacman()
    pac_obj.main_loop()
