try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


import time
from game import Game

# Create the game instance
game = Game()

# Define control functions
def play():
    game.GAME_STARTED = True
    game.GAME_OVER = False
    game.DISPLAY_INSTRUCTIONS = False
    game.interact.ALL_LIVES_LOST = False
    game.start_time = time.time()
    game.points = 0
    game.final_points = 0
    game.interact.truck.reset()
    game.interact.lives.reset()

def instructions():
    game.DISPLAY_INSTRUCTIONS = True
    game.GAME_STARTED = False

def exit_game():
    frame.stop()

def restart():
    if game.GAME_OVER:
        game.RESTART = True

# Set up the frame and handlers
frame = simplegui.create_frame("COLD WHEELS", game.WIDTH, game.HEIGHT)
frame.set_canvas_background(game.interact.background.get_color())
frame.set_draw_handler(game.draw)
frame.set_keydown_handler(game.interact.kbd.key_down)
frame.set_keyup_handler(game.interact.kbd.key_up)
frame.add_button("PLAY", play, game.BUTTON_WIDTH)
frame.add_button("HOW TO PLAY", instructions, game.BUTTON_WIDTH)
frame.add_button("RESTART", restart, game.BUTTON_WIDTH)
frame.add_button("EXIT", exit_game, game.BUTTON_WIDTH)
frame.start()
