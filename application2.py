import tkinter as tk
import gvalue as g


# メインウインドウ
class MainWin(tk.Frame):
    def __init__(self: tk.Tk, master):
        super().__init__(master)
        self.pack()

        # 定義
        self.bar = tk.Menu(self.master)
        self.fl_tab = FileTab(self)  # ファイルタブ
        self.ed_tab = EditTab(self)  # 編集タブ
        self.sm_tab = SimuTab(self)  # シミュレーションタブ
        self.st_tab = SetTab(self)   # 設定タブ
        self.vw_tab = ViewTab(self)  # 表示タブ
        self.hp_tab = HelpTab(self)  # ヘルプタブ

        # ウインドウの定義
        self.master.title(g.lg.tit)  # ウインドウタイトル
        self.master.state("zoomed")  # ウインドウ最大化
        self.master.configure(menu=self.bar)  # メニューバー追加


# ファイルタブクラス
class FileTab:
    def __init__(self, mw: MainWin):
        # 定義
        self.mw = mw
        self.menu = tk.Menu(self.mw.bar, tearoff=0)  # ファイルメニュー

        # 設定
        self.mw.bar.add_cascade(label=g.lg.fil, menu=self.menu)  # ファイルメニュー追加
        self.menu.add_command(label=g.lg.new, command=self.new)                # 新規作成
        self.menu.add_command(label=g.lg.opn, command=self.open)               # 開く
        self.menu.add_separator()
        self.menu.add_command(label=g.lg.sav, command=self.save)               # 上書き保存
        self.menu.add_command(label=g.lg.sva, command=self.saveas)             # 名前を付けて保存
        self.menu.add_separator()
        self.menu.add_command(label=g.lg.ext, command=self.mw.master.destroy)  # 終了

    # 新規作成
    def new(self):
        pass

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

        # 設定
        self.mw.bar.add_cascade(label=g.lg.edt, menu=self.menu)  # 編集メニュー追加
        self.menu.add_command(label=g.lg.add, command=kari)  # 追加
        self.menu.add_command(label=g.lg.ins, command=kari)  # 挿入
        self.menu.add_command(label=g.lg.dlt, command=kari)  # 削除


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
