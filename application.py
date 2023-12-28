import tkinter as tk
from PIL import ImageTk
import language as lg


# メインウインドウ
class MainWin(tk.Frame):
    def __init__(self: tk.Tk, master):
        super().__init__(master)  # 親クラスの継承
        self.pack()  # 配置

        # 定義
        self.bar = None
        self.file = None
        self.view = None
        self.help = None

        # ウインドウの設定
        self.master.title(lg.mw)  # ウインドウタイトル
        self.master.geometry("400x300")  # ウインドウサイズ(横x縦)
        self.widgets()  # ウィジェット

        # サブウインドウの定義
        self.pb_win = None
        self.app = None

    # ウィジェット
    def widgets(self: tk.Tk):
        # メニューバー
        self.bar = tk.Menu(self)
        self.master.configure(menu=self.bar)
        self.file = tk.Menu(self.bar, tearoff=0)  # ファイルメニュー
        self.bar.add_cascade(label=lg.fl, menu=self.file)
        self.file.add_command(label=lg.st)  # 設定
        self.file.add_separator()  # 境界線
        self.file.add_command(label=lg.ex, command=self.exit)  # 終了
        self.view = tk.Menu(self.bar, tearoff=0)  # 表示メニュー
        self.bar.add_cascade(label=lg.vw, menu=self.view)
        self.view.add_command(label=lg.pb, command=self.pb_win)  # 実習盤
        self.help = tk.Menu(self.bar, tearoff=0)  # ヘルプメニュー
        self.bar.add_cascade(label=lg.hp, menu=self.help)

    # 終了
    def exit(self):
        self.master.destroy()

    # 実習盤ウインドウ表示
    def pb_win(self):
        self.pb_win = tk.Toplevel(self.master)
        self.app = SubWin(self.pb_win)


# 実習盤ウインドウ
class SubWin(tk.Frame):
    def __init__(self: tk.Tk, master):
        super().__init__(master)  # 親クラスの継承
        self.pack()  # 配置

        # 定義
        self.cvs = None
        self.keep = []
        self.x = 200
        self.y = 500
        self.a = 2
        self.b = 0

        # ウインドウの設定
        self.master.title(lg.pb)  # ウインドウタイトル
        self.master.geometry("800x600")  # ウインドウサイズ(横x縦)
        self.widgets()  # ウィジェット
        self.event()  # イベント

    # ウィジェット
    def widgets(self: tk.Tk):
        # キャンバスの設定
        self.cvs = tk.Canvas(self.master, bg="white")  # 背景色
        self.cvs.pack(fill=tk.BOTH, expand=True)  # 配置

        # 部品の配置 https://imagingsolution.net/program/python/tkinter/canvas_drawing_lines_circles_shapes/#toc14
        self.cvs.create_text(self.x, self.y, tags="ss0_t0", text="SS0")
        self.cvs.create_oval(200, 400, 250, 450, tags="pb1", width=3, fill="#00BFFF")
        self.cvs.create_oval(300, 400, 350, 450, tags="pb2", width=3, fill="#C0C0C0")

        self.cvs.create_text(760, 590, tags="pt", text="x="+str(self.x)+", y="+str(self.y))
        self.cvs.create_text(760, 580, tags="ab", text="a="+str(self.a)+", b="+str(self.b))

    def event(self):
        def m_press(e):
            if e.num == 1:
                print("x=" + str(e.x) + ", y=" + str(e.y))
                # 要素の設定変更 https://daeudaeu.com/tkinter_canvas_method/
                self.cvs.itemconfig("pb1", fill="#1E90FF")
            if e.num == 3:
                self.cvs.itemconfig("pb2", fill="#A9A9A9")

        def m_release(e):
            if e.num == 1:
                self.cvs.itemconfig("pb1", fill="#00BFFF")
            if e.num == 3:
                self.cvs.itemconfig("pb2", fill="#C0C0C0")

        def k_press(e):
            if e.keysym in self.keep:
                return
            self.keep.append(e.keysym)
            if e.keysym == "1":
                self.cvs.itemconfig("pb1", fill="#1E90FF")
            if e.keysym == "2":
                self.cvs.itemconfig("pb2", fill="#A9A9A9")
            if e.keysym == "Right":
                self.x += 2
            if e.keysym == "Left":
                self.x -= 2
            if e.keysym == "Down":
                self.y += 2
            if e.keysym == "Up":
                self.y -= 2
            self.cvs.moveto("pt", x=self.x, y=self.y)
            self.cvs.moveto("ss0_t1", x=self.x, y=self.y)
            self.cvs.itemconfig("pt", text="x="+str(self.x)+", y="+str(self.y))

        def k_release(e):
            self.keep.remove(e.keysym)
            if e.keysym == "1":
                self.cvs.itemconfig("pb1", fill="#00BFFF")
            if e.keysym == "2":
                self.cvs.itemconfig("pb2", fill="#C0C0C0")

        self.master.bind("<ButtonPress>", m_press)
        self.master.bind("<ButtonRelease>", m_release)
        self.master.bind("<KeyPress>", k_press)
        self.master.bind("<KeyRelease>", k_release)


# アプリケーション
def application():
    root = tk.Tk()  # Tkinterインスタンスの生成
    app = SubWin(master=root)  # アプリケーション実行
    app.mainloop()  # ウインドウの描画
