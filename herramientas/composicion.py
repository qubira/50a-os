"""Arma las puertas bordadas, la portada con arco y balaustrada, y los símbolos bordados."""
import math
import random
import bordado as b


def envolver(svg, y, clase='flor-p', base=0.3, escala=2.4, alto=880):
    return f'<g class="{clase}" style="animation-delay: {base + y / alto * escala:.2f}s">{svg}</g>'


def puerta():
    r = random.Random(50)
    m = []

    def ramo(x, y, hojas, orden=None):
        return envolver(''.join(b.hoja(x, y, ln, an, ang, rnd=r) for ln, an, ang in hojas), orden if orden is not None else y, 'hoja-p')

    # hiedra superior frondosa
    m.append(envolver(b.hiedra([(-6, 14), (40, 30), (85, 18), (130, 34), (175, 22), (216, 36)], hojas_cada=17, tam=17, rnd=r), 20, 'hoja-p'))
    m.append(ramo(14, 20, [(46, 30, 40), (40, 26, 80), (36, 22, 10)], 30))
    # glicinas grandes cerca del centro
    for x, y, lg, an in [(104, 48, 120, 20), (136, 40, 190, 24), (170, 34, 250, 26), (200, 44, 175, 20)]:
        m.append(ramo(x, y - 4, [(22, 12, 150), (22, 12, 30)], y))
        m.append(envolver(b.glicina(x, y, lg, an, rnd=r), y + lg * .4))
    # hiedra por el borde exterior, con hojas grandes
    m.append(envolver(b.hiedra([(8, 40), (26, 120), (8, 200), (28, 280), (10, 360), (24, 430)], hojas_cada=19, tam=17, rnd=r, lado_ini=-1), 200, 'hoja-p'))
    # orquídeas
    m.append(ramo(52, 312, [(46, 20, 150), (42, 18, 205), (38, 16, 110)], 300))
    m.append(envolver(b.orquidea(62, 292, 40, 8), 292))
    m.append(envolver(b.orquidea(112, 352, 26, -14), 352))
    m.append(envolver(b.capullo(30, 372, 14, -60) + b.capullo(140, 330, 11, -40), 365))
    # rosas grandes
    m.append(ramo(48, 520, [(58, 30, 160), (54, 28, 222), (46, 24, 110), (44, 24, 270)], 500))
    m.append(ramo(122, 592, [(46, 24, 20), (42, 22, 80), (40, 20, -40)], 580))
    m.append(envolver(b.rosa(58, 512, 46, 10), 512))
    m.append(envolver(b.rosa(124, 586, 32, 40), 586))
    m.append(envolver(b.rosa(30, 600, 20, 70), 600))
    m.append(envolver(b.capullo(160, 560, 13, -60) + b.capullo(14, 452, 13, -120), 560))
    # parte baja
    m.append(envolver(b.hiedra([(14, 640), (52, 700), (24, 770), (62, 840), (36, 886)], hojas_cada=19, tam=17, rnd=r), 760, 'hoja-p'))
    oro = ''.join(f'<circle cx="{x}" cy="{y}" r="{rr}" fill="{col}" stroke="#9C7A2E" stroke-width=".7" stroke-dasharray="1.6 .7"/>'
                  for x, y, rr, col in [(100, 666, 9, b.ORO[2]), (114, 682, 7.5, b.ORO[1]), (92, 686, 7, b.ORO[2]), (106, 700, 5.5, b.ORO[1]), (122, 664, 5, b.ORO[2])])
    m.append(envolver(b.hoja(100, 660, 34, 16, -70, rnd=r) + b.hoja(100, 660, 30, 14, -120, rnd=r) + oro, 680))
    m.append(ramo(150, 842, [(48, 24, 200), (44, 22, -30), (40, 20, 250)], 830))
    m.append(envolver(b.rosa(150, 846, 32, 25), 846))
    m.append(ramo(196, 772, [(40, 20, 230), (36, 18, 170)], 772))
    m.append(envolver(b.capullo(194, 782, 14, -130) + b.orquidea(176, 720, 22, 20), 760))
    cuerpo = ''.join(m)
    return ('<svg aria-hidden="true" viewBox="0 0 210 880" preserveAspectRatio="xMidYMid slice" style="position: absolute; inset: 0; width: 100%; height: 100%{EXTRA}">'
            '<rect x="205" y="0" width="5" height="880" fill="#C9A24C" opacity=".55"/><rect x="203" y="0" width="1.2" height="880" fill="#FFFFFF" opacity=".5"/>'
            f'<g filter="url(#bordado)">{cuerpo}</g></svg>')


def balaustrada():
    out = ['<rect x="-2" y="556" width="424" height="18" rx="3" fill="url(#piedra)" stroke="#C9BE9C" stroke-width="1" stroke-dasharray="2.4 1"/>',
           '<rect x="-2" y="638" width="424" height="18" rx="3" fill="url(#piedra)" stroke="#C9BE9C" stroke-width="1" stroke-dasharray="2.4 1"/>']
    for x in [x for x in range(16, 420, 30) if not (186 < x < 234)]:
        d = f'M{x - 8} 574H{x + 8}L{x + 5} 582C{x + 13} 594 {x + 10} 608 {x + 4} 616L{x + 7} 638H{x - 7}L{x - 4} 616C{x - 10} 608 {x - 13} 594 {x - 5} 582Z'
        out.append(f'<path d="{d}" fill="url(#piedra)" stroke="#C9BE9C" stroke-width=".9" stroke-dasharray="2.2 .9"/>')
    for x0 in (-4, 190, 384):
        out.append(f'<rect x="{x0}" y="546" width="40" height="112" rx="2" fill="url(#piedra)" stroke="#C9BE9C" stroke-width="1" stroke-dasharray="2.4 1"/>')
        out.append(f'<rect x="{x0 - 4}" y="540" width="48" height="10" rx="2" fill="#E6DCC2" stroke="#C9BE9C" stroke-width=".8"/>')
        out.append(f'<rect x="{x0 + 8}" y="566" width="24" height="70" rx="2" fill="none" stroke="#C9A24C" stroke-width="1.2" stroke-dasharray="2 1"/>')
    return ''.join(out)


def arco():
    piedra = 'fill="url(#piedra)" stroke="#C9BE9C" stroke-width="1" stroke-dasharray="2.4 1"'
    out = ['<path d="M76 562V252A134 134 0 0 1 344 252V562H332V252A122 122 0 0 0 88 252V562Z" fill="#D9CFB3" opacity=".9"/>',
           '<path d="M88 562V252A122 122 0 0 1 332 252V562" fill="none" stroke="#2F3A1C" stroke-opacity=".18" stroke-width="10" filter="url(#bordado)"/>',
           f'<path d="M34 252A176 176 0 0 1 386 252H344A134 134 0 0 0 76 252Z" {piedra}/>',
           f'<rect x="34" y="252" width="42" height="310" {piedra}/>', f'<rect x="344" y="252" width="42" height="310" {piedra}/>',
           f'<rect x="26" y="242" width="58" height="14" rx="2" {piedra}/>', f'<rect x="336" y="242" width="58" height="14" rx="2" {piedra}/>',
           f'<path d="M193 72H227L221 124H199Z" {piedra}/>',
           # luz suave desde arriba a la izquierda sobre la piedra
           '<path d="M34 252A176 176 0 0 1 386 252H344A134 134 0 0 0 76 252Z M34 252H76V562H34Z M344 252H386V562H344Z" fill="url(#luzPiedra)"/>',
           # bases de las columnas
           f'<rect x="28" y="528" width="54" height="16" rx="2" {piedra}/>', f'<rect x="338" y="528" width="54" height="16" rx="2" {piedra}/>',
           '<path d="M42 252A168 168 0 0 1 378 252M68 252A142 142 0 0 1 352 252" fill="none" stroke="#C9BE9C" stroke-width="1.1" stroke-dasharray="2.4 1.2"/>',
           '<path d="M45 270V548M65 270V548M355 270V548M375 270V548" stroke="#DED4B8" stroke-width="1.2" stroke-dasharray="2.4 1.2"/>',
           # cordón dorado y perlas en el borde interior del arco
           '<path d="M79 556V252A131 131 0 0 1 341 252V556" fill="none" stroke="#C9A24C" stroke-width="2.2" stroke-dasharray="3 1.2"/>',
           '<path d="M84 556V252A126 126 0 0 1 336 252V556" fill="none" stroke="#FFFDF6" stroke-width="4.2" stroke-dasharray="0.1 7" stroke-linecap="round"/>',
           # dentículos bajo la cornisa del arco
           ''.join(f'<rect x="{210 + 160 * math.cos(math.radians(a)) - 3:.1f}" y="{252 - 160 * math.sin(math.radians(a)) - 3:.1f}" width="6" height="6" fill="#E6DCC2" stroke="#C9BE9C" stroke-width=".6" transform="rotate({90 - a} {210 + 160 * math.cos(math.radians(a)):.1f} {252 - 160 * math.sin(math.radians(a)):.1f})"/>' for a in range(172, 100, -9)),
           ''.join(f'<rect x="{210 + 160 * math.cos(math.radians(a)) - 3:.1f}" y="{252 - 160 * math.sin(math.radians(a)) - 3:.1f}" width="6" height="6" fill="#E6DCC2" stroke="#C9BE9C" stroke-width=".6" transform="rotate({90 - a} {210 + 160 * math.cos(math.radians(a)):.1f} {252 - 160 * math.sin(math.radians(a)):.1f})"/>' for a in range(8, 80, 9)),
           # corona dorada bordada en la clave
           '<path d="M197 112L194 88L203 96L210 82L217 96L226 88L223 112Z" fill="#E2C77E" stroke="#9C7A2E" stroke-width=".9" stroke-dasharray="1.8 .8"/>',
           '<rect x="196" y="112" width="28" height="5" rx="2" fill="#C9A24C" stroke="#9C7A2E" stroke-width=".6"/>',
           '<circle cx="210" cy="80" r="2.6" fill="#FFFDF6" stroke="#C9A24C" stroke-width=".8"/>',
           # volutas doradas en los capiteles
           '<path d="M30 249a5 5 0 1 1 8 4M80 249a5 5 0 1 0 -8 4M340 249a5 5 0 1 1 8 4M390 249a5 5 0 1 0 -8 4" fill="none" stroke="#C9A24C" stroke-width="1.6"/>',
           # rosetones en las columnas
           b.rosa(55, 410, 12, 20), b.rosa(365, 410, 12, 50)]
    return ''.join(out)


def paloma(x, y, s, espejo=False):
    t = f'translate({x} {y}) scale({-s if espejo else s} {s})'
    cuerpo = 'M0 0C6 -6 16 -6 22 -1C26 2 30 2 34 0C30 5 26 7 20 7C12 8 4 6 0 0Z'
    ala = 'M8 -2C10 -14 18 -22 30 -24C26 -16 22 -8 16 -2Z'
    puntadas = ''.join(f'M{10 + k * 2.6:.1f} -3L{14 + k * 3.4:.1f} {-10 - k * 2.4:.1f}' for k in range(5))
    return (f'<g transform="{t}"><path d="{cuerpo}" fill="#FBF8EE" stroke="#C9BE9C" stroke-width=".8" stroke-dasharray="1.8 .8"/>'
            f'<path d="{ala}" fill="#F4EFE0" stroke="#C9BE9C" stroke-width=".8" stroke-dasharray="1.8 .8"/>'
            f'<path d="{puntadas}" stroke="#DCD3BA" stroke-width="1.1" stroke-linecap="round"/>'
            '<circle cx="4" cy="-1" r=".9" fill="#4F5D2F"/><path d="M0 0L-3 1L0 1.6Z" fill="#C9A24C"/></g>')


def marco_portada():
    out = ['<rect x="8" y="6" width="404" height="788" rx="6" fill="none" stroke="#C9A24C" stroke-width="1.6" stroke-dasharray="3.2 1.4"/>',
           '<rect x="14" y="12" width="392" height="776" rx="4" fill="none" stroke="#C9BE9C" stroke-width=".9" stroke-dasharray="2 1.2"/>']
    for (x, y, g) in [(12, 10, 0), (408, 10, 30), (12, 790, 60), (408, 790, 90)]:
        out.append(b.hoja(x, y, 18, 9, 45 + g * 3, n=6) + b.hoja(x, y, 18, 9, -45 + g * 3, n=6) + b.rosa(x, y, 9, g))
    return ''.join(out)


def flora_portada():
    r = random.Random(9)
    m = [marco_portada()]

    def bp(svg, orden):
        return f'<g class="bp" style="animation-delay: {3.0 + orden * 0.12:.2f}s">{svg}</g>'

    # hiedra sobre el arco
    izq = [(210 + 182 * math.cos(math.radians(a)), 252 - 182 * math.sin(math.radians(a))) for a in range(176, 96, -12)]
    der = [(210 + 182 * math.cos(math.radians(a)), 252 - 182 * math.sin(math.radians(a))) for a in range(4, 84, 12)]
    m.append(bp(b.hiedra(izq, hojas_cada=20, tam=13, rnd=r), 0))
    m.append(bp(b.hiedra(der, hojas_cada=20, tam=13, rnd=r, lado_ini=-1), 1))
    # hiedra subiendo por las columnas
    m.append(bp(b.hiedra([(30, 560), (42, 480), (28, 400), (44, 320), (32, 262)], hojas_cada=22, tam=12, rnd=r), 2))
    m.append(bp(b.hiedra([(390, 560), (378, 480), (392, 400), (376, 320), (388, 262)], hojas_cada=22, tam=12, rnd=r, lado_ini=-1), 3))
    # glicinas colgando dentro del arco
    for k, (a, lg) in enumerate([(160, 90), (140, 60), (40, 60), (20, 90)]):
        x, y = 210 + 136 * math.cos(math.radians(a)), 252 - 136 * math.sin(math.radians(a))
        m.append(bp(b.glicina(x, y + 4, lg, 17, rnd=r), 4 + k))
    # orquídeas en los capiteles
    m.append(bp(b.hoja(56, 238, 28, 13, 200, rnd=r) + b.orquidea(56, 232, 24, 6), 8))
    m.append(bp(b.hoja(364, 238, 28, 13, -20, rnd=r) + b.orquidea(364, 232, 24, -6), 9))
    # rosas sobre la balaustrada
    for k, (x, y, R, g) in enumerate([(46, 556, 28, 0), (92, 574, 18, 30), (374, 556, 28, 20), (328, 574, 18, 50)]):
        hojas = b.hoja(x, y, R * 1.3, R * .7, 200 if x < 210 else -20, rnd=r) + b.hoja(x, y, R * 1.2, R * .65, 150 if x < 210 else 30, rnd=r)
        m.append(bp(hojas + b.rosa(x, y, R, g), 10 + k))
    m.append(bp(b.capullo(18, 548, 11, -100) + b.capullo(402, 548, 11, -80), 14))
    # guirnalda superior de lado a lado y glicinas en las esquinas
    # guirnalda que cuelga sobre la balaustrada con rosa central
    guir = [(30, 560)] + [(30 + 360 * t / 12, 560 + 26 * math.sin(math.pi * t / 12)) for t in range(1, 12)] + [(390, 560)]
    m.append(bp(b.hiedra(guir, hojas_cada=16, tam=12, rnd=r), 15))
    m.append(bp(b.hoja(210, 584, 30, 15, 160, rnd=r) + b.hoja(210, 584, 30, 15, 20, rnd=r) + b.rosa(210, 584, 20, 18) + b.capullo(184, 590, 9, 160) + b.capullo(236, 590, 9, 20), 16))
    for k, (x, y, lg, an) in enumerate([(32, 24, 110, 17), (56, 22, 78, 14), (388, 24, 110, 17), (364, 22, 78, 14)]):
        m.append(bp(b.glicina(x, y, lg, an, rnd=r), 16 + k))
    # rosas en los hombros del arco y capullos junto a la clave
    for k, (x, y, R, g) in enumerate([(44, 188, 20, 15), (376, 188, 20, 35)]):
        m.append(bp(b.hoja(x, y, 30, 16, 120 if x < 210 else 60, rnd=r) + b.hoja(x, y, 28, 15, 230 if x < 210 else -50, rnd=r) + b.rosa(x, y, R, g), 20 + k))
    m.append(bp(b.hoja(186, 80, 22, 11, 200, rnd=r) + b.capullo(184, 84, 10, -140) + b.hoja(234, 80, 22, 11, -20, rnd=r) + b.capullo(236, 84, 10, -40), 22))
    # palomas bordadas junto a la corona
    m.append(bp(paloma(150, 66, 1.05) + paloma(270, 66, 1.05, True), 24))
    # orquídeas colgando a los lados, fuera del arco
    m.append(bp(b.orquidea(16, 330, 18, 10) + b.orquidea(404, 330, 18, -10), 23))
    return ''.join(m)


def simbolos():
    rosa = '<symbol id="rosaV" viewBox="0 0 40 40">' + b.rosa(20, 20, 18.5, 12) + '</symbol>'
    rosa2 = '<symbol id="rosa" viewBox="0 0 40 40"><use href="#rosaV" width="40" height="40"/></symbol>'
    hoja = '<symbol id="hoja" viewBox="0 0 30 14">' + b.hoja(1, 7, 28, 12, 0, n=8) + '</symbol>'
    r = random.Random(4)
    adorno = ('<symbol id="adorno" viewBox="0 0 240 40">'
              + b.hiedra([(8, 24), (40, 18), (72, 24), (104, 19)], hojas_cada=16, tam=8, rnd=r)
              + b.hiedra([(232, 24), (200, 18), (168, 24), (136, 19)], hojas_cada=16, tam=8, rnd=r)
              + b.hoja(120, 20, 22, 11, 200) + b.hoja(120, 20, 22, 11, -20) + b.rosa(120, 20, 13, 8) + '</symbol>')
    return rosa, rosa2, hoja, adorno
