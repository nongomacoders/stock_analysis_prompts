import json
import sqlite3
import re
import sys
from pathlib import Path

plan = json.loads(Path(__file__).with_name('comparison_plan.json').read_text(encoding='utf-8'))
for info in plan['companies']:
    if len(sys.argv)>1 and info['ticker'] != sys.argv[1]:
        continue
    print(info['ticker'], Path(info['run'], 'status.json').read_text(encoding='utf-8'))
    conn = sqlite3.connect(Path(info['database']).resolve().as_uri()+'?mode=ro',uri=True)
    try:
        for row in conn.execute('SELECT package_id,validation_status,errors_json FROM section_response_attempts ORDER BY id DESC LIMIT 5'):
            print(row)
        last = conn.execute('SELECT a.response,s.manifest_json FROM section_response_attempts a JOIN sections s ON s.package_id=a.package_id WHERE validation_status=? ORDER BY a.id DESC LIMIT 1', ('rejected',)).fetchone()
        if last:
            manifest = json.loads(last[1])
            for block in re.findall(r'```json\s*\n(.*?)```',last[0],re.S):
                data = json.loads(block)
                for update in data.get('updates',[]):
                    for ev in update.get('evidence',[]):
                        texts = [s.get('text','') for s in manifest['selections'] if s['physical_page']==ev.get('physical_page')]
                        quote = ev.get('quote','')
                        if not any(quote in t for t in texts):
                            norm = lambda t: re.sub(r'\s+',' ',t).strip()
                            print(json.dumps(dict(question_id=update['question_id'],page=ev.get('physical_page'),quote=quote,
                                                  whitespace_normalized_match=any(norm(quote) in norm(t) for t in texts)),ensure_ascii=True))
    finally:
        conn.close()
