"""Pagine "comporto malattia" per CCNL (/stipendio-netto/<slug>/comporto-malattia/) e pagina di confronto /comporto-malattia/.
Dati in data/comporto.json, ricavati dai testi dei CCNL (articolo e link in ogni voce). Idempotente."""
import json, re, html as H
from pathlib import Path
R = Path(__file__).resolve().parent.parent
D = json.loads((R / "data/comporto.json").read_text())
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
          "<li>Il comporto vale solo dopo il periodo di prova.</li>"
          "<li>Gli infortuni sul lavoro e le malattie professionali seguono regole diverse.</li>"
          "<li>Per chi ha una disabilità i giudici chiedono spesso un comporto più lungo o un calcolo diverso: in questo caso rivolgiti a un sindacato o a un legale.</li>"
          "<li>Superato il comporto, l’azienda può licenziare ma deve pagare preavviso e TFR.</li></ul>")
urls = []
righe_hub = []
for slug, c in D.items():
    url = f"https://stipendioccnl.it/stipendio-netto/{slug}/comporto-malattia/"
    breve = c["nome"].split(" (")[0]
    title = f"Comporto malattia CCNL {breve} 2026: quanti giorni"
    desc = f"Periodo di comporto per malattia nel CCNL {c['nome']}: {c['sintesi']} di conservazione del posto. Tabella con l'articolo del contratto."
    t0 = c["tabelle"][0]
    faq = [(f"Quanto dura il comporto nel CCNL {breve}?", f"{c['sintesi'][0].upper()+c['sintesi'][1:]} di conservazione del posto. " + c["note"].split(". ")[0] + "."),
           ("Cosa succede quando finisce il comporto?", "L'azienda può licenziare per superamento del comporto, pagando preavviso e TFR. Prima della scadenza conviene chiedere l'aspettativa, se il CCNL la prevede.")]
    tabs = ""
    for t in c["tabelle"]:
        tabs += f"<h2>{e(t['titolo'])}</h2><table><thead><tr>" + "".join(f"<th>{e(x)}</th>" for x in t["cols"]) + "</tr></thead><tbody>" + "".join("<tr>" + "".join(f"<td>{e(x)}</td>" for x in r) + "</tr>" for r in t["righe"]) + "</tbody></table>"
    main = (f'<main class="w"><div class="crumb"><a href="/stipendio-netto/">Stipendi per CCNL</a> › <a href="/stipendio-netto/{slug}/">{e(breve)}</a> › Comporto malattia</div>'
            f"<h1>Comporto per malattia nel CCNL {e(c['nome'])}</h1>"
            f'<p class="lead">Periodo di comporto, cioè di conservazione del posto durante la malattia: <b>{e(c["sintesi"])}</b>. Superato questo limite l’azienda può licenziare.</p>' + tabs +
            f'<p class="note">{e(c["note"])} Fonte: <a href="{H.escape(c["url"])}" rel="noopener">{e(c["fonte"])}</a>.</p>'
            + COMUNE +
            f'<p>Quanto prendi in malattia? Parti dallo stipendio del tuo livello: <a href="/stipendio-netto/{slug}/">stipendio netto CCNL {e(breve)}</a>. '
            f'<a href="/comporto-malattia/">Confronta il comporto negli altri contratti</a>.</p>'
            "<h2>Domande frequenti</h2>" + "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in faq) + "</main>")
    crumbs = [("Home", "https://stipendioccnl.it/"), ("Stipendi per CCNL", "https://stipendioccnl.it/stipendio-netto/"),
              (breve, f"https://stipendioccnl.it/stipendio-netto/{slug}/"), ("Comporto malattia", url)]
    out = R / f"stipendio-netto/{slug}/comporto-malattia"; out.mkdir(exist_ok=True)
    (out / "index.html").write_text(head(url, title, desc, crumbs, faq) + main + TAIL)
    urls.append(url)
    righe_hub.append(f'<tr><td><a href="/stipendio-netto/{slug}/comporto-malattia/">{e(breve)}</a></td><td>{e(c["sintesi"])}</td></tr>')
    p = R / f"stipendio-netto/{slug}/index.html"; s = p.read_text()
    if "/comporto-malattia/" not in s:
        s = s.replace("</main>", f'<p><a href="/stipendio-netto/{slug}/comporto-malattia/">Comporto per malattia nel CCNL {e(breve)}</a></p></main>', 1)
        p.write_text(s)
# pagina di confronto
url = "https://stipendioccnl.it/comporto-malattia/"
title = "Comporto malattia 2026: quanti giorni in ogni CCNL"
desc = "Periodo di comporto per malattia nei principali CCNL: per quanti giorni il posto è conservato, con l'articolo del contratto."
faq = [("Cos'è il periodo di comporto?", "È il numero massimo di giorni di malattia durante i quali l'azienda non può licenziarti. Lo stabilisce il CCNL (art. 2110 c.c.)."),
       ("Posso usare le ferie per non superare il comporto?", "Puoi chiedere di convertire l'assenza in ferie; l'azienda deve valutare la richiesta tenendo conto delle esigenze organizzative.")]
main = ('<main class="w"><div class="crumb">Comporto malattia</div><h1>Comporto per malattia in ogni CCNL</h1>'
        '<p class="lead">Per quanti giorni di malattia il posto è conservato lo fissa il contratto collettivo. Scegli il tuo CCNL per la tabella completa.</p>'
        '<table><thead><tr><th>CCNL</th><th>Comporto</th></tr></thead><tbody>' + "".join(righe_hub) + "</tbody></table>"
        + COMUNE + "<h2>Domande frequenti</h2>" + "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in faq) + "</main>")
out = R / "comporto-malattia"; out.mkdir(exist_ok=True)
(out / "index.html").write_text(head(url, title, desc, [("Home", "https://stipendioccnl.it/"), ("Comporto malattia", url)], faq) + main + TAIL)
urls.append(url)
sm = (R / "sitemap.xml").read_text()
add = "".join(f"<url><loc>{u}</loc><lastmod>2026-11-26</lastmod></url>\n" for u in urls if u not in sm)
if add: (R / "sitemap.xml").write_text(sm.replace("</urlset>", add + "</urlset>"))
si = json.loads((R / "search-index.json").read_text())
if not any(x[1] == "/comporto-malattia/" for x in si):
    si.append(["Comporto malattia per CCNL", "/comporto-malattia/", 1]); (R / "search-index.json").write_text(json.dumps(si, ensure_ascii=False, separators=(",", ":")))
print(len(urls), "pagine")
