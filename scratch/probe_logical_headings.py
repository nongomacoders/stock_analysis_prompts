from pathlib import Path
import sys
import pdfplumber
sys.stdout.reconfigure(encoding='utf-8')
path=Path('companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf')
with pdfplumber.open(path) as doc:
    for n in [20,21,22,23,24,25,26,27,28,29,30,31]:
        words=doc.pages[n-1].extract_words(extra_attrs=['size','fontname'])
        lines={}
        for w in words:
            if w['top']<250 and w['size']>=9.5:
                lines.setdefault(round(w['top']),[]).append(w)
        print(n, ' | '.join(' '.join(w['text'] for w in ws)+f' [{ws[0]["size"]:.1f},{ws[0]["fontname"]}]' for ws in lines.values())[:720])
