import tkinter as tk


# メインウインドウ
class MainWin(tk.Frame):
    def __init__(self: tk.Tk, master):
        super().__init__(master)
        self.pack()


# メニューバークラス
class MenuBar:
    def __init__(self, mw: MainWin):
        # 定義
        self.mw = mw
        self.bar = tk.Menu(self.mw.master)


# アプリケーション
def application():
    root = tk.Tk()
    app = MainWin(master=root)
    app.mainloop()
