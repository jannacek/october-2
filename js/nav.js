/* ═══════════════════════════════════════════════════════════════════════════
   NAV — current page, mobile menu (accessible), in-page contents spy
   Agustín Martínez Caram PD Portfolio · v4 · October 2026
   ═══════════════════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  /* 1. CURRENT PAGE ─────────────────────────────────────────────────────── */

  function initializeActiveLink() {
    var file = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
    if (file === '') file = 'index.html';
    document.querySelectorAll('#sidebar .nav-link').forEach(function (link) {
      var href = (link.getAttribute('href') || '').split('#')[0].split('/').pop().toLowerCase();
      if (href === file) {
        link.classList.add('active');
        link.setAttribute('aria-current', 'page');
      }
    });
    // keep the current link in view inside the scrolling sidebar
    var cur = document.querySelector('#sidebar .nav-link[aria-current="page"]');
    if (cur && cur.scrollIntoView && window.innerWidth > 900) {
      var sb = document.getElementById('sidebar');
      if (sb && cur.offsetTop > sb.clientHeight - 120) {
        sb.scrollTop = cur.offsetTop - sb.clientHeight / 2;
      }
    }
  }

  /* 2. MOBILE MENU ──────────────────────────────────────────────────────── */

  function initializeHamburger() {
    var hamburger = document.querySelector('.hamburger');
    var sidebar = document.getElementById('sidebar');
    var overlay = document.querySelector('.sidebar-overlay');
    if (!hamburger || !sidebar) return;

    hamburger.setAttribute('aria-controls', 'sidebar');
    hamburger.setAttribute('aria-expanded', 'false');

    function setOpen(open) {
      sidebar.classList.toggle('open', open);
      hamburger.classList.toggle('open', open);
      hamburger.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (overlay) overlay.classList.toggle('open', open);
      if (open) {
        var first = sidebar.querySelector('.nav-link');
        if (first && window.innerWidth <= 900) first.focus({ preventScroll: true });
      }
    }

    hamburger.addEventListener('click', function () {
      setOpen(!sidebar.classList.contains('open'));
    });

    if (overlay) overlay.addEventListener('click', function () { setOpen(false); });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && sidebar.classList.contains('open')) {
        setOpen(false);
        hamburger.focus();
      }
    });

    sidebar.querySelectorAll('.nav-link').forEach(function (link) {
      link.addEventListener('click', function () {
        if (window.innerWidth <= 900) setOpen(false);
      });
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth > 900 && sidebar.classList.contains('open')) setOpen(false);
    });
  }

  /* 3. IN-PAGE CONTENTS (.toc) SCROLL SPY ───────────────────────────────── */

  function initializeScrollSpy() {
    var links = Array.prototype.slice.call(document.querySelectorAll('.toc a[href^="#"]'));
    if (!links.length || !('IntersectionObserver' in window)) return;

    var map = {};
    links.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        links.forEach(function (a) { a.removeAttribute('aria-current'); });
        var a = map[entry.target.id];
        if (a) a.setAttribute('aria-current', 'true');
      });
    }, { rootMargin: '-25% 0px -65% 0px', threshold: 0 });

    Object.keys(map).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) io.observe(el);
    });
  }

  function init() {
    initializeActiveLink();
    initializeHamburger();
    initializeScrollSpy();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
