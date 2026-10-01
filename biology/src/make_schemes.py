# -*- coding: utf-8 -*-
"""Рисует подписанные схемы строения (полихета и пиявка) для слайдов 4 и 7.

Схемы собственные (не чужие изображения): это снимает вопрос лицензии и
гарантирует, что подписи разборчивы и не налезают друг на друга.
"""
from PIL import Image, ImageDraw, ImageFont
import os

S = 2  # супер-сэмплинг для гладких линий
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "photos")

_BOXES = []  # рамки подписей — для проверки пересечений


def font(sz, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), int(round(sz * S)))


def line(d, p1, p2, color, w=3):
    d.line([p1[0] * S, p1[1] * S, p2[0] * S, p2[1] * S], fill=color, width=int(round(w * S)))


def ellipse(d, box, fill=None, outline=None, w=3):
    d.ellipse([box[0] * S, box[1] * S, box[2] * S, box[3] * S],
              fill=fill, outline=outline, width=int(round(w * S)))


def poly(d, pts, fill=None, outline=None, w=3):
    d.polygon([(x * S, y * S) for x, y in pts], fill=fill, outline=outline,
              width=int(round(w * S)))


def rrect(d, box, radius, fill=None, outline=None, w=3):
    d.rounded_rectangle([box[0] * S, box[1] * S, box[2] * S, box[3] * S],
                        radius=radius * S, fill=fill, outline=outline, width=int(round(w * S)))


def trim(im, margin=16):
    """Обрезает белые поля, оставляя небольшой отступ."""
    from PIL import ImageChops
    bg = Image.new("RGB", im.size, (255, 255, 255))
    bb = ImageChops.difference(im, bg).convert("L").point(lambda p: 255 if p > 12 else 0).getbbox()
    if not bb:
        return im
    x0, y0, x1, y1 = bb
    x0, y0 = max(0, x0 - margin), max(0, y0 - margin)
    x1, y1 = min(im.size[0], x1 + margin), min(im.size[1], y1 + margin)
    return im.crop((x0, y0, x1, y1))


def label(d, text, xy, target, f, color, side="left"):
    """Подпись с выноской к элементу схемы. side задаёт, с какой стороны текст."""
    d.text((xy[0] * S, xy[1] * S), text, font=f, fill=color)
    x0, y0, x1, y1 = [v / S for v in d.textbbox((xy[0] * S, xy[1] * S), text, font=f)]
    _BOXES.append((x0, y0, x1, y1, text))
    start = (x1 + 8, (y0 + y1) / 2) if side == "left" else (x0 - 8, (y0 + y1) / 2)
    line(d, start, target, color, 2)
    ellipse(d, (target[0] - 4, target[1] - 4, target[0] + 4, target[1] + 4), fill=color)


# ---------------------------------------------------------------- полихета
def draw_polychaete(path):
    _BOXES.clear()
    W, H = 1600, 1100
    im = Image.new("RGB", (W * S, H * S), (255, 255, 255))
    d = ImageDraw.Draw(im)
    OUTL, FILL, ACC = (31, 111, 120), (223, 239, 242), (139, 189, 190)
    DARK, TXT = (55, 55, 55), (18, 52, 58)
    f, fb = font(30), font(30, bold=True)

    # --- верх: червь целиком, вид сбоку ---
    cy = 250
    ellipse(d, (80, cy - 78, 250, cy + 78), fill=ACC, outline=OUTL, w=3)      # головная лопасть
    ellipse(d, (120, cy - 46, 152, cy - 14), fill=DARK)                       # глаз
    ellipse(d, (120, cy + 14, 152, cy + 46), fill=DARK)                       # глаз
    for dy in (-58, -30, 30, 58):                                             # щупальца
        line(d, (92, cy + dy * 0.55), (34, cy + dy), OUTL, 3)
    rrect(d, (232, cy - 60, 1350, cy + 60), 58, fill=FILL, outline=OUTL, w=3)  # туловище
    for x in range(340, 1300, 105):                                           # сегменты
        line(d, (x, cy - 56), (x, cy + 56), ACC, 2)
    for x in range(390, 1180, 105):                                           # параподии
        for sgn in (-1, 1):
            y0, y1 = cy + sgn * 55, cy + sgn * 95
            ellipse(d, (x - 32, min(y0, y1), x + 32, max(y0, y1)), fill=ACC, outline=OUTL, w=2)
            for a in (-26, -9, 9, 26):
                line(d, (x + a * 0.6, cy + sgn * 88), (x + a, cy + sgn * 132), DARK, 2)
    ellipse(d, (1330, cy - 48, 1440, cy + 48), fill=ACC, outline=OUTL, w=3)   # анальная лопасть

    label(d, "Головная лопасть", (20, 24), (176, cy - 70), fb, TXT)
    label(d, "Глаза", (20, 82), (136, cy - 30), f, TXT)
    label(d, "Щупальца", (20, 140), (66, cy - 30), f, TXT)
    label(d, "Сегменты тела", (620, 24), (760, cy - 58), fb, TXT)
    label(d, "Параподии", (1000, 24), (1035, cy - 90), fb, TXT)
    label(d, "Щетинки", (1270, 24), (1200, cy - 125), f, TXT)
    label(d, "Анальная лопасть", (1150, 380), (1385, cy + 46), fb, TXT)

    line(d, (60, 470), (1540, 470), (210, 224, 226), 2)

    # --- низ: строение параподия (поперечный разрез) ---
    rrect(d, (300, 560, 440, 1010), 26, fill=ACC, outline=OUTL, w=3)          # стенка тела
    rrect(d, (322, 585, 418, 985), 16, fill=(255, 255, 255), outline=OUTL, w=2)
    poly(d, [(440, 610), (700, 596), (900, 650), (900, 730), (700, 742), (440, 720)],
         fill=FILL, outline=OUTL, w=3)                                        # нотоподий
    poly(d, [(440, 850), (700, 838), (900, 890), (900, 962), (700, 974), (440, 940)],
         fill=FILL, outline=OUTL, w=3)                                        # невроподий
    ellipse(d, (470, 540, 610, 610), fill=ACC, outline=OUTL, w=2)             # спинной усик
    ellipse(d, (470, 962, 610, 1032), fill=ACC, outline=OUTL, w=2)            # брюшной усик
    for a in (-38, -13, 13, 38):                                              # щетинки
        line(d, (895, 688 + a * 0.5), (1010, 688 + a), DARK, 3)
        line(d, (895, 926 + a * 0.5), (1010, 926 + a), DARK, 3)

    label(d, "Спинной усик", (1060, 512), (546, 566), fb, TXT)
    label(d, "Нотоподий", (1060, 632), (700, 646), f, TXT)
    label(d, "Щетинки", (1060, 752), (960, 660), f, TXT)
    label(d, "Невроподий", (1060, 872), (700, 890), f, TXT)
    label(d, "Брюшной усик", (1060, 992), (546, 1000), fb, TXT)
    label(d, "Стенка тела", (20, 700), (306, 780), f, TXT)
    label(d, "Полость тела", (20, 860), (368, 860), f, TXT)

    trim(im.resize((W, H), Image.LANCZOS)).save(path)
    return W, H


# ------------------------------------------------------------------- пиявка
def draw_leech(path):
    _BOXES.clear()
    W, H = 1100, 1500
    im = Image.new("RGB", (W * S, H * S), (255, 255, 255))
    d = ImageDraw.Draw(im)
    OUTL, FILL, ACC = (150, 40, 80), (250, 233, 238), (226, 160, 180)
    DARK, TXT = (70, 30, 45), (74, 20, 42)
    f, fb = font(30), font(30, bold=True)
    cx = 400

    ellipse(d, (cx - 110, 120, cx + 110, 340), fill=ACC, outline=OUTL, w=3)   # передняя присоска
    ellipse(d, (cx - 46, 190, cx + 46, 282), fill=(255, 255, 255), outline=OUTL, w=2)
    ellipse(d, (cx - 26, 214, cx + 26, 258), fill=DARK)                       # ротовое отверстие
    ellipse(d, (cx - 128, 1160, cx + 128, 1416), fill=ACC, outline=OUTL, w=3)  # задняя присоска
    ellipse(d, (cx - 66, 1218, cx + 66, 1358), fill=(255, 255, 255), outline=OUTL, w=2)
    rrect(d, (cx - 92, 300, cx + 92, 1200), 46, fill=FILL, outline=OUTL, w=3)  # туловище
    for y in range(340, 1170, 26):                                            # кольца
        line(d, (cx - 90, y), (cx + 90, y), ACC, 2)
    rrect(d, (cx - 96, 620, cx + 96, 780), 20, fill=ACC, outline=OUTL, w=2)    # поясок
    for y in range(430, 1150, 78):                                            # папиллы
        for sgn in (-1, 1):
            ellipse(d, (cx + sgn * 92 - 6, y - 6, cx + sgn * 92 + 6, y + 6), fill=DARK)

    label(d, "Передняя присоска", (20, 30), (cx - 100, 190), fb, TXT)
    label(d, "Ротовое отверстие", (20, 92), (cx - 30, 236), f, TXT)
    label(d, "Кольца", (20, 900), (cx - 90, 900), f, TXT)
    label(d, "Папиллы", (20, 962), (cx - 92, 1010), f, TXT)
    label(d, "Задняя присоска", (20, 1330), (cx - 126, 1300), fb, TXT)
    label(d, "Поясок", (560, 640), (cx + 96, 700), fb, TXT)
    label(d, "Половые отверстия", (560, 762), (cx + 96, 800), f, TXT)

    trim(im.resize((W, H), Image.LANCZOS)).save(path)
    return W, H


def check():
    """Сообщает о подписях, которые вылезают за картинку или пересекаются."""
    problems = []
    for i in range(len(_BOXES)):
        x0, y0, x1, y1, t = _BOXES[i]
        if x0 < 0 or y0 < 0 or x1 > 1600 or y1 > 1600:
            problems.append(f"вылезает за край: {t}")
        for j in range(i + 1, len(_BOXES)):
            a0, b0, a1, b1, u = _BOXES[j]
            if x0 < a1 and a0 < x1 and y0 < b1 and b0 < y1:
                problems.append(f"пересечение: «{t}» и «{u}»")
    return problems


if __name__ == "__main__":
    print("полихета:", draw_polychaete(os.path.join(OUT, "polychaete_scheme_ru.png")))
    print("пиявка:", draw_leech(os.path.join(OUT, "leech_scheme_ru.png")))
    p = check()
    print("проблем с подписями:", len(p))
    for x in p:
        print("  -", x)
