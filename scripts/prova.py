"""Pagine "periodo di prova" per CCNL (/stipendio-netto/<slug>/periodo-di-prova/) e pagina di confronto /periodo-di-prova/.
Dati in data/prova.json, ricavati dai testi dei CCNL (articolo e link in ogni voce). Idempotente."""
import json, re, html as H
from pathlib import Path
R = Path(__file__).resolve().parent.parent
D = json.loads((R / "data/prova.json").read_text())
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
          "<li>Il patto di prova deve essere scritto nella lettera di assunzione, prima di iniziare. Senza, la prova non vale.</li>"
          "<li>Le durate del contratto sono massime: la lettera può prevederne una più breve, mai più lunga.</li>"
          "<li>Durante la prova ciascuna parte può chiudere il rapporto senza preavviso. Ti spettano comunque i giorni lavorati, il TFR e i ratei di tredicesima e ferie.</li>"
          "<li>Malattia, infortunio e congedo di maternità o paternità sospendono la prova, che riprende al rientro.</li></ul>")
urls = []
righe_hub = []
for slug, c in D.items():
    url = f"https://stipendioccnl.it/stipendio-netto/{slug}/periodo-di-prova/"
    breve = c["nome"].split(" (")[0]
    first, last = c["righe"][0], c["righe"][-1]
    title = f"Periodo di prova CCNL {breve} 2026: durata per livello"
    desc = f"Periodo di prova nel CCNL {c['nome']}: {first[0]} {first[1]}, {last[0]} {last[1]}. Tabella per livello con l'articolo del contratto."
    faq = [(f"Quanto dura il periodo di prova nel CCNL {breve}?", "; ".join(f"{a}: {b}" for a, b in c["righe"]) + "."),
           ("Durante la prova posso essere licenziato?", "Sì, ciascuna parte può chiudere il rapporto senza preavviso, ma ti spettano i giorni lavorati, il TFR e i ratei di tredicesima e ferie.")]
    tab = "".join(f"<tr><td>{e(a)}</td><td><b>{e(b)}</b></td></tr>" for a, b in c["righe"])
    main = (f'<main class="w"><div class="crumb"><a href="/stipendio-netto/">Stipendi per CCNL</a> › <a href="/stipendio-netto/{slug}/">{e(breve)}</a> › Periodo di prova</div>'
            f"<h1>Periodo di prova nel CCNL {e(c['nome'])}</h1>"
            f'<p class="lead">La durata massima dipende dal livello: da <b>{e(last[1])}</b> per {e(last[0])} a <b>{e(first[1])}</b> per {e(first[0])}.</p>'
            f"<table><thead><tr><th>Livello</th><th>Durata massima</th></tr></thead><tbody>{tab}</tbody></table>"
            f'<p class="note">{e(c["note"])} Fonte: <a href="{H.escape(c["url"])}" rel="noopener">{e(c["fonte"])}</a>.</p>'
            + COMUNE +
            f'<p>Quanto prendi durante la prova? Lo stipendio è quello del tuo livello: <a href="/stipendio-netto/{slug}/">stipendio netto CCNL {e(breve)}</a>. '
            f'<a href="/periodo-di-prova/">Confronta il periodo di prova negli altri contratti</a>.</p>'
            "<h2>Domande frequenti</h2>" + "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in faq) + "</main>")
    crumbs = [("Home", "https://stipendioccnl.it/"), ("Stipendi per CCNL", "https://stipendioccnl.it/stipendio-netto/"),
              (breve, f"https://stipendioccnl.it/stipendio-netto/{slug}/"), ("Periodo di prova", url)]
    out = R / f"stipendio-netto/{slug}/periodo-di-prova"; out.mkdir(exist_ok=True)
    (out / "index.html").write_text(head(url, title, desc, crumbs, faq) + main + TAIL)
    urls.append(url)
    righe_hub.append(f'<tr><td><a href="/stipendio-netto/{slug}/periodo-di-prova/">{e(breve)}</a></td><td>{e(last[0])}: {e(last[1])}</td><td>{e(first[0])}: {e(first[1])}</td></tr>')
    # link dalla pagina del CCNL
    p = R / f"stipendio-netto/{slug}/index.html"; s = p.read_text()
    if "/periodo-di-prova/" not in s:
        s = s.replace("</main>", f'<p><a href="/stipendio-netto/{slug}/periodo-di-prova/">Periodo di prova nel CCNL {e(breve)}</a></p></main>', 1)
        p.write_text(s)
# pagina di confronto
url = "https://stipendioccnl.it/periodo-di-prova/"
title = "Periodo di prova 2026: quanto dura in ogni CCNL"
desc = "Durata massima del periodo di prova nei principali contratti collettivi, livello per livello, con l'articolo del CCNL e le regole che valgono sempre."
faq = [("Quanto dura al massimo il periodo di prova?", "Lo stabilisce il CCNL in base al livello. Per legge non può superare 6 mesi."),
       ("Il periodo di prova deve essere scritto?", "Sì, il patto di prova deve risultare per iscritto nella lettera di assunzione, altrimenti non vale.")]
main = ('<main class="w"><div class="crumb">Periodo di prova</div><h1>Periodo di prova: quanto dura in ogni CCNL</h1>'
        '<p class="lead">Il periodo di prova massimo lo fissa il contratto collettivo in base al livello, e per legge non può superare 6 mesi. Scegli il tuo CCNL per la tabella completa.</p>'
        '<table><thead><tr><th>CCNL</th><th>Prova più breve</th><th>Prova più lunga</th></tr></thead><tbody>' + "".join(righe_hub) + "</tbody></table>"
        + COMUNE + "<h2>Domande frequenti</h2>" + "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in faq) + "</main>")
out = R / "periodo-di-prova"; out.mkdir(exist_ok=True)
(out / "index.html").write_text(head(url, title, desc, [("Home", "https://stipendioccnl.it/"), ("Periodo di prova", url)], faq) + main + TAIL)
urls.append(url)
sm = (R / "sitemap.xml").read_text()
add = "".join(f"<url><loc>{u}</loc><lastmod>2026-11-26</lastmod></url>\n" for u in urls if u not in sm)
if add: (R / "sitemap.xml").write_text(sm.replace("</urlset>", add + "</urlset>"))
si = json.loads((R / "search-index.json").read_text())
if not any(x[1] == "/periodo-di-prova/" for x in si):
    si.append(["Periodo di prova per CCNL", "/periodo-di-prova/", 1]); (R / "search-index.json").write_text(json.dumps(si, ensure_ascii=False, separators=(",", ":")))
print(len(urls), "pagine")
