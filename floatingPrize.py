import random
class FloatingPrize(object):
    def __init__(self, skylineDict):
        self.x = random.randint(10, len(skylineDict)-10)
        self.skylineDict = skylineDict
        self.y = self.skylineDict[self.x] - 20
        


class Coin(FloatingPrize):
    url = 'coin2.png'
    #taken from http://www.ruby2d.com/learn/sprites/
    def __init__(self, skylineDict):
        super().__init__(skylineDict)
        self.value = random.randint(0, 50)
        self.spriteCounter = 0
        self.dx=self.dy = 0
    @staticmethod
    def getSprites(w, h):
        Coin.width = width = w/6
        Coin.height = height = h
        sprites = []
        for i in range(6):
            sprites.append((i*width, 0, (i+1)*width, height))
        return sprites
        


        