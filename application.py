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
        self.row = 9  # 列数
        self.csr = [0, 0]  # 画面上カーソル座標
        self.scr = [0, 0, 0]  # スクロールバー座標(上座標, 長さ, 画面上座標)
        self.scr_d = 0     # スクロールバー移動用変数
        self.keep = []
        self.lad = ld.Ladder(self.row)
        self.com_frm = None  # 命令入力フレーム
        self.com_ent = None  # 命令入力欄
        self.com_str = ""  # 命令入力文字列
        self.com_num = 0  # 命令数
        self.io_list = []
        self.run = 0
        self.run_tag = []
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
        self.file.add_command(label=lg.op, command=self.open)     # 開く
        self.file.add_separator()                                 # 境界線
        self.file.add_command(label=lg.sv, command=self.save)     # 上書き保存
        self.file.add_separator()                                 # 境界線
        self.file.add_command(label=lg.sa)                        # 名前を付けて保存
        self.file.add_separator()                                 # 境界線
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
        self.cvs.pack(fill=tk.BOTH, expand=True)  # キャンバス配置
        self.csr_move()                           # カーソル設定
        self.scr_move()                           # スクロールバー設定
        self.com_dsp()                            # 画面に表示

    # 開く
    def open(self):
        f = open("test.sqe", "r", newline="")
        while True:
            s = repr(f.readline())[1:-1]
            # print(s)
            if s == "end\\n":
                break
            c = s.split()
            for i in range(self.row):
                xy = [int(c[6*i]), int(c[6*i+1])]
                brc = int(c[6*i+3])
                typ = c[6*i+2]
                tag = c[6*i+4]
                set = int(c[6*i+5])
                self.lad.add_com(xy, brc, typ, tag, set)
        i = 0
        while True:
            s = repr(f.readline())[1:-1]
            # print(s)
            if s == "end":
                break
            c = s.split()
            for j in range(4):
                # print("c[j] = " + c[j])
                if c[j] == "none":
                    self.io_list[i][j] = ""
                else:
                    self.io_list[i][j] = c[j]
            i += 1
        # print(self.io_list)
        f.close()
        self.scr_move()
        self.com_dsp()

    # 上書き保存
    def save(self):
        f = open("test.sqe", "w", newline="")
        for i in range(len(self.lad.ladder)):
            for j in range(self.row):
                f.write(str(j) + " ")
                f.write(str(i) + " ")
                f.write(self.lad.ladder[i][j].typ + " ")
                f.write(str(self.lad.ladder[i][j].brc) + " ")
                f.write(self.lad.ladder[i][j].tag + " ")
                f.write(str(self.lad.ladder[i][j].set) + " ")
            f.write("\n")
        f.writelines("end\n")
        for i in range(len(self.io_list)):
            for j in range(4):
                if self.io_list[i][j] == "":
                    f.write("none ")
                else:
                    f.write(self.io_list[i][j] + " ")
            f.write("\n")
        f.writelines("end")

        f.close()

    # 終了
    def exit(self):
        self.master.destroy()

    # シミュレーション開始
    def sm_run(self):
        if self.run == 0:   # 呼び出された初回の場合
            self.run = 1    # 実行フラグON
            self.lad.org()  # プログラム整理
            self.com_dsp()  # プログラム表示
        if self.run == 1:   # 実行中の場合
            for i in range(len(self.run_tag)):  # 出力の記号の数繰り返し
                self.cvs.delete(self.run_tag[i])  # 出力の記号削除
            self.run_tag = []
            # print("run")
            sw_on = []      # 入力
            if self.pb_app is not None:                          # 実習盤が表示されている場合
                for i in range(len(self.io_list)):               # 割付表の行数繰り返し
                    if self.io_list[i][1] in self.pb_app.sw_on:  # スイッチONリストにある場合
                        sw_on.append(self.io_list[i][0])         # 外部入力ONリストに追加
                        
            self.lad.change("x", 0, 1)         # スイッチの入力初期化
            for i in range(len(sw_on)):     # スイッチONリスト数繰り返し
                self.lad.change(sw_on[i], 1)   # スイッチON
            
            self.lad.run()  # ラダープログラム実行

            if self.pb_mas is None:               # 実習盤インスタンスがない場合
                pass
            elif not self.pb_mas.winfo_exists():  # 実習盤が表示されていない場合
                pass
            else:                                 # その他、実習盤に反映
                out_on = []  # 出力リストリセット
                for i in range(len(self.io_list)):  # 割付表の行数繰り返し
                    for j in range(len(self.lad.ladder)):  # ラダー図行数繰り返し
                        if self.io_list[i][2] == self.lad.ladder[j][-1].tag:  # ラダー図の変数が割付表にある場合
                            if self.lad.ladder[j][-1].opt == 1:  # ラダー図の変数がON出力の場合
                                out_on.append(self.io_list[i][3])  # 出力リストに追加
                                # print(out_on)
                self.pb_app.out_func(out_on)  # 実習盤出力

            for i in range(len(self.lad.ladder)):
                for j in range(self.row):
                    if self.lad.ladder[i][j].opt == 1:
                        self.cvs.create_rectangle(
                            j*80+71, i*60+40-self.scr[2], j*80+90, i*60+61-self.scr[2],
                            tags="on"+str(i)+str(j), fill="blue", width=0
                        )
                        self.run_tag.append("on"+str(i)+str(j))
                
            self.master.after(10, self.sm_run)  # 1000ms後に実行
        else:
            self.run = 0
            return

    # シミュレーション終了
    def sm_stop(self):
        for i in range(len(self.run_tag)):
            self.cvs.delete(self.run_tag[i])
        self.run_tag = []
        self.run = 9

    # 命令入力ウインドウ表示
    def in_win(self):
        if self.in_mas is None:
            self.in_mas = tk.Toplevel(self.master)
            self.in_app = InWin(self.in_mas)
        elif not self.in_mas.winfo_exists():
            self.in_mas = tk.Toplevel(self.master)
            self.in_app = InWin(self.in_mas)

    # 実習盤ウインドウ表示
    def pb_win(self):
        if self.pb_mas is None:
            self.pb_mas = tk.Toplevel(self.master)
            self.pb_app = PBWin(self.pb_mas)
        elif not self.pb_mas.winfo_exists():
            self.pb_mas = tk.Toplevel(self.master)
            self.pb_app = PBWin(self.pb_mas)

    # 割付表ウインドウ表示
    def io_win(self):
        if self.io_mas is None:
            self.io_mas = tk.Toplevel(self.master)
            self.io_app = IOWin(self.io_mas, self.io_list)
        elif not self.io_mas.winfo_exists():
            self.io_mas = tk.Toplevel(self.master)
            self.io_app = IOWin(self.io_mas, self.io_list)

    # イベント
    def event(self):
        def m_press(e):
            if e.num == 1:
                if self.com_frm is None:
                    if 40 < e.x < 760:
                        if 20 < e.y < 560:
                            self.csr[0] = (e.x - 38) // 80
                            self.csr[1] = (e.y - 20 + self.scr[2]) // 60
                            self.csr_move()  # カーソル移動
                            self.scr_move()  # スクロールバー移動
                            self.com_dsp()   # 移動反映
                    if 780 < e.x < 800:
                        if self.scr[0] < e.y < self.scr[0]+self.scr[1]:
                            self.keep.append("scr")
                            self.scr_d = e.y - self.scr[0]
            elif e.num == 3:
                print(self.pb_mas)
                print(self.pb_app)

        def m_release(e):
            if e.num == 1:
                if "scr" in self.keep:
                    self.keep.remove("scr")

        def mm_press(e):
            if e.num == 1:  # マウス左ダブルクリック
                if self.com_frm is None:
                    if 50 < e.x < 750:
                        if 20 < e.y < 580:
                            self.com_input()  # 命令入力

        def m_move(e):
            if "scr" in self.keep:
                scr_y = e.y - self.scr_d
                if scr_y >= 0:
                    if scr_y+self.scr[1] <= 600:
                        self.scr[0] = scr_y
                        self.scr_move()
                        self.com_dsp()

        def k_press(e):
            if e.keysym in self.keep:
                return
            self.keep.append(e.keysym)
            # print(e.keysym)
            if e.keysym in ["Shift_L", "Shift_R"]:
                self.keep.append("Shift")
            if e.keysym in ["Control_L", "Control_R"]:
                self.keep.append("Control")
            if e.keysym in ["b", "e", "i", "l", "o", "r", "s", ]:
                if self.com_frm is None:
                    self.com_input(e.keysym)
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
            if e.keysym == "space":
                if self.run == 1:
                    self.sm_run()
            if e.keysym == "BackSpace":
                if self.com_frm is None:
                    self.csr_move("Left")
                    if self.csr[1] < self.row-1:
                        self.lad.add_txt(self.csr, "bl")
                    else:
                        self.lad.add_txt(self.csr, "ent")
                    self.com_dsp(0)
            if e.keysym == "Delete":
                if self.csr[1] < self.row - 1:
                    self.lad.add_txt(self.csr, "bl")
                else:
                    self.lad.add_txt(self.csr, "ent")
                self.com_dsp(0)
            if e.keysym == "z":
                if self.com_frm is None:
                    if "Control" in self.keep:
                        print("back")
            if e.keysym == "Up":
                if self.com_frm is None:
                    self.csr_move("Up")
                    if "Control" in self.keep:
                        self.lad.add_pls([self.csr[0], self.csr[1]])
                        if self.lad.ladder[self.csr[1]][self.csr[0]].brc == 1:  # 分岐ある場合
                            self.lad.ladder[self.csr[1]][self.csr[0]].brc = 0   # 分岐消去
                        else:                                                   # 分岐ない場合
                            self.lad.ladder[self.csr[1]][self.csr[0]].brc = 1   # 分岐追加
                    self.com_dsp()
            if e.keysym == "Down":
                if self.com_frm is None:
                    if "Control" in self.keep:
                        self.lad.add_pls([self.csr[0], self.csr[1]])
                        if self.lad.ladder[self.csr[1]][self.csr[0]].brc == 1:  # 分岐ある場合
                            self.lad.ladder[self.csr[1]][self.csr[0]].brc = 0   # 分岐消去
                        else:                                                   # 分岐ない場合
                            self.lad.ladder[self.csr[1]][self.csr[0]].brc = 1   # 分岐追加
                    self.csr_move("Down")
                    self.com_dsp()
            if e.keysym == "Left":
                if self.com_frm is None:
                    self.csr_move("Left")
                    if "Control" in self.keep:
                        self.lad.add_pls([self.csr[0], self.csr[1]])
                        if self.lad.ladder[self.csr[1]][self.csr[0]].typ == "Ln":
                            self.lad.ladder[self.csr[1]][self.csr[0]].typ = "Bl"
                        elif self.lad.ladder[self.csr[1]][self.csr[0]].typ == "Bl":
                            self.lad.ladder[self.csr[1]][self.csr[0]].typ = "Ln"
                    self.com_dsp()
            if e.keysym == "Right":
                if self.com_frm is None:
                    if "Control" in self.keep:
                        self.lad.add_pls([self.csr[0], self.csr[1]])
                        if self.lad.ladder[self.csr[1]][self.csr[0]].typ == "Ln":
                            self.lad.ladder[self.csr[1]][self.csr[0]].typ = "Bl"
                        elif self.lad.ladder[self.csr[1]][self.csr[0]].typ == "Bl":
                            self.lad.ladder[self.csr[1]][self.csr[0]].typ = "Ln"
                    self.csr_move("Right")
                    self.com_dsp()

        def k_release(e):
            if e.keysym in self.keep:
                self.keep.remove(e.keysym)
            if e.keysym in ["Shift_L", "Shift_R"]:
                if "Shift" in self.keep:
                    self.keep.remove("Shift")
            if e.keysym in ["Control_L", "Control_R"]:
                if "Control" in self.keep:
                    self.keep.remove("Control")

        self.master.bind("<ButtonPress>", m_press)
        self.master.bind("<ButtonRelease>", m_release)
        self.master.bind("<Double-ButtonPress>", mm_press)
        self.master.bind("<Motion>", m_move)
        self.master.bind("<KeyPress>", k_press)
        self.master.bind("<KeyRelease>", k_release)

    # カーソル移動
    def csr_move(self, d=""):
        if d == "Right":
            if self.csr[0] < self.row-1:
                self.csr[0] += 1
            else:
                self.csr[0] = 0
                self.csr[1] += 1
            self.scr_move(1, "Down")
        elif d == "Left":
            if self.csr[0] > 0:
                self.csr[0] -= 1
            else:
                if self.csr[1] > 0:
                    self.csr[0] = self.row - 1
                    self.csr[1] -= 1
            self.scr_move(1, "Up")
        elif d == "Down":
            self.csr[1] += 1
            self.scr_move(1, "Down")
        elif d == "Up":
            if self.csr[1] > 0:
                self.csr[1] -= 1
                self.scr_move(1, "Up")

        # csr_y = self.csr[1]*60+20-self.scr[2]
        # if csr_y < 20:
        #     self.scr[1] = 5400 // max(len(self.lad.ladder), self.csr[1] + 1)  # スクロールバー長さ
        #     col = max(len(self.lad.ladder), self.csr[1]+1)
        #     self.scr[0] -= (600 - self.scr[1]) // (col - 9)  # スクロールバー上へ
        # elif csr_y > 520:
        #     self.scr[1] = 5400 // max(len(self.lad.ladder), self.csr[1] + 1)  # スクロールバー長さ
        #     col = max(len(self.lad.ladder), self.csr[1]+1)
        #     self.scr[0] += (600 - self.scr[1]) // (col - 9)  # スクロールバー下へ
        # self.cvs.moveto("csr", self.csr[0]*80+38, csr_y)

    # スクロールバー移動
    def scr_move(self, key=0, d=""):
        col = max(len(self.lad.ladder), self.csr[1]+1)  # プログラム列数
        self.scr[1] = 5400 // col  # スクロールバー長さ変更
        if self.scr[1] >= 600:
            self.scr[0] = 0
            self.scr[1] = 600
            self.scr[2] = 0
        else:
            if key == 1:                                     # キー入力の場合
                csr_y = self.csr[1] * 60 + 20 - self.scr[2]  # 画面上カーソル座標
                if csr_y < 20:                               # カーソルが画面上側に外れた場合
                    self.scr[2] = self.csr[1] * 60           # 画面スクロール
                    num = (600 - self.scr[1]) * self.scr[2]  # バー位置求める式分子
                    den = (col - 9) * 60                     # バー位置求める式分母
                    self.scr[0] = num // den                 # スクロールバー位置
                elif csr_y > 500:                            # カーソルが画面下側に外れた場合
                    self.scr[2] = self.csr[1] * 60 - 500     # 画面スクロール
                    num = (600 - self.scr[1]) * self.scr[2]  # バー位置求める式分子
                    den = (col - 9) * 60                     # バー位置求める式分母
                    self.scr[0] = num // den                 # スクロールバー位置
            # if d == "Down":
            #     self.scr[2] += 60
            #     num = (600 - self.scr[1]) * self.scr[2]  # バー位置求める式分子
            #     den = (col - 9) * 60                     # バー位置求める式分母
            #     self.scr[0] = num // den                 # スクロールバー位置
            # elif d == "Up":
            #     self.scr[2] -= 60
            #     num = (600 - self.scr[1]) * self.scr[2]  # バー位置求める式分子
            #     den = (col - 9) * 60                     # バー位置求める式分母
            #     self.scr[0] = num // den                 # スクロールバー位置
            else:
                num = self.scr[0] * (col - 9) * 60  # 移動量求める分子
                den = 600 - self.scr[1]             # 移動量求める分母
                self.scr[2] = num // den            # スクロール移動量

    # 命令入力
    def com_input(self, a=""):
        self.com_frm = tk.Frame(  # 入力フレーム追加
            self.cvs, width=300, height=120,
            relief=tk.RIDGE, bd=2
        )
        ti_l = tk.Label(self.com_frm, text=lg.ic)  # テキスト追加
        self.com_ent = tk.Entry(self.com_frm, font=("", 14), width=27)  # 入力欄追加
        self.com_ent.insert(0, a)                                       # 押したキー入力
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
            elif com_str[0] == "ins":
                self.lad.ins_rc([self.csr[0], self.csr[1]], com_str[1])
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
    def com_dsp(self, y=0):
        self.cvs.delete("all")  # キャンバス全削除
        for i in range(len(self.lad.ladder)):          # 行数繰り返し
            for j in range(self.row):                  # 列数繰り返し
                if self.lad.ladder[i][j].typ == "Ln":
                    com_i = self.line
                elif self.lad.ladder[i][j].typ == "M":
                    com_i = self.make
                elif self.lad.ladder[i][j].typ == "B":
                    com_i = self.brek
                elif self.lad.ladder[i][j].typ == "P":
                    com_i = self.plse
                elif self.lad.ladder[i][j].typ == "F":
                    com_i = self.fall
                elif self.lad.ladder[i][j].typ in ["R", "T", "C"]:
                    com_i = self.base
                else:
                    com_i = None
                com_d = self.cvs.create_image(
                    j*80+80, i*60+50-self.scr[2], image=com_i
                )
                self.cvs.lower(com_d)
                if self.lad.ladder[i][j].brc == 1:
                    self.cvs.create_line(
                        j*80+40, i*60+50-self.scr[2],
                        j*80+40, i*60+112-self.scr[2],
                        fill="black", width=2
                    )
                if self.lad.ladder[i][j].typ in self.lad.in_list:
                    if self.lad.ladder[i][j].typ != "Ln":
                        self.cvs.create_text(
                            j*80+80, i*60+30-self.scr[2],
                            text=self.lad.ladder[i][j].tag, font=("", 12, "bold")
                        )
                elif self.lad.ladder[i][j].typ in ["R", "T", "C"]:
                    self.cvs.create_text(
                        j*80+55, i*60+50-self.scr[2], 
                        text=self.lad.ladder[i][j].tag, font=("", 12, "bold"), anchor=tk.W
                    )
        self.cvs.create_line(40, 20, 40, 580, fill="black", width=2)  # 左側母線
        self.cvs.create_line(760, 20, 760, 580, fill="black", width=2)  # 右側母線

        # カーソル
        self.cvs.create_rectangle(
            0, 0, 80, 60, tags="csr", outline="blue", width=3
        )
        self.cvs.moveto("csr", self.csr[0]*80+38, self.csr[1]*60+20-self.scr[2])
        # self.csr_move()

        # スクロールバー
        self.cvs.create_rectangle(
            0, 0, 10, 100, tags="scr", fill="silver", width=0
        )
        self.cvs.coords("scr", 780, self.scr[0], 800, self.scr[0]+self.scr[1])
        # self.scr_move()


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

                # print("x=" + str(e.x) + ", y=" + str(e.y))
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
                self.pall_func(x=e.x + self.pall_d)

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

    # パレット動作
    def pall_func(self, x=None, d=None):
        pall_x = self.pall_x  # ローカル変数に代入
        if x is not None:     # 座尿から移動させる場合
            pall_x = x        # 座標を代入
        elif d is not None:   # 変位から移動させる場合
            pall_x += d         # 変位から座標を計算
        if 150 < pall_x < 650:  # 端でない場合
            self.pall_x = pall_x  # グローバル変数に代入
            ls_list = ["LS1", "LS2", "LS3", "LS4", "LS5"]
            for i in range(5):
                if ls_list[i] in self.sw_on:
                    self.sw_on.remove(ls_list[i])  # スイッチOFF
        elif pall_x >= 650:  # 右端の場合
            self.pall_x = 650
            if "LS1" not in self.sw_on:
                self.sw_on.append("LS1")
        elif pall_x <= 150:  # 左端の場合
            self.pall_x = 150
            if "LS2" not in self.sw_on:
                self.sw_on.append("LS2")
            if "LS3" not in self.sw_on:
                if "prd1" not in self.keep:
                    self.sw_on.append("LS3")
            if "LS4" not in self.sw_on:
                if "prd2" not in self.keep:
                    self.sw_on.append("LS4")
            if "LS5" not in self.sw_on:
                if "prd3" not in self.keep:
                    self.sw_on.append("LS5")
        self.cvs.moveto("pall", x=self.pall_x-80, y=60)
        self.cvs.moveto("prd1", x=self.pall_x-15, y=60)
        self.cvs.moveto("prd2", x=self.pall_x-15, y=90)
        self.cvs.moveto("prd3", x=self.pall_x-15, y=120)
        self.cvs.moveto("prd4", x=self.pall_x-15, y=150)

    # 出力動作
    def out_func(self, on):
        if "PL1" in on:
            self.cvs.lift("pl1n", "pl1f")
        else:
            self.cvs.lift("pl1f", "pl1n")
        if "PL2" in on:
            self.cvs.lift("pl2n", "pl2f")
        else:
            self.cvs.lift("pl2f", "pl2n")
        if "PL3" in on:
            self.cvs.lift("pl3n", "pl3f")
        else:
            self.cvs.lift("pl3f", "pl3n")
        if "PL4" in on:
            self.cvs.lift("pl4n", "pl4f")
        else:
            self.cvs.lift("pl4f", "pl4n")
        if "RY1" in on:
            self.pall_func(d=-1)
        else:
            pass
        if "RY2" in on:
            self.pall_func(d=1)
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
        # self.io_list[2][0].delete(0, 8)
        # self.io_list[2][0].insert(0, "x0")
        # self.io_list[3][0].delete(0, 8)
        # self.io_list[3][0].insert(0, "x1")
        # self.io_list[2][2].delete(0, 8)
        # self.io_list[2][2].insert(0, "y0")
        # self.dev_type("pb")

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
