class Ladder:
    tag_list = ["M", "B", "P", "F", "R", "T", "C", "St", "Rs"]  # 名付命令リスト
    in_list = ["M", "B", "P", "F", "Ln"]  # 入力命令リスト
    out_list = ["R", "T", "C", "St"]  # 出力命令リスト(リセット命令以外)
    end_list = ["R", "T", "C", "St", "Rs", "En"]  # 改行命令リスト

    def __init__(self):
        self.row = []     # 1行のラダープログラム
        self.ladder = []  # 全体のラダープログラム

    class Comp:
        def __init__(self, typ, brc):
            self.typ = typ   # 命令タイプ
            self.brc = brc   # 分岐
            self.tag = ""    # 名前
            self.set = 0     # 設定値
            self.ext = 0     # 外部入力
            self.opt = 0     # 出力
            self.c = 0       # カウント現在値
            self.lst = 0     # 前回値

        def dec(self, st):
            com = st.split()
            if com[0] == "ld":
                self.typ = "M"
            elif com[0] == "ldi":
                self.typ = "B"
            elif com[0] == "ldp":
                self.typ = "P"
            elif com[0] == "ldf":
                self.typ = "F"
            elif com[0] == "out":
                if com[1][0] in ["m", "y"]:
                    self.typ = "R"
                elif com[1][0] == "t":
                    self.typ = "T"
                elif com[1][0] == "c":
                    self.typ = "C"
                else:
                    print("No Command")
                    return 3  # コイルの種類が不明
            elif com[0] == "set":
                self.typ = "St"
            elif com[0] == "rst":
                self.typ = "Rs"
            else:
                print("No Command")
                return 1  # 命令タイプがない
            if self.typ in Ladder.tag_list:
                self.tag = com[1]
            try:
                if self.typ in ["T", "C"]:
                    self.set = int(com[2][1:])
            except IndexError:
                print("Index Error")
                return 2  # 設定値がない
            return 0

        def cal(self, ipt):
            if self.typ == "Ln":  # 導線命令
                self.opt = ipt
            elif self.typ == "M":  # a接点入力命令
                self.opt = ipt * self.ext
            elif self.typ == "B":  # b接点入力命令
                self.opt = ipt * abs(self.ext - 1)
            elif self.typ in Ladder.out_list:  # 出力命令
                if self.opt == 0:
                    self.opt = ipt
            elif self.typ == "Rs":  # リセット命令
                if self.opt == 0:
                    self.opt = ipt
            return self.opt

        def out(self):
            if self.typ == "T":                # タイマ出力命令の場合
                if self.opt == 1:              # 入力がONの場合
                    if self.lst == 0:          # 前回の出力がOFFの場合
                        self.c += 1            # カウントアップ
                        if self.c < self.set:  # 設定値に届いていない場合
                            self.opt = 0       # 出力OFF
                else:                          # 入力がOFFの場合
                    self.c = 0                 # カウントリセット
                self.lst = self.opt            # 前回値更新
            if self.typ == "C":                # カウンタ出力命令の場合
                pass                           #
            if self.typ == "St":               # セット命令の場合
                if self.ext+self.opt > 0:      # 前回出力ONまたはセット命令ONの場合
                    self.opt = 1               # 出力ON
                else:                          # 前回出力OFFかつセット命令OFFの場合
                    self.opt = 0               # 出力OFF

    def add(self, typ, brc, tag="", set=0):
        self.row.append(self.Comp(typ, brc))  # 行に追加
        if typ in self.tag_list:              # 名付命令の場合
            self.row[-1].tag = tag            # 名前を登録
        if typ in ["T", "C"]:                 # 設定値のある命令の場合
            self.row[-1].set = set            # 設定値を登録
        if typ in self.end_list:              # 改行命令の場合
            self.ladder.append(self.row)      # 行を全体に追加
            self.row = []                     # 行を初期化

    def change(self, tag, ext=None):
        for i in range(len(self.ladder)):  # 行数繰り返し
            for j in range(len(self.ladder[i])):  # 列数繰り返し
                if tag == self.ladder[i][j].tag:  # 引数のタグを見つけた場合
                    if None == ext:                                             # 設定値が指定されていない場合
                        self.ladder[i][j].ext = abs(self.ladder[i][j].ext - 1)  # 反転
                    else:                                                       # 設定値が指定されている場合
                        self.ladder[i][j].ext = ext                             # 変更

    def run(self):
        for i in range(len(self.ladder)):  # 行数繰り返し
            self.ladder[i][-1].opt = 0     # 出力結果リセット

        i = 0   # 行番号
        j = 0   # 列番号
        b = 1   # 信号
        k = []  # 位置情報記録

        for loop in range(100):
            if loop == 99:
                print("MUGEN")

            # print(str(i) + ", " + str(j))
            if self.ladder[i][j].brc == 1:  # 下に分岐がある場合
                k.append([i, j, b])         # 現在位置情報を記録

            b = self.ladder[i][j].cal(b)  # 演算

            if self.ladder[i][j].typ in self.in_list:  # 現在位置が入力命令の場合
                j += 1                                 # 右へ
                while True:                            # 上がなくなるまで繰り返し
                    if i == 0:                         # 一行目の場合
                        break                          # 繰り返し終了
                    if self.ladder[i-1][j].brc == 1:   # 上に分岐がある場合
                        i -= 1                         # 上へ
                    else:                              # 上に分岐がない場合
                        break                          # 繰り返し終了
                continue                               # 下の分岐確認へ

            if len(k) > 0:       # 位置情報の記録がある場合
                i = k[0][0] + 1  # 位置情報の一つ下
                j = k[0][1]      # 位置情報と同じ列
                b = k[0][2]      # 位置情報と同じ入力
                del k[0]         # 位置情報削除
                continue         # 下の分岐確認へ
            break  # すべての命令の演算終了

        for i in range(len(self.ladder)):                                    # 行数繰り返し
            if self.ladder[i][-1].typ in self.out_list:                      # 出力命令の場合
                self.ladder[i][-1].out()                                     # 出力命令演算
                self.change(self.ladder[i][-1].tag, self.ladder[i][-1].opt)  # 出力を入力に反映

        for i in range(len(self.ladder)):                                     # 行数繰り返し
            if self.ladder[i][-1].typ == "Rs":                                # リセット命令の場合
                if self.ladder[i][-1].opt == 1:                               # リセット命令がONの場合
                    for j in range(len(self.ladder)):                         # 行数繰り返し
                        if self.ladder[i][-1].tag == self.ladder[j][-1].tag:  # 同じ名前の場合
                            self.ladder[j][-1].c = 0                          # カウンタリセット
                    self.change(self.ladder[i][-1].tag, 0)                    # 入力にリセットを反映

    def check(self):
        for i in range(len(self.ladder)):
            for j in range(len(self.ladder[i])):
                if self.ladder[i][j].typ in self.tag_list:
                    tp_t = self.ladder[i][j].typ
                    tg_t = self.ladder[i][j].tag
                    ex_t = "ext=" + str(self.ladder[i][j].ext)
                    ot_t = "out=" + str(self.ladder[i][j].opt)
                    print(tp_t + " " + tg_t + " : " + ex_t + ", " + ot_t)


def test1():
    ld = Ladder()
    ld.add("M", 1, tag="x0")
    ld.add("St", 0, tag="m0")
    ld.add("M", 1, tag="x1")
    ld.add("Rs", 0, tag="m0")
    ld.add("M", 0, tag="m0")
    ld.add("R", 0, tag="y0")

    for t in range(10):
        print("t=" + str(t))
        if t == 1:
            ld.change("x0")
        if t == 2:
            ld.change("x0")
        if t == 5:
            ld.change("x1")
        if t == 6:
            ld.change("x1")
        ld.run()
        ld.check()

    """
    ld = Ladder()
    ld.add("M", 1, tag="x0")
    ld.add("B", 1, tag="t0")
    ld.add("R", 1, tag="m0")
    ld.add("M", 1, tag="m0")
    ld.add("Bl", 0)
    ld.add("T", 0, tag="t0", set=5)
    ld.add("M", 0, tag="m0")
    ld.add("Ln", 0)
    ld.add("R", 0, tag="y0")

    for t in range(10):
        print("t=" + str(t))
        if t == 1:
            ld.change("x0")
        if t == 2:
            ld.change("x0")
        ld.run()
        ld.check()
    """


def test2():
    com = "out t0 k1"
    comp = Ladder.Comp("", 0)
    comp.dec(com)
    print("typ=" + comp.typ)
    print("tag=" + comp.tag)
    print("set=" + str(comp.set))
