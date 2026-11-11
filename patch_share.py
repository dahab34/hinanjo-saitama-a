# -*- coding: utf-8 -*-
import sys, re
CSS = """
.share{display:flex;gap:6px;flex-wrap:wrap;margin-top:7px}
.share button{border:1px solid var(--line);background:#fff;color:var(--sub);font-size:12px;padding:4px 9px;border-radius:14px;cursor:pointer}
.share button.line{background:#06c755;border-color:#06c755;color:#fff;font-weight:600}
.share button.mail{color:var(--accent);border-color:var(--accent)}
.sharebar{margin-top:8px}
"""
JS = r"""
/* ===== 共有（LINE・メール・端末の共有） ===== */
function shText(s,dist){
 const k=KIND[s.kind]?KIND[s.kind][0]:"", fl=FLOOD[s.flood]?FLOOD[s.flood][0]:"";
 const map=(s.lat&&s.lng)?`https://www.google.com/maps/search/?api=1&query=${s.lat},${s.lng}`:mapsLink(s.city,s.addr);
 let t=`【避難先】${s.name}（${k}）\n住所：${s.city}${s.addr}`;
 if(s.tel) t+=`\n電話：${s.tel}`;
 if(fl) t+=`\n水害：${fl}`;
 if(dist!=null&&isFinite(dist)) t+=`\n現在地から約${fmtD(dist)}（直線）`;
 t+=`\n地図：${map}`;
 if(s.lat&&s.lng) t+=`\n地理院地図：${gsiLink(s)}`;
 return t;
}
function gsiLink(s){return `https://maps.gsi.go.jp/#17/${s.lat}/${s.lng}/&base=std&ls=std&disp=1&vs=c1g1j0h0k0l0u0t0z0r0s0m0f0&d=m`;}
function shFoot(){return `\n\n※開設状況は災害ごとに変わります。市町村の最新情報を確認してください。`;}
function doLine(text){location.href="https://line.me/R/share?text="+encodeURIComponent(text);}
function doMail(subj,text){location.href="mailto:?subject="+encodeURIComponent(subj)+"&body="+encodeURIComponent(text);}
function doNative(subj,text){navigator.share({title:subj,text:text}).catch(()=>{});}
function doCopy(text,btn){
 const ok=()=>{const o=btn.textContent;btn.textContent="✓ コピー済";setTimeout(()=>btn.textContent=o,1500);};
 if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(text).then(ok,()=>prompt("コピーしてください",text));}
 else prompt("コピーしてください",text);
}
function shareRow(subj,getText){
 const d=document.createElement("div");d.className="share";
 const mk=(cls,label,fn)=>{const b=document.createElement("button");b.className=cls;b.textContent=label;b.onclick=e=>{e.stopPropagation();fn(b);};d.appendChild(b);};
 mk("line","LINEで送る",()=>doLine(getText()));
 mk("mail","✉ メール",()=>doMail(subj,getText()));
 if(navigator.share) mk("","💬 SMS・他のアプリ",()=>doNative(subj,getText()));
 mk("","コピー",b=>doCopy(getText(),b));
 return d;
}
"""
def patch(path):
    h=open(path,encoding='utf-8').read()
    if 'function shText(' in h:
        return 'skip(already)'
    # 1) CSS
    h=h.replace('.card.match{', CSS.strip()+'\n.card.match{',1)
    # 2) JS helpers: before function pill(
    h=h.replace('function pill(cls,txt)', JS.strip()+'\nfunction pill(cls,txt)',1)
    # 2b) card 地理院地図 link
    a='<a href="${mapsLink(s.city,s.addr)}" target="_blank" rel="noopener">地図</a>'
    assert a in h
    h=h.replace(a, a+'${s.lat?` · <a href="${gsiLink(s)}" target="_blank" rel="noopener">地理院地図</a>`:""}',1)
    # 3) per-card share row
    old='  <div class="row">${dp}${pill(fl[1],fl[0])}</div>`;\n return c;'
    new=('  <div class="row">${dp}${pill(fl[1],fl[0])}</div>`;\n'
         ' c.appendChild(shareRow(`避難先：${s.name}`,()=>shText(s,dist)+shFoot()));\n return c;')
    assert old in h, 'card anchor not found'
    h=h.replace(old,new,1)
    # 4) GPS banner: share a summary (current location + nearest of each type)
    old2=' out.appendChild(banner);\n const LIM=15;'
    new2=(' {const near=(f)=>list.find(f);'
          'const picks=[["指定避難所（寝泊まり）",near(s=>s.kind==="K"||s.kind==="H")],["指定緊急避難場所",near(s=>s.kind==="Q"||s.kind==="P")],["福祉避難所",near(s=>s.kind==="F")]].filter(p=>p[1]);'
          'const sumText=()=>`【現在地から近い避難先】\\n現在地：https://www.google.com/maps/search/?api=1&query=${lat},${lng}\\n\\n`+'
          'picks.map(p=>`■${p[0]}\\n`+shText(p[1],p[1]._d)).join("\\n\\n")+shFoot();'
          'const bar=shareRow("現在地から近い避難先",sumText);bar.classList.add("sharebar");'
          'const lb=document.createElement("div");lb.style.cssText="font-size:12px;color:var(--sub);margin-top:6px";lb.textContent="▼ 現在地と最寄りの避難先をまとめて送る";'
          'banner.appendChild(lb);banner.appendChild(bar);}\n'
          ' out.appendChild(banner);\n const LIM=15;')
    assert old2 in h, 'gps anchor not found'
    h=h.replace(old2,new2,1)
    open(path,'w',encoding='utf-8').write(h)
    return 'patched'
if __name__=='__main__':
    for p in sys.argv[1:]:
        print(p.split('/')[-1], patch(p))
