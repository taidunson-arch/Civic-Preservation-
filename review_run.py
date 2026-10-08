#!/usr/bin/env python3
"""Validate a completed run and produce an offline, read-only agency review desk."""
from __future__ import annotations
import argparse
import base64
import csv
import hashlib
import html
import json
import os
from pathlib import Path
import sqlite3
from datetime import date, datetime, timezone

AXES = ('preservation_urgency', 'financial_risk', 'data_confidence', 'intervention_readiness')
SEAL = 'review-integrity.json'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def read_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f'duplicate JSON key: {key}')
            result[key] = value
        return result
    def invalid(value):
        raise ValueError(f'non-finite JSON value: {value}')
    return json.loads(path.read_text(encoding='utf-8-sig'), object_pairs_hook=pairs, parse_constant=invalid)

def index(rows, label):
    result = {}
    if not isinstance(rows, list):
        raise ValueError(f'{label} must be a list')
    for row in rows:
        pid = row.get('property_id')
        if not isinstance(pid, str) or not pid.strip() or pid in result:
            raise ValueError(f'{label}: missing or duplicate property identity')
        result[pid] = row
    return result

def inventory(root):
    result = {}
    for path in sorted(root.rglob('*')):
        if path.is_symlink() or getattr(path, 'is_junction', lambda: False)():
            raise ValueError('linked files/directories are not allowed in a sealed run')
        if path.is_file() and path.relative_to(root).as_posix() != SEAL:
            result[path.relative_to(root).as_posix()] = digest(path.read_bytes())
    return result

def load_run(root):
    root = Path(root).resolve(strict=True)
    inventory(root)  # Reject links before reading artifacts.
    manifest = read_json(root / 'manifest.json')
    if manifest.get('status') != 'COMPLETE' or not manifest.get('run_id') or (root / 'failure.json').exists():
        raise ValueError('review requires a completed, successful run')
    result = read_json(root / 'result.json')
    if manifest['as_of_date'] != result['run']['as_of_date']:
        raise ValueError('manifest/result dates disagree')
    date.fromisoformat(manifest['as_of_date'])
    leads = index(result['leads'], 'result leads')
    risks = index(result['risk_dimensions'], 'result risks')
    with (root / 'risk_dimensions.csv').open(encoding='utf-8-sig', newline='') as stream:
        csv_risks = index(list(csv.DictReader(stream)), 'CSV risks')
    if set(leads) != set(risks) or set(risks) != set(csv_risks):
        raise ValueError('property populations disagree across result and risk CSV')
    for pid, risk in risks.items():
        for axis in AXES:
            value = risk.get(axis)
            if not isinstance(value, str) or not value.strip() or value != csv_risks[pid].get(axis) or value != leads[pid].get(axis):
                raise ValueError(f'{pid}: missing or inconsistent {axis}')
    with (root / 'events.csv').open(encoding='utf-8-sig', newline='') as stream:
        events = list(csv.DictReader(stream))
    result['review_source_events'] = events
    actual_counts = {axis: {v: sum(r[axis] == v for r in risks.values()) for v in sorted({r[axis] for r in risks.values()})} for axis in AXES}
    if actual_counts != result.get('dimension_counts'):
        raise ValueError('dimension counts disagree with property assessments')
    return root, manifest, result

def seal_run(root):
    root, manifest, _ = load_run(root)
    path = root / SEAL
    # A seal is a baseline, never an implicit way to bless changed outputs.
    if path.exists():
        verify_run(root)
        return path
    seal = {'schema_version': 1, 'run_id': manifest['run_id'], 'created_at': datetime.now(timezone.utc).isoformat(),
            'files': inventory(root), 'scope': 'Local change detection; not a digital signature or agency acceptance.'}
    with path.open('x', encoding='utf-8') as stream:
        json.dump(seal, stream, indent=2, sort_keys=True)
    return path

def verify_run(root):
    root, manifest, result = load_run(root)
    seal = read_json(root / SEAL)
    if seal.get('schema_version') != 1 or seal.get('run_id') != manifest['run_id'] or seal.get('files') != inventory(root):
        raise ValueError('run integrity mismatch: files changed, added, or removed after sealing')
    return root, manifest, result

def case_snapshot(db_path, manifest):
    if db_path is None:
        return None
    path = Path(db_path).resolve(strict=True)
    db = sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)
    db.row_factory = sqlite3.Row
    try:
        db.execute('BEGIN')
        stored = db.execute('SELECT manifest FROM runs WHERE run_id=?', (manifest['run_id'],)).fetchone()
        if stored is None or json.loads(stored[0]) != manifest:
            raise ValueError('case database does not match this run manifest')
        # Include persistent cases for this run population, including cases originating in older runs.
        rows = db.execute('SELECT c.* FROM cases c JOIN properties p ON p.property_id=c.property_id WHERE p.run_id=? ORDER BY c.due_date,c.case_id', (manifest['run_id'],)).fetchall()
        return [dict(row) for row in rows]
    finally:
        db.close()

STYLE = '''
:root{font-family:Segoe UI,Arial,sans-serif;color:#173139;background:#edf2f2;font-size:15px}*{box-sizing:border-box}body{margin:0}header{background:#123c43;color:white;padding:30px 5vw}header small{letter-spacing:.16em;color:#adced0}h1{font-size:34px;margin:12px 0}h2{font-size:21px}p{line-height:1.55}main{max-width:1500px;margin:auto;padding:24px 4vw}.banner{border-left:5px solid #b96c18;padding:16px 20px;background:#fff3dd;margin-bottom:20px}.meta{color:#c7dddf}.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}.card{background:white;padding:20px;border:1px solid #cedadb;border-radius:8px}.card strong{font-size:29px;display:block;margin:8px 0}.muted{color:#50676d}.tools{display:flex;gap:15px;flex-wrap:wrap;align-items:end;margin:24px 0}label{display:grid;gap:6px;font-weight:600}input,select,button{font:inherit;padding:10px;border:1px solid #92aaad;border-radius:5px;background:white;color:#173139}button{cursor:pointer}button:hover,button:focus-visible{background:#d5ebeb;outline:2px solid #16727c}table{border-collapse:collapse;width:100%;background:white}th,td{text-align:left;padding:13px 12px;border-bottom:1px solid #dce5e6;vertical-align:top}th{font-size:12px;text-transform:uppercase;letter-spacing:.04em;background:#e2ebec}.scroll{overflow:auto;border:1px solid #cedadb;border-radius:7px}.pill{display:inline-block;font-size:11px;font-weight:700;padding:5px 7px;border-radius:4px;background:#e9eff0}.danger{background:#fbe1dc;color:#812f21}.unknown{background:#fff0ce;color:#775319}.detail{background:white;padding:24px;margin-top:22px;border:1px solid #b8cdcf;border-radius:8px}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f0f5f5;padding:16px;font-size:12px}summary{cursor:pointer;padding:12px 0;font-weight:600}footer{font-size:12px;padding:28px 0;color:#50676d}@media(max-width:850px){.cards{grid-template-columns:repeat(2,1fr)}h1{font-size:28px}}@media print{.tools,button{display:none}.scroll{overflow:visible}header{color:#173139;background:white}.cards{display:block}}
'''
SCRIPT = '''
const data=JSON.parse(document.getElementById('payload').textContent);
const $=id=>document.getElementById(id);
const text=(tag,value,cls)=>{const n=document.createElement(tag);n.textContent=String(value??'Unknown');if(cls)n.className=cls;return n};
const badge=value=>text('span',value,'pill '+(/OVERDUE|CRITICAL|DISTRESS|BLOCKED/.test(value)?'danger':/UNKNOWN|VERIFY|WATCH/.test(value)?'unknown':''));
const pretty=value=>JSON.stringify(value,null,2);
const risks=new Map(data.result.risk_dimensions.map(r=>[r.property_id,r]));
const cases=data.cases||[];
const laneLabels={preservation_urgency:'Preservation urgency',financial_risk:'Financial condition',data_confidence:'Data confidence',intervention_readiness:'Intervention readiness'};
const reasons={preservation_urgency:'preservation_reasons',financial_risk:'financial_reasons',data_confidence:'data_confidence_reasons',intervention_readiness:'readiness_reasons'};
function smallTable(rows,columns){const wrap=text('div','','scroll'),table=document.createElement('table'),head=document.createElement('tr');for(const [,label] of columns){const th=text('th',label);th.scope='col';head.append(th)}table.append(head);for(const row of rows){const tr=document.createElement('tr');for(const [key] of columns)tr.append(text('td',row[key]||'Unknown'));table.append(tr)}if(!rows.length){wrap.append(text('p','No records supplied.'))}else wrap.append(table);return wrap}
function dateCell(value,basis){const td=text('td',value||'Unknown');td.append(text('p',value?(basis||'Basis not supplied'):'No confirmed date','muted'));return td}
function cliffBasis(row){const matches=data.result.review_source_events.filter(e=>e.property_id===row.property_id&&e.event_type===row.owner_cliff_type&&e.event_date===row.owner_cliff_date);return [...new Set(matches.map(e=>e.basis).filter(Boolean))].join(' / ')}
for(const [key,label] of Object.entries(laneLabels)){const o=text('option',label);o.value=key;$('axis').append(o)}
function values(){const select=$('value');select.replaceChildren(text('option','All assessments'));select.firstChild.value='';for(const v of [...new Set([...risks.values()].map(r=>r[$('axis').value]))].sort()){const o=text('option',v);o.value=v;select.append(o)}render()}
function inspect(row){const d=$('detail');d.replaceChildren(text('h2',row.property_name||row.property_id),text('p',row.property_id,'muted'));const risk=risks.get(row.property_id);for(const [k,label] of Object.entries(laneLabels)){d.append(text('h3',label),badge(risk[k]),text('p',risk[reasons[k]]||'No explanation supplied'))}d.append(text('h3','Case responsibilities'),smallTable(cases.filter(c=>c.property_id===row.property_id),[['status','Status'],['assigned_to','Assigned to'],['original_due_date','Original obligation'],['due_date','Work due'],['version','Version']]));for(const [label,obj] of [['Assessment reasons and evidence',risk],['Property source fields',row],['Source events',data.result.review_source_events.filter(x=>x.property_id===row.property_id)],['Agency calendar',data.result.agency_calendar.filter(x=>x.property_id===row.property_id)],['Instrument positions',data.result.instruments.filter(x=>x.property_id===row.property_id)],['Case snapshot',data.cases===null?'Case database not supplied':cases.filter(x=>x.property_id===row.property_id)]]){const block=document.createElement('details');block.append(text('summary',label),text('pre',pretty(obj)));d.append(block)}d.hidden=false;d.focus();}
function render(){const query=$('search').value.toLowerCase();const list=data.result.leads.filter(r=>(r.property_id+' '+r.property_name).toLowerCase().includes(query)&&(!$('value').value||risks.get(r.property_id)[$('axis').value]===$('value').value));list.sort((a,b)=>((a.agency_action_date_override||a.agency_action_date)||'9999').localeCompare((b.agency_action_date_override||b.agency_action_date)||'9999')||(a.owner_cliff_date||'9999').localeCompare(b.owner_cliff_date||'9999')||a.property_id.localeCompare(b.property_id));$('rows').replaceChildren();for(const r of list){const tr=document.createElement('tr'),first=document.createElement('td'),button=text('button',r.property_name||r.property_id);button.addEventListener('click',()=>inspect(r));first.append(button,text('p',r.property_id,'muted'));tr.append(first);tr.append(dateCell((r.agency_action_date_override||r.agency_action_date),r.agency_action_basis),dateCell(r.owner_cliff_date,cliffBasis(r)));for(const k of Object.keys(laneLabels)){const td=document.createElement('td');td.append(badge(risks.get(r.property_id)[k]));tr.append(td)}const states=cases.filter(c=>c.property_id===r.property_id).map(c=>c.status);tr.append(text('td',data.cases===null?'Not connected':[...new Set(states)].map(s=>s+' ('+states.filter(x=>x===s).length+')').join(', ')||'No recorded case'));$('rows').append(tr)}$('count').textContent=`${list.length} of ${data.result.leads.length} properties`;if(!list.length){const tr=document.createElement('tr'),td=text('td','No properties match these filters.');td.colSpan=8;tr.append(td);$('rows').append(tr)}}
$('search').addEventListener('input',render);$('axis').addEventListener('change',values);$('value').addEventListener('change',render);values();
'''

def render_review(root, out, db_path=None, demo=False):
    root, manifest, result = verify_run(root)
    out = Path(out).resolve()
    if out == root or root in out.parents:
        raise ValueError('save review outside the sealed run directory')
    cases = case_snapshot(db_path, manifest)
    payload = json.dumps({'result': result, 'cases': cases}, ensure_ascii=True, allow_nan=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    def csp_hash(value):
        return 'sha256-' + base64.b64encode(hashlib.sha256(value.encode()).digest()).decode()
    esc = lambda value: html.escape(str(value), quote=True)
    n = len(result['leads'])
    unknown = sum(r['financial_risk'] == 'UNKNOWN' for r in result['risk_dimensions'])
    urgent = sum(r['preservation_urgency'] in ('OVERDUE', 'CRITICAL', 'URGENT') for r in result['risk_dimensions'])
    active = 'Not connected' if cases is None else str(sum(c['status'] not in ('CLOSED', 'CANCELLED') for c in cases))
    banner = 'SYNTHETIC DEMONSTRATION — not an agency portfolio. ' if demo else ''
    banner += 'Agency acceptance not established by this review. Verify source documents and applicable rules before action.'
    if result['run'].get('degraded'):
        banner += ' DEGRADED RUN: ' + result['run'].get('degraded_reason', '')
    document = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src '{csp_hash(SCRIPT)}'; style-src '{csp_hash(STYLE)}'; base-uri 'none'; form-action 'none'; connect-src 'none'"><title>CivicPreserve | Agency review</title><style>{STYLE}</style></head><body><header><small>CIVICPRESERVE / AGENCY REVIEW DESK</small><h1>Preservation starts with evidence.</h1><p class="meta">As of {esc(manifest['as_of_date'])} · {esc(manifest.get('market_id'))} · Run {esc(manifest['run_id'])}</p></header><main><div class="banner">{esc(banner)}</div><div class="cards"><section class="card">Properties in this run<strong>{n}</strong><span class="muted">Count is not proof of full book coverage</span></section><section class="card">Urgent preservation<strong>{urgent}</strong><span class="muted">Overdue, critical, or urgent</span></section><section class="card">Financial condition unknown<strong>{unknown}</strong><span class="muted">Missing information stays visible</span></section><section class="card">Open cases<strong>{esc(active)}</strong><span class="muted">Current database snapshot at export</span></section></div><h2>Agency intervention queue</h2><p>Agency act-by first, then owner cliff. Select a property to inspect evidence, positions and cases.</p><div class="tools"><label>Property search<input id="search" type="search" placeholder="Name or property ID"></label><label>Risk dimension<select id="axis"></select></label><label>Assessment<select id="value"></select></label><span id="count" role="status" aria-live="polite"></span></div><div class="scroll"><table><thead><tr><th scope="col">Property</th><th scope="col">Agency act-by</th><th scope="col">Owner cliff</th><th scope="col">Preservation</th><th scope="col">Financial</th><th scope="col">Confidence</th><th scope="col">Readiness</th><th scope="col">Cases</th></tr></thead><tbody id="rows"></tbody></table></div><section id="detail" class="detail" tabindex="-1" hidden aria-label="Property details"></section><details class="detail"><summary>Run provenance and review limitations</summary><p>Local integrity baseline verified before export. Checksums detect changes relative to that baseline; they do not authenticate the publisher. This file contains the run's data and is an internal working document, not a redacted public packet. Case states are a snapshot, not a live service.</p><pre>{esc(json.dumps({'run':result['run'], 'summary':result['summary'], 'exported_at':datetime.now(timezone.utc).isoformat()}, indent=2))}</pre></details><footer>Offline review · No external scripts, fonts, analytics or network calls · Decisions and case changes remain in the authorized agency workflow.</footer></main><script id="payload" type="application/json">{payload}</script><script>{SCRIPT}</script></body></html>'''
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('x', encoding='utf-8') as stream:
        stream.write(document)
    return out

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('seal', 'verify', 'review'):
        command = sub.add_parser(name)
        command.add_argument('--run-dir', required=True)
        if name == 'review':
            command.add_argument('--out', required=True)
            command.add_argument('--db')
            command.add_argument('--demo', action='store_true')
    args = parser.parse_args()
    try:
        if args.command == 'seal':
            print(seal_run(args.run_dir))
        elif args.command == 'verify':
            _, manifest, _ = verify_run(args.run_dir)
            print('Verified local integrity baseline: ' + manifest['run_id'])
        else:
            print(render_review(args.run_dir, args.out, args.db, args.demo))
    except (ValueError, KeyError, TypeError, OSError, sqlite3.Error) as exc:
        parser.exit(2, f'Review rejected: {exc}\n')

if __name__ == '__main__':
    main()
