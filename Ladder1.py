class Ladder:
    def __init__(self):
        self.row = []     # 1行のラダープログラム
        self.ladder = []  # 全体のラダープログラム
        self.relay = []   # コイル

    class Comp:
        def __init__(self, type, label="", branch="", rnum=0):
            self.type = type      # 要素の種類
            self.label = label    # 要素の名前
            self.branch = branch  # 分岐
            self.rnum = rnum      # コイルの番号
            self.exter = 0        # 外部入力
            self.output = 0       # 出力

        def cal(self, input):
            if self.type == "M":
                self.output = input * self.exter
            if self.type == "B":
                self.output = input * abs(self.exter - 1)
            if self.type == "Bl":
                self.output = 0
            if self.type in ["R", "Li", "En"]:
                self.output = input
            return self.output

    def add(self, type, label="", branch=""):
        if type in ["M", "B", "Li", "Bl", "En"]:
            self.row.append(self.Comp(type, label, branch))
        if type in ["R", "T", "C"]:
            rnum = len(self.relay)
            self.relay.append([label, 0])
            self.row.append(self.Comp(type, label, branch, rnum))
        if type in ["En", "R", "T", "C"]:
            self.ladder.append(self.row)
            self.row = []

    def change(self, label, ex=None):
        for i in range(len(self.ladder)):
            for j in range(len(self.ladder[i])):
                if self.ladder[i][j].label == label:
                    if ex == None:
                        self.ladder[i][j].exter = abs(self.ladder[i][j].exter - 1)
                    else:
                        self.ladder[i][j].exter = ex

    def changes(self):
        for i in range(len(self.relay)):
            self.change(self.relay[i][0], self.relay[i][1])

    def run(self):
        for i in range(len(self.ladder)):  # 行数繰り返し
            self.ladder[i][-1].output = 0  # 出力リセット
        for i in range(len(self.relay)):   # コイル数繰り返し
            self.relay[i][1] = 0           # 出力リセット
        i = 0   # 行
        j = 0   # 列
        b = 0   # ONかOFF
        k = []  # 位置情報記録
        c = 0
        while True:           # 最終行まで繰り返し
            if j == 0:        # 先頭の場合
                b = 1         # 信号送信開始
            # print("i=" + str(i) + ", j=" + str(j) + ", b=" + str(b))
            # print("type=" + self.ladder[i][j].type + ", branch=" + self.ladder[i][j].branch)
            if self.ladder[i][j].branch in ["u", "ud"]:  # 上に分岐している場合
                i -= 1                                   # 上へ
                k.insert(0, [i, j])                      # 現在位置記録
                continue                                 # 繰り返し最初から
            if self.ladder[i][j].branch in ["d", "ud"]:  # 下に分岐している場合
                k.insert(0, [i, j])                      # 現在位置記録
            b = self.ladder[i][j].cal(b)                 # 演算
            if b == 1:                                   # ONになった場合
                if self.ladder[i][j].type not in ["R", "T", "C", "En"]:  # 右にある場合
                    j += 1                               # 右へ
                    continue                             # 繰り返し最初から
                if self.ladder[i][-1].type in ["R", "T", "C"]:  # コイルの場合
                    self.relay[self.ladder[i][-1].rnum][1] = self.ladder[i][-1].output
            if len(k) > 0:                               # 情報記録している場合
                i = k[0][0] + 1                          # 記録の一つ下
                j = k[0][1]                              # 同じ列
                del k[0]                                 # 記録を消去
            i += 1                                       # 下へ
            j = 0                                        # 左へ
            if i == len(self.ladder):                    # 下にない場合
                break                                    # 終了
            c += 1
            if c == 100:
                print("mugen")
                break

    def check(self):
        for i in range(len(self.ladder)):
            for j in range(len(self.ladder[i])):
                if self.ladder[i][j].type in ["M", "B", "R", "T", "C"]:
                    t_st = self.ladder[i][j].type
                    l_st = self.ladder[i][j].label
                    e_st = "ex=" + str(self.ladder[i][j].exter)
                    o_st = "out=" + str(self.ladder[i][j].output)
                    print(t_st + " " + l_st + " : " + e_st + ", " + o_st)


def test():
    ld = Ladder()
    ld.add("M", "x0")
    ld.add("B", "x4")
    ld.add("R", "m0")
    ld.add("M", "m0")
    ld.add("Bl", branch="u")
    ld.add("En")
    ld.add("M", "m0")
    ld.add("R", "y0")
    # print(ld.ladder)

    for t in range(10):
        print("t=" + str(t))
        if t == 1:
            ld.change("x0")

        if t == 2:
            ld.change("x0")

        if t == 5:
            ld.change("x4")

        if t == 6:
            ld.change("x4")

        ld.run()
        ld.check()
        ld.changes()
        print("change")
        ld.check()
