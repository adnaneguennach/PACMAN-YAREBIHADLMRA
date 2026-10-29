from mazegenerator import MazeGenerator   
import pygame
from .config import ConfigParser

class MazeRendering:
    def __init__(self):
        # self.maze_grid = MazeGenerator(size = (lvl_width, lvl_height), perfect = False).maze
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.tile_size = 20

    def drawing_loop(self, config_path):
        # pass
        parser_obj = ConfigParser(config_path)
        parsed_data = parser_obj.parsing_data()
        levels = parsed_data["levels"]
        actual_lvl = 0

        while actual_lvl < len(levels):
            maze_grid = MazeGenerator(size = (levels[actual_lvl]["width"], levels[actual_lvl]["height"]), perfect = False).maze
            maze_width = levels[actual_lvl]["width"] * self.tile_size
            maze_height = levels[actual_lvl]["height"] * self.tile_size
            offset_x = (self.screen_width - maze_width) // 2
            offset_y = (self.screen_height - maze_height) // 2

            for y in range(levels[actual_lvl]["height"]):
                for x in range(levels[actual_lvl]["width"]):
                    grid_cell = maze_grid[y][x]
                    px = offset_x
                    py = offset_y
                    
                    print(px, py)
        # return levels



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

