"""Reconstruye Main.dc.html desde la base de la versión 46 aplicando todos los pasos del estilo bordado.
Uso (desde herramientas/): python reconstruir.py <base_v46.dc.html> ../project/Main.dc.html
"""
import re
import shutil
import subprocess
import sys

base, destino = sys.argv[1], sys.argv[2]
shutil.copy(base, destino)


def correr(script):
    subprocess.run([sys.executable, '-I', '-c', f"import sys; sys.path.insert(0,'.'); sys.argv=['x', r'{destino}']; exec(open('{script}', encoding='utf-8').read())"], check=True)


correr('aplicar_bordado.py')

s = open(destino, encoding='utf-8').read()
# óvalos más cortos
assert s.count('aspect-ratio: 170 / 220') == 4
s = s.replace('aspect-ratio: 170 / 220', 'aspect-ratio: 170 / 192')
s = s.replace('viewBox="0 0 170 220" style="pointer-events: none;', 'viewBox="0 0 170 220" preserveAspectRatio="none" style="pointer-events: none;')
# sin la sección "Palabra para la reina"
i = s.index('PALABRA PARA LA REINA')
a = s.rindex('<section', 0, i)
b = s.index('</section>', i) + len('</section>')
s = s[:a] + s[b:].lstrip('\n')
# retrato sin la foto de la portada (queda solo la del trono)
s, n = re.subn(r'<div class="fx-retrato-1" style="[^"]*"></div>', '', s)
assert n == 1
s = s.replace('retrato: 2, fiestas: 2', 'retrato: 1, fiestas: 2')
# el resplandor de la apertura se enciende y se apaga; la capa de puertas no bloquea toques al abrirse
a = '.resplandor{opacity:0;transition:opacity 1.6s 2.6s}.abriendo .resplandor{opacity:1}'
assert s.count(a) == 1
s = s.replace(a, '.resplandor{opacity:0}.abriendo .resplandor{animation:destello 3.2s ease 2.4s both}@keyframes destello{0%{opacity:0}40%{opacity:1}100%{opacity:0}}.abriendo{pointer-events:none}')
open(destino, 'w', encoding='utf-8').write(s)

correr('pulir_secciones.py')

# Mientras las puertas están cerradas o abriéndose solo existe la portada: así, al abrir el lazo,
# detrás de las puertas aparece la portada y no otra parte de la invitación.
s = open(destino, encoding='utf-8').read()
i = s.index('<section id="inicio"')
k = s.index('</section>', i) + len('</section>')
f = s.index('</footer>', k) + len('</footer>')
s = s[:k] + '\n<sc-if value="{{portadaAbierta}}" hint-placeholder-val="{{ true }}">' + s[k:f] + '\n</sc-if>' + s[f:]
# marcos más delgados: la foto ocupa más espacio y el borde queda fino
for viejo, nuevo, n in [
    ('M9 115A76 98 0 1 0 161 115A76 98 0 1 0 9 115ZM29 115A56 76 0 1 1 141 115A56 76 0 1 1 29 115Z',
     'M9 115A76 98 0 1 0 161 115A76 98 0 1 0 9 115ZM17 115A68 90 0 1 1 153 115A68 90 0 1 1 17 115Z', 4),
    ('style="animation-delay: .15s" cx="85" cy="115" rx="67" ry="88"', 'style="animation-delay: .15s" cx="85" cy="115" rx="74" ry="96"', 4),
    ('class="tz-perlas" cx="85" cy="115" rx="58" ry="78"', 'class="tz-perlas" cx="85" cy="115" rx="70.5" ry="92.5"', 4),
    ('style="animation-delay: .3s" cx="85" cy="115" rx="56" ry="76"', 'style="animation-delay: .3s" cx="85" cy="115" rx="68" ry="90"', 4),
    ('left: 17.06%; top: 17.7%; width: 65.9%; height: 69.1%', 'left: 10.59%; top: 11.82%; width: 78.82%; height: 81.82%', 4),
    ('ZM50 80H290V392H50Z', 'ZM32 64H308V408H32Z', 1),
    ('<rect x="41" y="71" width="258" height="330" fill="none" stroke="#EEF4E0" stroke-width="4"/>',
     '<rect x="24" y="56" width="292" height="360" fill="none" stroke="#EEF4E0" stroke-width="2.5"/>', 1),
    ('x="30" y="60" width="280" height="352"', 'x="21" y="53" width="298" height="366"', 1),
    ('class="tz-perlas" x="50" y="80" width="240" height="312"', 'class="tz-perlas" x="28.5" y="60.5" width="283" height="351"', 1),
    ('d="M50 80H290V392H50Z"', 'd="M32 64H308V408H32Z"', 1),
    ('left: 14.7%; top: 18.18%; width: 70.6%; height: 70.9%', 'left: 9.41%; top: 14.55%; width: 81.18%; height: 78.18%', 1),
]:
    assert s.count(viejo) == n, (s.count(viejo), viejo[:50])
    s = s.replace(viejo, nuevo)
a = "this.setState({ puerta: 'abierta' }); }, 5300);"
assert s.count(a) == 1
s = s.replace(a, "this.setState({ puerta: 'abierta' }); try { window.scrollTo(0, 0); } catch (e) {} }, 5300);")
open(destino, 'w', encoding='utf-8').write(s)
print('reconstruido')
