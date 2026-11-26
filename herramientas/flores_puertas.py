"""Las rosas, hojas y perlas de las puertas brotan al abrir la invitación (de arriba hacia abajo)."""
import re
import sys

p = sys.argv[1]
s = open(p, encoding='utf-8').read()
i = s.index('<symbol id="puertaArt" viewBox="0 0 210 880">')
j = s.index('</symbol>', i)
dentro = s[i + len('<symbol id="puertaArt" viewBox="0 0 210 880">'):j]


def retraso(x, y, base):
    return base + (float(y) / 880) * 2.4 + (float(x) / 210) * 0.35


def envolver_use(m):
    tag = m.group(0)
    x = float(re.search(r' x="([-0-9.]+)"', tag).group(1))
    y = float(re.search(r' y="([-0-9.]+)"', tag).group(1))
    clase = 'flor-p' if '#rosaV' in tag else 'hoja-p'
    return f'<g class="{clase}" style="animation-delay: {retraso(x, y, 0.3):.2f}s">{tag}</g>'


def envolver_perla(m):
    tag = m.group(0)
    x = float(re.search(r' cx="([-0-9.]+)"', tag).group(1))
    y = float(re.search(r' cy="([-0-9.]+)"', tag).group(1))
    return f'<g class="perla-p" style="animation-delay: {retraso(x, y, 0.9):.2f}s">{tag}</g>'


nuevo, n1 = re.subn(r'<use href="#(?:rosaV|hoja)"[^>]*/>', envolver_use, dentro)
# perlas: solo los círculos dentro del grupo de perlas
k = nuevo.index('<g fill="url(#perla)">')
perlas, n2 = re.subn(r'<circle [^>]*/>', envolver_perla, nuevo[k:])
nuevo = nuevo[:k] + perlas
print('flores/hojas:', n1, 'perlas:', n2)

assert s.count('<use href="#puertaArt"/>') == 2
s = s.replace('<use href="#puertaArt"/>', nuevo)
s = s[:i] + s[j + len('</symbol>'):]  # el símbolo ya no se usa

css = ('.flor-p,.hoja-p,.perla-p{transform-box:fill-box;transform-origin:50% 50%}'
       '.flor-p{animation:florBrota 1s cubic-bezier(.3,1.5,.5,1) both}'
       '.hoja-p{animation:hojaBrota .9s cubic-bezier(.3,1.4,.5,1) both}'
       '.perla-p{animation:perla .5s cubic-bezier(.3,1.6,.5,1) both}'
       '@keyframes florBrota{0%{opacity:0;transform:scale(0) rotate(-60deg)}45%{opacity:1}100%{opacity:1;transform:none}}'
       '@keyframes hojaBrota{0%{opacity:0;transform:scale(0) rotate(25deg)}50%{opacity:1}100%{opacity:1;transform:none}}'
       '@media (prefers-reduced-motion:reduce){.flor-p,.hoja-p,.perla-p{animation:none}}')
k = 'nav a{color:#3F5226;text-decoration:none}'
assert s.count(k) == 1
s = s.replace(k, k + '\n' + css)
open(p, 'w', encoding='utf-8').write(s)
print('ok')
