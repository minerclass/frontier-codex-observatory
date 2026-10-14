(() => {
  'use strict';
  const data = JSON.parse(document.getElementById('data').textContent);
  const charts = JSON.parse(document.getElementById('charts').textContent);
  const modelMap = new Map(data.models.map(model => [model.slug, model]));
  const escape = value => String(value ?? '').replace(/[&<>"']/g, character => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[character]));
  const typeNames = {'independent':'Independent evaluator','claim':'Own-lab claim','rival-table':'Rival-lab table'};
  const format = row => row.value === null ? 'Unavailable' : Number(row.value).toLocaleString(undefined, {maximumFractionDigits:2}) + (row.unit === 'percent' ? '%' : ' ' + row.unit);
  const views = [
    {id:'model-observatory',label:'Model map',height:900,note:'Select a model or an evaluation stage. A harness and a model form a system; the compiler is a separate agent.'},
    {id:'benchmark-landscape',label:'Independent benchmarks',height:880,receipt:'benchmark-landscape-sources',note:'Compare within each column. Finance gives partial credit; legal requires all criteria to pass; app scores average workflow success.'},
    {id:'performance-cost',label:'Cost & performance',height:790,receipt:'performance-cost-sources',note:'Recorded Vals task cost and terminal score. Costs retain the test rates, including Argon’s recorded $4/$20 tariff.'},
    {id:'claims-and-runs',label:'Claims & independent',height:850,receipt:'claims-and-runs-sources',note:'Company and Vals runs use different setups. Fallback counted as failure is an alternate scoring rule, not a new model.'}
  ];
  let active = views[0];
  const chart = document.getElementById('chart');
  const buttons = document.getElementById('views');
  const receipt = document.getElementById('receipt');
  function renderView(view) {
    active = view;
    for (const button of buttons.querySelectorAll('button')) button.setAttribute('aria-pressed', String(button.dataset.view === view.id));
    chart.srcdoc = charts[view.id];
    chart.title = view.label + ' — interactive chart';
    chart.height = view.height;
    document.getElementById('chart-note').textContent = view.note;
    receipt.open = false;
    receipt.hidden = !view.receipt;
    document.getElementById('receipt-content').replaceChildren();
  }
  for (const view of views) {
    const button = document.createElement('button');
    button.type = 'button'; button.dataset.view = view.id; button.textContent = view.label;
    button.addEventListener('click', () => renderView(view)); buttons.append(button);
  }
  receipt.addEventListener('toggle', () => {
    if (receipt.open && active.receipt && !receipt.querySelector('iframe')) {
      const frame = document.createElement('iframe');
      frame.className = 'chart-frame'; frame.title = active.label + ' source receipts'; frame.height = 660;
      frame.srcdoc = charts[active.receipt]; document.getElementById('receipt-content').append(frame);
    }
  });
  renderView(active);
  document.getElementById('stats').innerHTML = `<span><strong>${data.models.length}</strong>model labels</span><span><strong>${data.records.filter(row => row.value !== null).length}</strong>published values</span><span><strong>${new Set(data.records.map(row => row.sourceUrl)).size}</strong>source pages</span>`;
  const benchmark = document.getElementById('benchmark');
  const model = document.getElementById('model');
  const type = document.getElementById('type');
  const benchmarks = [...new Map(data.records.map(row => [row.benchmarkId, row.benchmark + ' · ' + row.publisher + ' · ' + row.benchmarkId])).entries()];
  benchmark.innerHTML = benchmarks.map(([id, label]) => `<option value="${escape(id)}">${escape(label)}</option>`).join('');
  model.insertAdjacentHTML('beforeend', data.models.map(model => `<option value="${escape(model.slug)}">${escape(model.name)}</option>`).join(''));
  function renderRecords() {
    const rows = data.records.filter(row => row.benchmarkId === benchmark.value && (model.value === 'all' || row.model === model.value) && (type.value === 'all' || row.sourceType === type.value));
    document.getElementById('count').textContent = `${rows.length} observations · Setup preserved · Every collected effort row retained`;
    const output = document.getElementById('record-output');
    if (!rows.length) { output.innerHTML = '<div class="empty">No published result matches this selection. A missing result is not zero.</div>'; return; }
    output.innerHTML = `<div class="record-table"><table><caption class="small quiet">${escape(rows[0].benchmark)} — ${escape(rows[0].publisher)} setup</caption><thead><tr><th scope="col">Model</th><th scope="col">Value</th><th scope="col">Setup</th><th scope="col">Source receipt</th><th scope="col">Cost / task</th></tr></thead><tbody>${rows.map(row => {
      const settings = Object.entries(row.setting).filter(([,value]) => value !== null).map(([key,value]) => `${key}: ${value}`);
      return `<tr><td><strong>${escape(modelMap.get(row.model).name)}</strong><span class="record-note small quiet">${escape(row.note)}</span></td><td class="numeric">${format(row)}<span class="origin">${escape(row.origin)}</span></td><td>${settings.length ? settings.map(escape).join('<br>') : '<span class="quiet">Not stated in extracted row</span>'}</td><td><a href="${escape(row.sourceUrl)}" target="_blank" rel="noopener noreferrer">${escape(row.publisher)} ↗</a><div class="origin">${escape(typeNames[row.sourceType])}</div><div class="small quiet">Source ${escape(row.sourceDate || 'date not stated')}<br>Read ${escape(row.readOn)} · ${row.sourceRead ? 'direct' : 'second-hand'}</div></td><td class="numeric">${row.costUsd === null ? '—' : '$' + row.costUsd.toFixed(2)}</td></tr>`;
    }).join('')}</tbody></table></div>`;
  }
  for (const control of [benchmark, model, type]) control.addEventListener('change', renderRecords);
  renderRecords();
  document.getElementById('model-table').innerHTML = `<table><thead><tr><th scope="col">Model / label</th><th scope="col">Maker</th><th scope="col">Verified release</th><th scope="col">Surface or naming note</th></tr></thead><tbody>${data.models.map(model => `<tr><td><strong>${escape(model.name)}</strong></td><td>${escape(model.maker)}</td><td>${model.releaseDate ? `<a href="${escape(model.releaseSource)}" target="_blank" rel="noopener">${escape(model.releaseDate)}</a>` : 'Not verified'}</td><td>${escape(model.note)}</td></tr>`).join('')}</tbody></table>`;
  document.getElementById('revision-log').innerHTML = `<div class="compare-list section">${data.revisions.map(revision => `<article><h3>Revision ${String(revision.revision).padStart(2,'0')} · ${escape(revision.date)}</h3><p>${escape(revision.reason)}</p><a href="${escape(revision.snapshot)}">Review snapshot JSON →</a></article>`).join('')}</div>`;
  document.getElementById('download').addEventListener('click', () => {
    const url = URL.createObjectURL(new Blob([JSON.stringify(data,null,2) + '\n'], {type:'application/json'}));
    const anchor = document.createElement('a'); anchor.href = url; anchor.download = 'codex-frontier-revision-02.json'; anchor.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
})();
