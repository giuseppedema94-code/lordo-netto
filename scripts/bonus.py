"""Pagina /bonus-isee/: bonus e assegni 2026 legati a ISEE o reddito, con calcolo dell'assegno unico.
Valori letti da circolari e pagine INPS (link in ogni voce). Tabella AUU da allegato 1 circ. INPS 7/2026. Idempotente."""
import json, re, html as H
from pathlib import Path
R = Path(__file__).resolve().parent.parent
AUU = json.loads((R / "data/auu-2026.json").read_text())
tpl = (R / "tredicesima-netta/index.html").read_text()
HEAD, TAIL = tpl[:tpl.find("<main")], tpl[tpl.find("</main>") + 7:]
e = lambda s: H.escape(s, quote=False)
C7 = "https://www.inps.it/content/dam/inps-site/it/scorporati/circolari-e-messaggi/2026/01/Circolare_15152/Allegati/16548_Circolare-numero-7-del-30-01-2026.pdf"
C7A = "https://www.inps.it/content/dam/inps-site/it/scorporati/circolari-e-messaggi/2026/01/Circolare_15152/Allegati/16549_Circolare-numero-7-del-30-01-2026_Allegato-n-1.pdf"
C29 = "https://www.inps.it/content/dam/inps-site/it/scorporati/circolari-e-messaggi/2026/03/Circolare_15207/Allegati/16651_Circolare-numero-29-del-27-03-2026.pdf"
NN = "https://www.inps.it/it/it/inps-comunica/notizie/dettaglio-news-page.news.2026.04.bonus-nuovi-nati-2026-al-via-le-domande.html"
BM = "https://www.inps.it/it/it/inps-comunica/notizie/dettaglio-news-page.news.2026.01.vademecum-bonus-mamme.html"
CD = "https://www.inps.it/it/it/inps-comunica/notizie/dettaglio-news-page.news.2026.09.carta-dedicata-a-te-modalit-operative-per-il-2026-2027.html"
BONUS = [
 ("Assegno unico universale", "Da 58,30 a 203,80 € al mese per ogni figlio minorenne", "ISEE fino a 17.468,51 € per l'importo pieno, decresce fino a 46.582,71 €; oltre o senza ISEE importo minimo", "Circolare INPS 7 del 30/1/2026", C7),
 ("Bonus asilo nido (nati dal 2024)", "3.600 € l'anno; 1.500 € sopra soglia o senza ISEE", "ISEE minorenni fino a 40.000 €, al netto dell'assegno unico", "Circolare INPS 29 del 27/3/2026", C29),
 ("Bonus asilo nido (nati prima del 2024)", "3.000 € fino a 25.000,99 €; 2.500 € fino a 40.000 €; 1.500 € oltre o senza ISEE", "ISEE minorenni, al netto dell'assegno unico", "Circolare INPS 29 del 27/3/2026", C29),
 ("Bonus nuovi nati", "1.000 € una tantum per ogni figlio nato o adottato nel 2026", "ISEE fino a 40.000 €, al netto dell'assegno unico", "INPS, notizia del 14/4/2026", NN),
 ("Bonus mamme lavoratrici", "60 € al mese, fino a 720 € l'anno", "Almeno 2 figli, fino ai 10 anni del più piccolo; reddito da lavoro fino a 40.000 € (non ISEE)", "INPS, vademecum gennaio 2026", BM),
 ("Carta Dedicata a te", "500 € l'anno per spesa alimentare", "ISEE ordinario fino a 15.000 €; assegnata dai Comuni", "INPS, messaggio 2906 del 22/9/2026", CD),
 ("Bonus sociali luce e gas", "Sconto automatico in bolletta", "ISEE fino a 9.796 € (soglia più alta per le famiglie numerose)", "ARERA", "https://www.arera.it/consumatori/bonus-sociale"),
]
url = "https://stipendioccnl.it/bonus-isee/"
title = "Bonus ISEE 2026: assegno unico, nido e nuovi nati"
desc = "Bonus e assegni 2026 per ISEE: importi e soglie dalle circolari INPS, con il calcolo dell'assegno unico per figlio in base al tuo ISEE."
faq = [("Quanto è l'assegno unico 2026?", "Da 203,80 € al mese per figlio minorenne con ISEE fino a 17.468,51 € a 58,30 € con ISEE oltre 46.582,71 € o senza ISEE (circolare INPS 7/2026), più eventuali maggiorazioni."),
       ("Qual è la soglia ISEE del bonus nuovi nati 2026?", "40.000 €, calcolati senza contare l'assegno unico. Il bonus vale 1.000 € per ogni figlio nato o adottato nel 2026."),
       ("Chi ha diritto alla carta Dedicata a te 2026?", "I nuclei con ISEE ordinario fino a 15.000 €, individuati dai Comuni. Vale 500 € l'anno.")]
ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://stipendioccnl.it/"}, {"@type": "ListItem", "position": 2, "name": "Bonus ISEE 2026", "item": url}]},
    {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]}
h = re.sub(r"<title>.*?</title>", f"<title>{e(title)}</title>", HEAD, count=1)
for k in ('name="description"', 'property="og:description"'):
    h = re.sub(r'(<meta ' + k + r' content=")[^"]*', lambda m: m.group(1) + H.escape(desc), h, count=1)
h = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + H.escape(title), h, count=1)
h = h.replace("https://stipendioccnl.it/tredicesima-netta/", url)
h = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>", h, count=1, flags=re.S)
tab = "".join(f'<div class="bn"><h3>{e(n)}</h3><p class="bn-i">{e(i)}</p><p>{e(s)}</p><p class="note">Fonte: <a href="{H.escape(u)}" rel="noopener">{e(f)}</a></p></div>' for n, i, s, f, u in BONUS)
calc = ('<div class="card form" id="auu"><h2>Calcola l\'assegno unico 2026</h2>'
        '<label>ISEE del nucleo (€)<input id="isee" type="number" min="0" step="100" value="20000" inputmode="numeric"></label>'
        '<label>Figli minorenni<input id="fm" type="number" min="0" max="10" value="1" inputmode="numeric"></label>'
        '<label>Figli tra 18 e 20 anni<input id="fg" type="number" min="0" max="10" value="0" inputmode="numeric"></label>'
        '<label><input id="noisee" type="checkbox"> Non presento l\'ISEE</label>'
        '<p class="res-hero" style="font-size:22px"><b id="auu-out">–</b></p>'
        '<p class="note">Importi base dalla tabella allegata alla circolare INPS 7/2026. Non include le maggiorazioni (figli con disabilità, dal terzo figlio, madre under 21, entrambi i genitori con reddito, figli sotto 1 anno), che aumentano l\'assegno.</p></div>'
        '<script>const T=' + json.dumps(AUU, separators=(",", ":")) + ';'
        'const f=n=>n.toLocaleString("it-IT",{minimumFractionDigits:2,maximumFractionDigits:2});'
        'function auu(){const no=document.getElementById("noisee").checked,i=+document.getElementById("isee").value||0;'
        'let r=T[T.length-1];if(!no)for(const x of T){if(x[0]===null||i<=x[0]){r=x;break}}'
        'const m=Math.max(0,+document.getElementById("fm").value||0),g=Math.max(0,+document.getElementById("fg").value||0),tot=m*r[1]+g*r[2];'
        'document.getElementById("auu-out").textContent=f(tot)+" € al mese ("+f(r[1])+" € per figlio minorenne"+(g?", "+f(r[2])+" € per figlio 18-20 anni":"")+")"}'
        '["isee","fm","fg","noisee"].forEach(id=>document.getElementById(id).addEventListener("input",auu));auu()</script>')
main = ('<main class="w"><div class="crumb"><a href="/">Home</a> › Bonus ISEE 2026</div>'
        f"<h1>{e('Bonus ISEE 2026: importi e soglie')}</h1>"
        '<p class="lead">I principali bonus per famiglie e lavoratori nel 2026, con importi e soglie presi dalle circolari INPS. Calcola qui sotto l\'assegno unico in base al tuo ISEE.</p>'
        + calc +
        '<h2>Tutti i bonus 2026</h2>'
        f'<div class="bns">{tab}</div>'
        '<style>#auu label{display:block;margin:10px 0;font-weight:600}#auu label input[type=number]{display:block;width:100%;max-width:260px;margin-top:4px}#auu label:has(input[type=checkbox]){font-weight:400}'
        '.bns{display:grid;gap:0 32px;grid-template-columns:repeat(auto-fill,minmax(280px,1fr))}.bn{border-top:1px solid var(--rule-soft);padding:14px 0}.bn h3{margin:0 0 4px;font-size:16px}.bn p{margin:4px 0}.bn-i{font-weight:700;color:var(--accent)}</style>'
        '<p class="note">"ISEE minorenni al netto dell\'assegno unico": l\'INPS calcola l\'ISEE senza contare l\'assegno unico già ricevuto. Le domande si presentano sul sito INPS o tramite patronato. Valori aggiornati al 27/11/2026.</p>'
        '<p>L\'assegno unico non entra nella busta paga: lo versa l\'INPS. Per sapere quanto prendi di stipendio usa il <a href="/">calcolatore dello stipendio netto</a>.</p>'
        "<h2>Domande frequenti</h2>" + "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in faq) + "</main>")
out = R / "bonus-isee"; out.mkdir(exist_ok=True)
(out / "index.html").write_text(h + main + TAIL)
sm = (R / "sitemap.xml").read_text()
if url not in sm:
    (R / "sitemap.xml").write_text(sm.replace("</urlset>", f"<url><loc>{url}</loc></url></urlset>"))
si = json.loads((R / "search-index.json").read_text())
if not any(x[1] == "/bonus-isee/" for x in si):
    si.append(["Bonus ISEE 2026: assegno unico, nido, nuovi nati", "/bonus-isee/", 1]); (R / "search-index.json").write_text(json.dumps(si, ensure_ascii=False, separators=(",", ":")))
