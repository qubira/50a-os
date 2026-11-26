// Motor mínimo para mostrar el diseño (.dc.html) fuera de Claude Design.
// Entiende {{expresiones}} en textos y atributos, <sc-if value> y <sc-for list as>,
// eventos onX="{{fn}}", ref="{{fn}}" y una clase con state / setState / renderVals.
(function () {
  var cache = new Map();
  function evalua(expr, scope) {
    var f = cache.get(expr);
    if (!f) {
      try { f = new Function('$s', 'with ($s) { return (' + expr + '); }'); } catch (e) { f = function () {}; }
      cache.set(expr, f);
    }
    try { return f(scope); } catch (e) { return undefined; }
  }
  var HUECO = /\{\{([\s\S]+?)\}\}/g;
  function soloHueco(txt) { var m = txt.match(/^\s*\{\{([\s\S]+?)\}\}\s*$/); return m ? m[1] : null; }
  function interpola(txt, scope) {
    return txt.replace(HUECO, function (_, e) { var v = evalua(e, scope); return v == null || v === false ? '' : String(v); });
  }

  // Convierte los hijos de un <sc-if>/<sc-for> en un fragmento plantilla reutilizable.
  function plantilla(el) {
    var frag = document.createDocumentFragment();
    while (el.firstChild) frag.appendChild(el.firstChild);
    return frag;
  }

  function compila(raiz, enlaces) {
    var hijos = Array.prototype.slice.call(raiz.childNodes);
    hijos.forEach(function (n) {
      if (n.nodeType === 3) {
        if (n.data.indexOf('{{') >= 0) enlaces.push(enlaceTexto(n));
        return;
      }
      if (n.nodeType !== 1) return;
      var tag = n.localName;
      if (tag === 'sc-if' || tag === 'sc-for') {
        var ancla = document.createComment(tag);
        n.parentNode.replaceChild(ancla, n);
        var expr = soloHueco(n.getAttribute(tag === 'sc-if' ? 'value' : 'list') || '') || 'false';
        var tpl = plantilla(n);
        enlaces.push(tag === 'sc-if' ? enlaceSi(ancla, expr, tpl) : enlacePara(ancla, expr, n.getAttribute('as') || 'item', tpl));
        return;
      }
      Array.prototype.slice.call(n.attributes).forEach(function (a) {
        if (a.name.indexOf('hint-placeholder') === 0) { n.removeAttribute(a.name); return; }
        if (a.value.indexOf('{{') < 0) return;
        n.removeAttribute(a.name);
        enlaces.push(enlaceAtributo(n, a.name, a.value));
      });
      compila(n, enlaces);
    });
  }

  function enlaceTexto(nodo) {
    var txt = nodo.data, ultimo;
    return function (scope) { var v = interpola(txt, scope); if (v !== ultimo) { nodo.data = v; ultimo = v; } };
  }

  function enlaceAtributo(el, nombre, txt) {
    var expr = soloHueco(txt), ultimo = {};
    if (nombre.indexOf('on') === 0 && expr) {
      var tipo = nombre.slice(2), clave = '__dc_' + tipo;
      el.addEventListener(tipo, function (e) { var h = el[clave]; if (typeof h === 'function') h(e); }, tipo === 'touchstart' || tipo === 'scroll' ? { passive: true } : false);
      return function (scope) { el[clave] = evalua(expr, scope); };
    }
    if (nombre === 'ref' && expr) {
      return function (scope) { var f = evalua(expr, scope); if (f !== ultimo) { ultimo = f; if (typeof f === 'function') f(el); } };
    }
    return function (scope) {
      var v = expr ? evalua(expr, scope) : interpola(txt, scope);
      if (v === ultimo) return;
      ultimo = v;
      if (nombre === 'value' && 'value' in el) { el.value = v == null ? '' : v; return; }
      if (v == null || (v === false && nombre.indexOf('aria-') !== 0)) el.removeAttribute(nombre);
      else el.setAttribute(nombre, String(v));
    };
  }

  function Bloque(tpl, ancla) {
    var frag = tpl.cloneNode(true);
    this.enlaces = [];
    compila(frag, this.enlaces);
    this.nodos = Array.prototype.slice.call(frag.childNodes);
    ancla.parentNode.insertBefore(frag, ancla);
  }
  Bloque.prototype.actualiza = function (scope) { for (var i = 0; i < this.enlaces.length; i++) this.enlaces[i](scope); };
  Bloque.prototype.quita = function () { this.nodos.forEach(function (n) { if (n.parentNode) n.parentNode.removeChild(n); }); };

  function enlaceSi(ancla, expr, tpl) {
    var bloque = null;
    return function (scope) {
      var v = !!evalua(expr, scope);
      if (v && !bloque) bloque = new Bloque(tpl, ancla);
      if (!v && bloque) { bloque.quita(); bloque = null; }
      if (bloque) bloque.actualiza(scope);
    };
  }

  function enlacePara(ancla, expr, como, tpl) {
    var bloques = [];
    return function (scope) {
      var lista = evalua(expr, scope) || [];
      while (bloques.length > lista.length) bloques.pop().quita();
      for (var i = 0; i < lista.length; i++) {
        if (!bloques[i]) bloques[i] = new Bloque(tpl, ancla);
        var sub = Object.create(scope);
        sub[como] = lista[i];
        sub.$index = i;
        bloques[i].actualiza(sub);
      }
    };
  }

  function DCLogic(props) { this.props = props || {}; this.state = {}; }
  DCLogic.prototype.setState = function (p) {
    var n = typeof p === 'function' ? p(this.state, this.props) : p;
    this.state = Object.assign({}, this.state, n);
    this.forceUpdate();
  };
  DCLogic.prototype.forceUpdate = function () {
    var self = this;
    if (self.__pendiente) return;
    self.__pendiente = true;
    Promise.resolve().then(function () { self.__pendiente = false; self.__pinta(); });
  };
  window.DCLogic = DCLogic;

  window.montarDC = function (Componente, props, plantillaEl, destino) {
    var comp = new Componente(props);
    var tpl = plantillaEl.content;
    var ancla = document.createComment('dc');
    destino.appendChild(ancla);
    var bloque = new Bloque(tpl, ancla);
    comp.__pinta = function () { bloque.actualiza(comp.renderVals()); };
    comp.__pinta();
    if (comp.componentDidMount) comp.componentDidMount();
    return comp;
  };
})();
