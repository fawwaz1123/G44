from vector import Vector
class Interaction:
    def __init__(self, truck, keyboard, background, lives):
        self.truck = truck
        self.keyboard = keyboard
        self.background = background
        self.lives = lives
        

    def update(self):
        if self.keyboard.right:
            self.truck.move_right()
        if self.keyboard.left:
            self.truck.move_left()
        if self.keyboard.up:
            self.truck.jump()
        if not self.keyboard.right and not self.keyboard.left:
            self.truck.stop()
        self.truck.update()