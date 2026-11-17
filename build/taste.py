# Applica le regole di design-taste al calcolatore: palette, caratteri, primo schermo, cedolino, consigli
import re
p='/home/claude/index.html'; s=open(p).read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:80],s.count(a)); s=s.replace(a,b)

# --- Caratteri: IBM Plex Sans per i testi, IBM Plex Mono per gli importi
a=s.index('<link rel="preload" href="fonts/figtree'); b=s.index('</style>',a)+len('</style>')
s=s[:a]+'''<link rel="preload" href="fonts/ibm-plex-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/ibm-plex-mono-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<style>
@font-face{font-family:"Plex";font-style:normal;font-weight:400;font-display:swap;src:url(fonts/ibm-plex-sans-latin-400-normal.woff2) format("woff2")}
@font-face{font-family:"Plex";font-style:normal;font-weight:500;font-display:swap;src:url(fonts/ibm-plex-sans-latin-500-normal.woff2) format("woff2")}
@font-face{font-family:"Plex";font-style:normal;font-weight:600;font-display:swap;src:url(fonts/ibm-plex-sans-latin-600-normal.woff2) format("woff2")}
@font-face{font-family:"Plex";font-style:normal;font-weight:700;font-display:swap;src:url(fonts/ibm-plex-sans-latin-700-normal.woff2) format("woff2")}
@font-face{font-family:"Plex Mono";font-style:normal;font-weight:400;font-display:swap;src:url(fonts/ibm-plex-mono-latin-400-normal.woff2) format("woff2")}
@font-face{font-family:"Plex Mono";font-style:normal;font-weight:500;font-display:swap;src:url(fonts/ibm-plex-mono-latin-500-normal.woff2) format("woff2")}
@font-face{font-family:"Plex Mono";font-style:normal;font-weight:600;font-display:swap;src:url(fonts/ibm-plex-mono-latin-600-normal.woff2) format("woff2")}
</style>'''+s[b:]
rep('--font:Figtree,system-ui,-apple-system,"Segoe UI",sans-serif;\n  --radius:14px; --shadow:0 1px 2px rgba(20,30,25,.06),0 6px 24px rgba(20,30,25,.06);',
    '--font:Plex,system-ui,-apple-system,"Segoe UI",sans-serif; --mono:"Plex Mono",ui-monospace,"SFMono-Regular",Menlo,monospace;\n  --radius:4px; --shadow:none;')
rep('--bg:#f4f3ee; --card:#ffffff; --ink:#17211e; --muted:#5d6a65; --line:#e2dfd6; --soft:#f6f5f0;','--bg:#f3f1ec; --card:#ffffff; --ink:#1a1f1d; --muted:#5b6461; --line:#dedad1; --soft:#f7f5f1;')

# --- Testata: neutra, con una striscia sottile nel colore del CCNL
rep('header.top{background:var(--brand);color:#fff}','header.top{background:var(--card);color:var(--ink);border-top:4px solid var(--brand);border-bottom:1px solid var(--line)}')
rep('.logo{display:flex;align-items:center;gap:10px;font-weight:800;font-size:18px;letter-spacing:-.01em;color:#fff;text-decoration:none;white-space:nowrap}',
    '.logo{display:flex;align-items:baseline;gap:8px;font-weight:700;font-size:18px;letter-spacing:-.01em;color:var(--ink);text-decoration:none;white-space:nowrap}')
rep('.logo span.mark{width:30px;height:30px;border-radius:8px;background:#fff;color:var(--brand);display:grid;place-items:center;font-weight:800}',
    '.logo span.mark{font-family:var(--mono);font-weight:600;color:var(--brand-t)}')
rep('header.top nav a{color:rgba(255,255,255,.82);text-decoration:none;white-space:nowrap}\nheader.top nav a:hover{color:#fff}',
    'header.top nav a{color:var(--muted);text-decoration:none;white-space:nowrap;background:linear-gradient(currentColor,currentColor) 0 100%/0 1px no-repeat;transition:background-size .2s,color .15s}\nheader.top nav a:hover{color:var(--ink);background-size:100% 1px}')

# --- Primo schermo
rep('''.hero{padding:30px 0 8px}
.hero h1{font-size:clamp(25px,3.6vw,34px);line-height:1.15;margin:0 0 8px;letter-spacing:-.02em;text-wrap:balance}
.hero p{margin:0;color:var(--muted);max-width:68ch}
.hero .lead{font-size:18px;font-weight:600;color:var(--ink)}''','''.hero{padding:34px 0 6px;display:grid;grid-template-columns:minmax(0,1.08fr) minmax(0,1fr);gap:22px;align-items:end}
.hero h1{font-size:clamp(28px,3.8vw,40px);line-height:1.1;margin:0;letter-spacing:-.025em;font-weight:700;text-wrap:balance}
.hero p{margin:0;color:var(--ink2);max-width:52ch;font-size:15.5px}
.hero .facts{display:flex;flex-wrap:wrap;gap:4px 18px;margin-top:10px;font-size:13px;color:var(--muted)}
.hero .facts b{font-family:var(--mono);font-weight:500;color:var(--ink)}''')
a=s.index('.perks{list-style:none'); b=s.index('/* Griglia principale */')
s=s[:a]+'\n'+s[b:]

# --- Sistema: angoli squadrati, ombre via, un solo stile
rep('.card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow)}','.card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius)}')
rep('.tabs,.seg{display:inline-flex;background:var(--chip);border-radius:10px;padding:3px}','.tabs,.seg{display:inline-flex;background:var(--chip);border-radius:4px;padding:2px}')
rep('.tabs button,.seg button{border:0;background:transparent;font:inherit;font-weight:600;color:var(--muted);cursor:pointer;border-radius:8px}','.tabs button,.seg button{border:0;background:transparent;font:inherit;font-weight:600;color:var(--muted);cursor:pointer;border-radius:3px}')
rep('.tabs button[aria-selected="true"],.seg button[aria-checked="true"]{background:var(--field);color:var(--brand-t);box-shadow:0 1px 3px rgba(0,0,0,.1)}','.tabs button[aria-selected="true"],.seg button[aria-checked="true"]{background:var(--field);color:var(--ink);box-shadow:0 0 0 1px var(--line)}')
rep('.sec-h .n{flex:none;width:24px;height:24px;border-radius:50%;background:var(--brand);color:#fff;font-size:13px;font-weight:700;display:grid;place-items:center}',
    '.sec-h .n{flex:none;font-family:var(--mono);font-size:13px;font-weight:600;color:var(--brand-t)}')
rep('border:1px solid var(--bd);border-radius:9px;background:var(--field);color:var(--ink);transition:border-color .15s,box-shadow .15s}','border:1px solid var(--bd);border-radius:4px;background:var(--field);color:var(--ink);transition:border-color .15s,box-shadow .15s}')
rep('.ctl.big input{font-size:22px;font-weight:700;letter-spacing:-.01em;','.ctl.big input{font-family:var(--mono);font-size:22px;font-weight:500;letter-spacing:-.01em;')
rep('.chip{background:var(--bsoft);color:var(--brand-t);font-weight:600;font-size:12px;padding:3px 9px;border-radius:99px;white-space:nowrap}',
    '.chip{background:transparent;color:var(--ink2);border:1px solid var(--line);font-weight:500;font-size:12px;padding:2px 8px;border-radius:3px;white-space:nowrap}')
rep('.dot{display:inline-block;flex:none;width:9px;height:9px;border-radius:3px;background:var(--c-altro)}','.dot{display:inline-block;flex:none;width:9px;height:9px;border-radius:1px;background:var(--c-altro)}')
rep('.fr{border:1px solid var(--line);border-radius:12px;','.fr{border:1px solid var(--line);border-radius:4px;')
rep('.fr-x{flex:none;width:34px;height:34px;border-radius:9px;','.fr-x{flex:none;width:34px;height:34px;border-radius:4px;')
rep('.btn{font:inherit;font-weight:600;font-size:14px;border:1px solid var(--bd);background:var(--field);padding:8px 14px;border-radius:9px;cursor:pointer;color:var(--ink)}\n.btn:hover{border-color:var(--brand-2);color:var(--brand-t)}',
    '.btn{font:inherit;font-weight:600;font-size:14px;border:1px solid var(--ink);background:var(--field);padding:9px 14px;border-radius:4px;cursor:pointer;color:var(--ink);transition:transform .12s,background .15s,color .15s}\n.btn:hover{transform:translateY(-1px);background:var(--ink);color:var(--card)}\n.btn:active{transform:translateY(0)}\n.btn.fr-add{border:1px dashed var(--bd);color:var(--ink2)}\n.btn.fr-add:hover{background:var(--field);color:var(--ink);border-color:var(--ink)}')
rep('.fr-add{width:100%;border-style:dashed}','.fr-add{width:100%}')

# --- Consigli: un solo stile, niente icone e pastelli
a=s.index('.tip{--tc:#0f5c4d'); b=s.index('.tip .k{',a)
s=s[:a]+'''.tip{display:block;border-top:1px solid var(--line);padding:11px 0 2px;font-size:13.5px;line-height:1.5;color:var(--ink2)}
.tip:first-child{border-top:0;padding-top:2px}
.tip b{display:block;font-size:14.5px;color:var(--ink);margin-bottom:2px;line-height:1.35}
'''+s[b:]
rep('.tips{list-style:none;margin:0;padding:0;display:grid;gap:8px}','.tips{list-style:none;margin:0;padding:0;display:grid}')
rep('''`<li class="tip ${t.k} t-${t.c||"aumento"}"><span class="ic" aria-hidden="true">${t.i||"💡"}</span><div><b>${t.t}</b>${t.d}</div></li>`''','''`<li class="tip ${t.k}"><b>${t.t}</b>${t.d}</li>`''')

# --- Risultato come cedolino
rep('.res-hero{position:sticky;top:0;z-index:2;background:var(--brand);color:#fff;padding:20px 22px 18px}','.res-hero{position:sticky;top:0;z-index:2;background:var(--card);color:var(--ink);padding:18px 22px 16px;border-top:4px solid var(--brand);border-bottom:1px solid var(--line)}')
rep('.res-hero .lbl{font-size:12.5px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:rgba(255,255,255,.72)}','.res-hero .lbl{font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}')
rep('.res-hero .val{font-size:clamp(40px,5.2vw,52px);font-weight:800;letter-spacing:-.03em;line-height:1.05;margin:4px 0 6px;font-variant-numeric:tabular-nums}','.res-hero .val{font-family:var(--mono);font-size:clamp(38px,4.8vw,48px);font-weight:500;letter-spacing:-.04em;line-height:1.05;margin:6px 0 6px;color:var(--ink)}')
rep('.res-hero .val small{font-size:17px;font-weight:600;letter-spacing:0;color:rgba(255,255,255,.72)}','.res-hero .val small{font-family:var(--font);font-size:15px;font-weight:500;letter-spacing:0;color:var(--muted)}')
rep('.res-hero .cap{font-size:13.5px;color:rgba(255,255,255,.82)}','.res-hero .cap{font-size:13px;color:var(--muted)}')
rep('.kpis strong{font-size:19px;font-variant-numeric:tabular-nums;letter-spacing:-.01em}','.kpis strong{font-family:var(--mono);font-size:18px;font-weight:500;letter-spacing:-.02em}')
rep('.bar{display:flex;height:12px;border-radius:99px;overflow:hidden;background:var(--track)}','.bar{display:flex;height:10px;border-radius:1px;overflow:hidden;background:var(--track)}')
rep('.legend b{color:var(--ink);font-variant-numeric:tabular-nums}','.legend b{color:var(--ink);font-family:var(--mono);font-weight:500}')
rep('table.ced{width:100%;border-collapse:collapse;font-size:14px}','table.ced{width:100%;border-collapse:collapse;font-size:14px;border-top:1px solid var(--ink)}')
rep('.ced td:last-child{text-align:right;white-space:nowrap;padding-left:12px;font-variant-numeric:tabular-nums}','.ced td:last-child{text-align:right;white-space:nowrap;padding-left:12px;font-family:var(--mono);font-size:13.5px}')
rep('.ced tr.gh th,.ced tr.gh td{border-top:1px solid var(--line);padding-top:11px;padding-bottom:5px;font-weight:700;font-size:15px}','.ced tr.gh th,.ced tr.gh td{border-top:1px solid var(--line);padding-top:11px;padding-bottom:5px;font-weight:600;font-size:14.5px}')
rep('.ced tbody:first-child tr.gh th,.ced tbody:first-child tr.gh td{border-top:0;padding-top:4px}','.ced tbody:first-child tr.gh th,.ced tbody:first-child tr.gh td{border-top:0;padding-top:9px}')
rep('.ced tfoot th,.ced tfoot td{background:var(--bsoft);color:var(--brand-t);font-weight:800;font-size:17px;padding:12px 14px}\n.ced tfoot th{border-radius:10px 0 0 10px}\n.ced tfoot td{border-radius:0 10px 10px 0}',
    '.ced tfoot th,.ced tfoot td{border-top:3px double var(--ink);color:var(--ink);font-weight:700;font-size:16px;padding:11px 0 4px;text-transform:uppercase;letter-spacing:.04em}\n.ced tfoot td{font-size:18px;letter-spacing:-.01em;text-transform:none}')
rep('.fuori{margin-top:14px;border:1px solid var(--line);border-radius:10px;','.fuori{margin-top:14px;border:1px solid var(--line);border-radius:4px;')
rep('.fuori b{font-variant-numeric:tabular-nums}','.fuori b{font-family:var(--mono);font-weight:500}')
rep('.fr-val b{color:var(--ink);font-variant-numeric:tabular-nums}','.fr-val b{color:var(--ink);font-family:var(--mono);font-weight:500}')
rep('.res-hero{position:static;border-radius:var(--radius) var(--radius) 0 0}','.res-hero{position:static}')
rep('''.mbar{position:fixed;left:0;right:0;bottom:0;z-index:30;display:flex;align-items:center;gap:10px;padding:10px 18px calc(10px + env(safe-area-inset-bottom,0px));background:var(--brand);color:#fff;''',
    '''.mbar{position:fixed;left:0;right:0;bottom:0;z-index:30;display:flex;align-items:center;gap:10px;padding:10px 18px calc(10px + env(safe-area-inset-bottom,0px));background:var(--ink);color:var(--card);''')
rep('.mbar strong{font-size:21px;font-weight:800;font-variant-numeric:tabular-nums}','.mbar strong{font-family:var(--mono);font-size:20px;font-weight:500}')

# Entrata del risultato al caricamento, una volta
rep('@media (prefers-reduced-motion:reduce){*{transition:none!important}}','''.res{animation:enter .5s cubic-bezier(.2,.7,.2,1) both}
@keyframes enter{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}''')

# --- Tabelle, alberi e annuncio: stesso sistema
rep('.ad{margin:0 0 34px;border:1px dashed var(--bd);border-radius:12px;','.ad{margin:0 0 34px;border:1px dashed var(--bd);border-radius:4px;')
rep('.tbl td.n,.tbl th.n{text-align:right;font-variant-numeric:tabular-nums}','.tbl td.n,.tbl th.n{text-align:right;font-family:var(--mono);font-size:13.5px}')
rep('.tree{background:var(--field);border:1px solid var(--line);border-radius:12px;','.tree{background:var(--field);border:1px solid var(--line);border-radius:4px;')

# --- Colori dei CCNL senza viola, lavanda o magenta
rep('const TEMI={commercio:["#3730a3","#4f46e5","#ecebfc"],dirterz:["#312e81","#4338ca","#e9e8fb"],tessile:["#5b2a86","#7a3db8","#f1e9f8"],',
    'const TEMI={commercio:["#9a3412","#c2410c","#fbeee6"],dirterz:["#7c2d12","#9a3412","#f8ebe4"],tessile:["#7f1d1d","#a63232","#f8e9e9"],')
rep('pubblici:["#701a55","#9d2a78","#f6e8f1"],','pubblici:["#854d0e","#a16207","#fbf1df"],')

# --- Primo schermo: testo
a=s.index('  <section class="hero">'); b=s.index('  </section>',a)+len('  </section>')
s=s[:a]+'''  <section class="hero">
    <h1>Stipendio netto 2026 per CCNL e livello</h1>
    <div>
      <p>Scegli contratto e livello: il calcolatore parte dal minimo del CCNL e ti dà la busta paga del mese, voce per voce, con IRPEF, contributi, addizionali del tuo comune e taglio del cuneo.</p>
      <p class="facts"><span><b>13</b> contratti nazionali</span><span>minimi in vigore al <b>1/11/2026</b></span><span>regole fiscali <b>L. 199/2025</b></span></p>
    </div>
  </section>'''+s[b:]

# --- Bottoni: verbo e oggetto
rep('<button class="btn" id="sharePdf" type="button">Salva PDF</button>','<button class="btn" id="sharePdf" type="button">Scarica il PDF</button>')
rep('<button class="btn" id="copy" type="button">Copia testo</button>','<button class="btn" id="copy" type="button">Copia il riepilogo</button>')
rep('<div class="det-head"><h3>Consigli</h3></div>','<div class="det-head"><h3>Come pagare meno tasse</h3></div>')
open(p,'w').write(s)
print('ok')
