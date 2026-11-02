class Player:
    def __init__(self, x, y, pixel_x, pixel_y, speed, maze_obj):
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
        step = self.speed
