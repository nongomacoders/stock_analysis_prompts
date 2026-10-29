"""Offline logical capture previews; no model calls or production DB writes."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
from types import SimpleNamespace

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT));sys.stdout.reconfigure(encoding='utf-8')
def offline(event,args):
    if event in {'socket.connect','socket.getaddrinfo','socket.sendto'}:
        raise RuntimeError('Offline capture preview')
sys.addaudithook(offline)
import pdfplumber
from section_capture.capture_planner import inspect_page,plan_capture_groups,partition_detected_ranges
from section_capture.report_map import scan_report
from section_capture.pdf_source import extract_structured_text
from section_capture.section_matcher import extract_all_app_sections

HERE=Path(__file__).resolve().parent
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,obj):p.write_bytes((json.dumps(obj,indent=2,ensure_ascii=False)+'\n').encode('utf-8'))
database=ROOT/'documents/analysis.sqlite'
baseline=HERE/'preservation_baseline.json'
if not baseline.exists():save(baseline,dict(production_database_sha256=digest(database)))
paths=[('NTU',ROOT/'companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf'),
       ('DCP_AFS',ROOT/'companies/retail/DCP/sources/completed/FY26/1780031707-FY2026AnnualFinancialStatements.pdf'),
       ('PAN',ROOT/'companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf')]
summary=[]
for label,path in paths:
    original_hash=digest(path)
    with pdfplumber.open(path) as native:
        source=SimpleNamespace(path=path,filename=path.name,sha256=original_hash,plumber=native,page_count=len(native.pages),report_map=None)
        source.report_map=scan_report(source)
        detected=extract_all_app_sections(source,use_llm=False)
        ranges=partition_detected_ranges(detected,source.page_count)
        plans=[];legacy=[]
        for sec in ranges:
            captures=[];profiles=[]
            for p in range(sec['start_page'],sec['end_page']+1):
                captures.append(SimpleNamespace(page=p,text=extract_structured_text(native.pages[p-1])))
                profiles.append(inspect_page(source,p))
            for group in plan_capture_groups(captures,profiles):
                plans.append(dict(parent_heading=sec['title'],logical_heading=group['heading'] or sec['title'],
                  physical_pages=group['pages'],source_characters=sum(len(c.text) for c in group['captures']),
                  boundary_reason=group['start_reason'],continuation_cut=group['continuation_cut'],
                  continuation_reason=group['continuation_reason'],
                  heading_evidence=[dict(physical_page=c.page,**profile) for c,profile in zip(group['captures'],group['profiles'],strict=True)]))
            old=[];chars=0
            for cap in captures:
                if old and (len(old)>=12 or chars+len(cap.text)>24000):legacy.append([old[0],old[-1]]);old=[];chars=0
                old.append(cap.page);chars+=len(cap.text)
            if old:legacy.append([old[0],old[-1]])
        actual=[p for g in plans for p in range(g['physical_pages'][0],g['physical_pages'][1]+1)]
        assert actual==list(range(1,source.page_count+1))
        assert all(g['physical_pages'][1]-g['physical_pages'][0]+1<=6 for g in plans)
        assert digest(path)==original_hash
        result=dict(source=str(path.relative_to(ROOT)),sha256=original_hash,physical_page_count=source.page_count,
          legacy_budget_only_groups=len(legacy),logical_groups=len(plans),legacy_page_spans=legacy,
          all_pages_once=True,maximum_pages=max(b-a+1 for a,b in (g['physical_pages'] for g in plans)),
          forced_continuation_cuts=sum(g['continuation_cut'] for g in plans),groups=plans)
        save(HERE/(label+'_plan.json'),result)
        rows=[f'# {label} logical capture preview','',f'{source.page_count} physical pages; {len(plans)} proposed captures. All pages included exactly once. No model calls or financial conclusions.',
          '', '| Physical pages | Proposed topic | Source characters | Boundary | Continuation cut |', '|---|---|---:|---|---|']
        rows += [f'| {g["physical_pages"][0]}–{g["physical_pages"][1]} | {g["logical_heading"].replace("|","/")} | {g["source_characters"]} | {g["boundary_reason"]} | {g["continuation_cut"]} |' for g in plans]
        (HERE/(label+'_plan.md')).write_bytes(('\n'.join(rows)+'\n').encode('utf-8'))
        item={k:v for k,v in result.items() if k not in {'groups','legacy_page_spans'}};summary.append(item)
        print(json.dumps(item),flush=True)
save(HERE/'preview_summary.json',summary)
assert digest(database)==json.loads(baseline.read_text(encoding='utf-8'))['production_database_sha256']
print('Production DB and source PDFs unchanged; no paid calls.')
