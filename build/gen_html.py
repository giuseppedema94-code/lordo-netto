import json, re, os, html, sys
D=json.load(open('/home/claude/build/pages.json'))
OUT=sys.argv[1]; BASE=sys.argv[2]  # es. /lordo-netto
NOINDEX=len(sys.argv)>3 and sys.argv[3]=='noindex'
SLUG={'commercio':'commercio-terziario','tessile':'tessile-abbigliamento','alimentare':'industria-alimentare','gomma':'gomma-plastica',
 'metalmeccanici':'metalmeccanici','studi':'studi-professionali','turismo':'turismo-alberghi','pubblici':'pubblici-esercizi',
 'logistica':'logistica-trasporto-merci','gasacqua':'gas-acqua','coopsoc':'cooperative-sociali','scuola':'scuola-statale','abi':'credito-abi','abicompl':'credito-abi-complementare','dirabi':'dirigenti-abi','dirterz':'dirigenti-terziario'}
CNEL={'commercio':'H011','tessile':'D014','alimentare':'E012','gomma':'B371','metalmeccanici':'C011','studi':'H442','turismo':'H052',
 'pubblici':'H05Y','logistica':'I100','abi':'J241','abicompl':'J241'}
SHORT={'commercio':'Commercio','tessile':'Tessile','alimentare':'Alimentare','gomma':'Gomma plastica','metalmeccanici':'Metalmeccanici',
 'studi':'Studi professionali','turismo':'Turismo','pubblici':'Pubblici esercizi','logistica':'Logistica','gasacqua':'Gas-Acqua','coopsoc':'Cooperative sociali','scuola':'Scuola statale','abi':'Credito ABI',
 'abicompl':'Credito ABI complementare','dirabi':'Dirigenti ABI','dirterz':'Dirigenti terziario'}
TEMI={'commercio':'#3730a3','dirterz':'#312e81','tessile':'#5b2a86','alimentare':'#0f5c4d','gomma':'#2f3e4e','metalmeccanici':'#1f4e79',
 'studi':'#0e5e6f','turismo':'#075985','pubblici':'#701a55','logistica':'#3f5f1f','gasacqua':'#355070','coopsoc':'#5c4a3a','scuola':'#4b3f72','abi':'#1b2f5b','abicompl':'#1b2f5b','dirabi':'#1b2f5b'}
ARCH='https://www.cnel.it/archivio-contratti/entra-nell-archivio/interroga-l-archivio'
def slug(t):
    t=t.lower().replace('ª','a').replace('°','').replace('(','').replace(')','').replace('.','')
    t=re.sub(r'[^a-z0-9]+','-',t).strip('-'); return t
def MENS(m): return '13 e mezza' if m==13.5 else str(int(m))
def lvslug(n):
    s=slug(n); return s if any(w in s for w in ('quadro','area','dirigente','viaggiante','docente','collaboratore','assistente','funzionario')) else s+'-livello'
def lvname(n):
    return n if any(w in n.lower() for w in ('quadro','area','dirigente','viaggiante','liv','docente','collaboratore','assistente','funzionario','operatore')) else f'livello {n}'
def corto(n):
    # nomi lunghi dei profili scuola, solo per i titoli: come li cerca la gente
    for a,b in (('Docente secondaria II grado','Docente superiori'),('Docente secondaria I grado','Docente scuola media'),('Docente infanzia e primaria','Insegnante infanzia e primaria'),
                ('diplomato (ITP)','ITP'),('Assistente amministrativo o tecnico','Assistente amministrativo'),(', ',' ')):
        n=n.replace(a,b)
    return n
def eur(v,d=0):
    s=f'{v:,.{d}f}'.replace(',','X').replace('.',',').replace('X','.'); return s+' €'
E=html.escape
CSS=''':root{--bg:#f6f7f8;--card:#fff;--ink:#16191d;--ink2:#3b4350;--mu:#667080;--line:#e4e7eb;--soft:#f6f7f8;--sep:#e4e7eb;--chip:#eef1f4;--bt:#16191d;color-scheme:light}
*{box-sizing:border-box}
body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;font-variant-numeric:tabular-nums;background:var(--bg);color:var(--ink);line-height:1.55}
header{background:var(--card);color:var(--ink);border-bottom:1px solid var(--line)}header .w{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:8px 16px;padding:14px 20px}
header a{color:var(--ink);text-decoration:none;font-weight:700;white-space:nowrap}header nav a{font-weight:400;color:var(--mu);margin-left:16px;font-size:15px}header nav a:hover{color:var(--ink)}
.w{max-width:860px;margin:0 auto;padding:0 20px}main.w{padding-top:26px;padding-bottom:40px}
.crumb{font-size:13.5px;color:var(--mu);margin-bottom:6px}.crumb a{color:var(--mu)}
h1{font-size:clamp(26px,4.4vw,36px);line-height:1.15;margin:0 0 10px}
h1::before{content:"";display:inline-block;width:10px;height:10px;border-radius:50%;background:var(--b);margin-right:10px;vertical-align:middle}
h2{font-size:21px;margin:32px 0 10px}
h3{font-size:16.5px;margin:18px 0 4px}
.lead{font-size:17px;color:var(--ink2);margin:0 0 18px}
.hero{background:var(--card);color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:18px 22px;display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.hero span{display:block;font-size:13px;color:var(--mu)}.hero b{font-weight:700;font-size:24px}
.hero .big b{font-size:34px}@media(max-width:620px){.hero{grid-template-columns:1fr 1fr}.hero .big{grid-column:1/-1}}
table{width:100%;border-collapse:separate;border-spacing:0;background:var(--card);border:1px solid var(--line);border-radius:8px;overflow:hidden;font-size:15px}
th,td{padding:9px 12px;border-bottom:1px solid var(--line);text-align:left}
th{background:var(--card);color:var(--mu);font-size:12.5px;font-weight:600;white-space:nowrap}
td.n,th.n{text-align:right;white-space:nowrap}
td.fut,th.fut{color:var(--mu)}
tr.me td{font-weight:700;color:var(--ink)}
.trt th.c{text-align:center;border-left:1px solid var(--line)}
.trt .lo{border-left:1px solid var(--line);color:var(--mu)}
.trt th.lo{color:var(--mu)}
.trt .ne{color:var(--ink);font-weight:700}
.trt th.ne{color:var(--ink)}
.trt td.fut.ne{color:var(--mu)}
.cta{display:inline-block;margin:20px 0 4px;background:var(--ink);color:var(--card)!important;text-decoration:none;font-weight:600;padding:12px 18px;border-radius:6px}
.note{font-size:13.5px;color:var(--mu)}
.box{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:14px 16px;margin-top:10px}
.lv{display:flex;flex-wrap:wrap;gap:8px;padding:0;list-style:none}.lv a{display:inline-block;padding:6px 12px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--ink);text-decoration:none;font-weight:600;font-size:14px}.lv a:hover{border-color:var(--mu)}
.tog{display:inline-flex;background:var(--chip);border-radius:6px;padding:2px;margin:6px 0 10px}.tog button{border:0;background:none;padding:6px 14px;border-radius:4px;font:inherit;font-size:13.5px;cursor:pointer;color:var(--mu)}.tog button.on{background:var(--card);color:var(--ink);font-weight:600;outline:1px solid var(--line)}
.tw{overflow-x:auto}
details{background:var(--card);border:1px solid var(--line);border-radius:8px;margin:8px 0;padding:10px 14px}details summary{cursor:pointer}details table{margin-top:10px}details .note{margin-left:6px}
footer{border-top:1px solid var(--line);padding:20px 0;font-size:13px;color:var(--mu)}
a{color:var(--ink)}
@media screen and (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0f1114;--card:#171a1e;--ink:#e8eaed;--ink2:#c3c8cf;--mu:#98a1ad;--line:#272c33;--soft:#1c2026;--sep:#272c33;--chip:#22272e;--bt:#e8eaed;color-scheme:dark}:root:not([data-theme="light"]) .theme-btn{border-color:var(--line)}}
@media screen{:root[data-theme="dark"]{--bg:#0f1114;--card:#171a1e;--ink:#e8eaed;--ink2:#c3c8cf;--mu:#98a1ad;--line:#272c33;--soft:#1c2026;--sep:#272c33;--chip:#22272e;--bt:#e8eaed;color-scheme:dark}:root[data-theme="dark"] .theme-btn{border-color:var(--line)}}
.theme-btn{background:transparent;border:1px solid #cfd4da;color:var(--ink2);border-radius:6px;padding:5px 10px;font:inherit;font-size:12.5px;font-weight:600;cursor:pointer;margin-left:16px}'''.replace('BASE',BASE)
def fit(t):
    # titolo entro 60 caratteri: aggiunge il marchio solo se c'è spazio
    return t+' | stipendioccnl' if len(t)+15<=60 else t
def ld(path,crumbs,extra=None):
    it=[{'@type':'ListItem','position':1,'name':'Home','item':'https://stipendioccnl.it/'}]
    acc=''
    for i,(t,u) in enumerate(crumbs,2):
        e={'@type':'ListItem','position':i,'name':t}
        e['item']='https://stipendioccnl.it'+(u[len(BASE):] if u else path)
        it.append(e)
    g=[{'@type':'BreadcrumbList','itemListElement':it}]+(extra or [])
    return '<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@graph':g},ensure_ascii=False).replace('</','<\\/')+'</script>'
def faq(qs):
    return {'@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':re.sub('<[^>]+>','',a)}} for q,a in qs]}
def faqhtml(qs):
    return '<h2>Domande frequenti</h2>'+''.join(f'<h3>{E(q)}</h3><p>{a}</p>' for q,a in qs)
def page(title,desc,path,color,body,crumbs,extra=None):
    rob='<meta name="robots" content="noindex, nofollow">' if NOINDEX else '<meta name="robots" content="index, follow">'
    cr=' › '.join(f'<a href="{u}">{E(t)}</a>' if u else E(t) for t,u in crumbs)
    return f'''<!DOCTYPE html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">{rob}<link rel="canonical" href="https://stipendioccnl.it{path}"><meta property="og:type" content="website"><meta property="og:locale" content="it_IT"><meta property="og:site_name" content="stipendioccnl"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="https://stipendioccnl.it{path}"><meta property="og:image" content="https://stipendioccnl.it/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#ffffff">{ld(path,crumbs,extra)}
<script>try{{var t=localStorage.getItem("tema");if(t==="light"||t==="dark")document.documentElement.setAttribute("data-theme",t)}}catch(e){{}}</script><style>{CSS}:root{{--b:{color}}}</style></head><body>
<header><div class="w"><a href="{BASE}/" aria-label="stipendioccnl" style="display:flex;align-items:center"><svg style="margin-right:8px;flex:none" viewBox="0 0 120 120" width="26" height="26" aria-hidden="true"><rect x="14" y="8" width="76" height="102" rx="10" style="fill:var(--ink)"/><rect x="26" y="24" width="52" height="7" rx="3.5" style="fill:var(--card);opacity:.45"/><rect x="26" y="40" width="52" height="7" rx="3.5" style="fill:var(--card);opacity:.45"/><rect x="26" y="58" width="34" height="10" rx="4" fill="#2f8a5f"/><path d="M86.0,59.0L91.7,64.7L99.5,62.6L101.6,70.4L109.4,72.5L107.3,80.3L113.0,86.0L107.3,91.7L109.4,99.5L101.6,101.6L99.5,109.4L91.7,107.3L86.0,113.0L80.3,107.3L72.5,109.4L70.4,101.6L62.6,99.5L64.7,91.7L59.0,86.0L64.7,80.3L62.6,72.5L70.4,70.4L72.5,62.6L80.3,64.7Z" fill="#2f8a5f" style="stroke:var(--card)" stroke-width="4" stroke-linejoin="round"/><path d="M76 86l7 7 13-14" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>stipendio<span style="font-weight:500;color:var(--mu)">ccnl</span></a><nav><a href="{BASE}/stipendio-netto/">Stipendi per CCNL</a><a href="{BASE}/">Calcolatore</a><button class="theme-btn" id="theme-toggle" type="button" aria-label="Cambia tema: dispositivo, chiaro o scuro">Tema: auto</button></nav></div></header>
<main class="w"><div class="crumb">{cr}</div>{body}</main>
<footer><div class="w">Stime 2026 con IRPEF 23-33-43%, INPS 9,19% (dipendenti statali 9,15%), addizionali regionale 1,73% e comunale 0,8% (medie), senza familiari a carico né fondi integrativi. Non sostituiscono la busta paga.<br><a href="{BASE}/note-legali/">Note legali</a> &nbsp; <a href="{BASE}/privacy/">Privacy e cookie</a> &nbsp; <a href="mailto:info@stipendioccnl.it">info@stipendioccnl.it</a></div></footer><script>(function(){{var M=["auto","light","dark"],N={{auto:"auto",light:"chiaro",dark:"scuro"}},b=document.getElementById("theme-toggle"),r=document.documentElement,m=Math.max(0,M.indexOf(r.getAttribute("data-theme")||"auto"));function s(){{b.textContent="Tema: "+N[M[m]]}}b.onclick=function(){{m=(m+1)%3;if(M[m]==="auto")r.removeAttribute("data-theme");else r.setAttribute("data-theme",M[m]);try{{M[m]==="auto"?localStorage.removeItem("tema"):localStorage.setItem("tema",M[m])}}catch(e){{}}s()}};s()}})()</script></body></html>'''
def write(rel,txt):
    p=os.path.join(OUT,rel); os.makedirs(os.path.dirname(p),exist_ok=True); open(p,'w').write(txt)

MESI={'gen':'Gen','feb':'Feb','mar':'Mar','apr':'Apr','mag':'Mag','giu':'Giu','lug':'Lug','ago':'Ago','set':'Set','ott':'Ott','nov':'Nov','dic':'Dic'}
def mref(h):
    import re
    w=re.findall(r'[a-zA-Z]{3}|\d{4}',h.lower().replace('da ',''))
    return MESI[w[0]]+' '+w[-1]
TOG='<div class="tog" role="group" aria-label="Periodo"><button type="button" class="on" data-p="m">Mensile</button><button type="button" data-p="a">Annuale</button></div>'
TJS="<script>document.querySelectorAll('.tog button').forEach(b=>b.onclick=()=>{document.querySelectorAll('.tog button').forEach(x=>x.classList.toggle('on',x===b));document.querySelectorAll('[data-m]').forEach(t=>t.textContent=t.dataset[b.dataset.p])})</script>"
def trhead(c,first=True):
    a=''.join(f'<th class="n c{" fut" if f else ""}" colspan="2">{E(h)}</th>' for h,f in c['trh'])
    b=''.join(f'<th class="n s lo{" fut" if f else ""}">Lordo</th><th class="n s ne{" fut" if f else ""}">Netto</th>' for h,f in c['trh'])
    return (f'<tr><th rowspan="2">Livello</th>{a}</tr><tr>{b}</tr>' if first else f'<tr>{a}</tr><tr>{b}</tr>')
def trcells(l,c):
    return ''.join(f'<td class="n lo{" fut" if f else ""}" data-m="{eur(t[0])}" data-a="{eur(t[2])}">{eur(t[0])}</td><td class="n ne{" fut" if f else ""}" data-m="{eur(t[1])}" data-a="{eur(t[3])}">{eur(t[1])}</td>' for t,(h,f) in zip(l['tr'],c['trh']))
urls=[]; hub_items=[]
for c in D:
    k=c['k']; cs=SLUG[k]; col=TEMI.get(k,'#0f5c4d'); sh=SHORT[k]; code=CNEL.get(k)
    off=(f'<div class="box"><b>Contratto ufficiale.</b> Il testo del CCNL è depositato nell\'archivio del CNEL, codice <b>{code}</b>: <a href="{ARCH}" rel="noopener">cercalo nell\'archivio CNEL</a>.</div>' if code else
         f'<div class="box"><b>Contratto ufficiale.</b> I CCNL sono depositati nell\'<a href="{ARCH}" rel="noopener">archivio del CNEL</a>.</div>')
    rows=''.join(f'<tr><td><a href="{BASE}/stipendio-netto/{cs}/{lvslug(l["n"])}/">{E(l["n"])}</a></td>{trcells(l,c)}</tr>' for l in c['lv'])
    body=f'''<h1>Stipendio netto {E(sh)} 2026: tutti i livelli</h1>
<p class="lead">{E(c["nome"])}: minimi in vigore, RAL e netto in busta per ogni livello, con {MENS(c["mens"])} mensilità. {E(c["fonte"])}.</p>
{TOG}<div class="tw"><table class="trt"><thead>{trhead(c)}</thead><tbody>{rows}</tbody></table></div>
<a class="cta" href="{BASE}/?ccnl={k}">Calcola il tuo netto {E(sh)}</a>
<p class="note">Il netto è quello di una busta ordinaria. Con superminimo, scatti, indennità o fondi integrativi usa il calcolatore.</p>{off}{TJS}'''
    lo=min(c['lv'],key=lambda x:x['netM']); hi=max(c['lv'],key=lambda x:x['netM'])
    qs=[(f'Quanto si prende netto con il CCNL {sh} nel 2026?',f'Con i minimi in vigore il netto in busta va da circa {eur(lo["netM"])} al mese ({E(lo["n"])}) a circa {eur(hi["netM"])} ({E(hi["n"])}), in una busta ordinaria senza familiari a carico.'),
        (f'Quante mensilità prevede il CCNL {sh}?',f'Il contratto prevede {MENS(c["mens"])} mensilità: la RAL minima è il minimo mensile moltiplicato per il numero di mensilità.'),
        (f'Quanto è la tredicesima netta con il CCNL {sh}?',f'Con i minimi 2026 va da circa {eur(min(x["t13n"] for x in c["lv"]))} a {eur(max(x["t13n"] for x in c["lv"]))} netti, per un anno intero di lavoro. Gli importi livello per livello sono nella <a href="{BASE}/tredicesima-netta/#{cs}">tabella della tredicesima netta</a>.'),
        ('Il netto indicato comprende scatti e superminimo?','No: è calcolato sul minimo contrattuale. Scatti di anzianità, superminimo, straordinari e addizionali del tuo comune lo cambiano; puoi inserirli nel calcolatore.')]
    body+=faqhtml(qs)
    write(f'stipendio-netto/{cs}/index.html',page(fit(f'Stipendio netto {sh} 2026 per livello'),f'Netto in busta 2026 con il CCNL {sh}: da {eur(lo["netM"])} a {eur(hi["netM"])} al mese. Minimi, RAL e netto per ogni livello, con IRPEF, INPS e addizionali.',f'/stipendio-netto/{cs}/',col,body,[('Stipendi per CCNL',f'{BASE}/stipendio-netto/'),(sh,None)],[faq(qs)]))
    urls.append(f'/stipendio-netto/{cs}/'); hub_items.append((sh,cs,c))
    for l in c['lv']:
        ln=lvname(l['n']); ls=lvslug(l['n'])
        others=''.join(f'<li><a href="{BASE}/stipendio-netto/{cs}/{lvslug(o["n"])}/">{E(o["n"])}</a></li>' for o in c['lv'] if o['i']!=l['i'])
        tr=lambda a,b,cl='':f'<tr class="{cl}"><td>{a}</td><td class="n">{b}</td></tr>'
        det=(tr('Lordo annuo (RAL minima)',eur(l['ral']))+tr('Contributi INPS','− '+eur(l['inps']))+tr('IRPEF netta','− '+eur(l['irpef']))+
             tr('Addizionali regionale e comunale','− '+eur(l['add']))+(tr('Taglio del cuneo e trattamento integrativo','+ '+eur(l['bonus'])) if l['bonus']>0.5 else '')+tr('Netto annuo',eur(l['netA']),'me'))
        body=f'''<h1>Stipendio netto {E(sh)} {E(ln)} 2026</h1>
<p class="lead">Con il CCNL {E(c["nome"])}, al {E(ln)} la retribuzione minima è di {eur(l["min"],2)} lordi al mese per {MENS(c["mens"])} mensilità{(", più "+eur(l["acc"],2)+" di "+l["al"]+" per 12 mensilità") if l.get("acc") else ""}: circa <b>{eur(l["netM"])} netti</b> in una busta ordinaria.</p>
<div class="hero"><div class="big"><span>Netto in busta</span><b>{eur(l["netM"])}</b></div><div><span>Lordo mensile</span><b>{eur(l["min"]+l.get("acc",0))}</b></div><div><span>Netto annuo</span><b>{eur(l["netA"])}</b></div></div>
<h2>Lordo e netto per mese di decorrenza</h2>{TOG}<div class="tw"><table class="trt"><thead>{trhead(c,False)}</thead><tbody><tr>{trcells(l,c)}</tr></tbody></table></div>{TJS}
<h2>Dal lordo al netto in un anno</h2><table><tbody>{det}</tbody></table>
<a class="cta" href="{BASE}/?ccnl={k}&amp;livello={l["i"]}">Calcola con il tuo comune e i tuoi dati</a>
<p class="note">Stima sul minimo contrattuale: superminimo, scatti di anzianità, straordinari, fondo pensione e addizionali del tuo comune cambiano il risultato. Nel calcolatore li trovi tutti.</p>
{off}'''
        qs=[(f'Quanto si prende netto al {ln} del CCNL {sh}?',f'Circa {eur(l["netM"])} al mese in una busta ordinaria del 2026, su un minimo di {eur(l["min"],2)} lordi. In un anno il netto è di circa {eur(l["netA"])}.'),
            (f'Qual è la RAL minima del {ln} {sh}?',f'La RAL minima è di {eur(l["ral"])}, cioè il minimo mensile per {MENS(c["mens"])} mensilità{" più le voci pagate su 12 mesi" if l.get("acc") else ""}.'),
            (f'Quanto è la tredicesima netta al {ln} {sh}?',f'Circa {eur(l["t13n"])} netti su {eur(l["t13l"])} lordi, per un anno intero di lavoro. Sulla tredicesima si pagano INPS e IRPEF ma non si applicano le detrazioni, che sono già nelle buste ordinarie: per questo il netto è più basso di quello di un mese normale.'+(' La quattordicesima di luglio ha un importo simile.' if c['mens']==14 else '')+f' <a href="{BASE}/tredicesima-netta/#{cs}">Come si calcola la tredicesima</a>.'),
            ('Perché il mio netto può essere diverso?','La stima usa il minimo contrattuale e le addizionali medie. Superminimo, scatti, straordinari, familiari a carico, fondo pensione e il tuo comune cambiano il risultato.')]
        body+=faqhtml(qs)+f'<h2>Altri livelli {E(sh)}</h2><ul class="lv">{others}</ul>'
        tt=f'Stipendio netto {sh} {ln} 2026: {eur(l["netM"])}'
        for alt in (f'Netto {sh} {ln} 2026: {eur(l["netM"])}',f'Stipendio {corto(ln)[:1].lower()+corto(ln)[1:]} 2026: {eur(l["netM"])}',f'{corto(ln)} 2026: {eur(l["netM"])} netti',f'{corto(ln)}: {eur(l["netM"])} netti'):
            if len(tt)>60: tt=alt
        dd=f'CCNL {sh}, {ln}: minimo {eur(l["min"],2)} lordi al mese, circa {eur(l["netM"])} netti in busta nel 2026.'
        if len(dd)>160: dd=f'{sh}, {ln}: {eur(l["min"],2)} lordi, circa {eur(l["netM"])} netti al mese nel 2026.'
        if len(dd)+39<=160: dd+=' Calcolo con IRPEF, INPS e addizionali.'
        write(f'stipendio-netto/{cs}/{ls}/index.html',page(fit(tt),
            dd,
            f'/stipendio-netto/{cs}/{ls}/',col,body,[('Stipendi per CCNL',f'{BASE}/stipendio-netto/'),(sh,f'{BASE}/stipendio-netto/{cs}/'),(l['n'],None)],[faq(qs)]))
        urls.append(f'/stipendio-netto/{cs}/{ls}/')

AGG='16 novembre 2026'
priv=f"""<h1>Privacy e cookie</h1><p class="lead">Informativa ai sensi degli artt. 13 e 14 del Regolamento UE 2016/679 (GDPR). Ultimo aggiornamento: {AGG}.</p>
<h2>Titolare del trattamento</h2><p>Il gestore di stipendioccnl.it. Contatto: <a href="mailto:info@stipendioccnl.it">info@stipendioccnl.it</a>.</p>
<h2>Quali dati raccoglie il sito</h2><p>Nessuno, attraverso il calcolatore. Il sito non ha account, moduli di registrazione o newsletter. I valori che inserisci (RAL, CCNL, comune, familiari, straordinari e gli altri campi) sono elaborati solo nel tuo browser e non vengono inviati a nessun server.</p>
<p>Se attivi l'opzione per ricordare i dati, il browser li salva sul tuo dispositivo nell'archiviazione locale (localStorage), con le chiavi <code>ln-dati</code> e <code>ln-comune</code>. Il sito salva allo stesso modo la scelta del tema chiaro o scuro, con la chiave <code>tema</code>. Questi dati restano sul tuo dispositivo: puoi cancellarli con il pulsante nel calcolatore o dalle impostazioni del browser.</p>
<h2>Hosting e dati tecnici</h2><p>Il sito è ospitato su GitHub Pages, servizio di GitHub, Inc. Come ogni server web, GitHub può registrare dati tecnici delle visite, come l'indirizzo IP, per motivi di sicurezza e di funzionamento del servizio. Il titolare non ha accesso a questi dati e non li usa. GitHub tratta i dati secondo la propria <a href="https://docs.github.com/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener">informativa sulla privacy</a>, anche con trasferimenti verso gli Stati Uniti basati sulle garanzie previste dal GDPR.</p>
<h2>Se scrivi a info@</h2><p>Se mandi un'email a info@stipendioccnl.it, il titolare usa il tuo indirizzo e il contenuto del messaggio solo per risponderti, sulla base della tua richiesta (art. 6.1.b GDPR). La posta è gestita tramite Aruba S.p.A. e Google (Gmail). I messaggi sono conservati per il tempo necessario a gestire la richiesta e poi cancellati.</p>
<h2>Cookie</h2><p>Il sito non usa cookie di profilazione, cookie pubblicitari, strumenti di statistica o contenuti di terze parti che installano cookie. L'archiviazione locale descritta sopra è tecnica, serve solo a funzioni che scegli tu e non richiede il consenso (art. 122 del Codice privacy e Linee guida del Garante del 10 giugno 2021). Per questo non c'è un banner dei cookie.</p><p>Se in futuro saranno aggiunti statistiche o pubblicità con cookie, questa pagina sarà aggiornata e ti verrà chiesto il consenso prima di attivarli.</p>
<h2>I tuoi diritti</h2><p>Puoi chiedere al titolare l'accesso ai tuoi dati, la rettifica, la cancellazione, la limitazione del trattamento e la portabilità, e puoi opporti al trattamento (artt. 15-22 GDPR), scrivendo a <a href="mailto:info@stipendioccnl.it">info@stipendioccnl.it</a>. Puoi anche presentare reclamo al <a href="https://www.garanteprivacy.it" rel="noopener">Garante per la protezione dei dati personali</a>.</p>"""
write('privacy/index.html',page('Privacy e cookie | stipendioccnl','Informativa privacy e cookie di stipendioccnl.it: nessun dato raccolto, nessun cookie di profilazione.','/privacy/','#16191d',priv,[('Privacy e cookie',None)]))
note=f"""<h1>Note legali</h1><p class="lead">Ultimo aggiornamento: {AGG}.</p>
<h2>Chi gestisce il sito</h2><p>stipendioccnl.it è un progetto personale e gratuito. Contatto: <a href="mailto:info@stipendioccnl.it">info@stipendioccnl.it</a>. Il sito non è collegato a sindacati, associazioni dei datori di lavoro, enti pubblici o al CNEL.</p>
<h2>Natura delle informazioni</h2><p>I calcoli e le tabelle sono stime a scopo informativo, basate sulle norme fiscali e contributive e sui minimi dei CCNL indicati nella sezione Fonti del calcolatore. Non sono una consulenza fiscale, contributiva o del lavoro e non sostituiscono la busta paga, il datore di lavoro, un consulente del lavoro, un commercialista o un CAF.</p>
<p>La retribuzione reale può essere diversa per molte ragioni: accordi aziendali, superminimi, scatti di anzianità, conguagli, detrazioni personali, addizionali del tuo comune, fondi e assistenza sanitaria, periodi lavorati e altro ancora.</p>
<h2>Limitazione di responsabilità</h2><p>Il gestore cura i contenuti con attenzione e li aggiorna quando cambiano le norme o i contratti, ma non garantisce che siano completi, esatti o aggiornati. Il gestore non risponde di decisioni prese sulla base dei risultati del sito: prima di decidere su offerte di lavoro, contratti o pagamenti, verifica i numeri con un professionista.</p>
<h2>Segnalazioni</h2><p>Se trovi un errore o un CCNL non aggiornato, scrivi a <a href="mailto:info@stipendioccnl.it">info@stipendioccnl.it</a>: le segnalazioni sono utili e vengono verificate.</p>
<h2>Link esterni</h2><p>I link a siti di terzi, come le fonti normative, sono forniti per comodità. Il gestore non controlla quei siti e non risponde dei loro contenuti.</p>
<h2>Contenuti</h2><p>Testi, calcolatore e grafica del sito sono del gestore di stipendioccnl.it. Le norme e i testi dei contratti collettivi citati appartengono ai rispettivi autori.</p>"""
write('note-legali/index.html',page('Note legali | stipendioccnl','Chi gestisce stipendioccnl.it, natura delle stime e limitazione di responsabilità.','/note-legali/','#16191d',note,[('Note legali',None)]))

cards=''.join(f'<tr><td><a href="{BASE}/stipendio-netto/{cs}/">{E(sh)}</a></td><td>{E(c["nome"])}</td><td class="n">{len(c["lv"])}</td></tr>' for sh,cs,c in hub_items)
body=f'''<h1>Stipendio netto 2026 per contratto e livello</h1><p class="lead">Scegli il tuo CCNL: per ogni livello trovi minimo, RAL e netto in busta.</p>
<table><thead><tr><th>CCNL</th><th>Contratto</th><th class="n">Livelli</th></tr></thead><tbody>{cards}</tbody></table>
<a class="cta" href="{BASE}/">Vai al calcolatore</a>
<h2>Come trovare il tuo CCNL e il tuo livello</h2>
<p>Il contratto collettivo applicato è scritto nella lettera di assunzione e, quasi sempre, nell'intestazione della busta paga, insieme al livello di inquadramento. Se non lo trovi, chiedi all'ufficio del personale: il datore di lavoro è tenuto a indicarlo. Il codice del contratto nell'archivio del CNEL compare anche nelle comunicazioni obbligatorie di assunzione.</p>
<h2>Cosa mostrano queste tabelle</h2>
<p>Per ogni livello trovi il minimo contrattuale mensile, la RAL minima (il minimo moltiplicato per le mensilità del contratto) e il netto di una busta ordinaria del 2026. Il netto tiene conto dei contributi INPS a carico del dipendente, dell'IRPEF con le aliquote 23, 33 e 43%, delle detrazioni per lavoro dipendente, delle addizionali regionale e comunale medie e del taglio del cuneo fiscale.</p>
<p>Quando un rinnovo prevede aumenti scaglionati, le tabelle mostrano anche le tranche future, così vedi quanto cambierà il netto dal mese di decorrenza.</p>
<h2>Perché il tuo netto può essere diverso</h2>
<p>Le cifre si riferiscono al minimo, senza familiari a carico. Per la mensilità di dicembre c'è la <a href="{BASE}/tredicesima-netta/">tabella della tredicesima netta</a> per ogni CCNL e livello. Superminimo, scatti di anzianità, indennità, straordinari, fondo pensione e le addizionali del tuo comune cambiano il risultato: nel calcolatore puoi inserirli tutti e ottenere il netto mese per mese, la tredicesima e la quattordicesima.</p>'''
qs=[('Dove trovo il CCNL che mi viene applicato?',"Nella lettera di assunzione e nell'intestazione della busta paga, insieme al livello. In caso di dubbio chiedi all'ufficio del personale."),
    ('Il netto delle tabelle è quello che ricevo in busta?','È il netto di una busta ordinaria sul minimo contrattuale, senza familiari a carico. Superminimo, scatti, straordinari e addizionali del tuo comune lo cambiano.')]
body+=faqhtml(qs)
write('stipendio-netto/index.html',page('Stipendio netto 2026 per CCNL e livello | stipendioccnl','Netto in busta 2026 per i principali CCNL italiani, livello per livello: minimi, RAL e netto mensile, con le tranche dei rinnovi.','/stipendio-netto/','#0f5c4d',body,[('Stipendi per CCNL',None)],[faq(qs)]))
urls.insert(0,'/stipendio-netto/')
exec(open('/home/claude/build/tredicesima.py').read())
json.dump(urls,open('/home/claude/build/urls.json','w'))
tree=''.join(f'<details class="tree"><summary><a href="stipendio-netto/{cs}/">{E(sh)}</a><small>{len(c["lv"])} livelli</small></summary><ul class="lv">'+''.join(f'<li><a href="stipendio-netto/{cs}/{lvslug(l["n"])}/">{E(l["n"])}</a></li>' for l in c['lv'])+'</ul></details>' for sh,cs,c in hub_items)
open('/home/claude/build/tree.html','w').write(tree)
print(len(urls),'pagine')
