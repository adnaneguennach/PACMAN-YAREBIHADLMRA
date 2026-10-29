from mazegenerator import MazeGenerator   
import pygame

class MazeRendering:
    def __init__(self, lvl_width, lvl_height, tile_size):
        self.maze_grid = MazeGenerator(size = (lvl_width, lvl_height), perfect = False).maze
        self.lvl_width = lvl_width
        self.lvl_height = lvl_height
    
    def draw_maze(self):
        maze_width = self.lvl_width * tile_size
        maze_height = self.lvl_height * tile_size

        running = True
        pygame.font.init()
        menu_font = pygame.font.Font("ByteBounce.ttf", 48)
        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill("purple")
            pygame.display.flip()
            clock.tick(60)
        return self.maze_grid


