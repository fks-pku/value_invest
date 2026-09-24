/* The editor is a separate local workbench; published reports remain self-contained. */
(() => {
  const $ = id => document.getElementById(id);
  const activeStates = new Set(['queued', 'running', 'validating', 'publishing']);
  let state, selected, operation, editNode, editVersion, previewSequence = 0, previewTimer, shownReport = '';
  let processState, processKey = '', refreshing = false;
  const token = document.querySelector('meta[name="research-token"]').content;
  function element(tag, text, className) {
    const el = document.createElement(tag); el.textContent = text;
    if (className) el.className = className;
    return el;
  }
  async function api(path, body) {
    const response = await fetch(path, body ? {method:'POST', headers:{'Content-Type':'application/json','X-Research-Token':token}, body:JSON.stringify(body)} : {cache:'no-store'});
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || '请求失败');
    return result;
  }
  function treeData() {
    const job = state.job;
    return job && activeStates.has(job.status) ? job.proposal.tree : state.tree;
  }
  function nodeById(id) { return treeData().nodes.find(n => n.id === id); }
  function select(id) {
    selected = nodeById(id)?.id || treeData().nodes[0].id;
    history.replaceState(null, '', '#' + encodeURIComponent(selected));
    for (const button of $('tree').querySelectorAll('[data-node]')) {
      if (button.dataset.node === selected) button.setAttribute('aria-current', 'page');
      else button.removeAttribute('aria-current');
    }
    const node = nodeById(selected), busy = state.job && activeStates.has(state.job.status);
    $('selected-label').textContent = `${selected} · L${node.level}`;
    for (const id of ['edit', 'add', 'remove', 'rerun']) $(id).disabled = Boolean(busy);
    $('add').disabled ||= node.level >= 5 || node.level === 1;
    $('remove').disabled ||= !node.parent_id;
    const stale = busy && state.job.proposal.affected_ids.includes(selected);
    $('pending').hidden = !stale; $('article').hidden = stale;
    $('pending-title').textContent = node.question;
    $('view-old').disabled = !state.tree.nodes.some(n => n.id === selected);
    showArticle();
    renderProcess();
  }
  function showArticle() {
    const url = '/report?v=' + state.version + '#' + encodeURIComponent(selected);
    if (shownReport !== url) { $('article').src = url; shownReport = url; }
  }
  function renderTree() {
    const nodes = treeData().nodes;
    function branch(parent) {
      const ul = document.createElement('ul');
      for (const node of nodes.filter(n => (n.parent_id || '') === parent)) {
        const li = document.createElement('li'), button = element('button', '', 'node');
        button.dataset.node = node.id;
        button.append(element('small', 'L' + node.level), element('span', node.question), element('i', '', node.passed ? 'passed' : ''));
        button.addEventListener('click', () => select(node.id)); li.append(button);
        if (nodes.some(n => n.parent_id === node.id)) li.append(branch(node.id));
        ul.append(li);
      }
      return ul;
    }
    $('tree').replaceChildren(branch(''));
  }
  async function refresh() {
    if (refreshing) return;
    refreshing = true;
    try {
      const prior = state;
      state = await api('/api/state');
      $('title').textContent = state.tree.title;
      $('cutoff').textContent = `AS OF ${state.tree.as_of_date} · 截面锁定`;
      const job = state.job, busy = job && activeStates.has(job.status);
      $('run-title').textContent = job ? ({queued:'已进入研究队列',running:'正在研究',validating:'正在验证',publishing:'正在发布',updated:'新报告已发布',failed:'未发布新版本',cancelled:'研究已取消'}[job.status] || job.status) : '可编辑 · 本地研究器';
      $('run-message').textContent = job?.message || '编辑问题后确认影响范围，研究完成后自动更新。';
      document.body.classList.toggle('running', Boolean(busy));
      document.body.classList.toggle('failed', job?.status === 'failed');
      $('cancel-run').hidden = !busy; $('retry').hidden = !job || !['failed','cancelled'].includes(job.status);
      if (!prior || prior.version !== state.version || prior.job?.id !== job?.id || prior.job?.status !== job?.status) {
        renderTree(); select(selected || decodeURIComponent(location.hash.slice(1)));
      }
      $('error').hidden = true;
      if (job) {
        $('process').hidden = false;
        if (processState && processState.job_id !== job.id) {
          processState = null; processKey = '';
          $('process-updates').replaceChildren(); $('process-nodes').replaceChildren();
          $('process-meta').textContent = '正在读取本轮执行记录…';
        }
        try {
          const progress = await api('/api/process');
          if (progress.job_id === job.id) {
            const key = JSON.stringify(progress);
            if (key !== processKey) {
              if (processState?.job_id !== progress.job_id) $('process').open = true;
              processState = progress; processKey = key; renderProcess();
            }
          }
        } catch (_) {
          $('process-meta').textContent = '过程记录暂不可用；报告连接正常';
        }
      } else { $('process').hidden = true; processState = null; processKey = ''; }
    } catch (error) {
      $('error').textContent = '无法连接本地服务：' + error.message; $('error').hidden = false;
    } finally { refreshing = false; }
  }
  function renderProcess() {
    const progress = processState;
    if (!progress || progress.job_id !== state?.job?.id) return;
    const time = progress.last_activity_at ? new Date(progress.last_activity_at).toLocaleTimeString('zh-CN', {hour12:false}) : '尚无';
    $('process-meta').textContent = `联网检索 ${progress.web_searches} 次 · 最近活动 ${time}`;
    $('process-note').textContent = progress.note;
    const updates = $('process-updates'); updates.replaceChildren();
    for (const update of progress.updates) {
      const li = element('li', '');
      li.append(element('span', String(update.sequence).padStart(2, '0'), 'update-number'), element('p', update.text)); updates.append(li);
    }
    if (!progress.updates.length) updates.append(element('li', '尚无进展摘要。执行器正在准备或尚未输出公开汇报。', 'process-empty'));
    const container = $('process-nodes'); container.replaceChildren();
    const nodes = progress.nodes.filter(n => !$('process-current').checked || n.id === selected);
    for (const node of nodes) {
      const section = element('section', '', 'process-node');
      const button = element('button', `${node.id} · ${node.question}`, 'process-node-link');
      button.addEventListener('click', () => select(node.id)); section.append(button);
      if (node.role === 'leaf') {
        section.append(element('p', `已记录：检索 ${node.search_runs} 轮 → 抽取 ${node.extractions} 条 → 复核 ${node.reviews} 条`, 'process-counts'));
        if (node.data_required.length) section.append(element('p', '取证目标：' + node.data_required.join('；'), 'process-target'));
        if (node.analysis_plan.length) section.append(element('p', '分析方法：' + node.analysis_plan.join('；'), 'process-target'));
        for (const source of node.sources) {
          const row = element('p', '', 'process-source');
          const link = element(source.url ? 'a' : 'span', source.title);
          if (source.url) { link.href = source.url; link.target = '_blank'; link.rel = 'noopener noreferrer'; }
          row.append(link, element('small', source.date)); section.append(row);
        }
      } else section.append(element('p', '汇总节点：整合子问题结论，不独立重复检索。', 'process-target'));
      if (node.conclusion) {
        section.append(element('strong', progress.status === 'updated' ? '本轮结论（已发布）' : '阶段性结论（未发布）'));
        section.append(element('p', node.conclusion));
        section.append(element('p', node.passed ? '执行器记录：本题充分；仍以发布门禁为准。' : '执行器记录：仍有证据缺口。', 'process-target'));
        if (node.gaps.length) section.append(element('p', '待补证：' + node.gaps.join('；'), 'process-target'));
      } else section.append(element('p', '尚未记录本轮结论。检索、解析与写入可能分批完成，数量不是完成百分比。', 'process-empty'));
      container.append(section);
    }
    if (!nodes.length) container.append(element('p', '当前问题不在本轮研究范围。取消勾选可查看本轮其它问题。', 'process-empty'));
  }
  $('process-current').addEventListener('change', renderProcess);
  function request() { return {version:editVersion, node_id:editNode, operation, question:$('question').value, reason:$('reason').value}; }
  async function preview() {
    const sequence = ++previewSequence; $('submit').disabled = true; $('editor-error').textContent = '';
    try {
      const impact = await api('/api/preview', request());
      if (sequence !== previewSequence) return;
      const container = $('impact-content'); container.replaceChildren();
      for (const [ids, label] of [[impact.research_ids,'重新检索与分析'],[impact.rollup_ids,'自底向上重新汇总'],[impact.removed_ids,'从本版移除（历史保留）']]) {
        if (!ids.length) continue;
        container.append(element('p', `${label} · ${ids.length} 个问题`));
        const ul = document.createElement('ul');
        ids.forEach(id => ul.append(element('li', (id === editNode && operation === 'edit' ? $('question').value : nodeById(id)?.question || $('question').value) + ' · ' + id)));
        container.append(ul);
      }
      $('submit').disabled = false;
    } catch (error) {
      if (sequence !== previewSequence) return;
      $('impact-content').textContent = error.message;
    }
  }
  function openEditor(mode, previous) {
    operation = mode; editNode = previous?.node_id || selected; editVersion = state.version;
    const node = nodeById(editNode); if (!node) return;
    $('editor-title').textContent = {edit:'编辑研究问题',add:'新增子问题',remove:'移除问题分支',rerun:'重新研究当前分支'}[mode];
    $('edit-location').textContent = `${editNode} · ${node.question}`;
    $('question').value = previous?.question || (mode === 'add' ? '' : node.question);
    $('question').disabled = ['remove','rerun'].includes(mode);
    $('reason').value = previous?.reason || '';
    $('submit').textContent = mode === 'remove' ? '确认移除并研究 →' : '保存并研究 →';
    $('editor').showModal(); preview();
    (mode === 'edit' || mode === 'add' ? $('question') : $('reason')).focus();
  }
  for (const mode of ['edit','add','remove','rerun']) $(mode).addEventListener('click', () => openEditor(mode));
  for (const id of ['close-editor','discard']) $(id).addEventListener('click', () => { ++previewSequence; $('editor').close(); });
  for (const id of ['question','reason']) $(id).addEventListener('input', () => { ++previewSequence; $('submit').disabled = true; clearTimeout(previewTimer); previewTimer = setTimeout(preview, 250); });
  $('edit-form').addEventListener('submit', async event => {
    event.preventDefault(); $('submit').disabled = true;
    try { await api('/api/research', request()); $('editor').close(); await refresh(); }
    catch (error) { $('editor-error').textContent = error.message; }
  });
  $('cancel-run').addEventListener('click', async () => {
    try { await api('/api/cancel', {}); await refresh(); } catch (error) { $('error').textContent = error.message; $('error').hidden = false; }
  });
  $('retry').addEventListener('click', () => openEditor(state.job.proposal.edit.operation, state.job.proposal.edit));
  $('view-old').addEventListener('click', () => { $('article').hidden = false; $('pending').hidden = true; $('run-message').textContent = '正在阅读上次已发布版本，不是编辑后问题的答案。'; });
  addEventListener('message', event => {
    if (event.source === $('article').contentWindow && event.data?.type === 'research-node' && state && nodeById(event.data.node)) select(event.data.node);
  });
  addEventListener('hashchange', () => { if (state) select(decodeURIComponent(location.hash.slice(1))); });
  refresh(); setInterval(refresh, 2500);
})();
