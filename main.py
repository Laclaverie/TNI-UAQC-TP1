import cv2

from interface import *
from imutils import *
from difference import *

# Devoir 1
# Nihal OUHAOUADA    |  OUHN11629909
# Pierre LACLAVERIE  |  LACP03119904
# Thibaud SIMON      |  SIMT15039901
# Yann REYNAUD       |  REYY07110005

# Dépendances
# Python >= 3.8
# OpenCV >= 4.0

def imshow(win_name, img, show):
    if show:
        cv2.imshow(win_name, img)

def process(path_ref,path_other, show_steps=False):
    im_out = cv2.imread(path_other) # image neutre

    # Etape 1 : Différence
    img = difference_filtered(path_ref,path_other)
    imshow("1. difference", img, show_steps)

    # Etape 2 : Threshold
    tr = thresholding(img)
    imshow("2. thresholding", tr, show_steps)

    # Etape 3: Erosion
    kernel = np.ones((5, 5), np.uint8)
    er = cv2.erode(tr, kernel, iterations=1)
    imshow("3. erosion", er, show_steps)
    dil = cv2.dilate(er, kernel, iterations=1)
    imshow("3 bis. dilatation", dil, show_steps)

    # Etape 4: Contours
    img = imClearborder(dil)
    c = contour(img)
    if show_steps:
        imshow("4. bounding boxes", drawRects(im_out.copy(), redefineAABBs(c, False)), show_steps)

    # Etape 5: filtrage des contours
    rects = redefineAABBs(c, True)

    # Dessin des contours sur l'image comparée
    im_out = drawRects(im_out, rects)
    imshow("5. fusion des bbox", im_out, show_steps)

    # Etape 6: déterminer degré de l'encombrement
    dirty_score = dirtyPercentage(img, rects)
    print("Dirty score = "+str(dirty_score))

    # convert to RGB to use it in PIL reprentation
    im_out = cv2.cvtColor(im_out, cv2.COLOR_BGR2RGB)
    return im_out, dirty_score

if __name__ == '__main__':
    main_window(process) # Passe le callback de la fonction process vers la gestion de l'UI
