#!/bin/sh
# Build completa: dati pagine, pagine CCNL, homepage, testata, sitemap/llms.txt, controllo SEO
set -e
cd /home/claude/build
node gen_pages.js
python3 gen_html.py /home/claude/lordo-netto ""
python3 build.py
python3 header.py
python3 finish.py
