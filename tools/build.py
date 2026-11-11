# -*- coding: utf-8 -*-
"""国土地理院の公開GeoJSONを取得し、9エリア版の避難所さがしを再生成する。
GitHub Actions から月1回実行。件数が大きく減った場合は更新しない（安全装置）。"""
import json, re, os, sys, urllib.request, email.utils, datetime
from collections import defaultdict, Counter
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
sys.path.insert(0,HERE); from patch_share import patch
import watch
BASE='https://hinanmap.gsi.go.jp/hinanjocp/defaultFtpData/geoJSON/'
CODES=['11000','10205','10209','10523','10524','10525','12208','08542']  # 埼玉県全域＋周辺7市町
STATE=os.path.join(HERE,'state.json'); MIN_RATIO=0.9

def fetch(code,typ):
    url=f'{BASE}{code}_{typ}.geojson'
    req=urllib.request.Request(url,headers={'User-Agent':'hinanjo-updater'})
    with urllib.request.urlopen(req,timeout=120) as r:
        lm=r.headers.get('Last-Modified'); data=json.loads(r.read().decode('utf-8-sig'))
    feats=data.get('features') or []
    if not feats: raise SystemExit(f'空データ: {url}')
    rows=[]
    for f in feats:
        p=dict(f.get('properties') or {}); c=(f.get('geometry') or {}).get('coordinates') or [None,None]
        p['経度'],p['緯度']=c[0],c[1]; rows.append(p)
    d=email.utils.parsedate_to_datetime(lm).astimezone(datetime.timezone(datetime.timedelta(hours=9))).date() if lm else None
    print(f'{code}_{typ}: {len(rows)}件 {d or "日付不明"}'); return rows,d

def parse_pm(a):
    a=(a or '').strip(); m=re.match(r'(.+?[都道府県])(.+)',a)
    if not m: return ''
    m2=re.match(r'(.+?[市区町村])',m.group(2)); return m.group(1)+(m2.group(1) if m2 else '')
def short(m): return re.sub(r'^.+?[都道府県]','',m)
def base(n): return re.sub(r'[\s　]','',re.sub(r'[（(].*?[)）]','',n or ''))
def jis5(cid): m=re.match(r'E(\d{5})',(cid or '').strip()); return m.group(1) if m else ''
OUTDOOR=re.compile(r'公園|グラウンド|グランド|広場|運動場|運動公園|緑地|河川敷|園庭|校庭|ピロティ|多目的')

def main():
    ev,sh,dates=[],[],[]
    for c in CODES:
        r,d=fetch(c,'2'); ev+=r; dates.append(d)
        r,d=fetch(c,'1'); sh+=r; dates.append(d)
    total=len(ev)+len(sh)
    prev=json.load(open(STATE)) if os.path.exists(STATE) else {}
    if prev.get('total') and total<prev['total']*MIN_RATIO:
        raise SystemExit(f'件数が前回{prev["total"]}→{total}に急減。安全のため更新を中止。')
    # 共通IDの自治体コード → 指定自治体名（住所の最頻値）
    votes=defaultdict(Counter)
    for r in ev+sh:
        k=jis5(r.get('共通ID')); n=parse_pm(r.get('住所'))
        if k and n: votes[k][n]+=1
    nmap={k:v.most_common(1)[0][0] for k,v in votes.items()}
    muni=lambda r: nmap.get(jis5(r.get('共通ID'))) or parse_pm(r.get('住所'))
    try: watch.run(ev,sh,muni,short,base)
    except Exception as e: print('watch失敗（更新は続行）:',e)
    emg=defaultdict(lambda:{'kozui':0,'outdoor':False})
    for r in ev:
        m=muni(r); nm=r.get('施設・場所名',''); e=emg[(m,base(nm))]
        e.setdefault('muni',m); e.setdefault('name',nm); e.setdefault('addr',r.get('住所',''))
        e.setdefault('lat',r['緯度']); e.setdefault('lng',r['経度'])
        if str(r.get('洪水','')).strip()=='1': e['kozui']=1
        if OUTDOOR.search(nm): e['outdoor']=True
    shl=defaultdict(lambda:{'fukushi':False})
    for r in sh:
        m=muni(r); nm=r.get('施設・場所名',''); s=shl[(m,base(nm))]
        s.setdefault('muni',m); s.setdefault('name',nm); s.setdefault('addr',r.get('住所',''))
        s.setdefault('lat',r['緯度']); s.setdefault('lng',r['経度'])
        if str(r.get('受入対象者','')).strip(): s['fukushi']=True
    facs=defaultdict(list)
    for key in set(emg)|set(shl):
        e=emg.get(key); s=shl.get(key); src=s or e; m=src['muni']; addr=src['addr']
        kind='F' if (s and s['fukushi']) else 'K' if s else 'P' if e['outdoor'] else 'Q'
        flood=('ok' if e['kozui'] else 'no') if e else '-'
        own=parse_pm(addr); rel=addr[len(own):] if own and addr.startswith(own) else addr
        if own and own!=m: rel=f'（{own}）'+rel
        def f6(x):
            try: return round(float(x),6)
            except: return 0
        facs[short(m)].append(dict(city=short(m),name=src['name'],addr=rel,kind=kind,flood=flood,lat=f6(src['lat']),lng=f6(src['lng'])))
    known=[d for d in dates if d]; asof=max(known) if known else datetime.date.today()
    asof_s=f'{asof.year}年{asof.month}月{asof.day}日時点'
    AREAS=[
     ('さいたま・南部','saitama-south',['さいたま市','川口市','蕨市','戸田市']),
     ('南西部','nanseibu',['朝霞市','志木市','和光市','新座市','富士見市','ふじみ野市','三芳町']),
     ('県央','kenou',['上尾市','桶川市','北本市','鴻巣市','伊奈町']),
     ('東部・千葉野田','toubu-noda',['春日部市','草加市','越谷市','八潮市','三郷市','吉川市','松伏町','野田市']),
     ('利根・茨城五霞','tone-goka',['行田市','加須市','羽生市','久喜市','蓮田市','幸手市','白岡市','宮代町','杉戸町','五霞町']),
     ('川越比企','kawagoe-hiki',['川越市','東松山市','坂戸市','鶴ヶ島市','毛呂山町','越生町','滑川町','嵐山町','小川町','川島町','吉見町','鳩山町','ときがわ町','東秩父村']),
     ('西部','seibu',['所沢市','飯能市','狭山市','入間市','日高市']),
     ('北部・群馬隣接','hokubu-gunma',['熊谷市','本庄市','深谷市','美里町','神川町','上里町','寄居町','太田市','藤岡市','千代田町','大泉町','邑楽町']),
     ('秩父','chichibu',['秩父市','横瀬町','皆野町','長瀞町','小鹿野町']),
    ]
    miss=sorted(set(c for _,_,cs in AREAS for c in cs)-set(facs))
    if miss: raise SystemExit(f'データ欠落の市町村あり: {miss}。更新を中止。')
    unassigned=sorted(set(facs)-set(c for _,_,cs in AREAS for c in cs))
    if unassigned: print('※エリア未割当（表示されない）:',unassigned)
    KORD={'K':0,'F':1,'Q':2,'P':3}; esc=lambda s: json.dumps(s or '',ensure_ascii=False)
    NOTE=(f'出典：国土地理院 指定緊急避難場所・指定避難所データ（{asof_s}）。水害○×は『洪水の指定緊急避難場所か否か』の自動判定。'
          '水害‐は指定避難所のみで種別データ未掲載。上階避難・協定避難先・電話・地区は未収録。最新は各市町村で確認を。')
    tpl=open(os.path.join(HERE,'template.html'),encoding='utf-8').read(); idx=[]; n_all=0
    for area,slug,cities in AREAS:
        rows=[f for c in cities for f in facs[c]]
        rows.sort(key=lambda f:(cities.index(f['city']),KORD.get(f['kind'],9),f['name']))
        raw='\n'+',\n'.join(f"[{esc(f['city'])},{esc(f['name'])},{esc(f['addr'])},\"-\",\"{f['kind']}\",\"{f['flood']}\",\"\",{f['lat']},{f['lng']}]" for f in rows)+'\n'
        h=re.sub(r'const RAW = \[.*?\]\.map\(',lambda _:'const RAW = ['+raw+'].map(',tpl,count=1,flags=re.S)
        h=re.sub(r'const CITIES=\[[^\]]*\];',lambda _:'const CITIES=['+','.join(esc(c) for c in cities)+'];',h,count=1)
        h=re.sub(r'const SRC=\{.*?\n\};',lambda _:'const SRC={\n '+',\n '.join(f'{esc(c)}:{esc(NOTE)}' for c in cities)+'\n};',h,count=1,flags=re.S)
        h=h.replace('避難所さがし 東松山営業所版',f'避難所さがし {area}版').replace('避難所さがし　東松山営業所版',f'避難所さがし　{area}版')
        fn=os.path.join(ROOT,f'hinanjo-{slug}.html'); open(fn,'w',encoding='utf-8').write(h); patch(fn)
        idx.append((area,f'hinanjo-{slug}.html',len(rows),cities)); n_all+=len(rows)
    li=''.join(f'<li><a href="{fn}">避難所さがし {a}版</a><span class="m">{n}件・{len(cs)}市町村<br>{"／".join(cs)}</span></li>' for a,fn,n,cs in idx)
    open(os.path.join(ROOT,'hinanjo-areas.html'),'w',encoding='utf-8').write(f'''<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>避難所さがし エリア索引（埼玉県＋周辺）</title>
<style>body{{margin:0;background:#f6f7f9;color:#1c2530;font-family:-apple-system,"Noto Sans JP","Yu Gothic",sans-serif;font-size:15px;line-height:1.6}}
.wrap{{max-width:760px;margin:0 auto;padding:16px}} h1{{font-size:18px}} .lead{{color:#5b6573;font-size:13px}}
ul{{list-style:none;padding:0}} li{{background:#fff;border:1px solid #e3e7ec;border-radius:12px;margin:8px 0;padding:12px 14px}}
li a{{font-weight:700;color:#2b5d8a;text-decoration:none;font-size:16px}} .m{{display:block;color:#5b6573;font-size:12px;margin-top:4px}}
.src{{color:#5b6573;font-size:12px;margin-top:16px}}</style></head>
<body><div class="wrap"><h1>避難所さがし｜エリア索引</h1>
<p class="lead">埼玉県全域（63市町村）＋隣接する群馬・千葉・茨城の周辺自治体（計70市町村・{n_all:,}施設）を9エリアに分割。各エリアをタップで開いてください。出典：国土地理院 指定緊急避難場所・指定避難所データ（{asof_s}）。毎月自動更新。</p>
<ul>{li}</ul>
<p class="src">※種別・水害可否はGSIデータからの自動判定です。上階避難の判断・協定避難先・電話番号などは含みません。GPS・共有ボタンは https:// で開いたときに動作します。</p>
</div></body></html>''')
    json.dump({'total':total,'facilities':n_all,'asof':str(asof),'built':str(datetime.date.today())},open(STATE,'w'),ensure_ascii=False,indent=1)
    print(f'完了: {n_all}施設 / {asof_s}')
if __name__=='__main__': main()
