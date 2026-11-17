# Demo della nuova testata: legge il sito costruito e scrive lordo-netto/demo/index.html (noindex)
import re, os, json, html as H
ROOT = '/home/claude/lordo-netto'
s = open(f'{ROOT}/index.html', encoding='utf-8').read()

# indice di ricerca dalle pagine per CCNL e livello
idx = []
base = f'{ROOT}/stipendio-netto'
for d in sorted(os.listdir(base)):
    p = f'{base}/{d}'
    if not os.path.isdir(p): continue
    t = open(f'{p}/index.html', encoding='utf-8').read()
    h1 = re.search(r'<h1>(.*?)</h1>', t).group(1)
    nome = H.unescape(re.sub(r'^Stipendio netto | 2026.*$', '', h1))
    idx.append([nome, f'/stipendio-netto/{d}/', 1])
    order=[]
    for m in re.findall(r'stipendio-netto/'+re.escape(d)+r'/([a-z0-9-]+)/', t):
        if m not in order: order.append(m)
    for l in order+[x for x in sorted(os.listdir(p)) if x not in order]:
        q = f'{p}/{l}/index.html'
        if os.path.isfile(q):
            h = H.unescape(re.search(r'<h1>(.*?)</h1>', open(q, encoding='utf-8').read()).group(1))
            idx.append([re.sub(r' livello (?=[A-Z][a-z])', ' ', re.sub(r'^Stipendio netto | 2026$', '', h)), f'/stipendio-netto/{d}/{l}/', 0])

logo = re.search(r'<svg class="logo-i".*?</svg>', s, re.S).group(0).replace('width="26" height="26"', 'width="44" height="44"')
ic = {'calc': '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 11h2M12 11h2M8 15h2M12 15h2M16 11v6"/>',
      'list': '<path d="M8 6h12M8 12h12M8 18h12M4 6h.01M4 12h.01M4 18h.01"/>',
      'bld': '<path d="M4 21V5l8-2v18M12 9l8 2v10M8 9v.01M8 13v.01M8 17v.01M16 14v.01M16 18v.01M2 21h20"/>',
      'swap': '<path d="M7 4v14M3 14l4 4 4-4M17 20V6M13 10l4-4 4 4"/>',
      'cal': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4M16 3v4M3 10h18"/>'}
I = lambda k: f'<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ic[k]}</svg>'
chips = [('Commercio', 'commercio-terziario'), ('Metalmeccanici', 'metalmeccanici'), ('Turismo', 'turismo-alberghi'),
         ('Pubblici esercizi', 'pubblici-esercizi'), ('Cooperative sociali', 'cooperative-sociali'), ('Scuola statale', 'scuola-statale')]
ok = {d for d in os.listdir(base)}
chips = [(n, sl) for n, sl in chips if sl in ok]

header = f'''<header class="nt" id="top-nt">
  <div class="nt-row">
    <a class="nt-brand" href="/demo/" aria-label="stipendioccnl">{logo}<span><b>stipendio<i>ccnl</i></b><small>Lo stipendio netto con il tuo contratto</small></span></a>
    <nav class="nt-tabs" aria-label="Sezioni">
      <a class="nt-tab on" href="/demo/" aria-current="page">{I('calc')}<span>Calcolatore</span></a>
      <a class="nt-tab" href="/stipendio-netto/">{I('list')}<span>Stipendi per CCNL</span></a>
      <a class="nt-tab" href="#costo" data-go="costo">{I('bld')}<span>Costo azienda</span></a>
      <a class="nt-tab" href="#netto-lordo" data-go="nl">{I('swap')}<span>Netto → lordo</span></a>
      <span class="nt-tab off" title="In arrivo">{I('cal')}<span>Rinnovi</span><em>presto</em></span>
    </nav>
    <button class="theme-btn" id="theme-toggle" type="button" aria-label="Cambia tema: dispositivo, chiaro o scuro">Tema: auto</button>
  </div>
  <div class="nt-band"><div class="nt-in">
    <div class="nt-search" role="search"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>
      <input id="nt-q" type="search" autocomplete="off" aria-label="Cerca contratto o livello" placeholder="Cerca contratto o livello, es. commercio IV o docente primaria">
      <ul id="nt-res" role="listbox" hidden></ul></div>
  </div></div>
  <nav class="nt-chips" aria-label="Contratti più cercati"><div class="nt-in">{''.join(f'<a href="/stipendio-netto/{sl}/">{n}</a>' for n, sl in chips)}<a class="all" href="/stipendio-netto/">Tutti i CCNL</a></div></nav>
</header>'''

css = '''<style>
.nt{background:var(--card);border-bottom:1px solid var(--line)}
.nt-row{max-width:1240px;margin:0 auto;padding:14px 24px 0;display:flex;align-items:flex-end;gap:28px;position:relative}
.nt-brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--ink);padding-bottom:12px;flex:none}
.nt-brand svg{flex:none}
.nt-brand b{display:block;font-size:26px;letter-spacing:-.02em;line-height:1}.nt-brand b i{font-style:normal;font-weight:500;color:var(--muted)}
.nt-brand small{display:block;font-size:12.5px;color:var(--muted);margin-top:4px;font-weight:500}
.nt-tabs{display:flex;gap:4px;flex:1;min-width:0;margin-right:52px}
.nt-tab{display:flex;align-items:center;gap:8px;padding:12px 15px;border-radius:8px 8px 0 0;background:#16191d;color:#fff;text-decoration:none;font-weight:600;font-size:14.5px;white-space:nowrap}
:root[data-theme="dark"] .nt-tab{background:#2a2f36}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .nt-tab{background:#2a2f36}}
.nt-tab:hover{background:#2f353d}.nt-tab.on{background:#2f8a5f}.nt-tab.off{opacity:.55;cursor:default}
.nt-tab em{font-style:normal;font-size:11px;font-weight:600;background:rgba(255,255,255,.18);padding:1px 6px;border-radius:4px}
.nt .theme-btn{position:absolute;right:24px;top:14px;width:36px;height:36px;padding:0;font-size:0;border-radius:50%;display:flex;align-items:center;justify-content:center}
.nt .theme-btn::before{content:"";width:16px;height:16px;border-radius:50%;border:2px solid currentColor;background:linear-gradient(90deg,currentColor 50%,transparent 50%)}
@media (max-width:1180px){.nt-tab{padding:11px 12px;font-size:14px}.nt-brand small{display:none}.nt-tabs{overflow-x:auto;scrollbar-width:none}.nt-tabs::-webkit-scrollbar{display:none}}
.nt-band{background:#2f8a5f}.nt-in{max-width:1240px;margin:0 auto;padding:12px 24px}
.nt-search{position:relative;display:flex;align-items:center;gap:10px;background:#fff;color:#16191d;border-radius:999px;padding:0 18px;height:46px}
.nt-search input{flex:1;min-width:0;border:0;font:inherit;font-size:15.5px;outline:none;background:transparent;color:#16191d}
.nt-search input::placeholder{color:#7b8491}
#nt-res{position:absolute;left:0;right:0;top:52px;margin:0;padding:6px;list-style:none;background:var(--card);border:1px solid var(--line);border-radius:10px;z-index:40;max-height:340px;overflow:auto}
#nt-res a{display:block;padding:9px 12px;border-radius:6px;color:var(--ink);text-decoration:none;font-size:14.5px}
#nt-res a.sel,#nt-res a:hover{background:var(--soft)}#nt-res a small{color:var(--muted);margin-left:6px}
#nt-res li.none{padding:9px 12px;color:var(--muted);font-size:14px}
.nt-chips .nt-in{padding:8px 24px;display:flex;gap:4px;justify-content:center;flex-wrap:wrap}
.nt-chips a{padding:7px 12px;border-radius:6px;color:var(--ink);text-decoration:none;font-size:14px}.nt-chips a:hover{background:var(--soft)}
.nt-chips a.all{color:#2f8a5f;font-weight:600}
.demo-bar{background:#fff7d6;color:#5c4a00;font-size:13px;text-align:center;padding:6px 12px}
:root[data-theme="dark"] .demo-bar{background:#3a3200;color:#f1e3a1}
@media (max-width:700px){
 .nt-row{flex-direction:column;align-items:stretch;gap:12px;padding:12px 16px 0;position:relative}
 .nt-brand{padding-bottom:0}.nt-brand small{display:none}.nt-brand b{font-size:22px}
 .nt .theme-btn{position:absolute;right:16px;top:20px;margin:0}
 .nt-tabs{margin-right:-16px}
 .nt-tabs{overflow-x:auto;scrollbar-width:none;margin:0 -16px;padding:0 16px}.nt-tabs::-webkit-scrollbar{display:none}.nt-tab{padding:10px 13px;font-size:14px}
 .nt-in{padding:10px 16px}.nt-search{height:44px}.nt-search input{font-size:15px}
 .nt-chips .nt-in{flex-wrap:nowrap;overflow-x:auto;justify-content:flex-start;padding:6px 10px;scrollbar-width:none}.nt-chips a{white-space:nowrap}
}
</style>'''

js = '''<script>
(()=>{const IDX=%s, q=document.getElementById("nt-q"), ul=document.getElementById("nt-res");
 const N=t=>t.toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g,"").replace(/[^a-z0-9 ]/g," ");
 const R={i:1,ii:2,iii:3,iv:4,v:5,vi:6,vii:7,viii:8,ix:9};
 const toks=t=>N(t).split(/\\s+/).filter(Boolean);
 const D=IDX.map(([l,u,c])=>({l,u,c,t:N(l)+" "+N(l).replace(/\\b(i|ii|iii|iv|v|vi|vii|viii|ix)\\b/g,m=>R[m])}));
 let sel=0,cur=[]; if(innerWidth<700) q.placeholder="Cerca contratto o livello";
 const esc=t=>t.replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));
 function show(){const w=toks(q.value); if(!w.length){ul.hidden=true;return;}
  cur=D.filter(d=>{const ws=d.t.split(/\\s+/); return w.every(x=>ws.some(y=>y.startsWith(x)));}).sort((a,b)=>b.c-a.c).slice(0,8); sel=0;
  ul.innerHTML=cur.length?cur.map((d,i)=>`<li><a href="${d.u}" class="${i?"":"sel"}">${esc(d.l)}${d.c?"<small>tutti i livelli</small>":""}</a></li>`).join(""):'<li class="none">Nessun contratto trovato. Prova con il nome del settore.</li>';
  ul.hidden=false;}
 q.addEventListener("input",show);
 q.addEventListener("keydown",e=>{ if(ul.hidden) return; const a=[...ul.querySelectorAll("a")];
  if(e.key==="ArrowDown"||e.key==="ArrowUp"){e.preventDefault(); if(!a.length)return; sel=(sel+(e.key==="ArrowDown"?1:a.length-1))%%a.length; a.forEach((x,i)=>x.classList.toggle("sel",i===sel)); a[sel].scrollIntoView({block:"nearest"});}
  else if(e.key==="Enter"&&a[sel]){e.preventDefault(); location.href=a[sel].href;}
  else if(e.key==="Escape"){ul.hidden=true;} });
 document.addEventListener("click",e=>{ if(!e.target.closest(".nt-search")) ul.hidden=true; });
 document.querySelectorAll("[data-go]").forEach(a=>a.addEventListener("click",e=>{e.preventDefault();
  if(a.dataset.go==="nl"){ if(typeof setMode==="function") setMode("nl"); document.getElementById("f")?.scrollIntoView({behavior:"smooth"}); }
  else { const g=[...document.querySelectorAll(".eyebrow")].find(p=>/Costo per l'azienda/.test(p.textContent)); const d=g&&g.nextElementSibling; if(d&&d.tagName==="DETAILS") d.open=true; (g||document.getElementById("costo-box"))?.scrollIntoView({behavior:"smooth",block:"start"}); }
 }));
})();
</script>''' % json.dumps(idx, ensure_ascii=False)

s = re.sub(r'<header class="top">.*?</header>', '<div class="demo-bar">Anteprima della nuova testata: il sito pubblico non è cambiato.</div>\n' + header, s, count=1, flags=re.S)
s = s.replace('</head>', css + '\n</head>', 1)
s = s.replace('</body>', js + '\n</body>', 1)
# percorsi relativi -> assoluti
for p in ('stipendio-netto/', 'note-legali/', 'privacy/', 'favicon.svg', 'favicon-32.png', 'apple-touch-icon.png'):
    s = s.replace(f'href="{p}', f'href="/{p}')
s = s.replace('fetch("data/', 'fetch("/data/')
s = re.sub(r'<meta name="robots"[^>]*>', '<meta name="robots" content="noindex, nofollow">', s, count=1)
os.makedirs(f'{ROOT}/demo', exist_ok=True)
open(f'{ROOT}/demo/index.html', 'w', encoding='utf-8').write(s)
print('demo', len(idx), 'voci di ricerca')
