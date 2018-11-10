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
import decryption
import cipher
import play_file
import embed_v2

IMG1="a"
IMG2="b"
FRAME_RATE = 44100
input_name = "input.wav"
output_name = "output.tmp"
img1 = NONE          #PhotoImgaeはガーベジコレクションとして削除されるため、グローバル変数に設定
img2 = NONE
info = NONE 

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
    cipher.print_info(w)                                      #情報の出力     
    cipher.make_cip(cipher.get_data(w))                              #画像ファイルの出力
    embed_v2.embed(IMG1)
    embed_v2.embed(IMG2)
    global info
    info = tkinter.Label(root,text="音声は画像に変換されました！",font=16)
    info.place(x=150,y=500)

def show_img1(event):                                          #ボタン2の処理
    global img1        
    img1 = ImageTk.PhotoImage(Image.open(IMG1+".png"))
    sub = Toplevel(root)
    sub.title(IMG1+".png")
    frame = tkinter.Frame(sub)
    frame.pack()
    label = tkinter.Label(frame, image=img1)
    label.pack()
    button = Button(sub, text="閉じる", command=sub.destroy)
    button.pack()
    sub.grab_set()                                             #サブウィンドウにフォーカスを当てる

def show_img2(event):                                          #ボタン3の処理
    global img2
    img2 = ImageTk.PhotoImage(Image.open(IMG2+".png"))
    sub = Toplevel(root)
    sub.title(IMG2+".png")
    frame = tkinter.Frame(sub)
    frame.pack()
    label = tkinter.Label(frame, image=img2)
    label.pack()
    button = Button(sub, text="閉じる", command=sub.destroy)    
    button.pack()
    sub.grab_set()                                               #サブウィンドウにフォーカスを当てる

def decode(event):                                                       #ボタン4の処理、画像を音声に逆変換
    channel = 2
    tmp_data = decryption.read_bmp(IMG1,IMG2)                           #画像読み込み
    decryption.make_wave_file(tmp_data, channel)       #音声ファイルの出力
    print("out.wavを保存しました。")
    global info
    info.config(text="音声に逆変換しました！",font=16)

def play_wave(event):
    play_file.wave_play("out.wav")

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
    mk_button(str="変換",c="blue",bx=100,by=300,func=encode)
    mk_button(str="画像1を表示",c="green",bx=300,by=200,func=show_img1)
    mk_button(str="画像2を表示",c="green",bx=300,by=400,func=show_img2)
    mk_button(str="復号",c="blue",bx=500,by=300,func=decode)
    mk_button(str="復号した音を再生する",c="red",bx=700,by=300,func=play_wave)
    root.mainloop()
    
