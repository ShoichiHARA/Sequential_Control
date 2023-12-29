from PIL import Image, ImageDraw


# 部品図形の生成
def image(out):
    # 切替スイッチ右
    ssr = Image.new(mode="RGB", size=(200, 200), color="white")
    ssr_d = ImageDraw.Draw(ssr)
    ssr_d.ellipse(xy=[0, 0, 200, 200], outline="black", width=6)
    ssr_d.line(xy=[152, 18, 18, 152], fill="black", width=7)
    ssr_d.line(xy=[182, 48, 48, 182], fill="black", width=7)

    # 切替スイッチ左
    ssl = Image.new(mode="RGB", size=(200, 200), color="white")
    ssl_d = ImageDraw.Draw(ssl)
    ssl_d.ellipse(xy=[0, 0, 200, 200], outline="black", width=6)
    ssl_d.line(xy=[48, 18, 182, 152], fill="black", width=7)
    ssl_d.line(xy=[18, 48, 152, 182], fill="black", width=7)

    # 押しボタンスイッチ1OFF
    pb1f = Image.new(mode="RGB", size=(80, 80), color="#46FF46")
    pb1f_d = ImageDraw.Draw(pb1f)
    pb1f_d.polygon(xy=[0, 80, 80, 0, 80, 80], fill="limegreen")
    pb1f_d.line(xy=[0, 0, 80, 80], fill="black", width=2)
    pb1f_d.line(xy=[0, 80, 80, 0], fill="black", width=2)
    pb1f_d.rectangle(xy=(0, 0, 80, 80), outline="black", width=2)
    pb1f_d.rectangle(xy=(10, 10, 70, 70), fill="lime", outline="black", width=2)

    # 押しボタンスイッチ1ON
    pb1n = Image.new(mode="RGB", size=(80, 80), color="lime")
    pb1n_d = ImageDraw.Draw(pb1n)
    pb1n_d.polygon(xy=[0, 80, 80, 0, 0, 0], fill="#00B400")
    pb1n_d.line(xy=[0, 0, 80, 80], fill="black", width=2)
    pb1n_d.line(xy=[0, 80, 80, 0], fill="black", width=2)
    pb1n_d.rectangle(xy=(0, 0, 80, 80), outline="black", width=2)
    pb1n_d.rectangle(xy=(10, 10, 70, 70), fill="limegreen", outline="black", width=2)

    # pb1f.show()

    if out == 1:
        ssr.save("image/SS_Right.png")
        ssl.save("image/SS_Left.png")
        pb1f.save("image/PB1_OFF.png")
        pb1n.save("image/PB1_ON.png")
