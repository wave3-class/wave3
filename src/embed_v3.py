import cv2
import numpy as np
def embed(filename,ifilename):
    img = cv2.imread(filename+".bmp",1)
    b, g, r = cv2.split(img)
    b0 = b.copy() // 16
    b1 = b.copy() % 16
    height,width = img.shape[:2]
    img2 = cv2.imread(ifilename,1)
    img2 = cv2.resize(img2,(height,width))
    b2, g2, r2 = cv2.split(img2)
    b2 = (b2 // 16) * 16 + b0
    g2 = (g2 // 16) * 16 + b1
    r2 = (r2 // 16) * 16 + b0
    img_bgra = cv2.merge((b2,g2,r2))
    cv2.imwrite(filename+".png",img_bgra)

def main():
    filename = input("ファイル名を入力してください")
    ifilename = input("ファイル名を入力してください")
    embed(filename,ifilename)

if __name__=='__main__':
    main()