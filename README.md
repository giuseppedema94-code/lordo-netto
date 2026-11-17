# Sorgenti di stipendioccnl.it

- `index.html`: sorgente della homepage con motore di calcolo e dati CCNL.
- `build/`: generatori delle pagine. `sh build/all.sh` ricostruisce tutto in /home/claude/lordo-netto (clone del branch main) e fa il controllo SEO.
- `verifica/`: tabelle ufficiali e script usati per le verifiche dei CCNL.

Percorsi attesi: questo branch in /home/claude/src, main in /home/claude/lordo-netto; prima della build: `ln -s /home/claude/src/build /home/claude/build && cp /home/claude/src/index.html /home/claude/index.html`.
