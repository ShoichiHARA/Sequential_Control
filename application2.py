import tkinter as tk
from functools import partial as pt
import gvalue as g
# import ladder as ld


# メインウインドウ
class MainWin(tk.Frame):
    def __init__(self: tk.Tk, master):
        super().__init__(master)
        self.pack()

        # 定義
        self.bar = tk.Menu(self.master)
        # self.lad = ld.Ladder1(self)  # ラダープログラム
        self.fl_tab = FileTab(self)  # ファイルタブ
        self.ed_tab = EditTab(self)  # 編集タブ
        self.sm_tab = SimuTab(self)  # シミュレーションタブ
        self.st_tab = SetTab(self)   # 設定タブ
        self.vw_tab = ViewTab(self)  # 表示タブ
        self.hp_tab = HelpTab(self)  # ヘルプタブ

        # ウインドウの定義
        self.master.title(g.lg.tit)  # ウインドウタイトル
        self.master.geometry("400x300")  # ウインドウサイズ
        # self.master.state("zoomed")  # ウインドウ最大化
        self.master.configure(menu=self.bar)  # メニューバー追加

        # 設定
        self.fl_tab.add_menu()  # ファイルメニュー追加


# ファイルタブクラス
class FileTab:
    def __init__(self, mw: MainWin):
        # 定義
        self.mw = mw
        self.menu = tk.Menu(self.mw.bar, tearoff=0)  # ファイルメニュー

        # 設定
        self.mw.bar.add_cascade(label=g.lg.fil, menu=self.menu)  # ファイルメニュー追加

    # メニュー追加
    def add_menu(self):
        self.menu.add_command(label=g.lg.new, command=self.new)                # 新規作成
        self.menu.add_command(label=g.lg.opn, command=self.open)               # 開く
        self.menu.add_separator()
        self.menu.add_command(label=g.lg.sav, command=self.save)               # 上書き保存
        self.menu.add_command(label=g.lg.sva, command=self.saveas)             # 名前を付けて保存
        self.menu.add_separator()
        self.menu.add_command(label=g.lg.cls, command=self.mw.ed_tab.delete)   # 閉じる
        self.menu.add_command(label=g.lg.ext, command=self.mw.master.destroy)  # 終了

    # 新規作成
    def new(self):
        self.mw.ed_tab.new()

    # 開く
    def open(self):
        pass

    # 上書き保存
    def save(self):
        pass

    # 名前を付けて保存
    def saveas(self):
        pass


# 編集タブクラス
class EditTab:
    def __init__(self, mw: MainWin):
        # 定義
        self.mw = mw
        self.menu = tk.Menu(self.mw.bar, tearoff=0)  # 編集メニュー
        self.csr = [0, 0]  # カーソル座標
        self.frm = tk.Frame(self.mw.master)  # ラダー用フレーム
        self.cvs = tk.Canvas(self.frm, bg="white", highlightthickness=0)  # 描画キャンバス
        self.scr = tk.Scrollbar(self.frm, orient=tk.VERTICAL)  # スクロールバー

        # メニューバー設定
        self.mw.bar.add_cascade(label=g.lg.edt, menu=self.menu)  # 編集メニュー追加
        self.menu.add_command(label=g.lg.add, command=kari)      # 追加
        self.menu.add_command(label=g.lg.ins, command=kari)      # 挿入
        self.menu.add_command(label=g.lg.dlt, command=kari)      # 削除

        # スクロールバー設定
        self.cvs.configure(yscrollcommand=self.scr.set)  # 画面を移動させるスクロールバーを設定
        self.scr.configure(command=self.cvs.yview)       # スクロールバーで画面を移動

        # カーソル設定
        self.mw.master.bind("<KeyPress>", pt(self.csr_move))
        self.mw.master.bind("<KeyPress-Up>", pt(self.csr_move, k="U"), "+")
        self.mw.master.bind("<KeyPress-Down>", pt(self.csr_move, k="D"), "+")
        self.mw.master.bind("<KeyPress-Left>", pt(self.csr_move, k="L"), "+")
        self.mw.master.bind("<KeyPress-Right>", pt(self.csr_move, k="R"), "+")

    # 新規作成
    def new(self):
        # 変数
        x1 = self.mw.st_tab.column * self.mw.st_tab.size * 30 + 50
        y1 = 600

        # 配置
        self.frm.pack(fill=tk.BOTH, expand=True)  # フレーム配置(fill:引き伸ばし)
        self.scr.pack(fill=tk.Y, side=tk.RIGHT)   # スクロールバー配置(side:右から)
        self.cvs.pack(fill=tk.BOTH, expand=True)  # キャンバス配置(expand:残領域に広げるか)
        self.cvs.create_line(50, 20, 50, y1)  # 左母線
        self.cvs.create_line(x1, 20, x1, y1)  # 右母線
        self.cvs.create_rectangle(1, 1, 10, 10, tags="csr", width=3, outline="blue")  # カーソル配置
        self.csr_move(None, "")

    # 画面削除
    def delete(self):
        self.frm.pack_forget()

    # カーソル移動
    def csr_move(self, e, k=""):
        if k == "U":              # 上
            if self.csr[1] > 0:   # 1列目でないばあい
                self.csr[1] -= 1  # 上へ
        elif k == "D":            # 下
            self.csr[1] += 1      # 下へ
        elif k == "L":            # 左
            if self.csr[0] > 0:   # 左端でない場合
                self.csr[0] -= 1  # 左へ
            else:                 # 左端の場合
                if self.csr[1] > 0:  # 1列目でない場合
                    self.csr[0] = self.mw.st_tab.column - 1  # 右端へ
                    self.csr[1] -= 1                         # 一つ上へ
        elif k == "R":  # 右
            if self.csr[0] < self.mw.st_tab.column - 1:  # 右端でない場合
                self.csr[0] += 1  # 右へ
            else:                 # 右端の場合
                self.csr[0] = 0   # 左端へ
                self.csr[1] += 1  # 一つ下へ
        elif e is None:
            pass
        else:
            print(e.keysym)
        x0 = self.csr[0] * self.mw.st_tab.size * 30 + 50
        y0 = self.csr[1] * self.mw.st_tab.size * self.mw.st_tab.height * 10 + 20
        x1 = (self.csr[0] + 1) * self.mw.st_tab.size * 30 + 50
        y1 = (self.csr[1] + 1) * self.mw.st_tab.size * self.mw.st_tab.height * 10 + 20
        self.cvs.coords("csr", x0, y0, x1, y1)


# シミュレーションタブクラス
class SimuTab:
    def __init__(self, mw: MainWin):
        # 定義
        self.mw = mw
        self.menu = tk.Menu(self.mw.bar, tearoff=0)  # 編集メニュー

        # 設定
        self.mw.bar.add_cascade(label=g.lg.sim, menu=self.menu)  # シミュレーションメニュー追加
        self.menu.add_command(label=g.lg.stt, command=kari)  # 開始
        self.menu.add_command(label=g.lg.pus, command=kari)  # 一時停止
        self.menu.add_command(label=g.lg.stp, command=kari)  # 停止


# 設定タブクラス
class SetTab:
    def __init__(self, mw: MainWin):
        # 定義
        self.mw = mw
        self.column = 9  # 列数
        self.size = 5    # サイズ
        self.height = 2  # 高さ
        self.menu = tk.Menu(self.mw.bar, tearoff=0)  # 編集メニュー

        # 設定
        self.mw.bar.add_cascade(label=g.lg.set, menu=self.menu)  # 設定メニュー追加
        self.menu.add_command(label=g.lg.add, command=kari)  # 追加
        self.menu.add_command(label=g.lg.ins, command=kari)  # 挿入
        self.menu.add_command(label=g.lg.dlt, command=kari)  # 削除


# 表示タブクラス
class ViewTab:
    def __init__(self, mw: MainWin):
        # 定義
        self.mw = mw
        self.menu = tk.Menu(self.mw.bar, tearoff=0)  # 編集メニュー

        # 設定
        self.mw.bar.add_cascade(label=g.lg.viw, menu=self.menu)  # 表示メニュー追加
        self.menu.add_command(label=g.lg.zin, command=self.zoom_in)   # 拡大
        self.menu.add_command(label=g.lg.zot, command=self.zoom_out)  # 縮小

    # 拡大
    def zoom_in(self):
        if self.mw.st_tab.size < 10:
            self.mw.st_tab.size += 1
            self.mw.ed_tab.csr_move(None, "")

    # 縮小
    def zoom_out(self):
        if self.mw.st_tab.size > 1:
            self.mw.st_tab.size -= 1
            self.mw.ed_tab.csr_move(None, "")


# ヘルプタブクラス
class HelpTab:
    def __init__(self, mw: MainWin):
        # 定義
        self.mw = mw
        self.menu = tk.Menu(self.mw.bar, tearoff=0)  # 編集メニュー

        # 設定
        self.mw.bar.add_cascade(label=g.lg.hlp, menu=self.menu)  # ヘルプメニュー追加


# 仮関数
def kari():
    pass


# アプリケーション
def application():
    root = tk.Tk()
    app = MainWin(master=root)
    app.mainloop()