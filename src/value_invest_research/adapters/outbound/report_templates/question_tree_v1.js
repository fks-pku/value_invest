/* Progressive enhancement only. All research text already exists in the HTML. */
(() => {
  const root = document.documentElement;
  const pane = document.getElementById('detail-pane');
  const articles = [...pane.querySelectorAll('.node-detail')];
  const nodes = new Map(articles.map(article => [article.id, article]));
  const links = [...document.querySelectorAll('[data-node-link]')];
  const toggle = document.getElementById('reading-mode');
  const fallback = articles.find(article => !article.dataset.parentId);
  let active = fallback;
  const behavior = matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth';

  function select(hash, scroll = false) {
    let id;
    try { id = decodeURIComponent(hash.replace(/^#/, '')); } catch { id = ''; }
    const destination = document.getElementById(id);
    const article = nodes.get(id) || destination?.closest('.node-detail') || active;
    active = article;
    const path = new Set();
    let ancestor = article;
    while (ancestor) {
      path.add(ancestor.id);
      ancestor = nodes.get(ancestor.dataset.parentId);
    }
    for (const item of articles) item.classList.toggle('is-active', item === article);
    for (const link of links) {
      const selected = link.dataset.nodeLink === article.id;
      link.classList.toggle('is-active', selected);
      link.classList.toggle('is-on-path', path.has(link.dataset.nodeLink));
      if (selected) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    }
    root.classList.add('js-ready');
    const target = destination || article;
    for (let detail = target.closest('details'); detail; detail = detail.parentElement?.closest('details')) detail.open = true;
    if (target.id === 'source-index' || target.closest('.source-index')) document.getElementById('source-index').open = true;
    if (scroll) target.scrollIntoView({behavior, block:'start'});
  }

  document.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#"]');
    if (!link || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    if (location.hash !== link.hash) history.pushState(null, '', link.hash);
    select(link.hash, true);
  });
  toggle.addEventListener('click', () => {
    const all = root.classList.toggle('show-all');
    toggle.textContent = all ? '单节点阅读' : '查看全文';
    toggle.setAttribute('aria-pressed', String(all));
    if (all) for (const detail of document.querySelectorAll('.supplementary-analysis')) detail.open = true;
    if (!all) select('#' + active.id, true);
  });
  addEventListener('hashchange', () => select(location.hash, true));
  addEventListener('popstate', () => select(location.hash, true));
  let printStates = [];
  addEventListener('beforeprint', () => {
    printStates = [...document.querySelectorAll('details')].map(detail => [detail, detail.open]);
    for (const [detail] of printStates) detail.open = true;
  });
  addEventListener('afterprint', () => { for (const [detail, open] of printStates) detail.open = open; });
  select(location.hash || '#' + fallback.id);
})();
