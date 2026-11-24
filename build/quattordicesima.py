# Pagina /quattordicesima-netta/: eseguita da gen_html.py (usa page, faq, faqhtml, eur, D, SLUG, SHORT...)
# Importi da mensAgg del motore (campi t14* in pages.json), nessuna modifica al motore.
def _quat():
    con=[c for c in D if c['mens']>13]
    senza=[SHORT[c['k']] for c in D if c['mens']<=13]
    com=next(c for c in D if c['k']=='commercio'); ex=next(l for l in com['lv'] if l['n']=='IV')
    def rng(c):
        a=min(l['t14n'] for l in c['lv']); b=max(l['t14n'] for l in c['lv'])
        return f'{eur(a)} netti' if round(a)==round(b) else f'da {eur(a)} a {eur(b)} netti'
    tab=''
    for i,c in enumerate(con):
        k=c['k']; cs=SLUG[k]; sh=SHORT[k]
        rows=''.join(f'<tr><td><a href="{BASE}/stipendio-netto/{cs}/{lvslug(l["n"])}/">{E(l["n"])}</a></td><td class="n">{eur(l["t14l"])}</td><td class="n"><b>{eur(l["t14n"])}</b></td></tr>' for l in c['lv'])
        nota=' Il contratto prevede mezza mensilità in più: gli importi sono la metà di una mensilità.' if c['mens']==13.5 else ''
        tab+=f'''<details id="{cs}"{" open" if i==0 else ""}><summary><b>{E(sh)}</b> <span class="note">{rng(c)}</span></summary>
<div class="tw"><table><thead><tr><th>Livello</th><th class="n">Quattordicesima lorda</th><th class="n">Quattordicesima netta</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="note">{E(c["nome"])}.{nota}</p></details>'''
    body=f'''<h1>Quattordicesima netta 2026: chi la prende e quanto vale</h1>
<p class="lead">La quattordicesima è una mensilità in più prevista da alcuni CCNL, tra cui Commercio, Turismo e Pubblici esercizi, e si paga di solito con lo stipendio di luglio. Come la tredicesima, si tassa senza detrazioni. Con il minimo del IV livello Commercio, {eur(ex["t14l"],2)} lordi, la quattordicesima netta è di circa <b>{eur(ex["t14n"])}</b>.</p>
<h2>Chi ha diritto alla quattordicesima</h2>
<p>Non è prevista dalla legge: spetta solo se la prevede il contratto collettivo applicato. Tra i contratti di questo sito la hanno {", ".join(SHORT[c["k"]] for c in con if c["mens"]==14)}. Le Cooperative sociali prevedono mezza mensilità in più. Non la prevedono {", ".join(senza)}.</p>
<p>Il pensionato che riceve la «quattordicesima» INPS è un caso diverso: è una somma aggiuntiva sulla pensione, con regole e importi propri.</p>
<h2>Come si calcola</h2>
<ol>
<li><b>Lordo.</b> Una retribuzione mensile per ogni anno intero di lavoro. Il periodo di maturazione di solito va da luglio a giugno: chi ha lavorato meno riceve un dodicesimo per ogni mese, e una frazione di almeno 15 giorni conta come mese intero.</li>
<li><b>Contributi.</b> Si tolgono i contributi INPS del dipendente, il 9,19% nel settore privato.</li>
<li><b>IRPEF.</b> Si applicano gli scaglioni (23%, 33%, 43%) senza detrazioni né taglio del cuneo, che sono già distribuiti sulle buste ordinarie.</li>
<li><b>Addizionali.</b> Le addizionali regionale e comunale non si trattengono sulla quattordicesima.</li>
</ol>
<p>Con il conguaglio di fine anno l'IRPEF si ricalcola sul reddito totale: la quattordicesima non fa pagare più tasse in assoluto, cambia solo il mese in cui si pagano.</p>
<h2>Esempio: IV livello Commercio</h2>
<table><tbody>
<tr><td>Quattordicesima lorda</td><td class="n">{eur(ex["t14l"],2)}</td></tr>
<tr><td>Contributi INPS</td><td class="n">− {eur(ex["t14c"],2)}</td></tr>
<tr><td>IRPEF, senza detrazioni</td><td class="n">− {eur(ex["t14i"],2)}</td></tr>
<tr class="me"><td><b>Quattordicesima netta</b></td><td class="n"><b>{eur(ex["t14n"],2)}</b></td></tr>
</tbody></table>
<p>La busta ordinaria dello stesso livello è di circa {eur(ex["netM"])} netti. Chi è stato assunto a gennaio riceve a luglio sei dodicesimi, circa {eur(ex["t14l"]/2)} lordi.</p>
<h2>Quattordicesima netta per CCNL e livello</h2>
<p>Importi 2026 sui minimi contrattuali, per un periodo intero di maturazione, senza scatti né superminimo.</p>
{tab}
<a class="cta" href="{BASE}/">Calcola la tua quattordicesima</a>
<script>function _o(){{var d=location.hash&&document.getElementById(location.hash.slice(1));if(d&&d.tagName==="DETAILS"){{d.open=true;d.scrollIntoView()}}}}addEventListener("hashchange",_o);_o()</script><p class="note">Per la mensilità di dicembre c'è la <a href="{BASE}/tredicesima-netta/">tabella della tredicesima netta</a>. Per il netto annuo con 14 mensilità c'è la <a href="{BASE}/ral-netto/">tabella RAL netto</a>.</p>'''
    qs=[('Quanto è la quattordicesima netta?',f'Circa il 70% della quattordicesima lorda per i redditi fino a 28.000 euro: si pagano l\'INPS (9,19%) e l\'IRPEF al 23% senza detrazioni. Al IV livello Commercio sono circa {eur(ex["t14n"])} netti su {eur(ex["t14l"])} lordi.'),
        ('Quando si paga la quattordicesima?','Di solito con lo stipendio di luglio. La data precisa e il periodo di maturazione, in genere da luglio a giugno, li fissa il CCNL.'),
        ('Chi ha diritto alla quattordicesima?','Solo i dipendenti a cui si applica un CCNL che la prevede, come Commercio, Turismo, Pubblici esercizi, Studi professionali, Industria alimentare, Logistica e Gas-Acqua. Metalmeccanici, Scuola, bancari ABI e altri contratti non la prevedono.'),
        ('Perché la quattordicesima netta è più bassa di uno stipendio normale?','Perché le detrazioni per lavoro dipendente e il taglio del cuneo sono già ripartiti sulle buste ordinarie. Sulla quattordicesima l\'IRPEF si paga piena; il conguaglio di fine anno riallinea il totale.')]
    body+=faqhtml(qs)
    tt='Quattordicesima netta 2026: calcolo e importi per CCNL'
    dd='Quattordicesima netta 2026: chi la riceve, quando si paga, come si calcola e quanto vale per livello nei CCNL che la prevedono, dal Commercio al Turismo.'
    write('quattordicesima-netta/index.html',page(fit(tt),dd,'/quattordicesima-netta/','#2f8a5f',body,[('Quattordicesima netta',None)],[faq(qs)]))
    urls.append('/quattordicesima-netta/')
_quat()
