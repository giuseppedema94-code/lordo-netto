"""Blocco 'Altri contratti' in fondo a ogni pagina di livello e di CCNL: link interni verso tutti i CCNL. Idempotente."""
import re, glob
hubs = []
for p in sorted(glob.glob('stipendio-netto/*/index.html')):
    slug = p.split('/')[1]
    t = re.search(r'<title>Stipendio netto (.+?) 2026', open(p).read())
    if t: hubs.append((slug, t.group(1)))
def blocco(cur):
    li = ''.join(f'<li><a href="/stipendio-netto/{s}/">{n}</a></li>' for s, n in hubs if s != cur)
    return f'<h2 id="altri-ccnl">Altri contratti</h2><ul class="lv">{li}</ul>'
import json, html as H
docs = json.load(open('data/testi-ccnl.json'))
def doc(cur):
    if cur not in docs: return ''
    u, t, f, pdf = docs[cur]
    return (f' <span class="doc-uff">Testo di riferimento: <a href="{H.escape(u)}" rel="noopener" target="_blank">{H.escape(t)}</a>'
            f' ({"PDF, " if pdf else ""}pubblicato da {H.escape(f)}).</span>')
n = 0
for p in glob.glob('stipendio-netto/*/index.html') + glob.glob('stipendio-netto/*/*/index.html'):
    s = open(p).read(); cur = p.split('/')[1]
    s = re.sub(r'<h2 id="altri-ccnl">.*?</ul>', '', s, flags=re.S)
    s = re.sub(r' <span class="doc-uff">.*?</span>', '', s)
    s = s.replace('<b>Contratto ufficiale.</b>', '<b>Contratto ufficiale.</b>' + doc(cur), 1)
    i = s.find('</main>')
    if i < 0: continue
    s = s[:i] + blocco(cur) + s[i:]
    open(p, 'w').write(s); n += 1
print(n, 'pagine,', len(hubs), 'contratti')
