import pygame
import math
from pygame.locals import *

def main():
    """Main game execution
    """
    game_init() # initializing game
    load_resources() # loading game resources
    game_loop() # looping through game

def game_init():
    """Initializing game
    """
    # initializing global variables
    global screen, width, height, keys, playerpos
    
    # initializing game
    pygame.init()
    width, height = 640, 480 # screen width and height
    keys = [False, False, False, False] # game keys (WASD)
    playerpos=[100,100] # player position
    screen = pygame.display.set_mode((width, height))

def load_resources():
    """Loading game resources
    """
    # initializing global variables
    global player, grass, castle

    # loading resources 
    player = pygame.image.load("resources/images/dude.png")
    grass = pygame.image.load("resources/images/grass.png")
    castle = pygame.image.load("resources/images/castle.png")

def draw_grass():
    """Drawing grass to the screen
    """
    # referencing global variables
    global width, height, grass, screen

    # iterating over width/grass_width
    for x in range(width/grass.get_width() + 1):
        # iterating over height/grass_height
        for y in range(height/grass.get_height()+1):
            # drawing grass on screen
            screen.blit(grass,(x*100,y*100))

def draw_castle():
    """Drawing castle
    """
    # referencing global variable(s)
    global castle, screen

    y_castle = 30
    # drawing castle(s) on the screen
    for x in range(4):
        screen.blit(castle, (0,y_castle))
        y_castle += 105

def draw_player():
    """Drawing player with z rotation
    """
    # referencing global variables
    global player, playerpos
    # calculazing z rotation value
    position = pygame.mouse.get_pos() # getting mouse position
    # calculating angle between mouse and player tan(angle) = (y2-y1)/(x2-x1)
    # angle = arctan((y2-y1)/(x2-x1))
    # angle is in radians
    angle = math.atan2(
        position[1]-(playerpos[1]+32),
        position[0]-(playerpos[0]+26)
    )
    angle_degress = 360-angle*57.29
    # player rotation
    playerrot = pygame.transform.rotate(player, angle_degress)
    # player new position
    playerpos1 = (
        playerpos[0]-playerrot.get_rect().width/2, 
        playerpos[1]-playerrot.get_rect().height/2)
    # drawing player on the screen
    screen.blit(playerrot, playerpos1)

def game_events():
    """Checking for game events
    """
    # referencing global variables
    global keys, playerpos
    # loop through events
    for event in pygame.event.get():
        # check if the event is the X button
        if event.type == pygame.QUIT:
            # if it is, quit the game
            pygame.quit()
            exit(0)
        # checking for key down keyboard events
        if event.type == pygame.KEYDOWN:
            if event.key == K_w: # 'w' key was pressed down
                keys[0] = True
            if event.key == K_a: # 'a' key was pressed down
                keys[1] = True
            if event.key == K_s: # 's' key was pressed down 
                keys[2] = True
            if event.key == K_d: # 'd' key was pressed down
                keys[3] = True
        # checking for key up keyboard events
        if event.type == pygame.KEYUP:
            if event.key == K_w: # 'w' key was pressed up
                keys[0] = False
            if event.key == K_a: # 'a' key was pressed up
                keys[1] = False
            if event.key == K_s: # 's' key was pressed up 
                keys[2] = False
            if event.key == K_d: # 'd' key was pressed up
                keys[3] = False

    # updating player position based on which key was pressed 
    # AKA moving player
    if keys[0]:
        playerpos[1]-=5
    elif keys[2]:
        playerpos[1]+=5
    if keys[1]:
        playerpos[0]-=5
    elif keys[3]:
        playerpos[0]+=5

def game_loop():
    """Infinite game loop
    """
    # referencing global variables
    global screen

    # keeping looping through game
    while True:
        # clear screen before drawing it again
        screen.fill(0)
        # drawing grass
        draw_grass()
        # drawing castle(s)
        draw_castle()
        # drawing player
        draw_player()
        # update the screen
        pygame.display.flip()
        # loading game events
        game_events()

if __name__ == "__main__":
    main()