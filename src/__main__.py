from .maze_rendering import MazeRendering
import sys

class Pacman:
    def __init__(self):
        pass
    
    def main_loop(self):
        if len(sys.argv) < 1:
            return "Config file not found"

        obj_maze = MazeRendering(40, 40, 10)
        config_file = sys.argv[1]
        print(obj_maze.drawing_loop(config_file))



if __name__ == "__main__":
    pac_obj = Pacman()
    pac_obj.main_loop()





