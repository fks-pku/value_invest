from __future__ import annotations


def report_css() -> str:
    return _css()


def _css() -> str:
    return """
:root {
  color-scheme: light;
  --bg: #f5f7fb;
  --surface: rgba(255,255,255,.88);
  --surface-strong: #ffffff;
  --text: #1d1d1f;
  --muted: #667085;
  --line: #d9e0ea;
  --blue: #0a84ff;
  --green: #1d9a6c;
  --amber: #b7791f;
  --red: #c2413d;
  --shadow: 0 20px 60px rgba(20, 32, 54, .10);
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", sans-serif;
  color: var(--text);
  background: radial-gradient(circle at 20% 0%, #e8f2ff 0, transparent 32rem), var(--bg);
  line-height: 1.62;
}
a { color: var(--blue); text-decoration: none; }
a:hover { text-decoration: underline; }
.hero {
  padding: 24px clamp(20px, 5vw, 72px) 52px;
  background: linear-gradient(180deg, rgba(255,255,255,.94), rgba(255,255,255,.58));
  border-bottom: 1px solid var(--line);
}
.top-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  justify-content: center;
  margin: 0 auto 44px;
}
.top-nav a {
  padding: 8px 12px;
  border: 1px solid rgba(10,132,255,.18);
  border-radius: 999px;
  background: rgba(255,255,255,.72);
  color: #28506f;
  font-size: 13px;
}
.hero-inner { max-width: 1120px; margin: 0 auto; }
.eyebrow, .section-kicker, .label {
  margin: 0 0 8px;
  color: var(--blue);
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
}
h1 { max-width: 980px; margin: 0; font-size: clamp(34px, 5vw, 68px); line-height: 1.04; letter-spacing: 0; }
.hero-subtitle { max-width: 720px; color: var(--muted); font-size: 19px; }
.hero-meta { display: flex; gap: 10px; flex-wrap: wrap; }
.hero-meta span, .state-pill {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: 6px 10px;
  background: rgba(255,255,255,.8);
  border: 1px solid var(--line);
  color: var(--muted);
  font-size: 13px;
}
.section { max-width: 1180px; margin: 0 auto; padding: 48px clamp(18px, 4vw, 36px); }
.section-heading { display: flex; align-items: end; justify-content: space-between; gap: 16px; margin-bottom: 20px; }
.section-heading h2 { margin: 0; font-size: clamp(28px, 3vw, 42px); letter-spacing: 0; }
.section-note, .muted { color: var(--muted); }
.goal-card, .chain-explain, .qa-card, .target-section .target-table, .source-collapse {
  border: 1px solid var(--line);
  border-radius: 22px;
  background: var(--surface);
  box-shadow: var(--shadow);
}
.goal-card {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
  padding: 22px;
}
.constraint-definition {
  grid-column: 1 / -1;
  border: 1px solid rgba(10,132,255,.16);
  border-radius: 18px;
  background: linear-gradient(180deg, #ffffff, #fbfdff);
  padding: 16px;
}
.constraint-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}
.constraint-grid article {
  border: 1px solid #e5edf7;
  border-radius: 16px;
  background: #f8fbff;
  padding: 14px;
}
.constraint-grid span {
  display: block;
  color: var(--blue);
  font-size: 12px;
  font-weight: 900;
  margin-bottom: 6px;
}
.constraint-grid p {
  margin: 0;
  color: #435064;
  font-size: 13px;
}
.goal-main { font-size: 22px; font-weight: 700; }
.industry-overview-section {
  display: grid;
  gap: 14px;
}
.industry-module {
  border: 1px solid var(--line);
  border-radius: 22px;
  background: var(--surface);
  box-shadow: var(--shadow);
  overflow: hidden;
}
.industry-module > summary {
  list-style: none;
  cursor: pointer;
}
.industry-module > summary::-webkit-details-marker {
  display: none;
}
.industry-module[open] > summary {
  border-bottom: 1px solid var(--line);
}
.industry-module-body {
  padding: 22px;
  min-width: 0;
  max-width: 100%;
}
.module-head {
  display: grid;
  grid-template-columns: auto 1fr auto;
  column-gap: 12px;
  row-gap: 3px;
  align-items: center;
  margin: 0;
  padding: 18px 22px;
}
.module-head .module-index {
  display: inline-flex;
  width: 34px;
  height: 34px;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  background: #eaf3ff;
  color: var(--blue);
  font-size: 12px;
  font-weight: 900;
}
.module-head .chevron {
  color: var(--muted);
  font-size: 18px;
  font-weight: 900;
  transition: transform .18s ease;
}
.industry-module[open] > .module-head .chevron {
  transform: rotate(90deg);
}
.module-head h3 {
  margin: 0;
  font-size: 21px;
}
.module-head p {
  margin: 0;
  color: var(--muted);
  font-size: 14px;
}
.overview-subtitle {
  color: #334155;
  font-size: 13px;
  font-weight: 900;
}
.chain-explain { padding: 22px; }
.chain-plain-summary { margin-top: 0; font-size: 18px; color: #344054; }
.chain-research-bridge, .chain-data-gaps {
  border: 1px solid rgba(10,132,255,.16);
  border-radius: 18px;
  background: linear-gradient(180deg, #ffffff, #fbfdff);
  padding: 16px;
  margin: 18px 0;
}
.chain-bridge-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}
.chain-bridge-card {
  border: 1px solid #e5edf7;
  border-radius: 16px;
  background: #f8fbff;
  padding: 14px;
}
.chain-bridge-card span {
  display: block;
  color: var(--muted);
  font-size: 12px;
  font-weight: 800;
  margin-bottom: 6px;
}
.chain-bridge-card strong {
  display: block;
  color: #223047;
  line-height: 1.55;
}
.chain-research-bridge > p {
  margin: 12px 0;
  color: #435064;
  line-height: 1.75;
}
.chain-node-lens {
  border: 1px solid #e7edf6;
  border-radius: 16px;
  background: #fff;
  padding: 14px;
  margin: 14px 0;
}
.chain-node-lens > b {
  display: block;
  color: #27364a;
  margin-bottom: 10px;
}
.chain-node-lens ul {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
  margin: 0;
  padding: 0;
  list-style: none;
}
.chain-node-lens li {
  border: 1px solid #edf1f7;
  border-radius: 14px;
  background: #fbfcff;
  padding: 12px;
}
.chain-node-lens li b {
  display: block;
  color: var(--blue);
  font-size: 12px;
  margin-bottom: 4px;
}
.chain-node-lens li span {
  display: block;
  color: #526071;
  font-size: 12px;
  line-height: 1.55;
}
.chain-data-gaps summary {
  cursor: pointer;
  font-weight: 900;
  color: #344054;
}
.chain-data-gaps ul {
  margin: 10px 0 0;
  padding-left: 20px;
  color: #526071;
  line-height: 1.75;
}
.chain-detail-panel,
.space-detail-panel {
  border: 1px solid rgba(10,132,255,.16);
  border-radius: 18px;
  background: #fbfcff;
  margin: 14px 0;
  overflow: hidden;
}
.chain-detail-panel > summary,
.space-detail-panel > summary {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 10px;
  align-items: center;
  list-style: none;
  cursor: pointer;
  padding: 14px 16px;
}
.chain-detail-panel > summary::-webkit-details-marker,
.space-detail-panel > summary::-webkit-details-marker {
  display: none;
}
.chain-detail-panel > summary span:first-child,
.space-detail-panel > summary span:first-child {
  color: #27364a;
  font-weight: 900;
}
.chain-detail-panel > summary small,
.space-detail-panel > summary small {
  color: var(--muted);
  font-size: 12px;
  line-height: 1.45;
}
.chain-detail-panel[open] > summary,
.space-detail-panel[open] > summary {
  border-bottom: 1px solid var(--line);
}
.chain-detail-body,
.space-detail-body {
  padding: 16px;
  min-width: 0;
  max-width: 100%;
}
.industry-space-summary {
  border: 1px solid rgba(10,132,255,.16);
  border-radius: 18px;
  background: linear-gradient(180deg, #ffffff, #fbfdff);
  padding: 16px;
  margin-bottom: 14px;
}
.industry-space-summary > p {
  margin: 0 0 12px;
  color: #344054;
  font-weight: 760;
  line-height: 1.75;
}
.space-bom-reasoning {
  display: grid;
  gap: 12px;
}
.space-node-card {
  border: 1px solid rgba(10,132,255,.16);
  border-radius: 16px;
  background: #fbfcff;
  overflow: hidden;
}
.space-node-card > summary {
  display: grid;
  grid-template-columns: auto minmax(160px, .45fr) minmax(240px, 1fr) auto;
  gap: 10px;
  align-items: center;
  list-style: none;
  cursor: pointer;
  padding: 14px 16px;
}
.space-node-card > summary::-webkit-details-marker {
  display: none;
}
.space-node-card[open] > summary {
  border-bottom: 1px solid var(--line);
}
.space-node-label {
  display: inline-flex;
  border-radius: 999px;
  background: #eef5ff;
  color: var(--blue);
  border: 1px solid #d8e8ff;
  font-size: 11px;
  font-weight: 900;
  padding: 3px 8px;
}
.space-node-card summary strong {
  color: #27364a;
  font-size: 14px;
}
.space-node-card summary small {
  color: #667085;
  font-size: 12px;
  line-height: 1.45;
}
.space-node-reasoning {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
  padding: 14px;
}
.space-node-section {
  border: 1px solid #e2e9f3;
  border-radius: 14px;
  background: #fff;
  padding: 12px;
}
.space-node-space-reasoning {
  border-color: #d9e8fb;
  background: #fbfdff;
}
.space-node-evidence {
  background: #fbfcff;
}
.space-node-section h4 {
  margin: 0 0 8px;
  color: #27364a;
  font-size: 13px;
}
.space-node-section p,
.space-node-section li {
  color: #526071;
  font-size: 12px;
  line-height: 1.65;
}
.space-node-section ul,
.space-node-section ol {
  margin: 0;
  padding-left: 18px;
}
.space-node-sources {
  margin-top: 10px;
}
.space-node-sizing {
  margin-top: 12px;
  border: 1px solid #d9e8fb;
  border-radius: 12px;
  background: linear-gradient(180deg, #f8fbff, #fff);
  padding: 12px;
}
.space-method-step {
  display: grid;
  gap: 8px;
  margin-bottom: 10px;
}
.space-step-title {
  display: flex;
  align-items: center;
  gap: 8px;
}
.space-step-title h5 {
  margin: 0;
  color: var(--blue);
  font-size: 12px;
}
.space-step-index {
  display: inline-flex;
  width: 22px;
  height: 22px;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  background: var(--blue);
  color: #fff;
  font-style: normal;
  font-size: 11px;
  font-weight: 900;
  flex: 0 0 auto;
}
.space-public-methods {
  margin-bottom: 0;
}
.space-method-card-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
}
.space-method-card {
  border: 1px solid #e1e9f4;
  border-radius: 12px;
  background: #fff;
  display: grid;
  grid-template-columns: minmax(128px, 168px) 1fr;
  gap: 12px;
  padding: 10px;
  min-width: 0;
}
.space-method-card header {
  border-right: 1px solid #edf1f7;
  display: grid;
  align-content: start;
  gap: 7px;
  padding-right: 10px;
}
.space-method-card header span {
  color: #27364a;
  font-size: 12px;
  font-weight: 900;
}
.space-method-card header small {
  width: max-content;
  color: var(--blue);
  background: #eef5ff;
  border: 1px solid #d8e8ff;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 900;
  padding: 2px 7px;
  white-space: nowrap;
}
.space-method-card-body {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 8px;
  min-width: 0;
}
.space-method-entry {
  border: 1px solid #edf1f7;
  border-radius: 10px;
  background: #fbfdff;
  padding: 9px;
  margin: 0;
}
.space-method-entry b {
  display: block;
  color: #1f2937;
  font-size: 12px;
  margin-bottom: 5px;
}
.space-method-entry p {
  margin: 0 0 8px;
  color: #344054;
  font-size: 12px;
  line-height: 1.55;
}
.space-method-entry p strong {
  color: var(--blue);
  font-size: 11px;
  font-weight: 900;
}
.space-method-entry dl {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 5px 10px;
  margin: 0;
}
.space-method-entry dl div {
  display: grid;
  grid-template-columns: 64px 1fr;
  gap: 6px;
}
.space-method-entry dt {
  color: var(--blue);
  font-size: 11px;
  font-weight: 900;
}
.space-method-entry dd {
  margin: 0;
  color: #526071;
  font-size: 11px;
  line-height: 1.45;
}
.space-method-entry-sources {
  margin-top: 8px;
}
.space-method-entry-sources .source-chips {
  gap: 5px;
}
.source-chip-missing {
  color: #956100;
  background: #fff7e6;
  border-color: #f4d28f;
}
.space-method-empty {
  align-self: center;
  margin: 0;
  color: var(--muted);
  font-size: 12px;
  line-height: 1.6;
}
.space-method-gap {
  border: 1px dashed #d8e3f2;
  border-radius: 10px;
  background: #fbfcff;
  padding: 9px;
  color: #5d6675;
}
.space-horizon-conclusion {
  display: grid;
  gap: 8px;
  margin-bottom: 10px;
}
.space-horizon-summary {
  border: 1px solid #e5edf7;
  border-radius: 10px;
  background: #fff;
  padding: 10px;
  margin: 0;
  color: #344054;
  font-size: 12px;
  line-height: 1.65;
}
.space-horizon-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 8px;
}
.space-horizon-card {
  border: 1px solid #e5edf7;
  border-radius: 10px;
  background: #fff;
  padding: 10px;
}
.space-horizon-card span {
  display: block;
  color: #667085;
  font-size: 11px;
  font-weight: 900;
  margin-bottom: 4px;
}
.space-horizon-card strong {
  display: inline-flex;
  border-radius: 999px;
  padding: 3px 8px;
  font-size: 12px;
  margin-bottom: 6px;
}
.space-horizon-large {
  color: var(--green);
  background: #e7f6ed;
}
.space-horizon-mid {
  color: var(--amber);
  background: #fff4d6;
}
.space-horizon-low {
  color: var(--red);
  background: #fee4e2;
}
.space-horizon-card p {
  margin: 0;
  color: #344054;
  font-size: 12px;
  line-height: 1.55;
}
.space-step-confidence {
  display: block;
  margin-top: 6px;
  color: #667085;
  font-size: 11px;
  font-weight: 900;
}
.space-node-sizing-table table {
  min-width: 760px;
}
.space-node-sizing-table th,
.space-node-sizing-table td {
  font-size: 12px;
}
.space-summary-grid,
.space-boundary-grid,
.space-driver-tree {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}
.space-summary-grid {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}
.space-boundary-grid {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}
.space-summary-grid article,
.space-boundary-grid article,
.space-driver-card,
.space-model-grid article {
  border: 1px solid #e5edf7;
  border-radius: 16px;
  background: #fff;
  padding: 14px;
}
.space-summary-grid span,
.space-boundary-grid span,
.space-driver-card span,
.space-model-grid span {
  display: block;
  color: var(--blue);
  font-size: 12px;
  font-weight: 900;
  margin-bottom: 6px;
}
.space-summary-grid strong,
.space-model-grid strong,
.space-boundary-grid p,
.space-driver-card b {
  display: block;
  margin: 0;
  color: #344054;
  font-size: 13px;
  line-height: 1.6;
}
.space-driver-card dl {
  display: grid;
  gap: 7px;
  margin: 10px 0 0;
}
.space-driver-card dl div {
  display: grid;
  grid-template-columns: 76px 1fr;
  gap: 8px;
}
.space-driver-card dt {
  color: var(--blue);
  font-size: 12px;
  font-weight: 900;
}
.space-driver-card dd {
  margin: 0;
  color: #526071;
  font-size: 12px;
  line-height: 1.55;
}
.space-gate-model {
  display: grid;
  gap: 12px;
}
.space-model-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
}
.space-model-note {
  border: 1px solid rgba(10,132,255,.16);
  border-radius: 16px;
  background: #fff;
  padding: 14px;
}
.space-model-note.warning {
  background: #fffaf0;
  border-color: #f4d28f;
}
.space-model-note b {
  display: block;
  color: #27364a;
  font-size: 13px;
  margin-bottom: 5px;
}
.space-model-note p {
  margin: 0;
  color: #526071;
  font-size: 13px;
  line-height: 1.65;
}
.space-evidence-pack {
  display: grid;
  gap: 12px;
}
.space-evidence-card {
  border: 1px solid rgba(10,132,255,.16);
  border-radius: 16px;
  background: linear-gradient(180deg, #ffffff, #f8fbff);
  padding: 14px;
}
.space-evidence-card header {
  border-bottom: 1px solid #e6edf7;
  margin-bottom: 12px;
  padding-bottom: 10px;
}
.space-evidence-card header span {
  display: inline-flex;
  color: var(--blue);
  background: #edf6ff;
  border: 1px solid #cfe6ff;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 900;
  padding: 3px 8px;
  margin-bottom: 8px;
}
.space-evidence-card h4 {
  margin: 0 0 5px;
  color: #1d2939;
  font-size: 16px;
}
.space-evidence-card header p {
  margin: 0;
  color: #526071;
  font-size: 13px;
  line-height: 1.6;
}
.space-evidence-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}
.space-evidence-grid section {
  border: 1px solid #e2e9f3;
  border-radius: 14px;
  background: #fff;
  padding: 12px;
}
.space-evidence-grid b {
  display: block;
  color: #27364a;
  font-size: 13px;
  margin-bottom: 7px;
}
.space-evidence-grid p,
.space-evidence-grid li {
  color: #526071;
  font-size: 12px;
  line-height: 1.65;
}
.space-evidence-grid ul,
.space-inference-chain {
  margin: 0;
  padding-left: 18px;
}
.space-refute-box {
  grid-column: 1 / -1;
  background: #fffaf0 !important;
  border-color: #f4d28f !important;
}
.space-evidence-sources {
  margin-top: 10px;
}
.space-scenario-table table { min-width: 1600px; }
.space-node-elasticity-table table { min-width: 2200px; }
.space-validation-table table { min-width: 1080px; }
.key-variable-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 14px;
}
.key-variable-bom-map {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 12px;
}
.key-variable-bom-card {
  border: 1px solid #d9e8fb;
  border-radius: 12px;
  background: #fbfdff;
  overflow: hidden;
}
.key-variable-bom-card > summary {
  list-style: none;
  cursor: pointer;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 8px;
  align-items: center;
  padding: 12px 14px;
}
.key-variable-bom-card > summary::-webkit-details-marker { display: none; }
.key-variable-bom-card > summary strong {
  color: #27364a;
  font-size: 13px;
}
.key-variable-bom-card > summary span:not(.chevron) {
  color: #667085;
  font-size: 11px;
  font-weight: 800;
}
.key-variable-bom-card[open] > summary {
  border-bottom: 1px solid #e6eaf1;
}
.key-variable-bom-card .overview-question-card {
  margin: 12px;
}
.qa-generation-table {
  overflow-x: auto;
  border: 1px solid var(--line);
  border-radius: 14px;
  background: #fbfcff;
}
.chain-map summary {
  cursor: pointer;
  font-weight: 800;
}
.chain-layer-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 12px; margin: 18px 0; }
.chain-layer-card {
  border: 1px solid var(--line);
  border-radius: 16px;
  background: var(--surface-strong);
  padding: 16px;
}
.chain-layer-card h3 { margin: 0 0 8px; font-size: 16px; }
.chain-stage-panel {
  padding: 0;
  overflow: hidden;
}
.chain-stage-panel .chain-stage-head {
  display: grid;
  gap: 8px;
  padding: 16px 16px 8px;
}
.chain-stage-panel .chain-stage-head strong {
  color: #344054;
  font-size: 13px;
  line-height: 1.55;
}
.chain-stage-panel summary {
  list-style: none;
  cursor: pointer;
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto auto;
  gap: 10px;
  align-items: center;
  padding: 16px;
}
.chain-stage-panel summary::-webkit-details-marker { display: none; }
.chain-stage-name {
  display: inline-flex;
  border-radius: 999px;
  background: #eaf3ff;
  color: #0a5dcc;
  font-weight: 900;
  font-size: 12px;
  padding: 4px 10px;
}
.chain-stage-panel summary small {
  color: var(--muted);
  font-weight: 800;
}
.chain-company-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 12px;
  padding: 0 16px 16px;
  margin: 0;
  list-style: none;
}
.chain-company-card {
  background: linear-gradient(180deg, #ffffff, #fbfdff);
}
.chain-company-list li.chain-company-card {
  border: 1px solid #edf1f7;
  border-radius: 12px;
  padding: 12px;
}
.chain-company-list li.chain-company-card b {
  display: block;
  color: #1d2939;
  font-size: 13px;
}
.chain-company-list li.chain-company-card span {
  display: block;
  color: #526071;
  font-size: 12px;
  margin-top: 4px;
}
.chain-company-list li.chain-company-card small {
  display: block;
  color: var(--blue);
  font-size: 11px;
  font-weight: 800;
  margin-top: 6px;
}
.chain-company-head {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  align-items: start;
  margin-bottom: 10px;
}
.chain-company-head b { display: block; color: #1d2939; }
.chain-company-head span {
  display: block;
  color: var(--blue);
  font-size: 12px;
  font-weight: 800;
}
.chain-company-head small {
  color: var(--muted);
  font-size: 11px;
  text-align: right;
}
.chain-map {
  overflow-x: auto;
  margin: 18px 0;
  border: 1px solid var(--line);
  border-radius: 14px;
  background: #fbfcff;
  padding: 14px;
}
.chain-relationship-graph,
.chain-map-card,
.component-value-chain,
.bom-taxonomy,
.bottleneck-release-timeline,
.target-profit-bridge,
.target-valuation-table {
  margin: 20px 0;
  border: 1px solid rgba(10,132,255,.16);
  border-radius: 18px;
  background:
    linear-gradient(135deg, rgba(10,132,255,.08), transparent 38%),
    linear-gradient(225deg, rgba(29,154,108,.08), transparent 42%),
    #ffffff;
  padding: 16px;
}
.component-value-chain,
.bottleneck-release-timeline,
.target-profit-bridge,
.target-valuation-table {
  overflow-x: auto;
}
.bom-taxonomy > p {
  margin: 0 0 12px;
  color: #465365;
  font-size: 13px;
  line-height: 1.65;
}
.bom-taxonomy-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 10px;
}
.bom-taxonomy-card {
  border: 1px solid #edf1f7;
  border-radius: 12px;
  background: #fbfcff;
  padding: 12px;
}
.bom-taxonomy-card span {
  display: block;
  color: var(--blue);
  font-size: 11px;
  font-weight: 900;
  margin-bottom: 5px;
}
.bom-taxonomy-card strong {
  display: block;
  color: #27364a;
  font-size: 13px;
}
.bom-taxonomy-card p {
  margin: 5px 0 0;
  color: #526071;
  font-size: 12px;
  line-height: 1.55;
}
.component-value-chain table,
.bottleneck-release-timeline table,
.target-profit-bridge table,
.target-valuation-table table {
  min-width: 1180px;
}
.chain-company-network {
  margin: 20px 0;
  border: 1px solid rgba(10,132,255,.18);
  border-radius: 18px;
  background:
    linear-gradient(135deg, rgba(10,132,255,.08), transparent 38%),
    linear-gradient(225deg, rgba(29,154,108,.08), transparent 42%),
    #ffffff;
  padding: 16px;
}
/* ---- competition node cards ---- */
.competition-node-card {
  border: 1px solid rgba(10,132,255,.16);
  border-radius: 16px;
  background: #fbfcff;
  overflow: hidden;
  margin-bottom: 12px;
}
.competition-node-card > summary {
  display: grid;
  grid-template-columns: auto minmax(160px, .45fr) auto auto;
  gap: 10px;
  align-items: center;
  list-style: none;
  cursor: pointer;
  padding: 14px 16px;
}
.competition-node-card > summary::-webkit-details-marker { display: none; }
.competition-node-card[open] > summary { border-bottom: 1px solid rgba(10,132,255,.16); }
.competition-node-index {
  display: inline-flex;
  border-radius: 999px;
  background: #eef5ff;
  color: #0a84ff;
  border: 1px solid #d8e8ff;
  font-size: 11px;
  font-weight: 900;
  padding: 3px 8px;
}
.competition-node-card summary strong { color: #27364a; font-size: 14px; }
.competition-intensity {
  font-size: 11px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 999px;
}
.competition-low { background: #e6f7ec; color: #1d9a6c; }
.competition-midlow { background: #eef5ff; color: #0a84ff; }
.competition-mid { background: #fff3e0; color: #cc7a00; }
.competition-high { background: #ffeaea; color: #c0392b; }
.competition-node-body { padding: 14px; }
.competition-bom-map,
.chokepoint-bom-map {
  display: grid;
  gap: 12px;
}
.competition-question-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
  margin-bottom: 12px;
}
.chokepoint-question-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
  margin-bottom: 12px;
}
.overview-research-unit {
  border: 1px solid #d9e8fb;
  border-radius: 12px;
  background: linear-gradient(180deg, #fbfdff, #fff);
  padding: 12px;
  margin-bottom: 12px;
}
.overview-unit-head {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  align-items: center;
  margin-bottom: 10px;
}
.overview-unit-head b { color: #27364a; font-size: 13px; }
.overview-unit-head span { color: #667085; font-size: 12px; }
.competition-subcard {
  border: 1px solid #edf1f7;
  border-radius: 12px;
  background: #fff;
  padding: 12px;
  margin-bottom: 10px;
}
.overview-question-card {
  display: grid;
  gap: 8px;
}
.competition-subcard h4 {
  margin: 0 0 8px;
  font-size: 13px;
  color: #27364a;
}
.competition-subcard p {
  margin: 0;
  font-size: 12px;
  color: #4a5568;
  line-height: 1.55;
}
.overview-answer {
  border-top: 1px solid #edf1f7;
  padding-top: 8px;
}
.overview-answer-structured {
  display: grid;
  gap: 6px;
}
.overview-answer-row {
  display: grid;
  grid-template-columns: 74px 1fr;
  gap: 8px;
  border: 1px solid #edf1f7;
  border-radius: 9px;
  background: #fbfcff;
  padding: 7px 8px;
}
.overview-answer-row span {
  color: #0a63ce;
  font-size: 11px;
  font-weight: 900;
}
.overview-answer-row p {
  margin: 0;
  color: #344054;
  font-size: 12px;
  line-height: 1.55;
}
.overview-answer-sources { margin-top: 2px; }
.competition-subcard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}
.competition-subcard-item {
  background: #fbfcff;
  border: 1px solid #edf1f7;
  border-radius: 10px;
  padding: 8px 10px;
}
.competition-subcard-item.col-span { grid-column: span 2; }
.competition-subcard-item > span { display: block; font-size: 11px; color: #667085; margin-bottom: 3px; }
.competition-subcard-item > strong { display: block; font-size: 14px; color: #27364a; }
.competition-subcard-item > small { display: block; font-size: 11px; color: #8896a7; margin-top: 2px; }
.competition-subcard-item > p { margin: 0; font-size: 12px; color: #4a5568; line-height: 1.5; }
.profit-pool-flow { margin: 20px 0; }
.profit-pool-table,
.chokepoint-scorecard {
  border: 1px solid #d9e4f2;
  border-radius: 12px;
  background: #fff;
  padding: 12px;
}
.chokepoint-scorecard strong {
  display: block;
  color: #27364a;
  margin-bottom: 6px;
}
.chokepoint-scorecard p {
  margin: 0 0 5px;
  color: #526071;
  font-size: 12px;
  line-height: 1.55;
}
.profit-pool-flow .chain-graph-head { margin-bottom: 10px; }
.profit-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 700;
}
.profit-high { background: #e6f7ec; color: #1d9a6c; }
.profit-mid { background: #fff3e0; color: #cc7a00; }
.profit-low { background: #ffeaea; color: #c0392b; }
.profit-rationale { font-size: 12px; color: #667085; line-height: 1.45; max-width: 320px; }
/* ---- end competition node cards ---- */
.chain-network-canvas {
  overflow-x: auto;
  border: 1px solid var(--line);
  border-radius: 16px;
  background: #fbfcff;
  padding: 14px;
}
.chain-network-stage-grid {
  min-width: 960px;
  display: grid;
  grid-template-columns: repeat(3, minmax(260px, 1fr));
  gap: 14px;
}
.chain-network-stage {
  border: 1px solid rgba(217,224,234,.88);
  border-radius: 16px;
  background: rgba(255,255,255,.92);
  padding: 12px;
}
.chain-network-stage strong { color: #1d2939; }
.chain-network-stage p {
  min-height: 42px;
  margin: 6px 0 10px;
  color: var(--muted);
  font-size: 13px;
}
.chain-network-stage > div {
  display: grid;
  gap: 8px;
}
.chain-network-node {
  display: grid;
  gap: 2px;
  border: 1px solid #dbe7f5;
  border-radius: 12px;
  background: #ffffff;
  padding: 8px 10px;
}
.chain-network-node b { color: #1d2939; }
.chain-network-node small { color: var(--blue); font-weight: 800; }
.chain-network-edge-list {
  min-width: 960px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
  gap: 10px;
  margin-top: 14px;
}
.chain-network-edge-card {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr);
  gap: 8px;
  align-items: center;
  border: 1px solid #e2e8f2;
  border-radius: 14px;
  background: #ffffff;
  padding: 10px;
  color: #344054;
}
.chain-network-edge-card b { color: var(--green); font-size: 18px; }
.chain-network-edge-card small {
  grid-column: 1 / -1;
  color: var(--muted);
  font-size: 12px;
}
.chain-simple-flow {
  border: 1px solid #d8e6f7;
  border-radius: 12px;
  background: #f7fbff;
  padding: 12px;
  margin-bottom: 12px;
}
.simple-flow-head {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 10px;
}
.simple-flow-head b { color: #27364a; }
.simple-flow-head span {
  color: var(--muted);
  font-size: 12px;
}
.chain-simple-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 8px;
}
.chain-simple-step {
  border: 1px solid #e1e7f0;
  border-radius: 12px;
  background: #fff;
  padding: 10px;
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 8px;
  align-items: start;
}
.chain-simple-step > span {
  display: inline-flex;
  width: 26px;
  height: 26px;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  background: var(--blue);
  color: #fff;
  font-weight: 900;
  font-size: 12px;
}
.chain-simple-step b {
  display: block;
  color: #27364a;
  font-size: 13px;
  margin-bottom: 4px;
}
.chain-simple-step p {
  margin: 0;
  color: #344054;
  font-size: 12px;
  line-height: 1.55;
}
.chain-simple-step small {
  display: block;
  margin-top: 6px;
  color: var(--muted);
  font-size: 11px;
  line-height: 1.45;
}
.chain-value-guide {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
  margin-bottom: 12px;
}
.chain-value-guide div {
  border: 1px solid #e2e8f2;
  border-radius: 12px;
  background: #ffffff;
  padding: 10px;
}
.chain-value-guide b {
  display: block;
  color: #1d2939;
  font-size: 13px;
}
.chain-value-guide span {
  display: block;
  color: var(--muted);
  font-size: 12px;
  margin-top: 4px;
}
.chain-sankey-list {
  display: grid;
  gap: 12px;
}
.chain-sankey-flow {
  display: grid;
  gap: 10px;
  border: 1px solid #e2e8f2;
  border-radius: 14px;
  background: #ffffff;
  padding: 12px;
}
.flow-step {
  display: flex;
  align-items: center;
  gap: 10px;
}
.flow-step span {
  display: inline-flex;
  width: 32px;
  height: 28px;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: #eaf3ff;
  color: var(--blue);
  font-weight: 900;
}
.flow-step b { color: #1d2939; }
.flow-route {
  display: grid;
  grid-template-columns: minmax(160px, .9fr) minmax(260px, 1.4fr) minmax(160px, .9fr);
  gap: 10px;
  align-items: center;
}
.flow-from,
.flow-to {
  font-weight: 900;
  color: #1d2939;
  border: 1px solid #e7edf5;
  border-radius: 12px;
  background: #fbfcff;
  padding: 10px;
}
.flow-from small,
.flow-to small {
  display: block;
  color: var(--muted);
  font-size: 11px;
  font-weight: 800;
  margin-bottom: 4px;
}
.flow-band {
  min-height: calc(18px + var(--flow-weight, 3) * 4px);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  background: #2b6cb0;
  color: #ffffff;
  font-size: 12px;
  font-weight: 900;
  padding: 7px 12px;
  text-align: center;
}
.flow-demand .flow-band { background: #b7791f; }
.flow-feedback .flow-band { background: #667085; }
.flow-fields {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}
.flow-fields div {
  border: 1px solid #edf1f7;
  border-radius: 12px;
  background: #fbfcff;
  padding: 10px;
}
.flow-fields b {
  display: block;
  color: var(--blue);
  font-size: 12px;
  margin-bottom: 4px;
}
.flow-fields p {
  margin: 0;
  color: #526071;
  font-size: 12px;
}
.heat-score { text-align: center; }
.heat-score span {
  display: inline-flex;
  min-width: 30px;
  height: 26px;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  font-weight: 900;
}
.heat-high span { background: #e7f6ed; color: var(--green); }
.heat-mid span { background: #fff4d6; color: var(--amber); }
.heat-low span { background: #fee4e2; color: var(--red); }
.chain-graph-head {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: end;
  margin-bottom: 12px;
}
.chain-graph-title {
  margin: 0;
  font-size: 18px;
  font-weight: 800;
  color: #1d2939;
}
.table-scroll {
  max-width: 100%;
  overflow-x: auto;
  overflow-y: hidden;
  -webkit-overflow-scrolling: touch;
  border: 1px solid var(--line);
  border-radius: 14px;
  background: #fff;
}
.table-scroll table {
  width: max-content;
  min-width: 100%;
}
table { width: 100%; border-collapse: collapse; }
th, td { padding: 12px 14px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }
th { color: #475467; font-size: 13px; background: #f7f9fc; }
.chain-chokepoints {
  margin-top: 12px;
  padding: 12px 14px;
  border-radius: 14px;
  background: #f7f9fc;
  color: #344054;
}
.qa-stack, .child-stack { display: grid; gap: 14px; }
.qa-card { padding: 0; overflow: clip; }
.qa-card.level-4 { background: rgba(255,255,255,.76); border-style: dashed; }
.qa-card.level-5 { background: rgba(247,249,252,.92); border-style: dashed; }
.qa-card.level-4 > summary { padding-left: 28px; }
.qa-card.level-5 > summary { padding-left: 36px; }
.qa-card summary {
  cursor: pointer;
  display: grid;
  grid-template-columns: auto 1fr auto auto;
  gap: 12px;
  align-items: center;
  padding: 18px 20px;
  list-style: none;
}
.qa-card summary::-webkit-details-marker { display: none; }
.qid {
  display: inline-flex;
  min-width: 54px;
  justify-content: center;
  padding: 5px 9px;
  border-radius: 999px;
  background: #eaf3ff;
  color: var(--blue);
  font-weight: 700;
  font-size: 13px;
}
.question { font-weight: 700; }
.qa-count { color: var(--muted); font-size: 13px; }
.chevron { color: var(--blue); font-size: 24px; transition: transform .2s ease; }
.qa-card[open] > summary .chevron { transform: rotate(90deg); }
.qa-body { padding: 0 20px 20px; display: grid; gap: 14px; }
.qa-block {
  border: 1px solid rgba(217,224,234,.82);
  border-radius: 16px;
  background: rgba(255,255,255,.68);
  padding: 14px;
}
.block-title { margin: 0 0 10px; font-weight: 800; color: #334155; }
.artifact-card {
  border: 1px solid var(--line);
  border-radius: 14px;
  background: var(--surface-strong);
  padding: 14px;
  min-width: 0;
  max-width: 100%;
}
.artifact-title {
  margin: 0 0 8px;
  font-weight: 800;
  color: #334155;
}
.artifact-table-wrap {
  overflow-x: auto;
  margin-bottom: 14px;
  border: 1px solid rgba(217,224,234,.8);
  border-radius: 12px;
}
.artifact-table th {
  white-space: nowrap;
}
.artifact-table td {
  min-width: 120px;
  font-size: 13px;
}
.l3-meta { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 10px; }
.l3-meta span {
  padding: 5px 8px;
  border-radius: 999px;
  background: #f3f6fa;
  color: #475467;
  font-size: 12px;
}
.l3-artifact dl { display: grid; gap: 10px; margin: 0; }
.l3-artifact dl div { display: grid; grid-template-columns: 74px 1fr; gap: 10px; }
dt { color: var(--blue); font-weight: 800; }
dd { margin: 0; color: #344054; }
.source-links { margin: 10px 0 0; color: var(--muted); font-size: 13px; }
.target-odds-model {
  border: 1px solid var(--line);
  border-radius: 18px;
  background: rgba(255,255,255,.74);
  padding: 16px;
  margin: 18px 0;
  overflow-x: auto;
}
.target-odds-model h3 { margin: 0 0 6px; font-size: 18px; }
.target-odds-model p,
.target-profit-bridge p:not(.artifact-title),
.target-valuation-table p:not(.artifact-title) { margin: 0 0 12px; color: var(--muted); font-size: 14px; }
.target-table, .target-odds-table, .source-table { background: var(--surface-strong); overflow: hidden; }
.target-table, .target-odds-table { border-radius: 22px; }
.target-odds-table { min-width: 1500px; }
.state-actionable_long { color: var(--green); border-color: rgba(29,154,108,.28); background: #eaf8f2; }
.state-watch_only { color: var(--amber); border-color: rgba(183,121,31,.28); background: #fff7e6; }
.state-no_action { color: var(--red); border-color: rgba(194,65,61,.24); background: #fff1f0; }
.source-collapse { padding: 16px 18px; }
.source-collapse summary { cursor: pointer; font-weight: 800; color: #334155; }
.source-table { margin-top: 14px; }
@media (max-width: 760px) {
  .goal-card { grid-template-columns: 1fr; }
  .chain-bridge-grid,
  .chain-node-lens ul,
  .constraint-grid,
  .chain-qa-grid,
    .chain-value-guide,
  .space-summary-grid,
  .space-node-reasoning,
  .space-horizon-grid,
  .space-boundary-grid,
  .space-driver-tree,
  .space-model-grid,
  .space-evidence-grid,
  .key-variable-grid,
    .overview-answer-row,
  .competition-question-grid,
  .chokepoint-question-grid,
  .space-method-card-grid,
  .flow-route,
  .flow-fields { grid-template-columns: 1fr; }
  .space-node-card > summary { grid-template-columns: 1fr auto; }
  .space-node-label,
  .space-node-card summary strong,
  .space-node-card summary small { grid-column: 1 / 2; }
  .qa-card summary { grid-template-columns: auto 1fr auto; }
  .qa-count { grid-column: 2 / 3; }
  .target-table, .target-odds-table, .source-table, .chain-table { font-size: 13px; }
  .space-method-card { grid-template-columns: 1fr; }
  .space-method-card header {
    border-right: 0;
    border-bottom: 1px solid #edf1f7;
    padding-right: 0;
    padding-bottom: 8px;
  }
  .space-method-entry dl { grid-template-columns: 1fr; }
  th, td { padding: 10px; }
}
"""
