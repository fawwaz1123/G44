try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from variables import HEART_IMG
class Lives:
    def __init__(self):
        self.one_life = True
        self.two_lives = True
        self.three_lives = True

    def draw(self, canvas):
        if self.one_life:
            canvas.draw_image(HEART_IMG, (60, 60), (120, 120), (800, 25), (60, 60))
        if self.two_lives:
            canvas.draw_image(HEART_IMG, (60, 60), (120, 120), (860, 25), (60, 60))
        if self.three_lives:
            canvas.draw_image(HEART_IMG, (60, 60), (120, 120), (920, 25), (60, 60))

    # The empty heart drawing from loose_life() has been merged into draw()
  # (i.e. both full and missing lives are drawn within draw())