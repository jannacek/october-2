/* ═══════════════════════════════════════════════════════════════════════════
   EVIDENCE — upgrades "on request" rows to live links when the file is published
   Each row: <li data-file="evidence/xyz.pdf"> … <span class="ev-state">On request</span>
   If the file exists next to the site, the row becomes a link; otherwise it stays as is.
   ═══════════════════════════════════════════════════════════════════════════ */

(function () {
  'use strict';
  if (!('fetch' in window) || location.protocol === 'file:') return;

  document.querySelectorAll('[data-file]').forEach(function (row) {
    var file = row.getAttribute('data-file');
    fetch(file, { method: 'HEAD' }).then(function (res) {
      if (!res.ok) return;
      var state = row.querySelector('.ev-state');
      if (!state) return;
      var a = document.createElement('a');
      a.href = file;
      a.target = '_blank';
      a.rel = 'noopener';
      a.textContent = 'Open file ↗';
      state.replaceWith(a);
    }).catch(function () { /* stay "on request" */ });
  });
})();
