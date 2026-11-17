/* @engine-start */
const P = {scaglioni:[[28000,.23],[50000,.33],[Infinity,.43]], sogliaInps1:56224, fpMax:5164.57, sanMax:3615.20};
function irpefLorda(r){let t=0,prev=0;for(const [lim,a] of P.scaglioni){if(r>prev){t+=(Math.min(r,lim)-prev)*a;}prev=lim;}return t;}
function detrLavoro(r,tipo){
  let d;
  if(r<=15000){d=1955;d=Math.max(d,tipo==="det"?690:1380);}
  else if(r<=28000)d=1910+1190*(28000-r)/13000;
  else if(r<=50000)d=1910*(50000-r)/22000;
  else d=0;
  if(r>25000&&r<=35000)d+=65;
  return d;
}
function detrConiuge(r){
  if(r<=15000)return 800-110*r/15000;
  if(r<=40000){let d=690;if(r>29000&&r<=29200)d+=10;else if(r>29200&&r<=34700)d+=20;else if(r>34700&&r<=35000)d+=30;else if(r>35000&&r<=35100)d+=20;else if(r>35100&&r<=35200)d+=10;return d;}
  if(r<=80000)return 690*(80000-r)/40000;
  return 0;
}
function detrFigli(r,n){if(!n)return 0;const k=(95000+15000*(n-1));return Math.max(0,950*n*(k-r)/k);}
function ulterioreCuneo(r){if(r<=20000||r>40000)return 0;if(r<=32000)return 1000;return 1000*(40000-r)/8000;}
function bonusCuneo(r,redLav){if(r>20000)return 0;const p=r<=8500?.071:(r<=15000?.053:.048);return redLav*p;}

/* Addizionali: dati ufficiali MEF – Dipartimento delle Finanze */
let ADD={reg:{},p2r:{},com:[]};
function progressivo(r,br){let t=0,prev=0;for(const [up,rate] of br){const lim=up==null?Infinity:up;if(r>prev)t+=(Math.min(r,lim)-prev)*rate/100;prev=lim;}return t;}
function addRegionale(r,reg,anno=2026){
  const R=(anno===2025?ADD.reg25:ADD.reg)[reg]; if(!R) return 0;
  let t=progressivo(r,R.b);
  switch(reg){
    case "Valle d'Aosta": if(r<=15000) t=0; break;
    case "Umbria": if(r<=28000) t=r*0.0123; else if(r<=50000) t=Math.max(0,t-150); break;
    case "Friuli Venezia Giulia": t=r<=15000? r*0.007 : r*0.0123; break;
    case "Lazio": if(r<=28000) t=r*0.0173; else if(r<=(anno===2025?35000:30000)) t=Math.max(0,t-60); break;
    case "Trento": if(r<=30000) t=0; break;
    case "Bolzano": { let d=r<=90000?430.5:0; if(r>50000) d+=Math.min(125,125*(r-50000)/25000); t=Math.max(0,t-d); break; }
  }
  return t;
}
function parseBr(t){return t.split(";").map(s=>{const [u,r]=s.split(":");return [u===""?null:+u,+r];});}
function parseCom(c){ // [nome,pr,esente,"up:rate;...",anno,spec,(esente2025,scaglioni2025 se diversi)]
  const br=parseBr(c[3]);
  return {nome:c[0],pr:c[1],es:c[2],br,anno:c[4],spec:c[5],es25:c.length>6?c[6]:c[2],br25:c.length>6?parseBr(c[7]):br};
}
function addComunale(r,c){ if(r<=c.es) return 0; return progressivo(r,c.br); }

function calcola(o){
  const ralBase=Math.max(0,o.ral+(o.extraBase||0)), ind=Math.max(0,o.ind||0), tram=Math.max(0,o.tram||0)*12;
  // Rimborsi spese/trasferte: se tassati entrano nel lordo; fringe benefit: oltre la soglia (1.000 / 2.000 € con figli) tassati per intero
  const rimb=Math.max(0,o.rimb||0), rimbTax=!!o.rimbTax;
  const fringe=Math.max(0,o.fringe||0), fringeSoglia=o.fringeFigli?2000:1000, fringeTax=fringe>fringeSoglia;
  // Straordinari: paga oraria (minimo/divisore orario) maggiorata; imponibili, non utili al TFR
  // paga oraria = (retribuzione mensile + indennità fisse) / divisore orario del CCNL
  // Straordinari (ora intera + maggiorazione) e maggiorazioni su orario ordinario (solo la percentuale)
  const strHr=o.strDiv>0?(ralBase/(o.mensN||13)+ind/12)/o.strDiv:0;
  let straord=0, strNFamt=0, tisAmt=0;
  for(const r of o.strRows||[]){ const a=strHr*r.ore*12*((r.s?1:0)+(r.p||0)/100); straord+=a; if(r.nf)strNFamt+=a; if(r.tis)tisAmt+=a; }
  // Bonus/MBO (tassati normalmente) e premio di risultato in denaro (contributi sì, IRPEF sostituita dall'1% fino a 5.000 €)
  const mbo=Math.max(0,o.mbo||0), pdr=Math.max(0,o.pdr||0), welf=Math.max(0,o.welf||0);
  const extraTax=(rimbTax?rimb:0)+(fringeTax?fringe:0)+straord+mbo+pdr;
  const ral=ralBase+ind+tram+extraTax;         // lordo annuo imponibile (concorso spese tranviarie: 12 mensilità)
  const baseTfr=ralBase+(o.indTfr===false?0:ind)+Math.min(mbo,o.mboTfrAmt||0)+Math.min(pdr,o.pdrTfrAmt||0); // retribuzione utile TFR
  const inpsBase=ral*o.inps;
  const inpsAgg=Math.max(0,ral-P.sogliaInps1)*0.01;
  const fsc=ral*(o.fsc||0);                    // Fondo di solidarietà del credito (quota lavoratore 0,067%)
  const fis=ral*(o.fis||0);                    // Fondo integrazione salariale (1/3 a carico del lavoratore)
  const ebt=ral*(o.ebt||0);                    // Ente bilaterale (es. commercio 0,05%)
  const inps=inpsBase+inpsAgg+fsc+fis+ebt;
  // Previdenza complementare (art. 10 e 51 c.2 lett. h TUIR): deducibile fino a 5.164,57 € tra lavoratore e datore
  const fpLav=baseTfr*(o.fpLavPct||0)/100+(o.fpLavFix||0)+(o.fpVol||0);   // in % o importo fisso annuo (es. Fondo Mario Negri)
  const fpDat=baseTfr*(o.fpDatPct||0)/100+(o.fpDatFix||0);
  const fpDed=Math.min(fpLav+fpDat,P.fpMax);
  const fpTfr=o.fpTfr?Math.max(0,baseTfr/13.5-baseTfr*0.005):0;
  // Assistenza sanitaria integrativa (art. 51 c.2 lett. a TUIR): esente fino a 3.615,20 € tra lavoratore e datore
  const sanLav=Math.max(0,(o.sanLav||0)+ral*(o.sanLavPct||0)/100), sanDat=Math.max(0,(o.sanDat||0)+ral*(o.sanDatPct||0)/100);
  const sanDed=Math.min(sanLav+sanDat,P.sanMax);
  // L. 199/2025: aumenti da rinnovi CCNL 2024-2026 pagati nel 2026 → imposta sostitutiva 5% (fuori da IRPEF e addizionali)
  // se il reddito di lavoro dipendente 2025 non supera 33.000 €
  const rinn=Math.max(0,o.rinn||0);
  const redPre=Math.max(0,ral-inps+fpDat-fpDed+sanDat-sanDed);
  const rinnOk=rinn>0&&(o.r25>0?o.r25:redPre)<=33000;
  const sost=rinnOk?rinn*0.05:0;
  // L. 199/2025 c. 8-9: premi di risultato 2026-2027 → imposta sostitutiva 1% fino a 5.000 €, se reddito di lavoro dell'anno prima ≤ 80.000 €
  const pdrOk=pdr>0&&(o.r25>0?o.r25:redPre)<=80000;
  const pdrDet=pdrOk?Math.min(pdr,5000)*(1-o.inps):0, pdrSost=pdrDet*0.01;
  // L. 199/2025 c. 10-11: straordinario notturno o festivo → imposta sostitutiva 15% sull'intero compenso, fino a 1.500 €,
  // se il reddito di lavoro 2025 non supera 40.000 € (circ. AdE 3/E 2026). Turismo e pubblici esercizi esclusi: per loro
  // c. 18-21, trattamento integrativo speciale esente pari al 15% del lordo, per le prestazioni da gennaio a settembre 2026.
  const strNF=strNFamt>0||tisAmt>0, str40=(o.r25>0?o.r25:redPre)<=40000;
  const strDet=strNFamt>0&&str40&&!o.strTur?Math.min(strNFamt,1500)*(1-o.inps):0, strSost=strDet*0.15;
  const tis=tisAmt>0&&str40&&o.strTur?tisAmt*0.15*9/12:0;
  // Rientro dei cervelli (impatriati): IRPEF e addizionali solo sulla quota imponibile; i contributi restano pieni
  const redLav=Math.max(0,redPre-(rinnOk?rinn:0)-pdrDet-strDet)*(o.impQ??1);
  const r=redLav+(o.altri||0);
  // per il taglio del cuneo le soglie contano anche la quota esente degli impatriati (L. 207/2024 c. 9, circ. AdE 4/E 2025)
  const rRif=r+(o.impQ!=null&&o.impQ<1?redLav/o.impQ*(1-o.impQ):0);
  const lorda=irpefLorda(r);
  const dLav=redLav>0?detrLavoro(r,o.tipo):0;
  const dCon=o.coniuge?detrConiuge(r):0;
  const dFig=detrFigli(r,o.figli||0);
  const dCun=redLav>0?ulterioreCuneo(rRif):0;
  let detr=dLav+dCon+dFig+dCun;
  if(r>200000)detr=Math.max(0,detr-440);
  const netta=Math.max(0,lorda-detr);
  let addReg=0, addCom=0, comSaldo=0, comAcc=0;
  if(netta>0){
    if(o.addMode==="cassa"){
      // Trattenute nel 2026: saldo regionale e comunale 2025 (al netto dell'acconto 30% già versato) + acconto comunale 2026 (30%)
      const r25=o.r25>0?o.r25:r;
      if(o.reg){
        addReg=addRegionale(r25,o.reg,2025);
        const c=o.com||{es:0,br:[[null,0]],es25:0,br25:[[null,0]]};
        comSaldo=0.7*addComunale(r25,{es:c.es25,br:c.br25});
        comAcc=0.3*addComunale(r25,c);
      } else { addReg=r25*o.addreg/100; comSaldo=0.7*r25*o.addcom/100; comAcc=0.3*r25*o.addcom/100; }
      addCom=comSaldo+comAcc;
    } else {
      if(o.reg){ addReg=addRegionale(r,o.reg); addCom=o.com?addComunale(r,o.com):r*o.addcom/100; }
      else { addReg=r*o.addreg/100; addCom=r*o.addcom/100; }
    }
  }
  const bonus=redLav>0?bonusCuneo(rRif,redLav):0;
  let ti=0;
  if(redLav>0){
    if(r<=15000){ if(lorda>dLav-75) ti=1200; }
    else if(r<=28000){ const s=dLav+dCon+dFig; if(s>lorda) ti=Math.min(1200,s-lorda); }
  }
  // quota IRPEF/addizionali attribuibili al solo reddito da lavoro (se ci sono altri redditi)
  const quota=r>0?redLav/r:1;
  const irpefLav=netta*quota, addRegL=addReg*quota, addComL=addCom*quota;
  const tratt=Math.max(0,o.tratt||0);
  const netto=ral-inps-fpLav-sanLav-irpefLav-addRegL-addComL+bonus+ti-sost-pdrSost-strSost+tis
             +(rimbTax?0:rimb)-(fringeTax?fringe:0)-tratt;   // il fringe è in natura: tassato ma non pagato in denaro
  return {mbo,pdr,pdrOk,pdrDet,pdrSost,welf,straord,strHr,strNFamt,strNF,str40,strDet,strSost,tis,fis,ebt,rinn,rinnOk,sost,rimb,rimbTax,fringe,fringeSoglia,fringeTax,tratt,tram,comSaldo,comAcc,fsc,sanLav,sanDat,sanDed,ralBase,ind,baseTfr,fpLav,fpDat,fpDed,fpTfr,ral,inps,inpsBase,inpsAgg,redLav,r,lorda,dLav,dCon,dFig,dCun,detr,netta:irpefLav,addReg:addRegL,addCom:addComL,bonus,ti,netto};
}
/* Busta di un mese ordinario (senza 13ª/14ª), come il cedolino:
   contributi sul lordo del mese, IRPEF sugli scaglioni mensili (annui/12), detrazioni in dodicesimi,
   addizionali in rate (AP 11 rate gen–nov, acconto AC 9 rate mar–nov) */
function bustaOrdinaria(x,o,mens){
  const sogliaM=Math.round(P.sogliaInps1/12);
  const rimbM=x.rimb/12, fringeM=x.fringeTax?x.fringe/12:0, trattM=x.tratt/12;
  const rmlBase=x.ralBase/mens, indM=x.ind/12, tramM=x.tram/12, strM=(x.straord||0)/12, rml=rmlBase+indM+tramM+strM+(x.rimbTax?rimbM:0)+fringeM;
  const baseTfrM=rmlBase+(o.indTfr===false?0:indM);
  const inpsM=rml*o.inps, ivsM=Math.max(0,rml-sogliaM)*0.01, fscM=rml*(o.fsc||0), fisM=rml*(o.fis||0), ebtM=rml*(o.ebt||0);
  const rinnM=x.rinnOk?(o.rinnM||0):0, sostM=rinnM*0.05;
  const fpLavM=baseTfrM*(o.fpLavPct||0)/100+((o.fpLavFix||0)+(o.fpVol||0))/12;
  const sanLavM=(o.sanLav||0)/12+rml*(o.sanLavPct||0)/100;
  const impM=Math.max(0,rml-inpsM-ivsM-fscM-fisM-ebtM-fpLavM-sanLavM-rinnM-x.strDet/12)*(o.impQ??1); // impatriati: solo la quota imponibile
  const lordaM=irpefLorda(impM*12)/12;
  const detrM=(x.dLav+x.dCun+x.dCon+x.dFig)/12;
  const nettaM=Math.max(0,lordaM-detrM);
  const aR=x.addReg/11, aS=x.comSaldo/11, aA=x.comAcc/9;
  const netM=rml-inpsM-ivsM-fscM-fisM-ebtM-fpLavM-sanLavM-nettaM-sostM-x.strSost/12+x.tis/12-aR-aS-aA+x.bonus/12+x.ti/12
            +(x.rimbTax?0:rimbM)-fringeM-trattM;
  return {strM,fisM,ebtM,rinnM,sostM,rimbM,fringeM,trattM,sogliaM,rmlBase,indM,inpsM,ivsM,fscM,fpLavM,sanLavM,impM,lordaM,detrM,nettaM,aR,aS,aA,netM};
}
/* Mensilità aggiuntiva (13ª a dicembre, 14ª a luglio) pagata insieme alla busta del mese.
   Contributi come una mensilità in più; IRPEF a tassazione separata nel mese: scaglioni mensili, senza detrazioni
   (le detrazioni sono già ripartite sui 12 mesi ordinari). Il conguaglio di fine anno riallinea il totale. */
function mensAgg(x,o,mens,b,f){
  const ext=x.ralBase/mens*(f??1), sogliaM=Math.round(P.sogliaInps1/12), rmlOrd=o.inps?b.inpsM/o.inps:0;
  const inps=ext*o.inps, ivs=Math.max(0,rmlOrd+ext-sogliaM)*0.01-Math.max(0,rmlOrd-sogliaM)*0.01;
  const fsc=ext*(o.fsc||0), fis=ext*(o.fis||0), ebt=ext*(o.ebt||0), fp=ext*(o.fpLavPct||0)/100, san=ext*(o.sanLavPct||0)/100;
  const contr=inps+ivs+fsc+fis+ebt+fp+san, imp=Math.max(0,ext-contr)*(o.impQ??1);
  const irpef=irpefLorda(imp*12)/12;
  return {ext,inps,ivs,fsc,fis,ebt,fp,san,contr,imp,irpef,net:ext-contr-irpef};
}
/* Costo annuo per l'azienda: retribuzione + contributi datore (aliquota complessiva indicativa) + INAIL + TFR
   + fondo pensione e cassa sanitaria a carico azienda con contributo di solidarietà 10% + buoni pasto */
function costoAzienda(x,o){
  const ral=x.ral, inps=ral*(o.caInps||0)/100, inail=ral*(o.caInail||0)/100, tfr=x.baseTfr/13.5;
  const fp=x.fpDat, san=x.sanDat, sol=(fp+san)*0.10, bp=(o.caBp||0)*(o.caBpG||0)*12;
  const tot=ral+(x.welf||0)+(x.rimb||0)+inps+inail+tfr+fp+san+sol+bp;
  return {ral,welf:x.welf||0,rimb:x.rimb||0,inps,inail,tfr,fp,san,sol,bp,tot};
}
function lordoDaNetto(targetMese,o,mens){
  let lo=0,hi=1e6;
  for(let i=0;i<80;i++){const m=(lo+hi)/2;const n=bustaOrdinaria(calcola({...o,ral:m,mbo:0,pdr:0,mboTfrAmt:0,pdrTfrAmt:0}),o,mens).netM;if(n<targetMese)lo=m;else hi=m;}
  return hi;
}
/* @engine-end */
