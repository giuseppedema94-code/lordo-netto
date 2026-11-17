# Ricostruisce lordo-netto/index.html dal sorgente /home/claude/index.html (indicizzabile)
import re
s=open('/home/claude/index.html').read()
d=open('/home/claude/build/addiz.json').read().replace('</','<\\/')
t=open('/home/claude/build/tree.html').read()
s=s.replace('@@ADDIZ@@',d).replace('@@TREE@@',t)

open('/home/claude/lordo-netto/index.html','w').write(s)
print('built')
