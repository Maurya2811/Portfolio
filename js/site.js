/*!
 * Rahul Maurya — Portfolio content hydrator (Phase 1)
 *
 * Philosophy: the HTML ships with authoritative fallback text so the site
 * works without JS, with a broken fetch, or for no-JS crawlers. When this
 * script loads successfully, it OVERRIDES the bound fields from data/site.json.
 *
 * Binding syntax:
 *   <span data-bind="owner.phone">+91 79054 96720</span>
 *     → element.textContent = data.owner.phone (only if resolved)
 *
 *   <a data-bind-href="owner.phoneTel" href="tel:+917905496720">...</a>
 *     → element.setAttribute('href', data.owner.phoneTel)
 *
 * Missing paths are silently ignored (fallback remains).
 */
(function () {
  function getPath(obj, path) {
    if (!obj || !path) return undefined;
    return path.split('.').reduce(function (acc, key) {
      return (acc == null) ? acc : acc[key];
    }, obj);
  }

  function hydrate(data) {
    // text content
    document.querySelectorAll('[data-bind]').forEach(function (el) {
      var v = getPath(data, el.getAttribute('data-bind'));
      if (v != null && v !== '') el.textContent = v;
    });
    // href attribute (most common)
    document.querySelectorAll('[data-bind-href]').forEach(function (el) {
      var v = getPath(data, el.getAttribute('data-bind-href'));
      if (v != null && v !== '') el.setAttribute('href', v);
    });
    // generic attribute: data-bind-attr-<name>="path"
    document.querySelectorAll('*').forEach(function (el) {
      if (!el.attributes) return;
      for (var i = 0; i < el.attributes.length; i++) {
        var a = el.attributes[i];
        if (a.name.indexOf('data-bind-attr-') === 0) {
          var attrName = a.name.replace('data-bind-attr-', '');
          var v = getPath(data, a.value);
          if (v != null && v !== '') el.setAttribute(attrName, v);
        }
      }
    });
  }

  // Resolve the data file relative to this script's location so the same
  // script works from index.html, projects/*.html, resume/index.html, etc.
  function resolveDataUrl() {
    var s = document.querySelector('script[src$="js/site.js"], script[src*="js/site.js?"]');
    if (!s) return 'data/site.json';
    // script src → .../js/site.js → swap to .../data/site.json
    return s.src.replace(/js\/site\.js(\?.*)?$/, 'data/site.json');
  }

  function run() {
    try {
      fetch(resolveDataUrl(), { cache: 'no-cache' })
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (d) { if (d) hydrate(d); })
        .catch(function () { /* fallback: HTML text stays */ });
    } catch (e) { /* noop */ }
  }

  if (document.readyState !== 'loading') run();
  else document.addEventListener('DOMContentLoaded', run);
})();
