import application2 as app
import ladder as ldd
import image as img

"""
exe化は、以下のコマンドをターミナルで実行
pyinstaller main.py --onefile --noconsole
"""


def main():
    # img.image(1)
    app.application()
    # ldd.test3()


if __name__ == "__main__":
    main()
