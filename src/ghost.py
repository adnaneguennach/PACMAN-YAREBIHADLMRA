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
        self.dead_speed = speed * 4

        self.target_x = x
        self.target_y = y
        self.target_px = self.px
        self.target_py = self.py

        self.seen = deque()
        self.range = []

        self.player_detectet_in_zone = False
        self.scared = False
        self.eaten = False
        self.start_to_return = False
        
        self.timer1 = 0
        self.timer2 = 0
        self.dead_timer = 0

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
        if Tools._touching_player(self, player):
            self.eaten = True
            return
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

                if best_neighbor is None:
                    return

                x, y = best_neighbor
                nx, ny = self.maze.get_dir(x, y, self.x, self.y)
                self.target_x = self.x + nx
                self.target_y = self.y + ny
                self.target_px, self.target_py = self.maze.cell_to_pixel(self.target_x, self.target_y)
            else:
                self.px += (dx / dist) * step
                self.py += (dy / dist) * step

    def to_start_and_freez(self, deltatime):
        step = self.dead_speed * deltatime * self.maze.cell_size
        dx = self.target_px - self.px
        dy = self.target_py - self.py
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist <= step:
            self.px = self.target_px
            self.py = self.target_py
            self.x = self.target_x
            self.y = self.target_y

            if (self.x, self.y) == (self.default_x, self.default_y):
                return

            next_move_to_start = Tools.next_step_bfs(
                (self.x, self.y), (self.default_x, self.default_y), self.maze)
            if next_move_to_start is None:
                return

            x, y = next_move_to_start
            nx, ny = self.maze.get_dir(x, y, self.x, self.y)
            self.target_x = self.x + nx
            self.target_y = self.y + ny
            self.target_px, self.target_py = self.maze.cell_to_pixel(
                self.target_x, self.target_y)
        else:
            self.px += (dx / dist) * step
            self.py += (dy / dist) * step

    def revive(self):
        self.x, self.y = self.default_x, self.default_y
        self.px, self.py = self.maze.cell_to_pixel(self.x, self.y)
        self.target_x, self.target_y = self.x, self.y
        self.target_px, self.target_py = self.px, self.py
        self.seen.clear()
        self.dead_timer = 0
        self.eaten = False
        self.player_detectet_in_zone = False

    def update(self, deltatime, player: Player):
        Tools.check_player_in_zone(self, player)

        if self.eaten:
            self.to_start_and_freez(deltatime)
            self.dead_timer += deltatime
            if self.dead_timer >= 6:
                self.revive()
        else:
            if Tools._touching_player(self, player):
                if player.power:
                    self.eaten = True
                    return
                print("loser")
                exit()

            if self.player_detectet_in_zone and not player.power:
                self.chassing(deltatime, player)
            elif self.player_detectet_in_zone and player.power:
                self.running(deltatime, player)
            else:
                self.random_move(deltatime, player)
        if player.power:
            self.timer1 += deltatime
            self.timer2 += deltatime
            if self.timer2 >= 4.5:
                self.timer2 = 0
                self.start_to_return = True
            if self.timer1 >= 6:
                self.timer1 = 0
                player.power = False
                self.start_to_return = False
        else:
            self.timer1 = 0
            self.timer2 = 0

    #___________________Draw_assi_adnane___________________
    # khassni nm7i player mn lparam
    def normal_mode(self, screen, ghost_png):
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

    def dead_mode(self, screen, ghost_png):
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

    def scare_mode(self, screen, ghost_png):
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

    def ghost_return(self, screen, ghost_png):
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
        

    def draw(self, screen, ghost_png, player: Player):
        if not player.power:
            self.normal_mode(screen, ghost_png)
        elif player.power and not self.eaten:
            if not self.start_to_return:
                self.scare_mode(screen, "assets/ghost_images/powerup.png")
            else:
                self.ghost_return(screen, "assets/ghost_images/ghost_return.png")
        elif self.eaten:
            self.dead_mode(screen, "assets/ghost_images/dead.png")