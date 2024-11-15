import tkinter as tk
from tkinter import ttk
from functools import partial as pt
import gvalue as g
import ladder as ld


# メインウインドウ
class MainWin(tk.Frame):
    def __init__(self: tk.Tk, master):
        super().__init__(master)
        self.pack()

        # 定義
        self.bar = tk.Menu(self.master)
        self.lad = ld.Ladder1(self)  # ラダープログラム
        self.fl_tab = FileTab(self)  # ファイルタブ
        self.ed_tab = EditTab(self)  # 編集タブ
        self.sm_tab = SimuTab(self)  # シミュレーションタブ
        self.st_tab = SetTab(self)   # 設定タブ
        self.vw_tab = ViewTab(self)  # 表示タブ
        self.hp_tab = HelpTab(self)  # ヘルプタブ

        # ウインドウの定義
        self.master.title(g.lg.tit)  # ウインドウタイトル
        self.master.geometry("600x400")  # ウインドウサイズ
        # self.master.state("zoomed")  # ウインドウ最大化
        self.master.configure(menu=self.bar)  # メニューバー追加

        # 設定
        self.fl_tab.add_menu()  # ファイルメニュー追加

        # テスト表示
        self.ed_tab.new()


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
        self.cm_fr = tk.Frame(self.mw.master)  # 命令入力用フレーム
        self.lb_fr = tk.Frame(self.cm_fr)      # 1段目フレーム
        self.bt_fr = tk.Frame(self.cm_fr)      # 2段目フレーム
        self.cm_bx = ttk.Combobox(self.lb_fr)  # 命令種類プルダウン
        self.cm_et = ttk.Entry(self.lb_fr)     # 入力フォーム
        self.ok_bt = tk.Button(self.bt_fr)     # 決定ボタン
        self.cn_bt = tk.Button(self.bt_fr)     # 取消ボタン

        # メニューバー設定
        self.mw.bar.add_cascade(label=g.lg.edt, menu=self.menu)  # 編集メニュー追加
        self.menu.add_command(label=g.lg.add, command=kari)      # 追加
        self.menu.add_command(label=g.lg.ins, command=kari)      # 挿入
        self.menu.add_command(label=g.lg.dlt, command=kari)      # 削除

        # スクロールバー設定
        self.cvs.configure(yscrollcommand=self.scr.set)  # 画面を移動させるスクロールバーを設定
        self.scr.configure(command=self.cvs.yview)       # スクロールバーで画面を移動

        # カーソル設定
        self.mw.master.bind("<KeyPress-Up>", pt(self.csr_move, k="U"), "+")
        self.mw.master.bind("<KeyPress-Down>", pt(self.csr_move, k="D"), "+")
        self.mw.master.bind("<KeyPress-Left>", pt(self.csr_move, k="L"), "+")
        self.mw.master.bind("<KeyPress-Right>", pt(self.csr_move, k="R"), "+")

        # 命令入力設定
        self.cm_fr.configure(bd=2, relief=tk.RAISED)  # フォーム用フレーム
        self.lb_fr.configure(padx=10, pady=10)                 # 1段目フレーム
        self.bt_fr.configure(pady=10)                 # 2段目フレーム
        self.cm_bx.configure(width=5, values=self.mw.lad.cm_ls, font=("", 12))
        self.cm_et.configure(width=20, font=("", 12))
        self.ok_bt.configure(width=10, text=g.lg.ook, command=self.ok_clk)
        self.cn_bt.configure(width=10, text=g.lg.ccl, command=self.cn_clk)
        self.cm_bx.pack(side=tk.LEFT)
        self.cm_et.pack(padx=10)
        self.cn_bt.pack(side=tk.RIGHT, padx=10)
        self.ok_bt.pack(anchor=tk.E)
        self.lb_fr.pack(anchor=tk.W)
        self.bt_fr.pack(anchor=tk.E)

        # テスト用
        self.imp_cmd(None)
        self.mw.master.bind("<KeyPress>", pt(self.csr_move))
        self.mw.master.bind("<KeyPress-l>", pt(self.draw_cmd, x=self.csr[0], y=self.csr[1], t="LD"), "+")
        self.mw.master.bind("<KeyPress-k>", pt(self.imp_cmd), "+")

    # 新規作成
    def new(self):
        # 変数
        x1 = self.mw.st_tab.column * self.mw.st_tab.size * 24 + 50
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
            if self.csr[1] > 0:   # 1列目でない場合
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
        x0 = self.csr[0] * self.mw.st_tab.size * 24 + 50
        y0 = self.csr[1] * self.mw.st_tab.size * 18 + self.mw.st_tab.height * 5 + 20
        x1 = (self.csr[0] + 1) * self.mw.st_tab.size * 24 + 50
        y1 = (self.csr[1] + 1) * self.mw.st_tab.size * 18 + self.mw.st_tab.height * 5 + 20
        self.cvs.coords("csr", x0, y0, x1, y1)

    # 命令入力フォーム
    def imp_cmd(self, e, t="", r=""):
        self.cm_bx.delete(0, tk.END)
        self.cm_et.delete(0, tk.END)
        self.cm_bx.insert(tk.END, t)
        self.cm_et.insert(tk.END, r)
        self.cm_fr.place(x=300, y=200)
        self.cm_et.focus_set()  # 入力フォームにフォーカス

    # 決定押下
    def ok_clk(self):
        t = self.cm_bx.get()  # 命令種類取得
        r = self.cm_et.get()  # レジスタ取得
        print(t, r)
        self.cm_fr.place_forget()  # 命令入力フォーム非表示

    # 取消押下
    def cn_clk(self):
        self.cm_fr.place_forget()

    # 命令描画
    def draw_cmd(self, e, x, y, t):  # xy:カーソルxy座標、t:命令種類
        self.delt_cmd(e, x, y)  # すでにあるもの削除
        x0 = x * self.mw.st_tab.size * 24 + 50  # 画面上原点（左上）x座標
        x1 = x0 + self.mw.st_tab.size * 8
        x2 = x0 + self.mw.st_tab.size * 10
        x3 = x0 + self.mw.st_tab.size * 12
        x4 = x0 + self.mw.st_tab.size * 14
        x5 = x0 + self.mw.st_tab.size * 16
        x6 = x0 + self.mw.st_tab.size * 24
        y0 = y * self.mw.st_tab.size * 18 + self.mw.st_tab.height * 5 + 20  # 画面上原点（左上）y座標
        y1 = y0 + self.mw.st_tab.size * 7
        y2 = y0 + self.mw.st_tab.size * 9
        y3 = y0 + self.mw.st_tab.size * 11
        y4 = y0 + self.mw.st_tab.size * 18
        tag = "t" + str(x) + str(y)

        if t in ["LD", "LDI", "LDP", "LDF", "AND", "OR"]:  # 入力命令基本
            self.cvs.create_line(x0, y2, x1, y2, tag=tag)
            self.cvs.create_line(x1, y1, x1, y3, tag=tag)
            self.cvs.create_line(x5, y1, x5, y3, tag=tag)
            self.cvs.create_line(x5, y2, x6, y2, tag=tag)
        if t in ["LDI"]:  # 入力命令B接点
            self.cvs.create_line(x1, y3, x5, y1, tag=tag)
        elif t in ["LDP"]:  # 入力命令立上りパルス
            self.cvs.create_line(x3, y1, x3, y3, tag=tag)
            self.cvs.create_line(x2, y2, x3, y1, tag=tag)
            self.cvs.create_line(x3, y1, x4, y2, tag=tag)
        elif t in ["LDF"]:  # 入力命令立下りパルス
            self.cvs.create_line(x3, y1, x3, y3, tag=tag)
            self.cvs.create_line(x2, y2, x3, y3, tag=tag)
            self.cvs.create_line(x3, y3, x4, y2, tag=tag)

    # 命令削除
    def delt_cmd(self, e, x, y):
        self.cvs.delete("t"+str(x)+str(y))
            


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
        self.height = 1  # 高さ
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
