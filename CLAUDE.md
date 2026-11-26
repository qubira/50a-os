# Invitación 50 años — Rofelia Veramendi Gamboa

Invitación digital (verde pacay, estilo realeza inglesa / cuento de hadas) hecha como
artboard de **Claude Design**. Publicada en: https://claude.ai/artifact/AdfThCnbjatiC22ezy8Nv3

## Estructura
- `project/Main.dc.html` — fuente de la invitación (formato `.dc.html` de Claude Design:
  markup dentro de `<x-dc>`, lógica en `class Component extends DCLogic` con `renderVals()`).
  No se abre directo en el navegador: necesita el runtime de Claude Design.
- `project/canvas.json` — índice del lienzo (un artboard, `is_interactive`, `expand: fill`).
- `recursos/lazo/` — imágenes del lazo. En el artifact están subidas como
  `/_blob/d192d68e52e97bdb85e09e07087d2468` (quieto) y `/_blob/5f3db68a8fa484e5d626c933cc4b0d73`
  (tira de 56 cuadros, 8×7, 480×406 cada uno).
- `recursos/fotos/` — fotos subidas al artifact (clases CSS en el `<helmet>`):
  `fondo-portada.jpg` → `.portada-foto` (`/_blob/5a4fbaf4dd6b78b2e6eda0e233e9d879`),
  Marcos de "Mi historia" = carruseles deslizables (`herramientas/carruseles.py`, lista `FOTOS`):
  retrato, Fiestas, Paseos, En familia y Hoy (2 fotos cada uno); clases `.fx-<marco>-<n>`, índice en `state.carrusel`.
  Los originales están en `../IMAGENES/`. Los óvalos "Infancia"/"Juventud" pasaron a llamarse FIESTAS y PASEOS.
- `recursos/musica/vivir-mi-vida.mp4` — la canción (original en `../MUSICA/`) metida en un .mp4 de solo audio
  con `herramientas/mp3_a_mp4.py` (los .mp3 no se aceptan como asset ni cargan como archivo del proyecto).
  Subida como `/_blob/95c09ea83465813c2b7c0307b45fc37e`, prop `musica`. Suena con `tocar()` en el mismo toque del lazo.
- `google/apps-script-confirmaciones.gs` — script de Google que escribe las confirmaciones en la hoja.
- `herramientas/` — scripts Python (Pillow) que sacaron los cuadros del lazo y armaron la tira.
- `versiones/` — primera versión independiente (HTML normal, se abre en cualquier navegador).

## Estilo actual: bordado sobre lino (versión 47)
- Fondo de lino `recursos/bordado/lino.jpg` → `/_blob/86ca6db8fe728776d4360789e4caac66` (clase `.lino`).
- `herramientas/bordado.py`: motivos en SVG con puntadas calculadas (hoja, rosa, orquídea, glicina, hiedra, capullo)
  y `DEFS` (gradiente `nudo`, filtro `bordado`, patrón `piedra`). `herramientas/composicion.py`: puertas,
  arco con balaustrada, flora de la portada y símbolos `rosaV`/`rosa`/`hoja`/`adorno` bordados.
- `herramientas/reconstruir.py recursos/base-v46.dc.html project/Main.dc.html` rehace todo el estilo bordado
  desde la base guardada (aplicar_bordado → óvalos cortos y sin "Palabra para la reina" → retrato solo con el trono
  → pulir_secciones). Si se cambian motivos o la portada, editar los scripts y correr esto.
- Portada: foto en la ventana del arco (`.foto-arco`), flores que brotan al abrir (`.bp`).

## Cómo publicar cambios
Edita `project/Main.dc.html` y publícalo con la herramienta Artifact:
`url` = https://claude.ai/artifact/AdfThCnbjatiC22ezy8Nv3, `root` = esta carpeta,
`file_path` = `project/Main.dc.html`. Una imagen nueva se sube con `asset: true` y se usa su `/_blob/<id>`.

## Datos del evento
- Viernes 11 de diciembre de 2026, 7:00 p. m. (prop `fecha` = `2026-12-11T19:00:00`).
- Elite Recepciones y Eventos — Paradero Arica, Av. Buenos Aires, Puente Piedra, Lima.
  Mapa: https://maps.app.goo.gl/4qMfbSf26ZC9ea8F7

## Invitados y confirmaciones
- Hoja de Google (prop `hoja`): https://docs.google.com/spreadsheets/d/1LUQ8exWlAte9zI2oxrd9SuNDqG85873wbvX_2Z-_9fc
  Columnas: FAMILIA · NOMBRE DE INVITADOS · TIPO DE REGALO · ¿CONFIRMARON?  (una fila por persona).
  Se lee con `.../gviz/tq?tqx=out:csv`.
- La familia sale de `?familia=` (o `#familia=`) en el enlace; si no coincide con la hoja,
  la portada y la tarjeta muestran una lista para elegirla.
- Confirmaciones: POST (JSON) a la aplicación web de Apps Script (prop `urlRespuestas`):
  https://script.google.com/macros/s/AKfycbxovDkrvMV5r17qy3gfgY8JU-bZx-XKtZwZDLA0NimmgPombntmNjEZT_8n5aKoh7xc3g/exec
  Implementada como "Ejecutar como: Yo" y acceso "Cualquier persona".

## Animaciones (todas en CSS/SMIL, sin JS de dibujo)
- Portada: lazo fotográfico que se desata (tira de cuadros con `steps()`), cae, se abren las puertas, la carta se acerca y aparecen las letras.
- Sobre: el sello late, la solapa se abre y la carta sale (`sb-*`).
- Secciones que se activan al verse (clase `visto` puesta por un IntersectionObserver vía `ref="{{ver}}"`):
  flores que brotan (`brota`), versículo letra por letra (`letras`), sello que cae (`sello`),
  marcos que se dibujan (`traza`, `tz-*`).
- Recepción: aves aleteando y parejas caminando (SMIL dentro del SVG del edificio).

## Versión web (Vercel)
- Repositorio: https://github.com/qubira/50a-os · Vercel sirve la carpeta `web/` (ver `vercel.json`).
- `web/index.html` se genera con `python herramientas/exportar_web.py` desde `project/Main.dc.html`
  (después de cualquier cambio de diseño: reconstruir → exportar → subir). Las fotos están en `web/a/` con el id del blob.
- `web/dc.js` = motor mínimo que entiende el formato DC; `web/logica.js` = lógica de la versión web (editar a mano).
- Invitación personal: `/i/<N.º>` (columna A de la hoja). Hoja: A N.º · B Nombre · C Adicionales · D Total de personas ·
  E Modalidad · F Confirmación · G Observaciones · H celular. La respuesta escribe "Confirmado – N personas" / "No asistirá"
  en F, más las columnas "Regalo" y "Respondió el" (el Apps Script las crea si faltan).
- `/enviar` = lista de invitados con botón de WhatsApp y su enlace personal.
- Probar en local: `python herramientas/servidor_local.py` → http://localhost:8940/i/1
