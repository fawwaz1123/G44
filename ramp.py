class Ramp:
    def __init__(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.start_x = start_pos[0]
        self.start_y = start_pos[1]
        self.end_pos = end_pos
        self.end_x = end_pos[0]
        self.end_y = end_pos[1]
        self.third_point = (self.end_pos[0], self.start_pos[1])
        self.third_x = self.third_point[0]
        self.third_y = self.third_point[1]

    def draw(self, canvas, offset):
        canvas.draw_polygon([
            (self.start_x - offset, self.start_y),
            (self.end_x - offset, self.end_y),
            (self.third_x - offset, self.third_y)
        ], 100, 'Maroon')

