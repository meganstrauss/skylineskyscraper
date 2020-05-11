import tkinter as tk
from cmu_112_graphics import *
import numpy as np
import cv2
from opencvfunctions import resize
from PIL import Image

class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.url = 'mario.png'
        #taken from https://www.trzcacak.rs/myfile/full/475-4755208_mario-fire-animation-mario-animation-sprite-sheet-png.png
        self.getArray()
        self.width = self.height = None
        self.isJumping = False
        self.jumpCount = 0
        self.spriteCounter = 0
        self.dy = 1
        self.dx = 4
        self.fallTime = 0
        self.isRunning = False
        self.isFalling = False
        self.runSpriteCounterForward = 0
        self.runSpriteCounterBackward = 0
        self.idleSprite = 0
        self.sprite = self.idleSprite
        self.jumpSpriteCounterForward = 0
        self.jumpSpriteCounterBackward = 0
        self.peak = None
        self.superJump = False
        self.jumpMax = 10
        self.superJumpCounter = 0
    def getArray(self):
        image = cv2.imread(self.url)
        image = np.asarray(image)
        self.array = image
    def getSprites(self, width, height):#crops the spritesheet
        w = self.width = width/16
        h = self.height = height/14
        sprites = []
        for col in range(14):
            for row in range(16):
                sprites.append((row*w, col*h, (row+1)*w, (col+1)*h))
        return sprites
    def turn(self, d):
        self.angle = d
    def currentSprite(self):
        if self.isJumping or self.isFalling:
            if self.dx>0:
                self.jumpSpriteCounterForward += 1
                if self.jumpSpriteCounterForward > 7:
                    self.jumpSpriteCounterForward = 7
                self.sprite = self.jumpSpriteCounterForward+160
                self.jumpSpriteCounterBackward = 0
            else:
                self.jumpSpriteCounterBackward += 1
                if self.jumpSpriteCounterBackward > 7:
                    self.jumpSpriteCounterBackward = 7
                self.sprite = self.jumpSpriteCounterBackward+176
                self.jumpSpriteCounterForward = 0
            self.runSpriteCounterForward = self.runSpriteCounterBackward = 0
        elif self.isRunning: 
            if self.dx >0:
                self.runSpriteCounterForward += 1
                self.runSpriteCounterForward %= 10
                self.sprite = self.runSpriteCounterForward+32 
                self.runSpriteCounterBackward = 0
            else:
                self.runSpriteCounterBackward += 1
                self.runSpriteCounterBackward %= 10
                self.sprite = self.runSpriteCounterBackward+48
                self.runSpriteCounterFoward = 0
            self.jumpSpriteCounterForward = self.jumpSpriteCounterBackward = 0
        else:
            self.sprite = self.idleSprite
            self.runSpriteCounterForward = self.runSpriteCounterBackward = 0
            self.jumpSpriteCounterForward = self.jumpSpriteCounterBackward = 0
        return self.sprite
    def run(self):
        self.isRunning = True
        self.x += int(self.dx)
        if self.dx < 7 and self.dx>-7:   
            self.dx*=1.15




























'''a = Player(0, 0)
image = resize(a.url, 300)
cv2.imshow('', image)
cv2.waitKey(0)'''

'''def appStarted(app):
    app.player = Player(300, 300)
    app.image = resize(app.player.url, 300)
    cv2.imshow('', app.image)
    app.sprites = Player.getSprites(app.image)
    app.pics = []
    for (x1, y1, x2, y2) in app.sprites:
        sprite = app.image[int(y1):int(y2), int(x1):int(x2)]
        app.pics.append(sprite)
def redrawAll(app, canvas):
    canvas.create_image(app.player.x, app.player.y, image=ImageTk.PhotoImage(image = Image.fromarray(app.image)))

runApp(width = 600, height = 600)'''

