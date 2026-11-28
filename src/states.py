import pygame
import random
from mazegenerator import MazeGenerator

from src.maze import EAST, NORTH, SOUTH, WEST, Maze
from src.player import Player
from src.tools import Tools
from src.ghost import Ghost

FPS = 60
CELL_SIZE = 40

KEY_TO_DIRECTION = {
    pygame.K_UP: NORTH,
    pygame.K_RIGHT: EAST,
    pygame.K_DOWN: SOUTH,
    pygame.K_LEFT: WEST,
    pygame.K_w: NORTH,
    pygame.K_d: EAST,
    pygame.K_s: SOUTH,
    pygame.K_a: WEST,
}
CHEAT_MODE = {
    pygame.K_m: "invesible"
}
GHOST_COLORS = ("red", "pink", "blue", "orange")



# adnane u need to add your states here

class PlayingState:
    def __init__(self, game):
        self.init_playing(game)

    def init_playing(self, game):
        level = game.levels[game.level_rank]
        walls = MazeGenerator(
            size=(level["width"], level["height"]), perfect=False, seed=game.seed
        ).maze
        self.maze = Maze(walls, CELL_SIZE, game.screen.get_size())
        self.maze_adapter = self.maze
        player_x, player_y = self.maze.center
        self.player = Player(player_x, player_y, 4, self.maze)

        corners = self.maze.corners
        self.ghosts = [Ghost(x, y, 3, self.maze) for x, y in corners]

    def revive_player(self):
        player_x, player_y = self.maze.center
        self.player = Player(player_x, player_y, 4, self.maze)

        corners = self.maze.corners
        self.ghosts = [Ghost(x, y, 3, self.maze) for x, y in corners]

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

    def _handle_playing_events(self, game):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                if event.key in KEY_TO_DIRECTION:
                    self.player.next_dir = KEY_TO_DIRECTION[event.key]





                # hado cheat mode zid lihom annimation f display
                if event.key == pygame.K_m:
                    self.player.invesible = True
                if event.key == pygame.K_k:
                    self.player.speed += 1
                if event.key == pygame.K_l:
                    if self.player.speed > 1:
                        self.player.speed -= 1
                if event.key == pygame.K_o:
                    if game.level_rank < len(game.config["levels"]) - 1 :
                        game.level_rank += 1
                        game.lives = game.mount_lives
                        self.init_playing(game)
                    
        return True

    def update(self, deltatime, ghost: Ghost, player: Player, game):
        Tools.check_player_in_zone(ghost, player)

        if ghost.eaten:
            ghost.to_start_and_freez(deltatime)
            ghost.dead_timer += deltatime
            if ghost.dead_timer >= 6:
                ghost.revive()
        else:
            if Tools._touching_player(ghost, player):
                if player.invesible:
                    pass
                elif player.power:
                    game.score += game.points_per_ghost
                    ghost.eaten = True
                    return
                elif game.lives - 1 > 0:
                    game.lives -= 1
                    self.revive_player()
                else:
                    print(game.lives)
                    print("loser")
                    exit()

            if ghost.player_detectet_in_zone and not player.power:
                ghost.chassing(deltatime, player)
            elif ghost.player_detectet_in_zone and player.power:
                ghost.running(deltatime, player, game)
            else:
                ghost.random_move(deltatime, player)
        if player.power:
            ghost.timer1 += deltatime
            ghost.timer2 += deltatime
            if ghost.timer2 >= 4.5:
                ghost.timer2 = 0.0
                ghost.start_to_return = True
            if ghost.timer1 >= 6:
                ghost.timer1 = 0.0
                player.power = False
        else:
            ghost.start_to_return = False
            ghost.timer1 = 0.0
            ghost.timer2 = 0.0

    def play(self, game):
        clock = pygame.time.Clock()
        while self._handle_playing_events(game):
            deltatime = clock.tick(FPS) / 1000

            self.player.update(deltatime, game, self.ghosts)
            for ghost in self.ghosts:
                self.update(deltatime, ghost, self.player, game)

            if self.check_win:
                if game.level_rank < len(game.config["levels"]) - 1 :
                    game.level_rank += 1
                    game.lives = game.mount_lives
                    self.init_playing(game)
                else:

                    # hna fin kan7ado lgame t9ad tzid chi 7aja
                    exit()

            self._draw(deltatime, game)

        pygame.quit()

    def _draw(self, deltatime, game):
        game.screen.fill("black")

        self.maze._render_hud(
            game.screen, game.score, game.lives, game.level_rank)
        self.maze.draw(game.screen)
        self.player.draw_and_switch(game.screen, deltatime)
        for ghost, color in zip(self.ghosts, GHOST_COLORS):
            ghost.draw(
                game.screen, f"assets/ghost_images/{color}.png", self.player)

        pygame.display.flip()
