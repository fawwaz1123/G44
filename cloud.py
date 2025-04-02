import random

class Cloud:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed

    def update(self, screen_width, truck_speed):
        parallax_factor = 0.5  
        self.x += self.speed - (truck_speed * parallax_factor)
        if self.x - self.size > screen_width:
            self.x = -self.size
        if self.x + self.size < 0:
            self.x = screen_width + self.size

    def draw(self, canvas):
        canvas.draw_circle((self.x, self.y), self.size, 1, "White", "White")
        canvas.draw_circle((self.x + self.size * 0.8, self.y + self.size * 0.2), 
                           self.size * 0.8, 1, "White", "White")
        canvas.draw_circle((self.x - self.size * 0.8, self.y + self.size * 0.2), 
                           self.size * 0.8, 1, "White", "White")
