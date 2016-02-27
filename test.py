"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/
"""
 
import pygame

from sappho import AnimatedSprite, TileMap, Tilesheet, tmx_file_to_tilemap_csv_string

 
WHITE = (255, 255, 255)

TILEMAP_CSV_STRING = "0,16,8\n9,4,2\n3,1,5"
 

# Setup
pygame.init()
 
# Set the width and height of the screen [width,height]
size = [700, 500]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Hide the mouse cursor
pygame.mouse.set_visible(0)
 
# Speed in pixels per frame
x_speed = 0
y_speed = 0
 
# Current position
x_coord = 10
y_coord = 10

animated_sprite = AnimatedSprite.from_file('test.gif')
tilesheet = Tilesheet.from_file('test_scene/tilesheet.png', 10, 10)

tilemap_csv_string = tmx_file_to_tilemap_csv_string("test_scene/test.tmx")
tilemap = TileMap.from_csv_string_and_tilesheet(tilemap_csv_string, tilesheet)
tilemap_surface = tilemap.to_surface()
 

# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            # User pressed down on a key
 
        elif event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            if event.key == pygame.K_LEFT:
                x_speed = -3
            elif event.key == pygame.K_RIGHT:
                x_speed = 3
            elif event.key == pygame.K_UP:
                y_speed = -3
            elif event.key == pygame.K_DOWN:
                y_speed = 3
 
        # User let up on a key
        elif event.type == pygame.KEYUP:
            # If it is an arrow key, reset vector back to zero
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_speed = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y_speed = 0
 
    # --- Game Logic
 
    # Move the object according to the speed vector.
    x_coord = x_coord + x_speed
    y_coord = y_coord + y_speed
 
    # --- Drawing Code
    #
    # First, clear the screen to WHITE. Don't put other drawing commands
    # above this, or they will be erased with this command.
    # screen.fill(WHITE)
    #
    # --- Background
    screen.blit(tilemap_surface, (0, 0))
 
    screen.blit(animated_sprite.image, (x_coord, y_coord))
    animated_sprite.update(clock)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # Limit frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()
