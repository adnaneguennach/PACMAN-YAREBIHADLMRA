"""Maze logic (walls, neighbours, pellets), screen layout and drawing."""

import pygame

# Wall bit flags stored in every grid cell.
NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8

# Direction -> (dx, dy) in cell coordinates.
DIRECTIONS = {NORTH: (0, -1), EAST: (1, 0), SOUTH: (0, 1), WEST: (-1, 0)}

# Cell values that are completely walled in (they never hold a pellet).
SOLID_CELLS = (15, 42)

WALL_THICKNESS = 2
WALL_COLOR = "blue"


class Maze:
    def __init__(self, walls, cell_size, screen_size):
        self.walls = walls
        self.cell_size = cell_size
        self.height = len(walls)
        self.width = len(walls[0])

        self.corners = [
            (0, 0),
            (self.width - 1, 0),
            (0, self.height - 1),
            (self.width - 1, self.height - 1),
        ]
        self.center = (self.width // 2, self.height // 2)

        # Pellets are stored as sets of (x, y) cells: eating one = .discard().
        self.power_pellets = set(self.corners)
        self.pellets = {
            (x, y)
            for y, row in enumerate(walls)
            for x, cell in enumerate(row)
            if cell not in SOLID_CELLS and (x, y) not in self.power_pellets
        }

        self._center_on_screen(screen_size)
        self._wall_rects = self._build_wall_rects()

    # ---------- logic ----------

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def has_wall(self, x, y, direction):
        return not self.in_bounds(x, y) or bool(self.walls[y][x] & direction)

    def can_move(self, x, y, direction):
        return not self.has_wall(x, y, direction)

    def reachable_neighbors(self, x, y):
        """Neighbouring cells that can be entered without crossing a wall."""
        return [
            (x + dx, y + dy)
            for direction, (dx, dy) in DIRECTIONS.items()
            if self.can_move(x, y, direction)
            and self.in_bounds(x + dx, y + dy)
        ]

    def adjacent_cells(self, x, y):
        """In-bounds neighbouring cells, ignoring walls."""
        return [
            (x + dx, y + dy)
            for dx, dy in DIRECTIONS.values()
            if self.in_bounds(x + dx, y + dy)
        ]

    # ---------- screen layout ----------

    def cell_to_pixel(self, x, y):
        """Top-left pixel of a cell."""
        return (
            self.offset_x + x * self.cell_size,
            self.offset_y + y * self.cell_size,
        )

    def cell_center(self, x, y):
        """Center pixel of a cell."""
        px, py = self.cell_to_pixel(x, y)
        half = self.cell_size // 2
        return px + half, py + half

    def pixel_to_cell(self, pixel_x, pixel_y):
        return (
            (pixel_x - self.offset_x) // self.cell_size,
            (pixel_y - self.offset_y) // self.cell_size,
        )

    def _center_on_screen(self, screen_size):
        screen_w, screen_h = screen_size
        maze_w = self.width * self.cell_size
        maze_h = self.height * self.cell_size
        if maze_w > screen_w or maze_h > screen_h:
            raise ValueError("Maze is too large for the screen resolution.")
        self.offset_x = (screen_w - maze_w) // 2
        self.offset_y = (screen_h - maze_h) // 2

    # ---------- drawing ----------

    def _build_wall_rects(self):
        """Compute every wall rectangle once instead of on every frame."""
        size, thick = self.cell_size, WALL_THICKNESS
        rects = []
        for y, row in enumerate(self.walls):
            for x, cell in enumerate(row):
                px, py = self.cell_to_pixel(x, y)
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