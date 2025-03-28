from vector import Vector
import math
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from variables import TYRE_IMG
class Wheel:
    def __init__(self, truck, is_front):
        # Attach the wheel to the truck pos
        self.truck = truck
        self.is_front = is_front
        self.radius = 30
        self.angle = 0
        self.wheel_speed = 0.05
        
        if self.is_front:
            self.offset = 55
        else:
            self.offset = -50    
        
    def update(self):
        truck_pos = self.truck.pos
        truck_angle = self.truck.angle

        offset_x = self.offset 
        offset_y = 25

        # calculate x and y roation of wheels using 2d matrix formulae
        rotated_x = offset_x * math.cos(truck_angle) - offset_y * math.sin(truck_angle)
        rotated_y = offset_x * math.sin(truck_angle) + offset_y * math.cos(truck_angle)

        self.pos = truck_pos.copy()  # Start at truck pos
        self.pos.x += rotated_x  # add rotated x offset
        self.pos.y += rotated_y  # add rotated y offset

        if self.truck.vel.x != 0: #if truck moving
            self.angle += self.truck.vel.x * self.wheel_speed  # roll wheels
    
    def draw(self, canvas, offset):
        canvas.draw_image(TYRE_IMG, 
                          (100, 100), 
                          (200, 199), 
                          (self.pos.x - offset, self.pos.y), 
                          (self.radius*2, self.radius*2), 
                          self.angle)
