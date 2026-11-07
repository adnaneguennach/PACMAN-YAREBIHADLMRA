import pygame
from mazegenerator import MazeGenerator

from src.config import ConfigParser
from src.maze_rendering import EAST, NORTH, SOUTH, WEST, MazeRendering
from src.player import Player

FPS = 60
CELL_SIZE = 40
PLAYER_SPEED = 4  # cells per second

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

        self.maze = MazeRendering(walls, CELL_SIZE, self.screen.get_size())
        x, y = self.maze.maze_adapter.center
        px, py = self.maze.maze_adapter.cell_to_pixel(x, y)
        self.player = Player(x, y, px, py, PLAYER_SPEED, self.maze.maze_adapter)

    def run(self):
        clock = pygame.time.Clock()
        while self._handle_events():
            self.player.update(clock.tick(FPS) / 1000)
            self._draw()
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
                    # FIX: Player reads `next_dir`, not `next_direction`
                    self.player.next_dir = KEY_TO_DIRECTION[event.key]
        return True

    def _draw(self):
        self.screen.fill("black")
        self.maze.draw(self.screen)
        self.player.draw(self.screen)  # FIX: was commented out
        pygame.display.flip()
