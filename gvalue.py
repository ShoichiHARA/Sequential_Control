# 言語クラス
class Language:
    lg_list = ["ENG", "JPN"]

    def __init__(self, lag="ENG"):
        self.lg = lag
        n = 0
        if self.lg in self.lg_list:
            n = self.lg_list.index(self.lg)
        self.tit = ["Sequential Control", "シーケンス制御"][n]
        self.fil = ["File", "ファイル"][n]
        self.new = ["New", "新規作成"][n]
        self.opn = ["Open", "開く"][n]
        self.sav = ["Save", "上書き保存"][n]
        self.sva = ["Save as", "名前を付けて保存"][n]
        self.ext = ["Exit", "終了"][n]
        self.edt = ["Edit", "編集"][n]
        self.add = ["Addition", "追加"][n]
        self.ins = ["Insertion", "挿入"][n]
        self.dlt = ["Deletion", "削除"][n]
        self.row = ["Row", "行"][n]
        self.clm = ["Column", "列"][n]
        self.sim = ["Simulation", "シミュレーション"][n]
        self.stt = ["Start", "開始"][n]
        self.pus = ["Pause", "一時停止"][n]
        self.stp = ["Stop", "停止"][n]
        self.set = ["Setting", "設定"][n]
        self.viw = ["View", "表示"][n]
        self.iol = ["I/O Allocation", "入出力割付"][n]
        self.cnv = ["Conveyor", "コンベア"][n]
        self.trf = ["Traffic Light", "信号機"][n]
        self.hlp = ["Help", "ヘルプ"][n]


lg = Language("JPN")
