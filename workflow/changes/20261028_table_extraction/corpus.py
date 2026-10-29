"""Export before/after native extraction on unchanged NTU/PAN source pages."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import pdfplumber
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT));sys.stdout.reconfigure(encoding='utf-8')
from section_capture.pdf_source import extract_structured_text
spec=importlib.util.spec_from_file_location('section_capture.old_pdf_source',HERE/'before_pdf_source.py');old=importlib.util.module_from_spec(spec);sys.modules[spec.name]=old;spec.loader.exec_module(old)
cases=[('NTU',ROOT/'companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf',[9,13,18,22,24,25,30,31]),
       ('PAN',ROOT/'companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf',[4,38,39,48,49,50])]
out=[]
for ticker,path,pages in cases:
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    with pdfplumber.open(path) as doc:
        for number in pages:
            page=doc.pages[number-1];before=old.extract_structured_text(page);after=extract_structured_text(page)
            for version,text in [('before',before),('after',after)]:
                dest=HERE/version/f'{ticker}_{number}.md';dest.parent.mkdir(exist_ok=True);dest.write_bytes(text.encode('utf-8'))
            out.append(dict(ticker=ticker,page=number,source=str(path),source_sha256=digest,before_chars=len(before),after_chars=len(after)))
(HERE/'corpus.json').write_bytes((json.dumps(out,indent=2)+'\n').encode('utf-8'))
print(json.dumps(out,indent=2))
