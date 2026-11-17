# Progetto grafico "Foglio paga" (calcolatore)

File da modificare: `/home/claude/index.html` (unico file: CSS in `<style>`, HTML, JS). Non toccare il motore di calcolo
(tra `/* @engine-start */` e `/* @engine-end */`), né i testi, né gli id esistenti. Non fare git, non pubblicare.

L'aspetto di base resta quello attuale (Figtree, schede arrotondate, colore del CCNL in `--brand`, tema scuro).
Si cambiano tre cose: la fascia in alto, il pannello del risultato (diventa un foglio paga a modulo continuo), la tabella del cedolino.

## 1. Fascia colorata in alto
- Avvolgi `<section class="hero">…</section>` in `<div class="band"><div class="wrap">…</div></div>` e spostalo fuori da `<main>` (subito dopo `</header>`), se oggi è dentro `main.wrap`.
- `.band{background:var(--brand);color:#fff;padding:26px 0 84px}`; h1 bianco; `.hero p, .hero .lead` bianco con opacità .85.
- `.badge` e `.perks li`: fondo `rgba(255,255,255,.14)`, testo bianco, nessun bordo; la spunta dei perks bianca.
- La griglia principale `.grid` sale sopra la fascia: `margin-top:-60px; position:relative`.
- `header.top` resta com'è (stesso colore): fascia e testata formano un unico blocco colorato.
- Tema scuro: la fascia resta `var(--brand)`.

## 2. Il risultato è un foglio paga a modulo continuo
Variabili nuove in `:root`: `--paper:#fffdf6; --rule:color-mix(in srgb,var(--brand) 30%,var(--line));`
Tema scuro (nelle due regole già esistenti del tema scuro): `--paper:#1c2321`.

`.res` (la scheda del risultato, che è anche il contenitore che scorre):
```css
.res{border-radius:3px;border:0;box-shadow:0 1px 2px rgba(20,30,25,.08),0 12px 32px rgba(20,30,25,.10);
  background:
    radial-gradient(circle,var(--bg) 0 4.5px,transparent 5px) left top/22px 24px repeat-y local,
    radial-gradient(circle,var(--bg) 0 4.5px,transparent 5px) right top/22px 24px repeat-y local,
    var(--paper)}
.res>*{margin-left:22px;margin-right:22px}
.res>.sr{margin:0}
```
Sono i fori di trascinamento ai due lati del foglio. Sotto i 520px togli fori e margini (`background:var(--paper)`, margini 0).
Controlla che nessun figlio di `.res` abbia un fondo che copre i fori; `.res-hero`, `.kpis`, `.res-body` restano dentro i margini.
Tra i blocchi usa una linea di strappo: `border-top:1px dashed var(--rule)` (al posto dei bordi pieni attuali di `.kpis`).

### Testata del foglio (nuova)
Subito prima di `.res-hero` aggiungi:
```html
<div class="slip-head" id="slip-head" aria-hidden="true">
  <div><span>CCNL</span><b id="sh-ccnl"></b></div>
  <div><span>Livello</span><b id="sh-liv"></b></div>
  <div><span>Mensilità</span><b id="sh-mens"></b></div>
  <div><span>Periodo</span><b id="sh-per"></b></div>
</div>
```
```css
.slip-head{display:grid;grid-template-columns:1.6fr 1.1fr .7fr 1.1fr;border:1px solid var(--rule);margin-top:16px}
.slip-head div{padding:6px 9px 7px;border-left:1px solid var(--rule);min-width:0}
.slip-head div:first-child{border-left:0}
.slip-head span{display:block;font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--brand-t);opacity:.8}
.slip-head b{display:block;font-size:13px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
@media (max-width:520px){.slip-head{grid-template-columns:1fr 1fr}.slip-head div:nth-child(3){border-left:0}.slip-head div:nth-child(n+3){border-top:1px solid var(--rule)}}
```
JS, dentro `render()` dove si aggiornano gli altri output (vicino a `$("out-mens").textContent=`):
- `sh-ccnl`: testo dell'opzione scelta in `#ccnl`, tagliato al primo " – " (es. "Commercio").
- `sh-liv`: testo dell'opzione scelta in `#livello`, tagliato al primo " – "; se il CCNL non ha livelli, "—".
- `sh-mens`: valore di `#mens`.
- `sh-per`: "Mese ordinario 2026" in vista mensile, "Anno 2026" in vista annuale (la vista dipende da `#d-m` `aria-checked`).

### Riquadro del netto
`.res-hero` resta pieno nel colore `--brand` con testo bianco, ma diventa la casella "netto a pagare" del foglio:
`border-radius:0; margin-top:0; border:1px solid var(--brand); padding:14px 16px;` `position:sticky;top:0` resta.
Dentro: etichetta `.lbl` a sinistra in alto, valore `.val` in `font-family:var(--mono);font-weight:600;font-size:clamp(34px,4.4vw,44px)`, `.cap` sotto.
`.kpis`: due caselle bordate `1px solid var(--rule)` senza raggio, attaccate sotto il netto (`border-top:0`), numeri in `var(--mono)`.

### Tabella del cedolino a tre colonne
Oggi `table.ced` ha due colonne (voce, importo). Deve averne tre: **Voce | Competenze | Trattenute**.
- Nel JS che costruisce la tabella (funzione che scrive `$("det").innerHTML`, righe fatte da `[etichetta, valore, classe]`):
  se il valore (stringa) comincia con "–" o "-" va nella colonna Trattenute **senza il segno**; altrimenti nella colonna Competenze;
  l'altra cella resta vuota. Vale anche per il totale nelle righe di gruppo (`tr.gh`).
  Le righe `info` e `warn` con valore vuoto: `<td colspan="3">`.
- Aggiungi `<thead><tr><th>Voce</th><th>Competenze</th><th>Trattenute</th></tr></thead>`.
- `tfoot`: `<th>Netto in busta</th><td colspan="2">importo</td>` (mantieni il testo attuale dell'etichetta).
- Se la funzione "Copia il riepilogo" o il PDF leggono le celle della tabella, adegua gli indici in modo che il testo copiato resti corretto (trattenute con il segno meno).
```css
table.ced{border:1px solid var(--rule);border-top:0}
.ced thead th{font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--brand-t);padding:6px 10px;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);text-align:right}
.ced thead th:first-child{text-align:left}
.ced td,.ced th{padding:5px 10px}
.ced td:nth-child(n+2),.ced tr.gh td{text-align:right;white-space:nowrap;font-family:var(--mono);font-size:13px;font-weight:500;width:104px;border-left:1px solid var(--rule)}
.ced tbody tr:not(.gh):nth-child(even) td{background:color-mix(in srgb,var(--brand) 5%,transparent)}   /* righe alternate, come la carta a bande */
.ced tr.gh th,.ced tr.gh td{background:var(--bsoft);border-top:1px solid var(--rule)}
.ced tfoot th,.ced tfoot td{background:var(--brand);color:#fff;border-radius:0;font-family:var(--mono)}
.ced tfoot th{font-family:var(--font);text-transform:uppercase;letter-spacing:.06em;font-size:13px}
```
Togli le vecchie regole in conflitto (`.ced td:last-child{…}`, raggi del tfoot, rientri che non servono più). Sotto i 420px la larghezza delle colonne importo scende a 84px e il carattere a 12px.
`.det-head` ("Cedolino" + interruttore Busta mensile / Totale annuo) resta sopra la tabella.

## 3. Resto
- Consigli (`.tip`), barra "Dove va il lordo", bottoni, modulo a sinistra, guida, FAQ, fonti: restano come sono.
- Stampa/PDF (`@media print`): il foglio si stampa senza fori (`background:#fff`, margini 0) e la fascia `.band` non si stampa colorata.
- `@media (prefers-reduced-motion:reduce)`: nessuna animazione nuova.

## Verifica obbligatoria prima di finire
```
cd /home/claude && python3 -I build/build.py
cd /tmp/jd && node t5.js && node t6.js      # nessuna riga che comincia con ERR
python3 /tmp/shot2.py                        # nessun errore JS, overflow 0 (tollerato 1px a 320)
```
Poi guarda con Read gli screenshot `/tmp/shots/a1440.png`, `/tmp/shots/a390.png`, `/tmp/shots/a768d.png` e correggi ciò che è rotto
(testo illeggibile, fori coperti, colonne che vanno a capo, cose che escono dallo schermo).
Rispondi con: cosa hai cambiato, esito dei tre comandi, cosa non sei riuscito a fare.
