from cmu_112_graphics import *
import tkinter as tk
import cv2
from uploadMode import *
from gameMode import *
from gameOverMode import *
from startScreen import *
from gallery import *

class myApp(ModalApp):
    url = '5.jpg'
    image = None
    def appStarted(self):
        self.win = False
        self.uploadMode = UploadMode()
        self.gameMode = GameMode()
        self.startScreen = StartScreen()
        self.galleryMode = Gallery()
        self.setActiveMode(self.startScreen)
        self.gameOverMode = GameOverMode()
        self.stars = 0
        self.score = 0

myApp(width = 600, height = 600)
