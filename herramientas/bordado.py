"""Motivos de bordado en SVG (hojas, rosas, orquídeas, glicinas, hiedra) y textura de lino.
Las puntadas se calculan como líneas: no usa clipPath, así se puede repetir sin ids.
"""
import math
import random

VERDES = ['#4F5D2F', '#5E6D38', '#6E7D43', '#7F8E52', '#93A266']
CREMAS = ['#FBF8EE', '#F4EFE0', '#EAE2CC', '#DCD3BA']
SOMBRA_CREMA = '#C9BE9C'
ORO = ['#B8913C', '#C9A24C', '#E2C77E']


def f(v):
    return f'{v:.1f}'.rstrip('0').rstrip('.') if abs(v) < 1e6 else str(v)


def rot(px, py, a):
    c, s = math.cos(a), math.sin(a)
    return px * c - py * s, px * s + py * c


# ---------- hoja con puntada de espiga (satén desde la nervadura) ----------
def hoja(x, y, largo, ancho, ang_deg, colores=None, n=None, rnd=None, borde=None, petalo=False):
    rnd = rnd or random.Random(int(x * 7 + y * 13))
    colores = colores or VERDES
    a = math.radians(ang_deg)
    n = n or max(6, int(largo / 3.2))

    def mid(u):
        return rot(u * largo, 0, a)

    def edge(u, lado):
        uu = min(1, max(0, u))
        if petalo:
            w = ancho / 2 * (math.sin(math.pi * (0.08 + 0.8 * uu)) ** 0.55) * (0.75 + 0.35 * uu)
        else:
            w = ancho / 2 * math.sin(math.pi * uu) ** 0.85 * (1 - 0.12 * uu)
        return rot(u * largo, lado * w, a)

    trazos = {}
    if petalo:
        # satén en abanico desde la base: tramo interior sombreado y tramo exterior claro
        borde_pts = [edge(i / (n * 2), -1) for i in range(1, n * 2 + 1)] + [edge(1 - i / (n * 2), 1) for i in range(0, n * 2)]
        for k, (ex, ey) in enumerate(borde_pts):
            mx, my = ex * 0.45, ey * 0.45
            trazos.setdefault(colores[0], []).append(f'M{f(x + ex * .08)} {f(y + ey * .08)}L{f(x + mx)} {f(y + my)}')
            trazos.setdefault(colores[1 + k % (len(colores) - 1)], []).append(f'M{f(x + mx)} {f(y + my)}L{f(x + ex)} {f(y + ey)}')
    for lado in ((-1, 1) if not petalo else ()):
        for k in range(n):
            u0 = k / n
            u1 = min(1, u0 + 0.16)
            mx, my = mid(u0 + 0.02)
            ex, ey = edge(u1, lado)
            c = colores[(k + (0 if lado < 0 else 2)) % len(colores)]
            trazos.setdefault(c, []).append(f'M{f(x + mx)} {f(y + my)}L{f(x + ex)} {f(y + ey)}')
    out = [f'<path d="{"".join(v)}" stroke="{c}" stroke-width="1.35" stroke-linecap="round" fill="none"/>' for c, v in trazos.items()]
    # contorno en punto partido y nervadura
    pts = [edge(i / 14, -1) for i in range(15)] + [edge(1 - i / 14, 1) for i in range(15)]
    d = 'M' + 'L'.join(f'{f(x + px)} {f(y + py)}' for px, py in pts) + 'Z'
    out.insert(0, f'<path d="{d}" fill="{colores[1]}" fill-opacity=".55"/>')
    out.append(f'<path d="{d}" fill="none" stroke="{borde or colores[0]}" stroke-width=".8" stroke-dasharray="2.2 .9"/>')
    tx, ty = mid(0.96)
    if not petalo:
        out.append(f'<path d="M{f(x)} {f(y)}L{f(x + tx)} {f(y + ty)}" stroke="{colores[-1]}" stroke-width=".7" stroke-dasharray="2 1"/>')
    return ''.join(out)


# ---------- rosa bordada (pétalos redondeados en satén, en anillos) ----------
def rosa(cx, cy, R, giro=0, rnd=None):
    crema = [SOMBRA_CREMA, CREMAS[2], CREMAS[1], CREMAS[0]]
    out = []
    for k in range(5):  # anillo exterior
        out.append(hoja(cx, cy, R, R * 1.05, giro + k * 72, colores=crema, n=8, borde=SOMBRA_CREMA, petalo=True))
    for k in range(5):  # anillo medio
        out.append(hoja(cx, cy, R * 0.7, R * 0.8, giro + 30 + k * 72, colores=crema, n=6, borde=SOMBRA_CREMA, petalo=True))
    for k in range(3):  # anillo interior
        out.append(hoja(cx, cy, R * 0.42, R * 0.6, giro + 10 + k * 120, colores=[SOMBRA_CREMA, CREMAS[2], CREMAS[1]], n=4, borde=SOMBRA_CREMA, petalo=True))
    out.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(R * 0.2)}" fill="{CREMAS[2]}"/>')
    for i, rr in enumerate([R * 0.19, R * 0.12, R * 0.06]):
        a0 = math.radians(giro + i * 80)
        a1 = a0 + math.radians(260)
        x0, y0 = cx + rr * math.cos(a0), cy + rr * math.sin(a0)
        x1, y1 = cx + rr * math.cos(a1), cy + rr * math.sin(a1)
        col = SOMBRA_CREMA if i % 2 == 0 else CREMAS[0]
        out.append(f'<path d="M{f(x0)} {f(y0)}A{f(rr)} {f(rr)} 0 1 1 {f(x1)} {f(y1)}" fill="none" stroke="{col}" stroke-width="{f(max(1.1, R * 0.06))}" stroke-linecap="round"/>')
    return ''.join(out)


# ---------- orquídea (5 pétalos de satén crema + labio + centro dorado) ----------
def orquidea(cx, cy, s, giro=0):
    out = []
    for k, (ang, lg, an) in enumerate([(-90, 1.0, .5), (-18, .95, .75), (54, .8, .5), (126, .8, .5), (198, .95, .75)]):
        out.append(hoja(cx, cy, s * lg, s * an, ang + giro, colores=[SOMBRA_CREMA, CREMAS[2], CREMAS[1], CREMAS[0]], n=9, borde=SOMBRA_CREMA, petalo=(k in (1, 4))))
    out.append(f'<ellipse cx="{f(cx)}" cy="{f(cy + s * .12)}" rx="{f(s * .2)}" ry="{f(s * .16)}" fill="{ORO[2]}" stroke="{ORO[0]}" stroke-width=".7" stroke-dasharray="1.5 .7"/>')
    out.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(s * .08)}" fill="{ORO[1]}"/>')
    return ''.join(out)


# ---------- racimo de glicina (nudos franceses) ----------
def glicina(x, y, largo, ancho=18, rnd=None):
    rnd = rnd or random.Random(int(x * 11 + y))
    out = [f'<path d="M{f(x)} {f(y - 8)}Q{f(x + 3)} {f(y - 2)} {f(x)} {f(y + 6)}" stroke="{VERDES[2]}" stroke-width="1.4" fill="none" stroke-dasharray="2.5 1"/>']
    filas = int(largo / 5.4)
    for i in range(filas):
        t = i / max(1, filas - 1)
        w = ancho * (1 - t) ** 0.8 + 3
        cnt = max(1, round(w / 5.2))
        yy = y + i * 5.4
        for j in range(cnt):
            xx = x - w / 2 + (j + 0.5) * w / cnt + rnd.uniform(-1.2, 1.2)
            r = 2.7 * (1 - 0.45 * t) + rnd.uniform(-.2, .3)
            out.append(f'<circle cx="{f(xx)}" cy="{f(yy + rnd.uniform(-1, 1))}" r="{f(r)}" fill="url(#nudo)"/>')
    return ''.join(out)


# ---------- hiedra: tallo en punto de tallo con hojitas ----------
def hiedra(puntos, hojas_cada=26, tam=13, rnd=None, lado_ini=1):
    rnd = rnd or random.Random(len(puntos) * 17)
    d = 'M' + 'L'.join(f'{f(px)} {f(py)}' for px, py in puntos)
    out = [f'<path d="{d}" stroke="{VERDES[1]}" stroke-width="1.7" fill="none" stroke-dasharray="3 1.1" stroke-linecap="round"/>']
    acum, lado = 0, lado_ini
    for (x0, y0), (x1, y1) in zip(puntos, puntos[1:]):
        seg = math.hypot(x1 - x0, y1 - y0)
        ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
        pos = hojas_cada - acum
        while pos < seg:
            t = pos / seg
            hx, hy = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            sz = tam * rnd.uniform(.8, 1.15)
            out.append(hoja(hx, hy, sz * 1.25, sz * .95, ang + lado * rnd.uniform(45, 70), rnd=rnd))
            lado = -lado
            pos += hojas_cada
        acum = (acum + seg) % hojas_cada
    return ''.join(out)


def capullo(x, y, s, ang=-90):
    return (hoja(x, y, s * 1.3, s * .7, ang, colores=[SOMBRA_CREMA, CREMAS[2], CREMAS[1], CREMAS[0]], n=6, borde=SOMBRA_CREMA)
            + hoja(x, y, s * .8, s * .45, ang - 35) + hoja(x, y, s * .8, s * .45, ang + 35))


DEFS = ('<radialGradient id="nudo" cx=".35" cy=".3" r=".75"><stop offset="0" stop-color="#FFFDF6"/><stop offset=".55" stop-color="#EEE6CF"/><stop offset="1" stop-color="#C9BE9C"/></radialGradient>'
        '<filter id="bordado" x="-10%" y="-10%" width="120%" height="120%" color-interpolation-filters="sRGB"><feDropShadow dx=".7" dy="1.1" stdDeviation=".7" flood-color="#2F3A1C" flood-opacity=".45"/></filter>'
        '<linearGradient id="luzPiedra" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".55"/><stop offset=".45" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="1" stop-color="#8F8466" stop-opacity=".28"/></linearGradient>'
        '<pattern id="piedra" width="5" height="7" patternUnits="userSpaceOnUse"><rect width="5" height="7" fill="#EFE8D4"/><path d="M1.2 0.6V6.2M3.7 3.4V9.4M3.7 -3.6V2.4" stroke="#DED4B8" stroke-width="1.1" stroke-linecap="round"/></pattern>')


def textura_lino(ruta, base=(228, 235, 214), tam=320, semilla=7):
    from PIL import Image, ImageFilter
    rnd = random.Random(semilla)
    im = Image.new('RGB', (tam, tam), base)
    px = im.load()
    filas = [rnd.uniform(-9, 9) for _ in range(tam)]
    cols = [rnd.uniform(-9, 9) for _ in range(tam)]
    for yy in range(tam):
        for xx in range(tam):
            v = filas[yy] * (0.6 if yy % 3 else 1.0) + cols[xx] * (0.6 if xx % 3 else 1.0) + rnd.uniform(-4, 4)
            px[xx, yy] = tuple(max(0, min(255, int(c + v))) for c in base)
    im = im.filter(ImageFilter.GaussianBlur(0.45))
    im.save(ruta, quality=86)
