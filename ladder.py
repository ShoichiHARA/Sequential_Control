class Ladder:
    tag_list = ["M", "B", "P", "F", "R", "T", "C", "St", "Rs"]  # 名付命令リスト
    in_list = ["M", "B", "P", "F", "Ln"]  # 入力命令リスト
    out_list = ["R", "T", "C", "St"]  # 出力命令リスト(リセット命令以外)
    end_list = ["R", "T", "C", "St", "Rs", "En"]  # 改行命令リスト

    def __init__(self, rnum=5):
        self.rnum = rnum
        self.row = []     # 1行のラダープログラム
        self.ladder = []  # 全体のラダープログラム
        self.add_pls([0, 0])

    class Comp:
        def __init__(self, typ, brc):
            self.typ = typ     # 命令タイプ
            self.brc = brc     # 分岐
            self.tag = "none"  # 名前
            self.set = 0       # 設定値
            self.ext = 0       # 外部入力
            self.opt = 0       # 出力
            self.cnt = 0       # カウント現在値
            self.c = 0
            self.lst = 0       # 前回値

        def dec(self, st):
            com = st.split()
            if com[0] == "brc":
                if com[1] in ["0", "1"]:
                    self.brc = int(com[1])
                    return 0
                else:
                    return 4  # 設定値が無効
            elif com[0] == "ln":
                self.typ = "Ln"
            elif com[0] == "bl":
                self.typ = "Bl"
            elif com[0] == "ent":
                self.typ = "En"
            elif com[0] == "ld":
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
            elif self.typ == "P":  # 立上りパルス
                self.opt = 0
                if self.ext == 1:
                    if self.lst == 0:
                        self.opt = ipt
                self.lst = self.ext
            elif self.typ == "F":  # 立下りパルス
                self.opt = 0
                if self.ext == 0:
                    if self.lst == 1:
                        self.opt = ipt
                self.lst = self.ext
            elif self.typ in Ladder.out_list:  # 出力命令
                if self.opt == 0:
                    self.opt = ipt
            elif self.typ == "Rs":  # リセット命令
                if self.opt == 0:
                    self.opt = ipt
            return self.opt

        def out(self):
            if self.typ == "T":                       # タイマ出力命令の場合
                if self.opt == 1:                     # 入力がONの場合
                    if self.lst == 0:                 # 前回の出力がOFFの場合
                        self.opt = 0                  # 出力OFF
                        self.c += 1                   # カウントアップ
                        if self.c == 5:               # 0.02秒*5回で0.1秒
                            self.c = 0                # カウントリセット
                            self.cnt += 1             # 設定カウントアップ
                            if self.cnt == self.set:  # 設定値に届いた場合
                                self.opt = 1          # 出力OFF
                else:                                 # 入力がOFFの場合
                    self.c = 0                        # カウントリセット
                    self.cnt = 0                      # 設定カウントリセット
                self.lst = self.opt                   # 前回値更新
            if self.typ == "C":                    # カウンタ出力命令の場合
                pass                               #
            if self.typ == "St":           # セット命令の場合
                if self.ext+self.opt > 0:  # 前回出力ONまたはセット命令ONの場合
                    self.opt = 1           # 出力ON
                else:                      # 前回出力OFFかつセット命令OFFの場合
                    self.opt = 0           # 出力OFF

    def jud_txt(self, txt):
        pass

    def add_pls(self, xy):
        while xy[1] >= len(self.ladder):                    # 指定した行があるまで繰り返し
            self.ladder.append([])                          # 行追加
            for i in range(self.rnum-1):                    # 最終列手前まで繰り返し
                self.ladder[-1].append(self.Comp("Bl", 0))  # 空白命令追加
            self.ladder[-1].append(self.Comp("En", 0))      # 改行命令追加

    def add_txt(self, xy, txt):
        self.add_pls(xy)  # 命令挿入空間作成
        err = self.ladder[xy[1]][xy[0]].dec(txt)  # 文字列から要素を判定
        if err != 0:                              # エラーの場合
            return err                            # 戻り値エラー種類
        return 0

    def add_com(self, xy, brc=None, typ=None, tag=None, set=None):
        self.add_pls(xy)                         # 命令挿入空間作成
        if brc is not None:                      # 分岐が設定されている場合
            self.ladder[xy[1]][xy[0]].brc = brc  # 分岐設定
        if typ is not None:                      # 種類が設定されている場合
            self.ladder[xy[1]][xy[0]].typ = typ  # 種類設定
        if tag is not None:                      # 名前が設定されている場合
            self.ladder[xy[1]][xy[0]].tag = tag  # 名前設定
        if set is not None:                      # 設定値が設定されている場合
            self.ladder[xy[1]][xy[0]].set = set  # 設定値設定

    def ins_rc(self, xy, rc):
        if rc == "c":
            self.ladder.insert(xy[1], [])
            for i in range(self.rnum):
                if xy[1] == 0:
                    brc = 0
                else:
                    brc = self.ladder[xy[1]-1][i].brc
                if i < self.rnum - 1:
                    self.ladder[xy[1]].append(self.Comp("Bl", brc))
                else:
                    self.ladder[xy[1]].append(self.Comp("En", brc))
        elif rc == "r":  # 列挿入は改善が必要
            for i in range(len(self.ladder)):
                self.ladder[i].insert(xy[0], self.Comp("Ln", 0))
                del self.ladder[i][-2]

    def org(self):
        i = 0
        while i < len(self.ladder):    # 最終行まで繰り返し
            f = 1                      # 空白命令のフラグ
            self.ladder[i][0].brc = 1  # 先頭の分岐
            for j in range(self.rnum):                         # 列数繰り返し
                if self.ladder[i][j].typ not in ["Bl", "En"]:  # 空白または改行以外の命令の場合
                    f = 0                                      # フラグリセット
            if f == 1:                 # 行になにもない場合
                del self.ladder[i]     # 行削除
                continue               # 行先頭へ
            i += 1                     # 次の行へ
        self.ladder[-1][0].brc = 0     # 最終号の先頭は分岐なし

    def add_row(self, typ, brc, tag="", set=0):
        self.row.append(self.Comp(typ, brc))  # 行に追加
        if typ in self.tag_list:              # 名付命令の場合
            self.row[-1].tag = tag            # 名前を登録
        if typ in ["T", "C"]:                 # 設定値のある命令の場合
            self.row[-1].set = set            # 設定値を登録
        if typ in self.end_list:              # 改行命令の場合
            self.ladder.append(self.row)      # 行を全体に追加
            self.row = []                     # 行を初期化

    def change(self, tag, ext=None, fa=0):
        for i in range(len(self.ladder)):  # 行数繰り返し
            for j in range(len(self.ladder[i])):  # 列数繰り返し
                if fa == 0:                                                         # 完全一致で検索
                    if tag == self.ladder[i][j].tag:                                # 引数のタグを見つけた場合
                        if ext is None:
                            self.ladder[i][j].ext = abs(self.ladder[i][j].ext - 1)  # 反転
                        else:                                                       # 設定値が指定されている場合
                            self.ladder[i][j].ext = ext                             # 変更
                elif fa == 1:                                                       # 前方一致で検索
                    if self.ladder[i][j].tag.startswith(tag):                       # 引数のタグで始まっている場合
                        if ext is None:                                             # 設定値が指定されていない場合
                            self.ladder[i][j].ext = abs(self.ladder[i][j].ext - 1)  # 反転
                        else:                                                       # 設定値が指定されている場合
                            self.ladder[i][j].ext = ext                             # 変更

    def clr_out(self):
        for i in range(len(self.ladder)):         # 行数繰り返し
            for j in range(len(self.ladder[i])):  # 列数繰り返し
                self.ladder[i][j].opt = 0         # 出力結果初期化

    def clr_ext(self):
        for i in range(len(self.ladder)):         # 行数繰り返し
            for j in range(len(self.ladder[i])):  # 列数繰り返し
                self.ladder[i][j].ext = 0         # 外部入力初期化

    def run(self):
        self.clr_out()  # 出力結果初期化

        i = 0   # 行番号
        j = 0   # 列番号
        b = 1   # 信号
        k = []  # 位置情報記録

        for loop in range(1000):
            if loop == 999:
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
    ld.add_row("M", 1, tag="x0")
    ld.add_row("St", 0, tag="m0")
    ld.add_row("M", 1, tag="x1")
    ld.add_row("Rs", 0, tag="m0")
    ld.add_row("M", 0, tag="m0")
    ld.add_row("R", 0, tag="y0")

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


def test3():
    ld = Ladder(3)

    ld.add_txt([0, 0], "ld x0")
    ld.add_txt([1, 0], "ldi x1")
    ld.add_txt([1, 0], "brc 1")
    ld.add_txt([2, 0], "out m0")
    ld.add_txt([0, 1], "ld m0")
    ld.add_txt([0, 2], "ld m0")
    ld.add_txt([1, 2], "ln")
    ld.add_txt([2, 2], "out y0")

    ld.org()

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


def test4(ld: Ladder):
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
