// Recibe las confirmaciones de la invitación y las escribe en la hoja.
// Hoja: A N.º · B Nombre · C Adicionales · D Total de personas · E Modalidad · F Confirmación · G Observaciones · H celular
// Escribe en "Confirmación" y en "Regalo" (si esa columna no existe, la crea al final).
var ID_HOJA = '1LUQ8exWlAte9zI2oxrd9SuNDqG85873wbvX_2Z-_9fc';

function doPost(e) {
  if (!e || !e.postData) return ContentService.createTextOutput('sin datos');
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    guardar(JSON.parse(e.postData.contents));
  } finally {
    lock.releaseLock();
  }
  return ContentService.createTextOutput('ok');
}

function clave(x) {
  return String(x == null ? '' : x).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/\s+/g, ' ').trim();
}

function columna(hoja, encabezados, nombre, crear) {
  for (var i = 0; i < encabezados.length; i++) if (clave(encabezados[i]) === clave(nombre)) return i + 1;
  if (!crear) return 0;
  var c = hoja.getLastColumn() + 1;
  hoja.getRange(1, c).setValue(nombre);
  return c;
}

// La lista de invitados es la pestaña con gid=0 ("Hoja 1"), aunque haya otras pestañas antes (dashboard).
function hojaInvitados() {
  var libro = SpreadsheetApp.openById(ID_HOJA);
  var hojas = libro.getSheets();
  for (var i = 0; i < hojas.length; i++) if (hojas[i].getSheetId() === 0) return hojas[i];
  for (var j = 0; j < hojas.length; j++) if (clave(hojas[j].getRange(1, 2).getValue()) === 'nombre') return hojas[j];
  return hojas[0];
}

function guardar(datos) {
  var hoja = hojaInvitados();
  var valores = hoja.getDataRange().getValues();
  var encabezados = valores[0];
  for (var i = 1; i < valores.length; i++) {
    var mismoId = datos.id != null && String(valores[i][0]).trim() === String(datos.id).trim();
    if (!mismoId || clave(valores[i][1]) !== clave(datos.nombre)) continue;
    if (datos.tipo === 'regalo') {
      // El regalo llega aparte, apenas el invitado toca "Lo regalo" (no depende de la confirmación).
      hoja.getRange(i + 1, columna(hoja, encabezados, 'Regalo', true)).setValue(datos.regalo || '');
      hoja.getRange(i + 1, columna(hoja, hoja.getRange(1, 1, 1, hoja.getLastColumn()).getValues()[0], 'Regalo elegido el', true)).setValue(new Date());
      return;
    }
    var n = Number(datos.personas) || 0;
    var texto = datos.asiste ? 'Confirmado – ' + n + (n === 1 ? ' persona' : ' personas') : 'No asistirá';
    hoja.getRange(i + 1, columna(hoja, encabezados, 'Confirmación', true)).setValue(texto);
    hoja.getRange(i + 1, columna(hoja, hoja.getRange(1, 1, 1, hoja.getLastColumn()).getValues()[0], 'Respondió el', true)).setValue(new Date());
    return;
  }
}

// Para probar desde el editor: elige "probar" en la lista y pulsa Ejecutar.
// Escribe en la fila N.º 1 (cámbialo si quieres) y luego vuelve a poner "Pendiente de confirmar" a mano.
function probar() {
  guardar({ id: '1', nombre: 'Rosella', asiste: true, personas: 1 });
  guardar({ tipo: 'regalo', id: '1', nombre: 'Rosella', regalo: 'Perfume' });
}
