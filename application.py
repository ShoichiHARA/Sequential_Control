import tkinter as tk
from tkinter import ttk
import ladder as ld
import language as lg


# メインウインドウ
class MainWin(tk.Frame):
    def __init__(self: tk.Tk, master):
        super().__init__(master)  # 親クラスの継承
        self.pack()  # 配置

        # 定義
        self.bar = tk.Menu(self)  # メニューバー
        self.file = tk.Menu(self.bar, tearoff=0)  # ファイルメニュー
        self.simu = tk.Menu(self.bar, tearoff=0)  # シミュレーションメニュー
        self.view = tk.Menu(self.bar, tearoff=0)  # 表示メニュー
        self.help = tk.Menu(self.bar, tearoff=0)  # ヘルプメニュー
        self.cvs = tk.Canvas(self.master, bg="white")  # キャンバス
        self.row = 7  # 列数
        self.csr = [0, 0]  # 画面上カーソル座標
        self.keep = []
        self.lad = ld.Ladder(self.row)
        self.com_frm = None  # 命令入力フレーム
        self.com_ent = None  # 命令入力欄
        self.com_str = ""  # 命令入力文字列
        self.com_num = 0  # 命令数
        self.io_list = []
        self.run = 0
        self.line = tk.PhotoImage(file="image/Line.png")
        self.make = tk.PhotoImage(file="image/Make.png")
        self.brek = tk.PhotoImage(file="image/Break.png")
        self.plse = tk.PhotoImage(file="image/Pulse.png")
        self.fall = tk.PhotoImage(file="image/Falling.png")
        self.base = tk.PhotoImage(file="image/Base_Out.png")

        # ウインドウの設定
        self.master.title(lg.mw)  # ウインドウタイトル
        self.master.geometry("800x600")  # ウインドウサイズ(横x縦)
        self.widgets()  # ウィジェット
        # self.coin = self.ComInput()  # 入力フレーム
        self.event()  # イベント

        # サブウインドウの定義
        self.in_mas = None
        self.pb_mas = None
        self.io_mas = None
        # self.io_mas = tk.Toplevel(self.master)
        self.in_app = None
        self.pb_app = None
        self.io_app = None
        # self.io_app = IOWin(self.io_win)

        # self.io_win()
        # self.io_mas.master.destroy()

        # リストの表作り
        for i in range(10):
            self.io_list.append(["", "", "", ""])

    # ウィジェット
    def widgets(self: tk.Tk):
        # メニューバー
        self.master.configure(menu=self.bar)                      # メニューバー追加
        self.bar.add_cascade(label=lg.fl, menu=self.file)         # ファイルメニュー追加
        self.file.add_command(label=lg.st)                        # 設定
        self.file.add_separator()                                 # 境界線
        self.file.add_command(label=lg.ex, command=self.exit)     # 終了
        self.bar.add_cascade(label=lg.sm, menu=self.simu)         # シミュレーションメニュー追加
        self.simu.add_command(label=lg.rn, command=self.sm_run)   # シミュレーション実行
        self.simu.add_separator()                                 # 境界線
        self.simu.add_command(label=lg.sp, command=self.sm_stop)  # シミュレーション停止
        self.bar.add_cascade(label=lg.vw, menu=self.view)         # 表示メニュー追加
        self.view.add_command(label=lg.pb, command=self.pb_win)   # 実習盤
        self.view.add_separator()                                 # 境界線
        self.view.add_command(label=lg.io, command=self.io_win)   # 割付表
        self.bar.add_cascade(label=lg.hp, menu=self.help)         # ヘルプメニュー追加

        # キャンバスの設定
        self.cvs.pack(fill=tk.BOTH, expand=True)                        # キャンバス配置
        self.cvs.create_line(50, 20, 50, 580, fill="black", width=3)    # 左側母線
        self.cvs.create_line(750, 20, 750, 580, fill="black", width=3)  # 右側母線

        # カーソル
        self.cvs.create_rectangle(
            0, 0, 100, 80, tags="csr", outline="blue", width=3
        )
        self.cvs.moveto("csr", self.csr[0]*100+50, self.csr[1]*80+20)

    # 終了
    def exit(self):
        self.master.destroy()

    # シミュレーション開始
    def sm_run(self):
        if self.run == 0:                         # 呼び出された初回の場合
            self.run = 1                          # 実行フラグON
            self.lad.org()
        if self.run == 1:
            print("run")
            for i in range(len(self.io_list)):
                if self.io_list[i][1] in self.pb_app.sw_on:
                    self.lad.change(self.io_list[i][0], 1)
                else:
                    self.lad.change(self.io_list[i][0], 0)
            self.lad.run()
            self.pb_app.out_on = []
            for i in range(len(self.io_list)):
                for j in range(len(self.lad.ladder)):
                    if self.io_list[i][2] == self.lad.ladder[j][-1].tag:
                        if self.lad.ladder[j][-1].opt == 1:
                            self.pb_app.out_on.append(self.io_list[j][3])
            if self.pb_app is not None:
                self.pb_app.out_func()
            self.master.after(1000, self.sm_run)
        else:
            self.run = 0
            return

    # シミュレーション終了
    def sm_stop(self):
        self.run = 9

    # 命令入力ウインドウ表示
    def in_win(self):
        self.in_mas = tk.Toplevel(self.master)
        self.in_app = InWin(self.in_mas)

    # 実習盤ウインドウ表示
    def pb_win(self):
        self.pb_mas = tk.Toplevel(self.master)
        self.pb_app = PBWin(self.pb_mas)

    # 割付表ウインドウ表示
    def io_win(self):
        self.io_mas = tk.Toplevel(self.master)
        self.io_app = IOWin(self.io_mas, self.io_list)

    # イベント
    def event(self):
        def m_press(e):
            if e.num == 1:
                if self.com_frm is None:
                    if 50 < e.x < 750:
                        if 20 < e.y < 580:
                            self.csr[0] = (e.x - 50) // 100
                            self.csr[1] = (e.y - 20) // 80
                            self.csr_move()
            elif e.num == 3:
                print(self.io_list)

        def m_release(e):
            if e.num == 1:
                pass

        def mm_press(e):
            if e.num == 1:  # マウス左ダブルクリック
                if self.com_frm is None:
                    if 50 < e.x < 750:
                        if 20 < e.y < 580:
                            self.com_input()  # 命令入力

        def k_press(e):
            if e.keysym in self.keep:
                return
            self.keep.append(e.keysym)
            # print(e.keysym)
            if e.keysym == "Return":
                if self.com_frm is not None:
                    self.com_ok()  # 命令入力決定
                else:
                    self.com_input()  # 命令入力
            if e.keysym == "Escape":
                if self.com_frm is not None:
                    self.com_cn()  # 命令入力取消
                else:
                    self.exit()  # プログラム終了
            if e.keysym == "Up":
                pass
            if e.keysym in ["Up", "Down", "Left", "Right"]:
                if self.com_frm is None:
                    self.csr_move(e.keysym)

        def k_release(e):
            if e.keysym in self.keep:
                self.keep.remove(e.keysym)

        self.master.bind("<ButtonPress>", m_press)
        self.master.bind("<ButtonRelease>", m_release)
        self.master.bind("<Double-ButtonPress>", mm_press)
        self.master.bind("<KeyPress>", k_press)
        self.master.bind("<KeyRelease>", k_release)

    # カーソル移動
    def csr_move(self, d=""):
        if d == "Right":
            if self.csr[0] < 6:
                self.csr[0] += 1
            else:
                if self.csr[1] < 6:
                    self.csr[0] = 0
                    self.csr[1] += 1
        elif d == "Left":
            if self.csr[0] > 0:
                self.csr[0] -= 1
            else:
                if self.csr[1] > 0:
                    self.csr[0] = 6
                    self.csr[1] -= 1
        elif d == "Down":
            if self.csr[1] < 6:
                self.csr[1] += 1
        elif d == "Up":
            if self.csr[1] > 0:
                self.csr[1] -= 1
        self.cvs.moveto("csr", self.csr[0]*100+50, self.csr[1]*80+20)

    # 命令入力
    def com_input(self):
        self.com_frm = tk.Frame(  # 入力フレーム追加
            self.cvs, width=300, height=120,
            relief=tk.RIDGE, bd=2
        )
        ti_l = tk.Label(self.com_frm, text=lg.ic)  # テキスト追加
        self.com_ent = tk.Entry(self.com_frm, font=("", 14), width=27)  # 入力欄追加
        ok_b = tk.Button(self.com_frm, text=lg.ok, width=8, command=self.com_ok)  # 決定ボタン追加
        cn_b = tk.Button(self.com_frm, text=lg.cn, width=8, command=self.com_cn)  # 取消ボタン追加
        ti_l.place(x=10, y=10)
        self.com_ent.place(x=10, y=40)
        ok_b.place(x=135, y=80)
        cn_b.place(x=215, y=80)
        self.com_frm.place(x=250, y=240)
        self.com_ent.focus_set()  # 入力欄有効

    # 命令入力決定
    def com_ok(self):
        print("ok")
        self.com_str = self.com_ent.get()  # 入力文字列取得
        self.com_frm.destroy()  # 入力フレーム削除
        self.com_frm = None     # 入力フレーム無効

        err = 0  # エラー判定プログラム作成予定

        com_str = self.com_str.split()
        if err == 1:
            return
        elif err == 2:
            return
        elif err == 3:
            return
        else:                                             # エラーでない場合
            if com_str[0] in ["out", "set", "rst"]:       # 出力命令の場合
                for i in range(self.csr[0], self.row-1):  # 最終列手前まで繰り返し
                    self.lad.add_txt(self.csr, "ln")      # 導線命令登録
                    self.csr_move("Right")                # カーソル右へ
                self.lad.add_txt(self.csr, self.com_str)  # 命令登録
                self.csr_move("Right")                    # カーソル右へ
            elif com_str[0] == "brc":                     # 分岐命令の場合
                self.lad.add_txt(self.csr, self.com_str)  # 命令登録
            else:                                         # その他命令の場合
                self.lad.add_txt(self.csr, self.com_str)  # 命令登録
                self.csr_move("Right")                    # カーソル右へ
            self.com_dsp()
            self.com_str = ""
            self.com_num += 1

    # 命令入力取消
    def com_cn(self):
        print("cancel")
        self.com_frm.destroy()
        self.com_frm = None

    # 命令表示
    def com_dsp(self):
        self.cvs.delete("all")  # キャンバス全削除
        for i in range(self.row):                  # 列数繰り返し
            for j in range(len(self.lad.ladder)):  # 行数繰り返し
                if self.lad.ladder[j][i].typ == "Ln":
                    com_i = self.line
                elif self.lad.ladder[j][i].typ == "M":
                    com_i = self.make
                elif self.lad.ladder[j][i].typ == "B":
                    com_i = self.brek
                elif self.lad.ladder[j][i].typ == "P":
                    com_i = self.plse
                elif self.lad.ladder[j][i].typ == "F":
                    com_i = self.fall
                elif self.lad.ladder[j][i].typ in ["R", "T", "C"]:
                    com_i = self.base
                else:
                    com_i = None
                com_d = self.cvs.create_image(i*100+100, j*80+60, image=com_i)
                self.cvs.lower(com_d)
                if self.lad.ladder[j][i].brc == 1:
                    self.cvs.create_line(
                        i*100+50, j*80+59, i*100+50, j*80+142,
                        fill="black", width=3
                    )
                if self.lad.ladder[j][i].typ in self.lad.in_list:
                    self.cvs.create_text(
                        i*100+100, j*80+30,
                        text=self.lad.ladder[j][i].tag, font=("", 12, "bold")
                    )
                elif self.lad.ladder[j][i].typ in ["R", "T", "C"]:
                    self.cvs.create_text(
                        i*100+70, j*80+60, text=self.lad.ladder[j][i].tag,
                        font=("", 12, "bold"), anchor=tk.W
                    )
        self.cvs.create_line(50, 20, 50, 580, fill="black", width=3)  # 左側母線
        self.cvs.create_line(750, 20, 750, 580, fill="black", width=3)  # 右側母線
        self.cvs.create_rectangle(
            0, 0, 100, 80, tags="csr", outline="blue", width=3
        )
        self.cvs.moveto("csr", self.csr[0]*100+50, self.csr[1]*80+20)


# 命令入力ウインドウ
class InWin(tk.Frame):
    def __init__(self: tk.Tk, master):
        super().__init__(master)
        self.pack()

        # 定義
        self.frm = None
        self.ctyp = None

        # ウインドウの設定
        self.master.title(lg.ic)
        self.master.geometry("400x100")
        self.widgets()

    def widgets(self: tk.Tk):
        # フレームの設定
        self.frm = tk.Frame(self.master)
        self.frm.pack(fill=tk.BOTH, expand=True)

        # 命令タイプ
        ls = [lg.mk, lg.br, lg.rp, lg.fp, lg.ot]
        self.ctyp = ttk.Combobox(self.frm, values=ls)
        self.ctyp.pack(side=tk.LEFT)


# 実習盤ウインドウ
class PBWin(tk.Frame):
    def __init__(self: tk.Tk, master):
        super().__init__(master)  # 親クラスの継承
        self.pack()  # 配置

        # 定義
        self.cvs = None
        self.keep = []
        self.sw_on = []  # スイッチ情報
        self.out_on = []
        self.pall_x = 400  # 製品x座標
        self.pall_d = 0    # マウス移動用変数
        self.x = 350  # 位置調整用x座標
        self.y = 460  # 位置調整用y座標
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
        self.pb3n = tk.PhotoImage(file="image/PB3_ON.png")
        self.pb3f = tk.PhotoImage(file="image/PB3_OFF.png")
        self.pb4n = tk.PhotoImage(file="image/PB4_ON.png")
        self.pb4f = tk.PhotoImage(file="image/PB4_OFF.png")
        self.pb5n = tk.PhotoImage(file="image/PB5_ON.png")
        self.pb5f = tk.PhotoImage(file="image/PB5_OFF.png")
        self.pl1f = tk.PhotoImage(file="image/PL1_OFF.png")
        self.pl1n = tk.PhotoImage(file="image/PL1_ON.png")
        self.pl2f = tk.PhotoImage(file="image/PL2_OFF.png")
        self.pl2n = tk.PhotoImage(file="image/PL2_ON.png")
        self.pl3f = tk.PhotoImage(file="image/PL3_OFF.png")
        self.pl3n = tk.PhotoImage(file="image/PL3_ON.png")
        self.pl4f = tk.PhotoImage(file="image/PL4_OFF.png")
        self.pl4n = tk.PhotoImage(file="image/PL4_ON.png")
        self.pall = tk.PhotoImage(file="image/Pallet.png")
        self.prd1 = tk.PhotoImage(file="image/Product.png")
        self.prd2 = tk.PhotoImage(file="image/Product.png")
        self.prd3 = tk.PhotoImage(file="image/Product.png")
        self.prd4 = tk.PhotoImage(file="image/Product.png")

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
        # 切替スイッチ0
        self.cvs.create_image(90, 350, tags="ss0r", image=self.ss0r)
        self.cvs.create_image(90, 350, tags="ss0l", image=self.ss0l)
        self.cvs.create_text(88, 405, tags="ss0_t1", text="SS0 (z)", font=("", 12, "bold"))
        self.cvs.create_text(68, 295, tags="ss0_t2", text=lg.mn, font=("", 12, "bold"))
        self.cvs.create_text(117, 295, tags="ss0_t3", text=lg.at, font=("", 12, "bold"))
        self.cvs.create_text(92, 275, tags="ss0_t4", text=lg.md, font=("", 12, "bold"))

        # 切替スイッチ1
        self.cvs.create_image(200, 350, tags="ss1r", image=self.ss1r)
        self.cvs.create_image(200, 350, tags="ss1l", image=self.ss1l)
        self.cvs.create_text(200, 405, tags="ss1_t1", text="SS1 (x)", font=("", 12, "bold"))
        self.cvs.create_text(178, 295, tags="ss1_t2", text=lg.of, font=("", 12, "bold"))
        self.cvs.create_text(227, 295, tags="ss1_t3", text=lg.on, font=("", 12, "bold"))
        self.cvs.create_text(200, 275, tags="ss1_t4", text=lg.co, font=("", 12, "bold"))

        # 押しボタンスイッチ1
        self.cvs.create_image(350, 490, tags="pb1n", image=self.pb1n)
        self.cvs.create_image(350, 490, tags="pb1f", image=self.pb1f)

        # 押しボタンスイッチ2
        self.cvs.create_image(430, 490, tags="pb2n", image=self.pb2n)
        self.cvs.create_image(430, 490, tags="pb2f", image=self.pb2f)

        # 押しボタンスイッチ3
        self.cvs.create_image(510, 490, tags="pb3n", image=self.pb3n)
        self.cvs.create_image(510, 490, tags="pb3f", image=self.pb3f)

        # 押しボタンスイッチ4
        self.cvs.create_image(590, 490, tags="pb4n", image=self.pb4n)
        self.cvs.create_image(590, 490, tags="pb4f", image=self.pb4f)

        # 押しボタンスイッチ5
        self.cvs.create_image(700, 490, tags="pb5n", image=self.pb5n)
        self.cvs.create_image(700, 490, tags="pb5f", image=self.pb5f)

        # パイロットランプ1
        self.cvs.create_image(350, 370, tags="pl1n", image=self.pl1n)
        self.cvs.create_image(350, 370, tags="pl1f", image=self.pl1f)

        # パイロットランプ2
        self.cvs.create_image(430, 370, tags="pl2n", image=self.pl2n)
        self.cvs.create_image(430, 370, tags="pl2f", image=self.pl2f)

        # パイロットランプ3
        self.cvs.create_image(510, 370, tags="pl3n", image=self.pl3n)
        self.cvs.create_image(510, 370, tags="pl3f", image=self.pl3f)

        # パイロットランプ4
        self.cvs.create_image(590, 370, tags="pl4n", image=self.pl4n)
        self.cvs.create_image(590, 370, tags="pl4f", image=self.pl4f)

        # 製品
        self.cvs.create_image(self.pall_x, 120, tags="pall", image=self.pall)
        self.cvs.create_image(self.pall_x, 75, tags="prd1", image=self.prd1)
        self.cvs.create_image(self.pall_x, 105, tags="prd2", image=self.prd2)
        self.cvs.create_image(self.pall_x, 135, tags="prd3", image=self.prd3)
        self.cvs.create_image(self.pall_x, 165, tags="prd4", image=self.prd4)

        self.cvs.create_text(760, 590, tags="pt", text="x="+str(self.x)+", y="+str(self.y))
        self.cvs.create_text(760, 580, tags="ab", text="a="+str(self.a)+", b="+str(self.b))

    # イベント
    def event(self):
        def m_press(e):
            if e.num == 1:
                if self.pall_x-80 < e.x < self.pall_x+80:  # パレット移動
                    if 60 < e.y < 180:
                        self.keep.append("prod")
                        self.pall_d = self.pall_x - e.x
                if self.pall_x-15 < e.x < self.pall_x+15:  # 製品選択
                    if 60 < e.y < 90:
                        if "prd1" in self.keep:
                            self.keep.remove("prd1")
                            self.cvs.lift("prd1", "pall")   # tk.Canvas.lift(前面に移動させたいタグ)
                        else:
                            self.keep.append("prd1")
                            self.cvs.lower("prd1", "pall")  # tk.Canvas.lower(背面に移動させたいタグ)
                    elif 90 < e.y < 120:
                        if "prd2" in self.keep:
                            self.keep.remove("prd2")
                            self.cvs.lift("prd2", "pall")
                        else:
                            self.keep.append("prd2")
                            self.cvs.lower("prd2", "pall")
                    elif 120 < e.y < 150:
                        if "prd3" in self.keep:
                            self.keep.remove("prd3")
                            self.cvs.lift("prd3", "pall")
                        else:
                            self.keep.append("prd3")
                            self.cvs.lower("prd3", "pall")
                if 310 < e.y < 390:  # 切替スイッチ
                    if 50 < e.x < 130:  # 切替スイッチ0
                        self.sw_func("SS0", 0)
                    elif 160 < e.x < 240:  # 切替スイッチ1
                        self.sw_func("SS1", 0)
                elif 460 < e.y < 520:  # 押しボタンスイッチ
                    if 320 < e.x < 380:
                        self.sw_func("PB1", 2)
                    elif 400 < e.x < 460:
                        self.sw_func("PB2", 2)
                    elif 480 < e.x < 540:
                        self.sw_func("PB3", 2)
                    elif 560 < e.x < 620:
                        self.sw_func("PB4", 2)
                if 450 < e.y < 530:  # 押しボタンスイッチ5
                    if 660 < e.x < 740:
                        self.sw_func("PB5", 2)

                print("x=" + str(e.x) + ", y=" + str(e.y))
                # 要素の設定変更 https://daeudaeu.com/tkinter_canvas_method/
            if e.num == 3:
                pass

        def m_release(e):
            if e.num == 1:
                if "prod" in self.keep:
                    self.keep.remove("prod")
                if "PB1" in self.sw_on:
                    self.sw_func("PB1", 1)
                elif "PB2" in self.sw_on:
                    self.sw_func("PB2", 1)
                elif "PB3" in self.sw_on:
                    self.sw_func("PB3", 1)
                elif "PB4" in self.sw_on:
                    self.sw_func("PB4", 1)
                elif "PB5" in self.sw_on:
                    self.sw_func("PB5", 1)
            if e.num == 3:
                pass

        def m_move(e):
            if "prod" in self.keep:
                if 150 < e.x+self.pall_d < 650:
                    self.pall_x = e.x + self.pall_d
                    self.cvs.moveto("pall", x=self.pall_x-80, y=60)
                    self.cvs.moveto("prd1", x=self.pall_x-15, y=60)
                    self.cvs.moveto("prd2", x=self.pall_x-15, y=90)
                    self.cvs.moveto("prd3", x=self.pall_x-15, y=120)
                    self.cvs.moveto("prd4", x=self.pall_x-15, y=150)

        def k_press(e):
            if e.keysym in self.keep:
                return
            self.keep.append(e.keysym)
            if e.keysym == "c":
                self.cvs.lift("pl1n", "pl1f")
                self.cvs.lift("pl2n", "pl2f")
                self.cvs.lift("pl3n", "pl3f")
                self.cvs.lift("pl4n", "pl4f")
            if e.keysym == "z":
                self.sw_func("SS0", 0)
            if e.keysym == "x":
                self.sw_func("SS1", 0)
            if e.keysym == "v":
                self.sw_func("PB1", 2)
            if e.keysym == "b":
                self.sw_func("PB2", 2)
            if e.keysym == "n":
                self.sw_func("PB3", 2)
            if e.keysym == "m":
                self.sw_func("PB4", 2)
            if e.keysym == "space":
                self.sw_func("PB5", 2)
            if e.keysym == "Right":
                self.x += 2
            if e.keysym == "Left":
                self.x -= 2
            if e.keysym == "Down":
                self.y += 2
            if e.keysym == "Up":
                self.y -= 2
            # self.cvs.moveto("pt", x=self.x, y=self.y)
            # self.cvs.moveto("pb2f", x=self.x, y=self.y)
            self.cvs.itemconfig("pt", text="x="+str(self.x)+", y="+str(self.y))

        def k_release(e):
            self.keep.remove(e.keysym)
            if e.keysym == "c":
                self.cvs.lift("pl1f", "pl1n")
                self.cvs.lift("pl2f", "pl2n")
                self.cvs.lift("pl3f", "pl3n")
                self.cvs.lift("pl4f", "pl4n")
            if e.keysym == "v":
                self.sw_func("PB1", 1)
            if e.keysym == "b":
                self.sw_func("PB2", 1)
            if e.keysym == "n":
                self.sw_func("PB3", 1)
            if e.keysym == "m":
                self.sw_func("PB4", 1)
            if e.keysym == "space":
                self.sw_func("PB5", 1)

        self.master.bind("<ButtonPress>", m_press)
        self.master.bind("<ButtonRelease>", m_release)
        self.master.bind("<Motion>", m_move)
        self.master.bind("<KeyPress>", k_press)
        self.master.bind("<KeyRelease>", k_release)

    # スイッチ動作
    def sw_func(self, tag, p):
        if p == 0:
            if tag in self.sw_on:  # ONからOFFへ
                if tag == "SS0":
                    self.cvs.lift("ss0l", "ss0r")
                elif tag == "SS1":
                    self.cvs.lift("ss1l", "ss1r")
                self.sw_on.remove(tag)
            else:                  # OFFからONへ
                if tag == "SS0":
                    self.cvs.lift("ss0r", "ss0l")
                elif tag == "SS1":
                    self.cvs.lift("ss1r", "ss1l")
                self.sw_on.append(tag)
        else:
            if p == 1:    # ONからOFFへ
                if tag == "PB1":
                    self.cvs.lift("pb1f", "pb1n")
                elif tag == "PB2":
                    self.cvs.lift("pb2f", "pb2n")
                elif tag == "PB3":
                    self.cvs.lift("pb3f", "pb3n")
                elif tag == "PB4":
                    self.cvs.lift("pb4f", "pb4n")
                elif tag == "PB5":
                    self.cvs.lift("pb5f", "pb5n")
                else:
                    return
                self.sw_on.remove(tag)
            elif p == 2:  # OFFからONへ
                if tag == "PB1":
                    self.cvs.lift("pb1n", "pb1f")
                elif tag == "PB2":
                    self.cvs.lift("pb2n", "pb2f")
                elif tag == "PB3":
                    self.cvs.lift("pb3n", "pb3f")
                elif tag == "PB4":
                    self.cvs.lift("pb4n", "pb4f")
                elif tag == "PB5":
                    self.cvs.lift("pb5n", "pb5f")
                else:
                    return
                self.sw_on.append(tag)

    # 出力動作
    def out_func(self):
        if "PL1" in self.out_on:
            self.cvs.lift("pl1n", "pl1f")
        else:
            self.cvs.lift("pl1f", "pl1n")
        if "PL2" in self.out_on:
            self.cvs.lift("pl2n", "pl2f")
        else:
            self.cvs.lift("pl2f", "pl2n")
        if "PL3" in self.out_on:
            self.cvs.lift("pl3n", "pl3f")
        else:
            self.cvs.lift("pl3f", "pl3n")
        if "PL4" in self.out_on:
            self.cvs.lift("pl4n", "pl4f")
        else:
            self.cvs.lift("pl4f", "pl4n")
        if "RY1" in self.out_on:
            pass
        else:
            pass
        if "RY2" in self.out_on:
            pass
        else:
            pass


# 割付表ウインドウ
class IOWin(tk.Frame):
    def __init__(self: tk.Tk, master, lst):
        super().__init__(master)
        self.pack()

        # 定義
        self.frm = tk.Frame(self.master)
        self.io_st = lst
        self.io_list = []
        self.keep = []

        # ウインドウの設定
        self.master.title(lg.io)
        self.master.geometry("400x600")
        self.widgets()
        self.event()

    # ウィジェット
    def widgets(self: tk.Tk):
        # フレームの設定
        self.frm.pack(fill=tk.BOTH, expand=True)

        # 表形状の入力欄
        x = [15, 100, 215, 300]
        print(len(self.io_st))
        for i in range(len(self.io_st)):
            row = []
            for j in range(4):
                row.append(tk.Entry(self.frm, font=("", 14), width=8))
                row[-1].insert(0, self.io_st[i][j])
                if j in [1, 3]:
                    row[-1].configure(state="readonly")
                row[-1].place(x=x[j], y=i*25+45)
            self.io_list.append(row)

        # 完了ボタン
        ok_b = tk.Button(self.frm, text=lg.ok, width=8, command=self.com_ok)
        cn_b = tk.Button(self.frm, text=lg.cn, width=8, command=self.com_cn)
        ok_b.place(x=235, y=560)
        cn_b.place(x=315, y=560)

        # テスト入力
        self.io_list[2][0].delete(0, 8)
        self.io_list[2][0].insert(0, "x0")
        self.io_list[3][0].delete(0, 8)
        self.io_list[3][0].insert(0, "x1")
        self.io_list[2][2].delete(0, 8)
        self.io_list[2][2].insert(0, "y0")
        self.dev_type("pb")

    # イベント
    def event(self):
        def k_press(e):
            if e.keysym in self.keep:
                return
            print(e.keysym)
            self.keep.append(e.keysym)
            if e.keysym == "k":
                self.dev_type("pb")

        def k_release(e):
            if e.keysym in self.keep:
                self.keep.remove(e.keysym)

        self.master.bind("<KeyPress>", k_press)
        self.master.bind("<KeyRelease>", k_release)

    # 割付決定
    def com_ok(self):
        for i in range(len(self.io_st)):
            for j in range(4):
                self.io_st[i][j] = self.io_list[i][j].get()
        self.master.destroy()

    # 割付取消
    def com_cn(self):
        self.master.destroy()

    # 機器側書き込み
    def dev_type(self, typ):
        pb_i = ["LS1", "LS2", "PB1", "PB2", "PB3", "PB4", "PB5", "SS0", "SS1", ""]
        pb_o = ["RY1", "RY2", "PL1", "PL2", "PL3", "PL4", "", "", "", ""]
        tl_i = ["", "", "", "", "", "", "", "", "", ""]
        tl_o = ["", "", "", "", "", "", "", "", "", ""]
        for i in range(len(self.io_st)):                   # 行数繰り返し
            self.io_list[i][1].configure(state="normal")   # 機器側入力書き込みモード
            self.io_list[i][3].configure(state="normal")   # 機器側出力書き込みモード
            self.io_list[i][1].delete(0, 8)                # 入力してあるもの削除
            self.io_list[i][3].delete(0, 8)                # 入力してあるもの削除
            if typ == "pb":                                # 実習盤の場合
                if i < len(pb_i):                          # 配列の要素内の場合
                    self.io_list[i][1].insert(0, pb_i[i])  # 機器側入力書き込み
                if i < len(pb_o):                          # 配列の要素内の場合
                    self.io_list[i][3].insert(0, pb_o[i])  # 機器側出力書き込み
            elif typ == "tl":                              # 信号機の場合
                if i < len(tl_i):
                    self.io_list[i][1].insert(0, tl_i[i])
                if i < len(tl_o):
                    self.io_list[i][3].insert(0, tl_o[i])
            self.io_list[i][1].configure(state="readonly")  # 機器側入力書き込み禁止
            self.io_list[i][3].configure(state="readonly")  # 機器側出力書き込み禁止


# アプリケーション
def application():
    root = tk.Tk()  # Tkinterインスタンスの生成
    app = MainWin(master=root)  # アプリケーション実行
    app.mainloop()  # ウインドウの描画
