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
 logistica:{cur:1,t:[['2025-01',(i,m)=>LOG(i,m,120)],['2026-01',(i,m)=>LOG(i,m,40)],['2027-01',(i,m)=>LOGV(i,m,30,40)],['2027-06',(i)=>[59.48,48.72,47.73,40,39.70,35.91,35.69,32.12,31.59,60.04,50,43.31,39.74,39.70,39.66,37.70,35.97][i]]]},
