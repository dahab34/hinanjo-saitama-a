# -*- coding: utf-8 -*-
"""エリア索引ページ（hinanjo-areas.html）とエリア版へのディープリンク対応。"""
import json, re
from urllib.parse import quote
K='https://dahab34.github.io/hinanjo/hinanjo.html'
H='https://dahab34.github.io/hinanjo/hinanjo-higashimatsuyama.html'
Q='https://dahab34.github.io/hinanjo/hinanjo-kuki.html'
# 市町の資料から作り込んだ「詳しい版」がある市町村だけ。（市町村, 何が詳しいか, [(リンク名, URL)]）
DETAIL=[
 ('鴻巣市','市のハザードマップ・避難所一覧より。丁目ごとの避難先、補助避難所、駐車場、要配慮者利用施設の一覧',[('鴻巣版で開く',K)]),
 ('北本市','市の避難所一覧より。丁目・地区名から避難先が分かる',[('鴻巣版で開く',K)]),
 ('川島町','町の避難所一覧・広域避難場所より。浸水しない階、駐車場、町外の避難先',[('鴻巣版で開く',K)]),
 ('桶川市','市の公式の避難所一覧より。全23施設の電話番号、福祉避難所',[('鴻巣版で開く',K)]),
 ('吉見町','町のハザードマップより。水害時に使える階（3階以上など）、電話番号、地区',[('鴻巣版で開く',K)]),
 ('加須市','市の水害時避難行動マップより。地域別の水害時避難場所（上階避難）、警戒レベル別タイムライン',[('鴻巣版で開く',K)]),
 ('久喜市','市のハザードマップ（令和5年3月版）より。全施設の洪水時に使える階（2階以上・3階以上など）、一時避難場所、協定締結先',[('久喜版で開く',Q)]),
 ('幸手市','市の洪水ハザードマップより。全施設の洪水時に使える階（2階以上・3階以上・使用不可）、電話番号',[('久喜版で開く',Q)]),
 ('杉戸町','町の洪水ハザードマップ（令和3年3月）より。利根川・江戸川・大落古利根川ごとの使用可否（全階・2階以上・使用不可）、電話番号、福祉避難所',[('久喜版で開く',Q)]),
 ('宮代町','町の避難所一覧より。電話番号、収容人数、消防団詰所（洪水時の階数の記載はなし）',[('久喜版で開く',Q)]),
 ('坂戸市','市の防災関連施設一覧より。災害の種類ごとの使用可否（洪水・土砂・地震・大火）、水害時は2階以上の施設、地域防災拠点・救護所、協定の福祉避難所',[('東松山版で開く',H)]),
 ('東松山市','市の公式一覧より。地区、電話番号、協定による避難先',[('東松山版で開く',H)]),
]

def deeplink(h):
    """?city=市町村名 でタブを選択、?gps=1 で現在地検索を自動開始。索引への戻りリンクも付ける。"""
    if 'URLSearchParams(location.search)' in h: return h
    h=re.sub(r'(<h1>[^<]*</h1>)',r'\1<a href="hinanjo-areas.html" style="display:inline-block;font-size:12.5px;color:var(--accent);margin:-4px 0 6px;text-decoration:none">‹ 市町村一覧にもどる</a>',h,count=1)
    i=h.rfind('render();\n</script>')
    assert i>=0,'render anchor'
    inj=('try{const _p=new URLSearchParams(location.search),_c=_p.get("city");if(_c&&CITIES.includes(_c))city=_c;}catch(e){}\n'
         'render();\n'
         'try{if(new URLSearchParams(location.search).get("gps")==="1")setTimeout(()=>document.getElementById("gps").click(),50);}catch(e){}\n')
    return h[:i]+inj+h[i+len('render();\n'):]

def make_index(areas, facs, asof_s, n_all):
    A=[{'n':a,'f':fn,'c':cs,'k':n} for a,fn,n,cs in areas]
    P={c:[[round(f['lat'],4),round(f['lng'],4)] for f in facs[c] if f['lat'] and f['lng']] for a in areas for c in a[3]}
    D=[{'c':c,'d':d,'l':[{'n':f'{c}の詳しい版を見る','u':u+'?city='+quote(c)} for n,u in ls[:1]]} for c,d,ls in DETAIL]
    J=lambda x: json.dumps(x,ensure_ascii=False,separators=(',',':'))
    return f'''<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>埼玉 避難所ナビ</title>
<style>
:root{{--bg:#f6f7f9;--card:#fff;--ink:#1c2530;--sub:#5b6573;--line:#e3e7ec;--accent:#2b5d8a;--accentbg:#eaf1f8;--star:#b6731a;--starbg:#fdf1dc}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Hiragino Kaku Gothic ProN","Hiragino Sans","Noto Sans JP","Yu Gothic UI","Yu Gothic",Meiryo,sans-serif;font-size:15px;line-height:1.55}}
.wrap{{max-width:760px;margin:0 auto;padding:16px 16px 40px}}
h1{{font-size:21px;margin:4px 0 2px}}
.meta{{color:var(--sub);font-size:13px}}
.badge{{display:inline-block;background:var(--accentbg);color:var(--accent);font-size:12px;font-weight:600;border-radius:6px;padding:2px 8px;margin-top:6px}}
.gps{{display:block;width:100%;margin:16px 0 10px;padding:15px 12px;font-size:17px;font-weight:700;color:#fff;background:var(--accent);border:0;border-radius:12px;cursor:pointer}}
.gps:disabled{{opacity:.7}}
.msg{{font-size:13px;color:#8a2a20;background:#fde8e8;border-radius:8px;padding:8px 10px;margin:0 0 10px;display:none}}
.search{{position:sticky;top:0;background:var(--bg);padding:8px 0;z-index:5}}
.search input{{width:100%;font-size:16px;padding:11px 12px;border:1px solid var(--line);border-radius:10px;background:#fff}}
.area{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 12px 10px;margin:10px 0}}
.ahead{{display:flex;justify-content:space-between;align-items:baseline;gap:8px;margin-bottom:8px}}
.ahead a{{font-weight:700;color:var(--ink);text-decoration:none;font-size:15.5px}}
.ahead span{{color:var(--sub);font-size:12px;white-space:nowrap}}
.chips{{display:flex;flex-wrap:wrap;gap:6px}}
.chip{{display:inline-flex;align-items:center;gap:4px;padding:7px 11px;border-radius:18px;border:1px solid var(--line);background:#fff;color:var(--ink);font-size:14px;text-decoration:none}}
.chip:active{{background:var(--accentbg)}}
.chip i{{font-style:normal;font-size:10.5px;font-weight:700;color:var(--star);background:var(--starbg);border-radius:4px;padding:0 4px}}
.hidden{{display:none}}
.none{{color:var(--sub);font-size:14px;padding:12px 2px;display:none}}
h2{{font-size:15px;margin:22px 0 4px}}
.lead{{color:var(--sub);font-size:12.5px;margin:0 0 6px}}
.det{{display:block;background:var(--card);border:1px solid var(--line);border-left:4px solid var(--star);border-radius:10px;padding:10px 12px;margin:8px 0;text-decoration:none;color:var(--ink)}}
.det b{{font-size:15px}} .det small{{display:block;color:var(--sub);font-size:12.5px;margin-top:3px}}
.det .ls{{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}} .det .ls a{{font-size:13px;font-weight:600;color:var(--star);background:var(--starbg);border-radius:8px;padding:5px 10px;text-decoration:none}}
.seg{{display:flex;background:#e9edf2;border-radius:10px;padding:3px;margin:0 0 4px}}
.seg button{{flex:1;border:0;background:transparent;padding:8px;font-size:14.5px;font-weight:600;color:var(--sub);border-radius:8px;cursor:pointer}}
.seg button.on{{background:#fff;color:var(--accent);box-shadow:0 1px 2px rgba(0,0,0,.08)}}
#mapwrap{{display:none;margin-top:8px}}
#map{{height:68vh;min-height:380px;border-radius:12px;border:1px solid var(--line);background:#e9edf2}}
.lg{{display:flex;flex-wrap:wrap;gap:4px 12px;font-size:12px;color:var(--sub);margin:8px 2px 0}}
.lg span::before{{content:"";display:inline-block;width:10px;height:10px;border-radius:50%;background:var(--c);margin-right:4px;vertical-align:-1px}}
.lbl{{background:#fff;border:1px solid #d5dbe3;border-radius:6px;box-shadow:0 1px 2px rgba(0,0,0,.12);font-size:12px;font-weight:700;color:#2b5d8a;padding:2px 6px;cursor:pointer}}
.lbl::before{{display:none}}
#map.lowz .lbl{{display:none}}
.pop b{{font-size:15px}} .pop a{{display:block;margin-top:6px;padding:7px 10px;border-radius:8px;text-align:center;text-decoration:none;font-weight:600;font-size:13.5px}}
.pop .p1{{background:var(--accent);color:#fff}} .pop .p2{{background:var(--starbg);color:var(--star)}}
.foot{{color:var(--sub);font-size:12px;margin-top:22px;line-height:1.7}}
</style></head>
<body><div class="wrap">
<h1>埼玉 避難所ナビ</h1>
<div class="meta">埼玉県全域＋周辺（群馬・千葉・茨城）{len(P)}市町村・{n_all:,}施設</div>
<div class="badge">データ：{asof_s}・毎月自動更新</div>

<button class="gps" id="gps" type="button">📍 今いる場所から一番近い避難所</button>
<div class="msg" id="msg"></div>

<div class="search"><div class="seg"><button id="t1" class="on" type="button">一覧</button><button id="t2" type="button">地図</button></div>
<input id="q" type="search" placeholder="市町村名で探す（例：北本、加須、さいたま）" autocomplete="off"></div>
<div id="listwrap"><div id="list"></div>
<div class="none" id="none">該当する市町村がありません。</div></div>
<div id="mapwrap"><div id="map"></div><div class="lg" id="lg"></div></div>

<h2>より詳しい版がある市町村</h2>
<p class="lead"><i style="font-style:normal;font-size:10.5px;font-weight:700;color:var(--star);background:var(--starbg);border-radius:4px;padding:0 4px">詳しい版</i> の市町村は、国土地理院データに加えて市町の資料から情報を足した版を開きます。</p>
<div id="det"></div>

<div class="foot">出典：国土地理院 指定緊急避難場所・指定避難所データ（{asof_s}）。種別・水害可否は自動判定で、上階避難の判断・協定避難先・電話番号は含みません（詳しい版を除く）。開設状況は災害ごとに変わるため、実際の避難は各市町村の防災無線・公式サイトの最新情報に従ってください。現在地検索は https:// で開いたときに使えます。</div>
</div>
<script>
const AREAS={J(A)}, PTS={J(P)}, DET={J(D)};
const detOf={{}}; DET.forEach(d=>detOf[d.c]=d);
const areaOf={{}}; AREAS.forEach(a=>a.c.forEach(c=>areaOf[c]=a));
const list=document.getElementById("list");
AREAS.forEach(a=>{{
  const box=document.createElement("div");box.className="area";
  box.innerHTML=`<div class="ahead"><a href="${{a.f}}">${{a.n}}</a><span>${{a.k.toLocaleString()}}件</span></div><div class="chips"></div>`;
  const ch=box.querySelector(".chips");
  a.c.forEach(c=>{{const e=document.createElement("a");e.className="chip";e.href=detOf[c]?detOf[c].l[0].u:`${{a.f}}?city=${{encodeURIComponent(c)}}`;
    e.dataset.c=c;e.innerHTML=c+(detOf[c]?"<i>詳しい版</i>":"");ch.appendChild(e);}});
  list.appendChild(box);
}});
document.getElementById("det").innerHTML=DET.map(d=>`<div class="det"><b>${{d.c}}</b><small>${{d.d}}</small><div class="ls">${{d.l.map(x=>`<a href="${{x.u}}">${{x.n}}</a>`).join("")}}</div></div>`).join("");
const kata=s=>s.replace(/[ァ-ン]/g,m=>String.fromCharCode(m.charCodeAt(0)-96));
const q=document.getElementById("q");
q.addEventListener("input",()=>{{
  const v=kata(q.value.trim()).replace(/[市町村]$/,"");let any=false;
  list.querySelectorAll(".area").forEach(box=>{{let n=0;
    box.querySelectorAll(".chip").forEach(e=>{{const hit=!v||e.dataset.c.includes(v);e.classList.toggle("hidden",!hit);if(hit)n++;}});
    box.classList.toggle("hidden",!n);if(n)any=true;}});
  document.getElementById("none").style.display=any?"none":"block";
}});
const COL=["#2b5d8a","#1d7a3d","#b6731a","#8e44ad","#c0392b","#16a085","#d35400","#2c3e50","#7f8c00"];
const t1=document.getElementById("t1"),t2=document.getElementById("t2"),lw=document.getElementById("listwrap"),mw=document.getElementById("mapwrap");
let map=null;
function mode(m){{t1.classList.toggle("on",m==="list");t2.classList.toggle("on",m==="map");lw.style.display=m==="list"?"":"none";mw.style.display=m==="map"?"block":"none";
  if(m==="map"){{if(!map)loadMap();else setTimeout(()=>map.invalidateSize(),50);}}}}
t1.onclick=()=>mode("list");t2.onclick=()=>mode("map");q.addEventListener("focus",()=>mode("list"));
function loadMap(){{
  const css=document.createElement("link");css.rel="stylesheet";css.href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css";document.head.appendChild(css);
  const js=document.createElement("script");js.src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js";
  js.onerror=()=>{{document.getElementById("map").innerHTML='<div style="padding:16px;color:#8a2a20">地図を読み込めませんでした（通信状況を確認してください）。一覧からお探しください。</div>';}};
  js.onload=()=>{{
    map=L.map("map",{{zoomControl:true}});
    L.tileLayer("https://cyberjapandata.gsi.go.jp/xyz/pale/{{z}}/{{x}}/{{y}}.png",{{maxZoom:18,attribution:'<a href="https://maps.gsi.go.jp/development/ichiran.html" target="_blank">国土地理院</a>'}}).addTo(map);
    const all=[];
    AREAS.forEach((a,i)=>a.c.forEach(c=>{{const p=PTS[c];if(!p||!p.length)return;
      let la=0,ln=0;p.forEach(x=>{{la+=x[0];ln+=x[1];}});la/=p.length;ln/=p.length;all.push([la,ln]);
      const dd=detOf[c], go=dd?dd.l[0].u:`${{a.f}}?city=${{encodeURIComponent(c)}}`;
      const mk=L.circleMarker([la,ln],{{radius:dd?11:9,color:"#fff",weight:2,fillColor:COL[i%COL.length],fillOpacity:.95}})
       .bindTooltip(c,{{permanent:true,interactive:true,direction:"right",offset:[7,0],className:"lbl"}})
       .on("click",()=>{{location.href=go;}}).addTo(map);
      const te=mk.getTooltip()&&mk.getTooltip().getElement();
      if(te){{te.style.pointerEvents="auto";te.addEventListener("click",e=>{{e.stopPropagation();location.href=go;}});}}
    }}));
    const z=()=>document.getElementById("map").classList.toggle("lowz",map.getZoom()<10);
    map.on("zoomend",z);map.fitBounds(all,{{padding:[16,16]}});z();
  }};
  document.head.appendChild(js);
  document.getElementById("lg").innerHTML=AREAS.map((a,i)=>`<span style="--c:${{COL[i%COL.length]}}">${{a.n}}</span>`).join("")+'<span style="--c:#999">大きい点＝詳しい版あり。点か市町村名を押すとその市町村のページへ</span>';
}}
const msg=document.getElementById("msg"),btn=document.getElementById("gps");
function show(t){{msg.textContent=t;msg.style.display="block";}}
btn.onclick=()=>{{
  if(!navigator.geolocation){{show("この端末では位置情報が使えません。市町村名で探してください。");return;}}
  btn.disabled=true;btn.textContent="📍 現在地を取得中…";msg.style.display="none";
  navigator.geolocation.getCurrentPosition(p=>{{
    const la=p.coords.latitude,ln=p.coords.longitude,r=Math.PI/180;let best=null,bd=1e18;
    for(const c in PTS)for(const [a,b] of PTS[c]){{const x=(b-ln)*Math.cos(la*r),y=a-la,d=x*x+y*y;if(d<bd){{bd=d;best=c;}}}}
    const km=Math.sqrt(bd)*111;
    if(!best||km>20){{btn.disabled=false;btn.textContent="📍 今いる場所から一番近い避難所";show("現在地の近く（約20km以内）に収録エリアの避難所がありません。");return;}}
    location.href=`${{areaOf[best].f}}?city=${{encodeURIComponent(best)}}&gps=1`;
  }},e=>{{btn.disabled=false;btn.textContent="📍 今いる場所から一番近い避難所";
    show(e.code===1?"位置情報の利用が許可されていません。設定で許可するか、市町村名で探してください。":"現在地を取得できませんでした。市町村名で探してください。");}},
  {{enableHighAccuracy:true,timeout:15000,maximumAge:60000}});
}};
</script>
</body></html>'''
