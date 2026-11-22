import time
import pygame
from mazegenerator import MazeGenerator

from src.config import ConfigParser
from src.maze import EAST, NORTH, SOUTH, WEST, Maze
from src.player import Player
from src.ghost import Ghost

FPS = 60
CELL_SIZE = 40

KEY_TO_DIRECTION = {
    pygame.K_UP: NORTH,
    pygame.K_RIGHT: EAST,
    pygame.K_DOWN: SOUTH,
    pygame.K_LEFT: WEST,
}
GHOST_COLORS = ("red", "pink", "blue", "orange")



# adnane u need to add your states here


class PlayingState:

    def __init__(self, game):
        self.level_rank = 0
        self.init_playing(game)

    @property
    def check_win(self):
        if self.maze is None:
            return False

        super_pacgum_zero = sum(
            sublist.count(0) for sublist in self.maze.super_pacgums
        )
        pacgum_zero = sum(
            sublist.count(0) for sublist in self.maze.pacgums
        )

        if (
            super_pacgum_zero == self.maze.width * self.maze.height
            and pacgum_zero == self.maze.width * self.maze.height
        ):
            return True

        return False

    def init_playing(self, game):
        level = game.config["levels"][self.level_rank]

        walls = MazeGenerator(
            size=(level["width"], level["height"]), perfect=False
        ).maze

        self.maze = Maze(walls, CELL_SIZE, game.screen.get_size())
        self.maze_adapter = self.maze

        player_x, player_y = self.maze.center
        self.player = Player(player_x, player_y, 4, self.maze)

        corners = self.maze.corners
        self.ghosts = [Ghost(x, y, 3, self.maze) for x, y in corners]


    def _handle_playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                if event.key in KEY_TO_DIRECTION:
                    self.player.next_dir = KEY_TO_DIRECTION[event.key]

        return True

    def play(self, game):
        clock = pygame.time.Clock()

        while self._handle_playing_events():
            deltatime = clock.tick(FPS) / 1000

            self.player.update(deltatime)
            for ghost in self.ghosts:
                ghost.update(deltatime, self.player)

            if self.check_win:
                if self.level_rank + 1 < len(game.config["levels"]):
                    self.level_rank += 1
                    self.init_playing(game)
                else:
                    exit()

            self._draw(deltatime, game)

        pygame.quit()

    def _draw(self, deltatime, game):
        game.screen.fill("black")

        self.maze.draw(game.screen)
        self.player.draw_and_switch(game.screen, deltatime)
        for ghost, color in zip(self.ghosts, GHOST_COLORS):
            ghost.draw(game.screen, f"assets/ghost_images/{color}.png", self.player)

        pygame.display.flip()
