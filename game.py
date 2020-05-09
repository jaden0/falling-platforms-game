# falling platform jumping game by julius and daddy

import pygame
from Classes import *
pygame.init()

# game components
gameHeight = 600
gameWidth = 800
topPlatformY = 1000
gravity = 2
win = pygame.display.set_mode((gameWidth, gameHeight),pygame.FULLSCREEN)
left = False
right = False
up = False
framesPerDrop = 2
dropFrame = 0
keys=[]
pygame.display.set_caption("Falling Platforms")
font = pygame.font.SysFont('comicsans', 30)
win.fill((0,0,0))

def redrawgamewindow():
    win.fill((0,0,0)) 
    text = font.render("Score: " + str(block.score), 1, (255,255,255))
    win.blit(text, (200, 10))
    text = font.render("Jetpacks: " + str(len(block.jetpacks)),1, (255,255,255))
    win.blit(text, (gameWidth * 3.5 / 5, 10))
    block.draw(win)
    for platform in platforms:
        platform.draw( win ) 
    pygame.display.update()

def gameOver():
    win.fill((0,0,0))
    font = pygame.font.SysFont('comicsans', 40)
    text = font.render("Game Over", 1, (255,255,50))
    win.blit( text, (200,200))
    text = font.render("Final Score: " + str(block.score), 1, (255,255,50))
    win.blit( text, (200,300))
    pygame.display.update()


###########################
# Game screen layout
sky_floor1 = platform(100,200,500,10,(245, 245, 66))
sky_floor2 = platform(1,200,400,10,(245, 245, 66))
floor = platform(0,500,590,10,(0,255,0))
sky_floor3 = platform(1,gameWidth-1,5,10,(245, 245, 66))
sky_floor4 = platform(1,200,310,10,(245, 245, 66))
sky_floor5 = platform(1,400,250,10,(245, 245, 66))
platforms = [sky_floor1, sky_floor2, sky_floor3, floor,sky_floor4 ,sky_floor5]
clock = pygame.time.Clock()
block = player(230,-50,40,40,gravity)
pFactory = platformFactory( gameWidth, 45, int(block.jumpVelocity**2 / (2 * gravity )) )
run = True
while run:
    ###########################
    # Loop basics
    clock.tick_busy_loop(60) 
    for event in pygame.event.get():  
        if event.type == pygame.QUIT: 
            run = False 

    ###########################
    # Button presses       
    pressed_buttons = pygame.key.get_pressed() 
    if pressed_buttons[pygame.K_q]:
        run = False 
    if pressed_buttons[pygame.K_LEFT] and block.x > 0 + block.vel_x:
        left = True
    if pressed_buttons[pygame.K_RIGHT] and block.x < gameWidth - block.vel_x - block.width:
        right = True
    if pressed_buttons[pygame.K_UP]  and (block.onPlatform or block.using_jetpack):
        up = True
        block.onPlatform = False
        if not block.using_jetpack:
            block.friction = 0
    if pressed_buttons[pygame.K_j]:
        block.useJetpack()

    ###########################
    # Game dynamics
    topPlatformY = 10000
    for platform in platforms:
        if topPlatformY > platform.y: 
           topPlatformY = platform.y
        block.checkForPlatform( platform )
        for coin in platform.coins:
            if block.checkForCoin( coin ):
                platform.coins.pop( platform.coins.index( coin ) )
        for jetpack in platform.jetpacks:
            if block.checkForJetpack( jetpack ):
                platform.jetpacks.pop( platform.jetpacks.index( jetpack ) )   
        if platform.y > gameHeight:
           platforms.pop( platforms.index( platform ) )

    if( topPlatformY > 0):
        newPlatform =  pFactory.makePlatform( platforms[len(platforms)-1], len(block.jetpacks) > 0 , block)
        platforms.append( newPlatform )


    if block.vel_y != 0:
       block.onPlatform = False
    block.move(left, right, up, gameWidth )

    # drop
    dropFrame += 1
    steps = 1
    if( dropFrame == framesPerDrop):
        dropFrame = 0
        for platform in platforms:
           platform.drop( steps )
        block.drop(steps)
    up = False
    right = False
    left = False
    #if( block.y < gameHeight ):
    redrawgamewindow()
    #else:
    #    gameOver()
pygame.quit()