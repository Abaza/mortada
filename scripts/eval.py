import json, time
from pathlib import Path
from fastapi_app.retriever import retrieve
from fastapi_app.llm_loader import stream

cases = json.loads(Path('tests/corpus.json').read_text())
lat=[]; em=f1=0
for c in cases:
    docs = retrieve(c['question'])
    prompt = c['question']+'\n'+"\n".join(t for t,_ in docs)
    t0=time.time(); ans=''.join(stream(prompt)); lat.append(time.time()-t0)
    if ans.strip()==c['answer'].strip(): em+=1
    inter=set(ans.split())&set(c['answer'].split())
    f1+=2*len(inter)/(len(ans.split())+len(c['answer'].split()) or 1)
print('EM',em/len(cases),'F1',f1/len(cases),'p95',sorted(lat)[int(.95*len(lat))-1])
