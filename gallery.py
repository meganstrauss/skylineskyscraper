from cmu_112_graphics import *
import tkinter as tk
from opencvfunctions import *
from PIL import Image 
import numpy as np
import cv2
'''taken from
https://www.google.com/url?sa=i&source=images&cd=&ved=2ahUKEwjfuu6K-JfmAhVDj1kKHRlgBjEQjRx6BAgBEAQ&url=https%3A%2F%2Fnypost.com%2F2019%2F01%2F23%2Fthe-super-tall-towers-transforming-nycs-skyline%2F&psig=AOvVaw3EeGf524FVFW-fEmjesbYE&ust=1575409541323039
https://www.google.com/url?sa=i&source=images&cd=&cad=rja&uact=8&ved=2ahUKEwi2moam-JfmAhWi1VkKHQu5CLUQjRx6BAgBEAQ&url=%2Furl%3Fsa%3Di%26source%3Dimages%26cd%3D%26ved%3D2ahUKEwjfuu6K-JfmAhVDj1kKHRlgBjEQjRx6BAgBEAQ%26url%3Dhttps%253A%252F%252Fen.wikipedia.org%252Fwiki%252FList_of_tallest_buildings_in_Cleveland%26psig%3DAOvVaw3EeGf524FVFW-fEmjesbYE%26ust%3D1575409541323039&psig=AOvVaw3EeGf524FVFW-fEmjesbYE&ust=1575409541323039
https://image.shutterstock.com/image-photo/downtown-chicago-skyline-sunset-illinois-260nw-523596268.jpg
https://assets.simpleviewinc.com/simpleview/image/upload/c_fill,h_280,q_50,w_640/v1/clients/denver/Denver_Skyline_Sunset_Credit_Colorado_Josh_b04f3f94-326b-481b-949b-309e521ff383.jpg
https://cdn.theatlantic.com/assets/media/img/mt/2017/11/Salesforce_Tower_Skyline/lead_720_405.jpg?mod=1533691912
https://img.andrewprokos.com/LOWER-MANHATTAN-WORLD-TRADE-CENTER-VIEW-2129-COLOR-1100PX.jpg
https://www.mas.org/wp-content/uploads/2017/10/accidental-skyline-rendering-with-treeline-pano.jpg
https://www.skyscraper.org/skyline/slider/images/1999.jpg
https://image.shutterstock.com/image-photo/long-exposure-pittsburgh-downtown-skyline-260nw-522950143.jpg
http://realestate.dmagazine.com/wp-content/uploads/2016/03/PupleSkyline_MNS2616.jpg
https://i.redd.it/0ek9lzcoidfx.jpg'''

class Gallery(Mode):
    def appStarted(self):
        self.imageURLs = [['1.jpg', '5.jpg', '11.jpg'], ['7.jpg', '8.jpeg', '10.jpg']]
        self.images = []
        for row in self.imageURLs:
            newRow = []
            for url in row:
                newRow.append(self.sizeImage(url))
            self.images.append(newRow)
        self.image = None
        self.url = None
        self.buttonR = self.width/16
        self.squareX = self.width/8
        self.squareY = self.height/6
        self.xList = [self.width/4, self.width/2, 3*self.width/4]
        self.yList = [self.height/4, 5*self.height/8]
    def mousePressed(self, event):
        for col in range(3):
            for row in range(2):
                x, y = self.xList[col], self.yList[row]
                rx, ry = int(self.width/10), int(self.height/8)
                if event.x in range(int(x-rx), int(x+rx)) and event.y in range(int(y-ry), int(y+ry)):
                    self.image = self.images[row][col]
                    self.url = self.imageURLs[row][col]
        if (event.x in range(int(3*self.width/4-self.buttonR), int(3*self.width/4+self.buttonR)) and
            event.y in range(int(7*self.height/8), int(7*self.height/8+self.buttonR)) and self.url!=None):
            self.app.image = self.image
            self.app.url = self.url
            self.app.setActiveMode(self.app.gameMode)
        elif (event.x in range(int(self.width/4-self.buttonR), int(self.width/4+self.buttonR)) and
            event.y in range(int(7*self.height/8), int(7*self.height/8+self.buttonR))):
            self.app.setActiveMode(self.app.startScreen)

    def sizeImage(self, image):
        height, width = int(self.height/4), int(self.width/5)
        image = cv2.imread(image)
        shrink = resize(image, height)
        crop = shrink[0:height, 0:width]
        return crop
    def redrawAll(self, canvas):
        xList = self.xList
        yList = self.yList
        for x in range(3):
            row = xList[x]
            for y in range(2):
                col = yList[y]
                canvas.create_image(row, col, image=ImageTk.PhotoImage(image = Image.fromarray(self.images[y][x])))
        if self.url==None:
            color = 'gray'
        else:
            color = 'green'
        canvas.create_rectangle(3*self.width/4-self.buttonR, 7*self.height/8,
         3*self.width/4+self.buttonR, 7*self.height/8+self.buttonR,fill = color)
        canvas.create_text(3*self.width/4, 7*self.height/8+self.buttonR/2,
         text = 'Play', font = 'times 25 bold', fill = 'white')
        canvas.create_rectangle(self.width/4-self.buttonR, 7*self.height/8,
         self.width/4+self.buttonR, 7*self.height/8+self.buttonR,fill = 'red')
        canvas.create_text(self.width/4, 7*self.height/8+self.buttonR/2,
         text = 'Back', font = 'times 25 bold', fill = 'white')
        if self.url!=None:
            for row in range(2):
                for col in range(3):
                    if self.imageURLs[row][col]==self.url:
                        x, y = row, col
                        break
            x, y = self.xList[y], self.yList[x]            
            canvas.create_rectangle(x-self.squareX, y-self.squareY, x+self.squareX, y+self.squareY, outline = 'green')


      