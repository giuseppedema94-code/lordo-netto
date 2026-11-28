"""Genera /costo-colf-badante/: costo annuo per la famiglia, contributi INPS trimestrali e netto del lavoratore.
Dati: minimi CCNL lavoro domestico 2026 (come la pagina stipendio-netto/colf-badanti); contributi orari INPS 2026
(circolare INPS n. 9 del 3/2/2026); Cassa Colf 0,06 €/ora (0,02 a carico del lavoratore). Idempotente."""
import json, re
from pathlib import Path
R = Path(__file__).resolve().parent.parent
URL = "https://stipendioccnl.it/costo-colf-badante/"
LIV = [("A", 908.10, 6.51), ("AS", 958.55, 6.76), ("B", 983.16, 7.01), ("BS", 1053.39, 7.45),
       ("C", 1123.63, 7.86), ("CS", 1193.84, 8.30), ("D", 1404.51, 9.57), ("DS", 1474.73, 9.97)]
# fasce INPS 2026, tempo indeterminato con CUAF: (limite paga oraria effettiva, totale, quota lavoratore)
FASCE = [(9.61, 1.70, 0.43), (11.70, 1.92, 0.48), (float("inf"), 2.34, 0.59)]
OLTRE24 = (1.24, 0.31)
DET = {1.70: 1.82, 1.92: 2.05, 2.34: 2.50, 1.24: 1.32}   # tempo determinato (contributo addizionale)
CASSA, CASSA_LAV = 0.06, 0.02
def contrib(paga_oraria_eff, ore_sett, determinato=False):
    if ore_sett > 24: tot, lav = OLTRE24
    else: tot, lav = next((t, l) for lim, t, l in FASCE if paga_oraria_eff <= lim)
    return (DET[tot] if determinato else tot), lav
def costo(conv, liv, ore=54, determinato=False):
    _, mens, oraria = next(x for x in LIV if x[0] == liv)
    if conv: ore = 54; mese = mens
    else: mese = oraria * ore * 52 / 12
    ore_anno = ore * 52
    eff = (mese * 13 / 12) / (ore * 52 / 12)
    tot, lav = contrib(eff, ore, determinato)
    retr = mese * 13
    tfr = retr / 13.5
    inps_dat = (tot - lav) * ore_anno
    cassa_dat = (CASSA - CASSA_LAV) * ore_anno
    totale = retr + tfr + inps_dat + cassa_dat
    trim = (tot + CASSA) * ore * 13
    netto = mese - (lav + CASSA_LAV) * ore * 52 / 12
    return dict(mese=mese, retr=retr, tfr=tfr, inps=inps_dat, cassa=cassa_dat, tot=totale, trim=trim, netto=netto, tot_h=tot, lav=lav)
E = costo(True, "BS")
assert abs(E["tot"] - 17432.22) < 0.05, E
assert abs(E["netto"] - 976.17) < 0.05, E   # coerente con la pagina CCNL colf (976 € netti)
def eur(x): return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
F = costo(False, "B", 20)
FAQ = [
 ("Quanto costa in tutto una badante convivente nel 2026?",
  f"Al livello BS, a tempo pieno (54 ore), circa {eur(E['tot'])} € l'anno, cioè {eur(E['tot']/12)} € al mese: stipendio e tredicesima, TFR, contributi INPS e Cassa Colf. Vitto e alloggio sono in più."),
 ("Quanto costa una colf a ore?",
  f"Al livello B per 20 ore a settimana circa {eur(F['tot'])} € l'anno, {eur(F['tot']/12)} € al mese, tutto compreso."),
 ("Quanto si paga di contributi INPS ogni trimestre?",
  f"Dipende da ore e paga oraria. Per una badante convivente con 54 ore a settimana sono circa {eur(E['trim'])} € a trimestre, Cassa Colf compresa. La quota del lavoratore si trattiene dalla sua paga."),
 ("Quando si pagano i contributi della colf?",
  "Entro il 10 aprile, il 10 luglio, il 10 ottobre e il 10 gennaio, per il trimestre appena finito. Se il rapporto finisce prima, entro 10 giorni dalla fine."),
]
OPT = "".join(f'<option value="{l}"{" selected" if l=="BS" else ""}>{l}</option>' for l, _, _ in LIV)
MAIN = f'''<main class="w"><div class="crumb"><a href="/stipendio-netto/colf-badanti/">Colf e badanti</a> › Costo per la famiglia</div><h1>Quanto costa una colf o una badante nel 2026</h1>
<p class="lead">Una badante convivente di livello BS costa alla famiglia circa <b>{eur(E['tot']/12)} € al mese</b>, {eur(E['tot'])} € l'anno: oltre alla paga ci sono tredicesima, TFR, contributi INPS e Cassa Colf. Calcola il costo per il tuo caso e quanto versare all'INPS ogni trimestre.</p>
<div class="box" id="colf-calc">
<p><b>Tipo di rapporto</b><br><label><input type="radio" name="c-tipo" value="conv" checked> Convivente (54 ore)</label> &nbsp; <label><input type="radio" name="c-tipo" value="ore"> A ore</label></p>
<p><label for="c-liv"><b>Livello</b> (<a href="/stipendio-netto/colf-badanti/">vedi le mansioni</a>)</label><br><select id="c-liv">{OPT}</select></p>
<p id="c-ore-p" hidden><label for="c-ore"><b>Ore a settimana</b></label><br><input id="c-ore" type="number" min="1" max="54" step="1" value="20" inputmode="numeric"></p>
<p><label><input id="c-det" type="checkbox"> Contratto a tempo determinato</label></p>
<div id="c-out" aria-live="polite"></div>
</div>
<h2>Cosa entra nel costo</h2>
<ul>
<li><b>Paga e tredicesima:</b> il minimo del CCNL lavoro domestico 2026 per 13 mensilità. Le ferie sono pagate dentro la paga mensile.</li>
<li><b>TFR:</b> la paga dell'anno, tredicesima compresa, divisa 13,5. Si paga alla fine del rapporto, o in anticipo una volta l'anno se le parti si accordano.</li>
<li><b>Contributi INPS:</b> un importo per ogni ora lavorata, che dipende dalla paga oraria (tredicesima compresa) o è fisso oltre le 24 ore settimanali. La famiglia li versa tutti e trattiene dalla paga la quota del lavoratore.</li>
<li><b>Cassa Colf:</b> 0,06 € l'ora, di cui 0,02 € a carico del lavoratore.</li>
</ul>
<h2>Contributi INPS 2026 per ora lavorata</h2>
<table><thead><tr><th>Paga oraria effettiva</th><th class="n">Totale</th><th class="n">Di cui lavoratore</th></tr></thead><tbody>
<tr><td>Fino a 9,61 €</td><td class="n">1,70 €</td><td class="n">0,43 €</td></tr>
<tr><td>Da 9,62 a 11,70 €</td><td class="n">1,92 €</td><td class="n">0,48 €</td></tr>
<tr><td>Oltre 11,70 €</td><td class="n">2,34 €</td><td class="n">0,59 €</td></tr>
<tr><td>Più di 24 ore a settimana</td><td class="n">1,24 €</td><td class="n">0,31 €</td></tr>
</tbody></table>
<p class="note">Valori per i contratti a tempo indeterminato, dalla circolare INPS n. 9 del 3 febbraio 2026. A tempo determinato si aggiunge l'1,4%. Per coniugi e parenti conviventi esentati dalla quota CUAF l'importo cambia di un centesimo. Esclusi dal calcolo: vitto e alloggio, scatti di anzianità, superminimi, straordinari. La famiglia può dedurre i contributi INPS fino a 1.549,37 € l'anno; per l'assistenza a una persona non autosufficiente spetta anche una detrazione del 19% su massimo 2.100 € di spesa, se il reddito non supera 40.000 €.</p>
<p>Il netto in busta per ogni livello è nella pagina <a href="/stipendio-netto/colf-badanti/">stipendio colf e badanti 2026</a>. Il TFR si stima anche con il <a href="/calcolo-tfr/">calcolatore TFR</a>.</p>
<h2>Domande frequenti</h2>
''' + "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in FAQ) + '''
<script>
(function(){
const LIV=''' + json.dumps({l: [m, o] for l, m, o in LIV}) + ''',FASCE=[[9.61,1.70,0.43],[11.70,1.92,0.48],[Infinity,2.34,0.59]],DET={"1.7":1.82,"1.92":2.05,"2.34":2.50,"1.24":1.32};
const $=id=>document.getElementById(id), f=x=>{const [i,d]=x.toFixed(2).split(".");return i.replace(/\\B(?=(\\d{3})+(?!\\d))/g,".")+","+d;};
function calc(){
  const conv=document.querySelector('input[name="c-tipo"]:checked').value==="conv"; $("c-ore-p").hidden=conv;
  const [mens,oraria]=LIV[$("c-liv").value], ore=conv?54:Math.min(54,Math.max(1,Math.round(parseFloat($("c-ore").value)||0)));
  const mese=conv?mens:oraria*ore*52/12, eff=(mese*13/12)/(ore*52/12);
  let [tot,lav]=ore>24?[1.24,0.31]:FASCE.find(x=>eff<=x[0]).slice(1);
  if($("c-det").checked) tot=DET[String(tot)];
  const oa=ore*52, retr=mese*13, tfr=retr/13.5, inps=(tot-lav)*oa, cassa=0.04*oa, T=retr+tfr+inps+cassa, trim=(tot+0.06)*ore*13, netto=mese-(lav+0.02)*ore*52/12;
  $("c-out").innerHTML="<table><tbody>"+
   "<tr><td>Paga lorda mensile</td><td class=\\"n\\">"+f(mese)+" €</td></tr>"+
   "<tr><td>Paga e tredicesima nell'anno</td><td class=\\"n\\">"+f(retr)+" €</td></tr>"+
   "<tr><td>TFR dell'anno</td><td class=\\"n\\">"+f(tfr)+" €</td></tr>"+
   "<tr><td>Contributi INPS a carico della famiglia ("+f(tot-lav)+" € l'ora)</td><td class=\\"n\\">"+f(inps)+" €</td></tr>"+
   "<tr><td>Cassa Colf a carico della famiglia</td><td class=\\"n\\">"+f(cassa)+" €</td></tr>"+
   "<tr class=\\"me\\"><td>Costo totale annuo</td><td class=\\"n\\"><b>"+f(T)+" €</b></td></tr>"+
   "<tr><td>Costo medio al mese</td><td class=\\"n\\"><b>"+f(T/12)+" €</b></td></tr>"+
   "<tr><td>Da versare all'INPS ogni trimestre (con la quota del lavoratore)</td><td class=\\"n\\">"+f(trim)+" €</td></tr>"+
   "<tr><td>Netto in busta per il lavoratore, al mese</td><td class=\\"n\\">"+f(netto)+" €</td></tr></tbody></table>";
}
document.querySelectorAll('input[name="c-tipo"]').forEach(e=>e.addEventListener("change",calc));
["c-liv","c-ore","c-det"].forEach(id=>{$(id).addEventListener("input",calc);$(id).addEventListener("change",calc);}); calc();
})();
</script></main>'''
TITLE = "Costo colf e badante 2026: calcolo e contributi INPS"
DESC = f"Quanto costa una colf o una badante nel 2026: paga, tredicesima, TFR, contributi INPS trimestrali e Cassa Colf. Badante convivente BS circa {eur(E['tot']/12)} € al mese."
ld = {"@context": "https://schema.org", "@graph": [
  {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://stipendioccnl.it/"},
     {"@type": "ListItem", "position": 2, "name": "Colf e badanti", "item": "https://stipendioccnl.it/stipendio-netto/colf-badanti/"},
     {"@type": "ListItem", "position": 3, "name": "Costo per la famiglia", "item": URL}]},
  {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]}
tpl = (R / "tredicesima-netta/index.html").read_text()
head = tpl[:tpl.find("<main")]
head = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", head, count=1)
head = re.sub(r'(<meta name="description" content=")[^"]*', r"\g<1>" + DESC, head, count=1)
head = re.sub(r'(<meta property="og:description" content=")[^"]*', r"\g<1>" + DESC, head, count=1)
head = re.sub(r'(<meta property="og:title" content=")[^"]*', r"\g<1>" + TITLE, head, count=1)
head = head.replace("https://stipendioccnl.it/tredicesima-netta/", URL)
head = re.sub(r'<script type="application/ld\+json">.*?</script>', '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>", head, count=1, flags=re.S)
tail = tpl[tpl.find("</main>") + len("</main>"):]
out = R / "costo-colf-badante"; out.mkdir(exist_ok=True)
(out / "index.html").write_text(head + MAIN + tail)
sm = (R / "sitemap.xml").read_text()
if URL not in sm:
    (R / "sitemap.xml").write_text(sm.replace("</urlset>", f"<url><loc>{URL}</loc><lastmod>2026-11-26</lastmod></url>\n</urlset>"))
si = json.loads((R / "search-index.json").read_text())
if not any(x[1] == "/costo-colf-badante/" for x in si):
    si.append(["Costo colf e badante contributi INPS", "/costo-colf-badante/", 1]); (R / "search-index.json").write_text(json.dumps(si, ensure_ascii=False, separators=(",", ":")))
# link dalla pagina CCNL colf
p = R / "stipendio-netto/colf-badanti/index.html"; s = p.read_text()
if "/costo-colf-badante/" not in s:
    s = s.replace("<h2>", '<p class="box"><b>Sei la famiglia?</b> <a href="/costo-colf-badante/">Calcola il costo totale e i contributi INPS trimestrali</a>.</p>\n<h2>', 1)
    p.write_text(s)
print("ok", eur(E["tot"]), eur(E["trim"]), eur(F["tot"]), eur(E["netto"]))
