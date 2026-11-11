from src.maze_rendering import Maze
from src.player import Player
from collections import deque
from src.tools import Tools
import random
import pygame


class Ghost:
    def __init__(self, x, y, speed, maze: Maze):
        self.maze = maze
        self.x = x
        self.y = y
        self.px, self.py = self.maze.cell_to_pixel(self.x, self.y)
        self.speed = speed

        self.target_x = x
        self.target_y = y
        self.target_px = self.px
        self.target_py = self.py
        self.seen = deque()

    def _touching_player(self, player: Player):
        dx = self.px - player.px
        dy = self.py - player.py
        dist = (dx**2 + dy**2) ** 0.5
        return dist <= self.maze.cell_size // 2

    def random_move(self, deltatime, player: Player):
        if self._touching_player(player):
            print("looooooooser")
            exit()
        step = self.speed * deltatime * self.maze.cell_size
        dx = self.target_px - self.px
        dy = self.target_py - self.py
        dist = (dx**2 + dy**2) ** 0.5

        if dist <= step:
            self.x = self.target_x
            self.y = self.target_y
            self.px = self.target_px
            self.py = self.target_py

            neighbors = self.maze.reachable_neighbors(self.x, self.y)
            if not neighbors:
                return
            unseen = [n for n in neighbors if n not in self.seen]
            choises = unseen if unseen else neighbors
            x, y = random.choice(choises)
            if len(self.seen) < 3:
                self.seen.append((x, y))
            else:
                self.seen.popleft()
                self.seen.append((x, y))

            nx, ny = self.maze.get_dir(x, y, self.target_x, self.target_y)
            self.target_x = self.x + nx
            self.target_y = self.y + ny
            self.target_px, self.target_py = self.maze.cell_to_pixel(
                self.target_x, self.target_y
            )

        else:
            self.px += (dx / dist) * step
            self.py += (dy / dist) * step

    def chassing(self, deltatime, player: Player):
        if self._touching_player(player):
            print("loseeeeeeer")
            exit()

        step = self.speed * self.maze.cell_size * deltatime
        dx = self.target_px - self.px
        dy = self.target_py - self.py
        dist = (dx**2 + dy**2) ** 0.5

        if dist <= step:
            self.px = self.target_px
            self.py = self.target_py
            self.x = self.target_x
            self.y = self.target_y

            next_step = Tools.next_step_bfs(
                (self.x, self.y), (player.x, player.y), self.maze
            )
            if not next_step:
                return

            nx, ny = self.maze.get_dir(*next_step)
            self.target_x = self.x + nx
            self.target_y = self.y + ny
            self.target_px, self.target_py = self.maze.cell_to_pixel(
                self.target_px, self.target_py
            )
        else:
            self.px += (dx / dist) * step
            self.py += (dy / dist) * step


    def update(self, deltatime, player: Player):
        # if player_detectet_in_zone:
        #     self.chassing(deltatime, player)
        self.random_move(deltatime, player)

    def draw(self, screen, ghost_png):
        self.spirite = pygame.image.load(ghost_png)
        self.spirite = pygame.transform.scale(
            self.spirite,
            (
                self.maze.cell_size - self.maze.cell_size // 4,
                self.maze.cell_size - self.maze.cell_size // 4,
            ),
        )
        screen.blit(
            self.spirite,
            (
                self.px + self.maze.cell_size // 6,
                self.py + self.maze.cell_size // 6,
            ),
        )
