# Pagina /stipendio-netto/colf-badanti/: CCNL lavoro domestico. Eseguita da gen_html.py.
# Calcolo a parte (non usa il motore): il datore domestico non trattiene l'IRPEF, in busta si tolgono
# solo la quota INPS del lavoratore (importo fisso orario) e la quota Cassa Colf. Dati in domestico.json.
def _dom():
    X=json.load(open('/home/claude/build/domestico.json'))
    H=52/12; ORE=X['ore_conviventi']; cc=X['cassacolf']
    def q24(paga):  # quota INPS lavoratore fino a 24 ore: fascia sulla paga oraria con il rateo di tredicesima
        eff=paga*13/12
        for lim,q in X['inps_fino24']:
            if lim is None or eff<=lim: return q
    def mese(paga,ore):
        h=ore*H; q=X['inps_oltre24'] if ore>24 else q24(paga)
        lor=paga*h; tr=(q+cc)*h
        return lor,tr,lor-tr
    cs='colf-badanti'; L=X['livelli']
    conv=[]
    for n,m,o,dsc in L:
        h=ORE*H; tr=(X['inps_oltre24']+cc)*h
        conv.append((n,m,tr,m-tr,dsc))
    rc=''.join(f'<tr><td><b>{n}</b><br><span class="note">{E(d)}</span></td><td class="n">{eur(m,2)}</td><td class="n">− {eur(t,2)}</td><td class="n"><b>{eur(v)}</b></td></tr>' for n,m,t,v,d in conv)
    rn=''
    for n,m,o,d in L:
        a=mese(o,20); b=mese(o,40)
        rn+=f'<tr><td><b>{n}</b></td><td class="n">{eur(o,2)}</td><td class="n">{eur(a[2])}</td><td class="n">{eur(b[2])}</td></tr>'
    g=lambda k: next(x for x in conv if x[0]==k)
    bs,csx,a=g('BS'),g('CS'),g('A')
    nB=next(x for x in L if x[0]=='B'); m25=mese(nB[2],25)
    body=f'''<h1>Stipendio netto colf e badanti 2026: CCNL lavoro domestico</h1>
<p class="lead">Nel 2026 una badante convivente di livello BS ha un minimo di {eur(bs[1],2)} lordi al mese, circa <b>{eur(bs[3])} netti</b> in busta. Il datore di lavoro domestico non trattiene l'IRPEF: dalla paga si tolgono solo i contributi INPS a carico del lavoratore e la quota della Cassa Colf.</p>
<h2>Minimi 2026 per lavoratori conviventi</h2>
<p>Minimo mensile per {ORE} ore settimanali, in vigore dal 1° gennaio 2026. Netto dopo la quota INPS del lavoratore ({eur(X["inps_oltre24"],2)} l'ora) e la Cassa Colf ({eur(cc,2)} l'ora), su circa {round(ORE*H)} ore al mese. Vitto e alloggio sono in più, a carico del datore.</p>
<div class="tw"><table><thead><tr><th>Livello</th><th class="n">Minimo lordo</th><th class="n">Trattenute</th><th class="n">Netto al mese</th></tr></thead><tbody>{rc}</tbody></table></div>
<h2>Paga oraria 2026 per lavoratori non conviventi</h2>
<p>Minimo orario e netto al mese con 20 e con 40 ore settimanali. Sotto le 25 ore la quota INPS dipende dalla paga oraria; da 25 ore in su è fissa a {eur(X["inps_oltre24"],2)} l'ora.</p>
<div class="tw"><table><thead><tr><th>Livello</th><th class="n">Minimo orario</th><th class="n">Netto, 20 ore</th><th class="n">Netto, 40 ore</th></tr></thead><tbody>{rn}</tbody></table></div>
<h2>Perché in busta non c'è l'IRPEF</h2>
<p>La famiglia che assume una colf o una badante non è sostituto d'imposta: paga lo stipendio lordo meno i contributi del lavoratore, e non versa tasse per suo conto. L'IRPEF la paga il lavoratore con la dichiarazione dei redditi, sul totale dell'anno, con le detrazioni per lavoro dipendente. Fino a 8.500 euro l'anno le detrazioni coprono tutta l'imposta. Per la dichiarazione il datore rilascia ogni anno il riepilogo dei compensi pagati.</p>
<p>Per questo il netto di queste tabelle non va confrontato con quello degli altri CCNL: lì l'IRPEF è già tolta in busta, qui va pagata dopo, se dovuta.</p>
<h2>Cosa si aggiunge al minimo</h2>
<ul>
<li><b>Tredicesima.</b> Una mensilità in più a dicembre, calcolata anche sul valore di vitto e alloggio per chi li riceve.</li>
<li><b>Vitto e alloggio.</b> Per il convivente sono dovuti dal datore. Se non vengono dati, valgono {eur(X["vitto_alloggio_giorno"],2)} al giorno (2,33 € a pasto e 2 € l'alloggio).</li>
<li><b>Scatti di anzianità</b> ogni due anni presso lo stesso datore.</li>
<li><b>TFR</b> alla fine del rapporto, e le indennità previste per baby sitter e per l'assistenza a più persone non autosufficienti.</li>
</ul>
<p>Il rinnovo del contratto prevede altri aumenti dal 1° gennaio 2027.</p>
<h2>Come si calcolano i contributi</h2>
<p>I contributi del lavoro domestico non sono una percentuale della paga ma un importo fisso per ogni ora pagata, aggiornato ogni anno dall'INPS. Il datore li versa ogni trimestre e trattiene in busta la parte del lavoratore. Fino a 24 ore settimanali la quota del lavoratore è di 0,43 € l'ora con paga oraria fino a 9,61 € (tredicesima compresa), 0,48 € fino a 11,70 € e 0,59 € oltre; da 25 ore in su è sempre di {eur(X["inps_oltre24"],2)} l'ora.</p>
<p class="note">Fonti: {E(X["fonte"])}. Stime sui minimi, senza scatti né superminimo. Verificato il 24/11/2026.</p>'''
    qs=[('Quanto prende netto una badante convivente nel 2026?',f'Con il livello BS (persona autosufficiente) il minimo è {eur(bs[1],2)} lordi al mese, circa {eur(bs[3])} netti. Con il livello CS (persona non autosufficiente) {eur(csx[1],2)} lordi, circa {eur(csx[3])} netti. Vitto e alloggio sono in più.'),
        ('Quanto è la paga oraria minima di una colf nel 2026?',f'Per un non convivente va da {eur(L[0][2],2)} l\'ora (livello A) a {eur(L[-1][2],2)} (livello DS). Per una colf con esperienza, livello B, è {eur(nB[2],2)} l\'ora: con 25 ore settimanali sono circa {eur(m25[2])} netti al mese.'),
        ('Il datore domestico trattiene l\'IRPEF?','No. La famiglia non è sostituto d\'imposta e trattiene solo i contributi INPS del lavoratore e la quota della Cassa Colf. L\'IRPEF, se dovuta, la paga il lavoratore con la dichiarazione dei redditi.'),
        ('Quanti contributi paga una colf?',f'Nel 2026 la quota a carico del lavoratore va da 0,43 a 0,59 euro l\'ora fino a 24 ore settimanali e vale {eur(X["inps_oltre24"],2)} l\'ora oltre le 24 ore. Il resto dei contributi lo paga il datore.')]
    body+=faqhtml(qs)
    tt='Stipendio netto colf e badanti 2026 per livello'
    dd=f'Stipendio colf e badanti 2026 col CCNL lavoro domestico: minimi per livello, paga oraria, contributi INPS e netto. Badante convivente BS: circa {eur(bs[3])} netti.'
    write(f'stipendio-netto/{cs}/index.html',page(fit(tt),dd,f'/stipendio-netto/{cs}/','#7a4f9a',body,[('Stipendi per CCNL',f'{BASE}/stipendio-netto/'),('Colf e badanti',None)],[faq(qs)]))
    urls.append(f'/stipendio-netto/{cs}/')
    p=os.path.join(OUT,'stipendio-netto/index.html'); s=open(p).read()
    s=s.replace('</tbody></table>',f'<tr><td><a href="{BASE}/stipendio-netto/{cs}/">Colf e badanti</a></td><td>Lavoro domestico (Fidaldo, Domina)</td><td class="n">{len(L)}</td></tr></tbody></table>',1)
    open(p,'w').write(s)
_dom()
