language = "ENG"

lang = ["ENG", "JPN"]
dic = [
    ["Sequential Control", "シーケンス制御"],
    ["File", "ファイル"],
    ["Setting", "設定"],
    ["Exit", "終了"],
    ["View", "表示"],
    ["Practice Board", "実習盤"],
    ["Help", "ヘルプ"],
    ["Manu", "手動"],
    ["Auto", "自動"],
    ["Continuous Operation", "連続運転"]
]

for i in range(len(lang)):
    if lang[i] == language:
        mw = dic[0][i]
        fl = dic[1][i]
        st = dic[2][i]
        ex = dic[3][i]
        vw = dic[4][i]
        pb = dic[5][i]
        hp = dic[6][i]
        mn = dic[7][i]
        at = dic[8][i]
