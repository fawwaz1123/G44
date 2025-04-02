import math

class Wheel:
    def __init__(self, truck, is_front):
        self.truck = truck
        self.pos = self.truck.pos.copy()
        self.is_front = is_front
        self.radius = 30
        self.angle = 0
        self.wheel_speed = 0.05
        self.offset = 55 if is_front else -50

    def update(self):
        truck_pos = self.truck.pos
        truck_angle = self.truck.angle
        offset_x = self.offset 
        offset_y = 25
        rotated_x = offset_x * math.cos(truck_angle) - offset_y * math.sin(truck_angle)
        rotated_y = offset_x * math.sin(truck_angle) + offset_y * math.cos(truck_angle)
        self.pos = truck_pos.copy()
        self.pos.x += rotated_x
        self.pos.y += rotated_y
        if self.truck.vel.x != 0:
            self.angle += self.truck.vel.x * self.wheel_speed

    def draw(self, canvas, offset, tyre_img):
        canvas.draw_image(
            tyre_img, 
            (100, 100), 
            (200, 199), 
            (self.pos.x - offset, self.pos.y), 
            (self.radius * 2, self.radius * 2), 
            self.angle
        )
