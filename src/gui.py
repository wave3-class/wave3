import os
import tkinter
import tkinter.filedialog
import tkinter.messagebox 
from tkinter import *
from PIL import Image,ImageTk
import wave
from scipy import fromstring, int16
import math

global FILENAMW
IMG1="a.bmp"
IMG2="b.bmp"
FRAME_RATE = 44100
input_name = "input.wav"
output_name = "output.tmp"


def print_info(sound):
    print("チャンネル数:", sound.getnchannels())
    print("サンプル幅:", sound.getsampwidth())
    print("サンプリング周波数:", sound.getframerate())
    print("フレーム数:", sound.getnframes())
    print("パラメータ:", sound.getparams())
    print("長さ（秒）:", float(sound.getnframes()) / sound.getframerate())


def get_data(sound):
    buffer = sound.readframes(sound.getnframes())
    buffer = fromstring(buffer, dtype=int16)
    data_a = []
    data_b = []
    channels = sound.getnchannels()
    print(len(buffer))
    for i in buffer:
        tmp = 32768+i
        data_a.append(tmp // 256)
        data_b.append(tmp % 256)
    data = [data_a, data_b, channels]
    return data


def make_cip(data):
    size = []
    size.append(int(math.sqrt(len(data[0])))+1)
    size.append(size[0])
    print(size)
    new_a = Image.new("RGB", size)
    new_b = Image.new("RGB", size)
    i = 0
    for x in range(0, size[0]):
        for y in range(size[1]):
            if x == 0 and y == 0:
                new_a.putpixel((x, y), (0, 0, 0))
                new_b.putpixel((x, y), (255, 255, 255))
            elif x == 1 and y == 0:
                new_a.putpixel((x, y), (data[2], data[2], data[2]))
                new_b.putpixel((x, y), (data[2], data[2], data[2]))
            elif i < len(data[0]):
                a = data[0][i]
                b = data[1][i]
                new_a.putpixel((x, y), (a, a, a))
                new_b.putpixel((x, y), (b, b, b))
            i += 1
    new_a.save(IMG1)
    new_b.save(IMG2)
    return 0

def dialog():
    fTyp = [("","*.wav")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    tkinter.messagebox.showinfo("wave","入力ファイルを選択してください！")
    filename = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
    #filename=(os.path.basename(filename))
    return filename   #フルパス

def voice_exchange(self):
    FILENAME = dialog()
    #変換して2つのファイルを保存
    w=wave.open(FILENAME)
    print_info(w)
    make_cip(get_data(w))

def show_img1(self):
    img = Image.open(IMG1)
    img.show()

def show_img2(self):
    img = Image.open(IMG2)
    img.show()

def mk_button1():
    button = tkinter.Button(text=u"変換",width=15,bg="blue")
    button.bind("<Button-1>",voice_exchange)
    button.place(x=50,y=250)

def mk_button2():
    button = tkinter.Button(text=u"画像1を表示",width=15,bg="green")
    button.bind("<Button-1>",show_img1)
    button.place(x=150,y=150)

def mk_button3():
    button = tkinter.Button(text=u"画像2を表示",width=15,bg="green")
    button.bind("<Button-1>",show_img2)
    button.place(x=150,y=350)

if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("title")
    root.geometry("500x500")
    mk_button1()
    mk_button2()
    mk_button3()
    root.mainloop()