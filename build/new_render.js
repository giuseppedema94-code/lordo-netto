let last=null;
const closed=new Set();           // gruppi del cedolino chiusi dall'utente
const esc=t=>String(t).replace(/&/g,"&amp;").replace(/</g,"&lt;");
const mns=v=>"− "+eur(Math.abs(v),2), pls=v=>"+ "+eur(Math.abs(v),2);
const ded=(l,v)=>v>0.004?[l,mns(v),""]:null;      // trattenuta
const cre=(l,v)=>v>0.004?[l,pls(v),""]:null;      // somma a favore
const inf=(l,v)=>[l,eur(v,2),"info"];             // riga informativa, non entra nei totali
function cedHtml(groups,netLbl,netVal){
  let h="";
  for(const g of groups){
    let rows=g.rows.filter(Boolean);
    if(!rows.length&&!g.always) continue;
    if(g.single&&rows.length===1) rows=[];
    const shut=closed.has(g.id)&&rows.length;
    h+=`<tbody class="grp${shut?" closed":""}" data-g="${g.id}"><tr class="gh"><th scope="rowgroup">`
      +(rows.length?`<button type="button" aria-expanded="${!shut}"><i class="dot ${g.id}"></i>${g.title}</button>`:`<span style="display:inline-flex;align-items:center;gap:10px"><i class="dot ${g.id}"></i>${g.title}</span>`)
      +`</th><td>${g.total}</td></tr>`;
    for(const r of rows) h+=`<tr class="${r[2]}"><td${r[2]==="warn"?' colspan="2"':""}>${r[0]}</td>${r[2]==="warn"?"":`<td>${r[1]}</td>`}</tr>`;
    h+=`</tbody>`;
  }
  return h+`<tfoot><tr class="net"><th scope="row">${netLbl}</th><td>${netVal}</td></tr></tfoot>`;
}
/* Riga di sintesi accanto a ogni sezione facoltativa */
function summaries(x,o){
  const put=(id,t,on)=>{const el=$(id); el.textContent=t; el.classList.toggle("on",!!on);};
  const k=$("ccnl").value;
  const c=[`INPS ${pct(o.inps*100)}`]; if(o.fis)c.push(`FIS ${pct(o.fis*100)}`); if(o.fsc)c.push("Fondo solidarietà"); if(o.ebt)c.push("Ente bilaterale");
  put("s-contr",c.join(" · "),c.length>1||o.inps!==0.0919);
  const auto=[];
  if(o.fsc)auto.push("Fondo di solidarietà del credito 0,067%"); if(o.ebt)auto.push("Ente bilaterale 0,05%");
  let at=auto.length?`Questo CCNL aggiunge in automatico: ${auto.join(", ")}.`:"";
  if(["tessile","alimentare","gomma","metalmeccanici"].includes(k)) at+=(at?" ":"")+"Industria con più di 15 dipendenti: scegli l'aliquota 9,49%.";
  $("contr-auto").textContent=at; $("contr-auto").hidden=!at;
  const fp=x.fpLav||x.fpDat;
  put("s-fp",fp?`${eur(x.fpLav)} tu + ${eur(x.fpDat)} azienda l'anno`:(o.fpTfr?"Solo TFR":"Nessun versamento"),fp);
  const sa=x.sanLav||x.sanDat;
  put("s-san",sa?`${eur(x.sanLav)} tu + ${eur(x.sanDat)} azienda l'anno`:"Nessuna",sa);
  const fam=[]; if(o.coniuge)fam.push("Coniuge"); if(o.figli)fam.push(o.figli===1?"1 figlio":`${o.figli} figli`);
  put("s-fam",fam.length?fam.join(" + "):"Nessuno",fam.length);
  put("s-add",selCom?`${selCom.reg} · ${selCom.nome}`:`Valori medi ${pct(o.addreg)} + ${pct(o.addcom)}`,selCom||o.r25);
  const al=[]; if(x.rimb)al.push(`Rimborsi ${eur(x.rimb/12)}`); if(x.tratt)al.push(`Trattenute ${eur(x.tratt/12)}`); if(x.fringe)al.push(`Benefit ${eur(x.fringe)}`);
  put("s-altro",al.length?al.join(" · "):"Nessuna voce",al.length);
}
function ccnlInfo(o){
  const c=CCNL[$("ccnl").value];
  if(!c.livelli.length){ $("ccnl-info").textContent="Senza tabella del contratto: scrivi la tua retribuzione e scegli le mensilità."; return; }
  const pr=c.preset||{}, chips=[];
  if(pr.fondo)chips.push(pr.fondo); if(pr.sanita)chips.push(pr.sanita);
  if(o.fis)chips.push(`FIS ${pct(o.fis*100)}`); if(o.ebt)chips.push("Ente bilaterale 0,05%"); if(o.fsc)chips.push("Fondo di solidarietà 0,067%");
  $("ccnl-info").innerHTML=`${esc(c.fonte)}.`+(chips.length?`<div class="chips"><span style="align-self:center">Già applicati:</span>${chips.map(t=>`<span class="chip">${esc(t)}</span>`).join("")}</div>`:"");
}
function render(){
  const o=opts(), mens=+$("mens").value||12;
  let ral;
  if(mode==="ln"){
    if(!ralTouched){const r=ralDaCcnl(); if(r!==null)setv("ral",unit==="m"?Math.round(r/mens*100)/100:r);}
    ral=(numv("ral")||0)*(unit==="m"?mens:1);
    const daCcnl=CCNL[$("ccnl").value].livelli.length&&!ralTouched;
    $("ral-hint").textContent=unit==="m"
      ?`× ${mens} mensilità = RAL ${eur(ral)}. Superminimo e scatti inclusi.`
      :(daCcnl?"È il minimo del CCNL: sostituiscilo con la tua RAL, superminimo e scatti inclusi.":`Pari a ${eur(ral/mens,2)} lordi per ${mens} mensilità.`);
  } else {
    ral=lordoDaNetto(numv("nettoTarget")||0,o,mens);
  }
  const x=calcola({...o,ral});
  const b=bustaOrdinaria(x,o,mens); last={x,mens,b};

  /* 1. Il numero che conta */
  if(mode==="ln"){
    $("out-lbl").textContent="Netto in busta";
    $("out-main").innerHTML=eur(b.netM)+" <small>al mese</small>";
    $("out-mens").textContent=`Busta ordinaria · ${mens} mensilità`;
    $("sub2-lbl").textContent="Lordo annuo"; $("out-ral").textContent=eur(x.ral);
    $("mbar-l").textContent="Netto in busta"; $("mbar-v").textContent=eur(b.netM);
  } else {
    $("out-lbl").textContent="RAL necessaria";
    $("out-main").innerHTML=eur(x.ralBase)+" <small>l'anno</small>";
    $("out-mens").textContent=`Per ${eur(b.netM)} netti in busta · ${mens} mensilità`;
    $("sub2-lbl").textContent="Lordo mensile (RML)"; $("out-ral").textContent=eur(x.ralBase/mens,2);
    $("mbar-l").textContent="RAL necessaria"; $("mbar-v").textContent=eur(x.ralBase);
  }
  $("out-na").textContent=eur(x.netto);

  /* 2. Ripartizione del lordo annuo: netto, contributi, imposte */
  const L=x.ral||1, sContr=x.inps+x.fpLav+x.sanLav, sTax=Math.max(0,x.netta+x.addReg+x.addCom+x.sost-x.bonus-x.ti), sNet=Math.max(0,L-sContr-sTax);
  const seg=[["net","Netto",sNet],["contr","Contributi e fondi",sContr],["tax","Imposte",sTax]];
  $("bar").innerHTML=seg.map(([k,,v])=>`<i style="width:${v/L*100}%;background:var(--c-${k})"></i>`).join("");
  $("legend").innerHTML=seg.map(([k,l,v])=>`<li><i class="dot ${k}"></i>${l} <b>${Math.round(v/L*100)}%</b></li>`).join("");

  /* 3. Cedolino a gruppi, mensile (busta ordinaria) o annuo */
  const M=detMode==="m";
  const rifR=o.r25>0?o.r25:x.r;
  if(selCom){
    const eff=v=>rifR>0?Math.round(v/rifR*10000)/100:0;
    setv("addreg",eff(x.addReg)); setv("addcom",eff(x.addCom));
    $("addreg-hint").textContent=`Media effettiva, ${selCom.reg}`;
    $("addcom-hint").textContent=`Media effettiva, ${selCom.nome}`;
  }
  const regLbl=selCom?selCom.reg:`media ${pct(o.addreg)}`, comLbl=selCom?selCom.nome:`media ${pct(o.addcom)}`;
  const v=M?{
    base:b.rmlBase, ind:b.indM, tram:x.tram/12, rimbT:x.rimbTax?b.rimbM:0, rimbE:x.rimbTax?0:b.rimbM, fringe:b.fringeM,
    inps:b.inpsM, ivs:b.ivsM, fsc:b.fscM, fis:b.fisM, ebt:b.ebtM, fp:b.fpLavM, san:b.sanLavM,
    imp:b.impM, lorda:b.lordaM, irpef:b.nettaM, sost:b.sostM, aR:b.aR, aS:b.aS, aA:b.aA, bonus:x.bonus/12, ti:x.ti/12, tratt:b.trattM, net:b.netM
  }:{
    base:x.ralBase, ind:x.ind, tram:x.tram, rimbT:x.rimbTax?x.rimb:0, rimbE:x.rimbTax?0:x.rimb, fringe:x.fringeTax?x.fringe:0,
    inps:x.inpsBase, ivs:x.inpsAgg, fsc:x.fsc, fis:x.fis, ebt:x.ebt, fp:x.fpLav, san:x.sanLav,
    imp:x.redLav, lorda:x.lorda*(x.r?x.redLav/x.r:1), irpef:x.netta, sost:x.sost, aR:x.addReg, aS:x.comSaldo, aA:x.comAcc, bonus:x.bonus, ti:x.ti, tratt:x.tratt, net:x.netto
  };
  const tLordo=v.base+v.ind+v.tram+v.rimbT+v.fringe;
  const tContr=v.inps+v.ivs+v.fsc+v.fis+v.ebt+v.fp+v.san;
  const tTax=v.irpef+v.sost+v.aR+v.aS+v.aA-v.bonus-v.ti;
  const tAltro=v.rimbE-v.fringe-v.tratt;
  const pos=(l,val)=>val>0.004?[l,eur(val,2),""]:null;
  const detr=M?[b.detrM?inf("Detrazioni del mese",b.detrM):null]
              :[x.dLav?inf("Detrazione lavoro dipendente",x.dLav):null,x.dCun?inf("Detrazione aggiuntiva cuneo fiscale",x.dCun):null,
                x.dCon?inf("Detrazione coniuge a carico",x.dCon):null,x.dFig?inf("Detrazione figli a carico",x.dFig):null];
  const groups=[
    {id:"comp",title:"Retribuzione lorda",total:eur(tLordo,2),always:true,single:true,rows:[
      [M?"Retribuzione mensile (RML)":"Retribuzione annua (RAL)",eur(v.base,2),""],
      pos(`Indennità fisse${o.indTfr===false?", non utili al TFR":""}`,v.ind),
      pos(`Concorso spese tranviarie, ${esc(o.tramCity)}`,v.tram),
      pos("Rimborsi spese tassati",v.rimbT),
      pos("Fringe benefit oltre soglia, in natura",v.fringe)]},
    {id:"contr",title:"Contributi e fondi",total:mns(tContr),always:true,rows:[
      ded(`INPS ${pct(o.inps*100)}`,v.inps),
      ded(M?`IVS aggiuntivo 1% oltre ${eur(b.sogliaM)} al mese`:"IVS aggiuntivo 1% oltre 56.224 € l'anno",v.ivs),
      ded("Fondo di solidarietà del credito 0,067%",v.fsc),
      ded(`Fondo integrazione salariale ${pct((o.fis||0)*100)}`,v.fis),
      ded("Ente bilaterale 0,05%",v.ebt),
      ded("Fondo pensione, tuo contributo",v.fp),
      x.fpLav+x.fpDat>P.fpMax?["Fondo pensione oltre 5.164,57 € l'anno: la parte in più è tassata.","","warn"]:null,
      ded("Assistenza sanitaria, tua trattenuta",v.san),
      x.sanLav+x.sanDat>P.sanMax?["Assistenza sanitaria oltre 3.615,20 € l'anno: la parte in più è tassata.","","warn"]:null]},
    {id:"tax",title:"Imposte",total:tTax>=0?mns(tTax):pls(tTax),always:true,rows:[
      inf(M?"Imponibile IRPEF del mese":"Imponibile IRPEF",v.imp),
      inf(M?"IRPEF lorda, scaglioni mensili":"IRPEF lorda",v.lorda),
      ...detr,
      ["IRPEF netta",mns(v.irpef),""],
      ded("Imposta sostitutiva 5% sugli aumenti da rinnovo",v.sost),
      ded(`Addizionale regionale 2025, ${esc(regLbl)}${M?" · rata 1 di 11":""}`,v.aR),
      ded(`Addizionale comunale 2025 a saldo, ${esc(comLbl)}${M?" · rata 1 di 11":""}`,v.aS),
      ded(`Addizionale comunale 2026 in acconto${M?" · rata 1 di 9":""}`,v.aA),
      cre("Bonus cuneo fiscale",v.bonus),
      cre("Trattamento integrativo",v.ti)]},
    {id:"altro",title:"Altre voci",total:tAltro>=0?pls(tAltro):mns(tAltro),rows:[
      cre("Rimborsi spese esenti",v.rimbE),
      ded("Fringe benefit in natura, non pagati in denaro",v.fringe),
      ded("Altre trattenute",v.tratt)]}
  ];
  $("det").innerHTML=cedHtml(groups,M?"Netto in busta":"Netto annuo",eur(v.net,2));
  $("det-note").textContent=M
    ?`Busta di un mese ordinario, senza ${mens>13?"tredicesima e quattordicesima":"tredicesima"}. Le addizionali si pagano a rate: 11 da gennaio a novembre, 9 da marzo a novembre per l'acconto.`
    :"Totale dell'anno: mensilità aggiuntive e conguaglio di dicembre compresi.";
  const fpTot=x.fpLav+x.fpDat+x.fpTfr, fu=$("fuori");
  fu.hidden=!(fpTot>0);
  if(fpTot>0){
    const parts=[x.fpLav&&`tu ${eur(x.fpLav)}`,x.fpDat&&`azienda ${eur(x.fpDat)}`,x.fpTfr&&`TFR ${eur(x.fpTfr)}`].filter(Boolean).join(" · ");
    fu.innerHTML=`Fuori busta, al fondo pensione: <b>${eur(fpTot)}</b> l'anno<small>${parts}</small>`;
  }

  /* 4. Sintesi delle sezioni e contatore fringe benefit */
  summaries(x,o); ccnlInfo(o);
  const fm=$("fringe-meter"), fv=x.fringe, fs=x.fringeSoglia;
  fm.hidden=!fv; fm.classList.toggle("over",x.fringeTax);
  $("fm-fill").style.width=Math.min(100,fv/fs*100)+"%";
  $("fm-txt").textContent=x.fringeTax?`Soglia di ${eur(fs)} superata: sono tassati tutti i ${eur(fv)}, non solo la parte in più.`:`Usati ${eur(fv)} su ${eur(fs)}: esenti, restano ${eur(fs-fv)}.`;
}
