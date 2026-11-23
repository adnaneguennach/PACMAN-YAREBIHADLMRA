
"""Maze logic (walls, neighbours, pellets), screen layout and drawing."""

import pygame

NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8

DIRECTIONS = {NORTH: (0, -1), EAST: (1, 0), SOUTH: (0, 1), WEST: (-1, 0)}

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

        self.super_pacgums = [
            [
                1 if (i == 0 and j == 0) or (i == 0 and j == self.height - 1) or (i == self.width - 1 and j == 0) or (i == self.width - 1 and j == self.height - 1) else 0
                for i in range(self.width)
            ]
            for j in range(self.height)
        ]

        self.pacgums = [
            [
                0 if walls[j][i] == 15 or (i in (0, self.width - 1) and j in (0, self.height - 1)) else 1
                for i in range(self.width)
            ]
            for j in range(self.height)
        ]

        self._center_on_screen(screen_size)

    # ---------- logic ----------

    def get_cor(self, direction):
        return DIRECTIONS[direction]

    def get_dir(self, x, y, target_x, target_y):
        cor_x = x - target_x
        cor_y = y - target_y
        return cor_x, cor_y

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def has_wall(self, x, y, direction):
        return not self.in_bounds(x, y) or bool(self.walls[y][x] & direction)

    def can_move(self, x, y, direction):
        return not self.has_wall(x, y, direction)

    def reachable_neighbors(self, x, y):
        return [
            (x + dx, y + dy)
            for direction, (dx, dy) in DIRECTIONS.items()
            if self.can_move(x, y, direction)
            and self.in_bounds(x + dx, y + dy)
        ]

    def adjacent_cells(self, x, y):
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
        self.screen_w, self.screen_h = screen_size
        maze_w = self.width * self.cell_size
        maze_h = self.height * self.cell_size
        if maze_w > self.screen_w or maze_h > self.screen_h:
            raise ValueError("Maze is too large for the screen resolution.")
        self.offset_x = (self.screen_w - maze_w) // 2
        self.offset_y = (self.screen_h - maze_h) // 1.2

    def _render_maze(self, cell_value, x, y, screen):
        pix, piy = self.cell_to_pixel(x, y)

        if (
            pix + self.cell_size >= self.screen_w
            or piy + self.cell_size >= self.screen_h
        ):
            print(
                "Error: maze is too large for the current screen "
                "resolution."
            )
            exit()

        if cell_value == 15:
            pygame.draw.rect(
                screen,
                "blue",
                (pix, piy, self.cell_size, self.cell_size),
            )

        if cell_value & 1:
            pygame.draw.rect(screen, "blue", (pix, piy, self.cell_size, 4))
        if cell_value & 4:
            pygame.draw.rect(
                screen,
                "blue",
                (pix, piy + self.cell_size, self.cell_size, 4),
            )

        if cell_value & 2:
            pygame.draw.rect(
                screen,
                "blue",
                (pix + self.cell_size, piy, 4, self.cell_size),
            )

        if cell_value & 8:
            pygame.draw.rect(screen, "blue", (pix, piy, 4, self.cell_size))

        center_x = pix + (self.cell_size // 2)
        center_y = piy + (self.cell_size // 2)

        if self.pacgums[y][x] == 1:
            pygame.draw.circle(
                screen, (255, 255, 255), (center_x, center_y), 4
            )
        elif self.super_pacgums[y][x] == 1:
            pygame.draw.circle(
                screen, (255, 255, 255), (center_x, center_y), 10
            )

    def _render_hud(self, screen, score, lives, level):
        if not hasattr(self, "font"):
            pygame.font.init()
        self.font = pygame.font.SysFont(None, 36)

        start_pointx = self.offset_x
        start_pointy = self.offset_y - 40

        hud_string = (
            f"Score: {score}          Lives: {lives}          Level: {level}"
        )
        text_surface = self.font.render(hud_string, True, (255, 255, 255))

        screen.blit(text_surface, (start_pointx, start_pointy))

    def draw(self, screen):
        for row_index, row in enumerate(self.walls):
            for col_index, cell_value in enumerate(row):
                pac_px, pac_py = self.cell_to_pixel(
                    col_index, row_index
                )

                if self.pacgums[row_index][col_index] == 1:
                    pygame.draw.circle(
                        screen,
                        (255, 255, 255),
                        (
                            pac_px + self.cell_size // 2,
                            pac_py + self.cell_size // 2,
                        ),
                        self.cell_size // 10,
                    )

                if self.super_pacgums[row_index][col_index] == 1:
                    pygame.draw.circle(
                        screen,
                        (255, 255, 255),
                        (
                            pac_px + self.cell_size // 2,
                            pac_py + self.cell_size // 2,
                        ),
                        self.cell_size // 5,
                    )

                self._render_maze(
                    cell_value, col_index, row_index, screen
                )
