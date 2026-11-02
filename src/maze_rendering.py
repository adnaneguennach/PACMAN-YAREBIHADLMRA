import pygame


class Maze:
    def __init__(self, screen, grid, tile=40):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.grid = grid
        self.cell_size = tile
        self.width = (self.screen_width - len(grid[0]) * tile) // 2
        self.height = (self.screen_height - len(grid) * tile) // 2
        self.offset_x = (self.screen_width - self.width) // 2
        self.offset_y = (self.screen_height - self.height) // 2

    def draw(self):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                px, py = self.width + (x * self.cell_size), self.height + (
                    y * self.cell_size
                )
                for bit, rect in (
                    (1, (px, py, self.cell_size, 2)),
                    (2, (px + self.cell_size - 2, py, 2, self.cell_size)),
                    (4, (px, py + self.cell_size - 2, self.cell_size, 2)),
                    (8, (px, py, 2, self.cell_size)),
                ):
                    if cell & bit:
                        pygame.draw.rect(self.screen, "blue", rect)

    # adnane implemente hadi 3awd
    def cell_to_pixel(self, x, y):
        pix_x = self.offset_x + (x * self.cell_size)
        pix_y = self.offset_y + (y * self.cell_size)
        return pix_x, pix_y

    def pixel_to_cell(self, pix_x, pix_y):
        x = (pix_x - self.offset_x) // self.cell_size
        y = (pix_y - self.offset_y) // self.cell_size
        return x, y

    def can_move():
        pass