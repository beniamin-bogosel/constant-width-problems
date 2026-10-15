'use strict';
(() => {
  const routes = [...document.querySelectorAll('.route')];
  const main = document.getElementById('content');
  const tree = document.getElementById('chapter-tree');
  const sidebar = document.getElementById('sidebar');
  const search = document.getElementById('search');
  const menu = document.getElementById('menu-button');
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  function closeReveals() {
    document.querySelectorAll('.reveal-button').forEach(button => {
      button.setAttribute('aria-expanded', 'false');
      document.getElementById(button.getAttribute('aria-controls')).hidden = true;
      button.querySelector('.toggle-label').textContent = button.dataset.closedLabel;
      button.querySelector('.symbol').textContent = '+';
    });
  }
  function navigate(initial = false) {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)) || 'overview'; } catch { id = 'not-found'; }
    const route = routes.find(section => section.id === id) || document.getElementById('not-found');
    closeReveals();
    routes.forEach(section => section.hidden = section !== route);
    document.querySelectorAll('[data-route-link]').forEach(link => {
      if (link.getAttribute('href') === '#' + route.id) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });
    const chapter = route.dataset.chapter;
    if (chapter) {
      if (!search.value.trim()) {
        tree.querySelectorAll('details').forEach(group => group.open = group.id === 'tree-' + chapter);
      }
      const group = document.getElementById('tree-' + chapter);
      if (group) group.open = true;
    }
    const breadcrumb = document.getElementById('breadcrumb');
    breadcrumb.replaceChildren();
    const addLink = (label, target) => {
      if (breadcrumb.childNodes.length) {
        const separator = document.createElement('span'); separator.textContent = ' / '; separator.setAttribute('aria-hidden','true'); breadcrumb.append(separator);
      }
      const node = document.createElement(target ? 'a' : 'span'); node.textContent = label;
      if (target) node.href = '#' + target; else node.setAttribute('aria-current','page');
      breadcrumb.append(node);
    };
    addLink('Collection', route.id === 'overview' ? null : 'overview');
    if (chapter) addLink('Chapter ' + route.dataset.chapterNumber, route.id === chapter ? null : chapter);
    if (route.dataset.problemNumber) addLink('Problem ' + route.dataset.problemNumber, null);
    if (route.id === 'not-found') addLink('Page not found', null);
    document.title = (route.id === 'overview' ? '' : route.dataset.title + ' · ') + 'Shapes of constant width';
    sidebar.classList.remove('is-open'); menu.setAttribute('aria-expanded','false');
    if (!initial) { window.scrollTo({top:0,left:0,behavior:'instant'}); main.focus({preventScroll:true}); }
  }
  document.addEventListener('click', event => {
    if (event.target.closest('.skip-link')) {
      event.preventDefault(); main.focus(); return;
    }
    const button = event.target.closest('.reveal-button');
    if (!button) return;
    const opening = button.getAttribute('aria-expanded') !== 'true';
    button.setAttribute('aria-expanded', String(opening));
    document.getElementById(button.getAttribute('aria-controls')).hidden = !opening;
    button.querySelector('.toggle-label').textContent = opening ? button.dataset.openLabel : button.dataset.closedLabel;
    button.querySelector('.symbol').textContent = opening ? '−' : '+';
  });
  let beforeSearch = null;
  search.addEventListener('input', () => {
    const query = normalize(search.value.trim());
    if (query && beforeSearch === null) beforeSearch = [...tree.querySelectorAll('details')].map(group => group.open);
    let count = 0;
    tree.querySelectorAll('details').forEach((group, index) => {
      let matches = 0;
      group.querySelectorAll('.problem-nav-item').forEach(item => {
        const match = !query || normalize(item.dataset.search).includes(query);
        item.hidden = !match; if (match) matches++;
      });
      group.hidden = matches === 0;
      if (query && matches) group.open = true;
      if (!query && beforeSearch) group.open = beforeSearch[index];
      count += matches;
    });
    if (!query) beforeSearch = null;
    document.getElementById('no-results').hidden = count !== 0;
    document.getElementById('search-status').textContent = query ? count + ' matching problems' : '';
  });
  menu.addEventListener('click', () => {
    const opened = sidebar.classList.toggle('is-open'); menu.setAttribute('aria-expanded',String(opened));
    if (opened) search.focus();
  });
  window.addEventListener('hashchange', () => navigate());
  window.addEventListener('pageshow', () => closeReveals());
  navigate(true);
})();
