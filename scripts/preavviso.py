"""Pagine "preavviso" per CCNL (/stipendio-netto/<slug>/preavviso/) e pagina di confronto /preavviso/.
Dati in data/preavviso.json, ricavati dai testi dei CCNL (articolo e link in ogni voce). Idempotente."""
import json, re, html as H
from pathlib import Path
R = Path(__file__).resolve().parent.parent
D = json.loads((R / "data/preavviso.json").read_text())
tpl = (R / "tredicesima-netta/index.html").read_text()
HEAD, TAIL = tpl[:tpl.find("<main")], tpl[tpl.find("</main>") + 7:]
e = lambda s: H.escape(s, quote=False)
def head(url, title, desc, crumbs, faq):
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]}
    h = re.sub(r"<title>.*?</title>", f"<title>{e(title)}</title>", HEAD, count=1)
    for k in ('name="description"', 'property="og:description"'):
        h = re.sub(r'(<meta ' + k + r' content=")[^"]*', lambda m: m.group(1) + H.escape(desc), h, count=1)
    h = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + H.escape(title), h, count=1)
    h = h.replace("https://stipendioccnl.it/tredicesima-netta/", url)
    return re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>", h, count=1, flags=re.S)
COMUNE = ("<h2>Regole che valgono sempre</h2><ul>"
          "<li>Il preavviso non si applica durante il periodo di prova né in caso di licenziamento per giusta causa.</li>"
          "<li>Chi non rispetta il preavviso paga all'altra parte un'indennità pari alla retribuzione dei giorni mancanti.</li>"
          "<li>Le ferie non si possono far rientrare nel periodo di preavviso (art. 2109 c.c.).</li>"
          "<li>Le dimissioni vanno date online con la procedura del Ministero del Lavoro, tranne che nel lavoro domestico e durante il periodo di prova.</li></ul>")
urls = []
righe_hub = []
for slug, c in D.items():
    url = f"https://stipendioccnl.it/stipendio-netto/{slug}/preavviso/"
    breve = c["nome"].split(" (")[0]
    title = f"Preavviso dimissioni e licenziamento CCNL {breve} 2026"
    desc = f"Giorni di preavviso nel CCNL {c['nome']}: {c['sintesi']} secondo livello e anzianità, per dimissioni e licenziamento. Tabella con l'articolo del contratto."
    t0 = c["tabelle"][0]
    faq = [(f"Quanti giorni di preavviso servono nel CCNL {breve}?", f"Dipende da livello e anzianità: {c['sintesi']}. " + c["note"].split(". ")[0] + "."),
           ("Cosa succede se non do il preavviso?", "L'azienda può trattenere dall'ultima busta paga l'indennità di mancato preavviso, pari alla retribuzione dei giorni non lavorati.")]
    tabs = ""
    for t in c["tabelle"]:
        tabs += f"<h2>{e(t['titolo'])}</h2><table><thead><tr>" + "".join(f"<th>{e(x)}</th>" for x in t["cols"]) + "</tr></thead><tbody>" + "".join("<tr>" + "".join(f"<td>{e(x)}</td>" for x in r) + "</tr>" for r in t["righe"]) + "</tbody></table>"
    main = (f'<main class="w"><div class="crumb"><a href="/stipendio-netto/">Stipendi per CCNL</a> › <a href="/stipendio-netto/{slug}/">{e(breve)}</a> › Preavviso</div>'
            f"<h1>Preavviso nel CCNL {e(c['nome'])}</h1>"
            f'<p class="lead">Il preavviso va <b>{e(c["sintesi"])}</b> secondo livello e anzianità di servizio.</p>' + tabs +
            f'<p class="note">{e(c["note"])} Fonte: <a href="{H.escape(c["url"])}" rel="noopener">{e(c["fonte"])}</a>.</p>'
            + COMUNE +
            f'<p>Quanto vale il preavviso in euro? Parti dallo stipendio del tuo livello: <a href="/stipendio-netto/{slug}/">stipendio netto CCNL {e(breve)}</a>. '
            f'<a href="/preavviso/">Confronta il preavviso negli altri contratti</a>.</p>'
            "<h2>Domande frequenti</h2>" + "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in faq) + "</main>")
    crumbs = [("Home", "https://stipendioccnl.it/"), ("Stipendi per CCNL", "https://stipendioccnl.it/stipendio-netto/"),
              (breve, f"https://stipendioccnl.it/stipendio-netto/{slug}/"), ("Preavviso", url)]
    out = R / f"stipendio-netto/{slug}/preavviso"; out.mkdir(exist_ok=True)
    (out / "index.html").write_text(head(url, title, desc, crumbs, faq) + main + TAIL)
    urls.append(url)
    righe_hub.append(f'<tr><td><a href="/stipendio-netto/{slug}/preavviso/">{e(breve)}</a></td><td>{e(c["sintesi"])}</td></tr>')
    p = R / f"stipendio-netto/{slug}/index.html"; s = p.read_text()
    if "/preavviso/" not in s:
        s = s.replace("</main>", f'<p><a href="/stipendio-netto/{slug}/preavviso/">Preavviso nel CCNL {e(breve)}</a></p></main>', 1)
        p.write_text(s)
# pagina di confronto
url = "https://stipendioccnl.it/preavviso/"
title = "Preavviso dimissioni e licenziamento 2026: giorni per CCNL"
desc = "Quanti giorni di preavviso servono per dimissioni e licenziamento nei principali CCNL, per livello e anzianità, con l'articolo del contratto."
faq = [("Chi decide i giorni di preavviso?", "Il contratto collettivo, in base a livello e anzianità. La legge (art. 2118 c.c.) rinvia al CCNL."),
       ("Il preavviso per le dimissioni è uguale a quello per il licenziamento?", "Dipende dal CCNL: in molti è più breve, in altri (es. metalmeccanici) è uguale.")]
main = ('<main class="w"><div class="crumb">Preavviso</div><h1>Preavviso di dimissioni e licenziamento in ogni CCNL</h1>'
        '<p class="lead">I giorni di preavviso li fissa il contratto collettivo in base a livello e anzianità. Scegli il tuo CCNL per la tabella completa.</p>'
        '<table><thead><tr><th>CCNL</th><th>Preavviso</th></tr></thead><tbody>' + "".join(righe_hub) + "</tbody></table>"
        + COMUNE + "<h2>Domande frequenti</h2>" + "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in faq) + "</main>")
out = R / "preavviso"; out.mkdir(exist_ok=True)
(out / "index.html").write_text(head(url, title, desc, [("Home", "https://stipendioccnl.it/"), ("Preavviso", url)], faq) + main + TAIL)
urls.append(url)
sm = (R / "sitemap.xml").read_text()
add = "".join(f"<url><loc>{u}</loc><lastmod>2026-11-26</lastmod></url>\n" for u in urls if u not in sm)
if add: (R / "sitemap.xml").write_text(sm.replace("</urlset>", add + "</urlset>"))
si = json.loads((R / "search-index.json").read_text())
if not any(x[1] == "/preavviso/" for x in si):
    si.append(["Preavviso per CCNL", "/preavviso/", 1]); (R / "search-index.json").write_text(json.dumps(si, ensure_ascii=False, separators=(",", ":")))
print(len(urls), "pagine")
