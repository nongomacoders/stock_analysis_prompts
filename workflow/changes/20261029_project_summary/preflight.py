"""Report candidate size and credential patterns without printing credential contents."""
import subprocess,json,re,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
raw=subprocess.check_output(['git','ls-files','-c','-o','--exclude-standard','-z'],cwd=ROOT)
names=sorted(set(filter(None,raw.decode('utf-8').split('\0'))));tot=collections.defaultdict(lambda:dict(files=0,bytes=0));large=[];hits=[]
patterns=[re.compile(rb'sk-or-v1-[0-9a-fA-F]{64}'),re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),re.compile(rb'AIza[0-9A-Za-z_-]{35}')]
for name in names:
    p=ROOT/name
    if not p.is_file():continue
    size=p.stat().st_size;key=name.split('/')[0];tot[key]['files']+=1;tot[key]['bytes']+=size
    if size>=100*1024*1024:large.append(dict(path=name,bytes=size))
    if p.suffix.lower() not in {'.sqlite','.png','.jpg','.jpeg','.pdf','.zip','.db'} and size<30*1024*1024:
        data=p.read_bytes()
        for i,pattern in enumerate(patterns):
            if pattern.search(data):hits.append(dict(path=name,pattern_index=i))
result=dict(groups=dict(tot),files_over_100MiB=large,credential_pattern_hits=hits)
(Path(__file__).parent/'preflight.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
