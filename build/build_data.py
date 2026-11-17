import csv, json
PR = {
 "Piemonte":"AL AT BI CN NO TO VB VC","Valle d'Aosta":"AO","Lombardia":"BG BS CO CR LC LO MB MI MN PV SO VA",
 "Bolzano":"BZ","Trento":"TN","Veneto":"BL PD RO TV VE VI VR","Friuli Venezia Giulia":"GO PN TS UD",
 "Liguria":"GE IM SP SV","Emilia-Romagna":"BO FC FE MO PC PR RA RE RN","Toscana":"AR FI GR LI LU MS PI PO PT SI",
 "Umbria":"PG TR","Marche":"AN AP FM MC PU","Lazio":"FR LT RI RM VT","Abruzzo":"AQ CH PE TE","Molise":"CB IS",
 "Campania":"AV BN CE NA SA","Puglia":"BA BR BT FG LE TA","Basilicata":"MT PZ","Calabria":"CS CZ KR RC VV",
 "Sicilia":"AG CL CT EN ME PA RG SR TP","Sardegna":"CA NU OR SS SU"}
p2r={p:r for r,ps in PR.items() for p in ps.split()}
NAMEMAP={"REGIONE VALLE D'AOSTA":"Valle d'Aosta","PROVINCIA AUTONOMA DI TRENTO":"Trento","PROVINCIA AUTONOMA DI BOLZANO":"Bolzano"}
rows=list(csv.reader(open('/home/claude/dl/reg2026.csv',encoding='latin-1'),delimiter=';'))[1:]
best={}
for x in rows:
    n=NAMEMAP.get(x[1]) or x[1].replace('REGIONE ','').title().replace("D'","d'").replace('-R','-R')
    num=int(x[2]); best.setdefault(n,{})
    best[n].setdefault(num,[]).append(x)
REG={}
fix={'Emilia-Romagna':'Emilia-Romagna','Friuli Venezia Giulia':'Friuli Venezia Giulia'}
for n,byn in best.items():
    k=max(byn); rr=byn[k]
    br=[]
    for x in rr:
        rate=float(x[7]); f=x[8].strip().lower()
        if 'unica' in f or 'oltre 50000' in f and 'fino' not in f: up=None
        else:
            import re; up=max(float(v) for v in re.findall(r'\d+\.\d+',f))
        br.append([up,rate])
    br=sorted([b for b in br if b[0]],key=lambda b:b[0])+[b for b in br if b[0] is None]
    REG[n]={'b':br,'num':k,'pub':rr[0][3],'disp':rr[0][4].strip()}
missing=set(PR)-set(REG); print('missing',missing, 'extra',set(REG)-set(PR))
for n in sorted(REG): print(n,REG[n]['num'],REG[n]['pub'],REG[n]['b'])
d=json.load(open('comuni.json'))
com=[]
for k,v in sorted(d.items(), key=lambda kv:(kv[1]['n'],kv[1]['p'])):
    b=';'.join(f"{'' if u is None else int(u)}:{r:g}" for u,r in v['b'])
    com.append([v['n'].title(),v['p'],int(v['e']),b,v['y'] or 0,1 if v['s'] else 0])
json.dump({'reg':{n:{'b':REG[n]['b'],'num':REG[n]['num'],'pub':REG[n]['pub']} for n in REG},'p2r':p2r,'com':com},open('addiz.json','w'),ensure_ascii=False,separators=(',',':'))
import os; print(os.path.getsize('addiz.json'))
