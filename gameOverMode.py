from cmu_112_graphics import *
import tkinter as tk
from opencvfunctions import findScreen, resize
import cv2
class GameOverMode(Mode):
    def appStarted(self):
        self.backgroundUrl = self.app.url
        self.background = resize(self.backgroundUrl, self.height)
        self.buttonX = (int(self.width/3), int(2*self.width/3))
        self.buttonY = (int(4*self.height/6), int(5*self.height/6))
        self.scrollX = 0
        self.backgroundSlice = findScreen(self.background, 0, self.width)
        self.starImage = self.loadImage('star3.png')
        self.starImage = self.scaleImage(self.starImage, 1/16)
        #taken from http://www.matim-dev.com/uploads/1/5/8/0/15804842/3163379_orig.png
    '''def getStarSprites(self):
        url = 'star3.png'
        #taken from http://www.matim-dev.com/uploads/1/5/8/0/15804842/3163379_orig.png
        image = cv2.imread(url)
        image = resize(image, self.height/8)
        newWidth, newHeight = len(image[1]), self.height/8
        image = Image.fromarray(image)
        sprites = []
        sprites.append(image.crop((0, 0, newWidth/2, newHeight)))
        sprites.append(image.crop((newWidth/2, 0, newWidth, newHeight)))
        return sprites'''

    def mousePressed(self, event):
        if (event.x in range(self.buttonX[0], self.buttonX[1]) 
            and event.y in range(self.buttonY[0], self.buttonY[1])):
            self.app.appStarted()
    def timerFired(self):
        self.scrollX+=1
        if self.scrollX>=len(self.background[1])-self.width:
            self.scrollX=0
        self.backgroundSlice = findScreen(self.background, 
        int(self.scrollX), int(self.scrollX+self.width))
    def redrawAll(self, canvas):
        canvas.create_image(self.width/2, self.height/2, image = 
        ImageTk.PhotoImage(image = Image.fromarray(self.backgroundSlice)))
        canvas.create_rectangle(self.buttonX[0], self.buttonY[0], 
        self.buttonX[1], self.buttonY[1], fill = 'orange')
        cx, cy = self.width/2, sum(self.buttonY)/2
        canvas.create_text(cx, cy, text = 'Play Again', fill = 'blue', font = 'times 25 bold')
        canvas.create_text(cx, self.app.height/3, text = 'GAME OVER', fill = 'white', font = 'times 50 bold')
        if self.app.win:
            canvas.create_text(cx, self.height/2, text = 'YOU WIN', fill = 'white', font = 'times 30 bold')
        else:
            canvas.create_text(cx, self.height/2, text = 'YOU LOSE', fill = 'white', font = 'times 30 bold')
        starDistance = self.width/6
        height = self.height/6
        if self.app.stars==1:
            canvas.create_image(cx-starDistance, height, image= ImageTk.PhotoImage(self.starImage))
        elif self.app.stars==2:
            canvas.create_image(cx, height, image= ImageTk.PhotoImage(self.starImage))
            canvas.create_image(cx-starDistance, height, image= ImageTk.PhotoImage(self.starImage))
        else:
            canvas.create_image(cx, height, image= ImageTk.PhotoImage(self.starImage))
            canvas.create_image(cx-starDistance, height, image= ImageTk.PhotoImage(self.starImage))
            canvas.create_image(cx+starDistance, height, image= ImageTk.PhotoImage(self.starImage))

            
    
