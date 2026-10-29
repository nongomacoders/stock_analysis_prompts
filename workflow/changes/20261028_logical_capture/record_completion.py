"""Record executed offline validation and unchanged production/source fingerprints."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,obj):p.write_bytes((json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
baseline=read(HERE/'preservation_baseline.json')
assert digest(ROOT/'documents/analysis.sqlite')==baseline['production_database_sha256']
summary=read(HERE/'preview_summary.json')
for item in summary:
    assert digest(ROOT/item['source'])==item['sha256']
    label=next(label for label in ['NTU','DCP_AFS','PAN'] if read(HERE/(label+'_plan.json'))['sha256']==item['sha256'])
    plan=read(HERE/(label+'_plan.json'))
    assert [p for g in plan['groups'] for p in range(g['physical_pages'][0],g['physical_pages'][1]+1)]==list(range(1,item['physical_page_count']+1))
ntu=read(HERE/'NTU_plan.json')
trade=next(g for g in ntu['groups'] if g['physical_pages']==[25,25])
assert trade['continuation_cut'] and trade['continuation_reason']=='note_starts_on_shared_page'
final=read(ROOT/'tmp/logical-capture-verified-20261028-result.json')
assert final['exit_code']==0
validation=HERE/'validation';validation.mkdir(exist_ok=True)
for result in (ROOT/'tmp').glob('logical-capture-*-result.json'):
    shutil.copy2(result,validation/result.name)
files=['section_capture/capture_planner.py','section_capture/section_matcher.py','section_capture/packages.py',
       'section_capture/one_shot_view.py','tests/test_capture_planner.py','tests/test_one_shot_pipeline.py',
       'docs/LOGICAL_CAPTURE.md','docs/WORKLOAD_RELIABILITY.md']
record=dict(completed_utc=datetime.now(timezone.utc).isoformat(),scope='Local logical PDF capture planning and offline integration; no paid reruns.',
 planner='native_logical_pages_v1',defaults=dict(max_pages=6,max_chars=24000,target_pages=3,target_chars=12000),
 source_previews=summary,final_test_result=final,final_test_command='.venv/Scripts/python.exe -m pytest tests -q -p no:cacheprovider -p workflow.changes.20261028_valuation_withholding.offline_pytest_plugin --basetemp=tmp/logical-capture-verified-20261028',
 production_database_unchanged=True,source_pdfs_unchanged=True,paid_model_calls=0,
 code_and_doc_hashes={p:digest(ROOT/p) for p in files},
 visual_inspection='Viewed unchanged NTU physical pages24 and25 in preserved PNGs; checked real shared trade-ECL/currency-note boundary.',
 iteration_record=['Initial focused tests29 passed,exit0.',
  'Integration51 passed/2 failed,exit1: orchestration fixture mocked partial ranges and cached-completion fixture marked only the first package; corrected fixtures to reflect isolated orchestration/all completed packages.',
  'Repaired capture/pipeline tests27 passed,exit0. Full213 passed,exit0.',
  'Visual inspection added shared-page subnote continuation check. Full213 passed/1 failed,exit1: synthetic heading overlapped fake body rows geometrically; separated fixture coordinates.',
  'Shared-page/capture tests19 passed,exit0; final full result above.'],
 limitations=['Native layout heuristic, no OCR or guaranteed semantic table boundaries.',
  'A shared physical page stays intact and can contain multiple topics; neighboring dependencies are explicit.',
  'More focused captures mean more possible model calls; quality/cost improvement not yet established by a paid comparison.',
  'Existing saved analysis is preserved; new planner applies to new captures.'])
save(HERE/'implementation_record.json',record)
print(json.dumps(dict(final_tests=final,production_unchanged=True,sources_unchanged=True,previewed_pages=sum(i['physical_page_count'] for i in summary),paid_calls=0)))
