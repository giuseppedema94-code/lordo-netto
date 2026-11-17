// Carica il motore di calcolo dal sorgente del calcolatore
const fs=require('fs');const s=fs.readFileSync('/home/claude/index.html','utf8');
const e=s.slice(s.indexOf('/* @engine-start */'),s.indexOf('/* @engine-end */'));
eval(e.replace(/^(const|let) (\w+)=/gm,'globalThis.$2='));
module.exports=(o,mens)=>{o={inps:.0919,tipo:'ind',addreg:1.73,addcom:.8,coniuge:false,figli:0,addMode:'cassa',mensN:mens,mens,...o};const x=calcola(o);const b=bustaOrdinaria(x,o,mens);return {x,b};};
