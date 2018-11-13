import cv2
import numpy as np
def embed(filename,ifilename):
    img = cv2.imread(filename+".bmp",1)
    b, g, r = cv2.split(img)
    height,width = img.shape[:2]
    img2 = cv2.imread(ifilename,1)
    img2 = cv2.resize(img2,(height,width))
    b2, g2, r2 = cv2.split(img2)
    img_bgra = cv2.merge((b2,g2,r2,b))
    cv2.imwrite(filename+".png",img_bgra)

def main():
    filename = input("ファイル名を入力してください")
    embed(filename)

if __name__=='__main__':
    main()