import math
import pygame
from src.maze_rendering import Maze


class Player:
    DIRECTION_ANGLES = {1: 270, 2: 0, 4: 90, 8: 180}

    def __init__(self, x, y, speed, maze: Maze):
        self.maze = maze
        self.x = x
        self.y = y
        self.px, self.py = self.maze.cell_to_pixel(self.x, self.y)
        self.speed = speed

        self.target_x = self.x
        self.target_y = self.y
        self.target_px = self.px
        self.target_py = self.py
        self.next_dir = None
        self.current_dir = None

        self.player_images = [
            "assets/player_images/1.png",
            "assets/player_images/2.png",
            "assets/player_images/3.png",
            "assets/player_images/4.png",
        ]
        self.var = 0
        self.index = 0

    def update(self, deltatime):
        step = self.speed * self.maze.cell_size * deltatime
        dx = self.target_px - self.px
        dy = self.target_py - self.py
        dist = (dx**2 + dy**2) ** 0.5
        if dist <= step:
            self.px = self.target_px
            self.py = self.target_py
            self.x = self.target_x
            self.y = self.target_y

            if self.next_dir is not None and self.maze.can_move(
                self.x, self.y, self.next_dir
            ):
                self.current_dir = self.next_dir
                self.next_dir = None
            if self.current_dir is not None and self.maze.can_move(
                self.x, self.y, self.current_dir
            ):
                nx, ny = self.maze.get_cor(self.current_dir)
                self.target_x = self.x + nx
                self.target_y = self.y + ny
                self.target_px, self.target_py = self.maze.cell_to_pixel(
                    self.target_x, self.target_y
                )

        else:
            self.px += (dx / dist) * step
            self.py += (dy / dist) * step

    def draw(self, screen, player_png):
        self.spirit = pygame.image.load(player_png)
        self.spirit = pygame.transform.scale(
            self.spirit,
            (
                self.maze.cell_size - self.maze.cell_size // 4,
                self.maze.cell_size - self.maze.cell_size // 4,
            ),
        )
        if self.current_dir == 2:
            pass
        elif self.current_dir == 1:
            self.spirit = pygame.transform.rotate(self.spirit, 90)
        elif self.current_dir == 4:
            self.spirit = pygame.transform.rotate(self.spirit, 270)
        elif self.current_dir == 8:
            self.spirit = pygame.transform.flip(self.spirit, True, True)
        screen.blit(
            self.spirit,
            (
                self.px + self.maze.cell_size // 6,
                self.py + self.maze.cell_size // 6
            )
        )

    def draw_and_switch(self, screen, deltatime):
        self.var += deltatime
        if self.var >= 0.1:
            self.var = 0
            self.index = (self.index + 1) % len(self.player_images)
            self.draw(screen, self.player_images[self.index])
        else:
            self.draw(screen, self.player_images[self.index])
