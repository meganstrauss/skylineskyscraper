import random
class Enemy(object):
    def __init__(self, width, height, skylineDict, backgroundWidth):
        self.backgroundWidth = backgroundWidth
        self.skylineDict = skylineDict
        self.width = width
        self.x = self.getX()
        self.y = skylineDict[self.x]
        self.dx = random.choice([-2, -1, 1, 2])
        self.dy = 0
        self.dxMemory = self.dx
        self.sprites = []
        self.spriteCounter = 0
        self.isSmart = True#random.choice([True, False])
        self.angle = 0
        self.spriteNumber = 1
        self.target = None
    def getX(self):
        x = random.randint(self.width/2, self.backgroundWidth-1)
        return x
        '''Fox.foxPlaces.append(x)
        for v in Fox.foxPlaces:
            if abs(x-v)<100:
                Fox.foxPlaces.remove(x)
                break
        if x not in Fox.foxPlaces:
            self.getX()'''
    
    def changeDirection(self):
        self.dx *= -1
        self.dxMemory = self.dx
    def walk(self):
        self.x += self.dx
        self.y += self.dy
        
        '''if self.dy != 0:
            self.y += self.dy
        else:
            self.x += self.dx
            self.y = self.skylineDict[self.x]'''
        self.spriteCounter += 1
        self.spriteCounter %= self.spriteNumber
    def follow(self, x):
        direction = self.x-x
        if direction<0:
            self.dx = 1
        elif direction >0:
            self.dx = -1
    def followOrNot(self):
        choice = random.choice([True, False])
        return choice
    def turn(self, angle):
        self.angle += angle
