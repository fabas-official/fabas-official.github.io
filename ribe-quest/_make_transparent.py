# ChatGPT生成画像（白背景）を、外側の白だけ透明にしてゲーム用PNGにする。
# 内部の白（目・ハイライト・銀の鎧）は、外周の濃い輪郭線で守られるので消えない＝
# 「ふちから繋がった白」だけをflood fillで塗りつぶして透明化する方式。
from PIL import Image, ImageDraw
import os

base = r"C:\Users\cjk13\Documents\Claude\ribe-quest\assets"
mapping = {
    "8eefc5f4-125e-417c-b420-8a89992a9471.png": "jelly.png",   # ぷるるんジェル
    "fa0decda-f620-4b88-ad52-c85a60e6e63c.png": "guard.png",   # アイアンガード
    "06e5ab91-b7b3-4d32-98b5-268632e36f25.png": "imp.png",     # インプデーモン
    "7175276a-be30-470e-b23c-8fdb2856a74d.png": "hero.png",    # 勇者
}
KEY = (255, 0, 255)  # 一時的なキー色（最後に透明へ）

for src, dst in mapping.items():
    p = os.path.join(base, src)
    if not os.path.exists(p):
        print("MISSING", src); continue
    img = Image.open(p).convert("RGB")
    w, h = img.size
    # 画像の縁の各所からflood fill（被写体が縁に触れていても背景を取りこぼさない）
    seeds = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1),
             (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2),
             (3, 3), (w - 4, 3), (3, h - 4), (w - 4, h - 4)]
    for s in seeds:
        try:
            ImageDraw.floodfill(img, s, KEY, thresh=48)  # 白＆アンチエイリアスのにじみまで
        except Exception:
            pass
    # キー色 → 透明
    img = img.convert("RGBA")
    data = img.getdata()
    newdata = [(0, 0, 0, 0) if (px[0] == 255 and px[1] == 0 and px[2] == 255) else px for px in data]
    img.putdata(newdata)
    # 透明な余白を切り詰める（配置しやすく）
    bbox = img.split()[3].getbbox()
    if bbox:
        img = img.crop(bbox)
    out = os.path.join(base, dst)
    img.save(out)
    print("OK", dst, img.size)
