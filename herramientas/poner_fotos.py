"""Pone la foto de fondo en la portada y las fotos en los marcos de 'Mi historia'."""
import re
import sys

p = sys.argv[1]
s = open(p, encoding='utf-8').read()
FONDO = '/_blob/5a4fbaf4dd6b78b2e6eda0e233e9d879'
FOTOS = {'retrato': '/_blob/ff19bab2dead28219ffa426869fc8c3f',
         'familia': '/_blob/14ddda6ddf706641b2d74b41ed4114e3',
         'hoy': '/_blob/57852b1e024459e83e522314bd49c412'}


def one(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90])
    s = s.replace(a, b)


L = s.split('\n')
i = [n for n, x in enumerate(L) if x.startswith('<section id="inicio"')][0]
# --- portada: quitar muro, arco, columnas y celosía; dejar cortinas, guirnalda y almenas
quitar = ['<rect width="420" height="800" fill="url(#muro)"/>', '<path d="M88 712V330A122', '<path d="M96 712V332A114',
          '<rect x="0" y="712" width="420" height="88" fill="url(#celosia)"/>', '<g filter="url(#relieveV)" fill="#D5E3BA"><path d="M60 330A150',
          '<g filter="url(#relieveV)"><use href="#hoja" x="132" y="160"', '<g filter="url(#relieveV)"><path d="M94.6 296.9']
nuevas = []
for n, x in enumerate(L):
    if i < n < i + 16 and any(x.startswith(q) for q in quitar):
        continue
    nuevas.append(x)
assert len(L) - len(nuevas) == 7, len(L) - len(nuevas)
s = '\n'.join(nuevas)
one('<section id="inicio" style="position: relative; overflow: hidden; height: 800px; background: #C9DAA8">',
    '<section id="inicio" class="portada-foto" style="position: relative; overflow: hidden; height: 800px">')
one('style="--base: {{baseAnim}}; position: absolute; left: 96px; right: 96px; top: 204px; bottom: 92px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; gap: 3px">',
    'style="--base: {{baseAnim}}; position: absolute; left: 30px; right: 30px; bottom: 56px; padding: 16px 14px 16px; box-sizing: border-box; border-radius: 20px; border: 1px solid rgba(255,255,255,0.8); background: rgba(247,250,240,0.84); box-shadow: 0 8px 24px rgba(47,66,24,0.28); -webkit-backdrop-filter: blur(4px); backdrop-filter: blur(4px); display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; gap: 2px">')
# tamaños más compactos dentro de la tarjeta
s = re.sub(r'(<p class="c50" style="[^"]*?)font-size: 132px', r'\1font-size: 72px', s, count=1)
s = re.sub(r'(<p class="escribe" style="animation-delay: calc\(var\(--base\) \+ 2\.4s\);[^"]*?)font-size: 62px', r'\1font-size: 50px', s, count=1)
s = re.sub(r'(<p class="escribe" style="animation-delay: calc\(var\(--base\) \+ 3\.8s\);[^"]*?)font-size: 38px', r'\1font-size: 30px', s, count=1)
one('DESLIZA ↓</p>', 'DESLIZA ↓</p>'.replace('DESLIZA', 'DESLIZA'))

# --- marcos
def marco(texto_div_ini, clase, quitar_contenido=True):
    global s
    k = s.index(texto_div_ini)
    a = s.rindex('<div style="position: absolute;', 0, k + 1)
    e = s.index('</div>', k) + len('</div>')
    div = s[a:e]
    div2 = re.sub(r'background: radial-gradient\(circle at 50% 40%, #F6F9EF, #E2EBD1\); ', '', div, count=1)
    div2 = div2.replace('<div style=', f'<div class="{clase}" style=', 1)
    if quitar_contenido:
        div2 = re.sub(r'>(<svg aria-hidden="true" width="26".*?</svg>)(RETRATO DE LA REINA)?</div>$', '></div>', div2, flags=re.S)
        assert div2.endswith('"></div>'), div2[-120:]
    s = s[:a] + div2 + s[e:]


marco('RETRATO DE LA REINA</div>', 'foto-retrato')
# óvalos en orden: INFANCIA, JUVENTUD, EN FAMILIA, HOY -> los dos últimos llevan foto
ovals = [m.start() for m in re.finditer(r'<div style="position: absolute; left: 17\.06%; top: 17\.7%;', s)]
assert len(ovals) == 4, len(ovals)
for idx, clase in reversed([(2, 'foto-familia'), (3, 'foto-hoy')]):
    a = ovals[idx]
    e = s.index('</div>', a) + len('</div>')
    div = s[a:e]
    div2 = div.replace('background: radial-gradient(circle at 50% 40%, #F6F9EF, #E2EBD1); ', '', 1).replace('<div style=', f'<div class="{clase}" style=', 1)
    div2 = re.sub(r'><svg aria-hidden="true" width="26".*?</svg></div>$', '></div>', div2, flags=re.S)
    assert div2.endswith('"></div>') and 'radial-gradient(circle at 50% 40%' not in div2, div2[-150:]
    s = s[:a] + div2 + s[e:]

css = ('.portada-foto{background:#E9E0E4 url(' + FONDO + ') 62% 0/cover no-repeat}'
       '.foto-retrato{background:#E2EBD1 url(' + FOTOS['retrato'] + ') 50% 30%/cover no-repeat}'
       '.foto-familia{background:#E2EBD1 url(' + FOTOS['familia'] + ') 50% 45%/cover no-repeat}'
       '.foto-hoy{background:#E2EBD1 url(' + FOTOS['hoy'] + ') 55% 30%/cover no-repeat}')
one('nav a{color:#3F5226;text-decoration:none}', 'nav a{color:#3F5226;text-decoration:none}\n' + css)
open(p, 'w', encoding='utf-8').write(s)
print('ok')
