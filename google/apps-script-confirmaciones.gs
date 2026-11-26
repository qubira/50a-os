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

function guardar(datos) {
  var hoja = SpreadsheetApp.openById(ID_HOJA).getSheets()[0];
  var valores = hoja.getDataRange().getValues();
  var encabezados = valores[0];
  var colConf = columna(hoja, encabezados, 'Confirmación', true);
  var colRegalo = columna(hoja, encabezados, 'Regalo', true);
  var colFecha = columna(hoja, encabezados, 'Respondió el', true);
  for (var i = 1; i < valores.length; i++) {
    var mismoId = datos.id != null && String(valores[i][0]).trim() === String(datos.id).trim();
    if (!mismoId || clave(valores[i][1]) !== clave(datos.nombre)) continue;
    var n = Number(datos.personas) || 0;
    var texto = datos.asiste ? 'Confirmado – ' + n + (n === 1 ? ' persona' : ' personas') : 'No asistirá';
    hoja.getRange(i + 1, colConf).setValue(texto);
    hoja.getRange(i + 1, colRegalo).setValue(datos.regalo || '');
    hoja.getRange(i + 1, colFecha).setValue(new Date());
    return;
  }
}

// Para probar desde el editor: elige "probar" en la lista y pulsa Ejecutar.
// Escribe en la fila N.º 1 (cámbialo si quieres) y luego vuelve a poner "Pendiente de confirmar" a mano.
function probar() {
  guardar({ id: '1', nombre: 'Rosella', asiste: true, personas: 1, regalo: 'Perfume' });
}
