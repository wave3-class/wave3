import os
import tkinter
import tkinter.filedialog
import tkinter.messagebox 
from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
import wave
from scipy import fromstring, int16
import math
import numpy
import array
import decryption
import cipher
import play_file
import embed_v3
import pyaudio
import glob

IMG1="a"
IMG2="b"
FRAME_RATE = 44100
input_name = "input.wav"
output_name = "output.tmp"
img1 = NONE          #PhotoImgaeはガーベジコレクションとして削除されるため、グローバル変数に設定
img2 = NONE
#info = NONE
frame = []                 #画像埋め込み用リスト
im = []
ic = []
INPUTFILE = NONE
EMBED_IMG = "lenna_c.bmp"

def dialog():                                                          #ダイアログ作成
    fTyp = [("","*.wav")]                                               #拡張子限定
    iDir = os.path.abspath(os.path.dirname(__file__))                    #ディレクリ変数
    #tkinter.messagebox.showinfo("wave","入力ファイルを選択してください！")
    filename = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
    #filename=(os.path.basename(filename))                    #ファイル名
    global INPUTFILE
    INPUTFILE = (os.path.basename(filename)) 
    return filename                                           #フルパスを戻り値

def encode(event):                                             #ボタン1の処理、二枚の画像に変換
    info.set("exchanging...")
    fname = dialog()                                         #ダイアログ作成
    w=wave.open(fname)                                        #入力ファイルを開く   
    cipher.print_info(w)                                      #情報の出力     
    cipher.make_cip(cipher.get_data(w))                              #画像ファイルの出力
    embed_v3.embed(IMG1,EMBED_IMG)
    embed_v3.embed(IMG2,EMBED_IMG)
    #global info
    #info = tkinter.Label(root,text="音声は画像に変換されました！",font=16)
    #info.place(x=150,y=500)
    info.set("音声は画像に変換されました！")

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
    #global info
    #info.config(text="音声に逆変換しました！",font=16)
    info.set("音声に逆変換しました！")

def play_input(event):
    info.set(INPUTFILE+"を再生しました")
    play_file.wave_play(INPUTFILE)

def play_output(event):
    info.set("out.wavを再生しました")
    play_file.wave_play("out.wav")

def nothing(event):
    print("-")

#----ボタン作成---- 
def mk_button(cnt,icon,relief,bx,by,w,h,func):
    frame.append(tkinter.Frame(root,bd=2,relief=relief,width=w,height=h))
    frame[cnt].place(x=bx,y=by)
    im.append(Image.open(icon+".png"))
    img_resize = im[cnt].resize((w,h))
    iDir = os.path.abspath(os.path.dirname(__file__))
    img_resize.save(iDir+"/"+icon+"_resized.png")
    ic.append(PhotoImage(file=icon+"_resized.png"))
    button = tkinter.Button(frame[cnt],relief=relief,image=ic[cnt],width=w,height=h)
    button.bind("<Button-1>",func)
    button.pack()

def get_list():
    ls = glob.glob("./*.jpg")
    ls += glob.glob("./*.png")
    ls += glob.glob("./*.bmp")
    for i in range(len(ls)):
        ls[i] = ls[i][2:]
    return ls

def chan_embed_img(event):
    global EMBED_IMG
    EMBED_IMG = v1.get()
    embed_v3.embed(IMG1,EMBED_IMG)
    embed_v3.embed(IMG2,EMBED_IMG)

def mk_combobox(v1,cnt,bx,by,w,h):
    frame.append(tkinter.Frame(root,width=w,height=h))
    frame[cnt].place(x=bx,y=by)
    cb = ttk.Combobox(frame[cnt], textvariable=v1)
    cb.bind('<<ComboboxSelected>>',chan_embed_img)
    lst = tuple(get_list())
    cb['values'] = lst
    cb.set("ファイルを選択してください")
    cb.grid(row=0, column=0)
#---------------

if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("execution")
    root.geometry("1200x700")
    info = tkinter.StringVar()
    label_info = Label(root,textvariable = info,font=16)
    label_info.place(x=450,y=600)
    info.set("presented by WAVE3")
    v1 = tkinter.StringVar()
    """
    mk_button(str="変換",c="blue",bx=100,by=300,func=encode)
    mk_button(str="画像1を表示",c="green",bx=300,by=200,func=show_img1)
    mk_button(str="画像2を表示",c="green",bx=300,by=400,func=show_img2)
    mk_button(str="復号",c="blue",bx=500,by=300,func=decode)
    mk_button(str="復号した音を再生する",c="red",bx=700,by=300,func=play_wave)
    """
    mk_button(cnt=0,icon="1",relief="raised",bx=75,by=135,w=140,h=70,func=encode)
    mk_button(cnt=1,icon="2",relief="raised",bx=75,by=225,w=140,h=140,func=encode)
    mk_button(cnt=2,icon="7",relief="raised",bx=75,by=385,w=140,h=70,func=play_input)
    mk_button(cnt=3,icon="3",relief="flat",bx=240,by=115,w=220,h=140,func=nothing)
    mk_button(cnt=4,icon="6",relief="flat",bx=240,by=335,w=220,h=140,func=nothing)
    mk_button(cnt=5,icon="8",relief="raised",bx=480,by=65,w=200,h=200,func=show_img1)
    mk_button(cnt=6,icon="8",relief="raised",bx=480,by=305,w=200,h=200,func=show_img2)
    mk_button(cnt=7,icon="5",relief="flat",bx=720,by=115,w=250,h=140,func=decode)
    mk_button(cnt=8,icon="4",relief="flat",bx=720,by=335,w=250,h=140,func=decode)
    mk_button(cnt=9,icon="2",relief="raised",bx=990,by=225,w=140,h=140,func=play_output)
    mk_button(cnt=10,icon="7",relief="raised",bx=990,by=385,w=140,h=70,func=play_output)
    mk_combobox(v1=v1,cnt=11,bx=530,by=550,w=100,h=100)

    # menu_bar
    menu_bar = Menu(root)
    root.config(menu = menu_bar)
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Exit", command=quit)
    menu_bar.add_cascade(label="Files", menu=file_menu)
    
    root.mainloop()
    
