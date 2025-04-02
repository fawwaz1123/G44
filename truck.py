import math
import time
from wheel import Wheel
try: 
    from user305_o32FtUyCKk_0 import Vector
except:
    from vector import Vector
class Truck:
    def __init__(self, height):
        self.height = height
        self.pos = Vector(200, self.height - 150)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0.5)
        self.angle = 0
        self.on_ground = True
        self.started = False
        self.on_rock = False
        self.on_ramp = False
        self.past_ramp1 = False
        self.past_ramp2 = False
        self.pos_y_copy = 0
        self.front_wheel = Wheel(self, True)
        self.back_wheel = Wheel(self, False)
        self.nitro_active = False
        self.nitro_end_time = 0

    def reset(self):
        self.vel = Vector(0, 0)
        self.angle = 0
        self.started = False
        self.pos = Vector(200, self.height - 150)
        self.past_ramp1 = False
        self.past_ramp2 = False
        self.nitro_active = False
        self.nitro_end_time = 0

    def activate_nitro(self, duration):
        self.nitro_active = True
        self.nitro_end_time = time.time() + duration

    def update(self):
        if self.started:
            self.vel.add(self.acc)
            self.pos.add(self.vel)
            if self.pos.y >= self.height - 150:
                self.pos.y = self.height - 150
                self.vel.y = 0
                self.on_ground = True
            else:
                self.on_ground = False

        if self.nitro_active and time.time() < self.nitro_end_time:
            if abs(self.vel.x) < 10:
                if self.vel.x >= 0:
                    self.vel.x += 5
                else:
                    self.vel.x -= 5
        else:
            self.nitro_active = False

        self.front_wheel.update()
        self.back_wheel.update()
    
        if self.on_rock:
            if not self.on_ground and abs(self.vel.x) > 0.1:
                self.angle = math.atan2(self.vel.y, self.vel.x)
            else:
                self.angle *= 0.95
        self.on_rock = False

    def move_right(self):
        if not self.started:
            self.started = True
        if self.on_ground:
            self.vel.x = 3
        else:
            self.vel.x = 4 
            self.angle -= 0.01  

    def move_left(self):
        if not self.started:
            self.started = True
        if self.on_ground:
            self.vel.x = -3 
        else:
            self.vel.x = -3
            self.angle += 0.02  

    def jump(self):
        if self.on_ground:
            self.vel.y = -15
            self.on_ground = False

    def stop(self):
        self.vel.x = 0

    def draw(self, canvas, offset, truck_img, tyre_img, flame_img):
        if self.nitro_active:
            flame_pos = (self.pos.x - offset - 120, self.pos.y - 10)
            fw = flame_img.get_width()
            fh = flame_img.get_height()
            scale = 0.3
            canvas.draw_image(
                flame_img,
                (fw / 2, fh / 2),
                (fw, fh),
                flame_pos,
                (fw * scale, fh * scale)
            )
        canvas.draw_image(
            truck_img, 
            (200, 72), 
            (400, 144), 
            (self.pos.x - offset, self.pos.y - 18),
            (200, 72), 
            self.angle
        )
        self.front_wheel.draw(canvas, offset, tyre_img)
        self.back_wheel.draw(canvas, offset, tyre_img)

    def rock_collision(self, rock):
        if rock.collided():
            rock.already_hit = True
            rock.hit_frame = time.time()
            R = self.pos.copy().subtract(rock.pos)
            normal = R.get_normalized()
            v_reflected = self.vel.copy().reflect(normal)
            v_tan = (self.vel + v_reflected) * 0.5
            v_tan.add(Vector(0, -2))
            blend = 0.6
            self.vel = self.vel * (1 - blend) + v_tan * blend
            self.angle = math.atan2(self.vel.y, self.vel.x)
            self.on_rock = True
            return True
        return False 

    def ramp_collision(self, keyboard):
        if (self.pos.x >= 320 and self.pos.x <= 850) or (self.pos.x >= 3100 and self.pos.x <= 3500):
            self.angle = -0.35
            if keyboard.right:
                self.vel.y = -1.8
                self.pos_y_copy = self.pos.y
            if keyboard.left: 
                self.vel.y = 0.5
                self.pos_y_copy = self.pos.y
            if not keyboard.left and not keyboard.right:
                self.pos.y = self.pos_y_copy
                self.vel.y = 0
        
        if self.pos.x >= 860:
            self.past_ramp1 = True
        if self.past_ramp1 and self.pos.x <= 860:
            self.pos.x = 860
            if keyboard.left:  
                self.stop()
        
        if self.pos.x >= 3600:
            self.past_ramp2 = True
        if self.past_ramp2 and self.pos.x <= 3600:
            self.pos.x = 3600
            if keyboard.left:  
                self.stop()
