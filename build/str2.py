p='/home/claude/index.html'; s=open(p).read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:70],s.count(a)); s=s.replace(a,b)
# --- HTML
a=s.index('            <summary><span class="t">Straordinari</span>'); b=s.index('          </details>',a)
s=s[:a]+'''            <summary><span class="t">Straordinari e maggiorazioni</span><span class="v" id="s-str"></span></summary>
            <div class="fields">
              <div class="f full">
                <p class="hint" style="margin-top:0"><b>Straordinario</b>: ore oltre il tuo orario, pagate per intero più la maggiorazione. <b>Maggiorazione</b>: notte o festivo dentro l'orario normale, già pagato nello stipendio: si aggiunge solo la percentuale.</p>
                <label class="sw" id="str-turni-box" hidden><input type="checkbox" id="strTurni"><span class="tr" aria-hidden="true"></span><span>Lavoro a turni</span></label>
                <div id="str-list" class="fr-list"></div>
                <button type="button" class="btn fr-add" id="str-add">+ Aggiungi straordinario o maggiorazione</button>
                <p class="hint" id="str-h"></p>
              </div>
            </div>
'''+s[b:]
# --- engine
rep('''  const straord=o.strOre>0&&o.strDiv>0?(ralBase/(o.mensN||13)+ind/12)/o.strDiv*(1+(o.strMagg||0)/100)*o.strOre*12:0;''',
'''  // Straordinari (ora intera + maggiorazione) e maggiorazioni su orario ordinario (solo la percentuale)
  const strHr=o.strDiv>0?(ralBase/(o.mensN||13)+ind/12)/o.strDiv:0;
  let straord=0, strNFamt=0, tisAmt=0;
  for(const r of o.strRows||[]){ const a=strHr*r.ore*12*((r.s?1:0)+(r.p||0)/100); straord+=a; if(r.nf)strNFamt+=a; if(r.tis)tisAmt+=a; }''')
rep('''  const strNF=straord>0&&(o.strTipo==="n"||o.strTipo==="f"), str40=(o.r25>0?o.r25:redPre)<=40000;
  const strDet=strNF&&str40&&!o.strTur?Math.min(straord,1500)*(1-o.inps):0, strSost=strDet*0.15;
  const tis=strNF&&str40&&o.strTur?straord*0.15*9/12:0;''','''  const strNF=strNFamt>0||tisAmt>0, str40=(o.r25>0?o.r25:redPre)<=40000;
  const strDet=strNFamt>0&&str40&&!o.strTur?Math.min(strNFamt,1500)*(1-o.inps):0, strSost=strDet*0.15;
  const tis=tisAmt>0&&str40&&o.strTur?tisAmt*0.15*9/12:0;''')
rep('''welf,straord,strNF,str40,''','''welf,straord,strHr,strNFamt,strNF,str40,''')
rep('''strOre:$("strOn").checked?numv("strOre")||0:0,strMagg:numv("strMagg")||0,strDiv:strDivisore(),strTipo:$("strTipo").value,''','''strRows:strRead(),strDiv:strDivisore(),''')
a=s.index('  { const on=$("strOn").checked; document.querySelectorAll("[data-str]")'); b=s.index('\n',s.index('put("s-str"',a))
s=s[:a]+'''  { const div=strDivisore(), n=(o.strRows||[]).length, k=$("ccnl").value;
    $("str-h").textContent=!div?"Per i dirigenti l'orario non è fissato dal CCNL: straordinari e maggiorazioni di norma non spettano.":
      `Paga oraria ${eur(x.strHr,2)}: retribuzione mensile${x.ind>0?" e indennità fisse":""} ÷ ${fmtIt(Math.round(div*100)/100)} ore${DIV[k]?" (divisore del CCNL)":""}. Percentuali precompilate dal CCNL${k==="metalmeccanici"?"":" (valori tipici: verifica sul tuo contratto)"}, modificabili. Non utili al TFR.`
      +(!x.strNF?"":o.strTur?(x.tis>0?" Turismo e pubblici esercizi: +15% esentasse su notturno e straordinario festivo da gennaio a settembre 2026.":" Trattamento integrativo turismo: non spetta, reddito 2025 oltre 40.000 €.")
        :(x.strDet>0?" Notturno e festivo: imposta al 15% fino a 1.500 € nel 2026 (straordinario: tutto il compenso; maggiorazione: la percentuale).":" Imposta al 15% su notturno e festivo: non spetta, reddito 2025 oltre 40.000 €."));
    for(const r of document.querySelectorAll("#str-list .fr")){ const q=r._q; r.querySelector(".st-h").textContent=q?`${eur(x.strHr*q.ore*((q.s?1:0)+q.p/100))} lordi al mese`:""; }
    put("s-str",n&&x.straord?`${n} ${n===1?"voce":"voci"} · ${eur(x.straord/12)}/mese`:"Nessuno",n>0&&x.straord>0); }'''+s[b:]
rep('''      pos(`Straordinari (${fmtIt(o.strOre||0)} ore al mese)`,v.str),''','''      pos("Straordinari e maggiorazioni",v.str),''')
rep('''      !M&&x.strDet>0&&x.straord>1500?[`Straordinario oltre 1.500 €: la parte in più (${eur(x.straord-1500)}) è tassata normalmente.`,"","warn"]:null,''',
'''      !M&&x.strDet>0&&x.strNFamt>1500?[`Notturno e festivo oltre 1.500 €: la parte in più (${eur(x.strNFamt-1500)}) è tassata normalmente.`,"","warn"]:null,''')
a=s.index('var MAGG={'); b=s.index('const ORE={',a)
s=s[:a]+'''var MAGG={commercio:[15,50,30],tessile:[35,56,61],alimentare:[45,50,60],gomma:[18,30,50],studi:[15,30,30],
  turismo:[30,60,30],pubblici:[30,60,30],logistica:[30,50,50],abi:[25,50,50],abicompl:[25,50,50],altro:[25,50,50]};
/* Maggiorazioni su orario ordinario [notturno, festivo]: valori tipici, modificabili */
var ORDM={commercio:[15,30],turismo:[25,20],pubblici:[25,20],altro:[25,30]};
/* Voci: [chiave, nome, straordinario (ora intera + %), notte/festivo (imposta 15%), trattamento integrativo turismo, % [non a turni, a turni]] */
var STR_MET=[
  ["sd2","Straordinario diurno, prime 2 ore",1,0,0,[25,25]],["sdx","Straordinario diurno, ore successive",1,0,0,[30,30]],
  ["ss2","Straordinario al sabato (orario su 5 giorni), prime 2 ore",1,0,0,[25,25]],["ssx","Straordinario al sabato, ore successive",1,0,0,[50,50]],
  ["sn2","Straordinario notturno, prime 2 ore",1,1,1,[50,40]],["snx","Straordinario notturno, ore successive",1,1,1,[50,45]],
  ["sf","Straordinario festivo",1,1,1,[55,55]],["sfr","Straordinario festivo con riposo compensativo",1,1,1,[35,35]],
  ["snf","Straordinario notturno festivo",1,1,1,[75,65]],["snfr","Straordinario notturno festivo con riposo compensativo",1,1,1,[55,50]],
  ["mn22","Maggiorazione notturno fino alle 22",0,1,1,[20,20]],["mn","Maggiorazione notturno dopo le 22",0,1,1,[30,20]],
  ["mf","Maggiorazione festivo",0,1,0,[50,50]],["mfr","Maggiorazione festivo con riposo compensativo",0,1,0,[10,10]],
  ["mnf","Maggiorazione notturno festivo",0,1,1,[60,60]],["mnfr","Maggiorazione notturno festivo con riposo compensativo",0,1,1,[35,35]]];
function strTipi(){ const k=$("ccnl").value; if(k==="metalmeccanici") return STR_MET;
  const m=MAGG[k]||MAGG.altro, d=ORDM[k]||ORDM.altro, L=[["sd","Straordinario diurno",1,0,0,[m[0],m[0]]]];
  if(k==="commercio"){ L[0][1]="Straordinario diurno, dalla 41ª alla 48ª ora"; L.push(["sd48","Straordinario diurno, oltre la 48ª ora",1,0,0,[20,20]]); }
  L.push(["sn","Straordinario notturno",1,1,1,[m[1],m[1]]],["sf","Straordinario festivo",1,1,1,[m[2],m[2]]],
    ["mn","Maggiorazione notturno (orario normale)",0,1,1,[d[0],d[0]]],["mf","Maggiorazione festivo (orario normale)",0,1,0,[d[1],d[1]]]);
  return L; }
function strDivisore(){ const k=$("ccnl").value; return DIV[k]||(ORE[k]||0)*52/12; }
function strPct(t){ const e=strTipi().find(z=>z[0]===t); return e?e[5][$("strTurni").checked?1:0]:0; }
function strRow(t){ const T=strTipi(); t=t&&T.some(z=>z[0]===t)?t:T[0][0]; const d=document.createElement("div"); d.className="fr";
  const g=(f,lab)=>`<optgroup label="${lab}">`+T.filter(f).map(([k,l])=>`<option value="${k}"${k===t?" selected":""}>${l}</option>`).join("")+"</optgroup>";
  d.innerHTML=`<div class="fr-h full"><select class="st-t" aria-label="Tipo">${g(z=>z[2],"Straordinario")}${g(z=>!z[2],"Maggiorazione su orario normale")}</select><button type="button" class="fr-x" aria-label="Rimuovi">×</button></div>
  <div><small>Ore al mese</small><div class="ctl" data-u="ore/mese"><input class="st-o" inputmode="decimal" type="text" value="8"></div></div>
  <div><small>Maggiorazione</small><div class="ctl" data-u="%"><input class="st-p" inputmode="decimal" type="text" value="${fmtIt(strPct(t))}"></div></div>
  <div class="fr-val st-h"></div>`; return d; }
function strRead(){ const T=strTipi(), out=[];
  for(const r of document.querySelectorAll("#str-list .fr")){ const e=T.find(z=>z[0]===r.querySelector(".st-t").value)||T[0];
    const q={s:!!e[2],nf:!!e[3],tis:!!e[4],ore:parseIt(r.querySelector(".st-o").value)||0,p:parseIt(r.querySelector(".st-p").value)||0};
    r._q=q; out.push(q); }
  $("str-turni-box").hidden=$("ccnl").value!=="metalmeccanici"; return out; }
function strReset(){ // cambio CCNL o turni: ricostruisce i tipi e rimette le % del contratto dove non modificate a mano
  for(const r of [...document.querySelectorAll("#str-list .fr")]){ const t=r.querySelector(".st-t").value, o=r.querySelector(".st-o").value, p=r.querySelector(".st-p").value, n=strRow(t);
    n.querySelector(".st-o").value=o; if(r.dataset.touched&&n.querySelector(".st-t").value===t){ n.querySelector(".st-p").value=p; n.dataset.touched=1; } r.replaceWith(n); } }
'''+s[b:]
rep('''strMaggTouched=false; setMagg(); render();});''','''strReset(); render();});''')
rep('''$("strOn").addEventListener("change",render);''','''$("str-add").addEventListener("click",()=>{ $("str-list").appendChild(strRow()); render(); });
$("strTurni").addEventListener("change",()=>{ strReset(); render(); });
$("str-list").addEventListener("click",e=>{ if(e.target.closest(".fr-x")){ e.target.closest(".fr").remove(); render(); } });
$("str-list").addEventListener("input",e=>{ if(e.target.matches("input[type=text]")){ liveFormat(e.target,e); if(e.target.matches(".st-p")) e.target.closest(".fr").dataset.touched=1; } render(); });
$("str-list").addEventListener("change",e=>{ if(e.target.matches(".st-t")){ const r=e.target.closest(".fr"); r.querySelector(".st-p").value=fmtIt(strPct(e.target.value)); delete r.dataset.touched; } render(); });''')
rep('''$("strTipo").addEventListener("change",()=>{setMagg();render();});
$("strMagg").addEventListener("input",()=>{strMaggTouched=true;});
setMagg();
''','')
rep('''["strOre","strMagg"].forEach(id=>$(id).addEventListener("input",e=>{liveFormat($(id),e);render();}));''','')
open(p,'w').write(s)
