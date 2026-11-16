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
.printbtn.main{background:var(--accent);color:#fff}
.printbtn.ready{background:#1d7a3d;border-color:#1d7a3d;color:#fff}
.printhint{font-size:12px;color:var(--sub);margin-top:6px}
#cityDocs{font-size:13px;}
.share.one{justify-content:flex-end}
.share .sendone{font-size:12px;padding:4px 12px;border-radius:14px;border:1px solid var(--line);background:#fff;color:var(--sub);cursor:pointer}
#cityDocs{margin:6px 2px 2px;line-height:1.7}
#cityDocs a{margin-right:2px}
#psLiveWrap{margin-top:10px}
#psLive{height:340px;border-radius:10px;border:1px solid var(--line);background:#e9edf2;z-index:0}
@media (min-width:900px){#psLive{height:440px}}
.lvbar{display:flex;flex-wrap:wrap;gap:4px 10px;align-items:center;font-size:12px;color:var(--sub);margin-top:5px}
.lvbar label{font-weight:600;color:var(--ink,#1c2530)}
.lvlg i{display:inline-block;width:11px;height:11px;border:1px solid #999;margin:0 2px 0 6px;vertical-align:-1px}
.lvmk{display:inline-block;white-space:nowrap;border:1.5px solid #000;border-radius:9px;padding:0 5px;font-size:12px;font-weight:800;line-height:1.4;background:#fff;color:#000;transform:translate(-50%,-50%);box-shadow:0 1px 2px rgba(0,0,0,.3);cursor:pointer}
.lv避{background:#cfe0ff}.lv緊{background:#ffe0b0}.lv水{background:#c8f0ff}.lv福{background:#f1d4f5}
.lvhome{display:block;color:#d00;font-size:26px;line-height:26px;text-align:center;-webkit-text-stroke:1.2px #fff;text-shadow:0 0 2px #000}
@media print{
 body.printing>*:not(#printSheet){display:none!important}
 body.printing{background:#fff!important}
 body.printing #printSheet{display:block}
 @page{size:A4 portrait;margin:0}
 /* 余白はシート側で持つ（ブラウザの「余白：なし」やプリンターの「用紙に合わせる」でも上が切れないように） */
 body.printing{margin:0!important;padding:0!important}

}
#printSheet{box-sizing:border-box;font-family:"Hiragino Kaku Gothic ProN","Hiragino Sans","Noto Sans JP","Yu Gothic",Meiryo,sans-serif;color:#000;font-size:14px;line-height:1.45}
#printSheet h1{font-size:18.7px;margin:0 0 2px}
#printSheet .ps-sub{font-size:12px;color:#333;margin-bottom:7.6px}
#printSheet .ps-top{display:flex;gap:15.1px;align-items:flex-start;border:1.6px solid #000;padding:11.3px;margin-bottom:11.3px}
#printSheet .ps-top .f{flex:1}
#printSheet .ps-row{display:flex;border-bottom:.8px solid #888;padding:4.2px 0 2px;font-size:13.3px}
#printSheet .ps-row b{width:90.7px;flex:none}
#printSheet .ps-qr{text-align:center;font-size:9.3px;width:75.6px;flex:none}
#printSheet .ps-qr svg{width:49.1px;height:49.1px}
#printSheet .ps-sec{border:0;padding:0;margin:0;background:none}
#printSheet h1,#printSheet h2,#printSheet b,#printSheet td,#printSheet div{color:#000}
#printSheet h2{font-size:13.3px;margin:0 0 3px;padding:3.5px 7.6px;background:#e6e6e6;border-left:9.4px solid #000}
#printSheet h2 small{font-weight:400;font-size:11.3px;margin-left:7.6px}
#printSheet table{width:100%;table-layout:fixed;border-collapse:collapse;page-break-inside:avoid}
#printSheet td.n{width:34px;text-align:center;padding-top:3.8px}
#printSheet td{border:.8px solid #666;padding:2px 5.3px;vertical-align:top}
#printSheet td.n{width:22.7px;text-align:center;font-weight:700}
#printSheet td.q{width:37.8px;text-align:center;font-size:8px;color:#333;padding:3px}
#printSheet td.q svg{width:34px;height:34px;display:block;margin:0 auto}
#printSheet td.d{width:60.5px;text-align:right;white-space:nowrap}
#printSheet .ps-nm{font-weight:700;font-size:13.3px;color:#000;line-height:1.3}
#printSheet .ps-sm{font-size:10.7px;color:#222;line-height:1.3}
#printSheet .ps-fl{display:inline-block;border:.8px solid #000;border-radius:3.8px;padding:0 4.5px;font-size:10.7px;margin-top:1.5px;line-height:1.35}
#printSheet .ps-fl.ng{background:#000;color:#fff}
#printSheet .ps-none{font-size:12px;color:#444;padding:3.8px 0}
#printSheet,#printSheet *{-webkit-print-color-adjust:exact;print-color-adjust:exact}
#printSheet .ps-mapbox{position:relative;width:680px;overflow:hidden;border:1.3px solid #000;background:#eee}
#printSheet .ps-tile{position:absolute;width:256px;height:256px;max-width:none}
#printSheet .ps-ov{position:absolute;left:0;top:0}
#printSheet .ps-pin{position:absolute;transform:translate(-50%,-50%);white-space:nowrap}
#printSheet .ps-mk{display:inline-block;border:1.4px solid #000;border-radius:9px;padding:0 4px;font-size:11.3px;font-weight:800;line-height:1.35;background:#fff;color:#000}
#printSheet .ps-g避{background:#cfe0ff} #printSheet .ps-g緊{background:#ffe0b0} #printSheet .ps-g水{background:#c8f0ff} #printSheet .ps-g福{background:#f1d4f5}
#printSheet .ps-home{color:#d00;font-size:29.3px;line-height:1;-webkit-text-stroke:1.2px #fff;text-shadow:0 0 2px #000}
#printSheet .ps-legend .ps-home{font-size:16px}
#printSheet .ps-homepin{z-index:3}
#printSheet .ps-edge{z-index:2}
#printSheet .ps-edge .ps-mk{border-style:dashed}
#printSheet .ps-scale{position:absolute;left:10px;bottom:10px;background:rgba(255,255,255,.9);padding:2px 5px;font-size:10.7px;font-weight:700}
#printSheet .ps-scale div{height:5px;border:1.5px solid #000;border-top:0;margin-bottom:1px}
#printSheet .ps-north{position:absolute;right:10px;top:8px;background:rgba(255,255,255,.9);padding:2px 6px;text-align:center;font-size:12px;font-weight:800;line-height:1.1}
#printSheet .ps-attr{position:absolute;right:4px;bottom:3px;font-size:8.7px;background:rgba(255,255,255,.85);padding:0 3px}
#printSheet .ps-legend{font-size:10.7px;margin-top:3.8px;line-height:1.55}
#printSheet .ps-dp{display:inline-block;width:12.1px;height:12.1px;border:1px solid #666;vertical-align:-2px;margin:0 3px 0 5.3px}
#printSheet .ps-fld{opacity:.62}
#printSheet .ps-legend .ps-mk{font-size:10px;margin:0 2px 0 0}
#printSheet td.n .ps-mk{font-size:10.7px}
#printSheet .ps-head{display:flex;align-items:baseline;gap:15.1px;flex-wrap:wrap;margin-bottom:5.7px}
#printSheet .ps-head h1{margin:0}
#printSheet .ps-head .ps-sub{margin:0}
#printSheet .ps-head{align-items:center}
#printSheet .ps-qrh{margin-left:auto;display:flex;align-items:center;gap:4px;font-size:9.3px;line-height:1.25}
#printSheet .ps-qrh svg{width:46px;height:46px;display:block}
#printSheet .ps-row2{display:flex;gap:15.1px}
#printSheet .ps-row2 .ps-row{flex:1}
#printSheet .ps-top{padding:5.7px 11.3px;margin-bottom:7.6px}
#printSheet .ps-lists{columns:2;column-gap:18.9px;margin-top:3.8px}
#printSheet .ps-it,#printSheet h2{break-inside:avoid;page-break-inside:avoid}
#printSheet h2{break-after:avoid}
#printSheet .ps-sec+.ps-sec{margin-top:6px}
#printSheet .ps-it{display:flex;gap:6px;align-items:flex-start;border-bottom:1px solid #999;padding:4px 0}
#printSheet .ps-it>.ps-mk{flex:none;margin-top:2px}
#printSheet .ps-tx{flex:1;min-width:0}
#printSheet .ps-iq{flex:none;width:37.8px}
#printSheet .ps-iq svg{width:37.8px;height:37.8px;display:block}
#printSheet .ps-d{float:right;font-weight:700;font-size:12px;margin-left:7.6px}
#printSheet .ps-foot{margin-top:5.7px;font-size:9.7px;line-height:1.35;color:#222;border-top:.8px solid #000;padding-top:5.7px}

/* 文字を大きく（見やすさ優先） */
#printSheet h1{font-size:24px}
#printSheet .ps-sub{font-size:14px}
#printSheet h2{font-size:16.5px;padding:3px 8px}
#printSheet h2 small{font-size:13px}
#printSheet .ps-nm{font-size:16.5px;line-height:1.3}
#printSheet .ps-d{font-size:15px}
#printSheet .ps-sm{font-size:13px;line-height:1.35}
#printSheet .ps-fl{font-size:13px}
#printSheet .ps-none{font-size:14px}
#printSheet .ps-mk{font-size:13.5px;padding:0 5px}
#printSheet .ps-legend{font-size:12.5px}
#printSheet .ps-legend .ps-mk{font-size:12px}
#printSheet .ps-foot{font-size:11.5px;line-height:1.4}
#printSheet .ps-scale{font-size:12.5px}
#printSheet .ps-north{font-size:14px}
#printSheet .ps-iq,#printSheet .ps-iq svg{width:44px;height:44px}
#printSheet .ps-qrh{font-size:11px}
#printSheet .ps-qrh svg{width:54px;height:54px}
#printSheet .ps-home{font-size:34px}

#printSheet .ps-depth{display:flex;align-items:center;gap:8px;border:1.6px solid #000;border-radius:4px;padding:4px 10px;margin:0 0 6px;font-size:14.5px;line-height:1.35}
#printSheet .ps-depth i,.lvdepth i{display:inline-block;width:18px;height:14px;border:1px solid #666;flex:none;vertical-align:-2px}
#printSheet .ps-depth small{font-size:12.5px;color:#222}
.lvdepth{border:1.5px solid #888;border-radius:8px;padding:8px 10px;margin:0 0 8px;font-size:14px;line-height:1.5;background:#fff}
.lvdepth small{display:block;font-size:12px;color:#555;margin-top:2px}
#printSheet .ps-in{width:680px;margin:0 auto}
@media print{body.printing #printSheet{padding-top:12mm}}
@media print and (min-width:780px){body.printing #printSheet{padding:17mm 15mm 12mm}}
@media print and (max-width:680px){body.printing #printSheet{zoom:0.971}}
@media print and (max-width:660px){body.printing #printSheet{zoom:0.941}}
@media print and (max-width:640px){body.printing #printSheet{zoom:0.912}}
@media print and (max-width:620px){body.printing #printSheet{zoom:0.882}}
@media print and (max-width:600px){body.printing #printSheet{zoom:0.853}}
@media print and (max-width:580px){body.printing #printSheet{zoom:0.824}}
@media print and (max-width:560px){body.printing #printSheet{zoom:0.794}}
@media print and (max-width:540px){body.printing #printSheet{zoom:0.765}}
@media print and (max-width:520px){body.printing #printSheet{zoom:0.735}}
@media print and (max-width:500px){body.printing #printSheet{zoom:0.706}}
@media print and (max-width:480px){body.printing #printSheet{zoom:0.676}}
@media print and (max-width:460px){body.printing #printSheet{zoom:0.647}}
@media print and (max-width:440px){body.printing #printSheet{zoom:0.618}}
@media print and (max-width:420px){body.printing #printSheet{zoom:0.588}}
@media print and (max-width:400px){body.printing #printSheet{zoom:0.559}}
@media print and (max-width:380px){body.printing #printSheet{zoom:0.529}}
@media print and (max-width:360px){body.printing #printSheet{zoom:0.500}}
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
 const flT=s=>{ if(s.flood==="up") return ["水害時は "+(s.fl||"上の階")+" へ",""]; if(s.flood==="no") return ["水害時は使えない","ng"]; if(s.flood==="ok") return ["水害時 1階から可",""]; return ["水害時：情報なし",""]; };
 const nt=(s,g)=>{ let t=String(s.note||"").replace(/・収容.*$/,""); if(g[3]==="福") t=t.replace(/被害が大きく避難生活が長引くときに市が開設/,"").replace(/^[・、\s]+/,""); return t?"　※"+E(t):""; };
 const FOK=s=>s.flood==="ok"||s.flood==="up";
 const bc=((isAddr&&String(base).replace(/^.+?[都道府県]/,"").match(/^(.+?[市町村])/))||[])[1]||(list[0]&&list[0].city)||"";
 const G=[["まず逃げる場所","指定緊急避難場所",isEmg,"緊"],
          ["寝泊まりする場所","指定避難所",s=>s.kind==="K"||s.kind==="H","避"],
          ["福祉避難所",`${bc}の要配慮者向け・状況に応じて開設`,s=>s.kind==="F"&&s.city===bc,"福"]];
 const key=s=>s.name+"|"+s.addr, top=g=>list.filter(g[2]).slice(0,N);
 const shown=new Set(); [G[0],G[1]].forEach(g=>top(g).forEach(s=>shown.add(key(s))));
 const needF=[G[0],G[1]].some(g=>top(g).some(s=>s.flood==="no"));
 if(needF&&list.some(s=>"KHQP".includes(s.kind)&&FOK(s)&&!shown.has(key(s))))
  G.splice(2,0,["水害のときの避難先","洪水でも使える施設",s=>"KHQP".includes(s.kind)&&FOK(s)&&!shown.has(key(s)),"水"]);
 const marks=[];
 const items=(g,n)=>{ const L=list.filter(g[2]).slice(0,n||N); if(!L.length) return g[3]==="福"?`<div class="ps-none">${E(bc)}の福祉避難所は公開データに載っていません。要配慮の方は、事前に市町村（福祉・防災の担当課）か担当のケアマネジャーに確認してください。</div>`:'<div class="ps-none">この周辺には登録がありません。</div>';
  return L.map((s,i)=>{ const f=flT(s), lb=g[3]+(i+1); marks.push({lat:s.lat,lng:s.lng,lb:lb,g:g[3],nm:s.name,d:s._d,fl:f[0]});
   const both=g[3]==="緊"&&(s.kind==="K"||s.kind==="H")?"（避難所も兼ねる）":"";
   return `<div class="ps-it"><span class="ps-mk ps-g${g[3]}">${lb}</span><div class="ps-tx"><div class="ps-nm">${E(s.name)}<span class="ps-d">約${_FD(s._d)}</span></div><div class="ps-sm">${E(s.city+s.addr)}${s.tel?"　☎"+E(s.tel):""}${both}</div><div class="ps-sm"><span class="ps-fl ${f[1]}">${f[0]}</span>${nt(s,g)}</div></div><div class="ps-iq">${qrSvg(`https://www.google.com/maps/dir/?api=1&destination=${s.lat},${s.lng}`)}</div></div>`; }).join(""); };
 const lists=G.map(g=>`<div class="ps-sec"><h2>${g[0]}<small>${g[1]}</small></h2>`+items(g,(G.length>3&&g[3]==="福")?2:N)+`</div>`).join("");
 const hz=qrSvg(`https://disaportal.gsi.go.jp/maps/index.html?ll=${lat},${lng}&z=16`);
 const el=document.getElementById("printSheet")||document.body.appendChild(Object.assign(document.createElement("div"),{id:"printSheet"}));
 el.innerHTML=`<div class="ps-in"><div class="ps-head"><h1>避難先マップ</h1><div class="ps-sub">${isAddr?`基準：<b>${E(base)}</b>`:`基準：現在地（${lat.toFixed(5)}, ${lng.toFixed(5)}）`}　作成日：${ds}</div>${hz?`<div class="ps-qrh">${hz}<span>ハザード<br>マップ</span></div>`:""}</div>
 <div class="ps-depth" id="psDepth" style="display:none"></div>
 <div class="ps-mapbox" id="psMapbox" style="height:${G.length>3?310:380}px"></div>
 <div class="ps-legend"><span class="ps-home">★</span>${isAddr?"この住所":"現在地"}　<span class="ps-mk ps-g緊">緊</span>まず逃げる場所　<span class="ps-mk ps-g避">避</span>寝泊まりする場所${G.some(g=>g[3]==="水")?'　<span class="ps-mk ps-g水">水</span>水害のときの避難先':""}　<span class="ps-mk ps-g福">福</span>福祉避難所　<span style="color:#c00">点線の円</span>＝直線500m・1km　地図の外の施設は縁に方向（→）と距離<br><b>洪水で浸かる深さ（想定最大規模・全河川の重ね合わせ）：</b><span class="ps-dp" style="background:#f7f5a9"></span>0.5m未満 <span class="ps-dp" style="background:#ffd8c0"></span>0.5〜3m（1階が浸かる） <span class="ps-dp" style="background:#ffb7b7"></span>3〜5m（2階まで） <span class="ps-dp" style="background:#ff9191"></span>5〜10m <span class="ps-dp" style="background:#f285c9"></span>10m以上</div>
 <div class="ps-lists">${lists}</div>
 <div class="ps-foot">距離は直線です。浸水や通行止めで通れない道もあります。どこが開くかは災害ごとに違うので、市町村の避難情報を確認してください。「水害時は使えない」場所には洪水のとき行かないこと。右のQRをスマホで読むと道案内が開きます。<br>出典：国土地理院 指定緊急避難場所・指定避難所データ${asof?"（"+E(asof)+"）":""}・各市町の避難所資料・地理院タイル（埼玉 避難所ナビ）</div></div>`;
 fillDepth(lat,lng,isAddr);
 drawMap(document.getElementById("psMapbox"),lat,lng,marks,onReady,G.length>3?310:380);
 showLive(lat,lng,marks,isAddr);
}
function drawMap(box,lat,lng,marks,onReady,H){
 const W=680,PAD=24,T=256; H=H||440;
 const wx=(ln,z)=>(ln+180)/360*T*2**z, wy=(la,z)=>{const r=la*Math.PI/180;return (1-Math.log(Math.tan(r)+1/Math.cos(r))/Math.PI)/2*T*2**z;};
 const M=marks.filter(m=>m.lat&&m.lng).map(m=>Object.assign({d:distM(lat,lng,m.lat,m.lng)},m));
 // 一番近い「まず逃げる場所」「寝泊まりする場所」と、700m以内の施設が入る、いちばん詳しい縮尺。中心は基準地点。
 const byD=M.slice().sort((a,b)=>a.d-b.d);
 let fit=["緊","避"].flatMap(g=>byD.filter(m=>m.g===g).slice(0,1)).concat(byD.filter(m=>m.d<=700)).filter(m=>m.d<=1500);
 if(!fit.length) fit=byD.slice(0,2);
 let z=17;
 for(;z>13;z--){ const cx=wx(lng,z), cy=wy(lat,z);
  if(fit.every(m=>Math.abs(wx(m.lng,z)-cx)<=W/2-PAD&&Math.abs(wy(m.lat,z)-cy)<=H/2-PAD)) break; }
 const ox=wx(lng,z)-W/2, oy=wy(lat,z)-H/2;
 let html="", n=0;
 for(let tx=Math.floor(ox/T);tx<=Math.floor((ox+W)/T);tx++) for(let ty=Math.floor(oy/T);ty<=Math.floor((oy+H)/T);ty++){ n++;
  html+=`<img class="ps-tile" alt="" style="left:${(tx*T-ox).toFixed(1)}px;top:${(ty*T-oy).toFixed(1)}px" src="https://cyberjapandata.gsi.go.jp/xyz/std/${z}/${tx}/${ty}.png"><img class="ps-tile ps-fld" alt="" style="left:${(tx*T-ox).toFixed(1)}px;top:${(ty*T-oy).toFixed(1)}px" src="https://disaportaldata.gsi.go.jp/raster/01_flood_l2_shinsuishin_data/${z}/${tx}/${ty}.png">`; n++; }
 const bx=W/2, by=H/2, mpp=156543.03392*Math.cos(lat*Math.PI/180)/2**z;
 html+=`<svg class="ps-ov" width="${W}" height="${H}">`+[500,1000].map(m=>{const r=m/mpp,ang=-0.6;return `<circle cx="${bx}" cy="${by}" r="${r}" fill="none" stroke="#c00" stroke-width="1.6" stroke-dasharray="6 5"/><text x="${bx+r*Math.cos(ang)+3}" y="${by+r*Math.sin(ang)-3}" font-size="12" font-weight="700" fill="#c00" stroke="#fff" stroke-width="3" paint-order="stroke">${m<1000?m+"m":"1km"}</text>`;}).join("")+`</svg>`;
 const AR=["→","↘","↓","↙","←","↖","↑","↗"], fmt=m=>m<1000?Math.round(m/10)*10+"m":(m/1000).toFixed(1)+"km";
 const groups=[], edge=[];
 M.forEach(m=>{ const x=wx(m.lng,z)-ox, y=wy(m.lat,z)-oy;
  if(x<PAD/2||x>W-PAD/2||y<PAD/2||y>H-PAD/2){ // 地図の外：縁に方向と距離を出す
   const dx=x-bx, dy=y-by, k=Math.min((W/2-30)/Math.abs(dx||1e-9),(H/2-14)/Math.abs(dy||1e-9));
   const ex=bx+dx*k, ey=Math.min(Math.max(by+dy*k,12),H-12), a=Math.round(((Math.atan2(dy,dx)*180/Math.PI)+360)%360/45)%8;
   const same=edge.find(q=>Math.hypot(q.lat-m.lat,q.lng-m.lng)<1e-5); if(same){same.lb.push(m.lb);return;}
   let ny=ey; while(edge.some(q=>Math.abs(q.x-ex)<110&&Math.abs(q.y-ny)<17)) ny+=(ey>H/2?-17:17);
   edge.push({x:ex,y:ny,lb:[m.lb],g:m.g,ar:AR[a],d:m.d,lat:m.lat,lng:m.lng});
   return; }
  const g=groups.find(q=>Math.hypot(q.x-x,q.y-y)<14); if(g){g.lb.push(m.lb);} else groups.push({x:x,y:y,lb:[m.lb],g:m.g}); });
 groups.forEach(q=>{ html+=`<div class="ps-pin" style="left:${q.x.toFixed(1)}px;top:${q.y.toFixed(1)}px"><span class="ps-mk ps-g${q.g}">${q.lb.join("・")}</span></div>`; });
 edge.forEach(q=>{ let st;
  if(q.x<=40) st=`left:4px;top:${q.y.toFixed(1)}px;transform:translate(0,-50%)`;
  else if(q.x>=W-40) st=`right:4px;top:${q.y.toFixed(1)}px;transform:translate(0,-50%)`;
  else st=`left:${Math.min(Math.max(q.x,70),W-70).toFixed(1)}px;top:${q.y.toFixed(1)}px`;
  html+=`<div class="ps-pin ps-edge" style="${st}"><span class="ps-mk ps-g${q.g}">${q.lb.join("・")} ${q.ar}${fmt(q.d)}</span></div>`; });
 html+=`<div class="ps-pin ps-homepin" style="left:${bx}px;top:${by}px"><span class="ps-home">★</span></div>`;
 const nice=[50,100,200,500,1000,2000].find(m=>m/mpp>=80)||2000, bl=nice/mpp;
 html+=`<div class="ps-scale"><div style="width:${bl.toFixed(0)}px"></div>${nice<1000?nice+"m":nice/1000+"km"}</div><div class="ps-north">▲<br>北</div><div class="ps-attr">地理院タイル（標準地図・洪水浸水想定区域［想定最大規模］）</div>`;
 box.innerHTML=html;
 let left=n, fired=false; const fin=()=>{ if(!fired){ fired=true; onReady&&onReady(); } };
 box.querySelectorAll("img").forEach(im=>{ const d=()=>{ if(--left<=0) fin(); }; if(im.complete) d(); else { im.onload=d; im.onerror=d; } });
 setTimeout(fin,8000);
}
function addPrintBtns(box,lat,lng,base,list,isAddr){
 const w=document.createElement("div"); w.className="printbtns";
 const mk=t=>{const b=document.createElement("button");b.type="button";b.className="printbtn";b.textContent=t;b.disabled=true;w.appendChild(b);return b;};
 const bImg=mk("🗺 地図を準備中…"), bPdf=mk("📄 PDFで保存"), bPr=mk("🖨 印刷する");
 bImg.classList.add("main");
 const fname=(isAddr?String(base).replace(/^.+?[都道府県]/,""):"現在地")+"_避難先マップ";
 const hint=document.createElement("div"); hint.className="printhint"; hint.textContent="画像で保存しておくと、電波がないときもスマホの写真から見られます。";
 const lv=document.createElement("div"); lv.id="psLiveWrap"; lv.innerHTML='<div id="psDepthLive" class="lvdepth" style="display:none"></div><div id="psLive"></div><div class="lvbar"><label><input type="checkbox" id="psFld" checked> 洪水で浸かる深さを重ねる</label><span class="lvlg"><i style="background:#f7f5a9"></i>0.5m未満<i style="background:#ffd8c0"></i>〜3m<i style="background:#ffb7b7"></i>〜5m<i style="background:#ff9191"></i>〜10m<i style="background:#f285c9"></i>10m〜</span></div>';
 box.appendChild(lv); box.appendChild(w); box.appendChild(hint);
 const ready=()=>{ bImg.disabled=bPdf.disabled=bPr.disabled=false; bImg.textContent="📷 画像で保存（スマホ向け）"; };
 bImg.onclick=()=>makeFile(bImg,"png",fname,"📷 画像で保存（スマホ向け）");
 bPdf.onclick=()=>makeFile(bPdf,"pdf",fname,"📄 PDFで保存");
 bPr.onclick=()=>doPrint();
 const build=()=>{ buildSheet(lat,lng,base,list,isAddr,ready); w._file=null; };
 build();
 if(!window.qrcode&&QRLIB) QRLIB.addEventListener("load",build,{once:true});
}
/* ===== この地点の想定浸水深（重ねている浸水マップの色をその地点で読む） ===== */
const DEPTHS=[[[247,245,169],"0.5m未満","床下が浸かるていど","水が引くまで家の2階で待つこともできる場合があります。早めに情報を確認。"],
 [[255,216,192],"0.5〜3m","1階が浸かる","1階は危険。2階以上か、「水害時OK」の避難先へ。"],
 [[255,183,183],"3〜5m","2階の床まで浸かる","2階でも危険。早めに浸からない場所へ逃げてください。"],
 [[255,145,145],"5〜10m","2階まで浸かる","家にとどまるのは危険。早めに浸からない場所へ逃げてください。"],
 [[242,133,201],"10m以上","3階以上まで浸かる","家にとどまるのは危険。早めに浸からない場所へ逃げてください。"],
 [[220,122,220],"20m以上","5階以上まで浸かる","家にとどまるのは危険。早めに浸からない場所へ逃げてください。"]];
const _DEP={};
function floodAt(lat,lng){
 const k=lat.toFixed(5)+","+lng.toFixed(5); if(_DEP[k]) return _DEP[k];
 const z=17,n=1<<z,xf=(lng+180)/360*n,r=lat*Math.PI/180,yf=(1-Math.log(Math.tan(r)+1/Math.cos(r))/Math.PI)/2*n;
 const tx=Math.floor(xf),ty=Math.floor(yf),px=Math.min(255,Math.floor((xf-tx)*256)),py=Math.min(255,Math.floor((yf-ty)*256));
 const url=`https://disaportaldata.gsi.go.jp/raster/01_flood_l2_shinsuishin_data/${z}/${tx}/${ty}.png`;
 return _DEP[k]=fetch(url,{mode:"cors"}).then(res=>{
  if(res.status===404) return {none:true};
  if(!res.ok) return null;
  return res.blob().then(b=>new Promise((ok,ng)=>{const im=new Image();im.crossOrigin="anonymous";im.onload=()=>ok(im);im.onerror=ng;im.src=URL.createObjectURL(b);})).then(im=>{
   const c=document.createElement("canvas");c.width=c.height=256;const x=c.getContext("2d");x.drawImage(im,0,0);
   const d=x.getImageData(px,py,1,1).data; if(d[3]<40) return {none:true};
   let best=-1,bd=1e9; DEPTHS.forEach((q,i)=>{const e=(q[0][0]-d[0])**2+(q[0][1]-d[1])**2+(q[0][2]-d[2])**2;if(e<bd){bd=e;best=i;}});
   return bd<2500?{i:best}:null;
  });
 }).catch(()=>null);
}
function depthHTML(r,isAddr,sheet){
 const where=isAddr?"この住所":"現在地";
 if(!r) return "";
 if(r.none) return `<span>★<b>${where}の洪水の深さ（想定最大）：浸水の想定なし</b>${sheet?"　":"<br>"}<small>大きな川があふれたときの想定です。小さな川・用水路や大雨で水がたまる浸水は含みません。</small></span>`;
 const q=DEPTHS[r.i];
 return `<i style="background:rgb(${q[0].join(",")})"></i><span>★<b>${where}の洪水の深さ（想定最大）：${q[1]}（${q[2]}）</b>${sheet?"　":"<br>"}<small>${q[3]}</small></span>`;
}
function fillDepth(lat,lng,isAddr){
 floodAt(lat,lng).then(r=>{
  [["psDepth",true],["psDepthLive",false]].forEach(([id,sh])=>{const e=document.getElementById(id);if(!e)return;const h=depthHTML(r,isAddr,sh);e.innerHTML=h;e.style.display=h?"":"none";});
  if(typeof fitSheet==="function") fitSheet();
 });
}
let LVMAP=null;
function showLive(lat,lng,marks,isAddr){
 const box=document.getElementById("psLive"); if(!box) return;
 const go=()=>{
  if(LVMAP){ LVMAP.remove(); LVMAP=null; }
  const m=L.map(box,{scrollWheelZoom:false,tap:true}); LVMAP=m;
  L.tileLayer("https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png",{maxZoom:18,attribution:'<a href="https://maps.gsi.go.jp/development/ichiran.html" target="_blank">地理院タイル</a>'}).addTo(m);
  const fl=L.tileLayer("https://disaportaldata.gsi.go.jp/raster/01_flood_l2_shinsuishin_data/{z}/{x}/{y}.png",{maxNativeZoom:17,maxZoom:18,opacity:.6,attribution:"洪水浸水想定区域（想定最大規模）"}).addTo(m);
  const cb=document.getElementById("psFld"); if(cb) cb.onchange=()=>{ cb.checked?fl.addTo(m):m.removeLayer(fl); };
  [500,1000].forEach(r=>L.circle([lat,lng],{radius:r,color:"#c00",weight:1.6,dashArray:"6 5",fill:false,interactive:false}).addTo(m));
  L.marker([lat,lng],{icon:L.divIcon({className:"",html:'<span class="lvhome">★</span>',iconSize:[26,26],iconAnchor:[13,13]}),zIndexOffset:1000}).addTo(m)
   .bindPopup(isAddr?"この住所":"現在地");
  const seen=[];
  marks.filter(x=>x.lat&&x.lng).forEach(x=>{
   const k=seen.find(q=>Math.abs(q.lat-x.lat)<1e-5&&Math.abs(q.lng-x.lng)<1e-5);
   const pop=`<b>${x.lb}　${x.nm}</b><br>約${_FD(x.d)}（直線）・${x.fl}<br><a href="https://www.google.com/maps/dir/?api=1&destination=${x.lat},${x.lng}" target="_blank" rel="noopener">▶ ここへ行く（ルート）</a>`;
   if(k){ k.mk.setIcon(L.divIcon({className:"",html:`<span class="lvmk lv${k.g}">${k.lbs.concat(x.lb).join("・")}</span>`,iconSize:null})); k.lbs.push(x.lb); k.mk.bindPopup(k.mk.getPopup().getContent()+"<hr style='margin:4px 0'>"+pop); return; }
   const mk=L.marker([x.lat,x.lng],{icon:L.divIcon({className:"",html:`<span class="lvmk lv${x.g}">${x.lb}</span>`,iconSize:null})}).addTo(m).bindPopup(pop);
   seen.push({lat:x.lat,lng:x.lng,g:x.g,lbs:[x.lb],mk:mk});
  });
  const near=marks.filter(x=>x.lat&&(x.d<=700||["緊1","避1"].includes(x.lb))&&x.d<=1500).map(x=>[x.lat,x.lng]);
  m.fitBounds(L.latLngBounds([[lat,lng]].concat(near)).pad(0.15),{maxZoom:17});
  setTimeout(()=>m.invalidateSize(),60);
 };
 if(window.L) return go();
 const css=document.createElement("link"); css.rel="stylesheet"; css.href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css"; document.head.appendChild(css);
 loadJS("https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js").then(go).catch(()=>{ box.innerHTML='<div style="padding:12px;color:#a33;font-size:13px">地図を読み込めませんでした（通信状況を確認してください）。</div>'; });
}
function loadJS(u){ return new Promise((ok,ng)=>{ const e=[...document.scripts].find(x=>x.src===u); if(e&&e._ok) return ok(); const s=e||document.createElement("script");
 s.src=u; s.addEventListener("load",()=>{s._ok=true;ok();}); s.addEventListener("error",ng); if(!e) document.head.appendChild(s); }); }
async function sheetCanvas(){
 const el=document.getElementById("printSheet"), inn=el.querySelector(".ps-in"); const keep=el.style.cssText, kz=inn.style.zoom;
 inn.style.zoom=""; el.style.cssText+=";display:block;position:absolute;left:0;top:0;z-index:-5;background:#fff;width:720px";
 try{
  await loadJS("https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js");
  return await html2canvas(inn,{scale:2,useCORS:true,backgroundColor:"#ffffff",logging:false,windowWidth:760,scrollX:0,scrollY:0});
 } finally { el.style.cssText=keep; inn.style.zoom=kz; }
}
async function makeFile(btn,type,fname,label){
 // 1回目のタップで作成、2回目のタップで保存（スマホは「タップ直後」でないと保存画面を出せないため）
 if(btn._blob){ saveBlob(btn._blob,fname+"."+type); return; }
 btn.disabled=true; btn.textContent=type==="png"?"📷 画像を作成中…":"📄 PDFを作成中…";
 try{
  const c0=await sheetCanvas(); let blob;
  // A4の紙に余白(左右15mm・上下16mm)を付けた画像にする。プリンターの印刷できない端で切れないように。
  const c=(()=>{const W=Math.round(c0.width*210/180),H=Math.round(W*297/210),m=W*15/210,t=W*16/210,aw=W-2*m,ah=H-2*t;
   let w=aw,h=c0.height*aw/c0.width; if(h>ah){h=ah;w=c0.width*ah/c0.height;}
   const k=document.createElement("canvas");k.width=W;k.height=H;const x=k.getContext("2d");x.fillStyle="#fff";x.fillRect(0,0,W,H);x.drawImage(c0,(W-w)/2,t,w,h);return k;})();
  if(type==="png"){ blob=await new Promise(r=>c.toBlob(r,"image/png")); }
  else{ await loadJS("https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js");
   const pdf=new window.jspdf.jsPDF({unit:"mm",format:"a4"}); pdf.addImage(c.toDataURL("image/jpeg",0.92),"JPEG",0,0,210,297); blob=pdf.output("blob"); }
  btn._blob=blob; btn.disabled=false; btn.classList.add("ready");
  btn.textContent=(type==="png"?"✅ 画像ができました → タップして保存":"✅ PDFができました → タップして保存");
 }catch(e){ btn.disabled=false; btn.textContent=label+"（もう一度）"; alertMsg("作成に失敗しました。通信状況を確認して、もう一度お試しください。"); }
}
function alertMsg(t){ const d=document.querySelector(".printhint"); if(d){ d.textContent="⚠ "+t; d.style.color="#a33"; } }
async function saveBlob(blob,name){
 // パソコン（Chrome・Edge）は「名前を付けて保存」の画面で保存先を選べるようにする
 if(window.showSaveFilePicker&&!/Android|iPhone|iPad|iPod/i.test(navigator.userAgent)){
  try{ const pdf=blob.type==="application/pdf";
   const hnd=await showSaveFilePicker({suggestedName:name,types:[{description:pdf?"PDF":"画像",accept:pdf?{"application/pdf":[".pdf"]}:{"image/png":[".png"]}}]});
   const w=await hnd.createWritable(); await w.write(blob); await w.close();
   if(pdf){ const u=URL.createObjectURL(blob); window.open(u,"_blank"); setTimeout(()=>URL.revokeObjectURL(u),60000); }
   return; }catch(e){ if(e&&e.name==="AbortError") return; }
 }
 const f=new File([blob],name,{type:blob.type});
 if(navigator.canShare&&navigator.canShare({files:[f]})){ try{ await navigator.share({files:[f],title:name}); return; }catch(e){ if(e&&e.name==="AbortError") return; } }
 const a=document.createElement("a"); a.href=URL.createObjectURL(blob); a.download=name; document.body.appendChild(a); a.click();
 setTimeout(()=>{ URL.revokeObjectURL(a.href); a.remove(); },5000);
}
function fitSheet(){
 // 内側(.ps-in, 幅680px)の高さを測り、A4の印刷範囲の縦横比（端末で余白が違うので小さい方）に収まるよう縮める。
 const el=document.getElementById("printSheet"); if(!el) return; const inn=el.querySelector(".ps-in"); if(!inn) return;
 inn.style.zoom=""; const keep=el.style.cssText;
 el.style.cssText+=";display:block;position:absolute;left:-10000px;top:0;visibility:hidden;zoom:1";
 const h=inn.scrollHeight, lim=680*1.36;
 el.style.cssText=keep;
 if(h>lim) inn.style.zoom=(lim/h).toFixed(3);
}
function doPrint(){
 fitSheet();
 document.body.classList.add("printing");
 const done=()=>{ document.body.classList.remove("printing"); window.removeEventListener("afterprint",done); };
 window.addEventListener("afterprint",done);
 window.print(); setTimeout(done,2000);
}
"""


ONESHARE = r'''
/* ===== 各施設カードの送るボタンを「📤 送る」1つに ===== */
(function(){
 function one(){
  document.querySelectorAll(".card .share:not(.one)").forEach(d=>{
   d.classList.add("one"); const bs=[...d.querySelectorAll("button")];
   const nat=bs.find(b=>/SMS|他のアプリ/.test(b.textContent)), cp=bs.find(b=>/コピー/.test(b.textContent));
   bs.forEach(b=>b.style.display="none");
   const b=document.createElement("button"); b.className="sendone"; b.textContent=nat?"📤 送る":"📤 送る（コピー）";
   b.onclick=e=>{e.stopPropagation(); (nat||cp).click(); if(!nat){const o=b.textContent;b.textContent="✓ コピーしました";setTimeout(()=>b.textContent=o,1500);}};
   d.appendChild(b);
  });
 }
 let q=false; new MutationObserver(()=>{if(q)return;q=true;requestAnimationFrame(()=>{q=false;one();});}).observe(document.body,{childList:true,subtree:true});
 one();
})();
'''

DOCJS = r'''
/* ===== 市町の公式資料（ハザードマップ・避難所一覧）へのリンク ===== */
(function(){
 if(typeof CITYDOCS==="undefined"||typeof tabsEl==="undefined") return;
 const box=document.createElement("div"); box.id="cityDocs"; tabsEl.insertAdjacentElement("afterend",box);
 const show=()=>{ const L=CITYDOCS[city]||[];
  box.innerHTML=L.length?`📄 <b>${city}の公式資料</b>：`+L.map(d=>`<a href="${d[1]}" target="_blank" rel="noopener">${d[0]}</a>`).join("　"):"";
  box.style.display=L.length?"":"none"; };
 const orig=render; render=function(){ const r=orig.apply(this,arguments); show(); return r; };
 show();
})();
'''

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


def patch(path, detail=None, docs=None):
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
    js = js + ONESHARE
    if docs:
        js = 'const CITYDOCS=' + json.dumps(docs, ensure_ascii=False) + ';\n' + js + DOCJS
    if detail:
        js = 'const DETAILURL=' + json.dumps(detail, ensure_ascii=False) + ';\n' + js
    js += ('try{const _p=new URLSearchParams(location.search),_la=parseFloat(_p.get("lat")),_ln=parseFloat(_p.get("lng"));'
           'if(isFinite(_la)&&isFinite(_ln))setTimeout(()=>_GPS(_la,_ln,null,_p.get("label")||"指定した地点"),60);}catch(e){}\n')
    i = h.rfind('</script>'); assert i > 0
    h = h[:i] + js + h[i:]
    open(path, 'w', encoding='utf-8').write(h)
    return 'patched'


def docs_map():
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import watch
    d = {}
    for label, url, _ in watch.PDFS:
        c, _, t = label.partition(' ')
        d.setdefault(c, []).append([t or label, url])
    return d


if __name__ == '__main__':
    for p in sys.argv[1:]:
        print(p.split('/')[-1], patch(p, docs=docs_map()))
