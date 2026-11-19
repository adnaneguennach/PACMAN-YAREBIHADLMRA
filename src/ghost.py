import random
from collections import deque

import pygame

from src.maze import Maze
from src.player import Player
from src.tools import Tools

REVIVE_TIME = 6
SCARED_SPRITE = "assets/ghost_images/powerup.png"
RETURN_SPRITE = "assets/ghost_images/ghost_return.png"
DEAD_SPRITE = "assets/ghost_images/dead.png"

_sprite_cache = {}


def _load_sprite(path, size):
    """Load and scale a sprite once; every later call reuses the surface."""
    key = (path, size)
    sprite = _sprite_cache.get(key)
    if sprite is None:
        sprite = pygame.image.load(path).convert_alpha()
        sprite = pygame.transform.scale(sprite, (size, size))
        _sprite_cache[key] = sprite
    return sprite


class Ghost:
    def __init__(self, x, y, speed, maze: Maze):
        self.maze = maze
        self.x = x
        self.y = y
        self.default_x = x
        self.default_y = y
        self.px, self.py = self.maze.cell_to_pixel(self.x, self.y)
        self.speed = speed
        self.dead_speed = speed * 4

        self.target_x = x
        self.target_y = y
        self.target_px = self.px
        self.target_py = self.py

        self.seen = deque(maxlen=3)
        self.range = []

        self.player_detectet_in_zone = False
        self.scared = False
        self.eaten = False
        self.start_to_return = False

        self.dead_timer = 0

    # ---------- movement helpers ----------

    def _advance(self, speed, deltatime):
        """Slide toward the target cell.

        Returns True when the ghost is standing exactly on the target cell
        (so the caller can pick the next one), False while still travelling.
        """
        step = speed * deltatime * self.maze.cell_size
        dx = self.target_px - self.px
        dy = self.target_py - self.py
        dist = (dx**2 + dy**2) ** 0.5

        if dist <= step:
            self.px, self.py = self.target_px, self.target_py
            self.x, self.y = self.target_x, self.target_y
            return True
        self.px += (dx / dist) * step
        self.py += (dy / dist) * step
        return False

    def _set_target(self, cell):
        """Aim at a cell next to the one the ghost is standing on."""
        nx, ny = self.maze.get_dir(cell[0], cell[1], self.x, self.y)
        self.target_x = self.x + nx
        self.target_y = self.y + ny
        self.target_px, self.target_py = self.maze.cell_to_pixel(
            self.target_x, self.target_y
        )

    # ---------- behaviours ----------

    def random_move(self, deltatime):
        if not self._advance(self.speed, deltatime):
            return
        neighbors = self.maze.reachable_neighbors(self.x, self.y)
        if not neighbors:
            return
        unseen = [n for n in neighbors if n not in self.seen]
        choice = random.choice(unseen or neighbors)
        self.seen.append(choice)
        self._set_target(choice)

    def chassing(self, deltatime, player: Player):
        if not self._advance(self.speed, deltatime):
            return
        next_step = Tools.next_step_bfs(
            (self.x, self.y), (player.x, player.y), self.maze
        )
        if next_step:  # None when ghost and player share a cell
            self._set_target(next_step)

    def running(self, deltatime, player: Player):
        if (self.x, self.y) not in self.range:
            return
        if not self._advance(self.speed, deltatime):
            return
        best_neighbor = None
        best_len = -1
        for neighbor in self.maze.reachable_neighbors(self.x, self.y):
            path = Tools.shortest_path(neighbor, (player.x, player.y), self.maze)
            if path and len(path) > best_len:
                best_len = len(path)
                best_neighbor = neighbor
        if best_neighbor is not None:
            self._set_target(best_neighbor)

    def to_start_and_freez(self, deltatime):
        if not self._advance(self.dead_speed, deltatime):
            return
        home = (self.default_x, self.default_y)
        if (self.x, self.y) == home:
            return
        next_step = Tools.next_step_bfs((self.x, self.y), home, self.maze)
        if next_step:
            self._set_target(next_step)

    # ---------- state ----------

    def touching(self, player: Player):
        """The one place that decides "ghost and player are touching"."""
        return Tools._touching_player(self, player)

    def eat(self):
        self.eaten = True
        self.dead_timer = 0

    def revive(self):
        self.x, self.y = self.default_x, self.default_y
        self.px, self.py = self.maze.cell_to_pixel(self.x, self.y)
        self.target_x, self.target_y = self.x, self.y
        self.target_px, self.target_py = self.px, self.py
        self.seen.clear()
        self.dead_timer = 0
        self.eaten = False
        self.player_detectet_in_zone = False

    def update(self, deltatime, player: Player, power_ending=False):
        """Move the ghost. Collisions and the power timer live in PlayingState."""
        Tools.check_player_in_zone(self, player)

        if self.eaten:
            self.to_start_and_freez(deltatime)
            self.dead_timer += deltatime
            if self.dead_timer >= REVIVE_TIME:
                self.revive()
        elif self.player_detectet_in_zone:
            if player.power:
                self.running(deltatime, player)
            else:
                self.chassing(deltatime, player)
        else:
            self.random_move(deltatime)

        self.scared = player.power and not self.eaten
        self.start_to_return = self.scared and power_ending

    # ---------- drawing ----------

    def sprite_path(self, normal_png):
        if self.eaten:
            return DEAD_SPRITE
        if self.start_to_return:
            return RETURN_SPRITE
        if self.scared:
            return SCARED_SPRITE
        return normal_png

    def draw(self, screen, normal_png):
        cell = self.maze.cell_size
        sprite = _load_sprite(self.sprite_path(normal_png), cell - cell // 4)
        screen.blit(sprite, (self.px + cell // 6, self.py + cell // 6))
