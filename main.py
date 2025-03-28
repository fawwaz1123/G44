try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import time
import random
from vector import Vector
from keyboard import Keyboard
from lives import Lives
from rock import Rock
from truck import Truck
from wheel import Wheel
from spritesheet import Spritesheet
from clock import Clock
from interaction import Interaction
from variables import WIDTH, HEIGHT, GAME_LENGTH, BUTTON_WIDTH, GAME_STARTED, GAME_OVER, DISPLAY_INSTRUCTIONS, DISPLAY_LEVEL_CHOICE, start_time, elapsed_time, points, EXPLOSION_IMG, BANNER_IMG,final_points

# Additional constants for rock spawning.
SPAWN_OFFSET = 300  # Increased so rocks spawn further ahead of the truck.
ZONE_WIDTH = 200    # Width of the spawn zone.
 
class Background:
    def __init__(self):
        self.color = "#4cb7f5"
    def get_color(self):
        return self.color

# Global objects
kbd = Keyboard()
truck = Truck()
background = Background()
lives = Lives()
spritesheet = Spritesheet(EXPLOSION_IMG)
clock = Clock()
interact = Interaction(truck, kbd, background, lives)

rocks = []         # Global list to hold multiple Rock objects.
next_spawn = GAME_LENGTH / 4  # Next spawn threshold (in x-coordinate).

def wrap_text(text, max_chars):
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

def draw_instructions(canvas):
    y_offset = 150
    max_chars_per_line = 50
    instructions = [
        "Welcome to COLD WHEELS!",
        "Use the LEFT and RIGHT arrow keys to move the truck.",
        "Press the UP arrow key to jump.",
        "Collect coins along the road to earn extra points.",
        "Avoid crashing into objects or falling off the road to keep your lives.",
        "Complete the level as fast as possible to earn more points.",
        "Good luck and have fun!"
    ]
    canvas.draw_text("HOW TO PLAY", (WIDTH / 3, 100), 50, "white", "monospace")
    for line in instructions:
        wrapped_lines = wrap_text(line, max_chars_per_line)
        for wrapped_line in wrapped_lines:
            canvas.draw_text(wrapped_line, (50, y_offset), 30, "white", "monospace")
            y_offset += 40

def draw_level_choice(canvas):
    canvas.draw_text("SELECT LEVEL", (WIDTH / 3, HEIGHT / 4), 50, "white", "monospace")
    level_buttons = [
        ("LEVEL 1", (WIDTH / 3, HEIGHT / 3)),
        ("LEVEL 2", (WIDTH / 3, HEIGHT / 3 + 70)),
        ("LEVEL 3", (WIDTH / 3, HEIGHT / 3 + 140)),
    ]
    for text, (x, y) in level_buttons:
        canvas.draw_polygon([(x, y), (x + 200, y), (x + 200, y + 50), (x, y + 50)], 2, "white", "blue")
        canvas.draw_text(text, (x + 20, y + 35), 30, "yellow", "monospace")

def draw_game_start(canvas):
    canvas.draw_text("COLD WHEELS", [WIDTH / 6, HEIGHT / 5], 100, "white", "monospace")

def draw_gameplay(canvas, offset, elapsed_time, points):
    global rocks, next_spawn
    # Display time and points.
    canvas.draw_text("Time: " + str(int(elapsed_time)) + "s", (800, 100), 30, "white")
    canvas.draw_text("Points: " + str(points), (800, 150), 30, "white")
    
    # Draw lives.
    lives.draw(canvas)
    
    
    # Draw the road and banner.
    canvas.draw_polygon([(0 - offset, HEIGHT - 100), (GAME_LENGTH - offset, HEIGHT - 100),
                         (GAME_LENGTH - offset, HEIGHT), (0 - offset, HEIGHT)], 1, "black", "green")
    canvas.draw_text("START", (20 - offset, HEIGHT - 120), 20, "white")
    canvas.draw_image(BANNER_IMG, (400, 200), (800, 400), (GAME_LENGTH - 30 - offset, HEIGHT - 120), (100, 50))
    progress = min(WIDTH * (truck.pos.x / GAME_LENGTH), WIDTH)
    canvas.draw_line((0, 50), (WIDTH, 50), 10, "gray")
    canvas.draw_line((0, 50), (progress, 50), 10, "blue")
    
    # Update truck state.
    interact.update()
    truck.draw(canvas, offset)
    
    # Check if the truck is near the next spawn threshold.
    if (truck.pos.x + SPAWN_OFFSET >= next_spawn) and (next_spawn < GAME_LENGTH):
        zone_start = next_spawn
        # Spawn multiple rocks (e.g. 2 to 4) within the zone.
        num_rocks = random.randint(2, 4)
        for i in range(num_rocks):
            spawn_x = random.randint(int(zone_start), int(zone_start + ZONE_WIDTH))
            rocks.append(Rock(truck, spawn_x))
        next_spawn += GAME_LENGTH / 4  # Move to next zone.
    
    # Draw each rock and handle collisions.
    for rock in rocks:
        rock.draw(canvas, offset)
        truck.rock_collision(rock)

def draw_explosion(canvas, offset):
    clock.tick()
    if clock.transition(5):
        spritesheet.next_frame()
        clock.time = 0
    spritesheet.draw(canvas, truck, offset)

def draw_game_over(canvas, points, elapsed_time):
    canvas.draw_text("FINISHED", (WIDTH / 2 - 100, HEIGHT / 2), 50, "green", "monospace")
    canvas.draw_text("POINTS: " + str(final_points), (WIDTH / 2 - 100, HEIGHT / 2 + 60), 40, "green", "monospace")
    canvas.draw_text("TIME: " + str(int(elapsed_time)) + "s", (WIDTH / 2 - 100, HEIGHT / 2 - 200), 50, "green", "monospace")

def draw_lives(canvas, offset):
    if truck.on_ground: # truck only explodes on ground
            if truck.angle > 1.2 or truck.angle < -1.2:
                if lives.three_lives:
                    lives.three_lives = False
                    truck.angle = 0
                elif lives.two_lives:
                    lives.two_lives = False
                    truck.angle = 0
                elif lives.one_life:
                    lives.one_life = False
                
    if lives.one_life == False:  # once all lives are lost
        draw_explosion(canvas, offset)
        # end game

def draw(canvas):
    global elapsed_time, points, GAME_OVER, GAME_STARTED
    if DISPLAY_INSTRUCTIONS:
        draw_instructions(canvas)
    elif DISPLAY_LEVEL_CHOICE:
        draw_level_choice(canvas)
    elif not GAME_STARTED and not GAME_OVER:
        draw_game_start(canvas)
    elif GAME_STARTED:
        elapsed_time = time.time() - start_time
        offset = max(0, truck.pos.x - WIDTH / 2)
        if offset > GAME_LENGTH - WIDTH:
            offset = GAME_LENGTH - WIDTH
        base_points = 10
        time_penalty = int(elapsed_time)
        distance_bonus = int(truck.pos.x / 100) * 5
        points = max(0, base_points - time_penalty + distance_bonus)
        draw_gameplay(canvas, offset, elapsed_time, points)

        # Check if the game is over
        if truck.pos.x >= GAME_LENGTH - 100:
            final_points = points 
            GAME_OVER = True
            GAME_STARTED = False
            final_points = points 
        
        draw_lives(canvas, offset)    
    if GAME_OVER:
        draw_game_over(canvas, points, elapsed_time)

def play():
    global GAME_STARTED, start_time, GAME_OVER, points, DISPLAY_INSTRUCTIONS, DISPLAY_LEVEL_CHOICE, rocks, next_spawn
    GAME_STARTED = True
    GAME_OVER = False
    DISPLAY_INSTRUCTIONS = False
    DISPLAY_LEVEL_CHOICE = False
    start_time = time.time()
    points = 0
    rocks = []              # Reset the rock list.
    next_spawn = GAME_LENGTH / 4  # Reset spawn threshold.
    truck.pos = Vector(200, HEIGHT - 150)
    truck.vel = Vector(0, 0)
    truck.angle = 0
    truck.started = False

def instructions():
    global DISPLAY_INSTRUCTIONS, GAME_STARTED, DISPLAY_LEVEL_CHOICE
    DISPLAY_INSTRUCTIONS = True
    GAME_STARTED = False
    DISPLAY_LEVEL_CHOICE = False

def levels():
    global DISPLAY_LEVEL_CHOICE
    DISPLAY_LEVEL_CHOICE = True

def exit_game():
    frame.stop()

frame = simplegui.create_frame("COLD WHEELS", WIDTH, HEIGHT)
frame.set_canvas_background(background.get_color())
frame.set_draw_handler(draw)
frame.set_keydown_handler(kbd.key_down)
frame.set_keyup_handler(kbd.key_up)
frame.add_button("PLAY", play, BUTTON_WIDTH)
frame.add_button("HOW TO PLAY", instructions, BUTTON_WIDTH)
frame.add_button("LEVELS", levels, BUTTON_WIDTH)
frame.add_button("EXIT", exit_game, BUTTON_WIDTH)
frame.start()
