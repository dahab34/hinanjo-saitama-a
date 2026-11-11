# -*- coding: utf-8 -*-
"""手作り版（鴻巣・東松山・久喜）の対象市町について、国土地理院データの前回との差分と
市の資料PDFの更新を検知し、変化があれば tools/issue.md を書き出す（ワークフローがIssue化）。"""
import json, os, urllib.request, urllib.error, re
HERE=os.path.dirname(os.path.abspath(__file__))
SNAP=os.path.join(HERE,'watch_state.json'); ISSUE=os.path.join(HERE,'issue.md')
TOOLS={
 'hinanjo.html（鴻巣）':['鴻巣市','北本市','吉見町','川島町','加須市','桶川市'],
 'hinanjo-higashimatsuyama.html（東松山）':['東松山市','滑川町','嵐山町','坂戸市','鳩山町','毛呂山町','吉見町','鶴ヶ島市','越生町','ときがわ町'],
 'hinanjo-kuki.html（久喜）':['久喜市','蓮田市','白岡市','加須市','幸手市','宮代町','杉戸町','五霞町'],
}
# (表示名, 現行URL, 翌年度版の予想URL or None)
PDFS=[
 ('加須市 水害時避難行動マップ','https://www.city.kazo.lg.jp/material/files/group/18/kazo_suigai_chizu_2025.pdf',
  'https://www.city.kazo.lg.jp/material/files/group/18/kazo_suigai_chizu_2026.pdf'),
 ('鴻巣市 避難所資料','https://www.city.kounosu.saitama.jp/uploaded/attachment/28597.pdf',None),
 ('東松山市 避難所資料','https://www.city.higashimatsuyama.lg.jp/uploaded/attachment/18643.pdf',None),
 ('北本市 洪水ハザードマップ','https://www.city.kitamoto.lg.jp/material/files/group/5/kozui_0225.pdf',None),
 ('吉見町 防災マップ（避難所）','https://www.town.yoshimi.saitama.jp/material/files/group/2/bousai_P07-P08.pdf',None),
 ('川島町 防災マップ（避難所）','https://www.town.kawajima.saitama.jp/secure/1515/P10-11.pdf',None),
 ('桶川市 避難場所一覧','https://www.city.okegawa.lg.jp/material/files/group/16/3hinannbasho.pdf',None),
 ('久喜市 避難所・避難場所一覧','https://www.city.kuki.lg.jp/_res/projects/default_project/_page_/001/007/443/1007443_021.pdf',None),
 ('幸手市 洪水ハザードマップ','https://www.city.satte.lg.jp/material/files/group/39/satte_kouzui_map.pdf',None),
 ('幸手市 地震ハザードマップ','https://www.city.satte.lg.jp/material/files/group/39/satte_jishin_map.pdf',None),
 ('杉戸町 洪水ハザードマップ','https://www.town.sugito.lg.jp/uploaded/attachment/13861.pdf',None),
 ('宮代町 避難所一覧','https://www.town.miyashiro.lg.jp/cmsfiles/contents/0000025/25603/P07-P08_hinanjoitiranzentaisakuinzu.pdf',None),
 ('久喜市 ハザードマップ（全ページ）','https://www.city.kuki.lg.jp/_res/projects/default_project/_page_/001/007/443/r5.3hm-zenpeji.pdf',None),
]
WATCHED=sorted({c for v in TOOLS.values() for c in v})

def head(url):
    try:
        req=urllib.request.Request(url,method='HEAD',headers={'User-Agent':'Mozilla/5.0 hinanjo-watch'})
        with urllib.request.urlopen(req,timeout=60) as r:
            return {'status':r.status,'lm':r.headers.get('Last-Modified'),'len':r.headers.get('Content-Length'),'etag':r.headers.get('ETag')}
    except urllib.error.HTTPError as e: return {'status':e.code}
    except Exception as e: return {'status':'err','msg':str(e)[:100]}

def run(ev_rows, sh_rows, muni, short, base):
    """ev_rows/sh_rows: GeoJSON properties の行。muni/short/base は build.py の関数。"""
    cur={}
    for typ,rows,flag in (('指定緊急避難場所',ev_rows,'洪水'),('指定避難所',sh_rows,'受入対象者')):
        for r in rows:
            c=short(muni(r))
            if c not in WATCHED: continue
            k=f"{c}|{typ}|{base(r.get('施設・場所名',''))}"
            cur[k]={'name':r.get('施設・場所名',''),'addr':r.get('住所',''),'flag':str(r.get(flag,'')).strip()}
    pdf={}
    for label,url,nxt in PDFS:
        pdf[label]={'base':head(url), 'next':head(nxt) if nxt else {}}
    prev=json.load(open(SNAP,encoding='utf-8')) if os.path.exists(SNAP) else None
    json.dump({'gsi':cur,'pdf':pdf},open(SNAP,'w',encoding='utf-8'),ensure_ascii=False,indent=0)
    if os.path.exists(ISSUE): os.remove(ISSUE)
    if prev is None:
        print('watch: 初回のため基準を記録（通知なし）'); return
    by_city={}
    P=prev.get('gsi',{})
    def add(c,line): by_city.setdefault(c,[]).append(line)
    for k in sorted(set(cur)-set(P)):
        c,t,_=k.split('|'); add(c,f"＋ 追加（{t}）：{cur[k]['name']}　{cur[k]['addr']}")
    for k in sorted(set(P)-set(cur)):
        c,t,_=k.split('|'); add(c,f"－ 削除（{t}）：{P[k]['name']}")
    for k in sorted(set(P)&set(cur)):
        c,t,_=k.split('|'); a,b=P[k],cur[k]
        if a['flag']!=b['flag']:
            lab='洪水指定' if t=='指定緊急避難場所' else '受入対象者'
            add(c,f"△ {lab}変更（{t}）：{b['name']}　「{a['flag'] or 'なし'}」→「{b['flag'] or 'なし'}」")
        elif a['addr']!=b['addr'] or a['name']!=b['name']:
            add(c,f"△ 名称/住所変更（{t}）：{a['name']}→{b['name']}　{b['addr']}")
    pdf_lines=[]
    for label,v in pdf.items():
        pv=(prev.get('pdf') or {}).get(label,{})
        b,pb=v['base'],pv.get('base',{})
        if b.get('status')==200 and pb.get('status')==200 and (b.get('lm'),b.get('len'),b.get('etag'))!=(pb.get('lm'),pb.get('len'),pb.get('etag')):
            pdf_lines.append(f"・{label}：ファイルが更新されました（{pb.get('lm')} → {b.get('lm')}）")
        if b.get('status')!=200 and pb.get('status')==200:
            pdf_lines.append(f"・{label}：これまでのPDFが見つからなくなりました（{b.get('status')}）。新版に差し替えられた可能性")
        n,pn=v['next'],pv.get('next',{})
        if n.get('status')==200 and pn.get('status')!=200:
            pdf_lines.append(f"・{label}：**翌年度版のPDFが公開されました**")
    if not by_city and not pdf_lines:
        print('watch: 変化なし'); return
    out=['手作り版の対象市町で、元データに変化がありました。内容を確認し、必要なら手作り版を更新してください。','']
    for tool,cities in TOOLS.items():
        hit=[c for c in cities if c in by_city]
        if not hit: continue
        out.append(f'## {tool}')
        for c in hit:
            out.append(f'**{c}**'); out+= [f'- {l}' for l in by_city[c][:40]]
            if len(by_city[c])>40: out.append(f'- …ほか{len(by_city[c])-40}件')
        out.append('')
    if pdf_lines: out+=['## 市の資料PDF']+pdf_lines+['']
    out.append('※ 国土地理院の公開データ・市の公開PDFの機械的な比較です。9エリア版は自動更新済み。')
    open(ISSUE,'w',encoding='utf-8').write('\n'.join(out)); print('watch: 変化あり → issue.md 作成')
