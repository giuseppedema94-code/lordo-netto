import csv, re, json, sys
DL='/home/claude/dl'
import os
Y0=int(os.environ.get('Y0','2026'))
years=[y for y in [2026,2025,2024,2023,2022,2021] if y<=Y0]
files={y:(f'{DL}/com2026.bin' if y==2026 else f'{DL}/com{y}.csv') for y in years}
def num(s):
    s=s.strip().replace('€','')
    if not s: return None
    s=s.replace('.','').replace(',','.') if ',' in s else s
    try: return float(s)
    except: return None
def amounts(desc):
    out=[]
    for m in re.findall(r'\d[\d.]*(?:,\d+)?',desc):
        if ',' in m: v=float(m.replace('.','').replace(',','.'))
        elif re.fullmatch(r'\d{1,3}(\.\d{3})+',m): v=float(m.replace('.',''))
        else:
            try: v=float(m)
            except: continue
        out.append(v)
    return [v for v in out if v>=1000]
data={}; issues=[]
for y in years:
    rows=list(csv.reader(open(files[y],encoding='utf-8',errors='replace'),delimiter=';'))
    h=rows[0]
    for x in rows[1:]:
        if len(x)<10: continue
        key=x[0]
        if key in data: continue
        a1=x[8].strip()
        if a1=='0*' or a1=='': 
            data.setdefault('_names',{})[key]=(x[1],x[2]); continue
        flag=x[h.index('FLAG_NUOVA')] if 'FLAG_NUOVA' in h else ''
        es=0.0; br=[]; spec=False
        pairs=[(x[i],x[i+1]) for i in range(8,8+24,2) if i+1<len(x)]
        for al,de in pairs:
            al=al.strip(); de=de.strip()
            if not al and not de: continue
            r=num(al) if al else None
            dl=de.lower()
            if 'esenzion' in dl or 'esente' in dl:
                am=amounts(de)
                if am: es=max(es,am[0])
                continue
            if r is None: spec=True; continue
            if 'unica' in dl or not de:
                br.append([None,r]); continue
            am=amounts(de)
            if 'oltre' in dl and len(am)==1: up=None
            elif am: up=max(am)
            else: spec=True; up=None
            br.append([up,r])
        imp=x[-1].strip()
        if imp and num(imp) and num(imp)>es: es=num(imp)
        if not br: spec=True; br=[[None,0.0]]
        # order brackets
        fin=sorted([b for b in br if b[0] is not None],key=lambda b:b[0]); inf=[b for b in br if b[0] is None]
        br=fin+(inf[-1:] if inf else ([[None,fin[-1][1]]] if fin else []))
        if fin and not inf: spec=True
        if flag=='0': spec=True
        rates=[b[1] for b in br]
        if any(r>1.5 or r<0 for r in rates): spec=True; issues.append((key,x[1],rates))
        data[key]={'n':x[1],'p':x[2],'y':y,'e':es,'b':br,'s':spec}
names=data.pop('_names',{})
for k,(n,p) in names.items():
    if k not in data: data[k]={'n':n,'p':p,'y':None,'e':0,'b':[[None,0.0]],'s':False}
print(len(data),'comuni', sum(1 for v in data.values() if v['y'] is None),'senza addizionale', sum(v['s'] for v in data.values()),'casi specifici',file=sys.stderr)
from collections import Counter
print(Counter(v['y'] for v in data.values()),file=sys.stderr)
print('issues',issues[:15],file=sys.stderr)
json.dump(data,open(f'/home/claude/build/comuni{Y0}.json','w'),ensure_ascii=False)
