import pygame
from enum import Enum
from mazegenerator import MazeGenerator
from config import ConfigParser
import time


TILE_SIZE = 20
COLOR = "blue"

class GameState(Enum):
    start_menu = 0



class GameEngine:
    def __init__(self, config = "config.json"):
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.config = ConfigParser(config).parsing_data()
        self.maze_width = 0
        self.maze_height = 0
        self.offset_x = 0
        self.offset_y = 0

    def _maze_generator(self, w, h):
        maze = MazeGenerator(size=(w, h), perfect = False).maze
        return maze

    def _cell_to_px(self,x, y):
        px = self.offset_x + (x * TILE_SIZE)
        py = self.offset_y + (y * TILE_SIZE)
        return px,py

    def _calculate_maze_size(self,maze):
        self.maze_width = len(maze[0]) * TILE_SIZE
        self.maze_height = len(maze) * TILE_SIZE

        self.offset_x = (self.screen.get_width() - self.maze_width) // 2
        self.offset_y = (self.screen.get_height() - self.maze_height) // 2


    def game_loop(self):

        #we loop over the lvls 
        #create the maze -> render it -> check pacgums all eaten if yes, go to next lvl

        levels = self.config["levels"]
        pygame.init()
        clock = pygame.time.Clock() 

        for i, lvl in enumerate(levels):
            maze = self._maze_generator(lvl["width"], lvl["height"])
            self._calculate_maze_size(maze)
            # print(f"MAZE NUMBER {i}: {maze} #############################\n\n")
            # lvl_done = False
            running = True

            while running:

                self.screen.fill("black")

                for y in range(len(maze)):
                    for x in range(len(maze[0])):
                        cell = maze[y][x]
                        px, py = self._cell_to_px(x, y)

                        if cell & 1:
                            pygame.draw.rect(self.screen, COLOR, (px, py, TILE_SIZE, 2))
                        if cell & 2:
                            pygame.draw.rect(self.screen, COLOR, (px + TILE_SIZE - 2, py, 2, TILE_SIZE))
                        if cell & 4:
                            pygame.draw.rect(self.screen, COLOR, (px, py + TILE_SIZE, TILE_SIZE, 2))

                        if cell & 8:
                            pygame.draw.rect(self.screen, COLOR, (px, py + 2, 2, TILE_SIZE))

                clock.tick(60)
                pygame.display.flip()
                


x = GameEngine()
x.game_loop()












