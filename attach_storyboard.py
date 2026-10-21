"""Attach existing real media to a locally running Agent Storyboard task.

Uses the documented existing API. No remote model invocation or credentials.
"""
import argparse,json,urllib.request,urllib.parse
from pathlib import Path

def attach(origin,project,shot,file,kind):
    parsed=urllib.parse.urlparse(origin)
    if parsed.scheme!='http' or parsed.hostname not in ('127.0.0.1','localhost') or parsed.username or parsed.password or parsed.path not in ('','/') or parsed.query or parsed.fragment:raise ValueError('Local HTTP origin required')
    file=Path(file).resolve(strict=True)
    def post(path,body):
        req=urllib.request.Request(origin.rstrip('/')+path,data=json.dumps(body).encode(),headers={'Content-Type':'application/json'},method='POST')
        with urllib.request.urlopen(req,timeout=30) as r:return json.load(r)
    queued=post('/api/generation/tasks',{'projectId':project,'shotIds':[shot]})
    rows=queued['queued']
    if len(rows)!=1:raise ValueError('Expected one new pending task; inspect existing tasks before retry')
    task=rows[0]['taskId'];post('/api/generation/tasks/'+urllib.parse.quote(task,safe='')+'/claim',{})
    return post('/api/generation/tasks/'+urllib.parse.quote(task,safe='')+'/complete',{'sourcePath':str(file),'mediaType':kind})

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--origin',default='http://127.0.0.1:43218');p.add_argument('--project',required=True);p.add_argument('--shot',required=True);p.add_argument('--file',required=True);p.add_argument('--kind',choices=['image','video'],required=True);a=p.parse_args();print(json.dumps(attach(a.origin,a.project,a.shot,a.file,a.kind),ensure_ascii=False))
