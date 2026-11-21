const fs=require('fs');
const s=fs.readFileSync('/home/claude/index.html','utf8');
const a=s.indexOf('const CCNL = {'), b=s.indexOf('\n};',a)+3;
const eng=s.split('/* @engine-start */')[1].split('/* @engine-end */')[0];
const ADD={reg:{},reg25:{},p2r:{},com:[]};
eval(eng+'\n'+s.slice(a,b).replace('const CCNL','globalThis.CCNL'));
const grab=n=>{const i=s.indexOf('const '+n+'={');const j=s.indexOf('\n};',i)+3;return s.slice(i,j).replace('const '+n,'globalThis.'+n);};
eval(grab('RINNOVI')); eval(grab('PROSSIMO'));
const R=(k,i,m)=>{const r=RINNOVI[k].r;return typeof r==='function'?r(m,i):r[i];};
const P=(k,i,m)=>PROSSIMO[k]&&PROSSIMO[k].inc?PROSSIMO[k].inc(i,m):null;
// tranche: [etichetta, funzione (i,m)->minimo, futura?]
const ABI_T=[[335.92,134.37,67.18,47.03],[291.88,116.75,58.38,40.86],[277.07,110.83,55.41,38.79],[264.07,105.63,52.81,36.97],[250,100,50,35],[215.68,86.27,43.14,30.20],[203.75,81.50,40.75,28.53],[193.32,77.33,38.66,27.06],[174.79,69.92,34.96,24.47]];
const MET=(i,m)=>R('metalmeccanici',i,m), LOG=(i,m,x)=>R('logistica',i,m)*x, LOGV=(i,m,x,y)=>i<9?LOG(i,m,x):R('logistica',i,m)/1.0625*y;
const RR=(k,x)=>(i,m)=>R(k,i,m)*x;
/* tranche di ogni rinnovo: [mese decorrenza, aumento a quella data]; cur = tranche in vigore oggi (= minimo in tabella) */
const SCH={
 commercio:{cur:4,t:[['2023-04',RR('commercio',30)],['2024-04',RR('commercio',70)],['2025-03',RR('commercio',30)],['2025-11',RR('commercio',35)],['2026-11',RR('commercio',35)],['2027-02',RR('commercio',40)]]},
 tessile:{cur:1,t:[['2024-12',RR('tessile',95)],['2026-01',RR('tessile',57)],['2027-01',RR('tessile',48)]]},
 alimentare:{cur:3,t:[['2023-12',RR('alimentare',75)],['2024-09',RR('alimentare',35)],['2025-01',RR('alimentare',60)],['2026-01',RR('alimentare',60)],['2027-01',RR('alimentare',39)],['2027-09',RR('alimentare',11)]]},
 gomma:{cur:0,t:[['2026-01',RR('gomma',60)],['2027-04',(i,m)=>P('gomma',i,m)],['2028-04',RR('gomma',60)],['2028-12',RR('gomma',15)]]},
 metalmeccanici:{cur:1,t:[['2025-06',(i,m)=>MET(i,m)*27.70/53.17],['2026-06',MET],['2027-06',(i,m)=>P('metalmeccanici',i,m)],['2028-06',(i,m)=>MET(i,m)*64.87/53.17]]},
 studi:{cur:2,t:[['2024-03',RR('studi',105)],['2024-10',RR('studi',45)],['2025-10',RR('studi',45)],['2026-12',RR('studi',20)]]},
 turismo:{cur:2,t:[['2024-07',RR('turismo',70)],['2025-06',RR('turismo',40)],['2026-05',RR('turismo',35)],['2027-04',RR('turismo',35)],['2027-11',RR('turismo',20)]]},
 pubblici:{cur:2,t:[['2024-06',RR('pubblici',50)],['2025-06',RR('pubblici',40)],['2026-06',RR('pubblici',40)],['2027-06',RR('pubblici',30)],['2027-12',RR('pubblici',40)]]},
 logistica:{cur:1,t:[['2025-01',(i,m)=>LOG(i,m,120)],['2026-01',(i,m)=>LOG(i,m,40)],['2027-01',(i)=>[46.67,36.67,36.67,30,30,26.67,26.67,23.33,23.33,50,40,33.33,30,30,30,28.33,26.67][i]],['2027-06',(i)=>[59.48,48.72,47.73,40,39.70,35.91,35.69,32.12,31.59,60.04,50,43.31,39.74,39.70,39.66,37.70,35.97][i]]]},
 gasacqua:{cur:1,t:[['2025-07',(i)=>[125.86, 113.67, 105.02, 96.36, 87.75, 82.4, 77.09, 69.69, 62.7][i]],['2026-07',(i)=>[83.91, 75.78, 70.01, 64.24, 58.5, 54.93, 51.39, 46.46, 41.8][i]],['2027-07',(i)=>[83.91, 75.78, 70.01, 64.24, 58.5, 54.93, 51.39, 46.46, 41.8][i]],['2027-10',(i)=>[69.94, 63.16, 58.36, 53.55, 48.76, 45.79, 42.84, 38.72, 34.84][i]]]},
 coopsoc:{cur:2,t:[['2024-02',(i)=>[52.63,53.16,55.79,60,61.58,63.16,63.16,66.84,71.05,71.05,76.84,84.74,96.84][i]],['2024-10',(i)=>[26.32,26.58,27.89,30,30.79,31.58,31.58,33.42,35.53,35.53,38.42,42.37,48.42][i]],['2025-10',(i)=>[26.32,26.58,27.89,30,30.79,31.58,31.58,33.42,35.53,35.53,38.42,42.37,48.42][i]]]},
 scuola:{cur:0,t:[['2026-01',()=>0],['2027-01',(i,m)=>P('scuola',i,m)]]},
 abi:{cur:3,t:[0,1,2,3].map(j=>[['2023-12','2024-09','2025-06','2026-03'][j],(i)=>ABI_T[i][j]])},
 abicompl:{cur:3,t:[0,1,2,3].map(j=>[['2023-12','2024-09','2025-06','2026-03'][j],(i)=>ABI_T[i][j]*.8])},
 dirabi:{cur:1,t:[['2025-08',()=>15000/13],['2026-01',()=>5000/13]]},
 dirterz:{cur:0,t:[['2026-01',()=>320],['2027-01',()=>260],['2028-01',()=>220]]}};
const MN=['Gen','Feb','Mar','Apr','Mag','Giu','Lug','Ago','Set','Ott','Nov','Dic'];
const TR={};
for(const [k,o] of Object.entries(SCH)){
  TR[k]=o.t.map(([d],j)=>{const [y,mo]=d.split('-').map(Number);
    const f=(i,m)=>{let v=m; if(j<o.cur){for(let h=o.cur;h>j;h--)v-=o.t[h][1](i,m);} else {for(let h=o.cur+1;h<=j;h++)v+=o.t[h][1](i,m);} return v;};
    return [MN[mo-1]+' '+y,f,d>'2026-11'?1:0];});
}
const today=new Date(2026,10,11);
const out=[];
for(const [k,c] of Object.entries(CCNL)){ if(!c.livelli||!c.livelli.length) continue;
  const IN=k==="scuola"?.0915:.0919;
  const lv=c.livelli.map(([n,m,acc,al],i)=>{acc=acc||0;const ral=m*c.mens;const o={ral,ind:acc*12,mens:c.mens,inps:IN,tipo:"ind",addreg:1.73,addcom:.8,coniuge:false,figli:0,addMode:"cassa"};
    const x=calcola(o);const bb=bustaOrdinaria(x,o,c.mens);const ag=mensAgg(x,o,c.mens,bb);
    return {t13l:ag.ext,t13n:ag.net,t13c:ag.contr,t13i:ag.irpef,i,n,min:m,acc,al:al||"",ral:ral+acc*12,netM:bb.netM,netA:x.netto,inps:x.inps,irpef:x.netta,add:x.addReg+x.addCom,bonus:x.bonus+x.ti};});
  const tr=(TR[k]||[['In vigore',(i,m)=>m]]);
  lv.forEach(l=>l.tr=tr.map(([lab,f,fut])=>{const m=Math.round(f(l.i,l.min)*100)/100,a=l.acc+(fut&&PROSSIMO[k]&&PROSSIMO[k].acc?PROSSIMO[k].acc(l.i):0),o={ral:m*c.mens,ind:a*12,mens:c.mens,inps:IN,tipo:"ind",addreg:1.73,addcom:.8,coniuge:false,figli:0,addMode:"cassa"};const x=calcola(o),bb=bustaOrdinaria(x,o,c.mens);return [m+a,bb.netM,m*c.mens+a*12,x.netto];}));
  out.push({k,nome:c.nome,mens:c.mens,fonte:c.fonte,lv,trh:tr.map(t=>[t[0],!!t[2]])});
}
fs.writeFileSync('/home/claude/build/pages.json',JSON.stringify(out));
console.log(out.map(c=>c.k+':'+c.lv.length).join(' '), out[0].lv[4]);
