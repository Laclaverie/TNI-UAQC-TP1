import numpy as np

import  cv2

def difference_filtered(ref_path, im_path):
    imRef = cv2.imread(ref_path)
    imRef = histEqualizing(imRef) # egalise luminance
    imRef = cv2.cvtColor(imRef, cv2.COLOR_BGR2GRAY)
    blurredRef = cv2.GaussianBlur(imRef, (7, 7), 0)

    imNew = cv2.imread(im_path)
    imNew = histEqualizing(imNew) # egalise luminance
    imNew = cv2.cvtColor(imNew, cv2.COLOR_BGR2GRAY)
    blurredNew = cv2.GaussianBlur(imNew , (7, 7), 0)

    #Soustraction
    grayDiff = cv2.absdiff(blurredRef, blurredNew)

    #Debruitage
    return cv2.bilateralFilter(grayDiff, 15, 32, 64)

def hist_color_img(img):
    """ 3-channel image"""
    histr = []
    histr.append(cv2.calcHist([img], [0], None, [256], [0, 256]))
    histr.append(cv2.calcHist([img], [1], None, [256], [0, 256]))
    histr.append(cv2.calcHist([img], [2], None, [256], [0, 256]))
    return histr

def histEqualizing(im) :
    L, A, B = cv2.split(cv2.cvtColor(im, cv2.COLOR_BGR2Lab))
    eq_L = cv2.equalizeHist(L)
    eq_image = cv2.cvtColor(cv2.merge([eq_L, A, B]), cv2.COLOR_LAB2BGR)
    return eq_image


def thresholding(im):
    #Elimination des points faibles (suppression si < 40)
    ret, pre_pass = cv2.threshold(im, 30, 255, cv2.THRESH_TOZERO)

    # Threshold Adaptatif
    thresh = cv2.adaptiveThreshold(pre_pass, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 19, -2)

    return thresh

if __name__ == '__main__':
    # Etape 1 : Différence
    im = difference_filtered("Images_1200/Chambre/Reference.jpg", "Images_1200/Chambre/IMG_6568.jpg")
    # Etape 2 : Threshold
    im = thresholding(im)
    cv2.imshow("resultat", im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
