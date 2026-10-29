"""Read-only native-geometry probes;preserve pre-change code and source hashes."""
import hashlib
import json
from pathlib import Path
import sys
import pdfplumber
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
sys.stdout.reconfigure(encoding='utf-8')
source=ROOT/'section_capture/pdf_source.py'
before=HERE/'before_pdf_source.py'
if not before.exists():before.write_bytes(source.read_bytes())
ledger=ROOT/'section_capture/question_ledger.py';before_ledger=HERE/'before_question_ledger.py'
if not before_ledger.exists():before_ledger.write_bytes(ledger.read_bytes())
ntu=ROOT/'companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf'
pan=ROOT/'companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf'
out=[]
for ticker,path,pages in [('NTU',ntu,[13,22,24,25,31]),('PAN',pan,[48,49])]:
    with pdfplumber.open(path) as doc:
        for number in pages:
            page=doc.pages[number-1]
            settings={'vertical_strategy':'text','horizontal_strategy':'lines','min_words_vertical':3,'text_x_tolerance':1}
            tables=page.find_tables(settings)
            item=dict(ticker=ticker,page=number,tables=[dict(bbox=t.bbox,rows=len(t.rows),cols=len(t.columns),sample=t.extract()[:3]) for t in tables])
            out.append(item)
    out.append(dict(ticker=ticker,source_sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
(HERE/'geometry_probe.json').write_bytes((json.dumps(out,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps(out,ensure_ascii=True,indent=2)[:11000])
