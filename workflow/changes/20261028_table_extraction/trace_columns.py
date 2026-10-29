import json
from pathlib import Path
import sys
import pdfplumber
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT));sys.stdout.reconfigure(encoding='utf-8')
from section_capture.pdf_source import extract_structured_text
snapshot={}
def trace(frame,event,arg):
    if frame.f_code.co_name=='extract_structured_text' and event=='return':
        for key in ['cols','mapped_rows','parsed_lines']:
            snapshot[key]=frame.f_locals.get(key)
    return trace
path=ROOT/'companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf'
with pdfplumber.open(path) as doc:
    sys.settrace(trace);text=extract_structured_text(doc.pages[21]);sys.settrace(None)
HERE=Path(__file__).resolve().parent
(HERE/'p22_trace.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(cols=snapshot['cols'],selected_rows=[r for r in snapshot['mapped_rows'] if any('390' in c or c in {'5','395'} for c in r.get('cells',[]))]),indent=2))
