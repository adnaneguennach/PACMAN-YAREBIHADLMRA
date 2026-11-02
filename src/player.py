from src.maze_rendering import Maze


class Player:
    def __init__(self, x, y, pixel_x, pixel_y, speed, maze_obj: Maze):
        self.cell_x = x
        self.cell_y = y
        self.pixel_x = pixel_x
        self.pixel_y = pixel_y
        self.speed = speed
        self.maze_obj = maze_obj

        self.current_dir = None
        self.next_dir = None

        self.target_cell_x = x
        self.target_cell_y = y
        self.target_px = pixel_x
        self.target_py = pixel_y

        self.start_angle = 20
        self.end_angle = 340

    def update(self, deltatime):
        step = self.speed * deltatime * self.maze_obj.tile
        dx = self.target_px - self.pixel_x
        dy = self.target_py - self.pixel_y
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist <= step:
            self.pixel_x = self.target_px
            self.pixel_y = self.target_py
            self.cell_x = self.target_cell_x
            self.cell_y = self.target_cell_y
            if self.next_dir and self.maze_obj.can_move(
                self.cell_x, self.cell_y, self.next_dir
            ):
                self.current_dir = self.next_dir
                self.next_dir = None

            if self.current_dir and self.maze_obj.can_move(
                self.cell_x, self.cell_y, self.current_dir
            ):
                dir_x, dir_y = self.get_cor(self.current_dir)
                self.target_cell_x = self.cell_x + dir_x
                self.target_cell_y = self.cell_y + dir_y
                self.target_px, self.target_py = (
                    self.maze_obj.cell_to_pixel(
                        self.target_cell_x, self.target_cell_y
                    )
                )

        else:
            self.pixel_x += (dx / dist) * step
            self.pixel_y += (dy / dist) * step
