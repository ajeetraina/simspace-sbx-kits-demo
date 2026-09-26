#!/usr/bin/env python3
"""Docker /Next slide theme — the dark IBM Plex Mono look.

Matches the "Docker does that?!" WeAreDevelopers 2026 deck: near-black navy
surface with a faint hexagon weave, monospace type, white cards that sit on a
hard offset shadow, one Docker-blue accent, and the real Docker mark bottom-right.

Slides are authored as SVG (1600x900) -> PNG (rsvg-convert) -> .webp (cwebp).
"""
import math

# ---- palette ---------------------------------------------------------------
BG      = "#0F1626"    # main surface
BG2     = "#0B111E"    # panel / darker
HEXCOL  = "#26365A"    # hexagon weave
WHITE   = "#FFFFFF"
MUTE    = "#9AA9C9"    # body text on dark
MUTE2   = "#66769B"    # dim
BLUE    = "#1D63ED"    # Docker blue — the accent
BLUE_D  = "#1750C8"
SKY     = "#7DA2FF"
TAN     = "#E9A96A"    # warm highlight (quotes / keywords)
GREEN   = "#3FB950"
GREEN_D = "#238636"
RED     = "#E5534B"
AMBER   = "#E3A008"
CARDW   = "#FFFFFF"    # white card
INK     = "#101A2E"    # text on white card
INKSUB  = "#5A6a88"    # sub text on white card
SHADOW  = "#05080F"    # hard offset shadow
LIGHT   = "#FFFFFF"    # light-slide surface

MONO  = '"IBM Plex Mono", Menlo, "DejaVu Sans Mono", monospace'
FONT  = MONO

DOCKER_D = ("M98.3 30.4c-2.7-1.8-8.9-2.5-13.7-1.6-.6-4.5-3.1-8.4-7.7-11.9l-2.6-1.7-1.7 2.6"
            "c-2.2 3.3-2.8 8.8-.4 12.9-1.1.6-3.2 1.4-6 1.3H1.2l-.2 1c-.6 3.6-.6 14.9 6.7 23.6"
            "C13.2 63.9 21.5 68 32 68c22.8 0 39.6-10.5 47.5-29.6 3.1.1 9.8.1 13.2-6.4.2-.4.8-1.4 1.6-3.6"
            "l.3-.9-2.3-1.1zM52.5 25.6h-8.9v8.9h8.9v-8.9zm-11.9 0h-8.9v8.9h8.9v-8.9zm-11.9 0H19.8v8.9h8.9"
            "v-8.9zm-11.9 0H7.9v8.9h8.9v-8.9zm35.7-11.9h-8.9v8.9h8.9v-8.9zm-11.9 0h-8.9v8.9h8.9v-8.9z"
            "m-11.9 0H19.8v8.9h8.9v-8.9zm23.8-11.9h-8.9v8.9h8.9V1.9z")


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---- primitives ------------------------------------------------------------
def t(x, y, s, size, color, weight=400, anchor="start", spacing=None,
      italic=False, opacity=None, family=None):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    sp = f' letter-spacing="{spacing}"' if spacing is not None else ""
    it = ' font-style="italic"' if italic else ""
    op = f' opacity="{opacity}"' if opacity is not None else ""
    fam = f" font-family='{family}'" if family else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
            f'fill="{color}"{a}{sp}{it}{op}{fam}>{esc(s)}</text>')


def rect(x, y, w, h, fill, rx=10, stroke=None, sw=0, dash=None, opacity=None):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    da = f' stroke-dasharray="{dash}"' if dash else ""
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{st}{da}{op}/>'


def line(x1, y1, x2, y2, color, sw=2, dash=None):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{da}/>'


def arrow(x1, y1, x2, y2, color=MUTE2, sw=3):
    ang = math.atan2(y2 - y1, x2 - x1)
    hl, hw = 15, 8
    bx, by = x2 - hl*math.cos(ang), y2 - hl*math.sin(ang)
    px, py = -math.sin(ang), math.cos(ang)
    pts = f"{bx+px*hw:.1f},{by+py*hw:.1f} {bx-px*hw:.1f},{by-py*hw:.1f} {x2:.1f},{y2:.1f}"
    return (f'<line x1="{x1}" y1="{y1}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round"/>'
            f'<polygon points="{pts}" fill="{color}"/>')


def docker_mark(x, y, w, color=WHITE, opacity=1.0):
    s = w / 100.0
    return (f'<g transform="translate({x},{y}) scale({s})" opacity="{opacity}">'
            f'<path fill="{color}" d="{DOCKER_D}"/></g>')


def check(cx, cy, r=13, fill=GREEN, mark=WHITE):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'
            f'<path d="M{cx-r*0.45},{cy} l{r*0.32},{r*0.4} l{r*0.62},-{r*0.72}" '
            f'stroke="{mark}" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


def cross(cx, cy, r=13, fill=RED, mark=WHITE):
    d = r*0.42
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'
            f'<path d="M{cx-d},{cy-d} l{2*d},{2*d} M{cx+d},{cy-d} l-{2*d},{2*d}" '
            f'stroke="{mark}" stroke-width="2.6" stroke-linecap="round"/>')


# ---- texture + chrome ------------------------------------------------------
def hexweave(color=HEXCOL, opacity=0.5, r=26):
    """Faint flat-top honeycomb across the whole canvas."""
    def hexpts(cx, cy):
        p = []
        for k in range(6):
            a = math.pi/180*(60*k)
            p.append(f"{cx+r*math.cos(a):.1f},{cy+r*math.sin(a):.1f}")
        return " ".join(p)
    dx = 1.5*r
    dy = math.sqrt(3)*r
    cells = []
    col = 0
    x = -r
    while x < 1640:
        yoff = 0 if col % 2 == 0 else dy/2
        y = -r + yoff
        while y < 940:
            cells.append(f'<polygon points="{hexpts(x, y)}"/>')
            y += dy
        x += dx
        col += 1
    return (f'<g fill="none" stroke="{color}" stroke-width="1" opacity="{opacity}">'
            + "".join(cells) + "</g>")


def footer(dark=True, tag=None):
    col = "#5a6a8f" if dark else "#9aa6c0"
    mk = WHITE if dark else "#c2ccdd"
    b = [t(70, 862, "D O C K E R   /   N   E   X   T", 15, col, 700, spacing=1)]
    if tag:
        b.append(t(1360, 862, tag, 14, col, 500, anchor="end"))
    b.append(docker_mark(1486, 838, 42, mk, opacity=0.92 if dark else 0.8))
    return "".join(b)


def eyebrow(x, y, s, color=SKY):
    return t(x, y, s, 15, color, 700, spacing=2)


# ---- cards -----------------------------------------------------------------
def card_hard(x, y, w, h, fill=CARDW, rx=14, dx=8, dy=10, shadow=SHADOW):
    """White card sitting on a solid offset shadow (the /Next neubrutalist look)."""
    return rect(x+dx, y+dy, w, h, shadow, rx=rx) + rect(x, y, w, h, fill, rx=rx)


def blue_card(x, y, w, h, rx=14, dx=8, dy=10):
    return (rect(x+dx, y+dy, w, h, SHADOW, rx=rx)
            + f'<defs></defs>'
            + rect(x, y, w, h, BLUE, rx=rx))


def chips(active, labels, x=1486, y=250, size=48, gap=16):
    """Right-rail progress chips; active one filled blue."""
    b = []
    for i, lab in enumerate(labels):
        cy = y + i*(size+gap)
        on = (i == active)
        b.append(rect(x, cy, size, size, BLUE if on else "none", rx=12,
                      stroke=(BLUE if on else "#2b3c5e"), sw=2))
        b.append(t(x+size/2, cy+size/2+7, lab, 20, WHITE if on else "#5c6d92",
                   700, anchor="middle"))
    return "".join(b)


# ---- block-diagram helpers -------------------------------------------------
def block(x, y, w, h, title, sub=None, variant="ghost", tsize=20):
    """A labelled block. variant: ghost | solid | blue | good | bad."""
    if variant == "blue":
        b = [rect(x, y, w, h, BLUE, rx=12)]
        tc, sc = WHITE, "#cfe0ff"
    elif variant == "solid":
        b = [rect(x, y, w, h, "#15223d", rx=12, stroke="#31456e", sw=1.6)]
        tc, sc = WHITE, MUTE
    elif variant == "good":
        b = [rect(x, y, w, h, "#12281c", rx=12, stroke=GREEN_D, sw=1.8)]
        tc, sc = "#8ff0a6", "#8aa596"
    elif variant == "bad":
        b = [rect(x, y, w, h, "#2a1518", rx=12, stroke="#7d2b2b", sw=1.8)]
        tc, sc = "#ff9e94", "#b98f8f"
    else:  # ghost
        b = [rect(x, y, w, h, "none", rx=12, stroke="#3a4d76", sw=1.8, dash="6 6")]
        tc, sc = "#c6d2ec", MUTE2
    if sub:
        b.append(t(x+w/2, y+h/2-4, title, tsize, tc, 700, anchor="middle"))
        b.append(t(x+w/2, y+h/2+22, sub, 14, sc, 400, anchor="middle"))
    else:
        b.append(t(x+w/2, y+h/2+tsize*0.34, title, tsize, tc, 700, anchor="middle"))
    return "".join(b)


def pill(x, y, w, h, label, fill, tcol, size=15, weight=700):
    return rect(x, y, w, h, fill, rx=h/2) + t(x+w/2, y+h/2+size*0.34, label, size, tcol, weight, anchor="middle")


def bullets(x, y, items, gap=58, size=22, color=WHITE, marker=BLUE, sub_color=MUTE):
    """items: list of str, or (head, sub)."""
    b = []
    for i, it in enumerate(items):
        yy = y + i*gap
        b.append(f'<circle cx="{x+6}" cy="{yy-7}" r="4.5" fill="{marker}"/>')
        if isinstance(it, tuple):
            head, sub = it
            b.append(t(x+26, yy, head, size, color, 600))
            b.append(t(x+26, yy+26, sub, size-6, sub_color, 400))
        else:
            b.append(t(x+26, yy, it, size, color, 500))
    return "".join(b)


# ---- SVG assembly ----------------------------------------------------------
COVER_DEFS = f'''<defs>
  <radialGradient id="glow" cx="0.86" cy="0.14" r="0.8">
    <stop offset="0" stop-color="#1D63ED" stop-opacity="0.30"/>
    <stop offset="1" stop-color="#1D63ED" stop-opacity="0"/>
  </radialGradient>
</defs>'''


def _svg(body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" '
            f'font-family=\'{FONT}\'>{defs}{body}</svg>')


def _dark_base(glow=True):
    b = [rect(0, 0, 1600, 900, BG, rx=0), hexweave()]
    if glow:
        b.append(rect(0, 0, 1600, 900, "url(#glow)", rx=0))
    return b


# ---- FRAMES ----------------------------------------------------------------
def cover(eyebrow_txt, title_lines, subtitle, foot_tag=None):
    b = _dark_base()
    b.append(docker_mark(1230, 150, 200, WHITE, 0.10))
    b.append(eyebrow(120, 300, eyebrow_txt, SKY))
    y = 400
    for ln in title_lines:
        b.append(t(120, y, ln, 78, WHITE, 700))
        y += 88
    b.append(t(124, y-18, subtitle, 26, MUTE, 400))
    b.append(footer(dark=True, tag=foot_tag))
    return _svg("".join(b), COVER_DEFS)


def section(num, title_lines, subtitle):
    b = _dark_base()
    b.append(t(120, 250, f"// {num:02d}", 26, BLUE, 700, spacing=2))
    y = 420
    for ln in title_lines:
        b.append(t(120, y, ln, 66, WHITE, 700))
        y += 78
    b.append(t(124, y-8, subtitle, 24, SKY, 400, italic=True))
    b.append(footer(dark=True))
    return _svg("".join(b), COVER_DEFS)


def content(title, subtitle, body, tag=None, active_chip=None, chip_labels=None):
    b = _dark_base(glow=False)
    b.append(t(70, 108, title, 44, WHITE, 700))
    if subtitle:
        b.append(t(72, 150, subtitle, 22, SKY, 400, italic=True))
    b.append(line(70, 176, 1400 if chip_labels else 1530, 176, "#22314e", sw=2))
    if chip_labels is not None:
        b.append(chips(active_chip, chip_labels))
    b.append(body)
    b.append(footer(dark=True, tag=tag))
    return _svg("".join(b), COVER_DEFS)


def light(title, body, tag=None):
    b = [rect(0, 0, 1600, 900, LIGHT, rx=0)]
    b.append(body)
    b.append(t(70, 862, "D O C K E R   /   N   E   X   T", 15, "#9aa6c0", 700, spacing=1))
    b.append(docker_mark(1486, 838, 42, "#1D2740", 0.85))
    if tag:
        b.append(t(1360, 862, tag, 14, "#9aa6c0", 500, anchor="end"))
    return _svg("".join(b))


def statement(pre, big_lines, foot=None):
    b = _dark_base()
    if pre:
        b.append(eyebrow(150, 300, pre, SKY))
    y = 420
    for ln in big_lines:
        col = WHITE
        b.append(t(150, y, ln, 58, col, 700))
        y += 74
    if foot:
        b.append(line(150, y-6, 380, y-6, BLUE, sw=5))
        b.append(t(150, y+44, foot, 23, MUTE, 400))
    b.append(footer(dark=True))
    return _svg("".join(b), COVER_DEFS)
