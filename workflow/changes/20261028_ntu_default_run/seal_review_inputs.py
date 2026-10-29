"""Preserve the exact new model subjects inside the audit's inputs directory."""
import importlib.util
from pathlib import Path
import shutil
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('runner',HERE/'rerun.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
run=Path(m.POINTER.read_text(encoding='utf-8').strip());target=run/'inputs/review_subject'
target.mkdir(exist_ok=False)
files=[]
for name in ['section_06_uncapped_v4.md','stage1.md','stage2.md','stage2_publication.md','publication_assessment.json']:
    p=run/'outputs'/name;shutil.copy2(p,target/name)
    assert m.sha(p)==m.sha(target/name)
    files.append(dict(original=str(p.relative_to(run)),preserved=str((target/name).relative_to(run)),sha256=m.sha(p)))
for name in ['check_uncapped_results.py','finalize_uncapped.py']:
    shutil.copy2(HERE/name,run/'inputs'/name)
m.save(run/'inputs/review_subject_manifest.json',dict(preserved_utc=m.utc(),files=files))
print('Five exact new subject files preserved and hash-verified; source/model outputs unchanged.')
