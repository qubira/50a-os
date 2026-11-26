"""Genera web/index.html (página normal para Vercel) a partir de project/Main.dc.html.
Uso (desde la carpeta del proyecto): python herramientas/exportar_web.py
La lógica de la versión web está en web/logica.js y el motor en web/dc.js.
"""
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(os.path.join(RAIZ, 'project', 'Main.dc.html'), encoding='utf-8').read()

a = s.index('<x-dc>') + len('<x-dc>')
b = s.index('</x-dc>')
cuerpo = s[a:b]
h1 = cuerpo.index('<helmet>')
h2 = cuerpo.index('</helmet>')
cabeza = cuerpo[h1 + len('<helmet>'):h2]
plantilla = cuerpo[h2 + len('</helmet>'):]


def una(t, viejo, nuevo, n=1):
    assert t.count(viejo) == n, (t.count(viejo), viejo[:80])
    return t.replace(viejo, nuevo)


# Las imágenes subidas a Claude (/_blob/<id>) están copiadas en web/a/
carpeta = os.path.join(RAIZ, 'web', 'a')
archivos = {os.path.splitext(f)[0]: f for f in os.listdir(carpeta)}


def blob(m):
    return '/a/' + archivos[m.group(1)]


cabeza = re.sub(r'/_blob/([0-9a-f]{32})', blob, cabeza)
plantilla = re.sub(r'/_blob/([0-9a-f]{32})', blob, plantilla)

# Sin lista de familias: cada invitado llega con su enlace personal
plantilla, n = re.subn(r'<sc-if value="\{\{pedirFamilia\}\}"[^>]*>.*?</sc-if>', '', plantilla, flags=re.S)
assert n == 2

# Tarjeta de confirmación para una persona (con sus acompañantes)
plantilla = una(plantilla, 'INVITACIÓN PARA LA</p>', '{{tituloTarjeta}}</p>')
plantilla = una(plantilla, 'color: #3F5226">Familia {{familia}}</p></sc-if>', 'color: #3F5226">{{familia}}</p></sc-if>')
reserva = '<p style="margin: 2px 0 0; font-size: 18px; color: #3F4A30">Hemos reservado <strong style="color: #2F3A22">{{cuposTexto}}</strong> en su honor</p>'
plantilla = una(plantilla, reserva,
                '<sc-if value="{{familiaLista}}">' + reserva.replace('en su honor', 'en tu honor') + '</sc-if>'
                '<sc-if value="{{!familiaLista}}"><p style="margin: 10px 0 0; font-size: 18px; line-height: 1.45; color: #3F4A30">{{avisoLista}}</p></sc-if>')
plantilla = una(plantilla, '<sc-if value="{{noEnviado}}" hint-placeholder-val="{{ true }}">\n<form',
                '<sc-if value="{{noEnviado && familiaLista}}">\n<form')
plantilla = una(plantilla, '¿ASISTIRÁN AL BAILE?</span>', '{{preguntaAsiste}}</span>')
plantilla = una(plantilla, '>Sí, asistiremos</button>', '>{{textoSi}}</button>')
plantilla = una(plantilla, '>No podremos ir</button>', '>{{textoNo}}</button>')
plantilla = una(plantilla, '<sc-if value="{{esSi}}" hint-placeholder-val="{{ true }}">', '<sc-if value="{{esSi && hayLista}}">')
plantilla = una(plantilla, '¿QUIÉNES ASISTIRÁN?', '¿CUÁNTOS ASISTIRÁN?')
plantilla = una(plantilla, 'Toca un nombre para marcarlo o desmarcarlo.', 'Elige cuántas personas vendrán, contándote a ti.')
plantilla = una(plantilla, 'aria-label="Invitados de la familia"', 'aria-label="Cuántas personas asistirán"')
plantilla = una(plantilla, 'ENVIAR RESPUESTA</button>', '{{textoEnviar}}</button>')
plantilla = una(plantilla, '¡Gracias, familia {{familia}}!', '¡Gracias, {{nombreCorto}}!')

titulo = 'Invitación · 50 años de Rofelia'
html = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{titulo}</title>
<meta name="description" content="Te invito a celebrar mis 50 años. Viernes 11 de diciembre de 2026, 7:00 p. m.">
<meta name="theme-color" content="#56663D">
<meta name="robots" content="noindex">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="Viernes 11 de diciembre de 2026 · Elite Recepciones y Eventos, Puente Piedra">
<meta property="og:image" content="/a/portada-og.jpg">
<meta property="og:type" content="website">
{cabeza.strip()}
</head>
<body>
<div id="app"></div>
<template id="dc">{plantilla.strip()}</template>
<script src="/dc.js"></script>
<script src="/logica.js"></script>
</body>
</html>
'''
open(os.path.join(RAIZ, 'web', 'index.html'), 'w', encoding='utf-8').write(html)
print('web/index.html', len(html))
