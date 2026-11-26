"""Collega lo stile Swiss (css/swiss.css), manifest e service worker (app installabile) a tutte le pagine HTML. Idempotente."""
import glob, re
MAN = '<link rel="manifest" href="/manifest.webmanifest">'
TC = '<meta name="theme-color" media="(prefers-color-scheme: light)" content="#ffffff">\n<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#111316">'
SWISS = '<link rel="stylesheet" href="/css/swiss.css?v=9">'
JS = ('<script id="pwa">if("serviceWorker"in navigator)addEventListener("load",()=>navigator.serviceWorker.register("/sw.js").catch(()=>{}));'
      'addEventListener("beforeinstallprompt",e=>{e.preventDefault();const b=document.getElementById("pwa-btn");if(!b)return;b.hidden=false;'
      'b.onclick=()=>{e.prompt();b.hidden=true}})</script>')
BTN = ' &nbsp; <button id="pwa-btn" type="button" hidden style="font:inherit;cursor:pointer">Installa l\'app</button>'
n = 0
for p in glob.glob('**/*.html', recursive=True):
    if p.startswith('.git'): continue
    s = o = open(p).read()
    if '</head>' not in s: continue
    if MAN not in s:
        s = s.replace('</head>', MAN + '\n</head>', 1)
    s = re.sub(r'<link rel="stylesheet" href="/css/swiss.css[^"]*">\n?', '', s)
    s = re.sub(r'<meta name="theme-color"[^>]*>\n?', '', s)
    s = s.replace('</head>', TC + '\n' + SWISS + '\n</head>', 1)
    s = re.sub(r'<script id="pwa">.*?</script>', '', s, flags=re.S)
    s = s.replace('</body>', JS + '</body>', 1)
    if 'id="pwa-btn"' not in s:
        s = re.sub(r'(<footer>.*?)(</div></footer>)', lambda m: m.group(1) + BTN + m.group(2), s, count=1, flags=re.S)
    if s != o: open(p, 'w').write(s); n += 1
print(n, 'pagine')
