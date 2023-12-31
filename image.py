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
    pb1f = Image.new(mode="RGB", size=(60, 60), color="#64FF64")  # 本体より明るめ
    pb1f_d = ImageDraw.Draw(pb1f)
    pb1f_d.polygon(xy=[0, 60, 60, 0, 60, 60], fill="limegreen")  # 本体より暗め
    pb1f_d.line(xy=[0, 0, 60, 60], fill="black", width=2)
    pb1f_d.line(xy=[0, 60, 60, 0], fill="black", width=2)
    pb1f_d.rectangle(xy=(0, 0, 60, 60), outline="black", width=2)
    pb1f_d.rectangle(xy=(5, 5, 55, 55), fill="lime", outline="black", width=2)  # 本体

    # 押しボタンスイッチ1ON
    pb1n = Image.new(mode="RGB", size=(60, 60), color="lime")  # 本体と同じ
    pb1n_d = ImageDraw.Draw(pb1n)
    pb1n_d.polygon(xy=[0, 60, 60, 0, 0, 0], fill="#00B400")  # 本体より暗めより暗め
    pb1n_d.line(xy=[0, 0, 60, 60], fill="black", width=2)
    pb1n_d.line(xy=[0, 60, 60, 0], fill="black", width=2)
    pb1n_d.rectangle(xy=(0, 0, 60, 60), outline="black", width=2)
    pb1n_d.rectangle(xy=(5, 5, 55, 55), fill="limegreen", outline="black", width=2)  # 本体より暗め

    # 押しボタンスイッチ2OFF
    pb2f = Image.new(mode="RGB", size=(60, 60), color="white")  # 本体より明るめ
    pb2f_d = ImageDraw.Draw(pb2f)
    pb2f_d.polygon(xy=[0, 60, 60, 0, 60, 60], fill="silver")  # 本体より暗め
    pb2f_d.line(xy=[0, 0, 60, 60], fill="black", width=2)
    pb2f_d.line(xy=[0, 60, 60, 0], fill="black", width=2)
    pb2f_d.rectangle(xy=(0, 0, 60, 60), outline="black", width=2)
    pb2f_d.rectangle(xy=(5, 5, 55, 55), fill="whitesmoke", outline="black", width=2)  # 本体

    # 押しボタンスイッチ2ON
    pb2n = Image.new(mode="RGB", size=(60, 60), color="whitesmoke")  # 本体と同じ
    pb2n_d = ImageDraw.Draw(pb2n)
    pb2n_d.polygon(xy=[0, 60, 60, 0, 0, 0], fill="darkgrey")  # 本体より暗めより暗め
    pb2n_d.line(xy=[0, 0, 60, 60], fill="black", width=2)
    pb2n_d.line(xy=[0, 60, 60, 0], fill="black", width=2)
    pb2n_d.rectangle(xy=(0, 0, 60, 60), outline="black", width=2)
    pb2n_d.rectangle(xy=(5, 5, 55, 55), fill="silver", outline="black", width=2)  # 本体より暗め

    # 押しボタンスイッチ3OFF
    pb3f = Image.new(mode="RGB", size=(60, 60), color="lightskyblue")
    pb3f_d = ImageDraw.Draw(pb3f)
    pb3f_d.polygon(xy=[0, 60, 60, 0, 60, 60], fill="dodgerblue")
    pb3f_d.line(xy=[0, 0, 60, 60], fill="black", width=2)
    pb3f_d.line(xy=[0, 60, 60, 0], fill="black", width=2)
    pb3f_d.rectangle(xy=(0, 0, 60, 60), outline="black", width=2)
    pb3f_d.rectangle(xy=(5, 5, 55, 55), fill="deepskyblue", outline="black", width=2)

    # 押しボタンスイッチ3ON
    pb3n = Image.new(mode="RGB", size=(60, 60), color="deepskyblue")
    pb3n_d = ImageDraw.Draw(pb3n)
    pb3n_d.polygon(xy=[0, 60, 60, 0, 0, 0], fill="royalblue")
    pb3n_d.line(xy=[0, 0, 60, 60], fill="black", width=2)
    pb3n_d.line(xy=[0, 60, 60, 0], fill="black", width=2)
    pb3n_d.rectangle(xy=(0, 0, 60, 60), outline="black", width=2)
    pb3n_d.rectangle(xy=(5, 5, 55, 55), fill="dodgerblue", outline="black", width=2)

    # 押しボタンスイッチ4OFF
    pb4f = Image.new(mode="RGB", size=(60, 60), color="#FFFF50")
    pb4f_d = ImageDraw.Draw(pb4f)
    pb4f_d.polygon(xy=[0, 60, 60, 0, 60, 60], fill="#C8C800")
    pb4f_d.line(xy=[0, 0, 60, 60], fill="black", width=2)
    pb4f_d.line(xy=[0, 60, 60, 0], fill="black", width=2)
    pb4f_d.rectangle(xy=(0, 0, 60, 60), outline="black", width=2)
    pb4f_d.rectangle(xy=(5, 5, 55, 55), fill="yellow", outline="black", width=2)

    # 押しボタンスイッチ4ON
    pb4n = Image.new(mode="RGB", size=(60, 60), color="yellow")
    pb4n_d = ImageDraw.Draw(pb4n)
    pb4n_d.polygon(xy=[0, 60, 60, 0, 0, 0], fill="#AAAA00")
    pb4n_d.line(xy=[0, 0, 60, 60], fill="black", width=2)
    pb4n_d.line(xy=[0, 60, 60, 0], fill="black", width=2)
    pb4n_d.rectangle(xy=(0, 0, 60, 60), outline="black", width=2)
    pb4n_d.rectangle(xy=(5, 5, 55, 55), fill="#C8C800", outline="black", width=2)

    # 押しボタンスイッチ5OFF
    pb5f = Image.new(mode="RGB", size=(80, 80), color="white")
    pb5f_d = ImageDraw.Draw(pb5f)
    pb5f_d.ellipse(xy=[0, 0, 80, 80], fill="red", outline="black", width=3)
    pb5f_d.ellipse(xy=[15, 15, 65, 65], fill="#FF2828", outline="black", width=3)

    # 押しボタンスイッチ5ON
    pb5n = Image.new(mode="RGB", size=(80, 80), color="white")
    pb5n_d = ImageDraw.Draw(pb5n)
    pb5n_d.ellipse(xy=[5, 5, 75, 75], fill="#D20000", outline="black", width=3)
    pb5n_d.ellipse(xy=[18, 18, 62, 62], fill="#E60000", outline="black", width=3)

    # pb5n.show()

    if out == 1:
        ssr.save("image/SS_Right.png")
        ssl.save("image/SS_Left.png")
        pb1f.save("image/PB1_OFF.png")
        pb1n.save("image/PB1_ON.png")
        pb2f.save("image/PB2_OFF.png")
        pb2n.save("image/PB2_ON.png")
        pb3f.save("image/PB3_OFF.png")
        pb3n.save("image/PB3_ON.png")
        pb4f.save("image/PB4_OFF.png")
        pb4n.save("image/PB4_ON.png")
        pb5f.save("image/PB5_OFF.png")
        pb5n.save("image/PB5_ON.png")
