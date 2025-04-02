try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


import time
import random

from background import Background
from cloud import Cloud
from ramp import Ramp
from nitro_boost import NitroBoost
from truck import Truck
from rock import Rock
from game_keyboard import Keyboard
from lives import Lives
from clock import Clock
from spritesheet import Spritesheet

class Game:
    def __init__(self):
        self.WIDTH = 1000
        self.HEIGHT = 600
        self.GAME_LENGTH = 5000
        self.BUTTON_WIDTH = 150

        self.GAME_STARTED = False
        self.GAME_OVER = False
        self.DISPLAY_INSTRUCTIONS = False
        self.RESTART = False

        self.start_time = 0
        self.elapsed_time = 0
        self.points = 0
        self.final_points = 0

        self.TRUCK_IMG_URL = "https://opengameart.org/sites/default/files/Body.png"
        self.TYRE_IMG_URL = "https://opengameart.org/sites/default/files/Tire.png"
        self.HEART_IMG_URL = "https://opengameart.org/sites/default/files/heart_15.png"
        self.EXPLOSION_IMG_URL = "https://opengameart.org/sites/default/files/explosion1_6.png"
        self.ROCK_IMG_URL = "https://opengameart.org/sites/default/files/styles/medium/public/rock_snowy_1a_al1.png"
        self.FLAME_IMG_URL = "https://dbdzm869oupei.cloudfront.net/img/sticker/preview/37333.png"
        self.TRUCK_IMG = simplegui.load_image(self.TRUCK_IMG_URL)
        self.TYRE_IMG = simplegui.load_image(self.TYRE_IMG_URL)
        self.HEART_IMG = simplegui.load_image(self.HEART_IMG_URL)
        self.EXPLOSION_IMG = simplegui.load_image(self.EXPLOSION_IMG_URL)
        self.ROCK_IMG = simplegui.load_image(self.ROCK_IMG_URL)
        self.FLAME_IMG = simplegui.load_image(self.FLAME_IMG_URL)

        self.SPAWN_OFFSET = 300  
        self.ZONE_WIDTH = 200    

        self.interact = self.create_interaction()
        self.spritesheet = Spritesheet(self.EXPLOSION_IMG)
        self.clock = Clock()

        # Create animated clouds for the background
        self.clouds = []
        for i in range(5):
            x = random.randrange(0, self.WIDTH)
            y = random.randrange(30, 150)
            size = random.randrange(20, 40)
            speed = random.uniform(0.3, 1.0)
            self.clouds.append(Cloud(x, y, size, speed))

    def create_interaction(self):
        # Create a simple Interaction object as a container for our game components
        interact = type('Interaction', (), {})()
        

        interact.truck = Truck(self.HEIGHT)
        interact.kbd = Keyboard()
        interact.background = Background()
        interact.lives = Lives()
        interact.clock = Clock()
        interact.ramps = [Ramp((650, 450), (725, 425)), Ramp((3400, 450), (3475, 425))]
        interact.nitro_boosts = [NitroBoost(1900, interact.truck.height - 150)]
        interact.rocks = []
        interact.length = self.GAME_LENGTH
        interact.next_spawn = self.GAME_LENGTH / 4
        interact.ALL_LIVES_LOST = False

        def update(canvas):
            if interact.kbd.right:
                interact.truck.move_right()
            if interact.kbd.left:
                interact.truck.move_left()
            if interact.kbd.up:
                interact.truck.jump()
            if not interact.kbd.right and not interact.kbd.left:
                interact.truck.stop()
            interact.truck.update()

            for nitro in interact.nitro_boosts:
                if nitro.check_collision(interact.truck):
                    interact.truck.activate_nitro(3)
        interact.update = update

        def spawn_rocks(spawn_offset, zone_width, height):
            if (interact.truck.pos.x + spawn_offset >= interact.next_spawn) and (interact.next_spawn < interact.length):
                zone_start = interact.next_spawn
                for _ in range(random.randint(1, 2)):
                    spawn_x = random.randint(int(zone_start), int(zone_start + zone_width))
                    interact.rocks.append(Rock(interact.truck, spawn_x, height))
                interact.next_spawn += interact.length / 4
        interact.spawn_rocks = spawn_rocks

        def handle_rock_collisions():
            for rock in interact.rocks:
                if interact.truck.rock_collision(rock):
                    if interact.lives.three_lives:
                        interact.lives.three_lives = False
                    elif interact.lives.two_lives:
                        interact.lives.two_lives = False
                    elif interact.lives.one_life:
                        interact.lives.one_life = False
                        interact.ALL_LIVES_LOST = True
        interact.handle_rock_collisions = handle_rock_collisions

        def handle_truck_rotation():
            if interact.truck.on_ground:
                if interact.truck.angle > 1.2 or interact.truck.angle < -1.2:
                    if interact.lives.three_lives:
                        interact.lives.three_lives = False
                        interact.truck.angle = 0
                    elif interact.lives.two_lives:
                        interact.lives.two_lives = False
                        interact.truck.angle = 0
                    elif interact.lives.one_life:
                        interact.lives.one_life = False
                        interact.ALL_LIVES_LOST = True
        interact.handle_truck_rotation = handle_truck_rotation

        return interact

    def wrap_text(self, text, max_chars):
        words = text.split(" ")
        lines = []
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 <= max_chars:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        return lines

    def draw_instructions(self, canvas):
        y_offset = 150
        max_chars_per_line = 50
        instructions = [
            "Welcome to COLD WHEELS!",
            "Use the LEFT and RIGHT arrow keys to move the truck.",
            "Press the UP arrow key to activate the truck's monster suspension and jump!",
            "When airborne, use the arrow keys to tilt.",
            "Avoid crashing into rocks or landing incorrectly to keep your lives.",
            "Complete the level as fast as possible to earn more points.",
            "Collect the nitro boost (yellow circle) for a speed boost and flames!",
            "Good luck and have fun!"
        ]
        canvas.draw_text("HOW TO PLAY", (self.WIDTH / 3, 100), 50, "white", "monospace")
        for line in instructions:
            for wrapped in self.wrap_text(line, max_chars_per_line):
                canvas.draw_text(wrapped, (50, y_offset), 30, "white", "monospace")
                y_offset += 40

    def draw_game_start(self, canvas):
        canvas.draw_text("COLD WHEELS", (self.WIDTH / 6, self.HEIGHT / 5), 100, "white", "monospace")
        canvas.draw_polygon([
            (0, self.HEIGHT - 130), 
            (self.GAME_LENGTH, self.HEIGHT - 130), 
            (self.GAME_LENGTH, self.HEIGHT), 
            (0, self.HEIGHT)
        ], 1, "green", "green")
        canvas.draw_image(
            self.TRUCK_IMG, (200, 72), (400, 144), 
            (self.WIDTH / 2, self.HEIGHT / 2), (400, 144)
        )
        canvas.draw_image(
            self.TYRE_IMG, (100, 100), (200, 199), 
            (400, 400), (140, 140)
        )
        canvas.draw_image(
            self.TYRE_IMG, (100, 100), (200, 199), 
            (610, 400), (140, 140)
        )
        canvas.draw_image(
            self.ROCK_IMG, (125, 91.5), (250, 183), 
            (40, 435), (167, 122)
        )
        canvas.draw_image(
            self.ROCK_IMG, (125, 91.5), (250, 183), 
            (200, 435), (167, 122)
        )
        canvas.draw_image(
            self.ROCK_IMG, (125, 91.5), (250, 183), 
            (870, 435), (167, 122)
        )

    def draw_gameplay(self, canvas, offset):
        self.elapsed_time = time.time() - self.start_time
        self.calculate_points(self.elapsed_time)
        canvas.draw_text("Time: " + str(int(self.elapsed_time)) + "s", (800, 100), 30, "white")
        canvas.draw_text("Points: " + str(self.points), (800, 150), 30, "white")

        canvas.draw_polygon([
            (0 - offset, self.HEIGHT - 100), 
            (self.GAME_LENGTH - offset, self.HEIGHT - 100),
            (self.GAME_LENGTH - offset, self.HEIGHT), 
            (0 - offset, self.HEIGHT)
        ], 1, "black", "green")
        canvas.draw_text("START", (20 - offset, self.HEIGHT - 120), 20, "white")

        progress = min(self.WIDTH * (self.interact.truck.pos.x / self.GAME_LENGTH), self.WIDTH)
        canvas.draw_line((0, 60), (self.WIDTH, 60), 10, "gray")
        canvas.draw_line((0, 60), (progress, 60), 10, "blue")

        for nitro in self.interact.nitro_boosts:
            nitro.draw(canvas, offset)
        for ramp in self.interact.ramps:
            ramp.draw(canvas, offset)

        self.interact.truck.draw(canvas, offset, self.TRUCK_IMG, self.TYRE_IMG, self.FLAME_IMG)
        self.interact.lives.draw(canvas, self.HEART_IMG)
        self.interact.truck.ramp_collision(self.interact.kbd)
        self.interact.update(canvas)

        self.interact.spawn_rocks(self.SPAWN_OFFSET, self.ZONE_WIDTH, self.HEIGHT)
        self.interact.handle_rock_collisions()
        self.interact.handle_truck_rotation()
        
        for rock in self.interact.rocks:
            rock.draw(canvas, offset, self.ROCK_IMG)

        if self.interact.truck.pos.x >= self.GAME_LENGTH - 100:
            self.final_points = self.points
            self.GAME_OVER = True
            self.GAME_STARTED = False

    def calculate_points(self, elapsed_time):
        base_points = 10
        time_penalty = int(elapsed_time)
        distance_bonus = int(self.interact.truck.pos.x / 100) * 5
        self.points = max(0, base_points - time_penalty + distance_bonus)

    def draw_game_over(self, canvas):
        canvas.draw_text("TIME: " + str(int(self.elapsed_time)) + "s", 
                         (self.WIDTH / 2 - 125, self.HEIGHT / 2 - 150), 40, "green", "monospace")
        canvas.draw_text("GAME OVER", 
                         (self.WIDTH / 2 - 150, self.HEIGHT / 2 - 50), 50, "green", "monospace")
        canvas.draw_text("POINTS: " + str(self.final_points), 
                         (self.WIDTH / 2 - 135, self.HEIGHT / 2 + 50), 40, "green", "monospace")
        canvas.draw_text("PRESS RESTART TO PLAY AGAIN", 
                         (self.WIDTH / 2 - 400, self.HEIGHT - 100), 50, "green", "monospace")

    def restart(self):
        if self.GAME_OVER:
            self.GAME_STARTED = False
            self.DISPLAY_INSTRUCTIONS = False
            self.GAME_OVER = False
            self.interact.truck.reset()
            self.interact.lives.reset()
            self.interact.ALL_LIVES_LOST = False
            self.start_time = time.time()
            self.points = 0
            self.final_points = 0

    def draw_explosion(self, canvas, offset):
        self.clock.tick()
        if self.clock.transition(5):
            self.spritesheet.next_frame()
            self.clock.time = 0
        self.spritesheet.draw(canvas, self.interact.truck, offset)

    def draw_lives(self, canvas, offset): 
        if self.interact.ALL_LIVES_LOST:
            self.final_points = 0
            self.draw_explosion(canvas, offset)
            if self.spritesheet.fin:
                self.GAME_OVER = True
                self.GAME_STARTED = False 
                self.ALL_LIVES_LOST = False 
                self.spritesheet.reset()

    def draw(self, canvas):
        truck_speed = self.interact.truck.vel.x
        for cloud in self.clouds:
            cloud.update(self.WIDTH, truck_speed)
            cloud.draw(canvas)
        
        if self.DISPLAY_INSTRUCTIONS:
            self.draw_instructions(canvas)
        elif not self.GAME_STARTED and not self.GAME_OVER:
            self.draw_game_start(canvas)
        elif self.GAME_STARTED:
            offset = max(0, self.interact.truck.pos.x - self.WIDTH / 2)
            if offset > self.GAME_LENGTH - self.WIDTH:
                offset = self.GAME_LENGTH - self.WIDTH
            self.draw_gameplay(canvas, offset)
            self.draw_lives(canvas, offset)
        if self.GAME_OVER:
            self.draw_game_over(canvas)
        if self.RESTART and not self.GAME_STARTED and self.GAME_OVER:
            self.restart()
            self.draw_game_start(canvas)
            self.RESTART = False

