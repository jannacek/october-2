/* ═══════════════════════════════════════════════════════════════════════════
   ANIMATIONS — scroll reveals and lab-specific effects
   Progressive enhancement: the page is fully readable without this file.
   Agustín Martínez Caram PD Portfolio · v4 · October 2026
   ═══════════════════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var canObserve = 'IntersectionObserver' in window;

  function revealAll() {
    document.querySelectorAll('.reveal, .reveal-stagger, .feed-forward, .draw-underline, [data-lab="4"] .act-item')
      .forEach(function (el) { el.classList.add('visible'); });
  }

  function observe(selector, options) {
    var els = document.querySelectorAll(selector);
    if (!els.length) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          io.unobserve(entry.target);
        }
      });
    }, options);
    els.forEach(function (el) {
      // anything already on screen is shown at once — no flash of hidden content
      var r = el.getBoundingClientRect();
      if (r.top < window.innerHeight * 0.98 && r.bottom > 0) {
        el.classList.add('visible');
      } else {
        io.observe(el);
      }
    });
  }

  // Failsafe: the head script hides reveal-on-scroll content (class "js") and starts a
  // timer that removes the class again. This function runs only if this file loaded and
  // started; it cancels that timer. If anything below throws, everything is shown at once.
  function init() {
    try {
      run();
    } catch (e) {
      document.documentElement.classList.remove('js');
      revealAll();
    }
  }

  function run() {
    if (window.__revealGuard) clearTimeout(window.__revealGuard);
    if (!document.documentElement.classList.contains('js')) { revealAll(); return; }
    if (reduce || !canObserve) {
      revealAll();
    } else {
      observe('.reveal', { threshold: 0.06, rootMargin: '0px 0px -40px 0px' });
      observe('.reveal-stagger', { threshold: 0.06, rootMargin: '0px 0px -40px 0px' });
      observe('.feed-forward', { threshold: 0.4 });
      observe('.draw-underline', { threshold: 0.5 });
      observe('[data-lab="4"] .act-item', { threshold: 0.15, rootMargin: '0px 0px -20px 0px' });

      // safety net: if anything is still hidden after 4 s (e.g. print preview), show it
      setTimeout(function () {
        document.querySelectorAll('.js .reveal:not(.visible), .js .reveal-stagger:not(.visible)')
          .forEach(function (el) {
            var r = el.getBoundingClientRect();
            if (r.top < window.innerHeight * 1.5) el.classList.add('visible');
          });
      }, 4000);
    }

    // Boundary-concept sequence pulse
    var bc = document.querySelector('.bc-sequence');
    if (bc && !reduce) setTimeout(function () { bc.classList.add('animating'); }, 800);
  }

  window.addEventListener('beforeprint', revealAll);

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
