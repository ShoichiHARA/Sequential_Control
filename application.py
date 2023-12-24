import tkinter as tk
from tkinter import messagebox


# マウス左押下
def push_l(eve):
    x = str(eve.x)
    y = str(eve.y)
    print("x=" + x + ", y=" + y)


# マウス左解放
def release_l(eve):
    print("release_L")


# マウス右押下
def push_r(eve):
    print("push_R")


# マウス右解放
def release_r(eve):
    print("release_R")


# 実習盤ウインドウ
def practice_board():
    # Tkinterインスタンスの生成
    root = tk.Tk()

    # 変数を使ってウインドウの設定
    root.title("Sequential_Control")  # ウインドウのタイトルの指定
    root.geometry("800x600")          # ウインドウサイズの指定(横x縦)

    # キャンバスの生成
    cvs = tk.Canvas(root, bg="white")    # 生成、背景色
    cvs.pack(fill=tk.BOTH, expand=True)  # 配置

    # マウスイベント
    cvs.bind("<Button-1>", push_l)
    cvs.bind("<ButtonRelease-1>", release_l)
    cvs.bind("<Button-3>", push_r)
    cvs.bind("<ButtonRelease-3>", release_r)

    """
    # 入力欄の生成
    obj1 = tk.Entry(width=40)   # 生成と幅の設定
    obj1.place(x=20, y=100)     # 座標の設定
    
    
    # ボタンの生成
    def ck_button():  # ボタンの動作
        print("push")
        val1 = obj1.get()  # 入力欄の値の取得
        messagebox.showinfo("event", val1 + " input")  # ダイヤログに表示
    
    
    btn1 = tk.Button(text="play", command=ck_button)  # 生成と実行関数の設定
    btn1.place(x=20, y=140)                             # 座標の設定
    """
    root.mainloop()


# アプリケーション
def application():
    practice_board()
