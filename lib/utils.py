import pygame


class Game(object):
    def __init__(self):
        self.coinSound = pygame.mixer.Sound("sounds/coin.wav")
        self.jumpSound = pygame.mixer.Sound("sounds/jump.wav")
        self.landSound = pygame.mixer.Sound("sounds/land.wav")
        self.bumpSound = pygame.mixer.Sound("sounds/bump.wav")
        self.jetpackSound = pygame.mixer.Sound("sounds/jetpack.wav")
        self.width=500
        self.height=500
        self.gravity = 1
        self.left = False
        self.right = False
        self.up = False
        self.jet = False
        self.platforms = []
        self.dropFrames = 2
        self.dropFrame = 0
        self.dropSteps = 1
        self.jetpackForce=1.5
        self.jetpackFuel=100
        self.greatLeaps = 0
        self.win = pygame.display.set_mode((self.width, self.height),pygame.FULLSCREEN)
        self.gameOverFont = pygame.font.SysFont('comicsans', 30)
        self.gameFont = pygame.font.SysFont('comicsans', 20)
        self.lavaBackground = LavaBackground(self.width, self.height)
    def drop(self):
        self.dropFrame += 1
        if self.dropFrame == self.dropFrames:
            self.dropFrame = 0
        if self.dropFrame == 0:
            for platform in self.platforms:
                platform.hitbox[1] += self.dropSteps
                for coin in platform.coins:
                    coin.touchpoint[1] += self.dropSteps
                for jetpack in platform.jetpacks:
                    jetpack.touchpoint[1] += self.dropSteps
            
    def resetLoop(self):
        self.left = False
        self.right = False
        self.up = False
        self.jet = False
        for platform in self.platforms:
            if platform.hitbox[1] > self.height+100:
                self.platforms.pop( self.platforms.index(platform))

    def gameover(self,player):
        self.win.fill((0,0,0))
        text = self.gameOverFont.render("GAME OVER",1, (255,0,0))
        self.win.blit(text, (int(self.width/2 - text.get_width()/2),int(self.height/3)) )
        text = self.gameOverFont.render("Final Score: %d" % player.score ,1, (10,200,200))
        self.win.blit(text, (int(self.width/2 - text.get_width()/2),int(self.height/3 + 50)) )
        pygame.display.update()

    def redrawgamewindow(self,player):
        self.win.fill((0,0,0))
        self.lavaBackground.drawBackground( self.win)
        player.draw(self.win)
        for platform in self.platforms:
            platform.draw(self.win)
        text = self.gameFont.render("SCORE: %d" % player.score,1, (255,255,255))
        self.win.blit(text, ((self.width/2 - text.get_width()/2),10))
        text = self.gameFont.render("LIFE: %d" % player.life,1, (255,255,255))
        self.win.blit(text, ((self.width/2 - text.get_width()/2 - 150),10))
        text = self.gameFont.render("JETPACKS: %d" % player.jetpacks,1, (255,255,255))
        self.win.blit(text, ((self.width/2 - text.get_width()/2 + 150),10))
        self.lavaBackground.drawFloor( self.win)
        pygame.display.update() 
# a lands on b
def land( a, b): 
    if a.hitbox[3] + a.hitbox[1] + a.vel_y >= b.hitbox[1] and \
                a.hitbox[1] + a.hitbox[3] <= b.hitbox[1] and \
                verticleTouch( a, b):
        return( True )
    else:
        return( False )

# a bumps head on b
def bump( a, b):
    if a.hitbox[1] + a.vel_y <= b.hitbox[1] + b.hitbox[3] and \
                a.hitbox[1] >= b.hitbox[1] + b.hitbox[3] and \
                verticleTouch(a, b):
        return( True )
    else:
        return( False )

# a and b alinged virtically
def verticleTouch(a,b):
    if a.hitbox[0] + a.hitbox[2] >= b.hitbox[0] and \
            a.hitbox[0] <= b.hitbox[0] + b.hitbox[2]:
        return( True )
    else:
        return( False )

def inBox( point, hitbox): # function returns true if point is in box
    if point[0] < hitbox[0] + hitbox[2] and \
       point[0] > hitbox[0] and \
       point[1] < hitbox[1] + hitbox[3] and \
       point[1] > hitbox[1]:
        return( True ) 
    else:
        return( False )


class LavaBackground(object):
    def __init__(self, gameWidth, gameHeight):
        self.gameHeight = gameHeight
        self.dropPixels = 0
        self.dropPerFrame = 2
        self.imageNumber = 0
        self.frame = 0
        self.framesPerImage = 10
        self.tilesPerWidth = 10
        self.tileSize = gameWidth // self.tilesPerWidth
        self.numberVerticalTiles = self.gameHeight // self.tileSize + 1
        self.lavaImages = []
        self.lavaImages.append(pygame.transform.scale(pygame.image.load("images/tiles/lava/lava_tile1.png"), (self.tileSize,self.tileSize) ))
        self.lavaImages.append(pygame.transform.scale(pygame.image.load("images/tiles/lava/lava_tile2.png"), (self.tileSize, self.tileSize) ))
        self.bottomlavaImages = []
        self.bottomlavaImages.append(pygame.transform.scale(pygame.image.load("images/tiles/lava/lava_tile3.png"), (self.tileSize,self.tileSize) ))
        self.bottomlavaImages.append(pygame.transform.scale(pygame.image.load("images/tiles/lava/lava_tile4.png"), (self.tileSize, self.tileSize) ))
    def drawBackground(self,win):
        self.frame += 1
        if self.frame == self.framesPerImage:
            self.frame = 0
            self.imageNumber = (self.imageNumber + 1) % 2
        self.dropPixels += self.dropPerFrame
        if self.dropPixels >= self.tileSize:
            self.dropPixels = 0    

        for j in range( 0, self.numberVerticalTiles):
            y = j * self.tileSize
            for i in range( 0, self.tilesPerWidth):
                x = i * self.tileSize
                win.blit( self.lavaImages[self.imageNumber], (x,y+self.dropPixels - self.tileSize))
    def drawFloor(self,win):
        y = self.gameHeight - self.tileSize
        for i in range( 0, self.tilesPerWidth):
            x = i * self.tileSize
            win.blit( self.bottomlavaImages[self.imageNumber], (x,y))
