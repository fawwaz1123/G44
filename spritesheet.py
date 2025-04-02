class Spritesheet:
    def __init__(self, img):
        self.img = img
        self.img_width = img.get_width()
        self.img_height = img.get_height()
        self.rows = 5
        self.columns = 10
        self.frame_width = self.img_width / self.columns
        self.frame_height = self.img_height / self.rows
        self.frame_centre_x = self.img_width / 2
        self.frame_centre_y = self.img_height / 2
        self.frame_index = (0, 0)
        self.fin = False

    def draw(self, canvas, truck, offset):
        frame_x = self.frame_index[1] * self.frame_width
        frame_y = self.frame_index[0] * self.frame_height

        if not self.fin:
            truck.pos.y = 450
            canvas.draw_image(
                self.img,
                (frame_x + self.frame_width / 2, frame_y + self.frame_height / 2),
                (self.frame_width, self.frame_height),
                (truck.pos.x - offset, truck.pos.y - 70),
                (self.frame_width * 2.5, self.frame_height * 2.5)
            )

    def next_frame(self):
        if self.fin:
            return
        row, col = self.frame_index
        col += 1
        if col >= self.columns:
            col = 0
            row += 1
            if row >= self.rows:
                self.fin = True
                row = 0
        self.frame_index = (row, col)

    def reset(self):
        self.frame_index = (0, 0)
        self.fin = False
