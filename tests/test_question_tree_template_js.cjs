// Navigation unit test against a small DOM double, not a browser/screenshot test.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
function classes() {
  const values = new Set();
  return {add:k=>values.add(k), contains:k=>values.has(k), toggle(k, on) {
    on = on === undefined ? !values.has(k) : on;
    if(on) values.add(k); else values.delete(k);
    return on;
  }};
}
const listeners = new Map();
const globalEvents = new Map();
const scrolls = [];
function element(id, parent='') {
  return {id, dataset:{parentId:parent}, classList:classes(), attrs:{},
    setAttribute(k,v){this.attrs[k]=v}, removeAttribute(k){delete this.attrs[k]},
    scrollIntoView(){scrolls.push(id)}};
}
const parent = element('ROOT');
const child = element('ROOT.child','ROOT');
const articles = [parent,child];
const links = articles.map(a=>Object.assign(element('link-'+a.id), {hash:'#'+a.id, dataset:{nodeLink:a.id}}));
const section = Object.assign(element('analysis-ROOT.child'), {closest:s=>s==='.node-detail'?child:null});
const source = Object.assign(element('source-index'), {open:false, closest:()=>null});
const supplement = Object.assign(element('supplement'), {open:false, closest:s=>s==='details'?supplement:s==='.node-detail'?child:null});
const supportingAnchor = Object.assign(element('supporting-anchor'), {closest:s=>s==='details'?supplement:s==='.node-detail'?child:null});
const toggle = Object.assign(element('reading-mode'), {addEventListener:(name,fn)=>listeners.set('toggle:'+name,fn)});
const pane = {querySelectorAll:()=>articles};
const byId = new Map([parent,child,section,source,toggle,supplement,supportingAnchor].map(e=>[e.id,e]));
byId.set('detail-pane',pane);
for (const a of articles) a.closest=s=>s==='.node-detail'?a:null;
const document = {documentElement:{classList:classes()}, getElementById:id=>byId.get(id),
  querySelectorAll:s=>s==='details'?[source,supplement]:s==='.supplementary-analysis'?[supplement]:links, addEventListener:(name,fn)=>listeners.set(name,fn)};
const location = {hash:'#ROOT.child'};
const history = {pushState(_,__,hash){location.hash=hash}};
vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../src/value_invest_research/adapters/outbound/report_templates/question_tree_v1.js'),'utf8'),
  {document,location,history,matchMedia:()=>({matches:true}),addEventListener:(name,fn)=>globalEvents.set(name,fn)}, {timeout:1000});
assert(child.classList.contains('is-active'));
assert(document.documentElement.classList.contains('js-ready'));
assert.equal(links[1].attrs['aria-current'],'page');
function click(link) {listeners.get('click')({target:{closest:()=>link},button:0,preventDefault(){}})};
click(links[0]);
assert(parent.classList.contains('is-active'));
assert.equal(location.hash,'#ROOT');
click({hash:'#analysis-ROOT.child'});
assert(child.classList.contains('is-active'));
assert.equal(scrolls.at(-1),'analysis-ROOT.child');
location.hash='#ROOT';
globalEvents.get('popstate')();
assert(parent.classList.contains('is-active'));
listeners.get('toggle:click')();
assert(document.documentElement.classList.contains('show-all'));
assert.equal(supplement.open,true);
listeners.get('toggle:click')();
assert(!document.documentElement.classList.contains('show-all'));
click({hash:'#source-index'});
assert.equal(source.open,true);
source.open=false;
supplement.open=false;
globalEvents.get('beforeprint')();
assert.equal(source.open,true);
assert.equal(supplement.open,true);
globalEvents.get('afterprint')();
assert.equal(source.open,false);
assert.equal(supplement.open,false);
click({hash:'#supporting-anchor'});
assert.equal(supplement.open,true);
assert(child.classList.contains('is-active'));
location.hash='#%ZZ';
globalEvents.get('hashchange')();
assert(child.classList.contains('is-active'));
console.log('PASS: deep link, selected node, ancestor path, section jump, history, full reading, source index, print, invalid hash');
