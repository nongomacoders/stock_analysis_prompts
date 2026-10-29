"""Read billing metadata for the first saved generation; no generation request."""
import json
from pathlib import Path
import sys
import urllib.request
import urllib.error
import urllib.parse
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'AGENTS.md').exists())
sys.path.insert(0,str(ROOT))
from section_capture.openrouter import get_openrouter_api_key
run=Path((Path(__file__).parent/'latest_run.txt').read_text(encoding='utf-8').strip())
receipt=json.loads((run/'receipts/section_01.json').read_text(encoding='utf-8'))
key=get_openrouter_api_key()
endpoint='https://openrouter.ai/api/v1/generation?'+urllib.parse.urlencode({'id':receipt['id']})
try:
    with urllib.request.urlopen(urllib.request.Request(endpoint,headers={'Authorization':'Bearer '+key}),timeout=30) as response:
        obj=json.load(response)
        result={'status':response.status,'data':obj.get('data')}
except urllib.error.HTTPError as exc:
    body=exc.read().decode('utf-8',errors='replace').replace(key,'[REDACTED]')
    try: error=json.loads(body).get('error')
    except json.JSONDecodeError: error='Non-JSON error response'
    result={'status':exc.code,'error':error}
(run/'billing_lookup_diagnostic.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'http_status':result['status'],'error':result.get('error'),'model_calls':0}))
