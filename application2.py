import tkinter as tk


# メインウインドウ
class MainWin(tk.Frame):
    def __init__(self: tk.Tk, master):
        super().__init__(master)
        self.pack()