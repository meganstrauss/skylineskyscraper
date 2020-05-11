import random
from cmu_112_graphics import *
from opencvfunctions import *

class StartScreen(Mode):
    def appStarted(self):
        #self.image = random.choice(self.app.images)
        self.backgroundUrl = self.app.url
        self.background = resize(self.backgroundUrl, self.height)
        self.buttonX = (int(self.width/3), int(2*self.width/3))
        self.buttonY = int(2*self.height/3)
        self.buttonR = int(self.width/5)
        #upload button is upload
        #play button is gallery
        self.uploadButton = (int(self.width/4)-self.buttonR, self.buttonY-self.buttonR, 
                int(self.width/4)+self.buttonR, self.buttonY+self.buttonR)
        self.playButton = (int(3*self.width/4)-self.buttonR,self.buttonY-self.buttonR, 
                            int(3*self.width/4)+self.buttonR,self.buttonY+self.buttonR)
        self.scrollX = 0
        self.backgroundSlice = findScreen(self.background, 0, self.width)
    def mousePressed(self, event):
        if (int(event.x) in range(self.uploadButton[0], self.uploadButton[2]) and
                int(event.y) in range(self.uploadButton[1], self.uploadButton[3])):
                self.app.setActiveMode(self.app.uploadMode)
        elif (int(event.x) in range(self.playButton[0], self.playButton[2]) and
                int(event.y) in range(self.playButton[1], self.playButton[3])):
                self.app.setActiveMode(self.app.galleryMode)
    def timerFired(self):
        self.scrollX += 1
        if self.scrollX>=len(self.background[1])-self.width:
            self.scrollX=0
        self.backgroundSlice = findScreen(self.background, 
        int(self.scrollX), int(self.scrollX+self.width))
    
    def redrawAll(self, canvas):
        canvas.create_image(self.width/2, self.height/2, image = 
        ImageTk.PhotoImage(image = Image.fromarray(self.backgroundSlice)))
        canvas.create_rectangle(self.width/4-self.buttonR, self.buttonY, 
        self.width/4+self.buttonR, self.buttonY+self.buttonR, fill = 'orange')
        canvas.create_text(self.width/4, self.buttonY+self.buttonR/2, text = 'Upload Image', fill = 'white', font = 'times 25 bold')
        canvas.create_rectangle(3*self.width/4-self.buttonR,self.buttonY, 
                            3*self.width/4+self.buttonR,self.buttonY+self.buttonR, fill = 'red')
        canvas.create_text(3*self.width/4, self.buttonY+self.buttonR/2, text = 'Choose From Gallery', fill = 'white', font = 'times 20 bold')
        canvas.create_text(self.width/2, self.app.height/3, text = 'Skyline Sidescroller', fill = 'white', font = 'times 50 bold')