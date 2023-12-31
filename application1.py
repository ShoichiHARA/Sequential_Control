import tkinter as tk
from tkinter import messagebox


# アプリケーション https://denno-sekai.com/tkinter-bind/
class Application(tk.Frame):
    def __init__(self: tk.Tk, master=None):
        super().__init__(master)  # 親クラスの継承
        self.pack()               # 配置

        # ウインドウの設定
        self.master.title("Sequential_Control")  # ウインドウタイトル
        self.master.geometry("400x300")          # ウインドウサイズ(横x縦)

        # メニューバーの設定
        self.bar = tk.Menu(self)                  # メニューバー
        self.master.configure(menu=self.bar)      # メニューバー設定
        self.file = tk.Menu(self.bar, tearoff=0)  # ファイルメニュー
        self.bar.add_cascade(label="File", menu=self.file)
        self.file.add_command(label="Setting")    # 設定
        self.file.add_separator()                 # 境界線
        self.file.add_command(label="Exit")       # 終了
        self.help = tk.Menu(self.bar, tearoff=0)  # ヘルプメニュー
        self.bar.add_cascade(label="Help", menu=self.help)

        # キャンバスの設定
        self.cvs = tk.Canvas(self.master, bg="white")  # 背景色
        self.cvs.pack(fill=tk.BOTH, expand=True)       # 配置

        # 実習盤の生成
        self.practice_board()

        # イベント
        self.event()

    def practice_board(self):
        # キャンバスの設定
        # self.cvs = tk.Canvas(self.master, bg="white")  # 背景色
        # self.cvs.pack(fill=tk.BOTH, expand=True)       # 配置
        # 配置の参考 https://imagingsolution.net/program/python/tkinter/widget_layout_pack/
        pass

    def event(self):
        def m_press(e):
            if e.num == 1:
                print("Press Left")
            if e.num == 3:
                print("Press Right")

        def m_release(e):
            if e.num == 1:
                print("Release Left")
            if e.num == 3:
                print("Release Right")

        def k_press(e):
            print(e.char, "press")

        def k_release(e):
            print(e.char, "release")

        self.master.bind("<ButtonPress>", m_press)      # マウス押下
        self.master.bind("<ButtonRelease>", m_release)  # マウス解放
        self.master.bind("<KeyPress>", k_press)         # キー押下
        self.master.bind("<KeyRelease>", k_release)     # キー解放


# アプリケーション
def application():
    # Tkinterインスタンスの生成
    root = tk.Tk()

    # アプリケーション実行
    app = Application(master=root)

    """
    # 変数を使ってウインドウの設定
    root.title("Sequential_Control")  # ウインドウのタイトルの指定
    root.geometry("800x600")          # ウインドウサイズの指定(横x縦)

    # 実習盤の生成
    practice_board(root)
    
    # ウインドウの描画
    root.mainloop()
    """

    # ウインドウの描画
    app.mainloop()
