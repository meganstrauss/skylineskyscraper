import cv2
import numpy as np
import matplotlib.pyplot as plt
from cmu_112_graphics import *
import random

#len(image[0])= height
#len(image[1])= width
#len(image) = width

def lines(image): #returns all lines in an image
    #taken from https://www.youtube.com/watch?v=eLTLtUVuuy4
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    gradient = cv2.Canny(blur, 50, 150)
    return gradient
def findSkyline(image): #returns only the top lines in an image
    image = np.array(image)
    newImage = np.zeros_like(image)
    for y in range(len(image[0])):
        for x in range(len(image)):
            if image[x, y] != 0:
                newImage[x, y] = 255
                break
    return(newImage)



def verticalLines(image):
    #taken from https://opencv-python-tutroals.readthedocs.io/en/latest/py_tu
    # torials/py_imgproc/py_houghlines/py_houghlines.html
    #gray = cv2.imread(image)
    edges = cv2.Canny(image, 50, 150, apertureSize = 3)
    lines = cv2.HoughLines(edges,.1,np.pi,10)
    verticalLinesList = []
    for line in lines:
        rho=line[0][0]
        theta = line[0][1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 400*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 400*(a))
        x0 = (x1+x2)/2
        verticalLinesList.append(x0)
    verticalLinesList.sort()
    return verticalLinesList


def makePolygons(image, verticalLinesList):
    thresh = 50
    i = 0
    polygons = []
    y1 = 0
    y2 = image.shape[0]-1
    y3 = (y1+y2)/2
    starts = []
    while i<len(verticalLinesList):
        x1 = verticalLinesList[i]
        starts.append(x1)
        j = i+1
        while j<len(verticalLinesList):
            x2 = verticalLinesList[j]
            if abs(x2-x1)>thresh:
                break
            j+= 1
        polygon = [[x1, y1], [x1, y3], [x1, y2], [x2, y2], [x2, y3], [x2, y1]]
        polygons.append(polygon)
        i = j+1
        while i<len(verticalLinesList):
            if abs(x2-verticalLinesList[i])>thresh:
                break
            i += 1
    return (polygons, starts)

def createMask(image, points):
    #taken from https://www.youtube.com/watch?v=eLTLtUVuuy4
    polygons = np.array(points, np.int32)
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, [polygons], (255, 255, 255))
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    return mask
def shrinkBuilding(mask, image, scale):
    height = len(image)
    newSize = int(height*scale)
    x1 = None
    x2 = None
    for x in range(len(mask[1])):
        y = mask[0][0]
        if mask[y, x]==255:
            if x1==None:
                x1 = x
        if x1!= None and mask[y, x]!=255:
            x2 = x
            break
    if x2==None:
        x2 = len(mask[1])-1
    new = cv2.resize(image[0:height, x1:x2], (int(x2-x1), newSize))
    newImage = image.copy()
    for x in range(x1, x2):
        for y in range(len(newImage)):
            newImage[y, x]=(255, 255, 255)
    start = len(newImage)-len(new)
    for x in range(x1, x2):
        for y in range(start, start+len(new)):
            newImage[y, x]=new[y-start, x-x1]
    return newImage
def newImage(image, mask):
    m = np.array(mask)
    n = np.array(image)
    for row in range(len(m)):
        for col in range(len(m[0])):
            if m[row][col]!= 0:
                n[row][col] = 255
    return n
def skylineDict(a):#returns a dictionary of top y value for each x
    d = dict()
    for y in range(len(a[0])):
        for x in range(len(a)):
            if a[x, y] == 255:
                d[y] = x
    return d

def skylinePolygon(image):
    j = lines(image)
    skyline = findSkyline(j)
    d = skylineDict(skyline)
    for i in range(len(image[1])):
            if i not in d:
                if i==0:
                    d[i]=self.d[i+1]
                    continue
                d[i]=d[i-1]
    points = []
    h = len(image)
    for x in range(len(image[1])-1):
        points.append((x, d[x]))
    w = len(image[1])-1
    for x in range(w, 0, -1):
        points.append((x, h-1))
    #taken from https://github.com/udacity/CarND-LaneLines-P1/issues/35
    points = np.array([points], dtype=np.int32)
    return points



'''image = cv2.imread('5.jpg')
blank = np.zeros_like(image)
polygon = skylinePolygon(image)
print(polygon)
blank = cv2.fillPoly(blank, polygon, 255)
cv2.imshow('', blank)
cv2.waitKey(0)'''



def resize(a, height): #resizes an image given a height proportional to the width
    if type(a)==str:
        a = cv2.imread(a)
        a = np.array(a)
    if len(a.shape)==3:
        a = cv2.cvtColor(a, cv2.COLOR_BGR2RGB)
    #a = cv2.cvtColor(a, cv2.COLOR_BGR2RGB)
    ratio = len(a[0])/len(a)
    newY = height
    newX = ratio*height
    new = cv2.resize(a, (int(newX), int(newY)))
    return new

def getColors():
    colors = [(255, 153, 51),
(243, 170, 23),
(246, 193, 87)]
    
    
    '''[(255, 0, 0),
(233, 114, 114),
(255, 216, 216),
(255, 255, 255),
(255, 145, 0),
(255, 180, 80),
(250, 85, 255),
(239, 69, 245),
(69, 163, 145),
(242, 247, 77)]'''
    return colors


    '''colors = [(0, 0, 255),
    (1, 190, 200),
    (18, 255, 255)
                    ]
    return colors
(255, 255, 255),
(255, 145, 0),
(255, 180, 80),
(242, 247, 77)]'''
def fillBackground(skylineDict, image, colors):
    newImage = image.copy()
    for x in range(len(image[1])):
        for y in range(len(image)):
            newImage[y, x] = random.choice(colors)
    blur = cv2.GaussianBlur(newImage, (5, 5), 0)
    blur = cv2.GaussianBlur(blur, (5, 5), 0)
    for x in range(len(image[1])):
        for y in range(len(image)):
            if y<skylineDict[x]:
                image[y, x] = blur[y, x]
    
    return image

'''image = cv2.imread('skyline.jpg')
l = verticalLines('skyline.jpg') 
li = lines(image)
sky = findSkyline(li)
d = skylineDict(sky)
b = fillBackground(d, image, colors)
p = makePolygons(image, l)[4]
mask = createMask(b, p)
polygon = shrinkBuilding(mask, b, 0.5)
cv2.imshow('', b)

cv2.waitKey(0)'''



'''image = cv2.imread('skyline.jpg')
l = lines('skyline.jpg')
s = findSkyline(l)
d = skylineDict(s)
new = cropBuildings(d, image)
cv2.imshow('', new)
cv2.waitKey(0)'''







def isInLine(x, y, a): #returns if the player is standing on a line and the slope of that line
    for line in a:
        x1,y1,x2,y2 = np.reshape(line, 4)
        slope = (y1-y2)/(x2-x1)
        angle = np.arctan(slope)
        for i in range(x2-x1):
            newX, newY = x1+1, x1+slope*i
            if (x,y)==(newX, newY):
                return (True, angle)
    return (False, 0)
def findScreen(a, x1, x2): #crops the image to the width of the playing screen
    h = len(a)
    crop = a[0:h, x1:x2]
    return(crop)
def findTallBuildings(skylineDict):
    tallBuildings = []
    top = None
    bottom = 0
    for x in skylineDict:
        if skylineDict[x]>bottom:
            bottom = skylineDict[x]
        if top==None or skylineDict[x]<top:
            top = skylineDict[x]
    maxHeight = bottom - (bottom-top)/2
    x = -1
    while x<len(skylineDict)-2:
        x += 1
        if skylineDict[x]<maxHeight:
            building = detectBuilding(x, maxHeight, skylineDict)
            tallBuildings.append(building)
            x = building[1]
        x += 1
    return(tallBuildings)
def detectBuilding(x, maxHeight, skylineDict):
    x1 = x
    right = None
    left = None
    while x1>0:  
        if skylineDict[x1]<skylineDict[x]:
            slope = 1
            while slope==1:
                if skylineDict[x1]<skylineDict[x1-1]-10:
                    slope = 1
                elif skylineDict[x1]>skylineDict[x1-1]+10:
                    slope = -1
                    break
                x1-=1
            left= x1
            break
        for i in range(10):
            if x1-i<0:
                break
            if skylineDict[x1-i]!=skylineDict[x1]:
                break
            if i==9:
                left = x1
                break
        if left != None:
            break
        x1 += 1
    x2 = left
    y = skylineDict[left]
    thresh = 3*y/4
    while x2<len(skylineDict):
        if skylineDict[x2]>thresh:
            slope = None
            for x in range(x1, x2-1):
                if x+1>=len(skylineDict):
                    break
                if skylineDict[x]<skylineDict[x+1]-10:
                    slope = -1
                elif skylineDict[x]>skylineDict[x+1]+10:
                    slope = 1
                else:
                    continue
            if slope == -1:
                memory = None
                while slope==-1:
                    if x2+1>=len(skylineDict):
                        break
                    if skylineDict[x2]<skylineDict[x2+1]-10:
                        slope = -1
                    elif skylineDict[x2]>skylineDict[x2+1]+10:
                        slope = 1
                        break
                    x2 += 1
                right = x2
        if right != None:
            break
        x2+=1
    if left==None and right==None:
        return(1, 1)
    '''elif left==None:
        left = right
    elif right==None:
        right = left'''
    if right == None:
        right = len(skylineDict)-1
    return(left, right)
def findPoints(building, skylineDict):
    x1, x2 = building
    if skylineDict[x1]<=skylineDict[x2]:
        points = [(x1, skylineDict[x2])]
    else:    
        points = []
    for x in range(x1, x2-1):
        if skylineDict[x]!= skylineDict[x+1]:
            points.append((x, skylineDict[x]))
    if skylineDict[x1]>skylineDict[x2]:
        points.append((x2, skylineDict[x1]))
    return [points]


'''im = cv2.imread('skyline.jpg')
l = lines(im)
v = verticalLines(l)
pl = makePolygons(im, v)
print(pl)
            
image = cv2.imread('skyline.jpg')
polygon = skylinePolygon(image)
blank = np.zeros_like(image)
blank = cv2.fillPoly(blank, polygon, (0, 0, 255))
vl = verticalLines(blank)
p = makePolygons(image, vl)
print(p)

cv2.imshow('', blank)
cv2.waitKey(0) '''  
