import cv2
import numpy as np
from Clahe import show_with_matplotlib

def imClearborder(img):
    # --- https://stackoverflow.com/questions/65534370/remove-the-element-attached-to-the-image-border
    # add 1 pixel white border all around
    pad = cv2.copyMakeBorder(img, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=255)
    h, w = pad.shape

    # create zeros mask 2 pixels larger in each dimension
    mask = np.zeros([h + 2, w + 2], np.uint8)

    # floodfill outer white border with black
    img_floodfill = cv2.floodFill(pad, mask, (0, 0), 0, (5), (0), flags=8)[1]

    # remove border
    img_floodfill = img_floodfill[1:h - 1, 1:w - 1]
    # cv2.imshow("floodFill", img_floodfill)
    # cv2.imshow("difference", img - img_floodfill)
    return img_floodfill

def contour(img_floodfill):
    ret, binary = cv2.threshold(img_floodfill, 40, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def drawRects(img_floodfill, rectangles):
    for b in rectangles:
        cv2.rectangle(img_floodfill, (b.x, b.y), (b.x + b.w, b.y + b.h), (155, 155, 0), 3)
        cv2.rectangle(img_floodfill, (b.x, b.y), (b.x + 3, b.y + 3), (255, 0, 0), 3)
    return img_floodfill

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class AABB:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.assigned = False
    def knows(self, id):
        if id in self.known:
            return True
        return False
    def overlaps(self, rect):
       l1 = Point(self.x, self.y)
       l2 = Point(rect.x, rect.y)
       r1 = Point(self.x + self.w, self.y + self.h)
       r2 = Point(rect.x + rect.w, rect.y + rect.h)

       if (abs((self.x + self.w / 2) - (rect.x + rect.w / 2)) * 2 < (self.w + rect.w)) and (abs((self.y + self.h / 2) - (rect.y + rect.h / 2)) * 2 < (self.h + rect.h)):
           return True

       return False


def redefineAABBs(contours, redefine=True):
    boxes = []
    #1. list the bouding boxes
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if w > 15 and h > 15:
            boxes.append(AABB(x, y, w, h)) #Add the bounding box to the array of valid ones

    intersections = redefine
    # Plusieurs passes - les rectangles ne peuvent s'intersecter qu'avec un à la fois
    # On itère jusqu'à ce que plus aucune intersection ne soit remarquée
    while intersections:
        new_boxes = []
        intersect_pass = False
        #Chaque boite verifie les autres
        for i in range(len(boxes)): # Complexité (pire cas) = O(n²/2)   - coef binomial: (n*(n+1)/2)
            a = boxes[i]
            # chercher une intersection avec j tant que la boite i n'est pas assignée
            for j in range(i, len(boxes)):
                if i == j: continue
                b = boxes[j]
                if b.assigned: continue
                if(a.overlaps(b)):
                    intersect_pass = True
                    #ajouter un rectangle inscrivant a,b
                    topleft = Point(min(a.x, b.x), min(a.y, b.y))
                    bottomright = Point(max(a.x+a.w, b.x+b.w), max(a.y+a.h, b.y+b.h))
                    w = bottomright.x - topleft.x
                    h = bottomright.y - topleft.y
                    a.assigned = True
                    b.assigned = True
                    new_boxes.append(AABB(topleft.x, topleft.y, w, h))
                    break
        # Ajout des boites qui n'ont jamais été assignée (sans intersections)
        for b in boxes:
            if not b.assigned:
                new_boxes.append(AABB(b.x, b.y, b.w, b.h))
        intersections = intersect_pass
        boxes = new_boxes.copy()
    return boxes

def dirtyPercentage(img, boxes):
    areaCount = 0
    imgArea=img.shape[0]*img.shape[1] #Calculate the are of the image
    for rect in boxes:
        areaCount += (rect.w * rect.h)
    #percentage of dirtyness calculated by the division of the squares area by the image area
    return round(areaCount/imgArea,3)*100