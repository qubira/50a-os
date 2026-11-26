"""Rediseño de la portada: foto en arco dorado, cortinas que se abren, texto abajo sin tarjeta."""
import re
import sys

p = sys.argv[1]
s = open(p, encoding='utf-8').read()


def one(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:100])
    s = s.replace(a, b)


one('<section id="inicio" class="portada-foto" style="position: relative; overflow: hidden; height: 800px">',
    '<section id="inicio" style="position: relative; overflow: hidden; height: 800px; background: #C9DAA8">')
one('<div class="{{claseCarta}}" style="position: relative; width: 420px; height: 800px; margin: 0 auto; transform-origin: 50% 42%">\n<svg aria-hidden="true" width="420" height="800" viewBox="0 0 420 800" style="position: absolute; inset: 0">',
    '<div class="{{claseCarta}}" style="position: relative; width: 420px; height: 800px; margin: 0 auto; transform-origin: 50% 42%; background: radial-gradient(ellipse 70% 55% at 50% 34%, #F6F9EF 0%, #E4EDD0 55%, #C3D69F 100%)">\n'
    '<div class="foto-arco" role="img" aria-label="Rofelia con su vestido verde" style="position: absolute; left: 80px; top: 66px; width: 260px; height: 396px; border-radius: 130px 130px 0 0; box-shadow: inset 0 0 0 1px rgba(255,255,255,0.5), inset 0 -40px 40px -20px rgba(47,66,24,0.25)"></div>\n'
    '<svg aria-hidden="true" width="420" height="800" viewBox="0 0 420 800" style="position: absolute; inset: 0">'
    '<g filter="url(#relieveV)"><path d="M80 462V196A130 130 0 0 1 340 196V462" fill="none" stroke="url(#oro)" stroke-width="7"/>'
    '<path d="M70 462V196A140 140 0 0 1 350 196V462" fill="none" stroke="#DCE8C5" stroke-width="9"/>'
    '<rect x="58" y="458" width="304" height="12" rx="3" fill="url(#oroV)"/><rect x="66" y="470" width="288" height="7" rx="2" fill="#D5E3BA"/></g>'
    '<path d="M89 456V196A121 121 0 0 1 331 196V456" fill="none" stroke="#FFFDF5" stroke-width="4" stroke-dasharray="0.1 7" stroke-linecap="round" filter="url(#relieveV)"/>'
    '<path d="M70 196A140 140 0 0 1 350 196" fill="none" stroke="#F6F9EF" stroke-width="4.5" stroke-dasharray="0.1 8" stroke-linecap="round" filter="url(#relieveV)"/>'
    '<g filter="url(#relieveV)"><use href="#hoja" x="178" y="48" width="26" height="12" transform="rotate(-20 191 54)"/><use href="#hoja" x="216" y="48" width="26" height="12" transform="rotate(20 229 54)"/><use href="#rosaV" x="196" y="40" width="28" height="28"/>'
    '<use href="#hoja" x="54" y="444" width="26" height="12" transform="rotate(-30 67 450)"/><use href="#rosaV" x="66" y="440" width="24" height="24"/><use href="#hoja" x="340" y="444" width="26" height="12" transform="rotate(30 353 450)"/><use href="#rosaV" x="330" y="440" width="24" height="24"/></g>'
    '</svg>\n'
    '<svg aria-hidden="true" width="420" height="800" viewBox="0 0 420 800" style="position: absolute; inset: 0">')
# quitar las borlas que colgaban sobre el arco
L = s.split('\n')
n = [i for i, x in enumerate(L) if x.startswith('<g filter="url(#relieveV)"><path d="M210 36V56" stroke="url(#oroV)"')]
assert len(n) == 1
del L[n[0]]
s = '\n'.join(L)

# texto: abajo, sobre el papel, sin tarjeta
s = re.sub(r'style="--base: \{\{baseAnim\}\}; position: absolute; left: 30px; right: 30px; bottom: 56px;[^"]*"',
           'style="--base: {{baseAnim}}; position: absolute; left: 24px; right: 24px; top: 488px; display: flex; flex-direction: column; align-items: center; text-align: center; gap: 0"', s, count=1)
assert 'top: 488px' in s


def tam(prefijo, viejo, nuevo):
    global s
    pat = re.compile(r'(' + re.escape(prefijo) + r'[^"]*?)' + re.escape(viejo))
    s, k = pat.subn(lambda m: m.group(1) + nuevo, s, count=1)
    assert k == 1, prefijo


s = s.replace('<svg aria-hidden="true" width="38" height="28" viewBox="0 0 64 48" fill="#5E7838"', '<svg aria-hidden="true" width="30" height="22" viewBox="0 0 64 48" fill="#5E7838"', 1)
tam('<p style="animation-delay: calc(var(--base) + 0.35s);', 'line-height: 1.7', 'line-height: 1.6')
tam('<p class="c50" style="', 'font-size: 72px', 'font-size: 60px')
tam('<p style="animation-delay: calc(var(--base) + 1.7s);', 'font-size: 20px; letter-spacing: 8px', 'font-size: 16px; letter-spacing: 7px')
tam('<p style="animation-delay: calc(var(--base) + 2.1s);', 'font-size: 30px', 'font-size: 24px')
tam('<p class="escribe" style="animation-delay: calc(var(--base) + 2.4s);', 'font-size: 50px', 'font-size: 46px')
tam('<p class="escribe" style="animation-delay: calc(var(--base) + 3.8s);', 'font-size: 30px', 'font-size: 26px')
tam('<svg aria-hidden="true" width="160" height="14" viewBox="0 0 160 14" style="animation-delay: calc(var(--base) + 5.2s);', 'margin-top: 6px', 'margin-top: 2px')
tam('<p style="animation-delay: calc(var(--base) + 5.5s);', 'font-size: 20px', 'font-size: 17px')
one('font-size: 11px; letter-spacing: 3px; color: #3F5226">DESLIZA ↓</p>', 'font-size: 10px; letter-spacing: 3px; color: #3F5226">DESLIZA ↓</p>')
s = s.replace('position: absolute; left: 0; right: 0; bottom: 22px; margin: 0; text-align: center; font-family: Cinzel, serif; font-weight: 600; font-size: 10px',
              'position: absolute; left: 0; right: 0; bottom: 14px; margin: 0; text-align: center; font-family: Cinzel, serif; font-weight: 600; font-size: 10px', 1)

# CSS: foto en el arco y cortinas que se abren desde cerradas
s = re.sub(r'\.portada-foto\{background:#E9E0E4 url\((/_blob/[0-9a-f]+)\) 62% 0/cover no-repeat\}',
           r'.foto-arco{background:#EDE4E8 url(\1) 76% 28%/170% auto no-repeat}', s, count=1)
assert '.foto-arco{' in s
one('.cortina{transform-box:fill-box;transform-origin:0% 50%;transform:scaleX(.5)}.carta-espera .cortina{transform:none}'
    '.carta-entra .cortina{animation:abrirCortina 2.6s cubic-bezier(.55,0,.2,1) 3.5s both}'
    '@keyframes abrirCortina{0%{transform:none}70%{transform:scaleX(.46)}85%{transform:scaleX(.52)}100%{transform:scaleX(.5)}}',
    '.cortina{transform-box:fill-box;transform-origin:0% 50%}.carta-espera .cortina{transform:scaleX(1.24)}'
    '.carta-entra .cortina{animation:abrirCortina 2.4s cubic-bezier(.55,0,.2,1) 3.3s both}'
    '@keyframes abrirCortina{0%{transform:scaleX(1.24)}72%{transform:scaleX(.96)}86%{transform:scaleX(1.02)}100%{transform:none}}')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
