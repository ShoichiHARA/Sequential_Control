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
        self.master.geometry("800x500")  # ウインドウサイズ
        # self.master.state("zoomed")  # ウインドウ最大化
        self.master.configure(menu=self.bar)  # メニューバー追加
        self.master.bind("<KeyRelease-Escape>", self.exit)

        # 設定
        self.lad.draw_lst()     # 描画用配列生成
        self.fl_tab.add_menu()  # ファイルメニュー追加

        # テスト表示
        self.ed_tab.new()

    # アプリケーション終了
    def exit(self, e=None):
        self.master.destroy()


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
        self.ps_sh = False  # シフトーキー押下
        self.ps_ct = False  # コントロールキー押下
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
        # self.cvs.bind("<KeyPress-Up>", pt(self.csr_move, k="U"), "+")
        # self.cvs.bind("<KeyPress-Down>", pt(self.csr_move, k="D"), "+")
        # self.cvs.bind("<KeyPress-Left>", pt(self.csr_move, k="L"), "+")
        # self.cvs.bind("<KeyPress-Right>", pt(self.csr_move, k="R"), "+")
        self.cvs.bind("<ButtonPress-1>", pt(self.csr_move, k="M"), "+")
        self.cvs.bind("<Double-ButtonPress-1>", pt(self.csr_move, k="K"), "+")

        # 命令入力設定
        self.cm_fr.configure(bd=2, relief=tk.RAISED)  # フォーム用フレーム
        self.lb_fr.configure(padx=10, pady=10)        # 1段目フレーム
        self.bt_fr.configure(pady=10)                 # 2段目フレーム
        self.cm_bx.configure(width=5, values=self.mw.lad.cm_ls, font=("", 12))
        self.cm_et.configure(width=20, font=("", 12))
        self.ok_bt.configure(width=10, text=g.lg.ook, command=self.ok_clk)
        self.cn_bt.configure(width=10, text=g.lg.ccl, command=self.cn_clk)
        self.cm_et.bind("<KeyPress-Return>", self.ok_clk)
        self.cm_et.bind("<KeyPress-Escape>", self.cn_clk)
        self.cm_bx.pack(side=tk.LEFT)
        self.cm_et.pack(padx=10)
        self.cn_bt.pack(side=tk.RIGHT, padx=10)
        self.ok_bt.pack(anchor=tk.E)
        self.lb_fr.pack(anchor=tk.W)
        self.bt_fr.pack(anchor=tk.E)

        # テスト用
        # self.imp_cmd(None)  # 命令入力フォーム表示
        self.cvs.bind("<KeyPress>", self.key_prs, "+")
        self.cvs.bind("<KeyRelease>", self.key_rls, "+")

    # 新規作成
    def new(self):
        # 配置
        self.frm.pack(fill=tk.BOTH, expand=True)  # フレーム配置(fill:引き伸ばし)
        self.scr.pack(fill=tk.Y, side=tk.RIGHT)   # スクロールバー配置(side:右から)
        self.cvs.pack(fill=tk.BOTH, expand=True)  # キャンバス配置(expand:残領域に広げるか)

        # 設定
        self.draw_cmd("all", 0, 0)  # 全体再描画
        self.cvs.focus_set()  # キャンバスにフォーカス

    # 画面削除
    def delete(self):
        self.frm.pack_forget()

    # キーイベント振り分け
    def key_prs(self, e):
        print("e.keysym:", e.keysym)
        if e.keysym in ["Up", "Down", "Right", "Left"]:
            self.csr_move(e, e.keysym[0])  # カーソル移動
        elif e.keysym == "Return":
            self.imp_cmd(e)  # 命令入力
        if e.keysym in ["Shift_L", "Shift_R"]:
            self.ps_sh = True  # シフトキー有効
        elif e.keysym in ["Control_L", "Control_R"]:
            self.ps_ct = True  # コントロールキー有効
        elif e.keysym in ["Delete", "BackSpace"]:
            self.delt_cmd(e)  # 命令削除
        elif e.keysym.isalpha() and (len(e.keysym) == 1):
            self.imp_cmd(e)  # 命令入力
        elif e.keysym == "F5":
            self.mw.lad.display()  # 命令を文字で表示
        elif e.keysym == "F6":
            self.draw_cmd("all", 0, 0)  # 再描画

    # キーイベント（離す）
    def key_rls(self, e):
        if e.keysym in ["Shift_L", "Shift_R"]:
            self.ps_sh = False
        elif e.keysym in ["Control_L", "Control_R"]:
            self.ps_ct = False

    # カーソル左上x座標計算
    def cal_csr_x(self, n):
        return n * self.mw.st_tab.size * 24 + 50

    # カーソル左上y座標計算
    def cal_csr_y(self, n):
        return n * (self.mw.st_tab.size * 18 + self.mw.st_tab.height * 5) + 20

    # カーソル移動
    def csr_move(self, e, k=""):
        # カーソル位置を代入
        x = self.csr[0]
        y = self.csr[1]

        # 上
        if k == "U":
            if y > 0:   # 1列目でない場合
                y -= 1  # 上へ
                if self.ps_ct:  # コントロールキー押しながら
                    if y >= len(self.mw.lad.dr_ls) - 2:  # カーソル位置がENDより下の場合
                        for i in range(y-len(self.mw.lad.dr_ls)+3):  # 行が足りない分
                            self.mw.lad.ins_row()  # 行追加
                    self.mw.lad.dr_ls[y][x].l = not self.mw.lad.dr_ls[y][x].l  # 変更
                    self.draw_cmd(e, x, y)  # 描画

        # 下
        elif k == "D":
            if self.ps_ct:  # コントロールキー押しながら
                if y >= len(self.mw.lad.dr_ls) - 2:  # カーソル位置がENDより下の場合
                    for i in range(y-len(self.mw.lad.dr_ls)+3):  # 行が足りない分
                        self.mw.lad.ins_row()  # 行追加
                self.mw.lad.dr_ls[y][x].l = not self.mw.lad.dr_ls[y][x].l  # 変更
                self.draw_cmd(e, x, y)  # 描画
            y += 1      # 下へ

        # 左
        elif k == "L":
            if x > 0:   # 左端でない場合
                x -= 1  # 左へ
                if self.ps_ct:  # コントロールキー押しながら
                    if y >= len(self.mw.lad.dr_ls) - 1:  # カーソル位置がENDより下の場合
                        for i in range(y-len(self.mw.lad.dr_ls)+2):  # 行が足りない分
                            self.mw.lad.ins_row()  # 行追加
                    if self.mw.lad.dr_ls[y][x].t is None:          # 空欄の場合
                        self.mw.lad.dr_ls[y][x].inp_cas(t="LINE")  # 線命令
                        self.draw_cmd(e, x, y)                     # 線描画
                    elif self.mw.lad.dr_ls[y][x].t == "LINE":      # 線の場合
                        self.mw.lad.dr_ls[y][x].inp_cas(t=None)    # 空白
                        self.draw_cmd(e, x, y)                     # 空白描画
            else:       # 左端の場合
                if y > 0:                          # 1列目でない場合
                    x = self.mw.st_tab.column - 1  # 右端へ
                    y -= 1                         # 一つ上へ

        # 右
        elif k == "R":
            if x < self.mw.st_tab.column - 1:  # 右端でない場合
                if self.ps_ct:  # コントロールキー押しながら
                    if y >= len(self.mw.lad.dr_ls) - 1:  # カーソル位置がENDより下の場合
                        for i in range(y-len(self.mw.lad.dr_ls)+2):  # 行が足りない分
                            self.mw.lad.ins_row()  # 行追加
                    if self.mw.lad.dr_ls[y][x].t is None:          # 空欄の場合
                        self.mw.lad.dr_ls[y][x].inp_cas(t="LINE")  # 線命令
                        self.draw_cmd(e, x, y)                     # 線描画
                    elif self.mw.lad.dr_ls[y][x].t == "LINE":      # 線の場合
                        self.mw.lad.dr_ls[y][x].inp_cas(t=None)    # 空白
                        self.draw_cmd(e, x, y)                     # 空白描画
                x += 1  # 右へ
            else:                 # 右端の場合
                x = 0   # 左端へ
                y += 1  # 一つ下へ
        elif k in ["M", "K"]:  # 左クリック
            if 50 <= e.x <= self.cal_csr_x(self.mw.st_tab.column):
                if 20 <= e.y:
                    x = (e.x - 50) // (self.cal_csr_x(1) - 50)
                    y = (e.y - 20) // (self.cal_csr_y(1) - 20)
        elif e is None:
            pass

        # カーソル描画
        x0 = self.cal_csr_x(x)
        y0 = self.cal_csr_y(y)
        x1 = self.cal_csr_x(x+1)
        y1 = self.cal_csr_y(y+1)
        self.cvs.coords("csr", x0, y0, x1, y1)  # カーソル図形移動

        # 自身の変数に戻す
        self.csr[0] = x
        self.csr[1] = y

        # 命令入力フォーム出現
        if k == "K":  # ダブルクリック
            self.imp_cmd(e)

    # 命令入力フォーム(カーソル位置の情報)
    def imp_cmd(self, e=None):
        self.cm_bx.delete(0, tk.END)  # プルダウン初期化
        self.cm_et.delete(0, tk.END)  # 入力欄初期化
        x = self.csr[0]  # カーソルx座標
        y = self.csr[1]  # カーソルy座標
        if y < len(self.mw.lad.dr_ls):  # END命令より上の場合
            if self.mw.lad.dr_ls[y][x].t not in [None, "LINE"]:  # 左の命令でない場合
                self.cm_bx.insert(tk.END, self.mw.lad.dr_ls[y][x].t)  # 命令種類表示
                self.cm_et.insert(tk.END, self.mw.lad.dr_ls[y][x].d)  # デバイス表示
        if e.keysym.isalpha() and (len(e.keysym) == 1):  # キーボードからの場合
            self.cm_et.insert(tk.END, e.keysym)
        self.cm_fr.place(x=300, y=200, anchor=tk.CENTER)
        self.cm_et.focus_set()  # 入力フォームにフォーカス

    # 決定押下
    def ok_clk(self, e=None):
        t = self.cm_bx.get()  # 命令種類取得
        d = self.cm_et.get()  # デバイス取得
        x = self.csr[0]  # カーソルx座標
        y = self.csr[1]  # カーソルy座標
        # print(t, ", ", d)
        self.cm_fr.place_forget()  # 命令入力フォーム非表示
        print("len =", len(self.mw.lad.dr_ls))
        if y >= len(self.mw.lad.dr_ls)-1:                # カーソル位置がENDより下の場合
            for i in range(y-len(self.mw.lad.dr_ls)+2):  # 行が足りない分
                self.mw.lad.ins_row()                    # 行追加
                print(i)
        self.mw.lad.dr_ls[y][x].inp_ent(t, d)  # 命令を入力
        self.draw_cmd(None, x, y)  # 描画
        self.cvs.focus_set()  # キャンバスにフォーカス
        self.csr_move(e, "R")  # カーソルを右へ

    # 取消押下
    def cn_clk(self, e=None):
        self.cm_fr.place_forget()  # 命令入力フォーム非表示
        self.cvs.focus_set()  # キャンバスにフォーカス

    # 命令描画
    def draw_cmd(self, e, x=0, y=0):  # xy:カーソルxy座標
        # 命令情報
        t = self.mw.lad.dr_ls[y][x].t
        d = self.mw.lad.dr_ls[y][x].d
        l = self.mw.lad.dr_ls[y][x].l

        # 全描画
        if e == "all":
            self.cvs.delete("all")
            for i in range(self.mw.st_tab.column):  # x軸
                for j in range(len(self.mw.lad.dr_ls)):  # y軸
                    self.draw_cmd(None, i, j)
            x1 = self.mw.st_tab.column * self.mw.st_tab.size * 24 + 50  # 右母線x座標
            y1 = 600                                                    # 母線y座標
            self.cvs.create_line(50, 20, 50, y1)  # 左母線
            self.cvs.create_line(x1, 20, x1, y1)  # 右母線
            self.cvs.create_rectangle(0, 0, 0, 0, tags="csr", width=3, outline="blue")
            self.csr_move(None)
            return

        x0 = self.cal_csr_x(x)  # 画面上原点（左上）x座標
        x1 = x0 + self.mw.st_tab.size * 8
        x2 = x0 + self.mw.st_tab.size * 10
        x3 = x0 + self.mw.st_tab.size * 12
        x4 = x0 + self.mw.st_tab.size * 14
        x5 = x0 + self.mw.st_tab.size * 16
        x6 = x0 + self.mw.st_tab.size * 24
        y0 = self.cal_csr_y(y)  # 画面上原点（左上）y座標
        y1 = y0 + self.mw.st_tab.size * 7
        y2 = y0 + self.mw.st_tab.size * 9
        y3 = y0 + self.mw.st_tab.size * 11
        y4 = y0 + self.mw.st_tab.size * 18
        tag = "x" + str(x) + "y" + str(y)
        self.cvs.delete(tag)  # すでにある描画削除

        if t in ["LD", "LDI", "LDP", "LDF"]:  # 入力命令基本
            self.cvs.create_line(x0, y2, x1, y2, tags=tag)
            self.cvs.create_line(x1, y1, x1, y3, tags=tag)
            self.cvs.create_line(x5, y1, x5, y3, tags=tag)
            self.cvs.create_line(x5, y2, x6, y2, tags=tag)
            self.cvs.create_text(
                x3, y1, anchor=tk.S, text=d, font=("", self.mw.st_tab.font), tags=tag
            )
        elif t == "LINE":  # 横線
            self.cvs.create_line(x0, y2, x6, y2, tags=tag)
        if t in ["LDI"]:  # 入力命令B接点
            self.cvs.create_line(x1, y3, x5, y1, tags=tag)
        elif t in ["LDP"]:  # 入力命令立上りパルス
            self.cvs.create_line(x3, y1, x3, y3, tags=tag)
            self.cvs.create_line(x2, y2, x3, y1, tags=tag)
            self.cvs.create_line(x3, y1, x4, y2, tags=tag)
        elif t in ["LDF"]:  # 入力命令立下りパルス
            self.cvs.create_line(x3, y1, x3, y3, tags=tag)
            self.cvs.create_line(x2, y2, x3, y3, tags=tag)
            self.cvs.create_line(x3, y3, x4, y2, tags=tag)
        if l:
            y5 = self.mw.st_tab.size * 18 + self.mw.st_tab.height * 5
            self.cvs.create_line(x0, y2, x0, y2+y5, tags=tag)

    # 命令削除
    def delt_cmd(self, e, x=None, y=None):
        if e is not None:
            if e.keysym == "BackSpace":  # バックスペース
                self.csr_move(e, "L")    # 一つ左へ
        if x is None:
            x = self.csr[0]
        if y is None:
            y = self.csr[1]
        tag = "x" + str(x) + "y" + str(y)  # タグ生成
        self.cvs.delete(tag)               # タグの描画すべて削除
        l = self.mw.lad.dr_ls[y][x].l      # 線
        self.mw.lad.dr_ls[y][x] = ld.DrawCom(l=l)  # 縦線以外命令初期化


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
        self.size = g.size0    # サイズ
        self.height = 1  # 高さ
        self.font = g.font0   # フォントサイズ
        self.menu = tk.Menu(self.mw.bar, tearoff=0, cursor="hand1")  # 編集メニュー
        self.sz_mn = tk.Menu(self.menu, tearoff=0, cursor="hand1")   # 描画サメニュー
        self.ft_mn = tk.Menu(self.menu, tearoff=0, cursor="hand1")   # 文字サメニュー

        # 設定
        self.mw.bar.add_cascade(label=g.lg.set, menu=self.menu)  # 設定メニュー追加
        self.menu.add_cascade(label=g.lg.siz, menu=self.sz_mn)   # 描画サメニュー追加
        self.sz_mn.add_command(label=g.lg.zin, command=self.draw_zoomin)   # 拡大
        self.sz_mn.add_command(label=g.lg.zot, command=self.draw_zoomout)  # 縮小
        self.menu.add_cascade(label=g.lg.fnt, menu=self.ft_mn)   # 文字サメニュー追加
        self.ft_mn.add_command(label=g.lg.zin, command=self.font_zoomin)   # 拡大
        self.ft_mn.add_command(label=g.lg.zot, command=self.font_zoomout)  # 縮小

    # 描画拡大
    def draw_zoomin(self):
        if self.size < 10:
            self.size += 1
            self.mw.ed_tab.draw_cmd("all")

    # 描画縮小
    def draw_zoomout(self):
        if self.size > 1:
            self.size -= 1
            self.mw.ed_tab.draw_cmd("all")

    # 文字拡大
    def font_zoomin(self):
        if self.font < 20:
            self.font += 2
            self.mw.ed_tab.draw_cmd("all")

    # 文字縮小
    def font_zoomout(self):
        if self.font > 2:
            self.font -= 2
            self.mw.ed_tab.draw_cmd("all")


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
            self.mw.ed_tab.draw_cmd("all")

    # 縮小
    def zoom_out(self):
        if self.mw.st_tab.size > 1:
            self.mw.st_tab.size -= 1
            self.mw.ed_tab.draw_cmd("all")


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
