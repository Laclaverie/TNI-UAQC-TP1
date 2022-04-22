import cv2
from matplotlib import pyplot as plt
import numpy as np


def denoise(img, convolution=0, kernelSize=5):
    blur = cv2.GaussianBlur(img, (kernelSize, kernelSize), convolution)
    return blur


def gradient_mag(img):
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # GrayScale color space

    # Gradient x is calculated:
    # the depth of the output is set to CV_16S to avoid overflow
    # CV_16S = one channel of 2-byte signed integers (16-bit signed integers)
    gradient_x = cv2.Sobel(gray_image, cv2.CV_16S, 1, 0, 3)

    # Gradient y is calculated:
    # the depth of the output is set to CV_16S to avoid overflow
    # CV_16S = one channel of 2-byte signed integers (16-bit signed integers)
    gradient_y = cv2.Sobel(gray_image, cv2.CV_16S, 0, 1, 3)

    # Conversion to an unsigned 8-bit type:
    abs_gradient_x = cv2.convertScaleAbs(gradient_x)
    abs_gradient_y = cv2.convertScaleAbs(gradient_y)

    # Combine the two images using the same weight:
    sobel_image = cv2.addWeighted(abs_gradient_x, 0.5, abs_gradient_y, 0.5, 0)
    return sobel_image


def nms(img):
    return


def weak_threshold(img):
    ret, img1 = cv2.threshold(img, 30, 150, cv2.THRESH_BINARY)
    return img1


def strong_threshold(img):
    ret, img1 = cv2.threshold(img, 20, 255, cv2.THRESH_BINARY)
    return img1


def double_threshold(img):
    return strong_threshold(img)


def canny(img_path, thresh=1):
    win_name = "canny"
    cv2.namedWindow(win_name, cv2.WINDOW_AUTOSIZE)

    # https://en.wikipedia.org/wiki/Canny_edge_detector
    img = cv2.imread(img_path)
    # Step 1. Denoise
    img = denoise(img)
    # Step 2. Gradient Magnitude
    # img = gradient_mag(img)
    # Step 3. Double threshold
    # img = double_threshold(img)
    img = cv2.Canny(img, thresh, 200)
    cv2.imshow(win_name, img)
    return img


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


def boundingRect(img_floodfill):
    # --- https://www.programcreek.com/python/example/89437/cv2.boundingRect
    ret, binary = cv2.threshold(img_floodfill, 40, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if w > 5 and h > 10:
            cv2.rectangle(img_floodfill, (x, y), (x + w, y + h), (155, 155, 0), 1)
    # cv2.imshow('boundingRec', img_floodfill)
    return img_floodfill


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    c = canny('Chambre/IMG_6567.jpg', 40)
    img = imClearborder(c)
    img = boundingRect(img)
    cv2.imshow("boundingRect", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
