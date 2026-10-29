"""Reviewed NTU capture plan, bounded paid pilot, then chronological isolated rerun."""
from collections import Counter
import copy
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sqlite3
import sys

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT));sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent
ENGINE=ROOT/'workflow/changes/20261028_ntu_default_run/rerun.py'
spec=importlib.util.spec_from_file_location('ntu_engine',ENGINE);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
PARENT=ROOT/'companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T114521Z_deepseek_default_no_requested_cap'
POINTER=HERE/'trial_run.txt'

base_compact=m.compact_section_prompt
def compact(manifest,texts,questions,rules):
    coverage={k:v for k,v in (manifest.get('capture_coverage') or {}).items() if k!='heading_observations'}
    topics=[dict(physical_page=p['physical_page'],heading=h['text'])
       for p in (manifest.get('capture_coverage') or {}).get('heading_observations',[])
       for h in p.get('heading_evidence',[]) if re.match(r'^\d+(?:\.\d+)*\s+[A-Za-z]',h['text'])]
    return base_compact(manifest,texts,questions,rules)+'\n\nCAPTURE BOUNDARIES (not proof of disclosure completeness):\n'+json.dumps(coverage,ensure_ascii=False)+'\nOBSERVED NOTE HEADINGS, INCLUDING STARTS LOWER ON SHARED PAGES:\n'+json.dumps(topics,ensure_ascii=False)+'''\nThe brief covers ALL supplied financial content, not only the named main topic or selected questions.
Mention secondary note starts and their material facts; carry their continuation Pending to the named next pages.
Do not call an entire capture "table only" when a second note also starts on that page.
For ledger evidence prefer a short 8–50 character verbatim locator from the supplied text, not an entire reconstructed table row.
Calculations belong in the answer with physical pages; never fabricate quote characters to reproduce a table.
Use only evidence actually supplied.'''
m.compact_section_prompt=compact

def include_resolved_index(database,manifest):
    from section_capture import question_ledger
    with sqlite3.connect(database) as c:
        resolved=[dict(question_id=q['question_id'],question=q['question'][:160])
                  for q in question_ledger.records(c,m.SHA) if q['status']=='resolved']
    if not resolved:return ''
    return '\nRESOLVED QUESTION INDEX (not new evidence): '+json.dumps(resolved,ensure_ascii=False)+'\nDo not recreate these as new questions. Reopen only for identified new contradictory evidence, preserving the original ID.'

def scope_recheck(run):
    from section_capture import db,question_ledger
    from section_capture.packages import extract_selection_texts
    p=run/'pilot';database=p/'experiment.sqlite';db.DB_PATH=database
    sec=next(s for s in db.list_sections(m.SHA,database) if s.manifest['capture_coverage']['chunk_pages']==[25,25])
    with db.connect_db(database) as c:records=question_ledger.records(c,m.SHA)
    manifest=copy.deepcopy(sec.manifest)
    questions=question_ledger.render_prompt(records,context=manifest,limit=2)
    prompt=compact(manifest,extract_selection_texts(manifest,sec.selected_text,sec.prompt),questions,m.read(p/'inputs/guardrails.json'))+include_resolved_index(database,manifest)
    answer,r=m.call(p,'page25_scope_recheck_v2',prompt,None)
    with db.connect_db(database) as c:c.execute('UPDATE sections SET prompt=? WHERE package_id=?',(prompt,sec.package_id))
    saved,_=db.save_section_llm_response(sec.package_id,answer,model=m.MODEL,tokens=r['usage'],db_path=database)
    assert saved.manifest['review']['ledger_validation']=='valid','Scope recheck ledger invalid; stop before full rerun'
    m.summarize(p);m.preserve(p);m.preserve(run)

def prepare():
    from PySide6.QtCore import QRectF
    from section_capture import db,question_ledger,report_map
    from section_capture.pdf_source import PdfSource
    from section_capture.packages import save_package
    run=PARENT.parent/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_deepseek_reviewed_logical')
    run.mkdir(exist_ok=False)
    for name in ['inputs','outputs','requests','receipts','gemini']:(run/name).mkdir()
    prior=m.read(PARENT/'plan.json');database=run/'experiment.sqlite'
    old=m.ro(PARENT/'experiment.sqlite');c=sqlite3.connect(database);old.backup(c);old.close()
    for table in ['sections','ledger_questions','ledger_events','section_response_attempts']:c.execute('DELETE FROM '+table)
    cols=[r[1] for r in c.execute('PRAGMA table_info(reports)')]
    clear=[x for x in cols if x.startswith(('stage1_','stage2_')) or x in {'target_price_zar','reference_price_zar','recommendation','upside_pct','dividend_yield_pct','tsr_pct','monitoring_triggers','valuation_summary_json','report_map_json'}]
    c.execute('UPDATE reports SET '+','.join('"'+x+'"=NULL' for x in clear)+",questions_ledger=''")
    prod=m.ro(ROOT/'documents/analysis.sqlite');prod.row_factory=sqlite3.Row
    rules=[dict(r) for r in prod.execute('SELECT * FROM sector_guardrails ORDER BY rule_code')]
    hashes=m.snap(prod);backup=sqlite3.connect(run/'inputs/production_snapshot.sqlite');prod.backup(backup);backup.close();prod.close()
    c.execute('DELETE FROM sector_guardrails')
    for r in rules:c.execute('INSERT INTO sector_guardrails ('+','.join(r)+') VALUES ('+','.join('?' for _ in r)+')',tuple(r.values()))
    for i,(target,q,closure) in enumerate(m.QUESTIONS,1):
        question_ledger.store(c,m.SHA,m.SHA,dict(question_id=f'Q-NTU-DEFAULT-{i:02d}',question=q,priority='high',
          target_document=prior['documents'][0]['filename'],target_section=target,evidence_required=closure,closure_condition=closure,
          status='open',answer='',evidence=[]),None,m.utc())
    c.execute('UPDATE reports SET questions_ledger=?',(question_ledger.render(question_ledger.records(c,m.SHA)),));c.commit();c.close()
    db.DB_PATH=database;report_map.CACHE_ROOT=database;report_map.QUESTIONS_ROOT=database
    automatic=m.read(HERE/'NTU_plan.json')['groups']
    joins={(9,11):'Income, comprehensive income and equity movements',
           (18,19):'Loss per share — total, continuing and discontinued',
           (27,29):'Fair-value measurement, methods and Level3 rollforward',
           (37,38):'Company information and back cover'}
    reviewed=[];skip=set()
    for original in automatic:
        start,end=original['physical_pages']
        if start in skip:continue
        matched=next(((a,b,title) for (a,b),title in joins.items() if a==start),None)
        if matched:
            a,b,title=matched;members=[g for g in automatic if a<=g['physical_pages'][0]<=b]
            assert [p for g in members for p in range(g['physical_pages'][0],g['physical_pages'][1]+1)]==list(range(a,b+1))
            item=copy.deepcopy(original);item.update(logical_heading=title,physical_pages=[a,b],
               source_characters=sum(g['source_characters'] for g in members),
               heading_evidence=[p for g in members for p in g['heading_evidence']],
               continuation_cut=members[-1]['continuation_cut'],continuation_reason=members[-1]['continuation_reason'],
               review_reason='Small related disclosures kept together after review; source text unchanged.')
            skip.update(g['physical_pages'][0] for g in members[1:])
        else:item=copy.deepcopy(original)
        if item['physical_pages']==[30,31]:item['logical_heading']='Segment results and core reconciliation — H1 2026'
        if item['physical_pages']==[32,33]:item['logical_heading']='Segment results and core reconciliation — H1 2025'
        if item['physical_pages']==[34,35]:item['logical_heading']='Segment results and core reconciliation — FY2025'
        item['analysis_role']='navigation_only' if item['physical_pages'] in [[1,2],[37,38]] else 'financial_analysis'
        reviewed.append(item)
    assert len(reviewed)==24 and sum(g['analysis_role']=='financial_analysis' for g in reviewed)==22
    assert [p for g in reviewed for p in range(g['physical_pages'][0],g['physical_pages'][1]+1)]==list(range(1,39))
    source=PdfSource(prior['documents'][0]['path']);source.report_map=report_map.scan_report(source)
    spans=[g['physical_pages'] for g in reviewed]
    try:
        for i,g in enumerate(reviewed):
            a,b=g['physical_pages'];captures=[]
            for p in range(a,b+1):
                w,h=source.size(p);cap=source.capture_area(p,QRectF(0,0,w,h))
                cap.content_type='table' if cap.text.count('|')>=4 else 'financial_note'
                if g['continuation_cut']:cap.warnings.append('A note starts on a shared page and may continue in the neighboring capture.')
                captures.append(cap)
            coverage=dict(planner='reviewed_native_logical_v1',parent_heading=g['parent_heading'],logical_heading=g['logical_heading'],
              requested_pages=[a,b],actual_document_range=[a,b],chunk_pages=[a,b],chunks=spans,chunk_index=i+1,chunk_count=len(spans),
              previous_chunk_pages=spans[i-1] if i else None,next_chunk_pages=spans[i+1] if i+1<len(spans) else None,
              continuation_cut=g['continuation_cut'],continuation_reason=g['continuation_reason'],source_characters=sum(len(cap.text) for cap in captures),
              heading_observations=g['heading_evidence'],review_reason=g.get('review_reason','Native logical boundary retained after review.'))
            saved=save_package(source=source,heading=g['logical_heading'],subheading=g['logical_heading'],
              question='Analyze the supplied logical unit and relevant ledger questions; respect adjacent-note dependencies.',
              captures=captures,output_root=database,sector='consumer_lending',ledger_contract=1,capture_coverage=coverage)
            with db.connect_db(database) as c:
                manifest=json.loads(c.execute('SELECT manifest_json FROM sections WHERE package_id=?',(saved.package_id,)).fetchone()[0])
                manifest['analysis_role']=g['analysis_role'];c.execute('UPDATE sections SET manifest_json=? WHERE package_id=?',(json.dumps(manifest,ensure_ascii=False),saved.package_id))
    finally:source.close()
    for name in ['source_pages.json','codex_review.md']:shutil.copy2(PARENT/'inputs'/name,run/'inputs'/name)
    m.save(run/'inputs/guardrails.json',rules);m.save(run/'inputs/reviewed_plan.json',reviewed)
    originals=[dict(path=str(p),sha256=m.sha(p)) for folder in ['outputs','requests','receipts'] for p in (PARENT/folder).iterdir() if p.is_file()]
    plan=dict(prior,created_utc=m.utc(),parent_run=str(PARENT),authorization='User approved plan review, small difficult-section pilot, then full chronological NTU rerun if pilot succeeds; Gemini remains manual Antigravity.',
      production_table_hashes=hashes,original_files=originals,section_prompt_revision='uncapped_v4',questions_per_capture=2,
      budgets=dict(section=None,stage1=None,stage2=None),planned_calls=24,
      design='Reviewed24-unit logical plan;22 analytical units,2 navigation units captured without standalone calls. Three-call independent pilot before full chronological run; no causal one-variable benchmark.',
      continue_with_explicit_failed_section_source=False,pilot_pages=[[21,23],[24,24],[25,25]],pilot_gate='All3 finish; literal ledger valid after at most one repair; independent POCI/sign/period/ECL-scope checks; stop broad trial on a failure.')
    m.save(run/'plan.json',plan);m.save(run/'status.json',dict(status='prepared',stage='not_started',calls=0))
    for label,src in [('transport_engine.py',ENGINE),('trial_driver.py',Path(__file__))]:shutil.copy2(src,run/'inputs'/label)
    pilot=run/'pilot';pilot.mkdir()
    for name in ['inputs','outputs','requests','receipts']:(pilot/name).mkdir()
    for name in ['guardrails.json','source_pages.json']:shutil.copy2(run/'inputs'/name,pilot/'inputs'/name)
    src=m.ro(database);dest=sqlite3.connect(pilot/'experiment.sqlite');src.backup(dest);src.close();dest.close()
    m.save(pilot/'plan.json',plan);m.save(pilot/'status.json',dict(status='prepared',stage='not_started',calls=0))
    rows=['# NTU reviewed logical capture plan','', '24 units;22 analytical calls plus2 navigation-only units. Full38-page coverage. Pilot is separate; full run starts with a fresh ledger.','', '| Pages | Reviewed unit | Role |', '|---|---|---|']
    rows += [f'| {g["physical_pages"][0]}–{g["physical_pages"][1]} | {g["logical_heading"]} | {g["analysis_role"]} |' for g in reviewed]
    m.text(run/'REVIEWED_PLAN.md','\n'.join(rows)+'\n');m.text(POINTER,str(run));m.preserve(run)
    print(json.dumps(dict(run=str(run),capture_units=24,analysis_calls=22,pilot_calls=3,stages=2,full_calls=24)))

def pilot(run):
    from section_capture import db,question_ledger
    from section_capture.packages import extract_selection_texts
    p=run/'pilot';database=p/'experiment.sqlite';db.DB_PATH=database
    sections=db.list_sections(m.SHA,database);rules=m.read(p/'inputs/guardrails.json')
    checks=[];repairs=0
    try:
        for index,sec in enumerate(sections,1):
            pages=sec.manifest['capture_coverage']['chunk_pages']
            if pages not in [[21,23],[24,24],[25,25]]:continue
            manifest=copy.deepcopy(sec.manifest)
            with db.connect_db(database) as c:records=question_ledger.records(c,m.SHA)
            questions=question_ledger.render_prompt(records,context=manifest,limit=2)
            prompt=compact(manifest,extract_selection_texts(manifest,sec.selected_text,sec.prompt),questions,rules)
            with db.connect_db(database) as c:c.execute('UPDATE sections SET manifest_json=?,prompt=? WHERE package_id=?',(json.dumps(manifest,ensure_ascii=False),prompt,sec.package_id))
            label=f'section_{index:02d}_uncapped_v4'
            answer,r=m.call(p,label,prompt,None)
            saved,_=db.save_section_llm_response(sec.package_id,answer,model=m.MODEL,tokens=r['usage'],cost_usd=r['cost_usd'],response_time_seconds=r['elapsed_seconds'],db_path=database)
            if saved.manifest['review']['ledger_validation']!='valid':
                if repairs>=1:raise RuntimeError('Pilot required more than one ledger repair; stop for diagnosis')
                errors=saved.manifest['review']['ledger_errors'];m.save(p/'outputs'/f'{label}.validation.json',errors)
                request=prompt+'\nReturn only one corrected fenced ledger JSON. Use short exact excerpts and existing IDs; omit unsupported updates rather than forcing closure.\nPrevious answer:\n'+answer+'\nErrors:\n'+json.dumps(errors)
                fixed,rr=m.call(p,label+'_repair',request,None);repairs+=1
                payloads=[json.loads(b) for b in re.findall(r'```json\s*\n(.*?)```',fixed,re.S|re.I)]
                assert len(payloads)==1 and payloads[0].get('ledger_version')==1
                def replace(match):
                    value=json.loads(match.group(1))
                    return '```json\n'+json.dumps(payloads[0],ensure_ascii=False)+'\n```' if isinstance(value,dict) and 'ledger_version' in value else match.group(0)
                effective=re.sub(r'```json\s*\n(.*?)```',replace,answer,flags=re.S|re.I)
                m.text(p/'outputs'/f'{label}.effective.md',effective)
                saved,_=db.save_section_llm_response(sec.package_id,effective,model=m.MODEL,tokens=rr['usage'],db_path=database)
                if saved.manifest['review']['ledger_validation']!='valid':raise RuntimeError('Pilot ledger repair rejected')
            checks.append(dict(label=label,physical_pages=pages,ledger_valid=True,completed=True))
        m.save(p/'pilot_execution.json',dict(checks=checks,repairs=repairs,semantic_review_pending=True))
        status=m.read(p/'status.json');status.update(status='pilot_complete_awaiting_semantic_review',completed_utc=m.utc());m.save(p/'status.json',status)
    finally:m.summarize(p);m.preserve(p);m.preserve(run)

if __name__=='__main__':
    action=sys.argv[1]
    if action=='prepare':prepare()
    else:
        run=Path(POINTER.read_text(encoding='utf-8').strip())
        if action=='pilot':pilot(run)
        elif action=='scope_recheck':scope_recheck(run)
        elif action=='execute':
            assert m.read(run/'pilot/semantic_review.json')['gate']=='PASS'
            original_compact=m.compact_section_prompt
            def full_compact(manifest,texts,questions,rules):
                return original_compact(manifest,texts,questions,rules)+include_resolved_index(run/'experiment.sqlite',manifest)
            m.compact_section_prompt=full_compact
            m.execute(run)
        else:raise ValueError(action)
