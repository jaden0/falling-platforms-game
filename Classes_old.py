import pygame
import random

def inBox( point, hitbox): # function returns true if point is in box
    if point[0] < hitbox[0] + hitbox[2] and \
       point[0] > hitbox[0] and \
       point[1] < hitbox[1] + hitbox[3] and \
       point[1] > hitbox[1]:
        return True
    else:
        return False

class platformFactory( object):
    def __init__(self, gameWidth, minHeight, maxHeight):
        self.gameWidth = gameWidth
        self.minHeight = minHeight
        self.maxHeight = maxHeight
    def makePlatform(self, topPlatform, hasJetpack, block):
        goodPlatform = False
        while( not goodPlatform ):
            aPlatform = self.suggestPlatform()
            if self.isPlatformJumpable( aPlatform, topPlatform, block) or hasJetpack:
                goodPlatform = True
            else: 
                print( "trying again")
        return( aPlatform )


    def suggestPlatform(self):
        width = random.randint(30, 3 * self.gameWidth / 5)
        x = random.randint( 1, self.gameWidth - width)
        y = - random.randint(self.minHeight, self.maxHeight)
        height = 10
        stickyColor = (112,227,73)
        slipperyColor = (151,212,245)
        mediumColor = (237, 132, 12)
        if random.random() < .2:
            color = slipperyColor
            friction = .1
        elif random.random() > .5:
            color = stickyColor
            friction = 3
        else:
            color = mediumColor 
            friction = 1
        aPlatform = platform(x,width, y,height, color ,friction)
        for iCoin in range(0,random.randint(0,3)):
            aCoin = coin(random.randint(x, x+width), y-8) 
            aPlatform.coins.append( aCoin)
        if random.random() < .08:
            aJetpack = Jetpack(random.randint(x, x+width), y-10, 50, 4)
            aPlatform.jetpacks.append( aJetpack )
        return( aPlatform )
    def isPlatformJumpable(self, aPlatform, topPlatform, block):
        canJump = True
        if aPlatform.x + aPlatform.width < topPlatform.x + topPlatform.width or aPlatform.x > topPlatform.x:
            dMin = block.jumpVelocity * block.maxVel_x / block.g
            dMax = 2 * dMin
            distance1 = topPlatform.x - ( aPlatform.x + aPlatform.width )
            distance2 = aPlatform.x - (topPlatform.x + topPlatform.width)
            distance = max( dMin, distance1, distance2)
            if (distance > dMax):
                canJump = False
                print( "Too far!" )
            maxHeight = block.jumpVelocity * distance / block.maxVel_x - block.g / 2 * (distance / block.maxVel_x) ** 2
            if( aPlatform.y - topPlatform.y > maxHeight):
                canJump = False
                print( "Too high!")
        else:
            canJump = False    
         
        return( canJump ) # TODO Write this function

class player(object):
    def __init__(self, x,y,width,height,g):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.score = 0
        self.vel_x = 0
        self.vel_y = 0
        self.jumpVelocity = 25
        self.g = g
        self.acceleration_x = .5
        self.maxVel_x = 5
        self.onPlatform = False
        self.friction = 1
        self.using_jetpack = False
        self.jetpacks = []
        self.hitbox = [x, y, width, height]
        self.fuel = 0
    def move(self,left,right,up, gameWidth):
        self.y += self.vel_y
        if self.x + self.vel_x >= 0 and self.x + self.width + self.vel_x <= gameWidth:
            self.x += self.vel_x
        else:
            if self.vel_x < 0:
                self.x = 0
            elif self.vel_x >0:
                self.x = gameWidth - self.width
            self.vel_x=0
        if left:
            self.vel_x -= self.acceleration_x * self.friction
            if self.vel_x <= -self.maxVel_x:
                self.vel_x = -self.maxVel_x
        elif right:
            self.vel_x += self.acceleration_x * self.friction
            if self.vel_x >= self.maxVel_x:
                self.vel_x = self.maxVel_x
        else:
            if self.vel_x < 0:
                self.vel_x = min(self.vel_x + self.friction * self.acceleration_x * .5, 0)
            if self.vel_x > 0:
                self.vel_x = max(self.vel_x - self.friction * self.acceleration_x * .5, 0)
        if up:
            if self.using_jetpack:
                self.fuel -= 1
                if self.fuel == 0:
                    self.using_jetpack = False
                self.vel_y -= self.strength
                if self.vel_y < -20 :
                    self.vel_y = -20
            else:
                self.vel_y = -self.jumpVelocity
        self.hitbox = [self.x, self.y, self.width, self.height]
        if not self.onPlatform:
            self.vel_y += self.g 


    def checkForPlatform(self,platform):
        # land on platform
        if self.height + self.y + self.vel_y > platform.y and \
                self.x + self.width >= platform.x and \
                self.x <= platform.x + platform.width and \
                self.y + self.height <= platform.y:
            self.vel_y = 0
            self.y = platform.y - self.height
            self.onPlatform = True
            self.friction = platform.friction
        # bump head
        if self.y >= platform.y + platform.height and \
                self.width + self.x >  platform.x and \
                platform.y + platform.height > self.y + self.vel_y and\
                self.x < platform.x + platform.width:
            self.vel_y = 0
            self.y = platform.y + platform.height
    def checkForJetpack(self, Jetpack):
        if inBox(Jetpack.touchPoint, self.hitbox):
            self.jetpacks.append( Jetpack )
            print( "adding jetpack")
            return( True )
        else:
            return( False )
    def checkForCoin( self, coin):
        if inBox( coin.touchPoint, self.hitbox):
            self.score += 1
            print( "coin")
            return( True )
        else: 
            return( False )
    def useJetpack(self):
        if len(self.jetpacks) > 0 and not self.using_jetpack:
            aJetpack = self.jetpacks.pop( 0 )
            self.fuel = aJetpack.fuel
            self.strength = aJetpack.strength
            self.using_jetpack = True
            self.friction = 1
            print( "Jetpack!!")
            print( "%d jetpacks left" % len(self.jetpacks))
    def drop(self, steps):
        self.y += steps
    def draw(self, win):
        pygame.draw.rect(win, (255,102,0), (self.x, self.y, self.width, self.height))

class platform(object):
    def __init__(self,x_a,x_b,y_a,y_b,color,friction=.5):
        self.x = x_a
        self.y = y_a
        self.width = x_b
        self.height = y_b
        self.color = color
        self.coins = []
        self.jetpacks = []
        self.friction=friction
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        for coin in self.coins:
            coin.draw( win )
        for jetpack in self.jetpacks:
            jetpack.draw( win )
    def drop( self , steps):
        self.y += steps
        for coin in self.coins:
            coin.drop( steps )
        for jetpack in self.jetpacks:
            jetpack.drop( steps )
 
            

class coin(object):
    def __init__(self, x,y):
        self.touchPoint = [x,y]
    def drop(self, steps):
        self.touchPoint[1] += steps
    def draw(self,win):
        pygame.draw.circle(win, (255,204,0), self.touchPoint, 6)

class Jetpack(object):
    def __init__(self,x,y,fuel,strength):
        self.fuel = fuel 
        self.strength = strength
        self.isUsed = False
        self.touchPoint = [x,y]
        self.width = 20
        self.height = 20
        self.x = self.touchPoint[0] - self.width / 2
        self.y = self.touchPoint[1] - self.height / 2
        self.color = (255,255,255)
    def drop(self, steps):
        self.touchPoint[1] += steps
    def draw(self,win):
        pygame.draw.circle(win, (50,20,255), self.touchPoint, int(self.width/2))
        pygame.draw.circle(win, self.color, self.touchPoint, 2)