import tkinter as tk
from tkinter import messagebox


# マウス押下
def m_press(eve):
    if eve.num == 1:  # マウス左押下
        x = str(eve.x)
        y = str(eve.y)
        print("x=" + x + ", y=" + y)

    if eve.num == 3:  # マウス右押下
        print("press_R")


# マウス解放
def m_release(eve):
    if eve.num == 1:  # マウス左押下
        print("release_L")

    if eve.num == 3:  # マウス右押下
        print("release_R")


# キー押下
def k_press(eve):
    print(eve.char, "press")


# キー解放
def k_release(eve):
    print(eve.char, "release")


# 実習盤ウインドウ
def practice_board(root):
    # キャンバスの生成
    cvs = tk.Canvas(root, bg="white")    # 生成、背景色
    cvs.pack(fill=tk.BOTH, expand=True)  # 配置

    # イベント
    cvs.bind("<ButtonPress>", m_press)
    cvs.bind("<ButtonRelease>", m_release)
    cvs.bind("<KeyPress>", k_press)
    cvs.bind("<KeyRelease>", k_release)
    cvs.focus_set()

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


# アプリケーション
def application():
    # Tkinterインスタンスの生成
    root = tk.Tk()

    # 変数を使ってウインドウの設定
    root.title("Sequential_Control")  # ウインドウのタイトルの指定
    root.geometry("800x600")          # ウインドウサイズの指定(横x縦)

    # 実習盤の生成
    practice_board(root)

    # ウインドウの描画
    root.mainloop()
