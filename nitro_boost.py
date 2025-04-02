import time
try:
    from user305_o32FtUyCKk_0 import Vector
except:
    from vector import Vector

class NitroBoost:
    def __init__(self, spawn_x, y):
        self.pos = Vector(spawn_x, y)
        self.radius = 20
        self.active = True

    def draw(self, canvas, offset):
        if self.active:
            canvas.draw_circle((self.pos.x - offset, self.pos.y), 
                               self.radius, 2, 'Yellow', 'Yellow')

    def check_collision(self, truck):
        d = truck.pos.copy().subtract(self.pos).length()
        if d < 50 and self.active:
            self.active = False
            return True
        return False
