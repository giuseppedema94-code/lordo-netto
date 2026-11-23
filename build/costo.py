# Pagine /costo-azienda/ e /netto-lordo/: eseguite da gen_html.py (usa page, faq, faqhtml, eur, E, BASE, write, urls, fit)
def _costo():
    T=json.load(open('/home/claude/build/costo.json'))
    g=lambda r: next(x for x in T if x['ral']==r)
    a,b,c=g(25000),g(30000),g(40000)
    pct=lambda x: f'{round(x["netA"]/x["tot"]*100)}'
    rows=''.join(f'<tr><td>{eur(x["ral"])}</td><td class="n"><b>{eur(x["tot"])}</b></td><td class="n">{eur(x["tot"]/12)}</td><td class="n">{eur(x["netA"])}</td></tr>' for x in T)
    body=f'''<h1>Costo azienda di un dipendente 2026</h1>
<p class="lead">Un dipendente con RAL di 30.000 euro costa all'azienda circa <b>{eur(b["tot"])} all'anno</b>, il 37% in più della RAL. In busta arrivano {eur(b["netA"])} netti: su 100 euro spesi dal datore, al lavoratore ne restano {pct(b)}.</p>
<h2>Cosa si aggiunge alla RAL</h2>
<p>Il datore paga la retribuzione lorda e, sopra, tre voci obbligatorie. I contributi INPS a suo carico, intorno al 29-30% della RAL per un impiegato di un'azienda privata (l'aliquota esatta dipende da settore, numero di dipendenti e agevolazioni). Il premio INAIL contro gli infortuni, che per un lavoro d'ufficio è sotto l'1%. Il TFR, cioè la liquidazione, che matura ogni anno per un importo pari a circa la RAL divisa per 13,5.</p>
<table><tbody>
<tr><td>RAL</td><td class="n">{eur(30000)}</td></tr>
<tr><td>Contributi INPS azienda (29,5%)</td><td class="n">+ {eur(b["inps"])}</td></tr>
<tr><td>INAIL (0,4%)</td><td class="n">+ {eur(b["inail"])}</td></tr>
<tr><td>TFR maturato (RAL / 13,5)</td><td class="n">+ {eur(b["tfr"])}</td></tr>
<tr class="me"><td><b>Costo azienda annuo</b></td><td class="n"><b>{eur(b["tot"])}</b></td></tr>
</tbody></table>
<p>Se il contratto prevede fondo pensione, cassa sanitaria o buoni pasto, il costo sale ancora. Nel <a href="{BASE}/#costo">calcolatore</a> puoi aggiungerli e cambiare le aliquote.</p>
<h2>Tabella costo azienda 2026</h2>
<p class="note">Impiegato del settore privato, INPS azienda 29,5%, INAIL 0,4%, TFR incluso; netto senza familiari a carico, addizionali regionale 1,73% e comunale 0,8%. Importi arrotondati all'euro.</p>
<div class="tw"><table><thead><tr><th>RAL</th><th class="n">Costo azienda</th><th class="n">Costo al mese (12)</th><th class="n">Netto annuo</th></tr></thead><tbody>{rows}</tbody></table></div>
<a class="cta" href="{BASE}/#costo">Calcola il costo con il tuo CCNL</a>
<p class="note">Per il netto mese per mese c'è la <a href="{BASE}/ral-netto/">tabella RAL netto</a>; per partire da uno stipendio netto, la pagina <a href="{BASE}/netto-lordo/">netto a lordo</a>.</p>'''
    qs=[('Quanto costa all\'azienda un dipendente con 30.000 euro lordi?',f'Circa {eur(b["tot"])} all\'anno nel 2026, cioè {eur(b["tot"]/12)} al mese su 12 mesi: RAL, contributi INPS a carico azienda (29,5%), INAIL e TFR.'),
        ('Quanto costa un dipendente con 25.000 euro lordi?',f'Circa {eur(a["tot"])} all\'anno, con INPS azienda al 29,5%, INAIL allo 0,4% e TFR.'),
        ('Quanto costa un dipendente con 40.000 euro lordi?',f'Circa {eur(c["tot"])} all\'anno. Al dipendente restano {eur(c["netA"])} netti.'),
        ('Come si calcola il costo azienda?','Si parte dalla RAL e si aggiungono i contributi INPS a carico del datore (circa 29-30%), il premio INAIL e il TFR maturato (RAL diviso 13,5). Una stima veloce: RAL per 1,37.'),
        ('Il TFR fa parte del costo azienda?','Sì. Il TFR viene pagato alla fine del rapporto o versato al fondo pensione, ma matura ogni mese ed è un costo dell\'anno in cui matura.')]
    body+=faqhtml(qs)
    write('costo-azienda/index.html',page(fit('Costo azienda dipendente 2026: calcolo e tabella'),f'Quanto costa un dipendente nel 2026: RAL più INPS azienda, INAIL e TFR. Con 30.000 euro lordi il costo è circa {eur(b["tot"])} all\'anno. Tabella fino a 80.000 €.','/costo-azienda/','#8a5a2f',body,[('Costo azienda',None)],[faq(qs)]))
    urls.append('/costo-azienda/')

    N=json.load(open('/home/claude/build/nettolordo.json'))
    h=lambda n: next(x for x in N if x['net']==n)
    p,q,s=h(1300),h(1500),h(2000)
    rows=''.join(f'<tr><td>{eur(x["net"])}</td><td class="n"><b>{eur(x["r13"])}</b></td><td class="n">{eur(x["lordoM"])}</td><td class="n">{eur(x["r14"])}</td></tr>' for x in N)
    body=f'''<h1>Da netto a lordo 2026: la RAL che serve</h1>
<p class="lead">Per avere 1.500 euro netti al mese nel 2026 serve una RAL di circa <b>{eur(q["r13"])}</b> su 13 mensilità, cioè {eur(q["lordoM"])} lordi al mese. Con 14 mensilità la RAL sale a {eur(q["r14"])}, perché lo stesso netto mensile si riceve per un mese in più.</p>
<h2>Come si passa dal netto al lordo</h2>
<p>Non esiste una percentuale fissa. IRPEF, detrazioni e taglio del cuneo cambiano con il reddito, quindi il lordo si trova per tentativi: si prova una RAL, si calcola il netto con le regole 2026 e si corregge finché il netto torna. La tabella sotto è fatta così, con lo stesso motore del calcolatore.</p>
<p>Lo scarto tra lordo e netto cresce con il reddito. A 1.000 euro netti il lordo mensile è quasi lo stesso ({eur(h(1000)["lordoM"])}), perché trattamento integrativo e taglio del cuneo compensano gran parte di tasse e contributi. A 1.500 euro netti il lordo è circa il 20% più alto, a 2.000 euro un terzo più alto ({eur(s["lordoM"])}).</p>
<h2>Tabella netto a lordo 2026</h2>
<p class="note">Netto di una busta ordinaria. Dipendente privato, INPS 9,19%, addizionali regionale 1,73% e comunale 0,8%, nessun familiare a carico. Tredicesima e quattordicesima nette sono più basse di una busta normale, perché su di esse non si applicano le detrazioni.</p>
<div class="tw"><table><thead><tr><th>Netto al mese</th><th class="n">RAL (13 mensilità)</th><th class="n">Lordo al mese</th><th class="n">RAL (14 mensilità)</th></tr></thead><tbody>{rows}</tbody></table></div>
<a class="cta" href="{BASE}/#netto-lordo">Calcola il lordo con il tuo comune</a>
<p class="note">Il percorso inverso è nella <a href="{BASE}/ral-netto/">tabella RAL netto</a>. Per sapere quanto costerebbe quella RAL al datore c'è la pagina <a href="{BASE}/costo-azienda/">costo azienda</a>.</p>'''
    qs=[('Quanto lordo serve per 1.500 euro netti al mese?',f'Circa {eur(q["r13"])} di RAL su 13 mensilità ({eur(q["lordoM"])} lordi al mese) o {eur(q["r14"])} su 14, nel 2026, senza familiari a carico.'),
        ('Quanto lordo serve per 1.300 euro netti al mese?',f'Circa {eur(p["r13"])} di RAL su 13 mensilità, cioè {eur(p["lordoM"])} lordi al mese.'),
        ('Quanto lordo serve per 2.000 euro netti al mese?',f'Circa {eur(s["r13"])} di RAL su 13 mensilità ({eur(s["lordoM"])} lordi al mese) o {eur(s["r14"])} su 14.'),
        ('Come si calcola il lordo partendo dal netto?','Si cerca la RAL che, tolti INPS 9,19%, IRPEF con detrazioni e cuneo fiscale e addizionali, dà il netto voluto. Non c\'è una formula diretta, perché le detrazioni cambiano con il reddito: la tabella e il calcolatore trovano il valore per approssimazioni successive.')]
    body+=faqhtml(qs)
    write('netto-lordo/index.html',page(fit('Netto a lordo 2026: tabella RAL per ogni netto mensile'),f'Quale RAL serve per un netto mensile da 1.000 a 4.000 euro nel 2026, su 13 o 14 mensilità. Per 1.500 euro netti servono circa {eur(q["r13"])} lordi l\'anno.','/netto-lordo/','#2f5f8a',body,[('Netto a lordo',None)],[faq(qs)]))
    urls.append('/netto-lordo/')
_costo()
