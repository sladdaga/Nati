// Contador de visitas (Abacus). Suma una sola vez por navegador (marca guardada en localStorage).
(function () {
  var el = document.getElementById('visit-counter');
  if (!el) return;
  var base = 'https://abacus.jasoncameron.dev/';
  var clave = 'natiallestero-web/total';
  var yaContada = false;
  try { yaContada = localStorage.getItem('visita-contada') === '1'; } catch (e) {}
  fetch(base + (yaContada ? 'get/' : 'hit/') + clave)
    .then(function (r) { return r.json(); })
    .then(function (d) {
      if (typeof d.value !== 'number') return;
      var it = document.documentElement.lang === 'it';
      el.textContent = (el.dataset.label || 'Visitas: ') + d.value.toLocaleString(it ? 'it-IT' : 'es-AR');
      try { localStorage.setItem('visita-contada', '1'); } catch (e) {}
    })
    .catch(function () {});
})();
