from PIL import Image, ImageDraw


# 部品図形の生成
def image(out):
    # 切替スイッチ右
    ssr = Image.new(mode="RGB", size=(80, 80), color="white")
    ssr_d = ImageDraw.Draw(ssr)
    ssr_d.ellipse(xy=[0, 0, 80, 80], outline="black", width=3)
    ssr_d.line(xy=[60, 5, 5, 60], fill="black", width=3)
    ssr_d.line(xy=[75, 20, 20, 75], fill="black", width=3)

    # 切替スイッチ左
    ssl = Image.new(mode="RGB", size=(80, 80), color="white")
    ssl_d = ImageDraw.Draw(ssl)
    ssl_d.ellipse(xy=[0, 0, 80, 80], outline="black", width=3)
    ssl_d.line(xy=[20, 5, 75, 60], fill="black", width=3)
    ssl_d.line(xy=[5, 20, 60, 75], fill="black", width=3)

    # 押しボタンスイッチ1OFF
    pb1f = Image.new(mode="RGB", size=(80, 80), color="#64FF64")  # 本体より明るめ
    pb1f_d = ImageDraw.Draw(pb1f)
    pb1f_d.polygon(xy=[0, 80, 80, 0, 80, 80], fill="limegreen")  # 本体より暗め
    pb1f_d.line(xy=[0, 0, 80, 80], fill="black", width=2)
    pb1f_d.line(xy=[0, 80, 80, 0], fill="black", width=2)
    pb1f_d.rectangle(xy=(0, 0, 80, 80), outline="black", width=2)
    pb1f_d.rectangle(xy=(10, 10, 70, 70), fill="lime", outline="black", width=2)  # 本体

    # 押しボタンスイッチ1ON
    pb1n = Image.new(mode="RGB", size=(80, 80), color="lime")  # 本体と同じ
    pb1n_d = ImageDraw.Draw(pb1n)
    pb1n_d.polygon(xy=[0, 80, 80, 0, 0, 0], fill="#00B400")  # 本体より暗めより暗め
    pb1n_d.line(xy=[0, 0, 80, 80], fill="black", width=2)
    pb1n_d.line(xy=[0, 80, 80, 0], fill="black", width=2)
    pb1n_d.rectangle(xy=(0, 0, 80, 80), outline="black", width=2)
    pb1n_d.rectangle(xy=(10, 10, 70, 70), fill="limegreen", outline="black", width=2)  # 本体より暗め

    # 押しボタンスイッチ2OFF
    pb2f = Image.new(mode="RGB", size=(80, 80), color="white")  # 本体より明るめ
    pb2f_d = ImageDraw.Draw(pb2f)
    pb2f_d.polygon(xy=[0, 80, 80, 0, 80, 80], fill="silver")  # 本体より暗め
    pb2f_d.line(xy=[0, 0, 80, 80], fill="black", width=2)
    pb2f_d.line(xy=[0, 80, 80, 0], fill="black", width=2)
    pb2f_d.rectangle(xy=(0, 0, 80, 80), outline="black", width=2)
    pb2f_d.rectangle(xy=(10, 10, 70, 70), fill="whitesmoke", outline="black", width=2)  # 本体

    # 押しボタンスイッチ2ON
    pb2n = Image.new(mode="RGB", size=(80, 80), color="whitesmoke")  # 本体と同じ
    pb2n_d = ImageDraw.Draw(pb2n)
    pb2n_d.polygon(xy=[0, 80, 80, 0, 0, 0], fill="darkgrey")  # 本体より暗めより暗め
    pb2n_d.line(xy=[0, 0, 80, 80], fill="black", width=2)
    pb2n_d.line(xy=[0, 80, 80, 0], fill="black", width=2)
    pb2n_d.rectangle(xy=(0, 0, 80, 80), outline="black", width=2)
    pb2n_d.rectangle(xy=(10, 10, 70, 70), fill="silver", outline="black", width=2)  # 本体より暗め

    # ssl.show()

    if out == 1:
        ssr.save("image/SS_Right.png")
        ssl.save("image/SS_Left.png")
        pb1f.save("image/PB1_OFF.png")
        pb1n.save("image/PB1_ON.png")
        pb2f.save("image/PB2_OFF.png")
        pb2n.save("image/PB2_ON.png")
