"""Lleva las secciones de abajo al estilo bordado: separadores, tarjetas con puntada, esquinas florales,
recepción tipo tapiz y programa con rosas bordadas."""
import random
import sys
import bordado as b

p = sys.argv[1]
s = open(p, encoding='utf-8').read()


def one(a, bb, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, bb)


SEP = '<svg class="rev-fade" aria-hidden="true" width="210" height="35" viewBox="0 0 240 40" style="align-self: center; margin: 4px 0 2px; overflow: visible"><use href="#adorno" width="240" height="40" filter="url(#bordado)"/></svg>'

# 1) separador bordado bajo cada subtítulo de sección
one('<p style="margin: 0 0 14px; font-style: italic; font-size: 16px; color: #5C6649">El gran día se acerca…</p>',
    '<p style="margin: 0 0 4px; font-style: italic; font-size: 16px; color: #5C6649">El gran día se acerca…</p>' + SEP.replace('margin: 4px 0 2px', 'margin: 0 0 14px'))
one('<p style="margin: 0; font-style: italic; font-size: 16px; color: #46582F">Una vida en pocos capítulos</p>',
    '<p style="margin: 0; font-style: italic; font-size: 16px; color: #46582F">Una vida en pocos capítulos</p>' + SEP)
one('<p style="margin: 0; font-style: italic; font-size: 16px; color: #5C6649">de una noche encantada</p>',
    '<p style="margin: 0; font-style: italic; font-size: 16px; color: #5C6649">de una noche encantada</p>' + SEP)
one('son mis deseos:</p>', 'son mis deseos:</p>' + SEP)
one('<p style="margin: 0; font-style: italic; font-size: 16px; color: #46582F">Antes del {{limiteTexto}}</p>',
    '<p style="margin: 0; font-style: italic; font-size: 16px; color: #46582F">Antes del {{limiteTexto}}</p>' + SEP)

# 2) tarjetas con puntada de hilo (borde interior punteado) sobre lino
PUNTADA = 'outline: 1.5px dashed #A9C084; outline-offset: -6px; box-shadow: 0 3px 10px rgba(47,58,28,0.12)'
one('border-radius: 12px; background: #FFFFFF; border: 1px solid #D4E2BC">',
    'border-radius: 12px; background: rgba(252,250,242,0.94); border: 1px solid #D4E2BC; ' + PUNTADA + '">')
one('<div class="rev-zoom" style="position: relative; background: #F7F9F0; border-radius: 12px; border: 1px solid #B9CD97;',
    '<div class="rev-zoom" style="position: relative; background: rgba(252,250,242,0.94); border-radius: 12px; border: 1px solid #B9CD97; ' + PUNTADA + ';')
one('background: #F7F9F0; border-radius: 12px; border: 1px solid #D4E2BC; padding: 22px 20px">',
    'background: rgba(252,250,242,0.94); border-radius: 12px; border: 1px solid #D4E2BC; padding: 26px 22px; ' + PUNTADA + '">')
one('<div style="background: #F7F9F0; border-radius: 12px; padding: 30px 22px;',
    '<div style="background: rgba(252,250,242,0.94); border-radius: 12px; ' + PUNTADA + '; padding: 30px 22px;')

# 3) programa: rosas bordadas y línea en puntada
one('<span style="width: 9px; height: 9px; background: #EEF4E2; border: 1.5px solid #5E7838; transform: rotate(45deg); margin-top: 7px; flex-shrink: 0"></span>',
    '<svg aria-hidden="true" width="20" height="20" viewBox="0 0 40 40" style="margin-top: 2px; flex-shrink: 0; overflow: visible"><use href="#rosaV" width="40" height="40" filter="url(#bordado)"/></svg>')
one('<span style="flex: 1; width: 1px; background: #B9CD97; margin-top: 4px"></span>',
    '<span style="flex: 1; width: 0; border-left: 1.6px dashed #93A266; margin-top: 4px"></span>')
one('<div style="display: flex; flex-direction: column; align-items: center; width: 14px">',
    '<div style="display: flex; flex-direction: column; align-items: center; width: 20px">')

# 4) recepción como tapiz: lino oscuro, marco dorado en puntada y dibujo en hilo
one('<section id="lugar" style="padding: 50px 26px 54px; background: #56663D;',
    '<section id="lugar" class="lino-oscuro" style="position: relative; padding: 56px 30px 60px; outline: 2px dashed rgba(226,199,126,0.8); outline-offset: -14px;')
one('<g fill="none" stroke="#F1EADA" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" filter="url(#sombra)">',
    '<g fill="none" stroke="#F1EADA" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="3.4 1.2" filter="url(#sombra)">')

# 5) esquinas florales bordadas en programa, regalos y confirmación
r = random.Random(3)


def esquina(espejo=False):
    g = (b.hiedra([(2, 6), (40, 14), (78, 8)], hojas_cada=15, tam=11, rnd=r) + b.hiedra([(6, 2), (12, 40), (6, 78)], hojas_cada=15, tam=11, rnd=r, lado_ini=-1)
         + b.hoja(20, 20, 26, 13, 60, rnd=r) + b.rosa(18, 18, 15, 10) + b.capullo(46, 30, 8, -40))
    t = ' transform="scale(-1 1)" transform-origin="45 45"' if espejo else ''
    lado = 'right: 0' if espejo else 'left: 0'
    return (f'<svg class="rev-fade" aria-hidden="true" width="90" height="90" viewBox="0 0 90 90" style="position: absolute; top: 6px; {lado}; overflow: visible; pointer-events: none">'
            f'<g filter="url(#bordado)"{t}>{g}</g></svg>')


ESQ = esquina() + esquina(True)
one('<section style="padding: 50px 28px 30px; display: flex; flex-direction: column; gap: 20px">',
    '<section style="position: relative; padding: 56px 28px 30px; display: flex; flex-direction: column; gap: 20px">' + ESQ)
one('<section id="regalos" style="padding: 50px 24px; display: flex; flex-direction: column; gap: 12px">',
    '<section id="regalos" style="position: relative; padding: 56px 24px 50px; display: flex; flex-direction: column; gap: 12px">' + ESQ)
one('<section id="confirmar" style="padding: 50px 22px 54px;', '<section id="confirmar" style="position: relative; padding: 56px 22px 54px;')
i = s.index('<section id="confirmar"')
k = s.index('>', i) + 1
s = s[:k] + ESQ + s[k:]

# CSS del tapiz oscuro
LINO = '/_blob/86ca6db8fe728776d4360789e4caac66'
one('nav a{color:#3F5226;text-decoration:none}',
    'nav a{color:#3F5226;text-decoration:none}\n.lino-oscuro{background-color:#56663D;background-image:url(' + LINO + ');background-size:320px 320px;background-blend-mode:multiply}')
open(p, 'w', encoding='utf-8').write(s)
print('ok', len(s))
