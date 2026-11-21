# Pagina /tredicesima-netta/: eseguita da gen_html.py (usa page, faq, eur, D, SLUG, SHORT...)
def _tred():
    com=next(c for c in D if c['k']=='commercio'); ex=next(l for l in com['lv'] if l['n']=='IV')
    meta=lambda v: eur(v/2)
    def rng(c):
        a=min(l['t13n'] for l in c['lv']); b=max(l['t13n'] for l in c['lv'])
        return f'{eur(a)} netti' if round(a)==round(b) else f'da {eur(a)} a {eur(b)} netti'
    tab=''
    for i,c in enumerate(D):
        k=c['k']; cs=SLUG[k]; sh=SHORT[k]
        rows=''.join(f'<tr><td><a href="{BASE}/stipendio-netto/{cs}/{lvslug(l["n"])}/">{E(l["n"])}</a></td><td class="n">{eur(l["t13l"])}</td><td class="n"><b>{eur(l["t13n"])}</b></td></tr>' for l in c['lv'])
        nota=' Per i docenti e gli ATA la tredicesima si calcola sullo stipendio tabellare: RPD e CIA sono pagati su 12 mesi e restano fuori.' if k=='scuola' else (' Le voci pagate su 12 mensilità restano fuori dalla tredicesima.' if any(l.get('acc') for l in c['lv']) else '')
        quat=' Il contratto prevede anche la quattordicesima, pagata di solito a luglio, con un importo simile.' if c['mens']==14 else (' Il contratto prevede mezza quattordicesima.' if c['mens']==13.5 else '')
        tab+=f'''<details id="{cs}"{" open" if i==0 else ""}><summary><b>{E(sh)}</b> <span class="note">{rng(c)}</span></summary>
<div class="tw"><table><thead><tr><th>Livello</th><th class="n">Tredicesima lorda</th><th class="n">Tredicesima netta</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="note">{E(c["nome"])}.{quat}{nota}</p></details>'''
    body=f'''<h1>Tredicesima netta 2026: quanto arriva a dicembre</h1>
<p class="lead">La tredicesima lorda vale una mensilità piena se hai lavorato tutto l'anno. Si pagano i contributi INPS e l'IRPEF, ma senza detrazioni: per questo il netto è più basso di quello di un mese normale. Con il minimo del IV livello Commercio, {eur(ex["t13l"],2)} lordi, la tredicesima netta è di circa <b>{eur(ex["t13n"])}</b>.</p>
<h2>Come si calcola la tredicesima netta</h2>
<ol>
<li><b>Lordo.</b> Retribuzione mensile (minimo, contingenza, scatti, superminimo) per i mesi lavorati nell'anno, diviso 12. Di solito una frazione di almeno 15 giorni conta come mese intero.</li>
<li><b>Contributi.</b> Si tolgono i contributi INPS del dipendente, il 9,19% nel settore privato.</li>
<li><b>IRPEF.</b> Sul resto si applicano gli scaglioni (23%, 33%, 43%) come su una mensilità in più. Le detrazioni per lavoro dipendente, il taglio del cuneo e il trattamento integrativo non si sommano: sono già distribuiti sulle buste da gennaio a dicembre.</li>
<li><b>Addizionali.</b> Le addizionali regionale e comunale non si trattengono sulla tredicesima: si pagano a rate nelle buste ordinarie.</li>
</ol>
<p>A fine anno il conguaglio IRPEF fa i conti sull'intero reddito, quindi il totale delle tasse non cambia: cambia solo come si distribuiscono tra i mesi.</p>
<h2>Esempio: IV livello Commercio</h2>
<table><tbody>
<tr><td>Tredicesima lorda</td><td class="n">{eur(ex["t13l"],2)}</td></tr>
<tr><td>Contributi INPS</td><td class="n">− {eur(ex["t13c"],2)}</td></tr>
<tr><td>IRPEF, senza detrazioni</td><td class="n">− {eur(ex["t13i"],2)}</td></tr>
<tr class="me"><td><b>Tredicesima netta</b></td><td class="n"><b>{eur(ex["t13n"],2)}</b></td></tr>
</tbody></table>
<p>La busta ordinaria dello stesso livello è di circa {eur(ex["netM"])} netti. Se hai lavorato sei mesi, la tredicesima lorda si dimezza a circa {meta(ex["t13l"])}.</p>
<h2>Quando si paga</h2>
<p>Di norma con lo stipendio di dicembre, prima di Natale; la data precisa la fissa il CCNL. Alcune aziende la pagano a ratei, un dodicesimo in ogni busta: il totale annuo è lo stesso. Se il rapporto finisce durante l'anno, i ratei maturati arrivano con l'ultima busta.</p>
<h2>Tredicesima netta per CCNL e livello</h2>
<p>Importi 2026 sui minimi contrattuali, per un anno intero di lavoro, senza scatti né superminimo.</p>
{tab}
<a class="cta" href="{BASE}/">Calcola la tua tredicesima</a>
<script>function _o(){{var d=location.hash&&document.getElementById(location.hash.slice(1));if(d&&d.tagName==="DETAILS"){{d.open=true;d.scrollIntoView()}}}}addEventListener("hashchange",_o);_o()</script><p class="note">Nel calcolatore scegli «Dicembre, con la tredicesima» nel campo della mensilità aggiuntiva: vedi la busta di dicembre completa, con la tua RAL, gli scatti e il tuo comune.</p>'''
    qs=[('Quanto è la tredicesima netta?',f'Circa il 70% della tredicesima lorda per i redditi fino a 28.000 euro: sul lordo si pagano l\'INPS (9,19%) e l\'IRPEF al 23% senza detrazioni. Al IV livello Commercio sono circa {eur(ex["t13n"])} netti su {eur(ex["t13l"])} lordi.'),
        ('Perché la tredicesima è tassata di più?','Non c\'è un\'aliquota speciale. Le detrazioni per lavoro dipendente sono già ripartite sulle dodici buste ordinarie, quindi sulla tredicesima l\'IRPEF si paga piena. Il conguaglio di fine anno riallinea il totale.'),
        ('La tredicesima spetta anche a chi ha lavorato pochi mesi?','Sì, in proporzione: un dodicesimo della retribuzione mensile per ogni mese lavorato. Di solito conta come mese intero una frazione di almeno 15 giorni.'),
        ('Sulla tredicesima si pagano le addizionali?','No, le addizionali regionale e comunale si trattengono a rate nelle buste ordinarie, non sulla tredicesima.')]
    body+=faqhtml(qs)
    tt='Tredicesima netta 2026: calcolo e importi per CCNL'
    dd='Tredicesima netta 2026: come si calcola, perché è più bassa di un mese normale e quanto vale livello per livello in 16 CCNL, dal Commercio alla Scuola.'
    write('tredicesima-netta/index.html',page(fit(tt),dd,'/tredicesima-netta/','#2f8a5f',body,[('Tredicesima netta',None)],[faq(qs)]))
    urls.append('/tredicesima-netta/')
_tred()
