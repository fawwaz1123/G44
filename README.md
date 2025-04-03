# G44
Team project for python game
background.py contains method to define a blue background
clock.py defines the clock to be used by spritesheet.py for explosions for frame rate and when to end
cloud.py define the clouds to be drawn on the canvas
game_keyboard.py define the keyboard input to be used for movement
game.py inclues the variables and methods that define the whole game with different screens
interaction.py takes the instatiated objects and handles the interaction between the objects
lives.py define the lives objects which is drawn and shows changes when hitting a rock or when upside down
main.py instatiates the game object and creates a canvas and define the draw, keyboard and buttons
nitro_boost.py define methods that spawns nitro boosts on screen and causes the truck to speed up
ramp.py defines the ramp and draws on the canvas a ramp
rock.py define the rocks and draws on canvas at certains parts in the game and handles collision with the truck 
spritesheet.py defines the exploasions sprite which is drawn
truck.py define the truck object which draws a truck and creates a wheel object and has all methods to involve its movements and collisions
wheel.py defines the wheel object which draws a wheel and calls the truck object to be with the truck as it moves as one whole object 
vector.py defines the vector class
