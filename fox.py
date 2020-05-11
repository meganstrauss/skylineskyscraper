from enemy import Enemy
import math, random
class Fox(Enemy):
    url = 'goomba.png'
    #taken from https://forum.processing.org/two/uploads/imageupload/316/A2C38EFGUD5M.png
    def __init__(self, width, height, skylineDict, backgroundWidth):
        super().__init__(width, height, skylineDict, backgroundWidth)
        self.spriteNumber = 8
        self.sprite = 16
        self.projectiles = []
        self.time = 0
    @staticmethod
    def getSprites(w, h):
        sprites = []
        w = int(w/8)
        h = int(h/8)
        Fox.width = w
        Fox.height = h
        for row in range(8):
            for col in range(8):
                sprites.append((row*w, col*h, (row+1)*w, (col+1)*h))
        return sprites
    def shoot(self, angle):
        self.projectiles.append(Projectile(self.x, self.y, angle))
    def choose(self):
        choices = [True] + [False]*20
        return(random.choice(choices))
    def walk(self):
        self.x += self.dx
        self.spriteCounter += 1
        self.spriteCounter %=8
        self.sprite = self.spriteCounter + 16


class Projectile(object):
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.dh = 5
        self.dy = self.dh*math.sin(self.angle)
        self.dx = self.dh*math.cos(self.angle)
        self.time = 0
        self.startY = self.y
        self.radius = 5
        self.width = self.height = 10
    def collide(self):
        self.x = -self.x*0.8
    