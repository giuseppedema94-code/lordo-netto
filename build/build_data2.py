import csv, json, re
exec(open('build_data.py').read().split("rows=list(")[0])   # PR, p2r, NAMEMAP
def regs(path):
    rows=list(csv.reader(open(path,encoding='latin-1'),delimiter=';'))[1:]
    best={}
    for x in rows:
        n=NAMEMAP.get(x[1]) or x[1].replace('REGIONE ','').title().replace("D'","d'")
        best.setdefault(n,{}).setdefault(int(x[2]),[]).append(x)
    out={}
    for n,byn in best.items():
        k=max(byn); br=[]
        for x in byn[k]:
            f=x[8].strip().lower()
            up=None if ('unica' in f or ('oltre 50000' in f and 'fino' not in f)) else max(float(v) for v in re.findall(r'\d+\.\d+',f))
            br.append([up,float(x[7])])
        br=sorted([b for b in br if b[0]],key=lambda b:b[0])+[b for b in br if b[0] is None]
        out[n]={'b':br,'num':k,'pub':byn[k][0][3]}
    assert set(out)==set(PR), set(PR)^set(out)
    return out
R26=regs('/home/claude/dl/reg2026.csv'); R25=regs('/home/claude/dl/reg2025.csv')
d26=json.load(open('comuni2026.json')); d25=json.load(open('comuni2025.json'))
enc=lambda v:';'.join(f"{'' if u is None else int(u)}:{r:g}" for u,r in v['b'])
com=[]; diff=0
for k,v in sorted(d26.items(), key=lambda kv:(kv[1]['n'],kv[1]['p'])):
    row=[v['n'].title(),v['p'],int(v['e']),enc(v),v['y'] or 0,1 if v['s'] else 0]
    w=d25.get(k)
    if w is None: w={'e':0,'b':[[None,0.0]],'y':None}
    if (int(w['e']),enc(w))!=(int(v['e']),enc(v)):
        row+= [int(w['e']),enc(w) if w['y'] else ':0']; diff+=1
    com.append(row)
json.dump({'reg':R26,'reg25':R25,'p2r':p2r,'com':com},open('addiz.json','w'),ensure_ascii=False,separators=(',',':'))
import os; print('comuni con aliquote 2025 diverse:',diff,'size',os.path.getsize('addiz.json'))
for n in R26:
    if R26[n]['b']!=R25[n]['b']: print('reg diversa',n,R25[n]['b'],'->',R26[n]['b'])
