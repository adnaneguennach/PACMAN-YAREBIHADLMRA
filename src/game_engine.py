import pygame
from mazegenerator import MazeGenerator

from src.config import ConfigParser
from src.events import LEVEL_CLEARED, PLAYER_DIED, EventManager
from src.maze import Maze
from src.states import (CELL_SIZE, GameOverState, MenuState, PlayingState,
                        StateMachine, TransitionState, VictoryState)

FPS = 60
DEFAULT_LIVES = 3


class GameEngine:
    def __init__(self, config_path):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.config = ConfigParser(config_path).parsing_data()
        self.levels = self.config["levels"]

        self.running = True
        self.deltatime = 0.0
        self.level_index = 0
        self.score = 0
        self.lives = self.config.get("lives", DEFAULT_LIVES)

        self.states = StateMachine()
        self.states.add("menu", MenuState(self))
        self.states.add("playing", PlayingState(self))
        self.states.add("transition", TransitionState(self))
        self.states.add("game_over", GameOverState(self))
        self.states.add("victory", VictoryState(self))

        self.events = EventManager()
        self.events.on(pygame.QUIT, self._on_quit)
        self.events.on(pygame.KEYDOWN, self._on_keydown)
        self.events.on(PLAYER_DIED, self._on_player_died)
        self.events.on(LEVEL_CLEARED, self._on_level_cleared)

    # ---------- levels ----------

    def current_level(self):
        return self.levels[self.level_index]

    def build_maze(self, level):
        walls = MazeGenerator(
            size=(level["width"], level["height"]), perfect=False
        ).maze
        return Maze(walls, CELL_SIZE, self.screen.get_size())

    def new_game(self):
        self.level_index = 0
        self.score = 0
        self.lives = self.config.get("lives", DEFAULT_LIVES)
        self.states.change("transition", message="Get ready!")

    def change_level(self, message):
        self.states.change("transition", message=message)

    # ---------- event handlers ----------

    def _on_quit(self, event):
        self.running = False

    def _on_keydown(self, event):
        if event.key == pygame.K_ESCAPE:
            self.running = False
        else:
            self.states.current.handle_event(event)

    def _on_player_died(self, event):
        self.lives -= 1
        if self.lives <= 0:
            self.states.change("game_over")
            return
        # Player died: switch to the next level (wraps to the first one).
        self.level_index = (self.level_index + 1) % len(self.levels)
        self.change_level("You died! Switching level...")

    def _on_level_cleared(self, event):
        self.level_index += 1
        if self.level_index >= len(self.levels):
            self.states.change("victory")
        else:
            self.change_level("Level cleared!")

    # ---------- main loop ----------

    def run(self):
        clock = pygame.time.Clock()
        self.states.change("menu")
        while self.running:
            self.deltatime = clock.tick(FPS) / 1000
            self.events.process()
            self.states.current.update(self.deltatime)
            self.states.current.draw(self.screen)
            pygame.display.flip()
        pygame.quit()