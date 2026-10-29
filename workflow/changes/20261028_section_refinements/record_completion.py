from pathlib import Path
import hashlib
import importlib.util
import json
import shutil
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('trial',HERE/'ntu_sections.py');t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
m=t.m;run=Path(t.POINTER.read_text(encoding='utf-8').strip())
assert not (ROOT/'tmp/section_refinements_20261028').exists()
tests=m.read(HERE/'test_result.json');assert tests['exit_code']==0
shutil.copy2(HERE/'test_result.json',run/'inputs/test_result.json')
# Drop duplicate derived handoff paragraphs if an audit close was safely replayed.
for path in [run/'RUN_SUMMARY.md',run/'gemini/PROMPT.md']:
    paragraphs=path.read_text(encoding='utf-8').split('\n\n');seen=set();unique=[]
    for paragraph in paragraphs:
        if paragraph.strip() and paragraph in seen:continue
        seen.add(paragraph);unique.append(paragraph)
    m.text(path,'\n\n'.join(unique))
m.preserve(run)
files=[]
for path in [ROOT/'prompts/common/12-analyst-reading-brief/v1.1.0/prompt.md',ROOT/'prompts/consumer_lending/12-analyst-reading-brief/v1.1.0/prompt.md',HERE/'ntu_sections.py']:
    files.append(dict(path=str(path.relative_to(ROOT)),sha256=m.sha(path)))
record=dict(completed_utc=m.utc(),run=str(run),files=files,tests=tests,test_folder_cleaned=True,
    verification=m.read(run/'verification.json'),completion=m.read(run/'completion_record.json'),preservation=m.read(run/'preservation.json'),
    retrospective='No shell/encoding/edit failures during implementation. One in-flight output probe returned exit1 before output existed;read completed receipts/status before opening live outputs. No automatic paid repairs. App rejection behavior reused unchanged;raw proposed ledger changes preserved separately.',
    source_review='Complete primary pages13,22,24,25,31 viewed read-only;financial corrections remain required;all other primary pages not independently visually reviewed this turn.')
m.save(HERE/'implementation_record.json',record)
print(json.dumps(dict(run=str(run),tests_exit_code=0,test_folder_cleaned=True,preservation=record['preservation'])))
