import random
from rock import Rock
class Interaction:
    def __init__(self, truck, keyboard, background, lives, ramps, length):
        self.truck = truck
        self.keyboard = keyboard
        self.background = background
        self.lives = lives
        self.ramps = ramps
        self.rocks = []  # Add rock handling to Interaction
        self.length = length
        self.next_spawn = length / 4  # Next spawn threshold (in x-coordinate)
        self.ALL_LIVES_LOST = False

        
    def update(self, canvas):
        # Update truck movement
        if self.keyboard.right:
            self.truck.move_right()
        if self.keyboard.left:
            self.truck.move_left()
        if self.keyboard.up:
            self.truck.jump()
        if not self.keyboard.right and not self.keyboard.left:
            self.truck.stop()
        self.truck.update()


    def spawn_rocks(self, spawn_offset, zone_width, height):
        # Spawn rocks if truck passes a spawn threshold
        if (self.truck.pos.x + spawn_offset >= self.next_spawn) and (self.next_spawn < self.length):
            zone_start = self.next_spawn
            num_rocks = random.randint(1, 2)  # Spawn 1 to 2 rocks
            for i in range(num_rocks):
                spawn_x = random.randint(int(zone_start), int(zone_start + zone_width))
                self.rocks.append(Rock(self.truck, spawn_x, height))
            self.next_spawn += self.length / 4  # Move to next zone

            
    def handle_rock_collisions(self):
        # Check collisions between truck and rocks
        for rock in self.rocks:
            if self.truck.rock_collision(rock):
                if self.lives.three_lives:
                    self.lives.three_lives = False
                elif self.lives.two_lives:
                    self.lives.two_lives = False
                elif self.lives.one_life:
                    self.lives.one_life = False
                    self.ALL_LIVES_LOST = True
