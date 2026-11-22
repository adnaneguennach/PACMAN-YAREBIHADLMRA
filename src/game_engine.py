import pygame
from src.config import ConfigParser
from src.maze import EAST, NORTH, SOUTH, WEST, Maze
from src.states import PlayingState



class GameEngine:
    def __init__(self, config_path):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        config_obj = ConfigParser(config_path)
        self.config = config_obj.parsing_data()
        self.level_rank = 0
        self.check_win = False
        self.config_adapter()


    def config_adapter(self):
        self.highscore_filename = self.config["highscore_filename"]
        self.seed = self.config["seed"]
        self.points_per_pacgum = self.config["points_per_pacgum"]
        self.points_per_super_pacgum = self.config["points_per_super_pacgum"]
        self.points_per_ghost = self.config["points_per_ghost"]
        self.level_max_time = self.config["level_max_time"]
        self.lives = self.config["lives"]
        self.palyer_speed = self.config["player_speed"]
        self.ghost_speed = self.config["ghost_speed"]


    def run(self):
        playing = PlayingState(self)
        playing.play(self)
        

    

    
