/* Runs only inside the local editor's report iframe. The offline report stays standalone. */
(() => {
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#"]');
    if (!link) return;
    const id = decodeURIComponent(link.hash.slice(1));
    if (document.getElementById(id)?.classList.contains('node-detail'))
      parent.postMessage({type: 'research-node', node: id}, '*');
  });

  function paragraphOf(node) {
    const element = node?.nodeType === Node.TEXT_NODE ? node.parentElement : node;
    return element?.closest?.('p[data-comment-node]');
  }
  function offerSelection() {
    const selection = getSelection();
    if (!selection || selection.isCollapsed || !selection.rangeCount) return;
    const range = selection.getRangeAt(0);
    const paragraph = paragraphOf(range.startContainer);
    if (!paragraph || paragraph !== paragraphOf(range.endContainer)) return;
    const article = paragraph.closest('.node-detail');
    if (!article || article.dataset.kind !== 'leaf') return;
    const quote = selection.toString().replace(/\s+/g, ' ').trim();
    if (quote.length < 2 || quote.length > 1200) return;
    parent.postMessage({type: 'research-passage-selection', node: paragraph.dataset.commentNode,
      section: Number(paragraph.dataset.commentSection), paragraph: Number(paragraph.dataset.commentParagraph),
      quote}, '*');
  }
  document.addEventListener('pointerup', offerSelection);
  document.addEventListener('keyup', offerSelection);
  let selectionScheduled = false;
  document.addEventListener('selectionchange', () => {
    if (selectionScheduled) return;
    selectionScheduled = true;
    requestAnimationFrame(() => { selectionScheduled = false; offerSelection(); });
  });
})();
