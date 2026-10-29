"""Read saved receipts only; no model calls or telemetry probes."""
import json
from pathlib import Path
from datetime import datetime, timezone

HERE=Path(__file__).resolve().parent
plan=json.loads((HERE/'comparison_plan.json').read_text(encoding='utf-8'))
result={'scope':'Completed trial receipts. The exact user stuck-question timestamp is not available here.',
        'companies':[], 'telemetry_flags':{'DOTNET_CLI_TELEMETRY_OPTOUT':'1','POWERSHELL_TELEMETRY_OPTOUT':'1'},
        'telemetry_causation':'No telemetry-related rejection appeared in the visible tools for this implementation/rerun sequence. Earlier project entries describe separate prior incidents. No host packet trace was collected.'}
for info in plan['companies']:
    run=Path(info['run'])
    receipts=[]
    for path in (run/'outputs').glob('*.run.json'):
        data=json.loads(path.read_text(encoding='utf-8'))
        label=path.name.removesuffix('.run.json')
        receipts.append(dict(label=label,elapsed_seconds=data.get('elapsed_seconds',0),
                             completion_tokens=data.get('completion_tokens',0),reasoning_tokens=data.get('reasoning_tokens',0),
                             completed_utc=datetime.fromtimestamp(path.stat().st_mtime,timezone.utc).isoformat()))
    requests=list((run/'requests').glob('*.md'))
    first=min(p.stat().st_mtime for p in requests)
    last=max(p.stat().st_mtime for p in (run/'outputs').glob('*.run.json'))
    item=dict(ticker=info['ticker'],primary_captures=sum(d['captures'] for d in info['documents']),
              successful_receipts=len(receipts),successful_ledger_repair_receipts=sum('_ledger_' in r['label'] for r in receipts),
              summed_recorded_call_seconds=round(sum(r['elapsed_seconds'] for r in receipts),2),
              first_request_utc=datetime.fromtimestamp(first,timezone.utc).isoformat(),
              last_receipt_utc=datetime.fromtimestamp(last,timezone.utc).isoformat(),
              observed_request_to_last_receipt_seconds=round(last-first,2),
              slowest_receipts=sorted(receipts,key=lambda r:r['elapsed_seconds'],reverse=True)[:4])
    result['companies'].append(item)
result['successful_receipts_total']=sum(c['successful_receipts'] for c in result['companies'])
result['successful_ledger_repairs_total']=sum(c['successful_ledger_repair_receipts'] for c in result['companies'])
result['test_process_seconds_from_observed_tool_results']=[53.58,69.94,64.24,9.19,72.64,67.86,75.53,69.67,68.49]
result['summed_test_process_seconds']=round(sum(result['test_process_seconds_from_observed_tool_results']),2)
result['timing_limits']='Companies ran concurrently and tests overlapped calls. Do not add process times to obtain wall time. Failed calls without receipts add unknown time/usage; saved call timings can include retries.'
(HERE/'delay_retrospective.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
