"""Convierte los marcos con foto en carruseles deslizables (scroll-snap) con puntitos y toque para avanzar."""
import re
import sys

p = sys.argv[1]
s = open(p, encoding='utf-8').read()

FOTOS = {
    # Retrato de la Reina: vestido verde (portada) y el trono
    'retrato': [('/_blob/46a35271e1f8f4635ab8116474f4c852', '50% 55%')],
    # Fiestas: bailando con el oso y abrazada al oso
    'fiestas': [('/_blob/2ff35ff0b052922acf2b713d649677f9', '40% 60%'), ('/_blob/ff19bab2dead28219ffa426869fc8c3f', '62% 35%')],
    # Paseos: escaleras y patio con plantas
    'paseos': [('/_blob/8bb4ffcb68ecab3eef8ad752dfeda33f', '45% 45%'), ('/_blob/4cea7a499eb1de9508cb81ac883d3650', '50% 50%')],
    # En familia: playa y mariachis
    'familia': [('/_blob/14ddda6ddf706641b2d74b41ed4114e3', '50% 45%'), ('/_blob/8dcd2b1b9bbca58d64b64d08a1f6bc49', '55% 50%')],
    # Hoy: selfie con gorra y camiseta de España
    'hoy': [('/_blob/57852b1e024459e83e522314bd49c412', '55% 30%'), ('/_blob/d4f144a312145dab0865a553e8d03b00', '55% 30%')],
}


def one(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90])
    s = s.replace(a, b)


css = []
for nombre, fotos in FOTOS.items():
    m = re.search(r'<div class="foto-' + nombre + r'" style="([^"]*)"></div>', s)
    assert m, nombre
    estilo = m.group(1)
    estilo = re.sub(r'display: flex;.*$', 'overflow: hidden;', estilo)  # conserva posición, tamaño y radio
    radio = 'border-radius: 50%; ' if 'border-radius: 50%' in estilo else ''
    slides = ''.join(f'<div class="fx-{nombre}-{i + 1}" style="flex: 0 0 100%; height: 100%; scroll-snap-align: center; scroll-snap-stop: always"></div>'
                     for i in range(len(fotos)))
    nuevo = (f'<div class="carrusel-marco" style="{estilo}">'
             f'<div class="carrusel" role="region" aria-label="Fotos, desliza para ver más" onScroll="{{{{car.{nombre}.onScroll}}}}" onClick="{{{{car.{nombre}.siguiente}}}}" '
             f'style="position: absolute; inset: 0; display: flex; overflow-x: auto; overflow-y: hidden; scroll-snap-type: x mandatory; -webkit-overflow-scrolling: touch; scrollbar-width: none; cursor: pointer; {radio}">{slides}</div>'
             f'<div aria-hidden="true" style="position: absolute; inset: 0; pointer-events: none; {radio}box-shadow: inset 0 4px 14px rgba(47,66,24,0.3)"></div>'
             f'<div aria-hidden="true" style="position: absolute; left: 0; right: 0; bottom: {"9%" if radio else "5%"}; display: flex; justify-content: center; gap: 6px; pointer-events: none">'
             f'<sc-for list="{{{{car.{nombre}.puntos}}}}" as="pt" hint-placeholder-count="{len(fotos)}"><span style="{{{{pt.estilo}}}}"></span></sc-for></div>'
             f'</div>')
    s = s[:m.start()] + nuevo + s[m.end():]
    for i, (url, pos) in enumerate(fotos):
        css.append(f'.fx-{nombre}-{i + 1}{{background:#E2EBD1 url({url}) {pos}/cover no-repeat}}')
    # quitar la regla vieja
    s, k = re.subn(r'\.foto-' + nombre + r'\{[^}]*\}', '', s, count=1)
    assert k == 1

css.append('.carrusel::-webkit-scrollbar{display:none}')
# los marcos dibujados encima no deben bloquear el deslizamiento
s = s.replace('<svg ref="{{ver}}" class="aguarda traza" aria-hidden="true" viewBox="0 0 340 440" style="position: absolute; inset: 0;',
              '<svg ref="{{ver}}" class="aguarda traza" aria-hidden="true" viewBox="0 0 340 440" style="pointer-events: none; position: absolute; inset: 0;')
s = s.replace('<svg ref="{{ver}}" class="aguarda traza" aria-hidden="true" viewBox="0 0 170 220" style="position: absolute; inset: 0;',
              '<svg ref="{{ver}}" class="aguarda traza" aria-hidden="true" viewBox="0 0 170 220" style="pointer-events: none; position: absolute; inset: 0;')
one('nav a{color:#3F5226;text-decoration:none}', 'nav a{color:#3F5226;text-decoration:none}\n' + ''.join(css))

# lógica: índice por carrusel, puntitos y toque para avanzar
conteos = ', '.join(f"{n}: {len(f)}" for n, f in FOTOS.items())
one("      familias, pedirFamilia, familiaLista,",
    "      car: Object.fromEntries(Object.entries({" + conteos + "}).map(([n, total]) => {\n"
    "        const idx = (s.carrusel && s.carrusel[n]) || 0;\n"
    "        const pon = (i) => this.setState({ carrusel: { ...(this.state.carrusel || {}), [n]: i } });\n"
    "        return [n, {\n"
    "          puntos: Array.from({ length: total }, (_, i) => ({ estilo: 'display: block; width: ' + (i === idx ? '16px' : '7px') + '; height: 7px; border-radius: 4px; background: ' + (i === idx ? '#FFFFFF' : 'rgba(255,255,255,0.6)') + '; box-shadow: 0 1px 3px rgba(0,0,0,0.45); transition: width .25s' })),\n"
    "          onScroll: (e) => { const el = e.currentTarget; const i = Math.round(el.scrollLeft / Math.max(1, el.clientWidth)); if (i !== idx) pon(i); },\n"
    "          siguiente: (e) => { const el = e.currentTarget; const i = (Math.round(el.scrollLeft / Math.max(1, el.clientWidth)) + 1) % total; el.scrollTo({ left: i * el.clientWidth, behavior: 'smooth' }); }\n"
    "        }];\n"
    "      })),\n"
    "      familias, pedirFamilia, familiaLista,")
open(p, 'w', encoding='utf-8').write(s)
print('ok')
