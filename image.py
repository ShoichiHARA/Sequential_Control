from PIL import Image, ImageDraw


# 部品図形の生成
def image(out):
    # 切替スイッチ右
    ssr = Image.new(mode="RGB", size=(80, 80), color="white")
    ssr_d = ImageDraw.Draw(ssr)
    ssr_d.ellipse(xy=[0, 0, 79, 79], outline="black", width=2)
    ssr_d.line(xy=[59, 6, 6, 59], fill="black", width=2)
    ssr_d.line(xy=[74, 21, 21, 74], fill="black", width=2)

    # 切替スイッチ左
    ssl = Image.new(mode="RGB", size=(80, 80), color="white")
    ssl_d = ImageDraw.Draw(ssl)
    ssl_d.ellipse(xy=[0, 0, 79, 79], outline="black", width=2)
    ssl_d.line(xy=[21, 6, 73, 58], fill="black", width=2)
    ssl_d.line(xy=[6, 21, 58, 73], fill="black", width=2)

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
    pb2n_d.polygon(xy=[0, 60, 60, 0, 0, 0], fill="darkgray")  # 本体より暗めより暗め
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
    pb5f_d.ellipse(xy=[0, 0, 79, 79], fill="red", outline="black", width=2)
    pb5f_d.ellipse(xy=[15, 15, 65, 65], fill="#FF2828", outline="black", width=2)

    # 押しボタンスイッチ5ON
    pb5n = Image.new(mode="RGB", size=(80, 80), color="white")
    pb5n_d = ImageDraw.Draw(pb5n)
    pb5n_d.ellipse(xy=[5, 5, 75, 75], fill="#D20000", outline="black", width=2)
    pb5n_d.ellipse(xy=[18, 18, 62, 62], fill="#E60000", outline="black", width=2)

    # パイロットランプ1OFF
    pl1f = Image.new(mode="RGB", size=(60, 60), color="white")
    pl1f_d = ImageDraw.Draw(pl1f)
    pl1f_d.ellipse(xy=[0, 0, 59, 59], fill="silver", outline="black", width=2)
    pl1f_d.ellipse(xy=[5, 5, 54, 54], fill="#00B400", outline="black", width=2)

    # パイロットランプ1ON
    pl1n = Image.new(mode="RGB", size=(60, 60), color="white")
    pl1n_d = ImageDraw.Draw(pl1n)
    pl1n_d.ellipse(xy=[0, 0, 59, 59], fill="silver", outline="black", width=2)
    pl1n_d.ellipse(xy=[5, 5, 54, 54], fill="lime", outline="black", width=2)

    # パイロットランプ2OFF
    pl2f = Image.new(mode="RGB", size=(60, 60), color="white")
    pl2f_d = ImageDraw.Draw(pl2f)
    pl2f_d.ellipse(xy=[0, 0, 59, 59], fill="silver", outline="black", width=2)
    pl2f_d.ellipse(xy=[5, 5, 54, 54], fill="darkgray", outline="black", width=2)

    # パイロットランプ2ON
    pl2n = Image.new(mode="RGB", size=(60, 60), color="white")
    pl2n_d = ImageDraw.Draw(pl2n)
    pl2n_d.ellipse(xy=[0, 0, 59, 59], fill="silver", outline="black", width=2)
    pl2n_d.ellipse(xy=[5, 5, 54, 54], fill="whitesmoke", outline="black", width=2)

    # パイロットランプ3OFF
    pl3f = Image.new(mode="RGB", size=(60, 60), color="white")
    pl3f_d = ImageDraw.Draw(pl3f)
    pl3f_d.ellipse(xy=[0, 0, 59, 59], fill="silver", outline="black", width=2)
    pl3f_d.ellipse(xy=[5, 5, 54, 54], fill="royalblue", outline="black", width=2)

    # パイロットランプ3ON
    pl3n = Image.new(mode="RGB", size=(60, 60), color="white")
    pl3n_d = ImageDraw.Draw(pl3n)
    pl3n_d.ellipse(xy=[0, 0, 59, 59], fill="silver", outline="black", width=2)
    pl3n_d.ellipse(xy=[5, 5, 54, 54], fill="deepskyblue", outline="black", width=2)

    # パイロットランプ4OFF
    pl4f = Image.new(mode="RGB", size=(60, 60), color="white")
    pl4f_d = ImageDraw.Draw(pl4f)
    pl4f_d.ellipse(xy=[0, 0, 59, 59], fill="silver", outline="black", width=2)
    pl4f_d.ellipse(xy=[5, 5, 54, 54], fill="#AAAA00", outline="black", width=2)

    # パイロットランプ4ON
    pl4n = Image.new(mode="RGB", size=(60, 60), color="white")
    pl4n_d = ImageDraw.Draw(pl4n)
    pl4n_d.ellipse(xy=[0, 0, 59, 59], fill="silver", outline="black", width=2)
    pl4n_d.ellipse(xy=[5, 5, 54, 54], fill="yellow", outline="black", width=2)

    # パレット
    pall = Image.new(mode="RGB", size=(160, 120), color="silver")
    pall_d = ImageDraw.Draw(pall)
    pall_d.rectangle(xy=(0, 0, 159, 119), outline="black", width=2)

    # 製品
    prod = Image.new(mode="RGB", size=(30, 30))
    prod_d = ImageDraw.Draw(prod)
    prod_d.ellipse(xy=[2, 2, 28, 28], fill="darkgray", outline="black", width=1)
    prod_d.line(xy=[0, 0, 30, 30], fill="black", width=2)
    prod_d.line(xy=[0, 30, 30, 0], fill="black", width=2)
    put = Image.new(mode="L", size=(30, 30), color="black")
    put_d = ImageDraw.Draw(put)
    put_d.ellipse(xy=[1, 1, 29, 29], fill="white")
    prod.putalpha(put)

    # 導線
    line = Image.new(mode="RGB", size=(80, 60), color="white")
    line_d = ImageDraw.Draw(line)
    line_d.line(xy=[0, 30, 80, 30], fill="black", width=2)

    # a接点
    make = Image.new(mode="RGB", size=(80, 60), color="white")
    make_d = ImageDraw.Draw(make)
    make_d.line(xy=[30, 20, 30, 40], fill="black", width=2)
    make_d.line(xy=[50, 20, 50, 40], fill="black", width=2)
    make_d.line(xy=[0, 30, 30, 30], fill="black", width=2)
    make_d.line(xy=[50, 30, 80, 30], fill="black", width=2)

    # b接点
    brek = make.copy()
    brek_d = ImageDraw.Draw(brek)
    brek_d.line(xy=[50, 20, 30, 40], fill="black", width=2)

    # 立ち上がりパルス
    plse = make.copy()
    plse_d = ImageDraw.Draw(plse)
    plse_d.line(xy=[40, 20, 40, 40], fill="black", width=2)
    plse_d.line(xy=[35, 30, 40, 20, 45, 30], fill="black", width=2)

    # 立ち下がりパルス
    fall = make.copy()
    fall_d = ImageDraw.Draw(fall)
    fall_d.line(xy=[40, 20, 40, 40], fill="black", width=2)
    fall_d.line(xy=[35, 30, 40, 40, 45, 30], fill="black", width=2)

    # 基本出力
    base = Image.new(mode="RGB", size=(80, 60), color="white")
    base_d = ImageDraw.Draw(base)
    base_d.arc(xy=[5, 5, 75, 55], start=152, end=208, fill="black", width=2)
    base_d.arc(xy=[5, 5, 75, 55], start=332, end=28, fill="black", width=2)
    base_d.line(xy=[0, 30, 5, 30], fill="black", width=2)
    base_d.line(xy=[75, 30, 80, 30], fill="black", width=2)

    # 応用出力
    # aply = Image.new(mode="RGB", size=(100, 80), color="white")

    base.show()

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
        pl1f.save("image/PL1_OFF.png")
        pl1n.save("image/PL1_ON.png")
        pl2f.save("image/PL2_OFF.png")
        pl2n.save("image/PL2_ON.png")
        pl3f.save("image/PL3_OFF.png")
        pl3n.save("image/PL3_ON.png")
        pl4f.save("image/PL4_OFF.png")
        pl4n.save("image/PL4_ON.png")
        pall.save("image/Pallet.png")
        prod.save("image/Product.png")
        line.save("image/Line.png")
        make.save("image/Make.png")
        brek.save("image/Break.png")
        plse.save("image/Pulse.png")
        fall.save("image/Falling.png")
        base.save("image/Base_Out.png")
