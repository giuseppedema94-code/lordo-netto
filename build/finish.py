# Passi finali della build: sitemap con lastmod, llms.txt, controllo SEO bloccante
import os, re, sys, json, html as H, datetime
ROOT = '/home/claude/lordo-netto'
oggi = datetime.date.today().isoformat()
urls = ['/'] + ['/note-legali/', '/privacy/'] + json.load(open('/home/claude/build/urls.json'))
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sm += ''.join(f'<url><loc>https://stipendioccnl.it{u}</loc><lastmod>{oggi}</lastmod></url>\n' for u in urls) + '</urlset>\n'
open(f'{ROOT}/sitemap.xml', 'w').write(sm)

# llms.txt: mappa del sito per assistenti AI
D = json.load(open('/home/claude/build/pages.json'))
sys.path.insert(0, '/home/claude/build')
righe = []
for u in urls:
    if u.count('/') == 3 and u.startswith('/stipendio-netto/'):
        t = open(f'{ROOT}{u}index.html', encoding='utf-8').read()
        h1 = H.unescape(re.search(r'<h1>(.*?)</h1>', t).group(1))
        d = H.unescape(re.search(r'<meta name="description" content="(.*?)"', t).group(1))
        righe.append(f'- [{h1}](https://stipendioccnl.it{u}): {d}')
llms = f'''# stipendioccnl.it

> Calcolatore gratuito dello stipendio netto 2026 in Italia, da lordo a netto e da netto a lordo, con i minimi dei principali CCNL. Regole 2026: IRPEF 23-33-43%, contributi INPS del dipendente 9,19% (statali 9,15%), addizionali regionali e comunali, taglio del cuneo fiscale, trattamento integrativo. I calcoli girano nel browser e nessun dato viene inviato.

## Strumenti
- [Calcolatore lordo-netto](https://stipendioccnl.it/): netto mensile e annuo da RAL o da CCNL e livello, con comune, familiari, straordinari, scatti, fondi.
- [Costo azienda](https://stipendioccnl.it/#costo): costo del lavoro per il datore.
- [Netto a lordo](https://stipendioccnl.it/#netto-lordo): RAL necessaria per un netto desiderato.
- [Confronto offerte](https://stipendioccnl.it/#confronta): due offerte di lavoro a confronto sul netto.

## Stipendi per CCNL e livello
- [Indice dei CCNL](https://stipendioccnl.it/stipendio-netto/)
{chr(10).join(righe)}

## Note
Le cifre sono stime sul minimo contrattuale, senza familiari a carico; non sostituiscono la busta paga. Aggiornato il {oggi}. Contatto: info@stipendioccnl.it
'''
open(f'{ROOT}/llms.txt', 'w').write(llms)

# controllo SEO su tutte le pagine: errori bloccano la build
err, warn = [], []
viste = {}
for u in urls:
    p = f'{ROOT}{u}index.html'
    t = open(p, encoding='utf-8').read()
    ti = re.findall(r'<title>(.*?)</title>', t)
    de = re.findall(r'<meta name="description" content="(.*?)"', t)
    h1 = re.findall(r'<h1[^>]*>', t)
    ca = re.findall(r'<link rel="canonical" href="(.*?)"', t)
    if len(ti) != 1: err.append(f'{u}: titoli {len(ti)}')
    elif len(H.unescape(ti[0])) > 60: warn.append(f'{u}: titolo {len(H.unescape(ti[0]))} car.')
    if len(de) != 1: err.append(f'{u}: descrizioni {len(de)}')
    elif not 70 <= len(H.unescape(de[0])) <= 160: warn.append(f'{u}: descrizione {len(H.unescape(de[0]))} car.')
    if len(h1) != 1: err.append(f'{u}: h1 {len(h1)}')
    if ca != [f'https://stipendioccnl.it{u}']: err.append(f'{u}: canonical {ca}')
    if 'noindex' in t: err.append(f'{u}: noindex')
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        try: json.loads(b.replace('<\\/', '</'))
        except Exception as e: err.append(f'{u}: JSON-LD non valido ({e})')
    if ti: viste.setdefault(ti[0], []).append(u)
for k, v in viste.items():
    if len(v) > 1: err.append(f'titolo duplicato su {len(v)} pagine: {k}')
print(f'SEO: {len(urls)} pagine, {len(err)} errori, {len(warn)} avvisi')
for x in warn[:20]: print('  avviso', x)
for x in err: print('  ERRORE', x)
sys.exit(1 if err else 0)
