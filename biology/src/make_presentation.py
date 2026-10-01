# -*- coding: utf-8 -*-
"""Генерация презентации «Многощетинковые черви. Пиявки» для урока биологии (8 класс)."""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
import copy

# ----------------------------------------------------------------------------
# Палитра и константы дизайна
# ----------------------------------------------------------------------------
DEEP_SEA   = RGBColor(0x0B, 0x2E, 0x4F)   # тёмно-синий (глубина моря)
OCEAN      = RGBColor(0x11, 0x5A, 0x8C)   # океанический синий
TEAL       = RGBColor(0x17, 0x9E, 0xA0)   # бирюзовый
MINT       = RGBColor(0x5F, 0xC9, 0xA6)   # мятно-зелёный
LEECH_ROSE = RGBColor(0xC0, 0x3A, 0x5B)   # малиновый (пиявки)
SAND       = RGBColor(0xF3, 0xEC, 0xDD)   # песочный фон
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
INK        = RGBColor(0x1C, 0x2B, 0x39)   # почти чёрный текст
GREY       = RGBColor(0x5A, 0x6B, 0x7B)
LIGHT_BLUE = RGBColor(0xE4, 0xF0, 0xF7)
LIGHT_ROSE = RGBColor(0xFA, 0xE6, 0xEA)
LIGHT_MINT = RGBColor(0xE6, 0xF5, 0xEE)
GOLD       = RGBColor(0xE8, 0xA8, 0x3A)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

import os as _os
_ASSETS = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "photos")
SCHEME_POLYCHAETE = _os.path.join(_ASSETS, "polychaete_scheme_ru.png")
SCHEME_LEECH = _os.path.join(_ASSETS, "leech_scheme_ru.png")

prs = Presentation()
prs.slide_width = SLIDE_W
prs.slide_height = SLIDE_H
BLANK = prs.slide_layouts[6]


# ----------------------------------------------------------------------------
# Вспомогательные функции
# ----------------------------------------------------------------------------
def add_slide():
    return prs.slides.add_slide(BLANK)


def set_bg(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def rect(slide, x, y, w, h, color, line=None, shape=MSO_SHAPE.RECTANGLE):
    shp = slide.shapes.add_shape(shape, x, y, w, h)
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(1.25)
    shp.shadow.inherit = False
    return shp


def textbox(slide, x, y, w, h, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    return tb, tf


def style_run(run, size=18, color=INK, bold=False, italic=False, font="Calibri"):
    run.font.size = Pt(size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.italic = italic
    run.font.name = font


def para(tf, text, size=18, color=INK, bold=False, italic=False,
         align=PP_ALIGN.LEFT, space_after=6, space_before=0, first=False,
         level=0, font="Calibri"):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    p.space_after = Pt(space_after)
    p.space_before = Pt(space_before)
    p.level = level
    run = p.add_run()
    run.text = text
    style_run(run, size, color, bold, italic, font)
    return p


def bullet(tf, text, size=17, color=INK, bold_lead=None, first=False,
           space_after=8, marker="•", marker_color=None, level=0):
    """Пункт списка с цветным маркером; bold_lead — часть до двоеточия выделяется."""
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.space_after = Pt(space_after)
    p.level = level
    mc = marker_color if marker_color else TEAL
    r0 = p.add_run()
    r0.text = marker + "  "
    style_run(r0, size, mc, True)
    if bold_lead:
        r1 = p.add_run()
        r1.text = bold_lead
        style_run(r1, size, color, True)
    r2 = p.add_run()
    r2.text = text
    style_run(r2, size, color, False)
    return p


def header(slide, title, accent=TEAL, kicker=None):
    """Верхняя плашка с заголовком слайда."""
    rect(slide, 0, 0, SLIDE_W, Inches(1.15), DEEP_SEA)
    rect(slide, 0, Inches(1.15), SLIDE_W, Inches(0.08), accent)
    tb, tf = textbox(slide, Inches(0.6), Inches(0.12), Inches(11.5), Inches(0.95),
                     anchor=MSO_ANCHOR.MIDDLE)
    if kicker:
        para(tf, kicker.upper(), size=12, color=MINT, bold=True, first=True, space_after=2)
        para(tf, title, size=27, color=WHITE, bold=True, space_after=0)
    else:
        para(tf, title, size=28, color=WHITE, bold=True, first=True, space_after=0)


def footer(slide, text="Многощетинковые черви. Пиявки  •  8 класс"):
    tb, tf = textbox(slide, Inches(0.6), Inches(7.0), Inches(9), Inches(0.4))
    para(tf, text, size=10, color=GREY, first=True, space_after=0)


def card(slide, x, y, w, h, fill, accent, title, lines,
         title_size=17, body_size=14):
    """Карточка-плашка с цветной полосой сверху."""
    box = rect(slide, x, y, w, h, fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    box.adjustments[0] = 0.06
    rect(slide, x, y, w, Inches(0.12), accent)
    tb, tf = textbox(slide, x + Inches(0.25), y + Inches(0.28),
                     w - Inches(0.5), h - Inches(0.45))
    para(tf, title, size=title_size, color=accent, bold=True, first=True, space_after=8)
    for ln in lines:
        para(tf, ln, size=body_size, color=INK, space_after=5)
    return box


def add_photo(slide, path, x, y, w, h):
    """Вставляет фотографию, вписывая её в заданный прямоугольник по центру."""
    from PIL import Image
    iw, ih = Image.open(path).size
    box_ratio = w / h
    img_ratio = iw / ih
    if img_ratio > box_ratio:
        pw, ph = w, int(w / img_ratio)
    else:
        ph, pw = h, int(h * img_ratio)
    px = x + (w - pw) / 2
    py = y + (h - ph) / 2
    return slide.shapes.add_picture(path, px, py, pw, ph)


def scheme_panel(slide, path, x, y, w, h, border=None):
    """Белая панель с подписанной схемой строения."""
    rect(slide, x, y, w, h, WHITE, line=border or LIGHT_BLUE,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    pad = Inches(0.16)
    add_photo(slide, path, x + pad, y + pad, w - 2 * pad, h - 2 * pad)


def fact_badge(slide, x, y, num, color):
    c = rect(slide, x, y, Inches(0.6), Inches(0.6), color, shape=MSO_SHAPE.OVAL)
    tf = c.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = str(num)
    style_run(r, 22, WHITE, True)
    return c


# ============================================================================
# СЛАЙД 1 — Титульный
# ============================================================================
s = add_slide()
set_bg(s, DEEP_SEA)
# декоративные волны/сегменты
rect(s, 0, Inches(5.7), SLIDE_W, Inches(1.8), OCEAN)
rect(s, 0, Inches(5.7), SLIDE_W, Inches(0.09), TEAL)
for i in range(11):
    x = Inches(0.7 + i * 1.15)
    rect(s, x, Inches(6.15), Inches(0.75), Inches(0.75), MINT, shape=MSO_SHAPE.OVAL)

tb, tf = textbox(s, Inches(0.9), Inches(1.35), Inches(11.5), Inches(3.6))
para(tf, "УРОК БИОЛОГИИ  •  8 КЛАСС", size=16, color=MINT, bold=True,
     first=True, space_after=14)
para(tf, "Многощетинковые черви", size=52, color=WHITE, bold=True, space_after=0)
para(tf, "Пиявки", size=52, color=TEAL, bold=True, space_after=18)
para(tf, "Строение, среда обитания, размножение и роль в природе",
     size=20, color=RGBColor(0xC9, 0xDD, 0xE8), italic=True, space_after=0)

tb, tf = textbox(s, Inches(0.9), Inches(6.05), Inches(11), Inches(1.1))
para(tf, "Тип Кольчатые черви  (Annelida)", size=16, color=WHITE, bold=True,
     first=True, space_after=2)
para(tf, "Классы: Многощетинковые (Polychaeta) и Поясковые (Clitellata — пиявки)",
     size=13, color=RGBColor(0xAE, 0xC9, 0xD8), space_after=0)


# ============================================================================
# СЛАЙД 2 — План урока
# ============================================================================
s = add_slide()
set_bg(s, SAND)
header(s, "План урока", accent=TEAL, kicker="Сегодня разберём")

items = [
    ("1", "Многощетинковые черви", "Среда обитания и внешнее строение", TEAL),
    ("2", "Параподии — «вёсла» и «жабры»", "Как полихеты двигаются и дышат", OCEAN),
    ("3", "Размножение полихет", "Раздельнополые, развитие с личинкой", MINT),
    ("4", "Пиявки", "Среда обитания, присоски, гирудин", LEECH_ROSE),
    ("5", "Размножение пиявок", "Гермафродиты, прямое развитие", RGBColor(0xA8, 0x2C, 0x4A)),
    ("6", "Сравнение и выводы", "Черви, интересные факты о полихетах и пиявках", GOLD),
]
y0 = Inches(1.65)
for i, (num, t, sub, col) in enumerate(items):
    yy = y0 + Inches(0.85) * i
    fact_badge(s, Inches(1.0), yy, num, col)
    tb, tf = textbox(s, Inches(1.9), yy - Inches(0.05), Inches(10.6), Inches(0.8),
                     anchor=MSO_ANCHOR.MIDDLE)
    para(tf, t, size=19, color=DEEP_SEA, bold=True, first=True, space_after=1)
    para(tf, sub, size=13, color=GREY, space_after=0)
footer(s)


# ============================================================================
# СЛАЙД 3 — Многощетинковые черви: среда обитания
# ============================================================================
s = add_slide()
set_bg(s, WHITE)
header(s, "Многощетинковые черви: где живут", accent=TEAL, kicker="Класс Polychaeta")
# левый блок
card(s, Inches(0.6), Inches(1.7), Inches(6.0), Inches(4.9), LIGHT_BLUE, TEAL,
     "Среда обитания",
     ["Преимущественно морские воды — солёная среда.",
      "Живут на дне (бентос) или в толще воды (планктон).",
      "Встречаются от прибрежного мелководья до глубин океана.",
      "Прячутся в грунте, норках, трубках или среди рифов."],
     title_size=20, body_size=16)
# правая инфографика
rect(s, Inches(6.9), Inches(1.7), Inches(5.8), Inches(4.9), DEEP_SEA,
     shape=MSO_SHAPE.ROUNDED_RECTANGLE)
tb, tf = textbox(s, Inches(7.2), Inches(2.0), Inches(5.2), Inches(4.3))
para(tf, "Почему именно море?", size=20, color=MINT, bold=True, first=True, space_after=14)
for t in ["Солёная вода поддерживает тело и помогает плавать.",
          "Обилие пищи: планктон, органические остатки на дне.",
          "Разнообразие «профессий»: ползающие, плавающие, сидячие формы.",
          "Именно полихеты — самые древние и многочисленные кольчецы."]:
    bullet(tf, t, size=15, color=RGBColor(0xDD, 0xEA, 0xF2),
           marker="→", marker_color=GOLD, space_after=12)
footer(s)


# ============================================================================
# СЛАЙД 4 — Внешнее строение полихет
# ============================================================================
s = add_slide()
set_bg(s, WHITE)
header(s, "Внешнее строение полихеты", accent=TEAL, kicker="Главная «фишка» — параподии")
card(s, Inches(0.6), Inches(1.7), Inches(6.1), Inches(2.3), LIGHT_BLUE, OCEAN,
     "Отделы тела",
     ["Головная лопасть — глаза и щупальца для ориентации.",
      "Туловище — множество сегментов (кольцев).",
      "Анальная лопасть — завершает тело."],
     title_size=18, body_size=15)
card(s, Inches(0.6), Inches(4.2), Inches(6.1), Inches(2.4), LIGHT_MINT, MINT,
     "Параподии",
     ["Боковые выросты на каждом сегменте с пучками щетинок.",
      "Работают как «вёсла» — помогают двигаться.",
      "Работают как жабры — участвуют в дыхании.",
      "Именно по ним класс получил название «многощетинковые»."],
     title_size=18, body_size=15)
# схема строения с русскими подписями справа
scheme_panel(s, SCHEME_POLYCHAETE, Inches(7.0), Inches(1.7), Inches(5.7), Inches(4.9), border=TEAL)
tb, tf = textbox(s, Inches(7.0), Inches(6.62), Inches(5.7), Inches(0.5))
para(tf, "Схема: головная и анальная лопасти, сегменты, параподии со щетинками, спинной и брюшной усики.",
     size=9, color=GREY, italic=True, first=True, space_after=0)
footer(s)


# ============================================================================
# СЛАЙД 5 — Размножение полихет
# ============================================================================
s = add_slide()
set_bg(s, WHITE)
header(s, "Размножение полихет", accent=MINT, kicker="Непрямое развитие")
card(s, Inches(0.6), Inches(1.7), Inches(5.7), Inches(4.9), LIGHT_MINT, MINT,
     "Особенности",
     ["Раздельнополые животные (есть самцы и самки).",
      "Половые клетки выметываются прямо в воду.",
      "Оплодотворение наружное — в морской воде.",
      "Развитие непрямое: есть стадия личинки."],
     title_size=20, body_size=16)
# схема этапов
rect(s, Inches(6.6), Inches(1.7), Inches(6.1), Inches(4.9), LIGHT_BLUE,
     shape=MSO_SHAPE.ROUNDED_RECTANGLE)
tb, tf = textbox(s, Inches(6.9), Inches(1.95), Inches(5.5), Inches(0.6))
para(tf, "Путь развития", size=18, color=OCEAN, bold=True, first=True, space_after=0)
stages = [
    ("Яйцо", "в воде"),
    ("Личинка", "плавает, не похожа на взрослого"),
    ("Молодой червь", "оседает на дно"),
    ("Взрослая особь", "растёт и сегментируется"),
]
sy = Inches(2.75)
for i, (t, sub) in enumerate(stages):
    yy = sy + Inches(0.95) * i
    col = TEAL if i % 2 == 0 else OCEAN
    c = rect(s, Inches(7.0), yy, Inches(0.55), Inches(0.55), col, shape=MSO_SHAPE.OVAL)
    ctf = c.text_frame
    pp = ctf.paragraphs[0]
    pp.alignment = PP_ALIGN.CENTER
    rr = pp.add_run(); rr.text = str(i + 1); style_run(rr, 18, WHITE, True)
    tb, tf = textbox(s, Inches(7.8), yy - Inches(0.06), Inches(4.6), Inches(0.75),
                     anchor=MSO_ANCHOR.MIDDLE)
    para(tf, t, size=16, color=DEEP_SEA, bold=True, first=True, space_after=0)
    para(tf, sub, size=12, color=GREY, space_after=0)
    if i < 3:
        rect(s, Inches(7.24), yy + Inches(0.6), Inches(0.07), Inches(0.35), MINT)
footer(s)


# ============================================================================
# СЛАЙД 6 — Пиявки: среда обитания
# ============================================================================
s = add_slide()
set_bg(s, WHITE)
header(s, "Пиявки: где живут", accent=LEECH_ROSE, kicker="Класс Поясковые")
card(s, Inches(0.6), Inches(1.7), Inches(6.0), Inches(4.9), LIGHT_ROSE, LEECH_ROSE,
     "Среда обитания",
     ["В основном пресные водоёмы: реки, озёра, пруды.",
      "Некоторые виды — во влажной почве тропиков.",
      "Есть и морские формы.",
      "Предпочитают чистую воду, богатую кислородом."],
     title_size=20, body_size=16)
rect(s, Inches(6.9), Inches(1.7), Inches(5.8), Inches(4.9), RGBColor(0x4A, 0x12, 0x22),
     shape=MSO_SHAPE.ROUNDED_RECTANGLE)
tb, tf = textbox(s, Inches(7.2), Inches(2.0), Inches(5.2), Inches(4.3))
para(tf, "Важно понимать", size=20, color=RGBColor(0xF2, 0xB8, 0xC6), bold=True,
     first=True, space_after=14)
for t in ["Пиявки — не только паразиты: многие ведут хищный образ жизни.",
          "Они дышат всей поверхностью тела — жабр нет.",
          "Тело уплощённое и очень гибкое — удобно прятаться.",
          "Живут в воде, но могут подолгу обходиться без неё."]:
    bullet(tf, t, size=15, color=RGBColor(0xF7, 0xE2, 0xE8),
           marker="→", marker_color=GOLD, space_after=12)
footer(s)


# ============================================================================
# СЛАЙД 7 — Внешнее строение пиявок
# ============================================================================
s = add_slide()
set_bg(s, WHITE)
header(s, "Внешнее строение пиявки", accent=LEECH_ROSE, kicker="Две присоски — две точки опоры")
card(s, Inches(0.6), Inches(1.7), Inches(6.1), Inches(2.3), LIGHT_ROSE, LEECH_ROSE,
     "Тело",
     ["Уплощённое, сегментированное.",
      "Без щетинок и без параподий — не как у полихет.",
      "Очень эластичное и растяжимое."],
     title_size=18, body_size=15)
card(s, Inches(0.6), Inches(4.2), Inches(6.1), Inches(2.4), LIGHT_MINT, TEAL,
     "Присоски",
     ["Передняя — с ротовым отверстием и хитиновыми зубчиками.",
      "Задняя — для прочного прикрепления к жертве или дну.",
      "Позволяют передвигаться «шагами» и удерживаться."],
     title_size=18, body_size=15)
# схема внешнего строения с русскими подписями
scheme_panel(s, SCHEME_LEECH, Inches(7.0), Inches(1.7), Inches(5.7), Inches(4.9), border=LEECH_ROSE)
tb, tf = textbox(s, Inches(7.0), Inches(6.62), Inches(5.7), Inches(0.5))
para(tf, "Схема строения пиявки: передняя и задняя присоски, поясок, половые отверстия, папиллы.",
     size=9, color=GREY, italic=True, first=True, space_after=0)
footer(s)


# ============================================================================
# СЛАЙД 8 — Внутреннее строение пиявок
# ============================================================================
s = add_slide()
set_bg(s, WHITE)
header(s, "Внутреннее строение и гирудин", accent=LEECH_ROSE, kicker="Секрет слюнных желез")
card(s, Inches(0.6), Inches(1.7), Inches(6.0), Inches(2.3), LIGHT_ROSE, LEECH_ROSE,
     "Полость тела",
     ["Вторичная полость (целом) сильно заросла соединительной тканью.",
      "Остались лишь небольшие каналы.",
      "Такое строение делает тело плотным и гибким."],
     title_size=18, body_size=15)
card(s, Inches(0.6), Inches(4.2), Inches(6.0), Inches(2.4), LIGHT_MINT, TEAL,
     "Гирудин",
     ["Вырабатывается в слюнных железах.",
      "Препятствует свёртыванию крови жертвы.",
      "Кровь течёт свободно, пока пиявка питается."],
     title_size=18, body_size=15)
rect(s, Inches(6.9), Inches(1.7), Inches(5.8), Inches(4.9), DEEP_SEA,
     shape=MSO_SHAPE.ROUNDED_RECTANGLE)
tb, tf = textbox(s, Inches(7.2), Inches(2.0), Inches(5.2), Inches(4.3))
para(tf, "Медицинское значение", size=20, color=MINT, bold=True, first=True, space_after=14)
for t in ["Гирудотерапия — лечение с помощью пиявок.",
          "Применяется после сложных пластических операций.",
          "Гирудин не даёт крови сворачиваться в месте шва.",
          "Это предотвращает тромбы, снимает отёк и улучшает питание тканей."]:
    bullet(tf, t, size=15, color=RGBColor(0xDD, 0xEA, 0xF2),
           marker="✚", marker_color=GOLD, space_after=12)
footer(s)


# ============================================================================
# СЛАЙД 9 — Размножение пиявок
# ============================================================================
s = add_slide()
set_bg(s, WHITE)
header(s, "Размножение пиявок", accent=MINT, kicker="Прямое развитие")
card(s, Inches(0.6), Inches(1.7), Inches(5.7), Inches(4.9), LIGHT_MINT, MINT,
     "Особенности",
     ["Гермафродиты — как дождевые черви.",
      "Оплодотворение перекрёстное.",
      "Яйца откладываются в кокон.",
      "Развитие прямое — без личинки."],
     title_size=20, body_size=16)
rect(s, Inches(6.6), Inches(1.7), Inches(6.1), Inches(4.9), LIGHT_BLUE,
     shape=MSO_SHAPE.ROUNDED_RECTANGLE)
tb, tf = textbox(s, Inches(6.9), Inches(1.95), Inches(5.5), Inches(0.6))
para(tf, "Путь развития", size=18, color=OCEAN, bold=True, first=True, space_after=0)
stages = [
    ("Яйцо в коконе", "защищено от внешней среды"),
    ("Маленький червь", "выходит из кокона"),
    ("Взрослая особь", "похожа на родителя"),
]
sy = Inches(2.9)
for i, (t, sub) in enumerate(stages):
    yy = sy + Inches(1.15) * i
    col = TEAL if i % 2 == 0 else OCEAN
    c = rect(s, Inches(7.0), yy, Inches(0.55), Inches(0.55), col, shape=MSO_SHAPE.OVAL)
    ctf = c.text_frame
    pp = ctf.paragraphs[0]; pp.alignment = PP_ALIGN.CENTER
    rr = pp.add_run(); rr.text = str(i + 1); style_run(rr, 18, WHITE, True)
    tb, tf = textbox(s, Inches(7.8), yy - Inches(0.06), Inches(4.6), Inches(0.85),
                     anchor=MSO_ANCHOR.MIDDLE)
    para(tf, t, size=16, color=DEEP_SEA, bold=True, first=True, space_after=0)
    para(tf, sub, size=12, color=GREY, space_after=0)
    if i < 2:
        rect(s, Inches(7.24), yy + Inches(0.6), Inches(0.07), Inches(0.5), MINT)
footer(s)


# ============================================================================
# СЛАЙД 10 — Сравнительная таблица
# ============================================================================
s = add_slide()
set_bg(s, SAND)
header(s, "Сравнение: полихеты и пиявки", accent=GOLD, kicker="Найдите отличия")

rows, cols = 7, 3
left, top = Inches(0.7), Inches(1.6)
width, height = Inches(11.9), Inches(5.0)
table = s.shapes.add_table(rows, cols, left, top, width, height).table
table.columns[0].width = Inches(3.2)
table.columns[1].width = Inches(4.35)
table.columns[2].width = Inches(4.35)

data = [
    ("Признак", "Многощетинковые черви", "Пиявки"),
    ("Среда обитания", "Моря (солёная вода), дно и толща", "Пресные водоёмы, реже почва и море"),
    ("Щетинки и параподии", "Есть — пучки на каждом сегменте", "Отсутствуют"),
    ("Присоски", "Нет", "Две: передняя и задняя"),
    ("Пол и размножение", "Раздельнополые", "Гермафродиты"),
    ("Развитие", "Непрямое — с личинкой", "Прямое — без личинки"),
    ("Особая черта", "Параподии — «вёсла» и жабры", "Гирудин — против свёртывания крови"),
]
for r in range(rows):
    for c in range(cols):
        cell = table.cell(r, c)
        cell.margin_left = Inches(0.12)
        cell.margin_right = Inches(0.08)
        cell.margin_top = Inches(0.04)
        cell.margin_bottom = Inches(0.04)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf = cell.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = data[r][c]
        if r == 0:
            style_run(run, 15, WHITE, True)
            cell.fill.solid(); cell.fill.fore_color.rgb = DEEP_SEA
        else:
            if c == 0:
                style_run(run, 14, DEEP_SEA, True)
                cell.fill.solid(); cell.fill.fore_color.rgb = RGBColor(0xE9, 0xDF, 0xC9)
            elif c == 1:
                style_run(run, 14, INK, False)
                cell.fill.solid(); cell.fill.fore_color.rgb = LIGHT_BLUE
            else:
                style_run(run, 14, INK, False)
                cell.fill.solid(); cell.fill.fore_color.rgb = LIGHT_ROSE
footer(s)


# ============================================================================
# СЛАЙД 11 — Интересные факты: полихеты
# ============================================================================
s = add_slide()
set_bg(s, WHITE)
header(s, "Интересные факты: полихеты", accent=TEAL, kicker="Удивительное рядом")
facts = [
    ("Морские гиганты", "Некоторые тропические многощетинковые черви достигают 3 метров в длину!", TEAL),
    ("Оптические волокна природы", "Червь «морская мышь» покрыт переливающимися щетинками: они как природные оптоволокна отражают свет и меняют цвет от синего до золотого, отпугивая хищников.", OCEAN),
    ("Светящиеся черви", "Многие глубоководные полихеты обладают биолюминесценцией: при опасности они «отстреливают» светящиеся части тела, чтобы ослепить врага.", MINT),
]
y0 = Inches(1.7)
for i, (t, d, col) in enumerate(facts):
    yy = y0 + Inches(1.65) * i
    rect(s, Inches(0.7), yy, Inches(11.9), Inches(1.45), LIGHT_BLUE,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    fact_badge(s, Inches(1.0), yy + Inches(0.4), i + 1, col)
    tb, tf = textbox(s, Inches(1.95), yy + Inches(0.16), Inches(10.4), Inches(1.15))
    para(tf, t, size=18, color=col, bold=True, first=True, space_after=4)
    para(tf, d, size=14, color=INK, space_after=0)
footer(s)


# ============================================================================
# СЛАЙД 12 — Интересные факты: пиявки
# ============================================================================
s = add_slide()
set_bg(s, WHITE)
header(s, "Интересные факты: пиявки", accent=LEECH_ROSE, kicker="Не всё так очевидно")
facts = [
    ("Не все пьют кровь", "Далеко не все пиявки — паразиты. Многие из них активные хищники: охотятся на улиток, личинок насекомых и других червей, заглатывая добычу целиком.", LEECH_ROSE),
    ("Рекордсмены по обжорству", "Медицинская пиявка может выпить крови в 5–10 раз больше собственного веса, а затем переваривать её и не питаться несколько месяцев.", RGBColor(0xA8, 0x2C, 0x4A)),
    ("Живые индикаторы", "Медицинская пиявка занесена в Красную книгу. Она очень чувствительна к загрязнению: если в водоёме живут пиявки — вода там относительно чистая.", GOLD),
]
y0 = Inches(1.7)
for i, (t, d, col) in enumerate(facts):
    yy = y0 + Inches(1.65) * i
    rect(s, Inches(0.7), yy, Inches(11.9), Inches(1.45), LIGHT_ROSE,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    fact_badge(s, Inches(1.0), yy + Inches(0.4), i + 1, col)
    tb, tf = textbox(s, Inches(1.95), yy + Inches(0.16), Inches(10.4), Inches(1.15))
    para(tf, t, size=18, color=col, bold=True, first=True, space_after=4)
    para(tf, d, size=14, color=INK, space_after=0)
footer(s)

# ============================================================================
# Вопрос к классу (по слайдам)
# ============================================================================
QUESTIONS = {
    1: "Дождевой червь — знакомый нам кольчатый червь. А где ещё в природе живут кольчатые черви?",
    2: "Кто из вас видел пиявку? Где это было — в пруду, в речке, в озере?",
    3: "Почему многощетинковые черви живут в море, а не в почве, как дождевой червь?",
    4: "Зачем червю на каждом сегменте параподии со щетинками — что они делают?",
    5: "Чем развитие с личинкой отличается от прямого развития, как у дождевого червя?",
    6: "Пиявка — это всегда паразит, который пьёт кровь, или бывает иначе?",
    7: "Почему одной присоски, как у осьминога, пиявке было бы недостаточно?",
    8: "Пиявка вводит гирудин, чтобы кровь не сворачивалась. Почему же тогда она не истекает кровью сама?",
    9: "Кто такие гермафродиты? Вспомните, у кого из знакомых животных так же.",
    10: "Найдите главное отличие: как по строению отличить полихету от пиявки?",
    11: "Какой из трёх фактов про полихет удивил вас больше всего и почему?",
    12: "Почему пиявку называют «живым индикатором» чистой воды?",
}

for idx, slide in enumerate(prs.slides, 1):
    if idx in QUESTIONS:
        slide.notes_slide.notes_text_frame.text = QUESTIONS[idx]

prs.save("/workspace/project/Многощетинковые_черви_и_пиявки.pptx")
print("Готово! Слайдов:", len(prs.slides._sldIdLst))
