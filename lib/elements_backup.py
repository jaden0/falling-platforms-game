import pygame 
import random
from lib.utils import *
from lib.items import *



class Player(object):
    def __init__(self, x,y):
        width = 36
        height = 54
        self.runRight = []
        self.runLeft = []
        self.idleRight = []
        self.idleLeft = []
        self.jumpRight = []
        self.jumpLeft = []
        self.score = 0
        self.vel_x = 0
        self.vel_y = 0
        self.jump_velocity = 15
        self.acceleration_x = .1
        self.max_vel_x = 3
        self.friction = 1
        self.hitbox = [x, y, width, height]
        self.platform = None
        self.score = 0
        self.jetpacks = 0
        self.using_jetpack = False
        self.life = 3
        self.state = 4 # 0: runRight, 1: runLeft, 2: jumpRight, 3:jumpLeft 4:idleRight 5: idleLeft
        self.animationStep = 0
        self.framesPerPic = 3
        self.padding = [15,8,24,5] # top left right bottom
        self.drawbox = [0,0,0,0] 
        paddedWidth = width + self.padding[1] + self.padding[2]
        paddedHeight = height + self.padding[0] + self.padding[3]
        for i in range(1,11):
            self.runRight.append(pygame.transform.scale(pygame.image.load("images/character/png/Run (%d).png" % i), (paddedWidth, paddedHeight)) )
            self.runLeft.append(pygame.transform.scale(pygame.transform.flip( pygame.image.load("images/character/png/Run (%d).png" % i ), True, False  ), (paddedWidth,paddedHeight) ) )
            self.idleRight.append(pygame.transform.scale( pygame.image.load("images/character/png/Idle (%d).png" % i ), (paddedWidth, paddedHeight)) )
            self.jumpRight.append(pygame.transform.scale(pygame.image.load("images/character/png/Jump (%d).png" % i), (paddedWidth, paddedHeight)) )
            self.jumpLeft.append(pygame.transform.scale(pygame.transform.flip( pygame.image.load("images/character/png/Jump (%d).png" % i ), True, False  ), (paddedWidth,paddedHeight) ) )
            self.idleLeft.append(pygame.transform.scale(pygame.transform.flip( pygame.image.load("images/character/png/Idle (%d).png" % i ), True, False  ), (paddedWidth,paddedHeight) ) )
    def setState(self, state):
        if self.state != state:
            self.state = state
            self.animationStep = 0
        
    def move(self, game):
        # left and right
        if game.left and game.right:
            game.left = False
            game.right = False
        if game.left:
            if not self.platform is None:
                self.setState(1)
            self.vel_x = max(self.vel_x - self.acceleration_x * self.friction *2, -self.max_vel_x)
        elif game.right:
            if not self.platform is None:
                self.setState(0)
            self.vel_x = min(self.vel_x + self.acceleration_x * self.friction *2, self.max_vel_x)
        else:
            if not self.platform is None:
                if self.vel_x < 0:
                    self.setState(5)
                    self.vel_x = min(0, self.vel_x +self.acceleration_x * self.friction)
                elif self.vel_x > 0:
                    self.setState(4)
                    self.vel_x = max(0,self.vel_x - self.acceleration_x * self.friction)
                else:
                    if self.state == 2:
                        self.setState(4)
                    elif self.state == 3:
                        self.setState(5)


        # gravity and jump
        self.vel_y += game.gravity
        if self.platform is not None and game.up and not self.using_jetpack:
            self.vel_y = -self.jump_velocity
            self.platform = None
            self.friction = 0
            game.jumpSound.play()
            if self.vel_x < 0:
                self.setState(3)
            elif self.vel_x >0:
                self.setState(2)
            else: 
                if self.state == 5:
                    self.setState(3)
                elif self.state == 4:
                    self.setState(2)

        # jetpack 
        if game.jet and not self.using_jetpack:
            if self.jetpacks > 0:
                self.jetpacks -= 1
                self.using_jetpack = True
                self.jetpack_fuel = game.jetpackFuel
                self.friction = 2
            else:
                pass # TODO: play out of jetpacks sound
        if self.using_jetpack and game.up:
            game.jetpackSound.play()
            self.platform = None
            self.vel_y -= game.jetpackForce
            self.jetpack_fuel -= 1
            if self.jetpack_fuel == 0:
                self.using_jetpack = False
        else:
            game.jetpackSound.stop()

        # platform dynamics
        if self.platform is None:
            for platform in game.platforms:
                if land( self, platform):
                    game.landSound.play()
                    self.hitbox[1]=platform.hitbox[1]-self.hitbox[3]
                    self.vel_y = 0
                    self.platform = platform
                    self.friction = platform.friction


                if bump( self, platform):
                    self.hitbox[1]=platform.hitbox[1]+platform.hitbox[3]
                    game.bumpSound.play()
                    self.vel_y = 0

        else:
            self.vel_y = 0
            if not verticleTouch(self,self.platform):
                self.platform = None
                self.friction = 0
                if self.vel_x < 0:
                    self.setState(3)
                if self.vel_x > 0:
                    self.setState(2)
                print( "fall off side")

        # Actually move
        if self.hitbox[0] + self.vel_x >= 0 and self.hitbox[0]+self.hitbox[2] <= game.width:
            self.hitbox[0] += self.vel_x
        else:
            if self.vel_x < 0:
                self.hitbox[0] = 0
            else:
                self.hitbox[0] = game.width - self.hitbox[2]
            self.vel_x = 0
        self.hitbox[1] += self.vel_y

        # get items
        for platform in game.platforms:
            for coin in platform.coins:
                if self.getItem( coin ,game):
                    print( "got coin")
                    platform.coins.pop( platform.coins.index( coin ) )
            for jetpack in platform.jetpacks:
                if self.getItem( jetpack ,game):
                    print( "got jetpack")
                    platform.jetpacks.pop( platform.jetpacks.index( jetpack) )
    def getItem(self,item,game):
        if inBox( item.touchpoint, self.hitbox):
            if type(item) is Coin:
                self.score += 1
                game.coinSound.play()
                return( True )
            elif type( item) is Jetpack:
                self.jetpacks += 1
                return( True )
        else:
            return( False )


    def drop( self, game):
        if game.dropFrame == 0:
            self.hitbox[1] += game.dropSteps

    def draw(self, win):
        leftShift = 15
        self.drawbox = [self.hitbox[0]-self.padding[1],self.hitbox[1]-self.padding[0],self.hitbox[2],self.hitbox[3]]
        if self.state in (1,3,5):
            self.drawbox[0] -= leftShift
        if self.using_jetpack:
            pygame.draw.rect(win, (255,40,0), self.hitbox) # TODO: draw the jetpack here
        if self.state == 0:
            win.blit(self.runRight[self.animationStep // self.framesPerPic], self.drawbox)
        elif self.state == 1:
            win.blit(self.runLeft[self.animationStep // self.framesPerPic], self.drawbox)
        elif self.state == 2:
            win.blit(self.jumpRight[self.animationStep // self.framesPerPic], self.drawbox)
        elif self.state == 3:
            win.blit(self.jumpLeft[self.animationStep // self.framesPerPic], self.drawbox)
        elif self.state == 4:
            win.blit(self.idleRight[self.animationStep // self.framesPerPic], self.drawbox)
        elif self.state == 5:
            win.blit(self.idleLeft[self.animationStep // self.framesPerPic], self.drawbox)
        self.animationStep += 1
        if self.animationStep == self.framesPerPic * 10:
            self.animationStep = 0
        #pygame.draw.rect(win, (255,40,0), self.hitbox, 2) 
     
       


class Platform(object):
    def __init__(self,x,y,width,height,color,friction, id):
        self.hitbox = [x, y, width, height]
        self.color = color
        self.friction = friction
        self.id = id
        self.font = pygame.font.SysFont('comicsans', 20)
        self.text = self.font.render(str(self.id),1, (255,255,255))
        self.jetpacks = []
        self.coins = []
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.hitbox)
        win.blit(self.text, (self.hitbox[0]+self.hitbox[2]-10, self.hitbox[1]-12))
        for coin in self.coins:
            coin.draw(win)
        for jetpack in self.jetpacks:
            jetpack.draw(win)


class PlatformFactory(object):
    def __init__(self, game, player):
        self.gameWidth = game.width
        self.gameHeight = game.height
        self.minHeight = int(player.hitbox[3]*1.2)
        self.maxHeight = int(player.jump_velocity**2 / (2 * game.gravity ))
        self.id = 1
        self.itemFactory = ItemFactory()
    
    def addPlatform(self, game, player):
        goodPlatform = False
        while( not goodPlatform):
            mustBeJumpable = True
            if game.greatLeaps > 0:
                mustBeJumpable = False
            aPlatform = self.suggestPlatform( game )
            if self.isPlatformJumpable( aPlatform, game, player) or not mustBeJumpable:
                goodPlatform = True
                for iCoin in range(0,random.randint(0,3)):
                    aCoin = self.itemFactory.makeCoin(random.randint(aPlatform.hitbox[0], aPlatform.hitbox[0]+aPlatform.hitbox[2]), aPlatform.hitbox[1]-8) 
                    aPlatform.coins.append( aCoin )
                if random.random() < .06:
                    aJetpack = self.itemFactory.makeJetpack(random.randint(aPlatform.hitbox[0], aPlatform.hitbox[0]+aPlatform.hitbox[2]), aPlatform.hitbox[1]-20)
                    aPlatform.jetpacks.append( aJetpack )
                    game.greatLeaps += 1
            else:
                print( "trying again to find jumpable platform")     
        game.platforms.append(aPlatform)
        self.id += 1
        print( "%d non jumpable platforms allowed" % game.greatLeaps )


    def isPlatformJumpable(self, aPlatform, game, player):
        canJump = True
        topPlatform = game.platforms[len(game.platforms)-1]
        if aPlatform.hitbox[0] + aPlatform.hitbox[2] < topPlatform.hitbox[0] + topPlatform.hitbox[2] or aPlatform.hitbox[0] > topPlatform.hitbox[0]:
            dMin = player.jump_velocity * player.max_vel_x / game.gravity
            dMax = 2 * dMin
            distance1 = topPlatform.hitbox[0] - ( aPlatform.hitbox[0] + aPlatform.hitbox[2] )
            distance2 = aPlatform.hitbox[0] - (topPlatform.hitbox[0] + topPlatform.hitbox[2])
            distance = max( dMin, distance1, distance2)
            if (distance > dMax):
                canJump = False
                print( "Too far!" )
            maxHeight = player.jump_velocity * distance / player.max_vel_x - game.gravity / 2 * (distance / player.max_vel_x) ** 2
            if( aPlatform.hitbox[1] - topPlatform.hitbox[1] > maxHeight):
                canJump = False
                print( "Too high!")
        else:
            canJump = False 
        return( canJump )

     
    def suggestPlatform(self, game):

        width = random.randint(30, 3 * self.gameWidth / 5)
        x = random.randint( 1, self.gameWidth - width)
        max_y = max(self.minHeight+4,self.maxHeight)
        if game.greatLeaps > 0 and random.random() < .2:
            max_y = int(2*self.gameHeight/3)
            game.greatLeaps -= 1
        print( "minHeight and max_y",self.minHeight, max_y)
        y = - random.randint(self.minHeight, max_y)
        height = 10
        stickyColor = (112,227,73)
        slipperyColor = (151,212,245)
        mediumColor = (237, 132, 12)
        if random.random() < .2:
            color = slipperyColor
            friction = .3
        elif random.random() > .5:
            color = stickyColor
            friction = 5
        else:
            color = mediumColor 
            friction = 2
        aPlatform = Platform(x, y,width, height, color ,friction, self.id)
        print( "Leaps: %d, maxHeight: %d max_y: %d" % (game.greatLeaps, self.maxHeight, max_y) )
        return( aPlatform )