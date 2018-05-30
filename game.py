import pygame
from pygame.locals import *

# initializing game
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

# loading resources for player
player = pygame.image.load("resources/images/dude.png")

# keeping looping through game
while 1:
    # clear screen before drawing it again
    screen.fill(0)
    # draw the screen elements
    screen.blit(player, (100, 100))
    # update the screen
    pygame.display.flip()
    # loop through events
    for event in pygame.event.get():
        # check if the event is the X button
        if event.type == pygame.QUIT:
            # if it is, quit the game
            pygame.quit()
            exit(0)
        