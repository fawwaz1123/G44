from vector import Vector 
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui  
from variables import WIDTH, HEIGHT
import random

class Rock:
    def __init__(self, truck, spawn_x):
        self.t = truck  
        self.x = spawn_x
        self.y = HEIGHT - 100
        self.pos = Vector(self.x, self.y)
        self.collide = False

    def draw(self, canvas, offset):
        canvas.draw_circle((self.pos.x - offset, self.pos.y), 50, 1, 'Grey', 'Grey')

    def collided(self):
        # Get the positions of both wheels.
        front_wheel = self.t.front_wheel.pos
        back_wheel = self.t.back_wheel.pos
        # Compute the average (midpoint) of the two wheel positions.
        avg_wheel = (front_wheel + back_wheel) * 0.5
        # Determine the distance between the rock's center and the average wheel position.
        d = avg_wheel.copy().subtract(self.pos).length()
        # Use a threshold (here, 50 pixels) to decide if a collision occurred.
        if d <= 50:
            self.collide = True
        else:
            self.collide = False
        return self.collide
