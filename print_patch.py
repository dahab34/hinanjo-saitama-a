# -*- coding: utf-8 -*-
"""住所から探す ＋ 近い避難所の印刷シート（A4・1枚）を、テンプレート系のページに追加する。
エリア版（自動生成）と、東松山版・久喜版（同じエンジン）に使える。"""
import sys

INDEX_URL = 'https://dahab34.github.io/hinanjo-saitama-a/hinanjo-areas.html'
QR_URL = 'https://cdn.jsdelivr.net/npm/qrcode-generator@1.4.4/qrcode.js'

CSS = """
.addrbox{display:flex;gap:6px;margin:6px 0 0}
.addrbox input{flex:1;min-width:0;font-size:16px;padding:9px 10px;border:1px solid var(--line);border-radius:10px;background:#fff}
.addrbox button{border:0;background:#e9eef4;color:var(--accent);font-weight:700;font-size:14px;padding:0 12px;border-radius:10px;cursor:pointer;white-space:nowrap}
.printbtns{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}
.printbtn{flex:1 1 180px;display:block;padding:10px;border:1px solid var(--accent);background:#fff;color:var(--accent);font-weight:700;font-size:14.5px;border-radius:10px;cursor:pointer}
#printSheet{display:none}
.printbtn:disabled{opacity:.6}
@media print{
 body.printing>*:not(#printSheet){display:none!important}
 body.printing{background:#fff!important}
 body.printing #printSheet{display:block}
 @page{size:A4 portrait;margin:10mm 12mm}
}
#printSheet{width:auto;max-width:100%;box-sizing:border-box;font-family:"Hiragino Kaku Gothic ProN","Hiragino Sans","Noto Sans JP","Yu Gothic",Meiryo,sans-serif;color:#000;font-size:10.5pt;line-height:1.45}
#printSheet h1{font-size:14pt;margin:0 0 .5mm}
#printSheet .ps-sub{font-size:9pt;color:#333;margin-bottom:2mm}
#printSheet .ps-top{display:flex;gap:4mm;align-items:flex-start;border:1.2pt solid #000;padding:3mm;margin-bottom:3mm}
#printSheet .ps-top .f{flex:1}
#printSheet .ps-row{display:flex;border-bottom:.6pt solid #888;padding:1.1mm 0 .5mm;font-size:10pt}
#printSheet .ps-row b{width:24mm;flex:none}
#printSheet .ps-qr{text-align:center;font-size:7pt;width:20mm;flex:none}
#printSheet .ps-qr svg{width:13mm;height:13mm}
#printSheet .ps-sec{border:0;padding:0;margin:0;background:none}
#printSheet h1,#printSheet h2,#printSheet b,#printSheet td,#printSheet div{color:#000}
#printSheet h2{font-size:10pt;margin:0 0 .6mm;padding:.7mm 2mm;background:#e6e6e6;border-left:2.5mm solid #000}
#printSheet h2 small{font-weight:400;font-size:8.5pt;margin-left:2mm}
#printSheet table{width:100%;table-layout:fixed;border-collapse:collapse;page-break-inside:avoid}
#printSheet td.n{width:9mm;text-align:center;padding-top:1mm}
#printSheet td{border:.6pt solid #666;padding:.5mm 1.4mm;vertical-align:top}
#printSheet td.n{width:6mm;text-align:center;font-weight:700}
#printSheet td.q{width:10mm;text-align:center;font-size:6pt;color:#333;padding:.6mm}
#printSheet td.q svg{width:9mm;height:9mm;display:block;margin:0 auto}
#printSheet td.d{width:16mm;text-align:right;white-space:nowrap}
#printSheet .ps-nm{font-weight:700;font-size:10pt;color:#000;line-height:1.3}
#printSheet .ps-sm{font-size:8pt;color:#222;line-height:1.3}
#printSheet .ps-fl{display:inline-block;border:.6pt solid #000;border-radius:1mm;padding:0 1.2mm;font-size:8pt;margin-top:.3mm;line-height:1.35}
#printSheet .ps-fl.ng{background:#000;color:#fff}
#printSheet .ps-none{font-size:9pt;color:#444;padding:1mm 0}
#printSheet,#printSheet *{-webkit-print-color-adjust:exact;print-color-adjust:exact}
#printSheet .ps-mapbox{position:relative;width:703px;overflow:hidden;border:1pt solid #000;background:#eee}
#printSheet .ps-tile{position:absolute;width:256px;height:256px;max-width:none}
#printSheet .ps-ov{position:absolute;left:0;top:0}
#printSheet .ps-pin{position:absolute;transform:translate(-50%,-50%);white-space:nowrap}
#printSheet .ps-mk{display:inline-block;border:1.4px solid #000;border-radius:9px;padding:0 4px;font-size:8.5pt;font-weight:800;line-height:1.35;background:#fff;color:#000}
#printSheet .ps-g避{background:#cfe0ff} #printSheet .ps-g緊{background:#ffe0b0} #printSheet .ps-g水{background:#c8f0ff} #printSheet .ps-g福{background:#f1d4f5}
#printSheet .ps-home{color:#d00;font-size:22pt;line-height:1;-webkit-text-stroke:1.2px #fff;text-shadow:0 0 2px #000}
#printSheet .ps-legend .ps-home{font-size:12pt}
#printSheet .ps-homepin{z-index:3}
#printSheet .ps-scale{position:absolute;left:10px;bottom:10px;background:rgba(255,255,255,.9);padding:2px 5px;font-size:8pt;font-weight:700}
#printSheet .ps-scale div{height:5px;border:1.5px solid #000;border-top:0;margin-bottom:1px}
#printSheet .ps-north{position:absolute;right:10px;top:8px;background:rgba(255,255,255,.9);padding:2px 6px;text-align:center;font-size:9pt;font-weight:800;line-height:1.1}
#printSheet .ps-attr{position:absolute;right:4px;bottom:3px;font-size:6.5pt;background:rgba(255,255,255,.85);padding:0 3px}
#printSheet .ps-legend{font-size:8.5pt;margin-top:1.2mm;line-height:1.6}
#printSheet .ps-legend .ps-mk{font-size:7.5pt;margin:0 2px 0 0}
#printSheet td.n .ps-mk{font-size:8pt}
#printSheet .ps-head{display:flex;align-items:baseline;gap:4mm;flex-wrap:wrap;margin-bottom:1.5mm}
#printSheet .ps-head h1{margin:0}
#printSheet .ps-head .ps-sub{margin:0}
#printSheet .ps-row2{display:flex;gap:4mm}
#printSheet .ps-row2 .ps-row{flex:1}
#printSheet .ps-top{padding:1.5mm 3mm;margin-bottom:2mm}
#printSheet .ps-lists{columns:2;column-gap:5mm;margin-top:1mm}
#printSheet .ps-it,#printSheet h2{break-inside:avoid;page-break-inside:avoid}
#printSheet h2{break-after:avoid}
#printSheet .ps-sec+.ps-sec{margin-top:1.6mm}
#printSheet .ps-it{display:flex;gap:1.6mm;align-items:flex-start;border-bottom:.5pt solid #999;padding:.8mm 0}
#printSheet .ps-it>.ps-mk{flex:none;margin-top:.4mm}
#printSheet .ps-tx{flex:1;min-width:0}
#printSheet .ps-d{float:right;font-weight:700;font-size:9pt;margin-left:2mm}
#printSheet .ps-foot{margin-top:1.5mm;font-size:7.3pt;line-height:1.35;color:#222;border-top:.6pt solid #000;padding-top:1.5mm}
"""

ADDR_HTML = ('<form class="addrbox" id="addrform" onsubmit="return false">'
             '<input id="addr" type="search" placeholder="住所から探す（例：北本市本町1-111）" enterkeyhint="search" autocomplete="off">'
             '<button id="addrgo" type="submit">住所で探す</button></form>')

JS = r"""
/* ===== 住所から探す ＋ 印刷シート ===== */
let CURBASE="現在地", QRLIB=null;
const _DATA=()=>typeof RAW!=="undefined"?RAW:GEO;
const _KN=k=>typeof KIND!=="undefined"?(KIND[k]?KIND[k][0]:""):((typeof KMAPg!=="undefined"&&KMAPg[k])||"");
const _MSG=html=>{ (typeof dynNote!=="undefined"?dynNote:out).innerHTML=html; if(typeof dynNote!=="undefined") out.innerHTML=""; };
const _GPS=(a,b,c,d)=>(typeof renderGpsU==="function"?renderGpsU:renderGps)(a,b,c,d);
const _FD=m=>m<1000?Math.round(m/10)*10+"m":(m/1000).toFixed(1)+"km";
function loadQR(){ if(window.qrcode||QRLIB) return; QRLIB=document.createElement("script"); QRLIB.src="__QR__"; document.head.appendChild(QRLIB); }
function qrSvg(t){ try{ if(!window.qrcode) return ""; const q=qrcode(0,"M"); q.addData(t); q.make(); return q.createSvgTag(2,0); }catch(e){ return ""; } }
async function geocode(text){
 const r=await fetch("https://msearch.gsi.go.jp/address-search/AddressSearch?q="+encodeURIComponent(text));
 if(!r.ok) throw new Error("http"); const a=await r.json();
 if(!a||!a.length) return null;
 const c=a[0].geometry.coordinates; return {lat:+c[1],lng:+c[0],title:(a[0].properties&&a[0].properties.title)||text};
}
(function(){
 const f=document.getElementById("addrform"), inp=document.getElementById("addr"), btn=document.getElementById("addrgo");
 if(!f) return;
 f.addEventListener("submit",async e=>{
  e.preventDefault(); const v=inp.value.trim(); if(!v) return;
  btn.disabled=true; btn.textContent="検索中…";
  try{
   const g=await geocode(v);
   if(!g){ _MSG('<div class="alert">⚠ その住所が見つかりませんでした。市町村名から入れてみてください（例：北本市本町1-111）。</div>'); return; }
   let m=1e18; _DATA().forEach(s=>{ if(s.lat&&s.lng){ const d=distM(g.lat,g.lng,s.lat,s.lng); if(d<m) m=d; } });
   if(m>5000){ _MSG(`<div class="alert">⚠ 「${g.title}」はこのページの対象エリアの外のようです。<br><a href="__INDEX__?addr=${encodeURIComponent(v)}">全エリアから探す ›</a></div>`); segEl.innerHTML=""; countEl.textContent=""; return; }
   _GPS(g.lat,g.lng,null,g.title);
  }catch(err){ _MSG('<div class="alert">⚠ 住所検索に失敗しました（通信状況を確認してください）。地名・施設名の検索や現在地ボタンもお使いいただけます。</div>'); }
  finally{ btn.disabled=false; btn.textContent="住所で探す"; }
 });
})();
function isEmg(s){ return s.kind==="Q"||s.kind==="P"||((s.kind==="K"||s.kind==="H")&&s.flood&&s.flood!=="-"); }
function buildSheet(lat,lng,base,list,isAddr,onReady){
 const E=s=>String(s==null?"":s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
 const N=3, now=new Date(), ds=`${now.getFullYear()}年${now.getMonth()+1}月${now.getDate()}日`;
 const asof=((typeof SRC!=="undefined"&&SRC[city]||"").match(/（([^）]*時点)）/)||[])[1]||"";
 const flT=s=>{ if(s.flood==="up") return ["水害時は "+(s.fl||"上の階")+" へ",""]; if(s.flood==="no") return ["水害時は使えない","ng"]; if(s.flood==="ok") return ["水害時 1階から可",""]; return ["水害時の可否：データ未掲載",""]; };
 const FOK=s=>s.flood==="ok"||s.flood==="up";
 const G=[["まず逃げる場所","指定緊急避難場所",isEmg,"緊"],
          ["寝泊まりする場所","指定避難所",s=>s.kind==="K"||s.kind==="H","避"],
          ["福祉避難所","要配慮者向け・状況に応じて開設",s=>s.kind==="F","福"]];
 const key=s=>s.name+"|"+s.addr, top=g=>list.filter(g[2]).slice(0,N);
 const shown=new Set(); [G[0],G[1]].forEach(g=>top(g).forEach(s=>shown.add(key(s))));
 const needF=[G[0],G[1]].some(g=>top(g).some(s=>s.flood==="no"));
 if(needF&&list.some(s=>"KHQP".includes(s.kind)&&FOK(s)&&!shown.has(key(s))))
  G.splice(2,0,["水害のときの避難先","洪水でも使える施設",s=>"KHQP".includes(s.kind)&&FOK(s)&&!shown.has(key(s)),"水"]);
 const marks=[];
 const items=(g,n)=>{ const L=list.filter(g[2]).slice(0,n||N); if(!L.length) return '<div class="ps-none">この周辺には登録がありません。</div>';
  return L.map((s,i)=>{ const f=flT(s), lb=g[3]+(i+1); marks.push({lat:s.lat,lng:s.lng,lb:lb,g:g[3]});
   const both=g[3]==="緊"&&(s.kind==="K"||s.kind==="H")?"（避難所も兼ねる）":"";
   return `<div class="ps-it"><span class="ps-mk ps-g${g[3]}">${lb}</span><div class="ps-tx"><div class="ps-nm">${E(s.name)}<span class="ps-d">約${_FD(s._d)}</span></div><div class="ps-sm">${E(s.city+s.addr)}${s.tel?"　☎"+E(s.tel):""}${both}</div><div class="ps-sm"><span class="ps-fl ${f[1]}">${f[0]}</span>${s.note?"　※"+E(s.note):""}</div></div></div>`; }).join(""); };
 const lists=G.map(g=>`<div class="ps-sec"><h2>${g[0]}<small>${g[1]}</small></h2>`+items(g,(G.length>3&&g[3]==="福")?2:N)+`</div>`).join("");
 const hz=qrSvg(`https://disaportal.gsi.go.jp/maps/index.html?ll=${lat},${lng}&z=16`);
 const el=document.getElementById("printSheet")||document.body.appendChild(Object.assign(document.createElement("div"),{id:"printSheet"}));
 el.innerHTML=`<div class="ps-head"><h1>わが家の避難先メモ</h1><div class="ps-sub">${isAddr?`基準：<b>${E(base)}</b>`:`基準：現在地（${lat.toFixed(5)}, ${lng.toFixed(5)}）`}　作成日：${ds}</div></div>
 <div class="ps-top"><div class="f">
  <div class="ps-row2"><div class="ps-row"><b>お名前</b><span></span></div><div class="ps-row"><b>緊急連絡先</b><span></span></div></div>
  <div class="ps-row"><b>メモ</b><span style="color:#777;font-size:8pt">持ち出し品・避難の手助けが必要なこと など</span></div>
 </div>${hz?`<div class="ps-qr">${hz}<br>ハザードマップ</div>`:""}</div>
 <div class="ps-mapbox" id="psMapbox" style="height:${G.length>3?390:470}px"></div>
 <div class="ps-legend"><span class="ps-home">★</span>${isAddr?"この住所":"現在地"}　<span class="ps-mk ps-g緊">緊</span>まず逃げる場所　<span class="ps-mk ps-g避">避</span>寝泊まりする場所${G.some(g=>g[3]==="水")?'　<span class="ps-mk ps-g水">水</span>水害のときの避難先':""}　<span class="ps-mk ps-g福">福</span>福祉避難所　<span style="color:#c00">点線の円</span>＝直線500m・1km</div>
 <div class="ps-lists">${lists}</div>
 <div class="ps-foot">距離は直線です。浸水や通行止めで通れない道もあります。どこが開くかは災害ごとに違うので、市町村の防災無線・避難情報を確認してください。「水害時は使えない」場所には洪水のとき行かないでください。<br>出典：国土地理院 指定緊急避難場所・指定避難所データ${asof?"（"+E(asof)+"）":""}・各市町の避難所資料・地理院タイル（埼玉 避難所ナビ）</div>`;
 drawMap(document.getElementById("psMapbox"),lat,lng,marks,onReady,G.length>3?390:470);
}
function drawMap(box,lat,lng,marks,onReady,H){
 const W=703,PAD=36,T=256; H=H||470;
 const wx=(ln,z)=>(ln+180)/360*T*2**z, wy=(la,z)=>{const r=la*Math.PI/180;return (1-Math.log(Math.tan(r)+1/Math.cos(r))/Math.PI)/2*T*2**z;};
 const pts=[{lat:lat,lng:lng}].concat(marks.filter(m=>m.lat&&m.lng));
 let z=17;
 for(;z>10;z--){ const xs=pts.map(p=>wx(p.lng,z)), ys=pts.map(p=>wy(p.lat,z));
  if(Math.max(...xs)-Math.min(...xs)<=W-2*PAD&&Math.max(...ys)-Math.min(...ys)<=H-2*PAD) break; }
 const xs=pts.map(p=>wx(p.lng,z)), ys=pts.map(p=>wy(p.lat,z));
 const ox=(Math.max(...xs)+Math.min(...xs))/2-W/2, oy=(Math.max(...ys)+Math.min(...ys))/2-H/2;
 let html="", n=0;
 for(let tx=Math.floor(ox/T);tx<=Math.floor((ox+W)/T);tx++) for(let ty=Math.floor(oy/T);ty<=Math.floor((oy+H)/T);ty++){ n++;
  html+=`<img class="ps-tile" alt="" style="left:${(tx*T-ox).toFixed(1)}px;top:${(ty*T-oy).toFixed(1)}px" src="https://cyberjapandata.gsi.go.jp/xyz/std/${z}/${tx}/${ty}.png">`; }
 const bx=wx(lng,z)-ox, by=wy(lat,z)-oy, mpp=156543.03392*Math.cos(lat*Math.PI/180)/2**z;
 html+=`<svg class="ps-ov" width="${W}" height="${H}">`+[500,1000].map(m=>{const r=m/mpp;return r<Math.max(W,H)*1.5?`<circle cx="${bx}" cy="${by}" r="${r}" fill="none" stroke="#c00" stroke-width="1.6" stroke-dasharray="6 5"/><text x="${bx+r*0.71+3}" y="${by-r*0.71-3}" font-size="12" font-weight="700" fill="#c00" stroke="#fff" stroke-width="3" paint-order="stroke">${m<1000?m+"m":m/1000+"km"}</text>`:"";}).join("")+`</svg>`;
 const groups=[]; marks.forEach(m=>{ if(!m.lat) return; const x=wx(m.lng,z)-ox, y=wy(m.lat,z)-oy;
  const g=groups.find(q=>Math.hypot(q.x-x,q.y-y)<14); if(g){g.lb.push(m.lb);} else groups.push({x:x,y:y,lb:[m.lb],g:m.g}); });
 groups.forEach(q=>{ html+=`<div class="ps-pin" style="left:${q.x.toFixed(1)}px;top:${q.y.toFixed(1)}px"><span class="ps-mk ps-g${q.g}">${q.lb.join("・")}</span></div>`; });
 html+=`<div class="ps-pin ps-homepin" style="left:${bx.toFixed(1)}px;top:${by.toFixed(1)}px"><span class="ps-home">★</span></div>`;
 const nice=[50,100,200,500,1000,2000].find(m=>m/mpp>=90)||2000, bl=nice/mpp;
 html+=`<div class="ps-scale"><div style="width:${bl.toFixed(0)}px"></div>${nice<1000?nice+"m":nice/1000+"km"}</div><div class="ps-north">▲<br>北</div><div class="ps-attr">地理院タイル（標準地図）</div>`;
 box.innerHTML=html;
 let left=n, fired=false; const fin=()=>{ if(!fired){ fired=true; onReady&&onReady(); } };
 box.querySelectorAll("img").forEach(im=>{ const d=()=>{ if(--left<=0) fin(); }; if(im.complete) d(); else { im.onload=d; im.onerror=d; } });
 setTimeout(fin,8000);
}
function addPrintBtns(box,lat,lng,base,list,isAddr){
 const w=document.createElement("div"); w.className="printbtns";
 const b1=document.createElement("button"); b1.type="button"; b1.className="printbtn"; w.appendChild(b1);
 b1.textContent="🗺 印刷用の地図を準備中…"; b1.disabled=true; b1.onclick=()=>doPrint();
 box.appendChild(w);
 const ready=()=>{ b1.disabled=false; b1.textContent="🖨 地図つきで印刷する（A4・1枚）"; };
 const build=()=>buildSheet(lat,lng,base,list,isAddr,ready);
 build();
 if(!window.qrcode&&QRLIB) QRLIB.addEventListener("load",build,{once:true});
}
function doPrint(){
 document.body.classList.add("printing");
 const done=()=>{ document.body.classList.remove("printing"); window.removeEventListener("afterprint",done); };
 window.addEventListener("afterprint",done);
 window.print(); setTimeout(done,2000);
}
"""


def _konosu(h):
    """鴻巣版（独自エンジン）の renderGps に基準地点と印刷ボタンを足す。"""
    a = h.index('function renderGps(lat,lng,acc){')
    b = h.index('\n}\n', a) + 3
    f = h[a:b]
    rep = [('function renderGps(lat,lng,acc){', 'function renderGps(lat,lng,acc,label){\n  const BASE=label||"現在地"; CURBASE=BASE; loadQR();'),
           ('hintEl.innerHTML="<b>現在地から近い順</b>に全施設（全タブ横断）を表示しています。地名で探すときは上の検索を。";',
            'hintEl.innerHTML=`<b>${BASE}から近い順</b>に全施設（全タブ横断）を表示しています。地名で探すときは上の検索を。`;'),
           ('countEl.textContent="現在地から近い順";', 'countEl.textContent=`${BASE}から近い順`;'),
           ('現在地から約 <b>', '${BASE}から約 <b>'),
           ('const G2=list.filter(s=>s.kind==="Q"||s.kind==="P").slice(0,LIM);', 'const G2=list.filter(isEmg).slice(0,LIM);'),
           ('\n  const LIM=15;', '\n  {const g=dynNote.querySelector(".gpsbest");if(g)addPrintBtns(g,lat,lng,BASE,list,!!label);}'
                              '\n  const LIM=15;')]
    for x, y in rep:
        assert x in f, x[:50]
        f = f.replace(x, y, 1)
    return h[:a] + f + h[b:]


def _template(h, detail):
    a = h.index('function renderGpsU(lat,lng,acc){')
    b = h.index('\n}\n', a) + 3
    f = h[a:b]
    f = f.replace('function renderGpsU(lat,lng,acc){', 'function renderGpsU(lat,lng,acc,label){\n const BASE=label||"現在地"; CURBASE=BASE; loadQR();', 1)
    f = f.replace('hintEl.innerHTML="<b>現在地から近い順</b>', 'hintEl.innerHTML=`<b>${BASE}から近い順</b>', 1)
    f = f.replace('全施設（全タブ横断）を表示しています。地名で探すときは上の検索を。";', '全施設（全タブ横断）を表示しています。地名で探すときは上の検索を。`;', 1)
    f = f.replace('countEl.textContent="現在地から近い順";', 'countEl.textContent=`${BASE}から近い順`;', 1)
    f = f.replace('現在地から約 <b>', '${BASE}から約 <b>', 1)
    f = f.replace('`【現在地から近い避難先】\\n現在地：https://www.google.com/maps/search/?api=1&query=${lat},${lng}\\n\\n`',
                  '`【${BASE}から近い避難先】\\n${label?"基準の住所："+label+"\\n":""}地点：https://www.google.com/maps/search/?api=1&query=${lat},${lng}\\n\\n`', 1)
    f = f.replace('shareRow("現在地から近い避難先",sumText)', 'shareRow(`${BASE}から近い避難先`,sumText)', 1)
    f = f.replace('lb.textContent="▼ 現在地と最寄りの避難先をまとめて送る";', 'lb.textContent=`▼ ${label?"この住所":"現在地"}と最寄りの避難先をまとめて送る`;', 1)
    f = f.replace('footEl.innerHTML=`現在地から全タブ横断で', 'footEl.innerHTML=`${BASE}から全タブ横断で', 1)
    f = f.replace('const G2=list.filter(s=>s.kind==="Q"||s.kind==="P").slice(0,LIM);', 'const G2=list.filter(isEmg).slice(0,LIM);', 1)
    f = f.replace('["指定緊急避難場所",near(s=>s.kind==="Q"||s.kind==="P")]', '["指定緊急避難場所",near(isEmg)]', 1)
    assert 'list.filter(isEmg)' in f and 'near(isEmg)' in f
    anchor = '\n out.appendChild(banner);\n const LIM=15;'
    assert anchor in f, 'banner anchor'
    add = ''
    if detail:
        add += ('\n {const du=typeof DETAILURL!=="undefined"&&DETAILURL[best.city];if(du){const d=document.createElement("div");d.style.cssText="margin-top:8px;font-size:13.5px";'
                'd.innerHTML=`📘 ${best.city}には市町の資料で作り込んだ<b>詳しい版</b>があります（水害時の階数など）。<a href="${du}&lat=${lat}&lng=${lng}&label=${encodeURIComponent(BASE)}">詳しい版で見る・印刷する ›</a>`;banner.appendChild(d);}}')
    add += ('\n addPrintBtns(banner,lat,lng,BASE,list,!!label);')
    f = f.replace(anchor, add + anchor, 1)
    assert f.count('BASE') >= 8, f.count('BASE')
    h = h[:a] + f + h[b:]
    h = h.replace(' if(dist!=null&&isFinite(dist)) t+=`\\n現在地から約${fmtD(dist)}（直線）`;',
                  ' if(dist!=null&&isFinite(dist)) t+=`\\n${CURBASE}から約${fmtD(dist)}（直線）`;', 1)
    return h


def patch(path, detail=None):
    """detail: {市町村名: 詳しい版のURL(?city=付き)} を渡すと、結果に詳しい版への案内を出す（エリア版用）。"""
    import json
    h = open(path, encoding='utf-8').read()
    if 'function buildSheet(' in h:
        return 'skip(already)'
    i = h.find('</style>'); assert i > 0
    h = h[:i] + CSS + h[i:]
    gb = '<button id="gps" type="button" class="gpsbtn">📍 今いる場所から一番近い避難所</button>'
    assert gb in h, 'gps button'
    h = h.replace(gb, gb + '\n  ' + ADDR_HTML, 1)
    if 'function renderGpsU(lat,lng,acc){' in h:
        h = _template(h, detail)
    else:
        h = _konosu(h)
    js = JS.replace('__QR__', QR_URL).replace('__INDEX__', INDEX_URL)
    if detail:
        js = 'const DETAILURL=' + json.dumps(detail, ensure_ascii=False) + ';\n' + js
    js += ('try{const _p=new URLSearchParams(location.search),_la=parseFloat(_p.get("lat")),_ln=parseFloat(_p.get("lng"));'
           'if(isFinite(_la)&&isFinite(_ln))setTimeout(()=>_GPS(_la,_ln,null,_p.get("label")||"指定した地点"),60);}catch(e){}\n')
    i = h.rfind('</script>'); assert i > 0
    h = h[:i] + js + h[i:]
    open(path, 'w', encoding='utf-8').write(h)
    return 'patched'


if __name__ == '__main__':
    for p in sys.argv[1:]:
        print(p.split('/')[-1], patch(p))
