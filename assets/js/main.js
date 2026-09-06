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
  if (navBtn && nav) {
    navBtn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      navBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
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
      // close sibling panels in the same paper
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

  // Copy BibTeX
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var src = document.getElementById(btn.getAttribute('data-copy'));
      if (!src) return;
      var text = src.textContent;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () { showToast('BibTeX copied'); }, function () { fallbackCopy(text); });
      } else { fallbackCopy(text); }
    });
  });
  function fallbackCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text; ta.setAttribute('readonly', ''); ta.style.position = 'absolute'; ta.style.left = '-9999px';
    document.body.appendChild(ta); ta.select();
    try { document.execCommand('copy'); showToast('BibTeX copied'); } catch (e) { showToast('Select the text and copy it'); }
    document.body.removeChild(ta);
  }

  // Research filters and search
  var filterBar = document.querySelector('.filters');
  if (filterBar) {
    var papers = Array.prototype.slice.call(document.querySelectorAll('.paper[data-area]'));
    var sections = Array.prototype.slice.call(document.querySelectorAll('.research-section'));
    var areaChips = filterBar.querySelectorAll('.chip[data-area]');
    var searchBox = filterBar.querySelector('.search-box');
    var countEl = filterBar.querySelector('.filter-count');
    var area = 'all';

    function apply() {
      var q = (searchBox ? searchBox.value : '').trim().toLowerCase();
      var shown = 0;
      papers.forEach(function (p) {
        var okArea = area === 'all' || p.getAttribute('data-area') === area;
        var okText = !q || p.textContent.toLowerCase().indexOf(q) !== -1;
        var show = okArea && okText;
        p.hidden = !show;
        if (show) shown++;
      });
      sections.forEach(function (s) {
        var any = s.querySelector('.paper:not([hidden])');
        s.hidden = !any;
      });
      if (countEl) countEl.textContent = shown === papers.length ? papers.length + ' papers' : shown + ' of ' + papers.length + ' papers';
    }
    areaChips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        area = chip.getAttribute('data-area');
        areaChips.forEach(function (c) { c.setAttribute('aria-pressed', c === chip ? 'true' : 'false'); });
        apply();
      });
    });
    if (searchBox) searchBox.addEventListener('input', apply);
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
