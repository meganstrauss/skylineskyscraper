import random
from opencvfunctions import resize
import cv2
import numpy as np
from cmu_112_graphics import *
class Parrot(object):
    url = 'parrot.png'
    #taken from https://www.trzcacak.rs/imgm/hJRwxhT_parrot-sprite-sheet-bird-transparency/
    def __init__(self, width, height, backgroundWidth):
        self.spriteCounter = 0
        self.flyCount = 0
        self.x = random.randint(0, backgroundWidth)
        self.y = 0
        self.radius = random.randint(0, width)
        self.range = (max(0, self.x-self.radius), min(self.x+self.radius, backgroundWidth))
        l = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]
        self.dy = random.choice(l)
        self.dx = random.choice(l)
        
    @staticmethod
    def getSprites(w, h):
        sprites = []
        w = int(w/3)
        h = int(h/3)
        Parrot.width = w
        Parrot.height = h
        for x in range(3):
            for y in range(3):
                sprites.append((x*w, y*h, (x+1)*w, (y+1)*h))
        return sprites
    def changeDirection(self, d):
        if d=='x':
            self.dx *= -1
        else:
            self.dy *= -1
    def fly(self):
        self.y += self.dy
        self.x += self.dx
        self.spriteCounter = (self.spriteCounter + 1) % 9























'''p = Parrot(300, 300)
def appStarted(app):
    app.player = p
    app.image = resize(app.player.url, 30)
    cv2.imshow('', app.image)
    app.sprites = Parrot.getSprites(app.image)
    app.pics = []
    for (x1, y1, x2, y2) in app.sprites:
        sprite = app.image[int(y1):int(y2), int(x1):int(x2)]
        app.pics.append(sprite)
def timerFired(app):
    app.player.spriteCounter += 1
    app.player.spriteCounter %= 9
    print(app.player.x, app.player.y)
def redrawAll(app, canvas):
    sprite = app.pics[app.player.spriteCounter]
    canvas.create_image(app.player.x, app.player.y, image=ImageTk.PhotoImage(image = Image.fromarray(sprite)))

runApp(width = 600, height = 600)'''



