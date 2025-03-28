from vector import Vector
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from wheel import Wheel
from variables import HEIGHT, TRUCK_IMG
import math

class Truck:
    def __init__(self):
        self.pos = Vector(200, HEIGHT - 150)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0.5)
        self.angle = 0
        self.on_ground = True
        self.started = False
        self.on_rock = False  # True if a rock collision occurs this frame
        
        # Create wheels
        self.front_wheel = Wheel(self, True)
        self.back_wheel = Wheel(self, False)

    def update(self):
        if self.started:
            self.vel.add(self.acc)
            self.pos.add(self.vel)
            
            if self.pos.y >= HEIGHT - 150:
                self.pos.y = HEIGHT - 150
                self.vel.y = 0
                self.on_ground = True
            else:
                self.on_ground = False

        # Update wheels
        self.front_wheel.update()
        self.back_wheel.update()

        # If a rock collision occurred, update the angle based on velocity.
        if self.on_rock:
            if not self.on_ground:
                if abs(self.vel.x) > 0.1:
                    self.angle = math.atan2(self.vel.y, self.vel.x)
            else:
                # On ground, you may gently damp the angle if desired.
                self.angle *= 0.95
        # Else, if not colliding with a rock, do not force the angle toward 0.
        # (The truck will maintain any rotation applied via move_right/move_left.)
        
        # Reset collision flag at end of update.
        self.on_rock = False

    def move_right(self):
        if not self.started:
            self.started = True
        if self.on_ground:
            self.vel.x = 3 
        else:
            self.vel.x = 3
            # When airborne, adjust the angle incrementally to tilt right.
            self.angle -= 0.01  

    def move_left(self):
        if not self.started:
            self.started = True
        if self.on_ground:
            self.vel.x = -3 
        else:
            self.vel.x = -3
            # When airborne, adjust the angle incrementally to tilt left.
            self.angle += 0.01  

    def jump(self):
        if self.on_ground:
            self.vel.y = -15
            self.on_ground = False
            # When jumping without a rock collision, do not force angle to 0.
            # (It will remain what it was from player input.)

    def stop(self):
        self.vel.x = 0

    def draw(self, canvas, offset):
        canvas.draw_image(TRUCK_IMG, 
                          (200, 72), 
                          (400, 144), 
                          (self.pos.x - offset, self.pos.y - 18),
                          (200, 72), 
                          self.angle)
        self.front_wheel.draw(canvas, offset)
        self.back_wheel.draw(canvas, offset)

    def rock_collision(self, rock):
        if rock.collided():
            # Compute R: vector from rock to truck.
            R = self.pos.copy().subtract(rock.pos)
            normal = R.get_normalized()
            # Compute reflected velocity using the reflect method.
            v_reflected = self.vel.copy().reflect(normal)
            # The average of the current velocity and its reflection is the tangential component:
            v_tan = (self.vel + v_reflected) * 0.5
            # Add a modest upward impulse to help lift the truck.
            upward_impulse = Vector(0, -2)
            v_tan.add(upward_impulse)
            # Blend the current velocity with the computed tangential velocity for a smooth transition.
            blend = 0.6  # Adjust between 0 (no change) and 1 (full change).
            self.vel = self.vel * (1 - blend) + v_tan * blend
            # Update the truck's angle based on the new velocity.
            self.angle = math.atan2(self.vel.y, self.vel.x)
            self.on_rock = True

                
