// Ventana emergente de las elecciones COM.It.Es. 2026: una vez por sesión.
(function () {
  var dialog = document.getElementById('promo-elecciones');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  var KEY = 'promoEleccionesVista';

  try {
    if (sessionStorage.getItem(KEY)) return;
  } catch (e) {}

  dialog.querySelectorAll('[data-promo-close]').forEach(function (btn) {
    btn.addEventListener('click', function () { dialog.close(); });
  });
  // Cerrar al tocar fuera del cuadro.
  dialog.addEventListener('click', function (event) {
    if (event.target === dialog) dialog.close();
  });
  dialog.addEventListener('close', function () {
    try { sessionStorage.setItem(KEY, '1'); } catch (e) {}
  });

  setTimeout(function () { dialog.showModal(); }, 1500);
})();
