import openpyxl,glob,json,re,sys
src=sys.argv[1]; out=[]
def cat(fn):
    f=fn.lower()
    if 'elettric' in f: return 'e'
    if 'plug' in f or 'phev' in f: return 'p'
    return 'a'
def num(v):
    if isinstance(v,(int,float)): return float(v)
    if isinstance(v,str):
        v=v.strip().replace('.','').replace(',','.')
        try: return float(v)
        except: return None
for f in sorted(glob.glob(src+'/*.xlsx')):
    c=cat(f); y=2025 if '2025' in f or 'phev-fuori' in f else 2026
    ws=openpyxl.load_workbook(f,read_only=True,data_only=True).worksheets[0]
    rows=list(ws.iter_rows(values_only=True)); h=[str(x or '').upper() for x in rows[0]]
    im=next(i for i,x in enumerate(h) if x.strip()=='MARCA'); imo=im+1
    ick=next(i for i,x in enumerate(h) if 'COSTO' in x)
    for r in rows[1:]:
        r=list(r)+[None]*10
        # rows without ID shift left by one in some files
        m,mo,ck=r[im],r[imo],num(r[ick])
        if ck is None and isinstance(r[im-1] if im>0 else None,str):
            m,mo,ck=r[im-1],r[im],num(r[ick-1])
        if not (isinstance(m,str) and isinstance(mo,str) and ck and 0.1<ck<5): continue
        out.append([m.strip(),re.sub(r'\s+',' ',mo.strip()),round(ck,4),c]+([y] if y!=2026 else []))
seen=set(); res=[]
for x in out:
    k=(x[0],x[1],x[3])
    if k in seen: continue
    seen.add(k); res.append(x)
res.sort(key=lambda x:(x[0],x[1]))
json.dump(res,open(sys.argv[2],'w'),ensure_ascii=False,separators=(',',':'))
from collections import Counter
print(len(res),Counter(x[3] for x in res),sum(1 for x in res if len(x)>4))
