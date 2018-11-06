import cv2
import numpy as np
def embed(filename):
    img = cv2.imread(filename)
    b,g,r = cv2.split(img)
    height,width = img.shape[:2]
    img2 = cv2.imread("lenna.bmp",0)
    img2 = cv2.resize(img2,(height,width))
    img_bgra = cv2.merge((b,g,r,img2))
    cv2.imwrite(filename,img_bgra)