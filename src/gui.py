import os
import tkinter
import tkinter.filedialog
import tkinter.messagebox 
from tkinter import *
from PIL import Image,ImageTk
import wave
from scipy import fromstring, int16
import math
import numpy
import array

IMG1="a.bmp"
IMG2="b.bmp"
FRAME_RATE = 44100
input_name = "input.wav"
output_name = "output.tmp"
img1 = NONE          #PhotoImgaeはガーベジコレクションとして削除されるため、グローバル変数に設定
img2 = NONE
info = NONE 


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
        a1 = tmp // 256
        a2 = a1
        a1 = a1 // 16
        a2 = a2 % 16
        b1 = tmp % 256
        b2 = b1
        b1 = b1 // 16
        b2 = b2 % 16
        data_a.append(a1+b1*16)
        data_b.append(a2+b2*16)
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
    new_a.save("a.bmp")
    new_b.save("b.bmp")
    return 0

def make_wave_file(data, channel):
    w = wave.open("out.wav","w")                                    #waveファイルを開く
    w.setframerate(FRAME_RATE)                                      #フレームレートの設定
    w.setnchannels(channel)                                         #チャンネル数の設定（1:モノラル 2:ステレオ)
    w.setsampwidth(2)                                               #サイズの設定(1:8bit 2:16bit 3:24bit)
    w.writeframes(data)                                             #データの書き込み
    w.close()                                                       #waveファイルを閉じる

def read_bmp(fname1,fname2):
    img1 = Image.open(IMG1)                                       #画像ファイルを開く(1)
    img2 = Image.open(IMG2)                                       #画像ファイルを開く(2)
    size = img1.size                                                #画像のサイズの取得
    data = []
    img1_rgb = img1.convert("RGB")                                  #画像をRGBへ変換(1)
    img2_rgb = img2.convert("RGB")                                  #画像をRGBへ変換(2)
    for i in range(size[0]):
        for j in range(size[1]):
            r1,g1,b1 = img1_rgb.getpixel((i,j))                     #RGB情報の取得(1)
            r2,g2,b2 = img2_rgb.getpixel((i,j))                     #RGB情報の取得(2)
            a1 = r1%16
            a2 = r2%16
            b1 = r1//16
            b2 = r2//16
            r1 = a1*16+a2
            r2 = b1*16+b2
            if i==0 and j==0:
                # if r1!=0:
                #     img1_rgb, img2_rgb = img2_rgb, img1_rgb         #上下の交換
                continue
            # elif i==1 and j==0:
            #     channel = r1                                        #チャンネルの設定
            else:
                #data[i][j] = r1*256+r2-32768
                data.append(r1*256+r2-32768)                        #データの追加
    return data

def dialog():                                                          #ダイアログ作成
    fTyp = [("","*.wav")]                                               #拡張子限定
    iDir = os.path.abspath(os.path.dirname(__file__))                    #ディレクリ変数
    tkinter.messagebox.showinfo("wave","入力ファイルを選択してください！")
    filename = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
    #filename=(os.path.basename(filename))                    #ファイル名
    return filename                                           #フルパスを戻り値

def encode(self):                                             #ボタン1の処理、二枚の画像に変換
    fname = dialog()                                          #ダイアログ作成
    w=wave.open(fname)                                        #入力ファイルを開く   
    print_info(w)                                             #情報の出力     
    make_cip(get_data(w))                                     #画像ファイルの出力
    global info
    info = tkinter.Label(root,text="音声は画像に変換されました！",font=16)
    info.place(x=150,y=500)

def show_img1(event):                                          #ボタン2の処理
    global img1        
    img1 = ImageTk.PhotoImage(Image.open(IMG1))
    sub = Toplevel(root)
    sub.title(IMG1)
    frame = tkinter.Frame(sub)
    frame.pack()
    label = tkinter.Label(frame, image=img1)
    label.pack()
    button = Button(sub, text="閉じる", command=sub.destroy)
    button.pack()
    sub.grab_set()                                             #サブウィンドウにフォーカスを当てる

def show_img2(event):                                          #ボタン3の処理
    global img2
    img2 = ImageTk.PhotoImage(Image.open(IMG2))
    sub = Toplevel(root)
    sub.title(IMG2)
    frame = tkinter.Frame(sub)
    frame.pack()
    label = tkinter.Label(frame, image=img2)
    label.pack()
    button = Button(sub, text="閉じる", command=sub.destroy)    
    button.pack()
    sub.grab_set()                                            #サブウィンドウにフォーカスを当てる

def decode(event):                                            #ボタン4の処理、画像を音声に逆変換
    channel = 2
    tmp_data = read_bmp(IMG1,IMG2)                            #画像読み込み
    make_wave_file(array.array('h', tmp_data), channel)       #音声ファイルの出力
    print("out.wavを保存しました。")
    global info
    info.config(text="音声に逆変換しました！",font=16)

#----ボタン作成---- 
def mk_button(str,c,func,bx,by,wd=20,ht=3):
    button = tkinter.Button(text=str,width=wd,height=ht,bg=c)
    button.bind("<Button-1>",func)
    button.place(x=bx,y=by)
    
#---------------

if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("title")
    root.geometry("950x600")
    mk_button(str="変換",c="blue",bx=200,by=300,func=encode)
    mk_button(str="画像1を表示",c="green",bx=400,by=200,func=show_img1)
    mk_button(str="画像2を表示",c="green",bx=400,by=400,func=show_img2)
    mk_button(str="復号",c="blue",bx=600,by=300,func=decode)
    root.mainloop()
    
