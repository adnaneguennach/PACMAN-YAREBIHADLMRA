"""Pygame state machine: menu, playing, level transition, game over, victory."""

import pygame

from src.events import LEVEL_CLEARED, PLAYER_DIED, EventManager
from src.ghost import Ghost
from src.maze import EAST, NORTH, SOUTH, WEST, Maze
from src.player import Player

CELL_SIZE = 40
PLAYER_SPEED = 4
GHOST_SPEED = 3
HIT_DISTANCE = 0.5  # in cells

KEY_TO_DIRECTION = {
    pygame.K_UP: NORTH,
    pygame.K_RIGHT: EAST,
    pygame.K_DOWN: SOUTH,
    pygame.K_LEFT: WEST,
}


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
        font = pygame.font.Font(None, size)
        surface = font.render(text, True, color)
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
    def __init__(self, game):
        super().__init__(game)
        self.timer = 0

    def init_ghosts(self, level):
        gx, gy = self.maze.corners[0]
        self.red_ghost = Ghost(
            gx, gy, level.get("ghost_speed", GHOST_SPEED), self.maze
        )
        gx, gy = self.maze.corners[1]
        self.pink_ghost = Ghost(
            gx, gy, level.get("ghost_speed", GHOST_SPEED), self.maze
        )
        gx, gy = self.maze.corners[2]
        self.blue_ghost = Ghost(
            gx, gy, level.get("ghost_speed", GHOST_SPEED), self.maze
        )

        gx, gy = self.maze.corners[3]
        self.orange_ghost = Ghost(
            gx, gy, level.get("ghost_speed", GHOST_SPEED), self.maze
        )

    def enter(self):
        level = self.game.current_level()
        self.maze: Maze = self.game.build_maze(level)
        px, py = self.maze.center
        self.player = Player(px, py, PLAYER_SPEED, self.maze)

        self.init_ghosts(level)
        

        self.finished = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in KEY_TO_DIRECTION:
            self.player.next_dir = KEY_TO_DIRECTION[event.key]

    def update(self, deltatime):
        if self.finished:
            return
        self.player.update(deltatime)
        self.red_ghost.update(deltatime, self.player)
        self.blue_ghost.update(deltatime, self.player)
        self.orange_ghost.update(deltatime, self.player)
        self.pink_ghost.update(deltatime, self.player)

        cell = (round(self.player.x), round(self.player.y))
        score, power = self.maze.eat_pellet(*cell)
        self.game.score += score
        

        if power:
            self.player.power = True

        dist = ((self.player.x - self.red_ghost.x) ** 2
                + (self.player.y - self.red_ghost.y) ** 2) ** 0.5
        if dist < HIT_DISTANCE:
            self.finished = True
            EventManager.post(PLAYER_DIED)
        elif self.maze.is_cleared():
            self.finished = True
            EventManager.post(LEVEL_CLEARED)

    def draw(self, screen):
        screen.fill("black")
        self.maze.draw(screen)
        self.player.draw_and_switch(screen, self.game.deltatime)
        self.red_ghost.draw(screen, "assets/ghost_images/red.png", self.player)
        self.blue_ghost.draw(screen, "assets/ghost_images/blue.png", self.player)
        self.orange_ghost.draw(screen, "assets/ghost_images/orange.png", self.player)
        self.pink_ghost.draw(screen, "assets/ghost_images/pink.png", self.player)
        font = pygame.font.Font(None, 32)
        hud = f"Score: {self.game.score}   Lives: {self.game.lives}   " \
              f"Level: {self.game.level_index + 1}"
        screen.blit(font.render(hud, True, "white"), (10, 10))
