# falling platform jumping game by julius and daddy

import pygame
from lib.elements import *
from lib.utils import *
from lib.items import *
pygame.init()


###########################
# Game Elements
player = Player(200,-100)
game = Game()

# first platform
game.platforms.append(Platform(0,0,game.width,10,(234,14,153),2,-1))


factory = PlatformFactory(game,player)
factory.addPlatform( game, player )


# __DEV__
doDrop = True


clock = pygame.time.Clock()
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
    if player.life > 0:
        if pressed_buttons[pygame.K_LEFT]:
            game.left = True
        if pressed_buttons[pygame.K_RIGHT]:
            game.right = True
        if pressed_buttons[pygame.K_UP]:
            game.up = True
        if pressed_buttons[pygame.K_j]:
            game.jet = True


    ###########################
    # Game dynamics
    topPlatformY = game.platforms[len(game.platforms)-1].hitbox[1]
    if topPlatformY > 10:
        factory.addPlatform( game, player )

   # development mode
    if player.hitbox[1] > 1000:
        player.hitbox[1] = -50
        player.vel_y = 0
        player.vel_x = 0
        player.platform = None
        player.hitbox[0] = int(game.width/2 - player.hitbox[2]/2)
        player.life -= 1


    if player.life > 0:
        game.drop() 
        player.drop(game)   
        player.move(game)
        game.resetLoop()  
        game.redrawgamewindow(player)
    else:
        game.gameover(player)