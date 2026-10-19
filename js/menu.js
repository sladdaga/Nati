// Menú principal: abierto en escritorio, desplegable en tablet y móvil.
(function () {
  var header = document.querySelector('.site-header');
  var menu = document.querySelector('.menu');
  if (!menu) return;
  var compact = window.matchMedia('(max-width: 960px)');

  function sync() {
    menu.open = !compact.matches;
  }

  sync();
  if (compact.addEventListener) compact.addEventListener('change', sync);
  else compact.addListener(sync);

  function close() {
    if (compact.matches) menu.open = false;
  }

  // Cerrar el menú después de elegir una sección, al tocar fuera o con Escape.
  menu.querySelectorAll('nav a').forEach(function (link) {
    link.addEventListener('click', close);
  });
  document.addEventListener('click', function (event) {
    if (!menu.contains(event.target)) close();
  });
  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' && compact.matches && menu.open) {
      close();
      menu.querySelector('summary').focus();
    }
  });

  // Sombra del encabezado al desplazarse.
  if (header) {
    var onScroll = function () {
      header.classList.toggle('is-scrolled', window.scrollY > 8);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }
})();
