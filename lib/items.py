import pygame

class ItemFactory(object):
    def __init__(self):
        self.coinImages = []
        self.coinRadius = 25
        for i in range(1,11):
            self.coinImages.append(pygame.transform.scale(pygame.image.load("images/items/coin/coin%02d.png" % i), (self.coinRadius, self.coinRadius)))
        self.jetpackWidth = 40
        self.jetpackHeight = 40
        self.jetpackImage = pygame.transform.scale(pygame.image.load("images/items/Jetpack.png") ,(self.jetpackWidth,self.jetpackHeight) )
    def makeCoin(self,x,y):
        aCoin = Coin(x,y)
        aCoin.coinImages = self.coinImages
        aCoin.radius = self.coinRadius
        return( aCoin )
    def makeJetpack(self,x,y):
        aJetpack = Jetpack(x,y)
        aJetpack.jetpackImage = self.jetpackImage
        aJetpack.width = self.jetpackWidth
        aJetpack.height = self.jetpackHeight
        return( aJetpack )





class Item(object):
    def __init__(self,x,y):
        self.touchpoint = [x,y]


class Jetpack(Item):
    def __init__(self,x,y):
        Item.__init__(self,x,y)
    def draw(self,win):
        win.blit( self.jetpackImage , (int(self.touchpoint[0]-self.width/2), int(self.touchpoint[1]-self.height/2)) )    

class Coin(Item):
    def __init__(self,x,y):
        Item.__init__(self,x,y)
        self.hitbox = [x-8, y-8, 16,16]
        self.framesPerImage = 3
        self.timeStep = 1
    def draw(self,win):
        self.timeStep += 1
        if self.timeStep == 10 * self.framesPerImage:
            self.timeStep = 0
        win.blit( self.coinImages[ self.timeStep // self.framesPerImage ] , (self.touchpoint[0]-self.radius, self.touchpoint[1]-self.radius) )    

        
       
