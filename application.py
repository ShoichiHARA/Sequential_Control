import tkinter as tk
from tkinter import messagebox

# Tkinterインスタンスの生成
root = tk.Tk()

# 変数を使ってウインドウの設定
root.title("Sequential_Control")  # ウインドウのタイトルの指定
root.geometry("480x320")          # ウインドウサイズの指定(横x縦)

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

