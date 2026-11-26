"""Aplica el estilo bordado sobre lino a la invitación (puertas, portada, símbolos y fondos)."""
import re
import sys
import bordado as b
import composicion as c

p = sys.argv[1]
s = open(p, encoding='utf-8').read()
LINO = '/_blob/86ca6db8fe728776d4360789e4caac66'
FOTO = '/_blob/5a4fbaf4dd6b78b2e6eda0e233e9d879'


def one(a, bb):
    global s
    assert s.count(a) == 1, (s.count(a), a[:100])
    s = s.replace(a, bb)


# 1) puertas
puerta = c.puerta()
for lado, extra in (('izq', ''), ('der', '; transform: scaleX(-1)')):
    m = re.search(r'(<div class="puerta ' + lado + r'" style="[^"]*)background: #DCE8C5; ([^"]*">)(<svg aria-hidden="true" viewBox="0 0 210 880".*?</svg>)</div>', s, flags=re.S)
    assert m, lado
    nuevo = m.group(1).replace('<div class="puerta ' + lado + '"', '<div class="puerta ' + lado + ' lino"') + m.group(2) + puerta.replace('{EXTRA}', extra) + '</div>'
    s = s[:m.start()] + nuevo + s[m.end():]

# 2) símbolos bordados + definiciones
rosa, rosa2, hoja, adorno = c.simbolos()
for id_, nuevo in (('rosaV', rosa), ('rosa', rosa2), ('hoja', hoja), ('adorno', adorno)):
    m = re.search(r'<symbol id="' + id_ + r'" viewBox="[^"]*">.*?</symbol>', s, flags=re.S)
    assert m, id_
    s = s[:m.start()] + nuevo + s[m.end():]
k = s.index('</defs></svg>')
s = s[:k] + b.DEFS + s[k:]

# 3) portada: arco de piedra bordado con balaustrada y la foto en la ventana
i = s.index('<section id="inicio"')
j = s.index('</section>', i) + len('</section>')
portada = ('<section id="inicio" class="lino" style="position: relative; overflow: hidden; height: 800px">\n'
           '<div class="{{claseCarta}}" style="position: relative; width: 420px; height: 800px; margin: 0 auto; transform-origin: 50% 40%">\n'
           '<div class="foto-arco" role="img" aria-label="Rofelia con su vestido verde" style="position: absolute; left: 76px; top: 118px; width: 268px; height: 452px; border-radius: 134px 134px 0 0; box-shadow: inset 0 0 18px rgba(47,58,28,0.35)"></div>\n'
           '<div class="velo-lino" aria-hidden="true" style="position: absolute; left: 76px; top: 118px; width: 268px; height: 452px; border-radius: 134px 134px 0 0; pointer-events: none"></div>\n'
           '<svg aria-hidden="true" width="420" height="800" viewBox="0 0 420 800" style="position: absolute; inset: 0"><g filter="url(#bordado)">'
           + c.arco() + c.balaustrada() + c.flora_portada() + '</g></svg>\n'
           '<div class="{{claseTexto}}" style="--base: {{baseAnim}}; position: absolute; left: 20px; right: 20px; top: 656px; display: flex; flex-direction: column; align-items: center; text-align: center; gap: 0">\n'
           '<p style="animation-delay: calc(var(--base) + 0.35s); margin: 0; font-family: Cinzel, serif; font-weight: 600; font-size: 10.5px; letter-spacing: 2.5px; line-height: 1.6; color: #4A5E33">CON TODO CARIÑO TE INVITAMOS<br>A CELEBRAR LOS 50 AÑOS DE</p>\n'
           '<p class="escribe" style="animation-delay: calc(var(--base) + 0.9s); margin: 0; padding: 0 8px; font-family: \'Great Vibes\', cursive; font-size: 50px; line-height: 1; color: #2F3A22">Rofelia</p>\n'
           '<p class="escribe" style="animation-delay: calc(var(--base) + 2.2s); margin: 0; padding: 0 8px; font-family: \'Great Vibes\', cursive; font-size: 28px; line-height: 1.1; color: #2F3A22">Veramendi Gamboa</p>\n'
           '<p style="animation-delay: calc(var(--base) + 3.4s); margin: 4px 0 0; font-family: Cinzel, serif; font-size: 11.5px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; color: #4A5E33">{{fechaLarga}}</p>\n'
           '</div>\n</div>\n</section>')
s = s[:i] + portada + s[j:]

# 4) fondos de lino en toda la invitación
m = re.search(r'<div style="(position: relative; width: 100%; max-width: 480px; margin: 0 auto; min-height: 100vh; box-sizing: border-box; )background: #F7F9F0; ', s)
assert m
s = s[:m.start()] + '<div class="lino" style="' + m.group(1) + s[m.end():]
s = s.replace('background: #E9F0DA;', 'background: rgba(200,214,172,0.3);')
s = s.replace('background: radial-gradient(ellipse at 50% 30%, #F3F7EA, #E2EBD1)', 'background: rgba(255,255,255,0.16)')

# 5) CSS
css = ('.lino{background-color:#E4EBD6;background-image:url(' + LINO + ');background-size:320px 320px}'
       '.foto-arco{background:#EDE4E8 url(' + FOTO + ') 70% 0/cover no-repeat}'
       '.velo-lino{background:radial-gradient(ellipse 75% 60% at 50% 45%, rgba(228,235,214,0) 55%, rgba(110,125,67,0.28) 100%), linear-gradient(180deg, rgba(214,226,190,0.18), rgba(214,226,190,0) 40%, rgba(63,82,38,0.12)), url(' + LINO + ');background-size:auto, auto, 320px 320px;mix-blend-mode:multiply;opacity:.9}'
       '.bp{transform-box:fill-box;transform-origin:50% 50%}.carta-espera .bp{opacity:0}'
       '.carta-entra .bp{animation:florBrota .9s cubic-bezier(.3,1.5,.5,1) both}'
       '@media (prefers-reduced-motion:reduce){.carta-entra .bp{animation:none}}')
one('nav a{color:#3F5226;text-decoration:none}', 'nav a{color:#3F5226;text-decoration:none}\n' + css)
open(p, 'w', encoding='utf-8').write(s)
print('ok', len(s))
