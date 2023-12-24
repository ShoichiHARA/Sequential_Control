import tkinter as tk
import language as lg


# メインウインドウ
class MainWin(tk.Frame):
    def __init__(self: tk.Tk, master):
        super().__init__(master)  # 親クラスの継承
        self.pack()               # 配置

        self.master.title(lg.mw)     # ウインドウタイトル
        self.master.geometry("400x300")  # ウインドウサイズ(横x縦)
        self.widgets()                   # ウィジェット

        self.bar = None
        self.file = None
        self.view = None
        self.help = None
        self.pb_win = None
        self.app = None

    # ウィジェット
    def widgets(self: tk.Tk):
        # メニューバー
        self.bar = tk.Menu(self)
        self.master.configure(menu=self.bar)
        self.file = tk.Menu(self.bar, tearoff=0)  # ファイルメニュー
        self.bar.add_cascade(label=lg.fl, menu=self.file)
        self.file.add_command(label=lg.st)        # 設定
        self.file.add_separator()                 # 境界線
        self.file.add_command(label=lg.ex, command=self.exit)  # 終了
        self.view = tk.Menu(self.bar, tearoff=0)  # 表示メニュー
        self.bar.add_cascade(label=lg.vw, menu=self.view)
        self.view.add_command(label=lg.pb, command=self.pb_win)  # 実習盤
        self.help = tk.Menu(self.bar, tearoff=0)  # ヘルプメニュー
        self.bar.add_cascade(label=lg.hp, menu=self.help)

    # 終了
    def exit(self):
        self.master.destroy()

    def pb_win(self):
        self.pb_win = tk.Toplevel(self.master)
        self.app = SubWindow(self.pb_win)


# サブウインドウ
class SubWindow(tk.Frame):
    def __init__(self: tk.Tk, master):
        super().__init__(master)  # 親クラスの継承
        self.pack()               # 配置

        self.master.title(lg.pb)         # ウインドウタイトル
        self.master.geometry("400x300")  # ウインドウサイズ(横x縦)
        self.widgets()                   # ウィジェット

        self.cvs = None

    # ウィジェット
    def widgets(self: tk.Tk):
        # キャンバスの設定
        self.cvs = tk.Canvas(self.master, bg="white")  # 背景色
        self.cvs.pack(fill=tk.BOTH, expand=True)  # 配置


# アプリケーション
def application():
    root = tk.Tk()              # Tkinterインスタンスの生成
    app = MainWin(master=root)  # アプリケーション実行
    app.mainloop()              # ウインドウの描画
