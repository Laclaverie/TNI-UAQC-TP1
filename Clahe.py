import numpy as np
import cv2
import matplotlib.pyplot as plt


def clahe_processing(path, limit=3, grid=(7, 7), gray=False):
    image=cv2.imread(path)
    if (len(image.shape) == 2):
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        gray = True

    clahe = cv2.createCLAHE(clipLimit=limit, tileGridSize=grid)
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))

    image = cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)
    if gray:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return np.uint8(image)

def clahe_processing2(path, clipl=2.0):
    # create a CLAHE object (Arguments are optional).
    clahe = cv2.createCLAHE(clipLimit=clipl, tileGridSize=(8, 8))
    # img = cv2.imread(path,0)  # conversion en niveau de gris : plus mtn
    img = cv2.imread(path)
    lab = img
    cv2.cvtColor(lab, cv2.COLOR_BGR2Lab)
    L,A,B = cv2.split(lab)

    cl1 = clahe.apply(L)
    lab=cv2.merge((cl1,A,B))
    lab2color=cv2.cvtColor(lab,cv2.COLOR_LAB2BGR)
    return np.uint8(lab2color)


#  : L*a*b* -> egalisation de L et refusion

def show_with_matplotlib(img, title="matplolib"):
    """Shows an image using matplotlib capabilities"""

    # Convert BGR image to RGB:
    img_RGB = img[:, :, ::-1]

    # Show the image using matplotlib:
    plt.figure()
    plt.imshow(img_RGB)
    plt.title(title)
    plt.show()
    cv2.waitKey()


def show_with_cv(img, title="CVCV"):
    plt.figure()
    cv2.imshow(title, img)


class ImgProc:
    def __init__(self, name):
        self.name = name

    def printImage(self, path):
        img = cv2.imread(path)
        # cv2.imshow(self.name, img)
        show_with_matplotlib(img)
