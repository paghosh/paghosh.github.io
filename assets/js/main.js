(function () {
  'use strict';

  // Theme toggle
  var root = document.documentElement;
  var toggle = document.querySelector('.theme-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) {}
    });
  }

  // Mobile nav
  var navBtn = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  function setNav(open) {
    if (!nav || !navBtn) return;
    nav.classList.toggle('open', open);
    navBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    navBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  if (navBtn && nav) {
    navBtn.addEventListener('click', function () { setNav(!nav.classList.contains('open')); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setNav(false); });
    document.addEventListener('click', function (e) { if (!e.target.closest('.site-header')) setNav(false); });
  }

  // Toast
  var toast = document.createElement('div');
  toast.className = 'toast';
  toast.setAttribute('role', 'status');
  document.body.appendChild(toast);
  function showToast(msg) {
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(showToast.t);
    showToast.t = setTimeout(function () { toast.classList.remove('show'); }, 1800);
  }

  // Abstract and BibTeX panels
  document.querySelectorAll('[data-panel-toggle]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var id = btn.getAttribute('data-panel-toggle');
      var panel = document.getElementById(id);
      if (!panel) return;
      var paper = btn.closest('.paper');
      var willOpen = !panel.classList.contains('open');
      if (paper) {
        paper.querySelectorAll('.paper-panel.open').forEach(function (p) { p.classList.remove('open'); });
        paper.querySelectorAll('[data-panel-toggle]').forEach(function (b) { b.setAttribute('aria-expanded', 'false'); });
      }
      if (willOpen) {
        panel.classList.add('open');
        btn.setAttribute('aria-expanded', 'true');
      }
    });
  });

  // Copy to clipboard: data-copy (element id) or data-copy-text (literal)
  function copyText(text, label) {
    var done = function () { showToast(label + ' copied'); };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, function () { fallbackCopy(text, done); });
    } else { fallbackCopy(text, done); }
  }
  function fallbackCopy(text, done) {
    var ta = document.createElement('textarea');
    ta.value = text; ta.setAttribute('readonly', ''); ta.style.position = 'absolute'; ta.style.left = '-9999px';
    document.body.appendChild(ta); ta.select();
    try { document.execCommand('copy'); done(); } catch (e) { showToast('Select the text and copy it'); }
    document.body.removeChild(ta);
  }
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var src = document.getElementById(btn.getAttribute('data-copy'));
      if (src) copyText(src.textContent, btn.getAttribute('data-copy-label') || 'BibTeX');
    });
  });
  document.querySelectorAll('[data-copy-text]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      copyText(btn.getAttribute('data-copy-text'), btn.getAttribute('data-copy-label') || 'Text');
    });
  });

  // Research filters and search
  var filterBar = document.querySelector('.filters');
  if (filterBar) {
    var papers = Array.prototype.slice.call(document.querySelectorAll('.paper[data-area]'));
    var sections = Array.prototype.slice.call(document.querySelectorAll('.research-section'));
    var areaChips = filterBar.querySelectorAll('.chip[data-area]');
    var searchBox = filterBar.querySelector('.search-box');
    var countEl = filterBar.querySelector('.filter-count');
    var empty = document.querySelector('.no-match');
    var area = 'all';

    function apply() {
      var q = (searchBox ? searchBox.value : '').trim().toLowerCase();
      var shown = 0;
      papers.forEach(function (p) {
        var okArea = area === 'all' || p.getAttribute('data-area') === area;
        var hay = (p.getAttribute('data-search') || p.textContent).toLowerCase();
        var okText = !q || hay.indexOf(q) !== -1;
        var show = okArea && okText;
        p.hidden = !show;
        if (show) shown++;
      });
      sections.forEach(function (s) {
        var any = s.querySelector('.paper:not([hidden])');
        s.hidden = !any;
      });
      if (countEl) countEl.textContent = shown === papers.length ? papers.length + ' papers' : shown + ' of ' + papers.length + ' papers';
      if (empty) empty.hidden = shown !== 0;
    }
    areaChips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        area = chip.getAttribute('data-area');
        areaChips.forEach(function (c) { c.setAttribute('aria-pressed', c === chip ? 'true' : 'false'); });
        apply();
      });
    });
    if (searchBox) {
      searchBox.addEventListener('input', apply);
      document.addEventListener('keydown', function (e) {
        if (e.key === '/' && document.activeElement !== searchBox && !/input|textarea/i.test(document.activeElement.tagName)) {
          e.preventDefault(); searchBox.focus();
        }
      });
    }
    apply();
  }

  // Books category filter
  var bookBar = document.querySelector('.book-cats');
  if (bookBar) {
    var cats = Array.prototype.slice.call(document.querySelectorAll('.book-cat'));
    bookBar.querySelectorAll('.chip').forEach(function (chip) {
      chip.addEventListener('click', function () {
        var key = chip.getAttribute('data-cat');
        bookBar.querySelectorAll('.chip').forEach(function (c) { c.setAttribute('aria-pressed', c === chip ? 'true' : 'false'); });
        cats.forEach(function (c) { c.hidden = key !== 'all' && c.id !== 'cat-' + key; });
      });
    });
  }
})();
