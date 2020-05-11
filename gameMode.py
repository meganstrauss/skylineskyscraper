from player import Player
from parrot import Parrot
from opencvfunctions import *
from cmu_112_graphics import *
import tkinter as tk
from enemy import Enemy
from fox import Fox
from snail import Snail
import numpy as np
import cv2
import math
import random
from floatingPrize import FloatingPrize, Coin


class GameMode(Mode):
    def appStarted(self):
        self.colors = getColors()
        self.backgroundUrl = self.app.url
        self.background = self.resizeBackground(self.backgroundUrl)
        self.lines = self.getLines()
        self.skyline = findSkyline(self.lines)
        self.skylineDict = skylineDict(self.skyline)
        self.getBackground(self.background)
        self.backgroundWidth = len(self.background[0]) - 1
        self.backgroundSlice = findScreen(self.background, 0, self.width)
        self.parrots = []
        self.foxes = []
        self.foxSprites = self.getFoxSprites()
        self.flipFoxSprites = self.getFlipSprites(self.foxSprites)
        self.getFoxes()
        self.snails = [Snail(self.width, self.height, self.skylineDict, self.backgroundWidth)]
        #self.getSnails()
        self.parrotSprites = self.getParrotSprites()
        self.flipParrotSprites = self.getFlipSprites(self.parrotSprites)
        self.getParrots()
        self.player = Player(50, self.skylineDict[37])
        self.scrollX = self.scrollY = 0
        self.sprites = self.getPlayerSprites()
        self.gameOver = False
        self.score = 0
        self.lineArray = self.getLineArray()
        self.coinSprites = self.getCoinSprites()
        self.snailSprites = self.getSnailSprites()
        self.flipSnailSprites = self.getFlipSprites(self.snailSprites)
        self.coins = []
        self.getCoins()
        self.difficulty = self.getDifficulty()
        self.oldX, self.oldY = self.player.x, self.player.y
        self.time = 0
        self.g = 2
        self.getPolygons()
        self.building = None
        self.time = 0
        self.maxScore = self.getMaxScore()
        #self.getPlatformList()
    def getPolygons(self):
        image = cv2.imread(self.backgroundUrl)
        image = resize(image, self.height)
        blank = np.zeros_like(image)
        polygon = skylinePolygon(image)

        blank = cv2.fillPoly(blank, polygon, 255)
        buildings = verticalLines(blank)
        self.polygons, self.buildings = makePolygons(self.background, buildings)
    def getBackground(self, image):
        self.background = fillBackground(self.skylineDict, image, self.colors)
    def getSnails(self):
        x = int(self.backgroundWidth/self.width)
        n = random.randint(4*x, 6*x)
        for i in range(n):
            self.snails.append(Snail(self.width, self.height, self.skylineDict, self.backgroundWidth))
    def getFoxes(self):
        x = int(self.backgroundWidth/self.width)
        n = random.randint(2*x, 4*x)
        for i in range(n):
            self.foxes.append(Fox(self.width, self.height, self.skylineDict, self.backgroundWidth))                
    def getParrots(self):
        n = int(self.backgroundWidth/self.width) + 1
        for i in range(n):
            self.parrots.append(Parrot(self.width, self.height, self.backgroundWidth))
    def getCoins(self):
        n = len(self.skylineDict)//75
        for i in range (n):
            self.coins.append(Coin(self.skylineDict))
    def getDifficulty(self):
        values = []
        score = 0
        for key in self.skylineDict:
            values.append(self.skylineDict[key])
        top, bottom = min(values), max(values)
        dif = bottom-top
        for i in range(5, len(values)):
            if abs(values[i]-values[i-5])>dif/4:
                score += 1
        score += self.backgroundWidth//self.width
        return score
    def getSnailSprites(self):
        i = Image.open(Snail.url)
        i = i.resize((int(self.width/30), int(self.width/30)), Image.ANTIALIAS)
        sprites = Snail.getSprites(int(self.width/30), int(self.width/30))
        return(self.getSprites(i, sprites))
    def getCoinSprites(self):
        i = Image.open(Coin.url)
        i = i.resize((int(self.width/8), int(self.width/40)), Image.ANTIALIAS)
        sprites = Coin.getSprites(int(self.width/8), int(self.width/40))
        return(self.getSprites(i, sprites))
    def getPlayerSprites(self):
        i = Image.open(self.player.url)
        i = i.resize((int(self.width*3/2), int(self.height*3/2)), Image.ANTIALIAS)
        sprites = self.player.getSprites(int(self.width*3/2), int(self.height*3/2))
        return(self.getSprites(i, sprites))
    def getParrotSprites(self):
        i = Image.open(Parrot.url)
        i = i.resize((int(self.width/4), int(self.height/4)), Image.ANTIALIAS)
        parrotSprites = Parrot.getSprites(int(self.width/4), int(self.height/4))
        return(self.getSprites(i, parrotSprites))
    def getFoxSprites(self):
        i = Image.open(Fox.url)
        i = i.resize((int(self.width/2), int(self.height/2)), Image.ANTIALIAS)
        foxSprites = Fox.getSprites(int(self.width/2), int(self.height/2))
        return(self.getSprites(i, foxSprites))
    def getFlipSprites(self, L):
        #taken from https://www.daniweb.com/programming/software-development/threads/334566/tkinter-flipping-reversing-gif-images
        result = []
        for sprite in L:
            flip = sprite.transpose(Image.FLIP_LEFT_RIGHT)
            result.append(flip)
        return result
    '''def getPlatformList(self):
        l  = []
        i = 0
        while i<len(self.skylineDict)-1:
            j = i+1
            print(j)
            if j>=len(self.skylineDict)-2:
                j = len(self.skylineDict)-1
                l.append(i, j)
                break
            while j<len(self.skylineDict) and self.skylineDict[i]==self.skylineDict[j]:
                j+= 1
            l.append((i, j))
            i = j+1
        self.platforms = l'''
    def checkSkylineDict(self):
        for i in range(len(self.background[1])):
            if i not in self.skylineDict:
                if i==0:
                    self.skylineDict[i]=self.skylineDict[i+1]
                    continue
                self.skylineDict[i]=self.skylineDict[i-1]
        '''for i in range(len(self.background[1])):
            if i not in self.skylineDict2:
                if i==0:
                    self.skylineDict2[i]=self.skylineDict2[i+1]
                    continue
                self.skylineDict2[i]=self.skylineDict2[i-1]'''
    '''def checkSkylineDict2(self):
        i = 0
        while i<len(self.platforms):
            x1, x2 = self.platforms[i]
            if i==len(self.platforms)-1:
                break
            if abs(x2-x1)<self.player.width/4:
                for x in range(x1, x2):
                    self.skylineDict[x] = self.skylineDict[x2+1]
                x3, x4 = self.platforms[i+1]
                self.platforms[i+1] = (x1, x4)
                self.platforms.pop(i)
            else:
                i += 1'''
    def resizeBackground(self, image):
        image = resize(image, self.height)
        return image
    def getLineArray(self):
        img = np.zeros_like(self.skyline)
        #taken from https://www.youtube.com/watch?v=eLTLtUVuuy4
        lines = cv2.HoughLinesP(self.skyline, 45, math.pi/180, 100, minLineLength = self.player.width, maxLineGap = 100)
        return lines
    def getLines(self):
        i = cv2.imread(self.backgroundUrl)
        l = lines(i)
        l = resize(l, self.width)
        return l
    def getSprites(self, a, l):
        sprites = []
        for v in l:
            sprite = a.crop(v)
            sprites.append(sprite)
        return sprites  
    def getBackgroundSlice(self):
        self.backgroundSlice = findScreen(self.background, 
        int(self.scrollX), int(self.scrollX+self.width))
    def keyPressed(self, event):
        if event.key=='Up':
            if self.player.isFalling:
                return
            self.player.isJumping = True
        if event.key=='Right':
            self.player.isRunning = True
            if self.player.dx<0:
                self.player.dx *= -1
        if event.key=='Left':
            self.player.isRunning = True
            if self.player.dx>0:   
                self.player.dx *= -1
        if event.key=='Space':
            self.player.superJump = True
        if event.key=='Enter':
            self.snails = []
            for fox in self.foxes:
                fox.projectiles = []
            self.parrots = []
            self.foxes = []
        if event.key=='b':
            self.player.x = len(self.skylineDict)-100
            
    def keyReleased(self, event):
        if event.key=='Right':
            self.player.isRunning = False
            self.player.dx = 2
        if event.key=='Left':
            self.player.isRunning = False
            self.player.dx = 2
        if event.key=='Space':
            self.superJump()
        self.checkY()  
    def checkX(self):
        if self.player.x<=self.width/2:
            self.scrollX = 0
        elif self.player.x<self.backgroundWidth-self.width/2:
            self.scrollX = self.player.x-self.width/2
        else:
            self.scrollX = self.backgroundWidth-self.width
        if self.player.x+self.player.dx<0:
            return False
        if self.player.dx>0:
            if self.skylineDict[self.player.x+int(self.player.dx+1)]>=self.player.y-10:
                return True
            else: return False
        else:
            if self.skylineDict[self.player.x+int(self.player.dx-1)]>=self.player.y-10:
                return True
            else: return False
        '''elif isInLine(self.player.x, self.player.y, self.lineArray)[0]:
            return True'''
    def checkY(self):
        if self.player.isJumping:
            if self.player.jumpCount<self.player.jumpMax:
                self.player.y-=7
                self.player.jumpCount += 1
            else:
                self.player.jumpCount = 0
                self.player.jumpMax = 10
                self.player.isJumping = False
                self.player.isFalling = True
                self.player.peak = self.player.y
                self.player.fallTime = 0
        elif self.player.isFalling:
            self.player.fallTime += self.timerDelay
            self.player.y = self.player.peak + self.g*((self.player.fallTime/100)**2)
            self.player.jumpCount = 0
        elif self.player.y<self.skylineDict[self.player.x]:
            self.player.isFalling = True
            self.player.fallTime = 0
            self.player.peak = self.player.y
            self.player.jumpCount = 0
        if self.player.y>=self.skylineDict[self.player.x]:
            self.player.y= self.skylineDict[self.player.x]
            self.player.jumpCount = 0
            self.player.isFalling = False
    def superJump(self):
        self.player.jumpMax = self.player.superJumpCounter
        self.player.superJumpCounter = 0
        self.player.superJump = False
        self.player.isJumping = True
        self.player.jumpCount = 0
    def checkCollision(self, other):
        x, y, w, h = int(self.player.x), int(self.player.y)+8, int(self.player.width/4), int(self.player.height/2)
        x1, y1, w1 = int(other.x-other.dx), int(other.y-other.dy), int(other.width)
        if x1 in range(x-w, x+w) and y1 in range(y-int(self.player.height), y):
            return True
        else: return False
    def checkPlatform(self):
        x1, x2 = int(self.player.x-self.player.width/2), int(self.player.x+self.player.width/2)
        x = x1
        platformWidth = 0
        start = end = x1
        for i in range(x1, x2):
            if platformWidth == 0:
                start = i
            end = i
            platformWidth += 1
        if platformWidth>=self.player.width/2:
            return (start, end, True)
        else:
            return(start, end, False)
    def getMaxScore(self):
        maxScore = 0
        for coin in self.coins:
            maxScore += coin.value*self.difficulty
        maxScore += len(self.skylineDict)
        return maxScore
    def getStars(self):
        if self.score <self.maxScore//3:
            return 1
        elif self.score in range(self.maxScore//3, 2*self.maxScore//3):
            return 2
        else:
            return 3

    def getAngle(self, character):
        boo, angle = isInLine(character.x, character.y, self.lineArray)
        if boo==True:
            character.angle = angle
        else:
            if character.angle!=0:
                character.angle -= character.dangle
                if character.angle<0:
                    character.angle = 0
    def timerFired(self):
        if self.gameOver:
            self.app.score = self.score
            self.app.stars = self.getStars()
            self.app.setActiveMode(self.app.gameOverMode)
        if self.player.x + 2*self.player.dx >= self.backgroundWidth:
            self.gameOver = True
            self.app.win = True
            return
        self.time += self.timerDelay
        self.updateProjectiles()
        if self.isBlocked():
            if self.time%2000==0:
                self.checkForBuildings()
        if self.player.isRunning:
            if self.checkX():
                self.player.run()
        start, end, boo = self.checkPlatform()
        if boo==False:
            if self.skylineDict[self.player.x-1]>self.skylineDict[self.player.x]:
                if start<self.player.x:    
                    self.player.x -= 1
                elif start>self.player.x:
                    self.player.x += 1
        for parrot in self.parrots:
            if self.checkCollision(parrot):
                self.gameOver = True
        for coin in self.coins:
            if self.checkCollision(coin):
                self.score += coin.value*self.difficulty
                self.coins.remove(coin)
            coin.spriteCounter += 1
            coin.spriteCounter %= 6
        remove = []
        for fox in self.foxes:
            if self.checkCollision(fox):
                if self.oldY<fox.y:
                    remove.append(fox)
                else:
                    self.gameOver = True
            for projectile in fox.projectiles:
                if self.checkCollision(projectile):
                    self.gameOver = True
        for fox in remove:
            self.foxes.remove(fox)
        for snail in self.snails:
            if self.checkCollision(snail):
                self.gameOver = True
        '''if self.player.superJump:
            self.player.superJumpCounter += 1
            if self.player.superJumpCounter >40:
                self.player.superJumpCouter = 40'''
        if self.oldX<self.player.x:
            self.score += self.player.x-self.oldX
        self.oldX, self.oldY = self.player.x, self.player.y
        self.getBackgroundSlice()
        self.checkY()
        self.moveParrots()
        self.moveSnails()
        self.moveFoxes()
        self.shootProjectiles()
        self.updateCoins()
    def updateCoins(self):
        for coin in self.coins:
            coin.y = self.skylineDict[coin.x] -10
    def shootProjectiles(self):
        for fox in self.foxes:
            fox.time += self.timerDelay
            if abs(self.player.x-fox.x)>200 and abs(self.player.x-fox.x)<self.width:
                if fox.time%3000==0:
                    x = self.player.x-fox.x
                    y = -(self.player.y-fox.y)
                    if y==0:
                        y = 1
                    angle = math.atan(y/x)
                    fox.shoot(angle)
    def updateProjectiles(self):
        for fox in self.foxes:
            remove  =[]
            for projectile in fox.projectiles:
                if projectile.x+projectile.dx>=len(self.skylineDict) or projectile.x+projectile.dx<0:
                    remove.append(projectile)
                projectile.y += projectile.dy
                projectile.x -= projectile.dx
                projectile.time += self.timerDelay
                if projectile.x>len(self.skylineDict)-1 or projectile.x<0: 
                        remove.append(projectile)
            for projectile in remove:
                if projectile in fox.projectiles:
                    fox.projectiles.remove(projectile)
    def isBlocked(self):
        '''for i in range(10):
            print(i, self.skylineDict[int(self.player.x+self.player.dx*i)], int(self.player.y+self.player.dy*i))  
            if self.skylineDict[int(self.player.x+self.player.dx*i)]<int(self.player.y+self.player.dy*i):
                return True
            if self.skylineDict[int(self.player.x+self.player.dx*i)]<self.player.y:
                return False'''
        for i in range(self.player.x, len(self.skylineDict)):
            if self.skylineDict[i]<self.player.y-40:
                if abs(self.player.x-i)<30:
                    return True
    def checkForBuildings(self):
        y1 = 0
        y2 = len(self.skyline)
        y3 = (y1+y2)/2
        polygon = None
        for i in range(self.player.x, len(self.skylineDict)):
            if self.skylineDict[i]<self.player.y-40:
                x1, x2 = detectBuilding(i, self.player.y, self.skylineDict)
                polygon = [[x1, y1], [x1, y3], [x1, y2], [x2, y2], [x2, y3], [x2, y1]]
                break
        if polygon != None:
            for v in polygon:
                if None in v:
                    return
            self.shrink(polygon)
                
    def shrink(self, polygon):
        mask = createMask(self.background, polygon)
        copy = self.background.copy()
        copy = fillBackground(self.skylineDict, copy, [(255, 255, 255)])
        newSkyline = shrinkBuilding(mask, copy, 0.8)
        l = lines(newSkyline.copy())
        s = findSkyline(l)
        self.skylineDict = skylineDict(s)
        self.checkSkylineDict()
        self.getBackground(newSkyline)
        #self.getPlatformList()
        #self.checkSkylineDict2()
    def moveFoxes(self):
        for fox in self.foxes:
            newX = fox.x+fox.dx
            if (newX<0 or newX>self.backgroundWidth):
            #self.skylineDict[fox.x]>self.skylineDict[newX]
                fox.changeDirection()
            elif self.skylineDict[newX]<self.skylineDict[fox.x]-10:
                fox.changeDirection()
            fox.walk()
            fox.y = self.skylineDict[fox.x]
    def moveSnails(self):
        for snail in self.snails:
            if snail.isSmart:
                snail.follow(self.player.x)
            newX = snail.x+snail.dx
            if newX>self.backgroundWidth:
                newX = self.backgroundWidth
            if newX<0 or newX>=self.backgroundWidth:
                snail.changeDirection()
            if self.skylineDict[newX]>snail.y+Snail.width:
                snail.dy = 1
                if snail.dx!= 0:
                    snail.dxMemory= snail.dx
                snail.dx = 0
            elif self.skylineDict[newX]<snail.y-Snail.width:
                snail.dy = -1
                if snail.dx!= 0:
                    snail.dxMemory= snail.dx
                snail.dx = 0
            else:
                snail.dy = 0
                snail.dx = snail.dxMemory
                #snail.y = self.skylineDict[snail.x]
            snail.walk()
    def moveParrots(self):
        for parrot in self.parrots:
            if parrot.x+parrot.dx>=self.backgroundWidth or parrot.x+parrot.dx<0:
                parrot.changeDirection('x')
            if parrot.x + parrot.dx>parrot.range[1]  or parrot.x+parrot.dx<parrot.range[0]:
                parrot.changeDirection('x')
            if parrot.y+parrot.dy>self.skylineDict[parrot.x+parrot.dx]:
                parrot.changeDirection('y')
            if parrot.y+parrot.dy<0:
                parrot.changeDirection('y')
            parrot.fly()
    def redrawAll(self, canvas):
        n = self.player.currentSprite()
        sprite = self.sprites[n]
        #taken from https://stackoverflow.com/questions/53308708/how-to-display-an-image-from-a-numpy-array-in-tkinter
        canvas.create_image(self.width/2, self.height/2, image = 
        ImageTk.PhotoImage(image = Image.fromarray(self.backgroundSlice)))
        #taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
        canvas.create_image(self.player.x-self.scrollX, 
        self.player.y-self.scrollY+8, image=ImageTk.PhotoImage(sprite), anchor = 's')
        '''canvas.create_oval(self.player.x-10-self.scrollX, 
        self.player.y-self.scrollY-10, self.player.x+10-self.scrollX, 
        self.player.y-self.scrollY+10, fill = 'blue')'''
        for parrot in self.parrots:
            if parrot.dx>0:    
                sprite = self.parrotSprites[parrot.spriteCounter]
            else:
                sprite = self.flipParrotSprites[parrot.spriteCounter]
            canvas.create_image(parrot.x-self.scrollX, parrot.y, image = ImageTk.PhotoImage(sprite))
        for fox in self.foxes:
            if fox.dx<0:    
                sprite = self.foxSprites[fox.sprite].rotate(fox.angle)
            else:
                sprite = self.flipFoxSprites[fox.sprite+16].rotate(fox.angle)
            canvas.create_image(fox.x-self.scrollX-10, fox.y-10, image = ImageTk.PhotoImage(sprite))
            for p in fox.projectiles:
                canvas.create_oval(p.x-5, p.y-5, p.x+5, p.y+5, fill = 'cyan')
        for snail in self.snails:
            sprite = self.snailSprites[snail.spriteCounter]
            canvas.create_image(snail.x-self.scrollX, snail.y, image = ImageTk.PhotoImage(sprite))
        for coin in self.coins:
            sprite = self.coinSprites[coin.spriteCounter]
            canvas.create_image(coin.x-self.scrollX, coin.y, image = ImageTk.PhotoImage(sprite))
        canvas.create_text(self.width/2, self.height/12, text = f'Score: {self.score}', font = 'times 30 bold', fill = 'green')
        
GameMode(width = 600, height = 600)