import pygame
import math
import random
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
    global screen, width, height, keys, playerpos, accuracy, arrows
    global badtimer,badtimer1, badguys, healthvalue

    # initializing game and game-related variables
    pygame.init()
    width, height = 640, 480 # screen width and height
    keys = [False, False, False, False] # game keys (WASD)
    playerpos=[100,100] # player position
    accuracy =[0,0] # player's accuracy
    arrows = [] # arrows
    badtimer=100 # timer to decrease for bad guys to appear 
    badtimer1=0 # timer to increase for bad guys to appear/disappear
    badguys=[[640,100]] # bad guys initial opsition
    healthvalue=194 # health value
    screen = pygame.display.set_mode((width, height))

def load_resources():
    """Loading game resources
    """
    # initializing global variables
    global player, grass, castle, arrow, gameover
    global badguyimg, badguyimg1, healthbar, health, youwin

    # loading resources 
    player = pygame.image.load("resources/images/dude.png")
    grass = pygame.image.load("resources/images/grass.png")
    castle = pygame.image.load("resources/images/castle.png")
    arrow = pygame.image.load("resources/images/bullet.png")
    healthbar = pygame.image.load("resources/images/healthbar.png")
    health = pygame.image.load("resources/images/health.png")
    badguyimg1 = pygame.image.load("resources/images/badguy.png")
    gameover = pygame.image.load("resources/images/gameover.png")
    youwin = pygame.image.load("resources/images/youwin.png")
    badguyimg = badguyimg1

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
    global player, playerpos, playerpos1
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

def draw_arrows():
    """Drawing the arrows fired by the player
    """
    # referencing global variables  
    global arrow, arrows

    # updating arrows position with velocity components
    for bullet in arrows:
        index=0
        # velocity vector components:
        # x-component: cos(angle) * acceleration
        # y-compoent: sin(angle) * acceleration
        velx=math.cos(bullet[0])*10 # x-component of the velocity vector 
        vely=math.sin(bullet[0])*10 # y-value of the velocity vector
        # adding velocities to the arrows position components
        bullet[1]+=velx
        bullet[2]+=vely
        # removing arrow from screen
        if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
            arrows.pop(index)
        index+=1

    # drawing arrows on screen
    for projectile in arrows:
        arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
        screen.blit(arrow1, (projectile[1], projectile[2]))

def draw_bad_guys():
    """Drawing bad guys 
    """
    # referencing global variables
    global badtimer, badtimer1, badguys, badguyimg 
    global healthvalue, accuracy, arrows

    # check if its time to add a new bad guy to the screen
    if badtimer == 0:
        # ok, its tim to add a new bad guy
        # adding a bad guy from any y-coordinate from the right of the screen
        # with boundaries
        badguys.append([640, random.randint(50,430)])
        # reduce time for bad guys to appear
        badtimer=100-(badtimer1*2)
        # check for another timer
        if badtimer1>=35:
            badtimer1=35
        else:
            badtimer1+=5
    index=0
    for badguy in badguys:
        # remove bad guys if they went off-screen
        if badguy[0]<-64:
            badguys.pop(index)
        # reduce bad guys x-position (move to the left)
        badguy[0]-=5 # use this variable to modify bad guys speed

        # blowing up castle
        badrect=pygame.Rect(badguyimg.get_rect())
        badrect.top=badguy[1]
        badrect.left=badguy[0]
        if badrect.left<64:
            healthvalue -= random.randint(5,20)
            badguys.pop(index)

        # keeping track of current arrow
        index1=0

        # checking for collision between bad guys and arrows
        for bullet in arrows:
            bullrect=pygame.Rect(arrow.get_rect()) # arrow rect
            bullrect.left=bullet[1] # left?
            bullrect.top=bullet[2] # top?

            # checking for collision between arrow and badguy
            if badrect.colliderect(bullrect):
                # a collision happened, increase accuracy?
                accuracy[0]+=1
                # removing bad guy and arrow from screen
                badguys.pop(index)
                arrows.pop(index1)
            index1+=1

        # keeping track of current bad guy
        index+=1

    # drawing bad guys
    for badguy in badguys:
        screen.blit(badguyimg, badguy)

def draw_clock():
    """Drawing a timer
    """
    # creating a font with size
    font = pygame.font.Font(None, 24) 
    # rendering a text containing the current time
    survivedtext = font.render(
        (str((90000-pygame.time.get_ticks())/60000)+
            ":"+str((90000-pygame.time.get_ticks())/1000%60).zfill(2)), 
        True,(0,0,0))

    # retrieving rect for text
    textRect = survivedtext.get_rect()
    # positioning text on top right corner
    textRect.topright=[635,5]
    # drawing text onto the screen
    screen.blit(survivedtext, textRect)

def draw_health():
    """Drawing health bar
    """
    # referencing global variables
    global healthbar, health, healthvalue

    # drawing health  bar
    screen.blit(healthbar, (5,5))
    for health1 in range(healthvalue):
        # according to how much value left, draw health
        screen.blit(health, (health1+8,8))

def check_for_end():
    """Checking for the end of game
    """
    # referencing global variables
    global running, exitcode, accuracy, gameover, accuracy_str

    # check if game needs to end
    if pygame.time.get_ticks()>=90000:
        # time has elapsed
        running=0
        exitcode=1
    if healthvalue<=0:
        # player health is gone
        running=0
        exitcode=0
    if accuracy[1]!=0:
        accuracy_str=accuracy[0]*1.0/accuracy[1]*100
    else:
        accuracy_str=0

def end_game():
    """Ending game
    """
    # referencing global variables
    global accuracy_str, gameover, youwin
    # check if player won/lost        
    if exitcode==0:
        # player lost
        pygame.font.init()
        font = pygame.font.Font(None, 24) # creating font
        # rendering text
        text = font.render("Accuracy: "+str(accuracy_str)+"%", True, (255,0,0))
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery+24
        screen.blit(gameover, (0,0))
        screen.blit(text, textRect) # adding text to screen
    else:
        # player won
        pygame.font.init()
        font = pygame.font.Font(None, 24) # creating font
        # rendering text
        text = font.render("Accuracy: "+str(accuracy_str)+"%", True, (0,255,0))
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery+24
        screen.blit(youwin, (0,0))
        screen.blit(text, textRect) # adding text to screen

    pygame.display.flip()
    
    # giving user the ability to quit game
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)


def game_events():
    """Checking for game events
    """
    # referencing global variables
    global keys, playerpos, accuracy, arrows, playerpos1
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
        # checking if mouse was clicked AKA an arrow was fired!
        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos() # mouse position
            accuracy[1]+=1 # increase y accuracy
            # calculating the arrow rotation based on the rotated player 
            # position and the cursor position. 
            # This rotation value is stored in the arrows array.
            # arrow = (angle, x, y)
            arrows.append(
                [math.atan2(
                    position[1]-(playerpos1[1]+32),
                    position[0]-(playerpos1[0]+26)),
                playerpos1[0]+32,playerpos1[1]+32])

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
    global screen, badtimer
    # initializing global variables
    global running, exitcode
    
    running = 1 # use to determine if player wins or loses
    exitcode = 0 # use to determine if game should be finished

    # keeping looping through game
    while running:
        # clear screen before drawing it again
        screen.fill(0)
        draw_grass() # drawing grass
        draw_castle() # drawing castle(s)
        draw_player() # drawing player
        draw_arrows() # drawing arrows
        draw_bad_guys() # drawing bad guys
        draw_clock() # drawing a clock
        draw_health() # drawing health!
        pygame.display.flip() # update the screen
        game_events() # loading game events
        # updating bad time for guys to appear
        badtimer-=1
        # checking for end game
        check_for_end()
    # ending game
    end_game()

if __name__ == "__main__":
    main()