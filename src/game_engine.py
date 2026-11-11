import pygame
from mazegenerator import MazeGenerator

from src.config import ConfigParser
from src.maze_rendering import EAST, NORTH, SOUTH, WEST, Maze
from src.player import Player
from src.ghost import Ghost

FPS = 60
CELL_SIZE = 40
PLAYER_SPEED = 4

KEY_TO_DIRECTION = {
    pygame.K_UP: NORTH,
    pygame.K_RIGHT: EAST,
    pygame.K_DOWN: SOUTH,
    pygame.K_LEFT: WEST,
}


class GameEngine:
    def __init__(self, config_path):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        level = ConfigParser(config_path).parsing_data()["levels"][0]
        walls = MazeGenerator(
            size=(level["width"], level["height"]), perfect=False
        ).maze

        self.maze = Maze(walls, CELL_SIZE, self.screen.get_size())
        player_x, player_y = self.maze.center
        self.player = Player(player_x, player_y, PLAYER_SPEED, self.maze)
        ghost_x, ghost_y = self.maze.corners[0]
        self.ghost = Ghost(ghost_x, ghost_y, 4, self.maze)

    def run(self):
        clock = pygame.time.Clock()
        while self._handle_events():
            deltatime = clock.tick(FPS) / 1000
            self.player.update(deltatime)
            self.ghost.update(deltatime, self.player)
            self._draw(deltatime)
        pygame.quit()

    def _handle_events(self):
        """Process input. Returns False when the game should quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key in KEY_TO_DIRECTION:
                    self.player.next_dir = KEY_TO_DIRECTION[event.key]
        return True

    def _draw(self, deltatime):
        self.screen.fill("black")
        self.maze.draw(self.screen)
        self.player.draw_and_switch(self.screen, deltatime)
        self.ghost.draw(self.screen, "assets/ghost_images/red.png")
        pygame.display.flip()
