from PIL import Image
import wave
import numpy
import sys
import struct
import array

FRAME_RATE = 44100

def make_wave_file(data, channel):
    w = wave.open("out.wav","w")
    w.setframerate(FRAME_RATE)
    w.setnchannels(channel)
    w.setsampwidth(2)
    w.writeframes(data)
    w.close()

def read_bmp(fname1,fname2):
    img1 = Image.open(fname1)
    img2 = Image.open(fname2)
    size = img1.size
    data = []
    img1_rgb = img1.convert("RGB")
    img2_rgb = img2.convert("RGB")
    for i in range(size[0]):
        for j in range(size[1]):
            r1,g1,b1 = img1_rgb.getpixel((i,j))
            r2,g2,b2 = img2_rgb.getpixel((i,j))
            if i==0 and j==0:
                if r1!=0:
                    img1_rgb, img2_rgb = img2_rgb, img1_rgb
            elif i==1 and j==0:
                channel = r1
            else:
                #data[i][j] = r1*256+r2-32768
                data.append(r1*256+r2-32768)
    return data,channel

def main():
    args = sys.argv
    # fname1 = input("ファイル名１を入力してください ")
    # fname2 = input("ファイル名２を入力してください ")
    if len(args)<3:
        print("コマンドライン引数として")
        print("ファイル名１ ファイル名２")
        print("を入力してください")
    else:
        fname1 = args[1]
        fname2 = args[2]
        tmp_data, channel = read_bmp(fname1, fname2)
        #data = array.array(tmp_data)
        make_wave_file(array.array('h',tmp_data), channel)

if __name__ == "__main__":
    main()