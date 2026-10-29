"""Independent calculations and evidence checks; never executes Gemini's script."""
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import sys
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
sys.stdout.reconfigure(encoding='utf-8')
run=Path((HERE/'review_run.txt').read_text(encoding='utf-8'))
BASE=run.parent;gemini=BASE/'20261028T170032Z_gemini';pilot=BASE/'20261028T163642Z_section_prompt_paired_pilot'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
def offline(event,args):
    if event in {'socket.connect','socket.getaddrinfo','socket.sendto'}:raise RuntimeError('Offline independent review')
sys.addaudithook(offline)
metrics=read(pilot/'comparison.json')
ids=[];cost=Decimal(0)
for p in (pilot/'receipts').glob('*.json'):
    r=read(p);request=read(pilot/'requests'/p.name)
    assert r['success'] and r['finish_reason']=='stop'
    assert request['provider']['only']==['fireworks'] and not request['provider']['allow_fallbacks']
    assert request['reasoning']=={'effort':'none','exclude':True}
    assert abs(r['cost_usd']-r['generation_metadata']['total_cost'])<1e-9
    ids.append(r['id']);cost+=Decimal(str(r['cost_usd']))
assert len(ids)==len(set(ids))==8 and cost==Decimal('0.0300091344')
verification=[]
for item in read(gemini/'inputs/manifest.json'):
    original=ROOT/item['original_path'];preserved=ROOT/item['preserved_path']
    verification.append(dict(path=item['original_path'],original_match=digest(original)==item['sha256'],copy_match=digest(preserved)==item['sha256']))
assert all(x['original_match'] and x['copy_match'] for x in verification)
new_pan=(pilot/'outputs/pan_operations_new.md').read_text(encoding='utf-8')
assert '197,608' in new_pan and '194,954' not in new_pan and '1,573' not in new_pan
old_shared=(pilot/'outputs/ntu_shared_page_old.md').read_text(encoding='utf-8')
delta=json.loads(re.search(r'```json\s*\n(.*?)```',old_shared,re.S).group(1))
quotes=[x['quote'] for u in delta['updates'] for x in u['evidence']]
source=read(pilot/'inputs/ntu_shared_page.json')['manifest']
normalize=lambda x:re.sub(r'\s+',' ',x).strip()
quote_checks=[dict(quote=q,length=len(q),literal=any(normalize(q) in normalize(s['text']) for s in source['selections'])) for q in quotes]
calc=dict(ntu_principal=3975+382-728+383-167,ntu_other_correct=702+28-116+30,
    ntu_other_wrong_ledger=702+28-116-30,ntu_wrong_minus_stated=(702+28-116-30)-644,
    trade_2026_net=374-5,trade_2025_net=419-6,trade_sept_net=364-10,
    trade_2025_net_current=345,trade_2025_net_bucket_sum=345+61+6+1,
    trade_2026_rate=5/374*100,trade_2025_rate=6/419*100,
    sept_current_implied_allowance_m=286*.0006,sept_30days_implied_allowance_m=52*.0019,
    pan_2025_clean=92643+2654+98636+1081+1513,
    pan_2025_overlapping=93724+2654+98636+1081+1513,
    pan_2025_excess=(93724+2654+98636+1081+1513)-196527,
    pan_2025_correct_using_inclusive=93724+2654+98636+1513,
    pan_2025_subtotal_overlap=93724-92643,
    pan_2026_component_model_sum=105478+2428+113613+18667+32124,
    pan_2026_mining_subtotal=65233+40246,
    pan_2026_group_underground_reported=105478,
    pan_aisc_normalized_m=420.686+87.718,
    pan_aisc_normalized_residual_m=508.405-(420.686+87.718),
    pan_aisc_group_per_oz_if_thousands=508405000/272373,
    pan_aisc_group_per_oz_if_literal_millions=508405000000/272373,
    pan_aisc_low_per_oz=420686000/247219,pan_aisc_high_per_oz=87718000/25154,
    pan_aisc_yoy_pct=(1867/1600-1)*100,pan_oz_yoy_pct=(272373/196927-1)*100)
assert calc['ntu_other_correct']==644 and calc['ntu_other_wrong_ledger']==584
assert calc['pan_2025_clean']==calc['pan_2025_correct_using_inclusive']==196527
assert calc['trade_2025_net_bucket_sum']==413
assert calc['pan_2025_excess']==1081
save(run/'calculations/results.json',dict(values=calc,pilot_totals=metrics['totals'],cost_usd=str(cost),
    gemini_preservation=verification,old_shared_quotes=quote_checks,
    note='Inputs transcribed from independently viewed NTU p13/25 and PAN p38/39/48/49/50. Expected losses do not establish actual defaults. PAN AISC normalization is conditional,not a verified source unit correction.'))
manifest=read(run/'inputs/manifest.json')
assert all(digest(Path(x['original']))==x['sha256'] and digest(run/x['saved'])==x['sha256'] for x in manifest['files'])
assert all(digest(Path(x['path']))==x['sha256'] for x in manifest['sources'])
c=sqlite3.connect((ROOT/'documents/analysis.sqlite').as_uri()+'?mode=ro',uri=True);tables={}
for name, in c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
    rows=c.execute('SELECT * FROM "'+name.replace('"','""')+'"').fetchall()
    tables[name]=hashlib.sha256(repr(sorted(rows,key=repr)).encode('utf-8')).hexdigest()
c.close();assert tables==manifest['production_table_hashes']
save(run/'preservation.json',dict(original_files_unchanged=True,source_pdfs_unchanged=True,production_all_tables_unchanged=True,
    gemini_manifest_entries=len(verification),preserved_review_files=len(manifest['files'])))
print(json.dumps(dict(values=calc,gemini_manifest_entries=len(verification),quote_checks=quote_checks,preservation=read(run/'preservation.json')),indent=2))
