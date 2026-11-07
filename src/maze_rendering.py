import pygame

from src.maze_adapter import EAST, NORTH, SOUTH, WEST, MazeAdapter

WALL_THICKNESS = 2
WALL_COLOR = "blue"


class MazeRendering:
    def __init__(self, walls, cell_size, screen_size):
        self.maze_adapter = MazeAdapter(walls, cell_size, screen_size)
        self._wall_rects = self._build_wall_rects()

    def _build_wall_rects(self):
        """Compute every wall rectangle once instead of on every frame."""
        maze = self.maze_adapter
        size, thick = maze.cell_size, WALL_THICKNESS
        rects = []
        for y, row in enumerate(maze.walls):
            for x, cell in enumerate(row):
                px, py = maze.cell_to_pixel(x, y)
                edges = {
                    NORTH: (px, py, size, thick),
                    EAST: (px + size - thick, py, thick, size),
                    SOUTH: (px, py + size - thick, size, thick),
                    WEST: (px, py, thick, size),
                }
                rects += [rect for bit, rect in edges.items() if cell & bit]
        return rects

    def draw(self, screen):
        for rect in self._wall_rects:
            pygame.draw.rect(screen, WALL_COLOR, rect)
