# Pagina /ral-netto/: eseguita da gen_html.py (usa page, faq, faqhtml, eur, E, BASE, write, urls)
def _ral():
    T=json.load(open('/home/claude/build/ral.json'))
    g=lambda r: next(x for x in T if x['ral']==r)
    a,b,c=g(25000),g(30000),g(40000)
    rows=''.join(f'<tr id="ral-{x["ral"]}"><td>{eur(x["ral"])}</td><td class="n">{eur(x["netA"])}</td><td class="n"><b>{eur(x["m13"])}</b></td><td class="n">{eur(x["m14"])}</td></tr>' for x in T)
    body=f'''<h1>RAL e netto 2026: quanto prendi al mese</h1>
<p class="lead">Con una RAL di 30.000 euro nel 2026 il netto è di circa <b>{eur(b["netA"])} all'anno</b>, cioè {eur(b["m13"])} al mese su 13 mensilità o {eur(b["m14"])} su 14. Sotto trovi la tabella da 12.000 a 100.000 euro lordi, per un dipendente del settore privato senza familiari a carico.</p>
<h2>Da lordo a netto: cosa si toglie</h2>
<p>Dalla RAL si tolgono tre voci. Primo, i contributi INPS del dipendente, il 9,19%. Poi l'IRPEF sul resto, con gli scaglioni 2026 al 23% fino a 28.000 euro, 33% fino a 50.000 e 43% oltre, meno le detrazioni per lavoro dipendente e il taglio del cuneo fiscale. Infine le addizionali regionale e comunale, che cambiano da comune a comune.</p>
<table><tbody>
<tr><td>RAL</td><td class="n">{eur(30000)}</td></tr>
<tr><td>Contributi INPS (9,19%)</td><td class="n">− {eur(b["inps"])}</td></tr>
<tr><td>IRPEF netta, dopo detrazioni e cuneo</td><td class="n">− {eur(b["irpef"])}</td></tr>
<tr><td>Addizionali regionale e comunale</td><td class="n">− {eur(b["add"])}</td></tr>
<tr class="me"><td><b>Netto annuo</b></td><td class="n"><b>{eur(b["netA"])}</b></td></tr>
</tbody></table>
<p>Su 30.000 euro lordi restano in tasca circa {round(b["netA"]/300)} euro ogni 100. A 40.000 euro la quota scende a {round(c["netA"]/400)}, perché una parte del reddito passa allo scaglione del 33% e le detrazioni calano.</p>
<h2>Tredici o quattordici mensilità</h2>
<p>Il netto annuo non cambia: cambia solo come viene diviso. Con la quattordicesima (Commercio, Turismo, Pubblici esercizi, Alimentare) la busta di ogni mese è più bassa, ma a luglio arriva una mensilità in più. Le cifre mensili in tabella sono quelle di una busta ordinaria; tredicesima e quattordicesima nette sono più basse perché su di esse non si applicano le detrazioni (vedi la <a href="{BASE}/tredicesima-netta/">pagina sulla tredicesima</a>).</p>
<h2>Tabella RAL netto 2026</h2>
<p class="note">Dipendente privato, INPS 9,19%, addizionale regionale 1,73% e comunale 0,8%, nessun familiare a carico. Importi arrotondati all'euro.</p>
<div class="tw"><table><thead><tr><th>RAL</th><th class="n">Netto annuo</th><th class="n">Netto mese (13)</th><th class="n">Netto mese (14)</th></tr></thead><tbody>{rows}</tbody></table></div>
<a class="cta" href="{BASE}/">Calcola il netto con il tuo comune</a>
<p class="note">Nel calcolatore puoi indicare comune, familiari a carico, fondo pensione e benefit. Se cerchi la RAL che serve per un certo netto, c'è la <a href="{BASE}/netto-lordo/">tabella netto a lordo</a>; per sapere quanto costi all'azienda, la pagina <a href="{BASE}/costo-azienda/">costo azienda</a>. Per i minimi contrattuali livello per livello c'è l'<a href="{BASE}/stipendio-netto/">elenco dei CCNL</a>.</p>'''
    qs=[('Quanto è il netto di 30.000 euro lordi?',f'Circa {eur(b["netA"])} all\'anno nel 2026: {eur(b["m13"])} al mese su 13 mensilità, {eur(b["m14"])} su 14. Il calcolo vale per un dipendente privato senza familiari a carico, con addizionali medie.'),
        ('Quanto è il netto di 25.000 euro lordi?',f'Circa {eur(a["netA"])} all\'anno, cioè {eur(a["m13"])} al mese su 13 mensilità.'),
        ('Quanto è il netto di 40.000 euro lordi?',f'Circa {eur(c["netA"])} all\'anno, cioè {eur(c["m13"])} al mese su 13 mensilità o {eur(c["m14"])} su 14.'),
        ('Che cos\'è la RAL?','La retribuzione annua lorda: tutto quello che il datore paga in un anno prima di contributi e tasse, compresi tredicesima ed eventuale quattordicesima. Non comprende i contributi a carico dell\'azienda, che fanno parte del costo del lavoro.'),
        ('Perché il mio netto è diverso dalla tabella?','Le addizionali regionale e comunale variano molto tra i comuni; familiari a carico, straordinari, premi, fondo pensione e buoni pasto spostano il risultato. Nel calcolatore puoi inserire tutte queste voci.')]
    body+=faqhtml(qs)
    tt='RAL netto 2026: tabella da 12.000 a 100.000 euro'
    dd=f'Netto 2026 per ogni RAL da 12.000 a 100.000 euro: annuo e mensile su 13 o 14 mensilità. Con 30.000 euro lordi il netto è circa {eur(b["m13"])} al mese.'
    write('ral-netto/index.html',page(fit(tt),dd,'/ral-netto/','#2f8a5f',body,[('RAL netto',None)],[faq(qs)]))
    urls.append('/ral-netto/')
_ral()
