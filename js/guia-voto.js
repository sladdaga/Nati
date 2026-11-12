(function () {
  'use strict';
  var g = document.getElementById('guia-voto');
  if (!g) return;
  g.classList.add('is-js');

  var $ = function (s, r) { return (r || g).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || g).querySelectorAll(s)); };

  var nodes = $$('.guide-node');
  var panels = $$('.guide-panel');
  var visuals = $$('.guide-visual');
  var prev = $('.guide-prev');
  var next = $('.guide-next');
  var progress = $('.guide-progress');
  var last = panels.length - 1;
  var cur = 0;

  function show(i) {
    cur = Math.max(0, Math.min(last, i));
    panels.forEach(function (p, k) { p.hidden = k !== cur; });
    nodes.forEach(function (n, k) {
      n.classList.toggle('is-current', k === cur);
      n.classList.toggle('is-done', k < cur);
      if (k === cur) n.setAttribute('aria-current', 'step'); else n.removeAttribute('aria-current');
    });
    var view = panels[cur].getAttribute('data-view');
    visuals.forEach(function (v) { v.hidden = v.getAttribute('data-for') !== view; });
    g.setAttribute('data-focus', panels[cur].getAttribute('data-focus') || '');
    prev.disabled = cur === 0;
    next.disabled = cur === last;
    progress.textContent = g.getAttribute('data-lbl-step') + ' ' + (cur + 1) + ' / ' + (last + 1);
  }

  nodes.forEach(function (n) {
    n.addEventListener('click', function () { show(parseInt(n.getAttribute('data-go'), 10)); });
  });
  prev.addEventListener('click', function () { show(cur - 1); });
  next.addEventListener('click', function () { show(cur + 1); });

  /* Boleta de práctica */
  var logo = $('.ballot-logo');
  var cands = $$('.cand');
  var msg = $('.ballot-msg');
  var MAX = 4;

  logo.addEventListener('click', function () {
    var on = logo.getAttribute('aria-pressed') !== 'true';
    logo.setAttribute('aria-pressed', String(on));
    msg.textContent = '';
  });
  cands.forEach(function (c) {
    c.addEventListener('click', function () {
      var on = c.getAttribute('aria-pressed') === 'true';
      if (!on) {
        var count = cands.filter(function (x) { return x.getAttribute('aria-pressed') === 'true'; }).length;
        if (count >= MAX) {
          msg.textContent = g.getAttribute('data-max-msg');
          return;
        }
      }
      c.setAttribute('aria-pressed', String(!on));
      msg.textContent = '';
    });
  });
  $('.guide-reset').addEventListener('click', function () {
    logo.setAttribute('aria-pressed', 'false');
    cands.forEach(function (c) { c.setAttribute('aria-pressed', 'false'); });
    msg.textContent = '';
  });

  /* Checklist */
  var checks = $$('.guide-check');
  var ok = $('.guide-ok');
  checks.forEach(function (c) {
    c.addEventListener('change', function () {
      var all = checks.every(function (x) { return x.checked; });
      ok.textContent = all ? g.getAttribute('data-checks-ok') : '';
    });
  });

  /* Sobres */
  var env = $('.env');
  var caps = g.getAttribute('data-captions').split('|');
  var cap = $('.env-caption');
  var btn = $('.env-btn');
  function setStage(s) {
    env.setAttribute('data-stage', String(s));
    cap.textContent = caps[s] || '';
    btn.disabled = s >= caps.length - 1;
  }
  btn.addEventListener('click', function () {
    setStage(Math.min(caps.length - 1, parseInt(env.getAttribute('data-stage'), 10) + 1));
  });
  setStage(0);

  show(0);
})();
