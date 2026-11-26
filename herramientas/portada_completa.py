"""Portada con la foto a pantalla completa y el texto claro abajo sobre un degradado."""
import re
import sys

p = sys.argv[1]
L = open(p, encoding='utf-8').read().split('\n')
i = [n for n, x in enumerate(L) if x.startswith('<section id="inicio"')][0]
j = i
while not L[j].startswith('</section>'):
    j += 1
sec = L[i:j + 1]

# 1) contenedor: la foto es el fondo completo
assert sec[1].startswith('<div class="{{claseCarta}}"')
sec[1] = '<div class="{{claseCarta}} foto-portada" style="position: relative; width: 420px; height: 800px; margin: 0 auto; transform-origin: 50% 40%">'
# 2) quitar arco, marco y cortinas (desde la foto del arco hasta el </svg> de las cortinas)
a = [k for k, x in enumerate(sec) if x.startswith('<div class="foto-arco"')][0]
b = [k for k, x in enumerate(sec) if x == '</svg>' and k > a][0]
sec[a:b + 1] = ['<div aria-hidden="true" style="position: absolute; inset: 0; background: linear-gradient(180deg, rgba(24,34,12,0.35) 0%, rgba(24,34,12,0) 16%, rgba(24,34,12,0) 46%, rgba(24,34,12,0.55) 64%, rgba(20,30,10,0.9) 100%)"></div>',
                '<div aria-hidden="true" style="position: absolute; inset: 12px; border: 1px solid rgba(240,222,170,0.75); outline: 1px solid rgba(240,222,170,0.4); outline-offset: 4px; pointer-events: none"></div>']
s = '\n'.join(sec)

# 3) texto abajo, claro
s = re.sub(r'(<div class="\{\{claseTexto\}\}" style="--base: \{\{baseAnim\}\}; )position: absolute; left: 24px; right: 24px; top: 488px;',
           r'\1position: absolute; left: 28px; right: 28px; bottom: 58px;', s, count=1)
s = s.replace('fill="#5E7838" filter="url(#relieveV)" style="animation-delay: var(--base)"', 'fill="#E9CD82" style="animation-delay: var(--base)"', 1)
# línea de invitación en una sola frase, sin repetir el 50 grande
s = re.sub(r'(<p style="animation-delay: calc\(var\(--base\) \+ 0\.35s\);[^"]*">)[^<]*<br>[^<]*(</p>)',
           r'\1CON TODO CARIÑO TE INVITAMOS<br>A CELEBRAR LOS 50 AÑOS DE\2', s, count=1)
s = re.sub(r'\n<p class="c50"[^\n]*</p>', '', s, count=1)
s = re.sub(r'\n<p style="animation-delay: calc\(var\(--base\) \+ 1\.7s\);[^\n]*AÑOS</p>', '', s, count=1)
s = re.sub(r'\n<p style="animation-delay: calc\(var\(--base\) \+ 2\.1s\);[^\n]*>de</p>', '', s, count=1)
assert 'class="c50"' not in s and '>de</p>' not in s
s = s.replace('animation-delay: calc(var(--base) + 2.4s)', 'animation-delay: calc(var(--base) + 0.9s)', 1)
s = s.replace('animation-delay: calc(var(--base) + 3.8s)', 'animation-delay: calc(var(--base) + 2.2s)', 1)
s = s.replace('animation-delay: calc(var(--base) + 5.2s)', 'animation-delay: calc(var(--base) + 3.4s)', 1)
s = s.replace('animation-delay: calc(var(--base) + 5.5s)', 'animation-delay: calc(var(--base) + 3.7s)', 1)
# colores claros
s = re.sub(r'color: #2E4219; text-shadow: [^;"]*', 'color: #F3E7C4; text-shadow: 0 1px 3px rgba(0,0,0,0.55)', s)
s = re.sub(r'color: #2A3D15; -webkit-text-stroke: ([0-9.]+)px #2A3D15; text-shadow: [^;"]*',
           r'color: #FFF8E6; -webkit-text-stroke: 0px transparent; text-shadow: 0 2px 10px rgba(0,0,0,0.55), 0 0 1px rgba(0,0,0,0.4)', s)
s = re.sub(r'font-size: 46px; line-height: 1.05;', 'font-size: 64px; line-height: 1;', s, count=1)
s = re.sub(r'font-size: 26px; line-height: 1.1;', 'font-size: 34px; line-height: 1.1;', s, count=1)
s = s.replace('stroke="#B88A2C" stroke-width="1.4"', 'stroke="#E9CD82" stroke-width="1.2"', 1)
s = re.sub(r'font-size: 17px; font-weight: 600; color: #22300F; text-shadow: 0 1px 0 #FFFFFF',
           'font-family: Cinzel, serif; font-size: 13px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; color: #F3E7C4; text-shadow: 0 1px 3px rgba(0,0,0,0.55)', s, count=1)
s = s.replace('letter-spacing: 3px; color: #3F5226">DESLIZA', 'letter-spacing: 3px; color: rgba(243,231,196,0.85)">DESLIZA', 1)
assert s.count('#F3E7C4') >= 2, s.count('#F3E7C4')

full = '\n'.join(L[:i]) + '\n' + s + '\n' + '\n'.join(L[j + 1:])
# CSS: la foto de fondo completa
full, k = re.subn(r'\.foto-arco\{background:#EDE4E8 url\((/_blob/[0-9a-f]+)\) [^}]*\}',
                  r'.foto-portada{background:#3B4A27 url(\1) 20% 0/cover no-repeat}', full, count=1)
assert k == 1
open(p, 'w', encoding='utf-8').write(full)
print('ok')
