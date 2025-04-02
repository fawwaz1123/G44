class Lives:
    def __init__(self):
        self.one_life = True
        self.two_lives = True
        self.three_lives = True

    def draw(self, canvas, heart_img):
        if self.one_life:
            canvas.draw_image(heart_img, (60, 60), (120, 120), (800, 25), (60, 60))
        if self.two_lives:
            canvas.draw_image(heart_img, (60, 60), (120, 120), (860, 25), (60, 60))
        if self.three_lives:
            canvas.draw_image(heart_img, (60, 60), (120, 120), (920, 25), (60, 60))
        if not self.one_life:
            canvas.draw_image(heart_img, (60, 180), (120, 120), (800, 25), (60, 60))
        if not self.two_lives:
            canvas.draw_image(heart_img, (60, 180), (120, 120), (860, 25), (60, 60))
        if not self.three_lives:
            canvas.draw_image(heart_img, (60, 180), (120, 120), (920, 25), (60, 60))

    def reset(self):
        self.one_life = True
        self.two_lives = True
        self.three_lives = True
