from cmu_112_graphics import *
import tkinter as tk
from opencvfunctions import resize
from PIL import Image 
import numpy as np

class UploadMode(Mode):
    def appStarted(self):
        self.buttonX = (int(self.width/3), int(2*self.width/3))
        self.buttonY = int(2*self.height/3)
        self.buttonR = int(self.width/10)
        self.backButton = (int(self.width/4)-self.buttonR, self.buttonY, 
                int(self.width/4)+self.buttonR, self.buttonY+self.buttonR)
        self.uploadButton = (int(self.width/2)-self.buttonR, self.buttonY, 
                int(self.width/2)+self.buttonR, self.buttonY+self.buttonR)
        self.playButton = (int(3*self.width/4)-self.buttonR,self.buttonY, 
                            int(3*self.width/4)+self.buttonR,self.buttonY+self.buttonR)
        self.image = None
    def mousePressed(self, event):
        if (int(event.x) in range(self.uploadButton[0], self.uploadButton[2]) and
                int(event.y) in range(self.uploadButton[1], self.uploadButton[3])):
                self.app.url = self.url = self.getUserInput('Enter image URL')
                self.app.image = self.image = self.retrieveImage()
        elif (int(event.x) in range(self.backButton[0], self.uploadButton[2]) and
            int(event.y) in range(self.backButton[1], self.uploadButton[3])):
            self.app.setActiveMode(self.app.startScreen)
        elif (int(event.x) in range(self.playButton[0], self.playButton[2]) and
                int(event.y) in range(self.playButton[1], self.playButton[3]) and self.app.url!= None):
                self.app.setActiveMode(self.app.gameMode)
    def retrieveImage(self):
        try: 
            image = resize(self.url, self.height/6)
            self.play = True
        except: image = None
        return image
    def redrawAll(self, canvas):
        canvas.create_rectangle(self.width/4-self.buttonR, self.buttonY, 
        self.width/4+self.buttonR, self.buttonY+self.buttonR, fill = 'red')
        canvas.create_rectangle(self.width/2-self.buttonR, self.buttonY, self.width/2+self.buttonR, self.buttonY+self.buttonR,
        fill = 'orange')
        canvas.create_text(self.width/2, self.buttonY+self.buttonR/2, text = 'Upload', fill = 'white', font = 'times 25 bold')
        canvas.create_text(self.width/4, self.buttonY+self.buttonR/2, text = 'Back', fill = 'white', font = 'times 25 bold')
        #canvas.create_text(self.app.width/2, self.app.height/3, text = '', font = 'times 30 bold')
        try:
            canvas.create_image(self.width/2, self.height/2, 
            image=ImageTk.PhotoImage(image = Image.fromarray(self.app.image)))
            canvas.create_rectangle(3*self.width/4-self.buttonR,self.buttonY, 
                            3*self.width/4+self.buttonR,self.buttonY+self.buttonR, fill = 'green')
            canvas.create_text(3*self.width/4, self.buttonY+self.buttonR/2, text = 'Play', fill = 'white', font = 'times 30 bold')
        except:
            pass
