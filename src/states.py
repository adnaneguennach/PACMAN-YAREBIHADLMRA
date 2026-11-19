"""Pygame state machine: menu, playing, level transition, game over, victory."""

import pygame

from src.events import LEVEL_CLEARED, PLAYER_DIED, EventManager
from src.ghost import Ghost
from src.maze import EAST, NORTH, SOUTH, WEST, Maze
from src.player import Player

CELL_SIZE = 40
PLAYER_SPEED = 4
GHOST_SPEED = 3

POWER_DURATION = 6.0  # seconds a power pellet lasts
POWER_WARNING = 4.5   # after this, scared ghosts show the "about to end" sprite

# One entry per maze corner, in the same order as Maze.corners.
GHOST_COLORS = ("red", "pink", "blue", "orange")

KEY_TO_DIRECTION = {
    pygame.K_UP: NORTH,
    pygame.K_RIGHT: EAST,
    pygame.K_DOWN: SOUTH,
    pygame.K_LEFT: WEST,
}

_fonts = {}


def get_font(size):
    """Fonts are loaded from disk, so build each size only once."""
    if size not in _fonts:
        _fonts[size] = pygame.font.Font(None, size)
    return _fonts[size]


class State:
    def __init__(self, game):
        self.game = game

    def enter(self, **kwargs):
        pass

    def exit(self):
        pass

    def handle_event(self, event):
        pass

    def update(self, deltatime):
        pass

    def draw(self, screen):
        pass


class StateMachine:
    def __init__(self):
        self.states = {}
        self.current = None

    def add(self, name, state):
        self.states[name] = state

    def change(self, name, **kwargs):
        if self.current:
            self.current.exit()
        self.current = self.states[name]
        self.current.enter(**kwargs)


class TextState(State):
    """Base for simple full-screen text states."""

    def _text(self, screen, text, size, y_offset=0, color="white"):
        surface = get_font(size).render(text, True, color)
        rect = surface.get_rect(
            center=(screen.get_width() // 2,
                    screen.get_height() // 2 + y_offset)
        )
        screen.blit(surface, rect)


class MenuState(TextState):
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.game.new_game()

    def draw(self, screen):
        screen.fill("black")
        self._text(screen, "PACMAN", 120, -60, "yellow")
        self._text(screen, "Press ENTER to start - ESC to quit", 40, 40)


class TransitionState(TextState):
    DURATION = 1.5

    def enter(self, message="", **kwargs):
        self.message = message
        self.timer = self.DURATION

    def update(self, deltatime):
        self.timer -= deltatime
        if self.timer <= 0:
            self.game.states.change("playing")

    def draw(self, screen):
        screen.fill("black")
        self._text(screen, self.message, 60, -30, "yellow")
        self._text(
            screen,
            f"Level {self.game.level_index + 1} - Lives: {self.game.lives}",
            40, 30,
        )


class EndState(TextState):
    title = ""

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.game.states.change("menu")

    def draw(self, screen):
        screen.fill("black")
        self._text(screen, self.title, 100, -50, "red")
        self._text(screen, f"Score: {self.game.score}", 50, 30)
        self._text(screen, "Press ENTER to return to the menu", 36, 90)


class GameOverState(EndState):
    title = "GAME OVER"


class VictoryState(EndState):
    title = "YOU WIN!"


class PlayingState(State):
    def init_ghosts(self, level):
        speed = level.get("ghost_speed", GHOST_SPEED)
        corners = self.maze.corners[:len(GHOST_COLORS)]
        self.ghosts = [Ghost(x, y, speed, self.maze) for x, y in corners]

    def enter(self, **kwargs):
        level = self.game.current_level()
        self.maze: Maze = self.game.build_maze(level)
        px, py = self.maze.center
        self.player = Player(px, py, PLAYER_SPEED, self.maze)

        self.init_ghosts(level)

        self.power_timer = 0.0
        self.finished = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in KEY_TO_DIRECTION:
            self.player.next_dir = KEY_TO_DIRECTION[event.key]

    def _update_power(self, deltatime):
        """Single power-up clock for the whole level (ghosts only read it)."""
        if self.player.power:
            self.power_timer += deltatime
            if self.power_timer >= POWER_DURATION:
                self.player.power = False
        return self.player.power and self.power_timer >= POWER_WARNING

    def _resolve_ghost_hits(self):
        """Handle every ghost touching the player. True if the player died."""
        for ghost in self.ghosts:
            if ghost.eaten or not ghost.touching(self.player):
                continue
            if self.player.power:
                ghost.eat()
            else:
                self.finished = True
                EventManager.post(PLAYER_DIED)
                return True
        return False

    def update(self, deltatime):
        if self.finished:
            return

        self.player.update(deltatime)

        cell = (round(self.player.x), round(self.player.y))
        score, power = self.maze.eat_pellet(*cell)
        self.game.score += score
        if power:
            self.player.power = True
            self.power_timer = 0.0  # eating another pellet restarts the clock

        power_ending = self._update_power(deltatime)

        for ghost in self.ghosts:
            ghost.update(deltatime, self.player, power_ending)

        if self._resolve_ghost_hits():
            return
        if self.maze.is_cleared():
            self.finished = True
            EventManager.post(LEVEL_CLEARED)

    def draw(self, screen):
        screen.fill("black")
        self.maze.draw(screen)
        self.player.draw_and_switch(screen, self.game.deltatime)
        for ghost, color in zip(self.ghosts, GHOST_COLORS):
            ghost.draw(screen, f"assets/ghost_images/{color}.png")
        hud = f"Score: {self.game.score}   Lives: {self.game.lives}   " \
              f"Level: {self.game.level_index + 1}"
        screen.blit(get_font(32).render(hud, True, "white"), (10, 10))