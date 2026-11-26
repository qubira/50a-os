"""Rediseña las rosas (rosaV y rosa) y la hoja: pétalos en capas con degradado, centro enrollado."""
import math
import re
import sys

p = sys.argv[1]
s = open(p, encoding='utf-8').read()

PETALO = 'M0 0C-8.6 -2.6 -11.6 -11 -8.2 -15.8C-5.6 -19.2 -2 -18.6 0 -16.9C2 -18.6 5.6 -19.2 8.2 -15.8C11.6 -11 8.6 -2.6 0 0Z'
BORDE = 'M-7.2 -15.4C-4.8 -18 -1.8 -17.4 0 -15.9C1.8 -17.4 4.8 -18 7.2 -15.4'


def capa(n, escala, giro, relleno, trazo, ancho, borde=True):
    out = []
    for k in range(n):
        ang = giro + k * 360 / n
        t = f'translate(20 20) rotate({ang:.1f}) scale({escala})'
        out.append(f'<path transform="{t}" d="{PETALO}" fill="{relleno}" stroke="{trazo}" stroke-width="{ancho / escala:.2f}"/>')
        if borde:
            out.append(f'<path transform="{t}" d="{BORDE}" fill="none" stroke="#FFFFFF" stroke-opacity=".85" stroke-width="{0.9 / escala:.2f}" stroke-linecap="round"/>')
    return ''.join(out)


rosa = ('<symbol id="rosaV" viewBox="0 0 40 40">'
        + capa(5, 1.08, 0, 'url(#petaloA)', '#93AB6C', 0.55)
        + capa(5, 0.78, 36, 'url(#petaloB)', '#9DB476', 0.5)
        + capa(4, 0.52, 10, 'url(#petaloC)', '#9DB476', 0.45)
        + '<circle cx="20" cy="20" r="4.6" fill="url(#rosaCentro)" stroke="#93AB6C" stroke-width="0.5"/>'
        + '<path d="M20.4 17.2C22.6 17.4 23.4 19.9 21.9 21.4C20.3 22.9 17.6 22.2 17.4 20C17.2 18.3 18.7 17.3 20 17.8C21 18.2 21.2 19.6 20.3 20.1" fill="none" stroke="#7E975A" stroke-width="0.85" stroke-linecap="round"/>'
        + '<path d="M18 16.8C19.2 16.1 20.8 16 22 16.6" fill="none" stroke="#FFFFFF" stroke-opacity=".9" stroke-width="0.7" stroke-linecap="round"/>'
        + '</symbol>')
rosa_clara = '<symbol id="rosa" viewBox="0 0 40 40"><use href="#rosaV" width="40" height="40"/></symbol>'
hoja = ('<symbol id="hoja" viewBox="0 0 30 14">'
        '<path d="M1 7C6 1.2 16 -0.4 29 7C16 14.4 6 12.8 1 7Z" fill="url(#hojaGrad)" stroke="#86A05E" stroke-width="0.7"/>'
        '<path d="M1.5 7C9 6.2 18 6.3 27.5 7" fill="none" stroke="#7E975A" stroke-width="0.75" stroke-linecap="round"/>'
        '<path d="M8 6.6C10 4.6 12 3.6 14 3.2M14 6.4C16 4.4 18 3.6 20 3.4M20 6.6C21.6 5.2 23 4.6 24.5 4.5M8 7.4C10 9.4 12 10.4 14 10.8M14 7.6C16 9.6 18 10.4 20 10.6M20 7.4C21.6 8.8 23 9.4 24.5 9.5" fill="none" stroke="#86A05E" stroke-opacity=".7" stroke-width="0.45" stroke-linecap="round"/>'
        '<path d="M4 6.2C9 3 16 2 23 4" fill="none" stroke="#FFFFFF" stroke-opacity=".7" stroke-width="0.6" stroke-linecap="round"/>'
        '</symbol>')
grads = ('<radialGradient id="petaloA" cx=".5" cy="1" r="1.05"><stop offset="0" stop-color="#7F9A55"/><stop offset=".35" stop-color="#A9C084"/><stop offset=".7" stop-color="#D8E6BE"/><stop offset="1" stop-color="#F3F8E8"/></radialGradient>'
         '<radialGradient id="petaloB" cx=".5" cy="1" r="1.05"><stop offset="0" stop-color="#7F9A55"/><stop offset=".45" stop-color="#B7CC92"/><stop offset="1" stop-color="#EEF5E0"/></radialGradient>'
         '<radialGradient id="petaloC" cx=".5" cy="1" r="1.05"><stop offset="0" stop-color="#6F8A48"/><stop offset=".5" stop-color="#BFD39C"/><stop offset="1" stop-color="#EAF2DA"/></radialGradient>'
         '<radialGradient id="rosaCentro" cx=".45" cy=".4" r=".7"><stop offset="0" stop-color="#F4F8EA"/><stop offset=".6" stop-color="#CADBA8"/><stop offset="1" stop-color="#A3BB7C"/></radialGradient>'
         '<linearGradient id="hojaGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E3EDCF"/><stop offset=".5" stop-color="#C9DCA6"/><stop offset="1" stop-color="#AFC88A"/></linearGradient>')


def reemplazar(id_, nuevo):
    global s
    m = re.search(r'<symbol id="' + id_ + r'" viewBox="[^"]*">.*?</symbol>', s, flags=re.S)
    assert m, id_
    s = s[:m.start()] + nuevo + s[m.end():]


reemplazar('rosaV', rosa)
reemplazar('rosa', rosa_clara)
reemplazar('hoja', hoja)
assert s.count('</defs></svg>') >= 1
s = s.replace('</defs></svg>', grads + '</defs></svg>', 1)
open(p, 'w', encoding='utf-8').write(s)
print('ok')
