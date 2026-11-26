// Lógica de la invitación (versión web). Cada invitado abre su propio enlace: /i/<N.º de la hoja>.
// Hoja: A N.º · B Nombre · C Adicionales · D Total de personas · E Modalidad · F Confirmación · G Observaciones · H celular
var CONFIG = {
  fecha: '2026-12-11T19:00:00',
  musica: '/a/vivir-mi-vida.mp3',
  hoja: '1LUQ8exWlAte9zI2oxrd9SuNDqG85873wbvX_2Z-_9fc',
  urlRespuestas: 'https://script.google.com/macros/s/AKfycbzNULKIt2OstY0uC-CuDzeR-FY889Eg4iU7UBpoN_pGVzIqlyu6yENKQHXwzPSHlrxXIA/exec'
};

function idDelEnlace() {
  try {
    var m = window.location.pathname.match(/\/i\/([^/?#]+)/);
    if (m) return decodeURIComponent(m[1]).split('-')[0];
    var q = new URLSearchParams(window.location.search);
    var h = new URLSearchParams(String(window.location.hash || '').replace(/^#/, ''));
    return q.get('i') || h.get('i') || null;
  } catch (e) { return null; }
}

function leerCSV(t) {
  var filas = [], fila = [], campo = '', q = false;
  for (var i = 0; i < t.length; i++) {
    var c = t[i];
    if (q) { if (c === '"') { if (t[i + 1] === '"') { campo += '"'; i++; } else q = false; } else campo += c; }
    else if (c === '"') q = true;
    else if (c === ',') { fila.push(campo); campo = ''; }
    else if (c === '\n' || c === '\r') { if (c === '\r' && t[i + 1] === '\n') i++; fila.push(campo); filas.push(fila); fila = []; campo = ''; }
    else campo += c;
  }
  if (campo || fila.length) { fila.push(campo); filas.push(fila); }
  return filas;
}

class Component extends DCLogic {
  constructor(p) {
    super(p);
    this.state = { puerta: 'cerrada', reservados: null, regaloHoja: '', asiste: 'si', cuantos: null, invitado: null, cargado: false, hojaError: false, enviado: false, error: false, sonando: false, qId: idDelEnlace() };
  }
  componentDidMount() {
    this.t = setInterval(() => this.forceUpdate(), 1000);
    // Las fotos de los marcos avanzan solas cada 4 s (cada marco a destiempo); se pausan 7 s si alguien las toca.
    this.carEls = this.carEls || {}; this.carTocado = this.carTocado || {}; this.tick = 0;
    this.tAuto = setInterval(() => {
      this.tick++;
      Object.keys(this.carEls).forEach((n, k) => {
        const el = this.carEls[n];
        if (!el || !el.isConnected || !el.clientWidth || (this.tick + k) % 4 !== 0) return;
        if (Date.now() - (this.carTocado[n] || 0) < 7000) return;
        const total = el.children.length;
        const i = (Math.round(el.scrollLeft / el.clientWidth) + 1) % total;
        el.scrollTo({ left: i * el.clientWidth, behavior: 'smooth' });
      });
    }, 1000);
    this.cargarHoja();
    // Música: suena con el primer toque en cualquier parte (los navegadores no dejan antes) y solo una vez.
    const a = new Audio();
    a.src = CONFIG.musica; a.loop = false; a.preload = 'auto'; a.volume = 0.8;
    a.addEventListener('play', () => this.setState({ sonando: true }));
    a.addEventListener('pause', () => this.setState({ sonando: false }));
    a.addEventListener('ended', () => { this.termino = true; this.setState({ sonando: false, termino: true }); });
    this.audioEl = a;
    this.gesto = () => this.sonar();
    this.eventos = ['pointerdown', 'pointerup', 'touchstart', 'touchend', 'mousedown', 'mouseup', 'click', 'keydown'];
    this.eventos.forEach((ev) => document.addEventListener(ev, this.gesto, { capture: true, passive: true }));
    setTimeout(() => this.sonar(), 300);
  }
  sonar() {
    const a = this.audioEl;
    // La canción arranca una sola vez: después de empezar, ningún toque la vuelve a iniciar.
    if (!a || this.yaInicio || this.termino || this.pausadaPorUsuario || !a.paused) return;
    try {
      const pr = a.play();
      const ok = () => { this.yaInicio = true; this.setState({ sonando: true }); this.eventos.forEach((ev) => document.removeEventListener(ev, this.gesto, { capture: true })); };
      if (pr && pr.then) pr.then(ok).catch(() => {}); else ok();
    } catch (e) {}
  }
  // El regalo se guarda en la hoja apenas lo marcan (sin esperar la confirmación). Si tocan varios seguidos, se manda una vez.
  guardarRegalo(reservados, catalogo) {
    const inv = this.state.invitado;
    if (!inv) return;
    clearTimeout(this.tRegalo);
    this.tRegalo = setTimeout(() => {
      const regalo = catalogo.filter((r) => reservados[r.id]).map((r) => r.nombre).join(', ');
      fetch(CONFIG.urlRespuestas, { method: 'POST', mode: 'no-cors', headers: { 'Content-Type': 'text/plain;charset=utf-8' },
        body: JSON.stringify({ tipo: 'regalo', id: inv.id, nombre: inv.nombre, regalo: regalo }) }).catch(() => {});
    }, 1200);
  }
  cargarHoja() {
    if (!this.state.qId) { this.setState({ cargado: true }); return; }
    fetch('https://docs.google.com/spreadsheets/d/' + CONFIG.hoja + '/gviz/tq?tqx=out:csv&headers=1&gid=0&_=' + Date.now())
      .then((r) => { if (!r.ok) throw new Error(r.status); return r.text(); })
      .then((t) => {
        const tabla = leerCSV(t);
        const colRegalo = (tabla[0] || []).findIndex((h) => String(h).normalize('NFD').replace(/[̀-ͯ]/g, '').trim().toLowerCase() === 'regalo');
        const fila = tabla.slice(1).find((x) => String(x[0] || '').trim() === String(this.state.qId).trim() && String(x[1] || '').trim());
        if (!fila) { this.setState({ cargado: true, invitado: null }); return; }
        const adicionales = parseInt(fila[2], 10) || 0;
        const total = Math.max(1, parseInt(fila[3], 10) || (1 + adicionales));
        const inv = { id: String(fila[0]).trim(), nombre: String(fila[1]).trim(), total: total, confirmo: String(fila[5] || '').trim() };
        const cambio = { cargado: true, hojaError: false, invitado: inv, cuantos: total, regaloHoja: colRegalo >= 0 ? String(fila[colRegalo] || '') : '' };
        // Si ya respondió antes, muestra su respuesta (y deja modificarla).
        if (/^confirmad/i.test(inv.confirmo)) { const n = parseInt((inv.confirmo.match(/\d+/) || [])[0], 10); Object.assign(cambio, { enviado: true, asiste: 'si', cuantos: n || total }); }
        else if (/^no\b/i.test(inv.confirmo)) Object.assign(cambio, { enviado: true, asiste: 'no' });
        this.setState(cambio);
      })
      .catch(() => this.setState({ cargado: true, hojaError: true }));
  }
  renderVals() {
    const s = this.state;
    const inv = s.invitado;
    const familia = inv ? inv.nombre : '';
    const nombreCorto = familia.split(/\s+/)[0] || '';
    const cupos = inv ? inv.total : 1;
    const varios = cupos > 1;
    const cuantos = Math.min(cupos, Math.max(1, s.cuantos || cupos));
    const casillaBase = 'display: inline-flex; align-items: center; justify-content: center; flex-shrink: 0; width: 26px; height: 26px; border-radius: 13px; font-size: 16px; font-weight: 700; ';
    const invitados = [];
    for (let n = 1; n <= cupos; n++) {
      const on = n === cuantos;
      invitados.push({ nombre: n === 1 ? '1 persona' : n + ' personas', marcado: on ? 'true' : 'false', check: on ? '✓' : '',
        estilo: 'display: flex; align-items: center; gap: 12px; width: 100%; min-height: 52px; padding: 8px 14px; border-radius: 10px; text-align: left; cursor: pointer; font-size: 19px; ' + (on ? 'border: 1px solid #56663D; background: #EEF4E2; color: #2F3A22;' : 'border: 1px solid #C9D9AE; background: #FFFFFF; color: #7A8468;'),
        casilla: casillaBase + (on ? 'background: #56663D; color: #F7F1E3; border: 1px solid #56663D;' : 'background: #FFFFFF; color: transparent; border: 1px solid #A9C084;'),
        toggle: () => this.setState({ cuantos: n, error: false }) });
    }
    const conPortada = s.puerta !== 'abierta';
    const f = new Date(CONFIG.fecha);
    const diff = Math.max(0, f.getTime() - Date.now());
    const pad = (n) => String(n).padStart(2, '0');
    const sep = 'display: flex; flex-direction: column; align-items: center; gap: 6px; padding: 0 clamp(7px, 3vw, 12px); min-width: 0; ';
    const cuenta = [
      [Math.floor(diff / 86400000), 'DÍAS'], [Math.floor(diff / 3600000) % 24, 'HORAS'],
      [Math.floor(diff / 60000) % 60, 'MINUTOS'], [Math.floor(diff / 1000) % 60, 'SEGUNDOS']
    ].map((x, i) => ({ valor: pad(x[0]), etiqueta: x[1], estilo: sep + (i < 3 ? 'border-right: 1px solid #B9CD97;' : '') }));
    const meses = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'];
    const dias = ['Domingo','Lunes','Martes','Miércoles','Jueves','Viernes','Sábado'];
    const h = f.getHours();
    const horaTexto = ((h % 12) || 12) + ':' + pad(f.getMinutes()) + (h < 12 ? ' a. m.' : ' p. m.');
    const fechaLarga = dias[f.getDay()] + ', ' + f.getDate() + ' de ' + meses[f.getMonth()] + ' de ' + f.getFullYear();
    const lim = new Date(f.getTime() - 7 * 86400000);
    const limiteTexto = lim.getDate() + ' de ' + meses[lim.getMonth()];
    const chispas = [];
    for (let i = 0; i < 16; i++) {
      const size = 6 + (i * 7) % 9;
      chispas.push({ style: 'left: ' + ((i * 29 + 11) % 100) + '%; width: ' + size + 'px; height: ' + size + 'px; animation-duration: ' + (7 + (i * 13) % 7) + 's; animation-delay: ' + (-((i * 11) % 9)) + 's; opacity: 0.8' });
    }
    const btnBase = 'min-height: 44px; padding: 0 16px; border-radius: 999px; font-family: Cinzel, serif; font-size: 10px; letter-spacing: 1.5px; cursor: pointer; white-space: nowrap; ';
    const catalogo = [
      { id: 'sobres', nombre: 'Lluvia de sobres', detalle: 'Se recibirán en la recepción' },
      { id: 'joyas', nombre: 'Joyas y accesorios', detalle: 'Aretes, collar, pulsera o reloj' },
      { id: 'perfume', nombre: 'Perfume', detalle: 'Aromas florales o frescos' },
      { id: 'cartera', nombre: 'Cartera o bolso', detalle: 'Elegante, para salir o para el día a día' },
      { id: 'belleza', nombre: 'Set de belleza', detalle: 'Cremas, cuidado de la piel o maquillaje' },
      { id: 'ropa', nombre: 'Prendas finas', detalle: 'Blusas, chalinas o pañuelos de seda' },
      { id: 'spa', nombre: 'Día de spa', detalle: 'Masajes o tratamiento facial' },
      { id: 'experiencia', nombre: 'Una experiencia', detalle: 'Cena especial, paseo o entradas a un espectáculo' },
      { id: 'flores', nombre: 'Flores y plantas', detalle: 'Orquídeas o un arreglo floral' },
      { id: 'cocina', nombre: 'Para la cocina', detalle: 'Cafetera, freidora de aire o licuadora' },
      { id: 'hogar', nombre: 'Tesoros para el hogar', detalle: 'Juego de copas, vajilla o mantelería' }
    ];
    const reservados = s.reservados || Object.fromEntries(catalogo.filter((r) => s.regaloHoja && s.regaloHoja.split(/\s*,\s*/).indexOf(r.nombre) >= 0).map((r) => [r.id, true]));
    const regalos = catalogo.map((r, i) => {
      const on = !!reservados[r.id];
      return Object.assign({}, r, { clase: i % 2 ? 'rev-der' : 'rev-izq', reservado: on ? 'true' : 'false', btnTexto: on ? 'RESERVADO ✓' : 'LO REGALO',
        btnStyle: btnBase + (on ? 'border: 1px solid #56663D; background: #56663D; color: #F7F1E3;' : 'border: 1px solid #A9C084; background: #EEF4E2; color: #3F5226;'),
        pick: () => { const nuevos = Object.assign({}, reservados, { [r.id]: !on }); this.setState({ reservados: nuevos }); this.guardarRegalo(nuevos, catalogo); } });
    });
    const opt = (on) => 'min-height: 50px; border-radius: 10px; font-size: 18px; font-weight: 600; cursor: pointer; ' + (on ? 'border: 1px solid #56663D; background: #56663D; color: #F7F1E3;' : 'border: 1px solid #A9C084; background: #FFFFFF; color: #3F5226;');
    const esSi = s.asiste === 'si';
    const lugar = (n) => n + (n === 1 ? ' lugar' : ' lugares');
    const tocar = () => { this.pausadaPorUsuario = false; this.sonar(); };
    return {
      car: Object.fromEntries(Object.entries({ retrato: 1, fiestas: 2, paseos: 2, familia: 2, hoy: 2 }).map(([n, total]) => {
        const idx = (s.carrusel && s.carrusel[n]) || 0;
        const pon = (i) => this.setState({ carrusel: Object.assign({}, this.state.carrusel || {}, { [n]: i }) });
        return [n, {
          puntos: Array.from({ length: total }, (_, i) => ({ estilo: 'display: block; width: ' + (i === idx ? '16px' : '7px') + '; height: 7px; border-radius: 4px; background: ' + (i === idx ? '#FFFFFF' : 'rgba(255,255,255,0.6)') + '; box-shadow: 0 1px 3px rgba(0,0,0,0.45); transition: width .25s' })),
          ref: (this.refsCar = this.refsCar || {})[n] || (this.refsCar[n] = (el) => { this.carEls[n] = el; }),
          tocado: () => { this.carTocado[n] = Date.now(); },
          onScroll: (e) => { const el = e.currentTarget; const i = Math.round(el.scrollLeft / Math.max(1, el.clientWidth)); if (i !== idx) pon(i); },
          siguiente: (e) => { this.carTocado[n] = Date.now(); const el = e.currentTarget; const i = (Math.round(el.scrollLeft / Math.max(1, el.clientWidth)) + 1) % total; el.scrollTo({ left: i * el.clientWidth, behavior: 'smooth' }); }
        }];
      })),
      pedirFamilia: false, familiaLista: !!inv, mostrarBanner: true,
      bannerTexto: inv ? 'Para ' + familia : 'Bienvenidos al baile real',
      tituloTarjeta: inv ? 'INVITACIÓN ESPECIAL PARA' : 'INVITACIÓN PERSONAL',
      familia, nombreCorto, cupos, cuposTexto: lugar(cupos), invitados, hayLista: varios,
      avisoLista: !s.qId ? 'Para confirmar, abre el enlace personal que te enviamos por WhatsApp.'
        : !s.cargado ? 'Cargando tu invitación…'
        : s.hojaError ? 'No pudimos cargar tu invitación. Vuelve a intentarlo en un momento.'
        : 'No encontramos tu invitación. Revisa el enlace que te enviamos o escríbenos por WhatsApp.',
      preguntaAsiste: varios ? '¿ASISTIRÁN AL BAILE?' : '¿ASISTIRÁS AL BAILE?',
      textoSi: varios ? 'Sí, asistiremos' : 'Sí, asistiré', textoNo: varios ? 'No podremos ir' : 'No podré ir',
      errorTexto: 'No pudimos enviar tu respuesta. Inténtalo de nuevo.', horaTexto, fechaLarga, limiteTexto, cuenta, chispas, regalos,
      mostrarPortada: conPortada, portadaAbierta: !conPortada,
      claseTexto: s.puerta === 'cerrada' ? 'oculto' : 'anima',
      baseAnim: '3.7s',
      claseCarta: s.puerta === 'cerrada' ? 'carta-espera' : 'carta-entra',
      clasePortada: s.puerta === 'abriendo' ? 'abriendo' : '',
      rootExtra: conPortada ? 'height: min(100vh, 880px); overflow: hidden;' : '',
      claseSobre: s.sobre ? 'sb-abre' : 'sb-espera',
      ver: this.refVer || (this.refVer = (el) => {
        if (!el) return;
        if (typeof IntersectionObserver === 'undefined') { el.classList.add('visto'); return; }
        if (!this.io2) this.io2 = new IntersectionObserver((es) => es.forEach((x) => { if (x.isIntersecting) { x.target.classList.add('visto'); this.io2.unobserve(x.target); } }), { threshold: 0.35 });
        this.io2.observe(el);
      }),
      setSobre: this.refSobre || (this.refSobre = (el) => {
        if (!el || this.io) return;
        if (typeof IntersectionObserver === 'undefined') { this.setState({ sobre: true }); return; }
        this.io = new IntersectionObserver((es) => { if (es.some((x) => x.isIntersecting)) { this.io.disconnect(); this.setState({ sobre: true }); } }, { threshold: 0.6 });
        this.io.observe(el);
      }),
      abrir: () => {
        if (s.puerta !== 'cerrada') return;
        this.setState({ puerta: 'abriendo' });
        tocar();
        this.tp = setTimeout(() => { this.setState({ puerta: 'abierta' }); try { window.scrollTo(0, 0); } catch (e) {} }, 5300);
      },
      noLlega: diff > 0, yaLlego: diff === 0,
      cronograma: [
        { hora: '7:00 P. M.', titulo: 'Bienvenida', detalle: 'Saludo a familiares e invitados' },
        { hora: '8:00 P. M.', titulo: 'Entrada de la reina', detalle: 'Ingreso de la homenajeada y presentación de su corte familiar' },
        { hora: '8:30 P. M.', titulo: 'Palabras de honor', detalle: 'Mensajes de su familia y de la cumpleañera' },
        { hora: '9:00 P. M.', titulo: 'Brindis de honor', detalle: 'Alzamos las copas por sus 50 años' },
        { hora: '9:15 P. M.', titulo: 'Vals de aniversario', detalle: 'Con su familia y todos sus invitados' },
        { hora: '9:45 P. M.', titulo: '¡Rompe la piñata!', detalle: 'Y saludos y felicitaciones a la cumpleañera' },
        { hora: '10:15 P. M.', titulo: 'Cena', detalle: 'Servida en el gran salón' },
        { hora: '11:00 P. M.', titulo: 'Baile general', detalle: '¡A bailar hasta el último hechizo!' }
      ],
      esSi: esSi, esNo: !esSi, siStyle: opt(esSi), noStyle: opt(!esSi),
      elegirSi: () => this.setState({ asiste: 'si' }),
      elegirNo: () => this.setState({ asiste: 'no' }),
      error: s.error, enviando: !!s.enviando, textoEnviar: s.enviando ? 'ENVIANDO…' : 'ENVIAR RESPUESTA',
      enviar: (e) => {
        e.preventDefault();
        if (!inv || s.enviando) return;
                const datos = { id: inv.id, nombre: inv.nombre, asiste: esSi, personas: esSi ? cuantos : 0, total: cupos };
        this.setState({ enviando: true, error: false });
        fetch(CONFIG.urlRespuestas, { method: 'POST', mode: 'no-cors', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify(datos) })
          .then(() => this.setState({ enviando: false, enviado: true, error: false }))
          .catch(() => this.setState({ enviando: false, error: true }));
      },
      editar: () => this.setState({ enviado: false }),
      enviado: s.enviado, noEnviado: !s.enviado,
      gracias: esSi
        ? (cuantos > 1 ? 'Reservamos ' + cuantos + ' lugares para ustedes. ¡Los esperamos en el palacio!' : '¡Te esperamos en el palacio!')
        : 'Lamentamos que no puedas acompañarnos. ¡Gracias por avisar!',
      tieneMusica: !s.termino,
      musicaLabel: s.sonando ? 'Pausar música' : 'Reproducir música',
      alternarMusica: () => { const a = this.audioEl; if (!a) return; if (!a.paused) { a.pause(); this.pausadaPorUsuario = true; } else if (!this.termino) { this.pausadaPorUsuario = false; a.play().catch(() => {}); } }
    };
  }
}

// Apariciones: cada bloque con .revela / .rev-* aparece al entrar en pantalla (funciona en todos los celulares).
(function () {
  var SEL = '.revela,.rev-izq,.rev-der,.rev-zoom,.rev-fade';
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) {
    es.forEach(function (x) {
      if (!x.isIntersecting) return;
      var el = x.target;
      // las tarjetas de una lista aparecen una tras otra
      var hermanos = el.parentNode ? Array.prototype.filter.call(el.parentNode.children, function (h) { return h.matches(SEL); }) : [];
      var i = hermanos.indexOf(el);
      el.style.transitionDelay = (i > 0 ? Math.min(i % 4, 3) * 0.08 : 0) + 's';
      el.classList.add('vis');
      io.unobserve(el);
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' }) : null;
  function busca() {
    document.querySelectorAll(SEL).forEach(function (el) {
      if (el.__rev) return;
      el.__rev = true;
      if (io) io.observe(el); else el.classList.add('vis');
    });
  }
  var pendiente = false;
  new MutationObserver(function () {
    if (pendiente) return;
    pendiente = true;
    requestAnimationFrame(function () { pendiente = false; busca(); });
  }).observe(document.getElementById('app'), { childList: true, subtree: true });
  window.addEventListener('load', busca);
})();

// La portada está dibujada a 420 × 800: se achica para que entre completa en el ancho y el alto del celular.
(function () {
  var ancho = 0;
  function ajusta() {
    if (window.innerWidth === ancho) return; // al esconderse la barra del navegador solo cambia el alto: no mover nada
    ancho = window.innerWidth;
    var w = Math.min(ancho, 480), h = window.innerHeight - 56;
    var k = Math.min(1, w / 420, Math.max(h / 800, (w / 420) * 0.8));
    document.documentElement.style.setProperty('--k', k.toFixed(4));
  }
  ajusta();
  window.addEventListener('resize', ajusta);
  window.addEventListener('orientationchange', function () { ancho = 0; setTimeout(ajusta, 300); });
})();

window.invitacion = montarDC(Component, {}, document.getElementById('dc'), document.getElementById('app'));
