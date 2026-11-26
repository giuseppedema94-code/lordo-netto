"""Genera /calcolo-tfr/ (calcolatore TFR 2026) con testata e piè di pagina della pagina tredicesima. Idempotente.
Regole: art. 2120 c.c. (quota = retribuzione annua / 13,5; rivalutazione 1,5% + 75% inflazione FOI),
L. 297/1982 (contributo 0,50% a carico del TFR), imposta sostitutiva 17% sulla rivalutazione,
tassazione separata TUIR artt. 17 e 19 (aliquota media sul reddito di riferimento)."""
import json, re
from pathlib import Path
R = Path(__file__).resolve().parent.parent
COEFF, COEFF_MESE = 5.234938, "ottobre 2026"   # ultimo coefficiente ISTAT di rivalutazione del TFR al 31/12/2025
URL = "https://stipendioccnl.it/calcolo-tfr/"
TITLE = "Calcolo TFR 2026: quanto matura e quanto prendi netto"
DESC = ("Calcolo TFR 2026: quota annua (RAL diviso 13,5 meno lo 0,50%), rivalutazione ISTAT e TFR netto alla fine del "
        "rapporto con la tassazione separata.")
SC = [(28000, .23), (50000, .33), (float("inf"), .43)]
def irpef(r):
    t, p = 0, 0
    for lim, a in SC:
        if r > p: t += (min(r, lim) - p) * a
        p = lim
    return t
def calcolo(ral, anni, fondo=None, mesi=12):
    q = ral / 13.5 - ral * 0.005               # quota annua accantonata
    f0 = q * anni if fondo is None else fondo
    riv = f0 * COEFF / 100 * 0.83
    q26 = q * mesi / 12
    lordo = f0 + riv + q26
    imp = f0 + q26
    tot_anni = anni + mesi / 12
    rif = imp / tot_anni * 12 if tot_anni > 0 else 0
    al = irpef(rif) / rif if rif > 0 else 0
    tasse = imp * al
    return dict(q=q, f0=f0, riv=riv, q26=q26, lordo=lordo, rif=rif, al=al, tasse=tasse, netto=lordo - tasse)
def eur(x): return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
E = calcolo(30000, 10)
assert abs(E["q"] - 2072.22) < 0.01 and abs(E["netto"] - 18452.15) < 0.05, E
FAQ = [
 ("Quanto TFR matura in un anno?",
  f"Circa la RAL divisa 13,5, meno lo 0,50% della retribuzione che il datore versa all'INPS. Con 30.000 € lordi l'anno sono {eur(E['q'])} €."),
 ("Come si rivaluta il TFR?",
  "Ogni 31 dicembre il TFR già accantonato cresce dell'1,5% più il 75% dell'inflazione ISTAT dell'anno. Sulla rivalutazione si paga un'imposta del 17%, trattenuta ogni anno."),
 ("Quanto si paga di tasse sul TFR?",
  "Il TFR ha la tassazione separata: si divide per gli anni di servizio, si moltiplica per 12 e sul risultato si calcola l'aliquota IRPEF media, che poi si applica a tutto il TFR. Non si pagano le addizionali regionale e comunale."),
 ("Quanto prende netto chi ha 10 anni di servizio con 30.000 € di RAL?",
  f"Circa {eur(E['netto'])} € netti su {eur(E['lordo'])} € lordi, lasciando il lavoro a fine 2026, senza contare le rivalutazioni degli anni passati."),
]
MAIN = f'''<main class="w"><div class="crumb">Calcolo TFR</div><h1>Calcolo TFR 2026: quanto matura e quanto prendi netto</h1>
<p class="lead">Ogni anno il TFR cresce di circa la tua RAL divisa 13,5, meno lo 0,50%. Il fondo già accantonato si rivaluta dell'1,5% più il 75% dell'inflazione: nel 2026, con l'ultimo dato ISTAT ({COEFF_MESE}, valido per chi lascia il lavoro tra metà ottobre e metà novembre), la rivalutazione è del <b>{eur(COEFF)}%</b>. Alla fine del rapporto il TFR ha una tassazione separata, con un'aliquota media di solito più bassa di quella sullo stipendio.</p>
<div class="box" id="tfr-calc">
<p><label for="t-ral"><b>RAL lorda annua</b> (tredicesima e quattordicesima comprese)</label><br><input id="t-ral" type="number" min="0" step="100" value="30000" inputmode="decimal"> €</p>
<p><label for="t-anni"><b>Anni di servizio fino al 31/12/2025</b></label><br><input id="t-anni" type="number" min="0" max="50" step="0.5" value="10" inputmode="decimal"></p>
<p><label for="t-fondo"><b>TFR maturato al 31/12/2025</b> (lo trovi in busta paga; se lo lasci vuoto lo stimo dalla RAL)</label><br><input id="t-fondo" type="number" min="0" step="100" placeholder="facoltativo" inputmode="decimal"> €</p>
<p><label for="t-mesi"><b>Mesi lavorati nel 2026</b> prima della fine del rapporto</label><br><input id="t-mesi" type="number" min="0" max="12" step="1" value="12" inputmode="numeric"></p>
<div id="t-out" aria-live="polite"></div>
</div>
<h2>Come si calcola</h2>
<ol>
<li><b>Quota dell'anno.</b> La retribuzione annua, comprese le mensilità aggiuntive, divisa 13,5. Da questa si toglie lo 0,50% della retribuzione, il contributo che il datore versa all'INPS (legge 297/1982).</li>
<li><b>Rivalutazione.</b> Al 31 dicembre il TFR accantonato fino all'anno prima cresce dell'1,5% più il 75% dell'aumento dei prezzi ISTAT (famiglie di operai e impiegati). Sulla rivalutazione il datore trattiene un'imposta del 17%.</li>
<li><b>Tasse.</b> Alla fine del rapporto si calcola il reddito di riferimento: TFR diviso gli anni di servizio, per 12. L'IRPEF di quel reddito, con gli scaglioni 2026 (23%, 33%, 43%), dà l'aliquota media, che si applica al TFR senza le rivalutazioni già tassate. Niente addizionali regionali e comunali.</li>
<li><b>Ricalcolo.</b> Più avanti l'Agenzia delle Entrate rifà i conti con l'aliquota media dei tuoi ultimi cinque anni di redditi e può chiedere o restituire una differenza.</li>
</ol>
<p class="note">Stima per il TFR rimasto in azienda o nel Fondo di Tesoreria INPS, maturato dal 2001 in poi. Se il TFR è stato versato a un fondo pensione valgono altre regole: sulla parte maturata dal 2007 un'imposta dal 15% al 9%, che scende con gli anni di iscrizione. Senza il TFR della busta paga il fondo è stimato con la RAL attuale e senza le rivalutazioni passate, quindi esce più basso del reale. Fonti: art. 2120 del Codice civile, <a href="https://ance.it/2026/01/legge-29-maggio-1982-n-297-tfr-indice-istat-relativo-al-mese-di-dicembre-2025/" rel="noopener">coefficiente ISTAT di dicembre 2025 (2,311148%)</a>, <a href="https://www.assolombarda.it/servizi/informazioni-economiche/trattamento-di-fine-rapporto-tfr-nota-informativa-ottobre-2026" rel="noopener">coefficiente di {COEFF_MESE}</a>.</p>
<p>Vuoi sapere anche quanto prenderesti di disoccupazione? <a href="/calcolo-naspi/">Calcola la NASpI</a>. Per lo stipendio netto di oggi: <a href="/stipendio-netto/">cerca il tuo CCNL</a>.</p>
<h2>Domande frequenti</h2>
''' + "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in FAQ) + '''
<script>
(function(){
const COEFF=''' + str(COEFF) + ''',SC=[[28000,.23],[50000,.33],[Infinity,.43]],$=id=>document.getElementById(id);
const f=x=>{const [i,d]=x.toFixed(2).split(".");return i.replace(/\\B(?=(\\d{3})+(?!\\d))/g,".")+","+d;};
const irpef=r=>{let t=0,p=0;for(const [l,a] of SC){if(r>p)t+=(Math.min(r,l)-p)*a;p=l;}return t;};
const num=id=>parseFloat(($(id).value||"").replace(",","."));
function calc(){
  const ral=Math.max(0,num("t-ral")||0), anni=Math.max(0,num("t-anni")||0), mesi=Math.min(12,Math.max(0,Math.round(num("t-mesi")||0)));
  const fv=num("t-fondo"), q=ral/13.5-ral*0.005, f0=isNaN(fv)?q*anni:Math.max(0,fv);
  const riv=f0*COEFF/100*0.83, q26=q*mesi/12, lordo=f0+riv+q26, imp=f0+q26, ta=anni+mesi/12;
  const rif=ta>0?imp/ta*12:0, al=rif>0?irpef(rif)/rif:0, tasse=imp*al;
  $("t-out").innerHTML="<table><tbody>"+
   "<tr><td>Quota TFR di un anno intero</td><td class=\\"n\\">"+f(q)+" €</td></tr>"+
   "<tr><td>TFR al 31/12/2025"+(isNaN(fv)?" (stima)":"")+"</td><td class=\\"n\\">"+f(f0)+" €</td></tr>"+
   "<tr><td>Rivalutazione 2026 (ultimo dato ISTAT), netta del 17%</td><td class=\\"n\\">+ "+f(riv)+" €</td></tr>"+
   "<tr><td>Quota 2026 ("+mesi+" mesi)</td><td class=\\"n\\">+ "+f(q26)+" €</td></tr>"+
   "<tr><td>TFR lordo alla fine del rapporto</td><td class=\\"n\\">"+f(lordo)+" €</td></tr>"+
   "<tr><td>Aliquota media (reddito di riferimento "+f(rif)+" €)</td><td class=\\"n\\">"+(al*100).toFixed(2).replace(".",",")+"%</td></tr>"+
   "<tr><td>Tasse</td><td class=\\"n\\">− "+f(tasse)+" €</td></tr>"+
   "<tr class=\\"me\\"><td>TFR netto stimato</td><td class=\\"n\\"><b>"+f(lordo-tasse)+" €</b></td></tr></tbody></table>";
}
["t-ral","t-anni","t-fondo","t-mesi"].forEach(id=>$(id).addEventListener("input",calc)); calc();
})();
</script></main>'''
ld = {"@context": "https://schema.org", "@graph": [
  {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://stipendioccnl.it/"},
                                                 {"@type": "ListItem", "position": 2, "name": "Calcolo TFR", "item": URL}]},
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
out = R / "calcolo-tfr"; out.mkdir(exist_ok=True)
(out / "index.html").write_text(head + MAIN + tail)
sm = (R / "sitemap.xml").read_text()
if URL not in sm:
    (R / "sitemap.xml").write_text(sm.replace("</urlset>", f"<url><loc>{URL}</loc><lastmod>2026-11-26</lastmod></url>\n</urlset>"))
si = json.loads((R / "search-index.json").read_text())
if not any(x[1] == "/calcolo-tfr/" for x in si):
    si.append(["Calcolo TFR liquidazione", "/calcolo-tfr/", 1]); (R / "search-index.json").write_text(json.dumps(si, ensure_ascii=False, separators=(",", ":")))
print("ok", eur(E["q"]), eur(E["lordo"]), eur(E["netto"]))
