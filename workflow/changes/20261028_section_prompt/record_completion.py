from pathlib import Path
import hashlib
import importlib.util
import json
import shutil
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('pilot_driver',HERE/'pilot.py');t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
run=Path(t.POINTER.read_text(encoding='utf-8').strip())
paths=[ROOT/'section_capture/packages.py',ROOT/'section_capture/question_ledger.py',ROOT/'tests/test_section_prompt.py',ROOT/'tests/test_workload_reliability.py']
paths+=list((ROOT/'prompts').glob('*/12-analyst-reading-brief/v1.1.0/prompt.md'))
files=[]
for path in paths:
    dest=run/'inputs/implementation'/path.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,dest)
    files.append(dict(path=str(path.relative_to(ROOT)),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
for name in ['full_test_result.json','target_test_result.json']:shutil.copy2(HERE/name,run/'inputs'/name)
assert not any((ROOT/'tmp'/name).exists() for name in ['section_prompt_target_20261028','section_prompt_full_20261028'])
t.m.preserve(run)
record=dict(completed_utc=t.m.utc(),run=str(run),files=files,full_tests=t.m.read(HERE/'full_test_result.json'),
    initial_targeted_tests=t.m.read(HERE/'target_test_result.json'),test_folders_cleaned=True,
    all_originals_and_sources_preserved=t.m.read(run/'preservation.json'),paid_calls=8,paid_repairs=0,gemini_api_calls=0,
    tooling_retrospective='TOOL_CHEATSHEET.md section37;large reads/line-ending warnings covered by existing guidance.',
    decision='Simpler first-pass prompt implemented;limited paired pilot supports usability,not universal financial accuracy;remaining errors preserved in versioned audit.')
t.m.save(HERE/'implementation_record.json',record)
print(json.dumps(dict(full_test_exit_code=record['full_tests']['exit_code'],test_folders_cleaned=True,preservation=record['all_originals_and_sources_preserved'])))
