import tkinter as tk
from PIL import ImageTk, Image
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
        self.x = 60
        self.y = 540
        self.a = 2
        self.b = 0
        self.ss0r = tk.PhotoImage(file="image/SS_Right.png")
        self.ss0l = tk.PhotoImage(file="image/SS_Left.png")
        self.ss1r = tk.PhotoImage(file="image/SS_Right.png")
        self.ss1l = tk.PhotoImage(file="image/SS_Left.png")
        self.pb1n = tk.PhotoImage(file="image/PB1_ON.png")
        self.pb1f = tk.PhotoImage(file="image/PB1_OFF.png")
        self.pb2n = tk.PhotoImage(file="image/PB2_ON.png")
        self.pb2f = tk.PhotoImage(file="image/PB2_OFF.png")

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
        # 切替スイッチ1
        self.cvs.create_image(40, 450, tags="ss0r", image=self.ss0r, anchor=tk.NW)
        self.cvs.create_image(40, 450, tags="ss0l", image=self.ss0l, anchor=tk.NW)
        self.cvs.create_text(44, 540, tags="ss0_t1", text="SS0 (z)", anchor=tk.NW, font=("", 18))
        self.cvs.create_text(50, 424, tags="ss0_t2", text=lg.mn, font=("", 18))
        self.cvs.create_text(115, 424, tags="ss0_t3", text=lg.at, font=("", 18))
        # self.cvs.create_text(self.x, self.y, tags="ss0_t2", text=lg.mn, anchor=tk.NW, font=("", 18))

        # 押しボタンスイッチ1
        self.cvs.create_image(200, 450, tags="pb1n", image=self.pb1n, anchor=tk.NW)
        self.cvs.create_image(200, 450, tags="pb1f", image=self.pb1f, anchor=tk.NW)

        # 押しボタンスイッチ2
        self.cvs.create_image(300, 450, tags="pb2n", image=self.pb2n, anchor=tk.NW)
        self.cvs.create_image(300, 450, tags="pb2f", image=self.pb2f, anchor=tk.NW)

        self.cvs.create_text(760, 590, tags="pt", text="x="+str(self.x)+", y="+str(self.y))
        self.cvs.create_text(760, 580, tags="ab", text="a="+str(self.a)+", b="+str(self.b))

    def event(self):
        def m_press(e):
            if e.num == 1:
                print("x=" + str(e.x) + ", y=" + str(e.y))
                # 要素の設定変更 https://daeudaeu.com/tkinter_canvas_method/
            if e.num == 3:
                pass

        def m_release(e):
            if e.num == 1:
                pass
            if e.num == 3:
                pass

        def k_press(e):
            if e.keysym in self.keep:
                return
            self.keep.append(e.keysym)
            if e.keysym == "1":
                self.cvs.lift("pb1n", "pb1f")
            if e.keysym == "2":
                self.cvs.lift("pb2n", "pb2f")
            if e.keysym == "z":
                if "ss0" in self.keep:
                    self.cvs.lift("ss0l", "ss0r")
                    self.keep.remove("ss0")
                else:
                    self.cvs.lift("ss0r", "ss0l")
                    self.keep.append("ss0")
            if e.keysym == "Right":
                self.x += 2
            if e.keysym == "Left":
                self.x -= 2
            if e.keysym == "Down":
                self.y += 2
            if e.keysym == "Up":
                self.y -= 2
            # self.cvs.moveto("pt", x=self.x, y=self.y)
            # self.cvs.moveto("ss0_t2", x=self.x, y=self.y)
            self.cvs.itemconfig("pt", text="x="+str(self.x)+", y="+str(self.y))

        def k_release(e):
            self.keep.remove(e.keysym)
            if e.keysym == "1":
                self.cvs.lift("pb1f", "pb1n")
            if e.keysym == "2":
                self.cvs.lift("pb2f", "pb2n")

        self.master.bind("<ButtonPress>", m_press)
        self.master.bind("<ButtonRelease>", m_release)
        self.master.bind("<KeyPress>", k_press)
        self.master.bind("<KeyRelease>", k_release)


# アプリケーション
def application():
    root = tk.Tk()  # Tkinterインスタンスの生成
    app = SubWin(master=root)  # アプリケーション実行
    app.mainloop()  # ウインドウの描画
