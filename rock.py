try:
    from user305_o32FtUyCKk_0 import Vector
except:
    from vector import Vector
class Rock:
    def __init__(self, truck, spawn_x, height):
        self.t = truck
        self.x = spawn_x
        self.y = height - 100
        self.pos = Vector(self.x, self.y)
        self.collide = False
        self.already_hit = False
        self.hit_frame = 0

    def draw(self, canvas, offset, rock_img):
        canvas.draw_circle((self.pos.x - offset, self.pos.y), 20, 1, 'Grey', 'Grey')
        canvas.draw_image(
            rock_img, 
            (125, 91.5), 
            (250, 183), 
            (self.pos.x - offset, self.pos.y - 25), 
            (125, 91.5)
        )
    
    def collided(self):
        front_wheel = self.t.front_wheel.pos
        back_wheel = self.t.back_wheel.pos
        avg_wheel = (front_wheel + back_wheel) * 0.5
        d = avg_wheel.copy().subtract(self.pos).length()
        self.collide = (d <= 50 and not self.already_hit)
        return self.collide
