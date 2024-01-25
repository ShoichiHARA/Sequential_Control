import sys
import cx_Freeze

"""
exeファイル作成
ターミナルで以下のコマンドを実行
python setup.py build
"""

base = None

if sys.platform == "win32":
    base = "Win32GUI"

# スクリプトの設定
exe = cx_Freeze.Executable(
    script="main.py",
    base=base
)

# オプション
options = {
    "base": "Win32GUI",         # コンソール非表示
    "include_files": [("image", "image")]  # ファイルの追加
}

# exeファイルの生成
cx_Freeze.setup(
    name="Sequential_Control",
    version="0.2",
    description="converter",
    options={"build_exe": options},
    executables=[exe],
)
