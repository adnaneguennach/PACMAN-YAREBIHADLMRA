from mazegenerator import MazeGenerator   
import pygame
from .config import ConfigParser

class MazeRendering:
    def __init__(self):
        # self.maze_grid = MazeGenerator(size = (lvl_width, lvl_height), perfect = False).maze
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.tile_size = 40
        self.offset_x = 0
        self.offset_y = 0
        self.maze_grid = list()

    def drawing_loop(self, levels, actual_lvl):

        for y in range(levels[actual_lvl]["height"]):
            for x in range(levels[actual_lvl]["width"]):
                
                grid_cell = self.maze_grid[y][x]
                px = self.offset_x + (x*self.tile_size)
                py = self.offset_y + (y*self.tile_size)

                if grid_cell & 1: # NORTH
                    pygame.draw.rect(self.screen, "blue", (px, py, self.tile_size, 2)) # reminder : (start_x , start_y, chehal fiha mn px, width dyalha)
                
                if grid_cell & 2: #EAST
                    pygame.draw.rect(self.screen, "blue", (px + self.tile_size - 2, py, 2, self.tile_size))
                
                if grid_cell & 4: #SOUTH
                    pygame.draw.rect(self.screen, "blue", (px, py + self.tile_size - 2, self.tile_size, 2))
                
                if grid_cell & 8: #WEST
                    pygame.draw.rect(self.screen, "blue", (px, py, 2, self.tile_size))





    def draw_maze(self, config_path):
        
        #PARSER_VARS 
        parser_obj = ConfigParser(config_path)
        parsed_data = parser_obj.parsing_data()

    
        #PYGAME_VARS
        running = True
        pygame.font.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        #menu_font = pygame.font.Font("ByteBounce.ttf", 48)

        #LEVELS INIT VARS
        levels = parsed_data["levels"]
        actual_lvl = 0


        #MAZE INITIALISATION VARS
        self.maze_grid = MazeGenerator(size = (levels[actual_lvl]["width"], levels[actual_lvl]["height"]), perfect = False).maze
        maze_width = levels[actual_lvl]["width"] * self.tile_size
        maze_height = levels[actual_lvl]["height"] * self.tile_size
        self.offset_x = (self.screen_width - maze_width) // 2
        self.offset_y = (self.screen_height - maze_height) // 2

        

        #GAME LOOP
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.drawing_loop(levels, actual_lvl)

        
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()

