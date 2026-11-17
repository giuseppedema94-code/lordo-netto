# Progetto grafico "Strumento" (scelto dall'utente)

Riferimento visivo: apri con Read `/tmp/prev/A-strumento.png` e il suo sorgente `/tmp/prev/A-strumento.html` (CSS compatto: copiane misure e colori).
File da modificare: `/home/claude/index.html` (CSS in `<style>`, HTML, JS). Non toccare il motore di calcolo
(tra `/* @engine-start */` e `/* @engine-end */`), gli id, i segnaposto `@@ADDIZ@@` e `@@TREE@@`. Niente git, niente pubblicazione.

Principi: neutri + inchiostro scuro, **nessun colore d'accento**; il colore compare solo dove ha un significato
(grafico a barre, pallini delle voci, avvisi, pallino del CCNL). Un solo sistema di raggi. Niente ombre. Leggero.

## Token (sostituisci i valori in `:root`)
```
--bg:#f6f7f8; --card:#fff; --ink:#16191d; --ink2:#3b4350; --muted:#667080; --line:#e4e7eb; --bd:#cfd4da; --soft:#f6f7f8;
--field:#fff; --chip:#eef1f4; --track:#e4e7eb;
--brand:#16191d; --brand-2:#16191d; --brand-t:#16191d; --brand-soft:#eef1f4; --bsoft:#eef1f4;
--c-net:#2e7d5b; --c-contr:#d9a23b; --c-tax:#c4553a;
--radius:8px; --ri:6px; --rc:4px; --shadow:none;
--font:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
```
Tema scuro (nelle due regole esistenti `:root:not([data-theme="light"])` dentro la media query e `:root[data-theme="dark"]`):
`--bg:#0f1114; --card:#171a1e; --ink:#e8eaed; --ink2:#c3c8cf; --muted:#98a1ad; --line:#272c33; --bd:#3a414b; --soft:#1c2026; --field:#111418; --chip:#22272e; --track:#272c33; --brand:#e8eaed; --brand-2:#e8eaed; --brand-t:#e8eaed; --bsoft:#22272e; --brand-soft:#22272e`
(nel tema scuro i bottoni pieni hanno fondo chiaro e testo scuro: usa `color:var(--card)` sui fondi `var(--brand)`, mai `#fff` fisso).

- **Carattere:** solo font di sistema. Elimina i `<link rel="preload">` dei font e tutte le regole `@font-face`.
  `body{font-variant-numeric:tabular-nums}`.
- **Raggi:** schede `var(--radius)`; campi, bottoni, interruttori segmentati, righe ripetute (`.fr`) `var(--ri)`; etichette/chip `var(--rc)`.
  Cerca tutti i `border-radius` nel CSS e riportali a uno di questi tre (restano 99px/50% solo per pallini, barra del grafico e levette degli switch).
- **Ombre:** togli tutti i `box-shadow` decorativi (resta l'anello di focus). Stato selezionato dei segmenti: `box-shadow:0 0 0 1px var(--line)`.

## Colore del CCNL: solo un piccolo segno
- `applyTema()` oggi imposta `--brand`, `--brand-2`, `--brand-soft`. Deve impostare **solo** `--ccnl` (il primo colore di `TEMI[...]`, default `#667080`). Non deve più cambiare `--brand*` né il meta theme-color.
- Mostra il segno in due punti: un pallino 8px `background:var(--ccnl)` prima del testo dell'etichetta "CCNL applicato", e lo stesso pallino nella riga `#out-mens` del risultato (o subito prima), seguito dal nome breve del CCNL. Nient'altro usa `--ccnl`.

## Testata e primo schermo
- `header.top`: fondo `var(--card)`, testo `var(--ink)`, `border-bottom:1px solid var(--line)`, alta 52px. Logo: testo "€ Lordo-Netto" in grassetto, senza riquadro attorno a "€". Link del menu `var(--muted)`, `var(--ink)` al passaggio. Bottone tema: bordo `var(--bd)`, testo `var(--ink2)`.
- Hero: niente fascia, niente badge, niente elenco `.perks` (rimuovi quell'HTML e il relativo CSS). Resta:
  `<h1>Calcolo stipendio netto 2026</h1>` e `<p class="lead">Dal lordo al netto con il tuo CCNL · 13 contratti · minimi al 1/11/2026</p>`
  h1 26px/700/-.02em, margine `26px 0 4px`; lead `var(--muted)` 15px, margine `0 0 20px`.

## Modulo
- Numeri di sezione (`.sec-h .n`): niente cerchio pieno, solo la cifra in `var(--muted)` grassetto.
- Campi: bordo `var(--bd)`, raggio `var(--ri)`; focus `border-color:var(--ink)` + `box-shadow:0 0 0 3px color-mix(in srgb,var(--ink) 14%,transparent)`.
- Chip "Già applicati": fondo `var(--chip)`, testo `var(--ink2)`, raggio `var(--rc)`, 12px, peso 500.
- Switch accesi, link, frecce dei `details`: `var(--ink)`. Link nel testo: `var(--ink)` sottolineati.
- Bottoni `.btn`: bordo `var(--bd)`, fondo `var(--field)`; al passaggio bordo `var(--ink)`. Bottone primario del risultato ("Scarica il PDF"): fondo `var(--ink)`, testo `var(--card)`.

## Risultato (come nell'anteprima)
- `.res-hero`: fondo `var(--card)`, testo `var(--ink)`, `border-bottom:1px solid var(--line)`, padding `18px 20px`; etichetta 12px maiuscola `var(--muted)`; valore 42px/700/-.03em; "al mese" 15px `var(--muted)`. Resta `position:sticky;top:0`.
- `.kpis`: due celle separate da `1px solid var(--line)`, numeri 18px/700.
- Barra: alta 8px, raggio 99px, 2px di spazio tra i segmenti, colori `--c-net/--c-contr/--c-tax`.
- Tabella `.ced`: solo linee orizzontali `1px solid var(--line)`; righe di gruppo in grassetto; sottovoci `var(--muted)` rientrate di 16px senza linea; importi allineati a destra;
  piede "Netto in busta": nessun fondo, `border-top:2px solid var(--ink)`, 16px/700.
- Consigli `.tip`: fondo `var(--card)`, bordo `1px solid var(--line)`, raggio `var(--ri)`, e a sinistra `border-left:3px solid var(--tc)` (il colore del tipo resta solo lì e nel titolo `b`); togli fondi pastello e il riquadro dell'icona (l'emoji resta, senza box).
- Barra mobile `.mbar`: fondo `var(--ink)`, testo `var(--card)`.

## Guida, tabelle, FAQ, fonti
Stessi token: schede bianche con bordo `var(--line)`, tabelle con sole linee orizzontali, intestazioni `var(--muted)` 12.5px, nessuna tinta colorata. `.tree` raggio `var(--ri)`.

## Verifica obbligatoria
```
cd /home/claude && python3 -I build/build.py
cd /tmp/jd && node t5.js && node t6.js       # nessuna riga ERR
python3 /tmp/shot2.py                         # nessun errore JS; overflow 0 (tollerato 1 a 320)
grep -c "font-face\|box-shadow" /home/claude/index.html   # riporta il numero
```
Guarda con Read `/tmp/shots/a1440.png`, `/tmp/shots/a390.png`, `/tmp/shots/a768d.png` e confronta con `/tmp/prev/A-strumento.png`:
stessi colori, stessi raggi ovunque (nessun angolo diverso dagli altri), niente resti di colore del vecchio tema (viola, verde di marca, pastelli).
Correggi finché coincide. Resoconto breve: cosa hai cambiato, esito dei comandi, cosa resta.
