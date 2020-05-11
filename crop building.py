import cv2
import numpy as np

img = cv2.imread("skyline.jpg")
crop_img = img[108:136, 17:34]
#taken from https://www.youtube.com/watch?v=eLTLtUVuuy4
def regionOfInterest(image):
    polygons = np.array([[(210, 25), (195, 41), (195, 136), (200, 72), (211, 56)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    return mask

def newImage(image, mask):
    m = np.array(mask)
    n = np.array(image)
    for row in range(len(m)):
        for col in range(len(m[0])):
            if m[row][col]!= 0:
                n[row][col] = 255
    return n



#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
mask = regionOfInterest(img)
mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
new = newImage(img, mask)
#res = cv2.bitwise_and(img,img,mask = mask)


'''img[17:45,15:32] = crop_img'''
cv2.imshow("cropped", new)
cv2.waitKey(0)