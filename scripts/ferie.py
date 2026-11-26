"""Pagine "ferie e permessi" per CCNL (/stipendio-netto/<slug>/ferie-permessi/) e pagina di confronto /ferie-permessi/.
Dati in data/ferie.json, ricavati dai testi dei CCNL (articolo e link in ogni voce). Idempotente."""
import json, re, html as H
from pathlib import Path
R = Path(__file__).resolve().parent.parent
D = json.loads((R / "data/ferie.json").read_text())
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
COMUNE = ("<h2>Regole che valgono sempre</h2><ul><li>Le ferie maturano per dodicesimi: un mese lavorato (o più di 15 giorni) vale un dodicesimo.</li><li>Almeno 2 settimane vanno godute nell'anno, se le chiedi; le altre 2 entro i 18 mesi successivi.</li><li>Le ferie minime non si possono pagare al posto di goderle, salvo quando il rapporto finisce.</li><li>Nel part-time le ore di permesso si riducono in proporzione all'orario.</li></ul>")
VECCHIO = ("<h2>Regole che valgono sempre</h2><ul>"
          "<li>Il patto di prova deve essere scritto nella lettera di assunzione, prima di iniziare. Senza, la prova non vale.</li>"
          "<li>Le durate del contratto sono massime: la lettera può prevederne una più breve, mai più lunga.</li>"
          "<li>Durante la prova ciascuna parte può chiudere il rapporto senza preavviso. Ti spettano comunque i giorni lavorati, il TFR e i ratei di tredicesima e ferie.</li>"
          "<li>Malattia, infortunio e congedo di maternità o paternità sospendono la prova, che riprende al rientro.</li></ul>")
urls = []
righe_hub = []
for slug, c in D.items():
    url = f"https://stipendioccnl.it/stipendio-netto/{slug}/ferie-permessi/"
    breve = c["nome"].split(" (")[0]
    first, last = c["righe"][0], c["righe"][-1]
    title = f"Ferie e permessi CCNL {breve} 2026: giorni e ore ROL"
    desc = f"Ferie e permessi nel CCNL {c['nome']}: {c['ferie']} di ferie e {c['permessi']} di permessi retribuiti all'anno. Tabella con l'articolo del contratto."
    faq = [(f"Quanti giorni di ferie e ore di permesso spettano nel CCNL {breve}?", "; ".join(f"{a}: {b}" for a, b in c["righe"]) + "."),
           ("Le ferie non godute si perdono?", "Le 4 settimane minime di legge vanno godute e non si possono pagare, salvo alla fine del rapporto. Le ferie e i permessi non goduti si pagano in busta paga quando il rapporto si chiude.")]
    tab = "".join(f"<tr><td>{e(a)}</td><td><b>{e(b)}</b></td></tr>" for a, b in c["righe"])
    main = (f'<main class="w"><div class="crumb"><a href="/stipendio-netto/">Stipendi per CCNL</a> › <a href="/stipendio-netto/{slug}/">{e(breve)}</a> › Ferie e permessi</div>'
            f"<h1>Ferie e permessi nel CCNL {e(c['nome'])}</h1>"
            f'<p class="lead">In un anno intero spettano <b>{e(c["ferie"])}</b> di ferie e <b>{e(c["permessi"])}</b> di permessi retribuiti. Chi lavora meno di un anno li matura in dodicesimi.</p>'
            f"<table><thead><tr><th>Voce</th><th>Quanto spetta</th></tr></thead><tbody>{tab}</tbody></table>"
            f'<p class="note">{e(c["note"])} Fonte: <a href="{H.escape(c["url"])}" rel="noopener">{e(c["fonte"])}</a>.</p>'
            + COMUNE +
            f'<p>Quanto vale un giorno di ferie? Parti dallo stipendio del tuo livello: <a href="/stipendio-netto/{slug}/">stipendio netto CCNL {e(breve)}</a>. '
            f'<a href="/ferie-permessi/">Confronta ferie e permessi negli altri contratti</a>.</p>'
            "<h2>Domande frequenti</h2>" + "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in faq) + "</main>")
    crumbs = [("Home", "https://stipendioccnl.it/"), ("Stipendi per CCNL", "https://stipendioccnl.it/stipendio-netto/"),
              (breve, f"https://stipendioccnl.it/stipendio-netto/{slug}/"), ("Ferie e permessi", url)]
    out = R / f"stipendio-netto/{slug}/ferie-permessi"; out.mkdir(exist_ok=True)
    (out / "index.html").write_text(head(url, title, desc, crumbs, faq) + main + TAIL)
    urls.append(url)
    righe_hub.append(f'<tr><td><a href="/stipendio-netto/{slug}/ferie-permessi/">{e(breve)}</a></td><td>{e(c["ferie"])}</td><td>{e(c["permessi"])}</td></tr>')
    # link dalla pagina del CCNL
    p = R / f"stipendio-netto/{slug}/index.html"; s = p.read_text()
    if "/ferie-permessi/" not in s:
        s = s.replace("</main>", f'<p><a href="/stipendio-netto/{slug}/ferie-permessi/">Ferie e permessi nel CCNL {e(breve)}</a></p></main>', 1)
        p.write_text(s)
# pagina di confronto
url = "https://stipendioccnl.it/ferie-permessi/"
title = "Ferie e permessi 2026: quanti ne spettano in ogni CCNL"
desc = "Giorni di ferie e ore di permessi retribuiti (ROL ed ex festività) nei principali contratti collettivi, con l'articolo del CCNL."
faq = [("Quante ferie spettano per legge?", "Almeno 4 settimane all'anno (art. 10 D.Lgs. 66/2003); il CCNL può darne di più."),
       ("Cosa sono ROL ed ex festività?", "Sono ore di permesso retribuito: i ROL nascono dalla riduzione dell'orario annuo, le ex festività sostituiscono quattro festività abolite nel 1977. Le ore le stabilisce il CCNL.")]
main = ('<main class="w"><div class="crumb">Ferie e permessi</div><h1>Ferie e permessi: quanti ne spettano in ogni CCNL</h1>'
        '<p class="lead">Per legge spettano almeno 4 settimane di ferie all’anno. Il resto (giorni in più, ROL, ex festività) lo stabilisce il contratto collettivo. Valori per un anno intero con orario a tempo pieno.</p>'
        '<table><thead><tr><th>CCNL</th><th>Ferie all’anno</th><th>Permessi retribuiti</th></tr></thead><tbody>' + "".join(righe_hub) + "</tbody></table>"
        + COMUNE + "<h2>Domande frequenti</h2>" + "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in faq) + "</main>")
out = R / "ferie-permessi"; out.mkdir(exist_ok=True)
(out / "index.html").write_text(head(url, title, desc, [("Home", "https://stipendioccnl.it/"), ("Ferie e permessi", url)], faq) + main + TAIL)
urls.append(url)
sm = (R / "sitemap.xml").read_text()
add = "".join(f"<url><loc>{u}</loc><lastmod>2026-11-26</lastmod></url>\n" for u in urls if u not in sm)
if add: (R / "sitemap.xml").write_text(sm.replace("</urlset>", add + "</urlset>"))
si = json.loads((R / "search-index.json").read_text())
if not any(x[1] == "/ferie-permessi/" for x in si):
    si.append(["Ferie e permessi per CCNL", "/ferie-permessi/", 1]); (R / "search-index.json").write_text(json.dumps(si, ensure_ascii=False, separators=(",", ":")))
print(len(urls), "pagine")
