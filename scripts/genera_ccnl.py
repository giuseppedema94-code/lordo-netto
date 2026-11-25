#!/usr/bin/env python3
"""Aggiunge al sito i contratti descritti in data/ccnl-nuovi.json.
Per ogni contratto crea la pagina del CCNL e una pagina per livello, poi aggiorna
calcolatore (index.html), elenco contratti, tredicesima, quattordicesima, indice di ricerca e sitemap.
Nessuna AI: template + aritmetica (scripts/netto.py, stesse regole del calcolatore).
Uso: python3 scripts/genera_ccnl.py   (dalla radice del repo; si puo rilanciare: sostituisce le pagine generate)"""
import datetime as dt
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import netto as N  # noqa: E402

SITE = "https://stipendioccnl.it"
OGGI = dt.date.today().isoformat()
TPL_LIV = (ROOT / "stipendio-netto/gas-acqua/4-livello/index.html").read_text(encoding="utf-8")
TPL_CCNL = (ROOT / "stipendio-netto/gas-acqua/index.html").read_text(encoding="utf-8")
CNEL = ('<div class="box"><b>Contratto ufficiale.</b> I CCNL sono depositati nell\'<a href="https://www.cnel.it/archivio-contratti/'
        'entra-nell-archivio/interroga-l-archivio" rel="noopener">archivio del CNEL</a>.{extra}</div>')
TOG_JS = ("<script>document.querySelectorAll('.tog button').forEach(b=>b.onclick=()=>{document.querySelectorAll('.tog button')"
          ".forEach(x=>x.classList.toggle('on',x===b));document.querySelectorAll('[data-m]').forEach(t=>t.textContent=t.dataset[b.dataset.p])})</script>")


def eur(x, dec=False):
    if dec:
        return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{round(x):,}".replace(",", ".")


def e(s):
    return html.escape(str(s), quote=True)


def mens_txt(m):
    return {13.5: "13 e mezza", 14: "14", 13: "13", 15: "15", 12: "12"}.get(m, str(m).replace(".", ","))


def slug_liv(lab):
    s = re.sub(r"[^a-z0-9]+", "-", lab.lower().replace("°", "").replace("ª", "")).strip("-")
    return s if s.startswith(("quadro", "q-")) or "livello" in s or s.startswith("dirig") else s + "-livello"


def testa(tpl, title, desc, url, ld):
    s = re.sub(r"<title>.*?</title>", f"<title>{e(title)}</title>", tpl, count=1)
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{e(desc)}">', s, count=1)
    s = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{e(title)}">', s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{e(desc)}">', s, count=1)
    s = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', s, count=1)
    s = re.sub(r'<script type="application/ld\+json">.*?</script>',
               lambda m: '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>", s, count=1, flags=re.S)
    return s


def con_main(tpl, main):
    i, j = tpl.index('<main class="w">'), tpl.index("</main>")
    return tpl[:i] + main + tpl[j:]


def faq_ld(faq):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faq]}


def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u}
                                                          for i, (n, u) in enumerate(items)]}


def faq_html(faq):
    return "<h2>Domande frequenti</h2>" + "".join(f"<h3>{e(q)}</h3><p>{a}</p>" for q, a in faq)


def periodi_tab(c, righe, link=True):
    """righe: lista di (etichetta, href, indice livello). Colonne: periodi del contratto."""
    P = c["periodi"]
    th1 = ("<th rowspan=\"2\">Livello</th>" if link else "") + "".join(
        f'<th class="n c{" fut" if p.get("fut") else ""}" colspan="2">{e(p["label"])}</th>' for p in P)
    th2 = "".join(f'<th class="n s lo{" fut" if p.get("fut") else ""}">Lordo</th><th class="n s ne{" fut" if p.get("fut") else ""}">Netto</th>' for p in P)
    body = ""
    for lab, href, i in righe:
        tds = ""
        for p in P:
            mn = p["minimi"][i]
            f = " fut" if p.get("fut") else ""
            nm, na = N.mensile(mn, c["mens"]), N.annuo(mn * c["mens"])["netto"]
            tds += (f'<td class="n lo{f}" data-m="{eur(mn)} €" data-a="{eur(mn * c["mens"])} €">{eur(mn)} €</td>'
                    f'<td class="n ne{f}" data-m="{eur(nm)} €" data-a="{eur(na)} €">{eur(nm)} €</td>')
        body += "<tr>" + (f'<td><a href="{href}">{e(lab)}</a></td>' if link else "") + tds + "</tr>"
    return (('<div class="tog" role="group" aria-label="Periodo"><button type="button" class="on" data-p="m">Mensile</button>'
             '<button type="button" data-p="a">Annuale</button></div>')
            + f'<div class="tw"><table class="trt"><thead><tr>{th1}</tr><tr>{th2}</tr></thead><tbody>{body}</tbody></table></div>')


def pagina_livello(c, i):
    lab, mn = c["livelli"][i]
    mens, br, base = c["mens"], c["breve"], f"/stipendio-netto/{c['slug']}/"
    url = f"{SITE}{base}{slug_liv(lab)}/"
    a = N.annuo(mn * mens)
    nm, tr = N.mensile(mn, mens), N.tredicesima(mn)
    lv = f"livello {lab}" if not lab.lower().startswith(("quadro", "dirig")) else lab
    title = f"Stipendio netto CCNL {br} {lv} 2026: {eur(nm)} €"
    desc = (f"CCNL {br}, {lv}: minimo {eur(mn, True)} € lordi al mese a tempo pieno: retribuzione netta di circa {eur(nm)} € in busta nel 2026. "
            f"Netto annuo, tredicesima e calcolo con IRPEF e INPS.")
    q14 = (f' La <a href="/quattordicesima-netta/#{c["slug"]}">quattordicesima di luglio</a> ha un importo simile.' if mens >= 14 else "")
    faq = [
        (f"Quanto si prende netto al {lv} del CCNL {br}?",
         f"Circa {eur(nm)} € al mese in una busta ordinaria del 2026, su un minimo di {eur(mn, True)} € lordi. In un anno il netto è di circa {eur(a['netto'])} €."),
        (f"Qual è la RAL minima del {lv} {br}?",
         f"La RAL minima è di {eur(mn * mens)} €, cioè il minimo mensile per {mens_txt(mens)} mensilità."),
        (f"Quanto è la tredicesima netta al {lv} {br}?",
         f"Circa {eur(tr)} € netti su {eur(mn)} € lordi, per un anno intero di lavoro. Sulla tredicesima si pagano INPS e IRPEF ma non si applicano "
         f"le detrazioni, che sono già nelle buste ordinarie: per questo il netto è più basso di quello di un mese normale.{q14} "
         f'<a href="/tredicesima-netta/#{c["slug"]}">Come si calcola la tredicesima</a>.'),
        ("Perché il mio netto può essere diverso?",
         "La stima usa il minimo contrattuale e le addizionali medie. Superminimo, scatti, straordinari, familiari a carico, fondo pensione e il tuo comune cambiano il risultato."),
    ]
    righe_tab = [("Lordo annuo (RAL minima)", f"{eur(a['ral'])} €", ""), ("Contributi INPS", f"− {eur(a['inps'])} €", ""),
                 ("IRPEF netta", f"− {eur(a['netta'])} €", ""), ("Addizionali regionale e comunale", f"− {eur(a['add'])} €", "")]
    if a["bonus"] + a["ti"] >= 0.5:
        righe_tab.append(("Taglio del cuneo e trattamento integrativo", f"+ {eur(a['bonus'] + a['ti'])} €", ""))
    righe_tab.append(("Netto annuo", f"{eur(a['netto'])} €", "me"))
    tab = "<table><tbody>" + "".join(f'<tr class="{k}"><td>{t}</td><td class="n">{v}</td></tr>' for t, v, k in righe_tab) + "</tbody></table>"
    storico = ""
    if len(c["periodi"]) > 1:
        storico = "<h2>Lordo e netto per mese di decorrenza</h2>" + periodi_tab(c, [(lab, "", i)], link=False)
    altri = "".join(f'<li><a href="{base}{slug_liv(l)}/">{e(l)}</a></li>' for j, (l, _) in enumerate(c["livelli"]) if j != i)
    fonte = f' Fonte dei minimi: <a href="{e(c["fonte_url"])}" rel="noopener">{e(c["fonte_nome"])}</a>.' if c.get("fonte_url") else ""
    main = (f'<main class="w"><div class="crumb"><a href="/stipendio-netto/">Stipendi per CCNL</a> › <a href="{base}">{e(br)}</a> › {e(lab)}</div>'
            f"<h1>Stipendio netto {e(br)} {e(lv)} 2026</h1>\n"
            f'<p class="lead">Con il CCNL {e(br)}, al {e(lv)} la retribuzione minima è di {eur(mn, True)} € lordi al mese per {mens_txt(mens)} mensilità{c.get("mens_nota", "")}: '
            f"circa <b>{eur(nm)} € netti</b> in una busta ordinaria.</p>\n{da_sapere(c)}"
            f'<div class="hero"><div class="big"><span>Netto in busta</span><b>{eur(nm)} €</b></div><div><span>Lordo mensile</span><b>{eur(mn)} €</b></div>'
            f'<div><span>Netto annuo</span><b>{eur(a["netto"])} €</b></div></div>\n'
            + storico + "\n<h2>Dal lordo al netto in un anno</h2>" + tab + "\n"
            f'<a class="cta" href="/?ccnl={c["key"]}&amp;livello={i}">Calcola con il tuo comune e i tuoi dati</a>\n'
            '<p class="note">Stima sul minimo contrattuale: superminimo, scatti di anzianità, straordinari, fondo pensione e addizionali del tuo comune '
            "cambiano il risultato. Nel calcolatore li trovi tutti.</p>\n" + CNEL.format(extra=fonte)
            + (TOG_JS if storico else "") + faq_html(faq)
            + f'<h2>Altri livelli {e(br)}</h2><ul class="lv">{altri}</ul></main>')
    ld = {"@context": "https://schema.org", "@graph": [crumbs([("Home", SITE + "/"), ("Stipendi per CCNL", SITE + "/stipendio-netto/"),
                                                                ("" + br, SITE + base), (lab, url)]), faq_ld(faq)]}
    return url, con_main(testa(TPL_LIV, title, desc, url, ld), main)


def da_sapere(c):
    return f'<p class="note"><b>Da sapere:</b> {e(c["note"])}</p>\n' if c.get("note") else ""


def pagina_ccnl(c):
    br, base, mens = c["breve"], f"/stipendio-netto/{c['slug']}/", c["mens"]
    url = SITE + base
    nets = [N.mensile(mn, mens) for _, mn in c["livelli"]]
    trs = [N.tredicesima(mn) for _, mn in c["livelli"]]
    lo, hi = min(range(len(nets)), key=nets.__getitem__), max(range(len(nets)), key=nets.__getitem__)
    title = f"Stipendio netto {br} 2026: tutti i livelli"
    desc = (f"CCNL {br} 2026: minimi, RAL e netto in busta di tutti i livelli, da {eur(nets[lo])} € a {eur(nets[hi])} € netti al mese. "
            f"Con {mens_txt(mens)} mensilità.")
    faq = [
        (f"Quanto si prende netto con il CCNL {br} nel 2026?",
         f"Con i minimi in vigore il netto in busta va da circa {eur(nets[lo])} € al mese ({c['livelli'][lo][0]}) a circa {eur(nets[hi])} € "
         f"({c['livelli'][hi][0]}), in una busta ordinaria senza familiari a carico."),
        (f"Quante mensilità prevede il CCNL {br}?",
         f"Il contratto prevede {mens_txt(mens)} mensilità: la RAL minima è il minimo mensile moltiplicato per il numero di mensilità."),
        (f"Quanto è la tredicesima netta con il CCNL {br}?",
         f"Con i minimi 2026 va da circa {eur(min(trs))} € a {eur(max(trs))} € netti, per un anno intero di lavoro. Gli importi livello per livello sono nella "
         f'<a href="/tredicesima-netta/#{c["slug"]}">tabella della tredicesima netta</a>.'),
        ("Il netto indicato comprende scatti e superminimo?",
         "No: è calcolato sul minimo contrattuale. Scatti di anzianità, superminimo, straordinari e addizionali del tuo comune lo cambiano; puoi inserirli nel calcolatore."),
    ]
    righe = [(l, f"{base}{slug_liv(l)}/", i) for i, (l, _) in enumerate(c["livelli"])]
    fonte = f' Fonte dei minimi: <a href="{e(c["fonte_url"])}" rel="noopener">{e(c["fonte_nome"])}</a>.' if c.get("fonte_url") else ""
    main = (f'<main class="w"><div class="crumb"><a href="/stipendio-netto/">Stipendi per CCNL</a> › {e(br)}</div>'
            f"<h1>Stipendio netto {e(br)} 2026: tutti i livelli</h1>\n"
            f'<p class="lead">{e(c["nome"])}: minimi in vigore, RAL e netto in busta per ogni livello, con {mens_txt(mens)} mensilità{c.get("mens_nota", "")}. {e(c["fonte"])}.</p>\n{da_sapere(c)}'
            + periodi_tab(c, righe) + "\n"
            f'<a class="cta" href="/?ccnl={c["key"]}">Calcola il tuo netto {e(br)}</a>\n'
            '<p class="note">Il netto è quello di una busta ordinaria. Con superminimo, scatti, indennità o fondi integrativi usa il calcolatore.</p>'
            + CNEL.format(extra=fonte) + TOG_JS + faq_html(faq) + "</main>")
    ld = {"@context": "https://schema.org", "@graph": [crumbs([("Home", SITE + "/"), ("Stipendi per CCNL", SITE + "/stipendio-netto/"),
                                                                (br, url)]), faq_ld(faq)]}
    return url, con_main(testa(TPL_CCNL, title, desc, url, ld), main), (nets, trs)


def tabella_13(c, trs, quale):
    base = f"/stipendio-netto/{c['slug']}/"
    rows = "".join(f'<tr><td><a href="{base}{slug_liv(l)}/">{e(l)}</a></td><td class="n">{eur(mn)} €</td><td class="n"><b>{eur(t)} €</b></td></tr>'
                   for (l, mn), t in zip(c["livelli"], trs))
    return (f'<details id="{c["slug"]}"><summary><b>{e(c["breve"])}</b> <span class="note">da {eur(min(trs))} € a {eur(max(trs))} € netti</span></summary>\n'
            f'<div class="tw"><table><thead><tr><th>Livello</th><th class="n">{quale} lorda</th><th class="n">{quale} netta</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>\n<p class="note">{e(c["nome"])}. {e(c["fonte"])}.</p></details>')


def inserisci_prima(s, marker, blocco, chiave):
    if chiave in s:
        return s
    i = s.index(marker)
    return s[:i] + blocco + s[i:]


def main():
    dati = json.loads((ROOT / "data/ccnl-nuovi.json").read_text(encoding="utf-8"))
    urls, idx = [], json.loads((ROOT / "search-index.json").read_text(encoding="utf-8"))
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    elenco = (ROOT / "stipendio-netto/index.html").read_text(encoding="utf-8")
    tred = (ROOT / "tredicesima-netta/index.html").read_text(encoding="utf-8")
    quat = (ROOT / "quattordicesima-netta/index.html").read_text(encoding="utf-8")
    for c in dati:
        c.setdefault("periodi", [{"label": c.get("periodo", "2026"), "minimi": [m for _, m in c["livelli"]]}])
        url, pg, (nets, trs) = pagina_ccnl(c)
        out = ROOT / "stipendio-netto" / c["slug"]
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(pg, encoding="utf-8")
        urls.append(url)
        idx = [x for x in idx if not x[1].startswith(f"/stipendio-netto/{c['slug']}/")]
        idx.append([c["breve"], f"/stipendio-netto/{c['slug']}/", 1])
        for i, (lab, _) in enumerate(c["livelli"]):
            u, p = pagina_livello(c, i)
            d = out / slug_liv(lab)
            d.mkdir(exist_ok=True)
            (d / "index.html").write_text(p, encoding="utf-8")
            urls.append(u)
            idx.append([f"{c['breve']} {lab}", u.replace(SITE, ""), 0])
        # calcolatore: oggetto CCNL
        voce = (f'  {c["key"]}:{{nome:{json.dumps(c["nome"], ensure_ascii=False)},mens:{c["mens"]},fonte:{json.dumps(c["fonte"], ensure_ascii=False)},\n'
                f'    livelli:{json.dumps(c["livelli"], ensure_ascii=False)}, def:{c.get("def", len(c["livelli"]) // 2)},\n'
                f'    note:{json.dumps(c.get("note", ""), ensure_ascii=False)}}},\n')
        home = re.sub(r"\n  " + re.escape(c["key"]) + r":\{nome:.*?\n    note:.*?\},\n", "\n", home, flags=re.S)
        home = inserisci_prima(home, "  abi:{nome:", voce, f'  {c["key"]}:{{nome:')
        # home: albero dei contratti
        lis = "".join(f'<li><a href="stipendio-netto/{c["slug"]}/{slug_liv(l)}/">{e(l)}</a></li>' for l, _ in c["livelli"])
        albero = (f'<details class="tree"><summary><a href="stipendio-netto/{c["slug"]}/">{e(c["breve"])}</a><small>{len(c["livelli"])} livelli</small>'
                  f'</summary><ul class="lv">{lis}</ul></details>')
        home = inserisci_prima(home, '<details class="tree"><summary><a href="stipendio-netto/gas-acqua/">', albero, f'href="stipendio-netto/{c["slug"]}/"')
        riga = (f'<tr><td><a href="/stipendio-netto/{c["slug"]}/">{e(c["breve"])}</a></td><td>{e(c["nome"])}</td>'
                f'<td class="n">{len(c["livelli"])}</td></tr>')
        elenco = inserisci_prima(elenco, '<tr><td><a href="/stipendio-netto/gas-acqua/">', riga, f'href="/stipendio-netto/{c["slug"]}/"')
        tred = inserisci_prima(tred, '<details id="gas-acqua">', tabella_13(c, trs, "Tredicesima"), f'id="{c["slug"]}"')
        if c["mens"] >= 14:
            quat = inserisci_prima(quat, '<details id="gas-acqua">', tabella_13(c, trs, "Quattordicesima"), f'id="{c["slug"]}"')
    (ROOT / "index.html").write_text(home, encoding="utf-8")
    (ROOT / "stipendio-netto/index.html").write_text(elenco, encoding="utf-8")
    (ROOT / "tredicesima-netta/index.html").write_text(tred, encoding="utf-8")
    (ROOT / "quattordicesima-netta/index.html").write_text(quat, encoding="utf-8")
    (ROOT / "search-index.json").write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    nuovi = "".join(f"<url><loc>{u}</loc><lastmod>{OGGI}</lastmod></url>\n" for u in urls if f"<loc>{u}</loc>" not in sm)
    (ROOT / "sitemap.xml").write_text(sm.replace("</urlset>", nuovi + "</urlset>"), encoding="utf-8")
    print(f"{len(dati)} contratti, {len(urls)} pagine")
    import runpy; runpy.run_path(str(Path(__file__).with_name("link_ccnl.py")))


if __name__ == "__main__":
    main()
