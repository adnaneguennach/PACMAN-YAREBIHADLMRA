from src.maze import Maze
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
        self.default_x = x
        self.default_y = y
        self.px, self.py = self.maze.cell_to_pixel(self.x, self.y)
        self.speed = speed

        self.target_x = x
        self.target_y = y
        self.target_px = self.px
        self.target_py = self.py

        self.seen = deque()
        self.player_detectet_in_zone = False
        self.scared = False
        self.range = []
        self.timer = 0

    def random_move(self, deltatime, player: Player):
        if Tools._touching_player(self, player):
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
        if Tools._touching_player(self, player):
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
                # makil9ach path f l7ala dyal lghost w lplayer f nefs cell
                return
            x, y = next_step
            nx, ny = self.maze.get_dir(x, y, self.x, self.y)
            self.target_x = self.x + nx
            self.target_y = self.y + ny
            self.target_px, self.target_py = self.maze.cell_to_pixel(
                self.target_x, self.target_y
            )
        else:
            self.px += (dx / dist) * step
            self.py += (dy / dist) * step



    def running(self, deltatime, player: Player):
        if (self.x, self.y) in self.range:
            step = self.speed * deltatime * self.maze.cell_size
            dx = self.target_px - self.px
            dy = self.target_py - self.py
            dist = (dx ** 2 + dy ** 2) ** 0.5

            if dist <= step:
                self.px = self.target_px
                self.py = self.target_py
                self.x = self.target_x
                self.y = self.target_y

                neighbors = self.maze.reachable_neighbors(self.x, self.y)
                best_neighbor = None
                best_dist = -1
                for neighbor in neighbors:
                    path = Tools.shortest_path(neighbor, (player.x, player.y), self.maze)
                    if path and len(path) > best_dist:
                        best_dist = len(path)
                        best_neighbor = neighbor

                x, y = best_neighbor
                nx, ny = self.maze.get_dir(x, y, self.x, self.y)
                self.target_x = self.x + nx
                self.target_y = self.y + ny
                self.target_px, self.target_py = self.maze.cell_to_pixel(self.target_x, self.target_y)

            else:
                self.px += (dx / dist) * step
                self.py += (dy / dist) * step

    def manage_ghost_life(self, deltatime, player):
        Tools.check_player_in_zone(self, player)
        # if ghost_dead:
        #     all_moves = stop_moving
        # if self.player_eat_super_pacgum:
        #     self.scared = True
        #     self.player_eat_super_pacgum = False

    def update(self, deltatime, player: Player):
        self.manage_ghost_life(deltatime, player)
        # if self.player_detectet_in_zone and not self.scared:
        #     self.chassing(deltatime, player)
        if self.player_detectet_in_zone:
            self.running(deltatime, player)
        if not self.player_detectet_in_zone:
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
