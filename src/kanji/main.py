from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.colors import HexColor
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import argparse

HORI_PADDING = 50
VERT_PADDING = 80

H = 840
V = 595

V_NUM = 8
H_NUM = 8

NAME_FONT_SIZE = 20
BIG_FONT_SIZE = 48

SHIFT = 10


size = (V - HORI_PADDING * 2) / V_NUM
name_size = (H - VERT_PADDING * 2) / H_NUM - size
# フォントの読み込み
FONT_NAME = "UDDigiKyokashoN-R"
pdfmetrics.registerFont(TTFont(FONT_NAME, "/mnt/c/Windows/Fonts/UDDigiKyokashoN-R.ttc"))


def main(file_path, s, big=False):
    page = canvas.Canvas(file_path, pagesize=portrait(A4))
    page.setLineWidth(1)

    gen = (c for c in s)

    stop = False
    page_num = 0
    while not stop:
        page_num += 1

        page.drawCentredString(V / 2, 50, str(page_num))

        for j in range(H_NUM - 1, -1, -1):
            for i in range(V_NUM):
                c = next(gen, None)
                if c is None:
                    stop = True
                    break
                page.rect(
                    HORI_PADDING + i * size,
                    SHIFT + VERT_PADDING + j * (size + name_size),
                    size,
                    size,
                )
                if big:
                    page.setFont(FONT_NAME, BIG_FONT_SIZE)
                    page.setFillColor(HexColor(0xCCCCCC))
                    page.drawCentredString(
                        HORI_PADDING + i * size + size / 2,
                        SHIFT
                        + VERT_PADDING
                        + j * (size + name_size)
                        + size / 2
                        - BIG_FONT_SIZE / 2.7,
                        c,
                    )
                    page.setFillColor(HexColor(0x000000))

                page.rect(
                    HORI_PADDING + i * size,
                    SHIFT + VERT_PADDING + j * (size + name_size) + size,
                    size,
                    name_size,
                )
                page.setFont(FONT_NAME, NAME_FONT_SIZE)
                page.drawCentredString(
                    HORI_PADDING + i * size + size / 2,
                    SHIFT
                    + VERT_PADDING
                    + j * (size + name_size)
                    + size
                    + name_size / 2
                    - NAME_FONT_SIZE / 2.7,
                    c,
                )

            if stop:
                break

        if not stop:
            page.showPage()
    return page


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("--big", help="optional", action="store_true")
    args = parser.parse_args()

    file_name = args.source.replace(".txt", ".pdf")
    if args.big:
        file_name = file_name.replace(".", "-big.")

    with open(args.source) as f:
        s = f.read().replace("\n", "")
    page = main(file_name, s, args.big)
    page.save()
