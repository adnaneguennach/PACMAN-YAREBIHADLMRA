from mazegenerator import MazeGenerator   
import pygame
from .config import ConfigParser

class MazeRendering:
    def __init__(self, lvl_width, lvl_height, tile_size):
        self.maze_grid = MazeGenerator(size = (lvl_width, lvl_height), perfect = False).maze
        self.lvl_width = lvl_width
        self.lvl_height = lvl_height
    

    def drawing_loop(self, config_path):
        # pass
        parser_obj = ConfigParser(config_path)
        return parser_obj.parsing_data()


    def draw_maze(self):
        maze_width = self.lvl_width * tile_size
        maze_height = self.lvl_height * tile_size

        running = True
        pygame.font.init()
        menu_font = pygame.font.Font("ByteBounce.ttf", 48)
        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        offset_x = (screen_width - maze_width) // 2 # (1920 - 800) = 1120 / 2 = 560
        offset_y = (screen_height - maze_height) // 2 

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # for y in range(self.)
            screen.fill("purple")
            pygame.display.flip()
            clock.tick(60)
        return self.maze_grid

