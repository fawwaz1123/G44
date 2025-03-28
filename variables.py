try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
# constants
WIDTH, HEIGHT = 1000, 600
GAME_LENGTH = 5000
BUTTON_WIDTH = 150

# booleans
GAME_STARTED = False
GAME_OVER = False
DISPLAY_INSTRUCTIONS = False
DISPLAY_LEVEL_CHOICE = False 

# time and point tracker
start_time = 0
elapsed_time = 0
points = 0
final_points = 0
# Load Images
TRUCK_IMG_URL = "https://opengameart.org/sites/default/files/Body.png"
TYRE_IMG_URL = "https://opengameart.org/sites/default/files/Tire.png"
BANNER_IMG_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Checkered_flag.svg/800px-Checkered_flag.svg.png"
HEART_IMG_URL = "https://opengameart.org/sites/default/files/heart_15.png"
EXPLOSION_IMG_URL = "https://opengameart.org/sites/default/files/explosion1_6.png"

TRUCK_IMG = simplegui.load_image(TRUCK_IMG_URL)
TYRE_IMG = simplegui.load_image(TYRE_IMG_URL)
BANNER_IMG = simplegui.load_image(BANNER_IMG_URL)
HEART_IMG = simplegui.load_image(HEART_IMG_URL)
EXPLOSION_IMG = simplegui.load_image(EXPLOSION_IMG_URL)