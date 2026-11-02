import pygame
from mazegenerator import MazeGenerator
from src.config import ConfigParser
from src.maze_rendering import Maze
from src.player import Player


class GameEngine:
    def __init__(self, config_path):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.level = ConfigParser(config_path).parsing_data()["levels"][0]
        self.grid = MazeGenerator(
            size=(self.level["width"], self.level["height"]), perfect=False
        ).maze
        self.maze = Maze(self.screen, self.grid)
        # self.player = Player()

    def update_playing(self, deltatime):
        self.player.update(deltatime)

    def draw_maze(self):
        pygame.init()
        clock = pygame.time.Clock()
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE
                ):
                    running = False

            delta_time = clock.tick(60) / 1000.0
            self.screen.fill("black")
            self.maze.draw()
            # self.update_playing(delta_time)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
