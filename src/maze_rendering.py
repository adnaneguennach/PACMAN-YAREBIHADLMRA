import pygame


class Maze:
    def __init__(self, screen, grid, tile=40):
        self.screen = screen
        self.grid = grid
        self.tile = tile
        self.x = (screen.get_width() - len(grid[0]) * tile) // 2
        self.y = (screen.get_height() - len(grid) * tile) // 2

    def draw(self):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                px, py = self.x + (x * self.tile), self.y + (y * self.tile)
                for bit, rect in (
                    (1, (px, py, self.tile, 2)),
                    (2, (px + self.tile - 2, py, 2, self.tile)),
                    (4, (px, py + self.tile - 2, self.tile, 2)),
                    (8, (px, py, 2, self.tile)),
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
