"""Genera /calcolo-naspi/ (calcolatore NASpI 2026) usando testata e piè di pagina della pagina tredicesima.
Regole: D.Lgs. 22/2015 artt. 4-5; importi 2026 circolare INPS n. 4 del 28/1/2026. Idempotente."""
import json, re
from pathlib import Path
R = Path(__file__).resolve().parent.parent
SOGLIA, MAX = 1456.72, 1584.70
URL = "https://stipendioccnl.it/calcolo-naspi/"
TITLE = "Calcolo NASpI 2026: importo, durata e riduzione mese per mese"
DESC = ("Calcolo NASpI 2026 dalla RAL: 75% della retribuzione media fino a 1.456,72 €, massimo 1.584,70 € al mese, "
        "durata pari a metà delle settimane lavorate e riduzione del 3% dal sesto mese.")
FAQ = [
 ("Quanto prende di NASpI chi guadagna 25.000 € lordi l'anno?",
  "Circa 1.249 € lordi al mese nei primi cinque mesi: la retribuzione media mensile è di 2.082 €, quindi 75% di 1.456,72 € più 25% della parte oltre la soglia. Dal sesto mese l'importo cala del 3% al mese."),
 ("Quanto dura la NASpI?",
  "Metà delle settimane con contributi negli ultimi quattro anni: con quattro anni pieni di lavoro, 104 settimane, cioè circa 24 mesi."),
 ("La NASpI è lorda o netta?",
  "Gli importi sono lordi. INPS trattiene l'IRPEF; le detrazioni per lavoro dipendente si applicano se le chiedi nella domanda, e il netto dipende anche dagli altri redditi dell'anno."),
 ("Quando inizia la riduzione del 3%?",
  "Dal primo giorno del sesto mese di NASpI, oppure dell'ottavo se alla data della domanda hai almeno 55 anni. Ogni mese il 3% si toglie dall'importo del mese prima."),
]
def eur(x): return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
def es(ral):
    r = ral / 52 * 4.33
    a = 0.75 * r if r <= SOGLIA else 0.75 * SOGLIA + 0.25 * (r - SOGLIA)
    return r, min(a, MAX)
r25, a25 = es(25000)
assert abs(a25 - 1248.79) < 0.01, a25  # controllo dell'esempio nelle FAQ
MAIN = f'''<main class="w"><div class="crumb">Calcolo NASpI</div><h1>Calcolo NASpI 2026: quanto prendi e per quanto tempo</h1>
<p class="lead">La NASpI è il 75% della tua retribuzione media mensile fino a {eur(SOGLIA)} €, più il 25% della parte che supera questa soglia, con un massimo di <b>{eur(MAX)} € lordi al mese</b> nel 2026. Dura metà delle settimane lavorate negli ultimi quattro anni e dal sesto mese cala del 3% al mese.</p>
<div class="box" id="naspi-calc">
<p><label for="n-ral"><b>RAL lorda annua</b> (stipendio lordo dell'anno, tredicesima compresa)</label><br><input id="n-ral" type="number" min="0" step="100" value="25000" inputmode="decimal"> €</p>
<p><label for="n-sett"><b>Settimane con contributi negli ultimi 4 anni</b> (massimo 208)</label><br><input id="n-sett" type="number" min="0" max="208" step="1" value="208" inputmode="numeric"></p>
<p><label><input id="n-55" type="checkbox"> Alla data della domanda ho almeno 55 anni</label></p>
<div id="n-out" aria-live="polite"></div>
</div>
<h2>Come si calcola</h2>
<ol>
<li><b>Retribuzione media mensile.</b> INPS somma lo stipendio imponibile degli ultimi quattro anni, lo divide per le settimane con contributi e moltiplica per 4,33. Con uno stipendio costante equivale alla RAL divisa 52 per 4,33.</li>
<li><b>Importo.</b> Fino a {eur(SOGLIA)} € spetta il 75%. Sopra, il 75% di {eur(SOGLIA)} € più il 25% della parte che eccede. In ogni caso non oltre {eur(MAX)} € al mese.</li>
<li><b>Riduzione.</b> Dal primo giorno del sesto mese l'importo cala del 3% ogni mese, calcolato su quello del mese precedente. Dall'ottavo mese se alla domanda hai almeno 55 anni.</li>
<li><b>Durata.</b> Metà delle settimane con contributi negli ultimi quattro anni, tolte quelle già usate per un'altra disoccupazione: al massimo 104 settimane.</li>
</ol>
<h2>Chi ne ha diritto</h2>
<ul>
<li>Chi perde il lavoro senza volerlo: licenziamento, fine di un contratto a termine, dimissioni per giusta causa, risoluzione consensuale nella procedura di conciliazione.</li>
<li>Servono almeno 13 settimane di contributi negli ultimi quattro anni.</li>
<li>Se nei 12 mesi prima ti sei dimesso volontariamente da un altro lavoro, le 13 settimane devono essere maturate nel nuovo rapporto, salvo alcune eccezioni come le dimissioni per giusta causa.</li>
<li>La domanda si presenta all'INPS entro 68 giorni dalla fine del rapporto, anche tramite patronato.</li>
</ul>
<p class="note">Stima con le regole 2026 del D.Lgs. 22/2015 e della <a href="https://www.inps.it/it/it/inps-comunica/notizie/dettaglio-news-page.news.2026.01.integrazione-salariale-assegni-disoccupazione-e-fondi-importi-2026.html" rel="noopener">circolare INPS n. 4 del 28 gennaio 2026</a>. Importi lordi: INPS trattiene l'IRPEF; le detrazioni per lavoro dipendente si applicano se le chiedi nella domanda. Importo e durata ufficiali li stabilisce INPS quando accoglie la domanda. <a href="https://www.inps.it/it/it/dettaglio-scheda.it.schede-servizio-strumento.schede-servizi.50593.naspi-indennit-mensile-di-disoccupazione.html" rel="noopener">Scheda INPS sulla NASpI</a>.</p>
<p>Vuoi sapere quanto prendi oggi di stipendio netto? <a href="/">Calcola il netto in busta</a> o cerca il tuo <a href="/stipendio-netto/">contratto e livello</a>.</p>
<h2>Domande frequenti</h2>
''' + "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in FAQ) + '''
<script>
(function(){
const S=''' + str(SOGLIA) + ''',M=''' + str(MAX) + ''',$=id=>document.getElementById(id);
const f=x=>{const [i,d]=x.toFixed(2).split(".");return i.replace(/\\B(?=(\\d{3})+(?!\\d))/g,".")+","+d;};
function calc(){
  const ral=Math.max(0,parseFloat($("n-ral").value)||0), w=Math.min(208,Math.max(0,Math.floor(parseFloat($("n-sett").value)||0))), o55=$("n-55").checked;
  const out=$("n-out");
  if(w<13){out.innerHTML="<p><b>Con meno di 13 settimane di contributi negli ultimi 4 anni la NASpI non spetta.</b></p>";return;}
  const r=ral/52*4.33, a=Math.min(M, r<=S?0.75*r:0.75*S+0.25*(r-S));
  const giorni=Math.floor(w/2)*7, s=o55?8:6, mesi=Math.ceil(giorni/30);
  let tot=0, rows="";
  for(let m=1;m<=mesi;m++){
    const g=Math.min(30,giorni-(m-1)*30), v=a*Math.pow(0.97,Math.max(0,m-s+1)), q=v*g/30; tot+=q;
    rows+="<tr><td>"+m+"°"+(g<30?" ("+g+" giorni)":"")+"</td><td class=\\"n\\">"+f(q)+" €</td></tr>";
  }
  out.innerHTML="<table><tbody><tr><td>Retribuzione media mensile</td><td class=\\"n\\">"+f(r)+" €</td></tr>"+
   "<tr class=\\"me\\"><td>NASpI lorda nei primi "+(s-1)+" mesi</td><td class=\\"n\\"><b>"+f(a)+" €</b></td></tr>"+
   "<tr><td>Durata</td><td class=\\"n\\">"+Math.floor(w/2)+" settimane (circa "+Math.round(giorni/30.4)+" mesi)</td></tr>"+
   "<tr><td>Totale lordo nel periodo</td><td class=\\"n\\">"+f(tot)+" €</td></tr></tbody></table>"+
   "<details><summary>Importo mese per mese</summary><table><thead><tr><th>Mese</th><th class=\\"n\\">Lordo</th></tr></thead><tbody>"+rows+"</tbody></table></details>";
}
["n-ral","n-sett","n-55"].forEach(id=>$(id).addEventListener("input",calc)); $("n-55").addEventListener("change",calc); calc();
})();
</script></main>'''
ld = {"@context": "https://schema.org", "@graph": [
  {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://stipendioccnl.it/"},
                                                 {"@type": "ListItem", "position": 2, "name": "Calcolo NASpI", "item": URL}]},
  {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]}
tpl = (R / "tredicesima-netta/index.html").read_text()
head = tpl[:tpl.find("<main")]
head = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", head, count=1)
for prop in ("description",):
    head = re.sub(r'(<meta name="description" content=")[^"]*', r"\g<1>" + DESC, head, count=1)
head = re.sub(r'(<meta property="og:description" content=")[^"]*', r"\g<1>" + DESC, head, count=1)
head = re.sub(r'(<meta property="og:title" content=")[^"]*', r"\g<1>" + TITLE, head, count=1)
head = head.replace("https://stipendioccnl.it/tredicesima-netta/", URL)
head = re.sub(r'<script type="application/ld\+json">.*?</script>', '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>", head, count=1, flags=re.S)
tail = tpl[tpl.find("</main>") + len("</main>"):]
out = R / "calcolo-naspi"; out.mkdir(exist_ok=True)
(out / "index.html").write_text(head + MAIN + tail)
# sitemap e indice di ricerca
sm = (R / "sitemap.xml").read_text()
if URL not in sm:
    sm = sm.replace("</urlset>", f"<url><loc>{URL}</loc><lastmod>2026-11-26</lastmod></url>\n</urlset>")
    (R / "sitemap.xml").write_text(sm)
si = json.loads((R / "search-index.json").read_text())
if not any(x[1] == "/calcolo-naspi/" for x in si):
    si.append(["Calcolo NASpI disoccupazione", "/calcolo-naspi/", 1]); (R / "search-index.json").write_text(json.dumps(si, ensure_ascii=False, separators=(",", ":")))
print("ok", eur(r25), eur(a25))
