import sys

from src.game_engine import GameEngine


class Pacman:
    def main_loop(self):
        if len(sys.argv) < 2:
            print("Error: config file not provided")
            sys.exit(1)

        GameEngine(sys.argv[1]).run()


if __name__ == "__main__":
    Pacman().main_loop()
