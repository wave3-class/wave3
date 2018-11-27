import tkinter as tk
from tkinter import ttk
from tkinter import Menu

win = tk.Tk()
win.title("Title")
a_label = ttk.Label(win, text="Hello")
a_label.grid(column=0, row=0)
menu_bar = Menu(win)
win.config(menu = menu_bar)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Exit", command=quit)
menu_bar.add_cascade(label="Files", menu=file_menu)
win.mainloop() 