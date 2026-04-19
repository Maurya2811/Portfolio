/*!
 * Rahul Maurya — Portfolio theme controller
 * - Dark is the default; user choice persisted to localStorage.
 * - Injects a toggle button into the nav on every page.
 * - Re-renders Mermaid diagrams with a matching theme when toggled.
 */
(function () {
  var KEY = 'rm-theme';
  var root = document.documentElement;
  var stored = null;
  try { stored = localStorage.getItem(KEY); } catch (e) { /* privacy mode */ }
  var initial = stored === 'dark' || stored === 'light' ? stored : 'dark';
  root.setAttribute('data-theme', initial);

  var SUN_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg>';
  var MOON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3a7 7 0 0 0 9.79 9.79z"/></svg>';

  var btn;

  function mermaidVars(theme) {
    if (theme === 'dark') {
      return {
        theme: 'dark',
        themeVariables: {
          background: '#0a0f24',
          primaryColor: '#17204a',
          primaryTextColor: '#e6ecff',
          primaryBorderColor: '#7cf5c2',
          lineColor: '#7cf5c2',
          secondaryColor: '#111735',
          tertiaryColor: '#0f1530',
          fontFamily: 'Inter, sans-serif'
        }
      };
    }
    return {
      theme: 'base',
      themeVariables: {
        background: '#ffffff',
        primaryColor: '#ffffff',
        primaryTextColor: '#0b1020',
        primaryBorderColor: '#0ea371',
        lineColor: '#0ea371',
        secondaryColor: '#f6f8fc',
        tertiaryColor: '#eef2fb',
        fontFamily: 'Inter, sans-serif'
      }
    };
  }

  function renderMermaid() {
    if (!window.mermaid) return;
    var els = document.querySelectorAll('.mermaid, pre.mermaid');
    if (!els.length) return;
    els.forEach(function (el) {
      if (!el.dataset.mermaidSrc) el.dataset.mermaidSrc = el.textContent.trim();
      el.removeAttribute('data-processed');
      el.innerHTML = el.dataset.mermaidSrc;
    });
    var cfg = mermaidVars(root.getAttribute('data-theme'));
    try {
      window.mermaid.initialize(Object.assign({ startOnLoad: false, securityLevel: 'loose' }, cfg));
      if (typeof window.mermaid.run === 'function') {
        window.mermaid.run({ querySelector: '.mermaid, pre.mermaid' });
      } else if (typeof window.mermaid.init === 'function') {
        window.mermaid.init(undefined, els);
      }
    } catch (e) { /* noop */ }
  }

  function updateBtn() {
    if (!btn) return;
    var isDark = root.getAttribute('data-theme') === 'dark';
    btn.innerHTML = isDark ? SUN_SVG : MOON_SVG;
    btn.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
    btn.setAttribute('title', isDark ? 'Switch to light mode' : 'Switch to dark mode');
    btn.setAttribute('aria-pressed', String(isDark));
  }

  function setTheme(t) {
    root.setAttribute('data-theme', t);
    try { localStorage.setItem(KEY, t); } catch (e) { /* noop */ }
    updateBtn();
    renderMermaid();
  }

  function toggle() {
    setTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
  }

  function injectBtn() {
    var nav = document.querySelector('header.nav');
    if (!nav) return;
    btn = document.createElement('button');
    btn.className = 'theme-toggle';
    btn.type = 'button';
    btn.addEventListener('click', toggle);
    var cta = nav.querySelector('.nav-cta');
    if (cta) nav.insertBefore(btn, cta); else nav.appendChild(btn);
    updateBtn();
  }

  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  ready(function () {
    injectBtn();
    // Mermaid may load after DOMContentLoaded (defer/async on CDN); try now and retry briefly.
    renderMermaid();
    var tries = 0;
    var iv = setInterval(function () {
      if (window.mermaid || tries > 10) { clearInterval(iv); renderMermaid(); }
      tries++;
    }, 150);
  });
})();
