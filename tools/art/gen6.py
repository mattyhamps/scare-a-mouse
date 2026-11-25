import json, math
src=open('./gen5.py').read()
exec(src[:src.index("boards={}")])
boards={}
def crd(ps):
    d=f'M {ps[0][0]} {ps[0][1]}'
    for i in range(len(ps)-1):
        a=ps[i-1] if i>0 else ps[i]; bb=ps[i]; c=ps[i+1]; e=ps[i+2] if i+2<len(ps) else c
        d+=f' C {bb[0]+(c[0]-a[0])/6:.1f} {bb[1]+(c[1]-a[1])/6:.1f}, {c[0]-(e[0]-bb[0])/6:.1f} {c[1]-(e[1]-bb[1])/6:.1f}, {c[0]} {c[1]}'
    return d
cheese=f'<svg viewBox="0 0 100 100" width="22" height="22"><path d="M8 74 L92 74 L92 40 Z" fill="{Q["mustard"]}"/><path d="M8 74 L92 40 L62 20 Z" fill="#ecc260"/><circle cx="62" cy="60" r="6" fill="{Q["mustard2"]}"/></svg>'
lock=lambda s=22: f'<svg viewBox="0 0 100 100" width="{s}" height="{s}"><path d="M32 46 L32 32 C32 12 68 12 68 32 L68 46" fill="none" stroke="{Q["lav2"]}" stroke-width="10"/><rect x="18" y="44" width="64" height="46" rx="12" fill="{Q["mustard"]}"/><rect x="50" y="44" width="32" height="46" rx="12" fill="{Q["mustard2"]}"/><circle cx="50" cy="64" r="7" fill="{Q["ink"]}"/></svg>'
# ---- 38 floor plan
def room(x,y,w,h,name,bg,sh,state,ic=''):
    if state=='fog':
        return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:18px;background:{Q["lav"]};box-shadow:inset -10px -10px 0 {Q["lav2"]};display:grid;place-items:center;font:700 30px Fredoka;color:{Q["cream"]}">?</div>'
    ring=f'box-shadow:inset -10px -10px 0 {sh},0 0 0 6px {Q["mustard"]};' if state=='here' else f'box-shadow:inset -10px -10px 0 {sh};'
    return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:18px;background:{bg};{ring}display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;color:{Q["cream"]}">{ic}<b style="{TT};font-size:20px">{name}</b><span style="font:700 14px Fredoka,sans-serif">{"✓ 30/30" if state=="done" else "4/30"}</span></div>'
book=f'<svg viewBox="0 0 100 100" width="34" height="34"><path d="M10 22 L50 30 L90 22 L90 80 L50 88 L10 80 Z" fill="{Q["cream"]}"/><path d="M50 30 L90 22 L90 80 L50 88 Z" fill="{Q["cream2"]}"/><rect x="8" y="20" width="8" height="62" rx="3" fill="{Q["coral"]}"/></svg>'
quill=f'<svg viewBox="0 0 100 100" width="34" height="34"><path d="M82 10 C40 18 22 50 20 84 C46 72 72 46 82 10 Z" fill="{Q["cream"]}"/><path d="M82 10 C62 40 44 62 20 84 C46 72 72 46 82 10 Z" fill="{Q["cream2"]}"/></svg>'
b=f'''<div style="{SC}background:{Q["purple"]}">{deco(390,844,5,14)}
  {pill(16,20,358,52,Q["mustard"],Q["mustard2"],'Castle',20)}
  <div style="position:absolute;left:0;right:0;top:94px;text-align:center;{TT};font-size:30px;color:{Q["cream"]}">First floor</div>
  <div style="position:absolute;left:16px;right:16px;top:146px;height:560px;border-radius:24px;background:{Q["cream"]};box-shadow:0 6px 0 {Q["cream2"]}"></div>
  <svg width="390" height="844" style="position:absolute;left:0;top:0"><path d="M100 600 L100 290 L262 290 L262 420 L262 530" fill="none" stroke="{Q["cream2"]}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/></svg>
  {room(34,476,136,212,'Library',Q['navy'],Q['navy2'],'done',book)}
  {room(34,166,136,286,'Study',Q['orange'],Q['orange2'],'here',quill)}
  {room(194,166,162,180,'','','','fog')}{room(194,364,162,124,'','','','fog')}{room(194,506,162,182,'','','','fog')}
  <div style="position:absolute;left:128px;top:172px">{sv('mouse',36)}</div>
  {pill(16,730,164,52,Q["cream"],Q["cream2"],'Cellars',18)}{pill(210,730,164,52,Q["lav"],Q["lav2"],lock(22)+' Upstairs',18,Q["cream"])}
</div>'''
boards['MedRetro-floor.dc.html']=('38 · Two-tone: a floor plan',b)
# ---- 39 win screen
N=7; cs=46; ox=(390-N*cs)//2; oy=200
cells=''.join(f'<rect x="{x*cs}" y="{y*cs}" width="{cs}" height="{cs}" fill="{Q["cream"] if (x+y)%2 else Q["cream2"]}"/>' for y in range(N) for x in range(N))
bd=f'<svg width="{N*cs}" height="{N*cs}" style="position:absolute;left:{ox}px;top:{oy}px;overflow:visible"><rect x="-12" y="-12" width="{N*cs+24}" height="{N*cs+24}" rx="22" fill="{Q["navy"]}"/>{cells}</svg>'
ribbon=f'''<svg width="320" height="80" style="position:absolute;left:35px;top:214px"><path d="M8 26 L46 26 L46 70 L26 58 L6 70 Z" fill="{Q["coral2"]}"/><path d="M312 26 L274 26 L274 70 L294 58 L314 70 Z" fill="{Q["coral2"]}"/><rect x="30" y="10" width="260" height="52" rx="12" fill="{Q["coral"]}"/><rect x="30" y="46" width="260" height="16" rx="8" fill="{Q["coral2"]}"/></svg>
  <div style="position:absolute;left:35px;width:320px;top:226px;text-align:center;{TT};font-size:26px;color:{Q["cream"]}">Mouse escaped!</div>'''
hole=f'<svg width="74" height="40" viewBox="0 0 74 40"><ellipse cx="37" cy="26" rx="34" ry="13" fill="{Q["ink"]}"/></svg>'
rep=f'<svg viewBox="0 0 100 100" width="20" height="20"><path d="M48 18 L12 50 L48 82 Z M88 18 L52 50 L88 82 Z" fill="{Q["cream"]}"/></svg>'
b=f'''<div style="{SC}background:{Q["purple"]}">{bd}
  <div style="position:absolute;inset:0;background:rgba(30,20,14,.6)"></div>
  <div style="position:absolute;left:30px;right:30px;top:244px;height:410px;border-radius:26px;background:{Q["cream"]};box-shadow:0 8px 0 {Q["cream2"]}"></div>
  {ribbon}
  <svg width="390" height="844" style="position:absolute;left:0;top:0">{spark(70,300,10,Q["mustard"])}{star8(322,320,12,Q["pink"])}{spark(300,380,7,Q["mustard"])}{star8(80,400,8,Q["pink"])}</svg>
  <div style="position:absolute;left:0;right:0;top:296px;display:flex;justify-content:center;align-items:flex-end;gap:4px">{sv('mouse',92)}{hole}</div>
  <div style="position:absolute;left:0;right:0;top:402px;text-align:center;font:600 17px Fredoka,sans-serif">Level 47 solved</div>
  {pill(118,434,154,42,Q["mustard"],Q["mustard2"],'+3 '+cheese,20)}
  {pill(54,500,282,54,Q["olive"],Q["olive2"],'Next level',20,Q["cream"])}
  {pill(54,572,134,50,Q["cream2"],'#cdb683','All levels',16)}{pill(202,572,134,50,Q["navy"],Q["navy2"],rep+' Replay',16,Q["cream"])}
</div>'''
boards['MedRetro-win.dc.html']=('39 · Two-tone: the win screen',b)
# ---- 40 how to play
chainrow=''.join(f'<div style="display:flex;align-items:center;gap:8px;justify-content:center;margin:4px 0">{sv(a,48)}<b style="font:700 15px Fredoka,sans-serif;color:{Q["mustard"]}">scares</b>{sv(b2,48)}</div>' for a,b2 in [('cat','mouse'),('dog','cat'),('bear','dog')])
b=f'''<div style="{SC}background:{Q["purple"]}">{deco(390,844,9,18)}
  <div style="position:absolute;inset:0;background:rgba(30,20,14,.35)"></div>
  <div style="position:absolute;left:24px;right:24px;top:110px;height:620px;border-radius:26px;background:{Q["cream"]};box-shadow:0 8px 0 {Q["cream2"]}"></div>
  <div style="position:absolute;left:46px;right:46px;top:134px;height:210px;border-radius:20px;background:{Q["navy"]};box-shadow:inset -10px -10px 0 {Q["navy2"]};display:flex;flex-direction:column;justify-content:center">{chainrow}</div>
  <div style="position:absolute;left:40px;right:40px;top:366px;text-align:center;{TT};font-size:28px;line-height:1.1">Animals scare each other</div>
  <div style="position:absolute;left:46px;right:46px;top:452px;text-align:center;font:600 16px/1.45 Fredoka,sans-serif">Each animal scares just one other. A scared animal runs straight away, and it can scare the next animal on its way.</div>
  <div style="position:absolute;left:0;right:0;top:562px;display:flex;justify-content:center;gap:8px">{''.join(f'<b style="width:12px;height:12px;border-radius:50%;background:{Q["mustard"] if k==1 else Q["cream2"]}"></b>' for k in range(4))}</div>
  {pill(54,596,282,54,Q["mustard"],Q["mustard2"],'Next',20)}
  <div style="position:absolute;left:0;right:0;top:672px;text-align:center;font:700 16px Fredoka,sans-serif;color:{Q["brown"]}">Skip</div>
</div>'''
boards['MedRetro-howto.dc.html']=('40 · Two-tone: a how-to-play card',b)
# ---- 41 Kitchens
def node(n,x,y,state):
    bg={'done':Q['mustard'],'cur':Q['cream'],'next':Q['cream'],'lock':Q['lav']}[state]
    sh={'done':Q['mustard2'],'cur':Q['cream2'],'next':Q['cream2'],'lock':Q['lav2']}[state]
    ring=f'box-shadow:0 4px 0 {sh},0 0 0 6px {Q["coral"]};' if state=='cur' else f'box-shadow:0 4px 0 {sh};'
    tick=f'<b style="position:absolute;right:-6px;bottom:-6px;width:18px;height:18px;border-radius:50%;background:{Q["green"]};color:#fff;font:700 11px Fredoka;display:grid;place-items:center">✓</b>' if state=='done' else ''
    return f'<div style="position:absolute;left:{x-22}px;top:{y-22}px;width:44px;height:44px;border-radius:50%;background:{bg};{ring}display:grid;place-items:center;font:700 16px Fredoka,sans-serif;color:{Q["ink"]}">{n}{tick}</div>'
pts=[(112,720),(185,690),(262,650),(290,585),(222,540),(132,505),(94,445),(152,398),(240,366),(290,302)]
road=crd([(195,860),(150,790)]+pts+[(250,240),(195,190)])
nodes=''.join(node(171+k,x,y,'done' if k<6 else 'cur' if k==6 else 'next' if k==7 else 'lock') for k,(x,y) in enumerate(pts))
def hearth(x,y): return f'''<svg width="130" height="124" style="position:absolute;left:{x}px;top:{y}px"><rect x="0" y="0" width="130" height="124" rx="14" fill="{Q["lav"]}"/><rect x="96" y="0" width="34" height="124" rx="14" fill="{Q["lav2"]}"/>
  <path d="M24 124 L24 74 C24 40 106 40 106 74 L106 124 Z" fill="#3a2418"/><path d="M48 124 C44 106 56 96 62 86 C64 100 78 104 72 124 Z" fill="{Q["mustard"]}"/><path d="M58 124 C56 112 62 106 64 100 C68 108 72 114 68 124 Z" fill="{Q["orange"]}"/>
  <ellipse cx="65" cy="84" rx="26" ry="17" fill="#4a4652"/><path d="M65 67 A26 17 0 0 1 91 84 A26 17 0 0 1 72 100 A26 17 0 0 0 82 84 Z" fill="#35323c"/><circle cx="56" cy="58" r="7" fill="{Q["cream"]}" opacity=".9"/><circle cx="70" cy="48" r="5" fill="{Q["cream"]}" opacity=".75"/></svg>'''
def table(x,y): return f'''<svg width="130" height="96" style="position:absolute;left:{x}px;top:{y}px"><rect x="12" y="0" width="106" height="12" rx="6" fill="{Q["brown2"]}"/><rect x="2" y="18" width="126" height="58" rx="12" fill="{Q["brown"]}"/><rect x="2" y="62" width="126" height="14" rx="7" fill="{Q["brown2"]}"/><rect x="12" y="82" width="106" height="12" rx="6" fill="{Q["brown2"]}"/>
  <ellipse cx="32" cy="40" rx="15" ry="8" fill="{Q["mustard"]}"/><path d="M68 30 L94 30 L88 48 L74 48 Z" fill="{Q["cream"]}"/><path d="M98 50 L120 50 L120 32 Z" fill="{Q["mustard"]}"/><circle cx="56" cy="56" r="7" fill="{Q["coral"]}"/></svg>'''
def sacks(x,y): return f'<svg width="124" height="90" style="position:absolute;left:{x}px;top:{y}px">' + ''.join(f'<path d="M{a} 86 C{a-8} 86 {a-10} 50 {a+6} 42 L{a+4} 32 L{a+26} 32 L{a+24} 42 C{a+40} 50 {a+38} 86 {a+30} 86 Z" fill="{Q["tan"]}"/><path d="M{a+18} 46 C{a+34} 54 {a+34} 84 {a+30} 86 L{a+16} 86 C{a+24} 74 {a+24} 56 {a+18} 46 Z" fill="{Q["tan2"]}"/><rect x="{a+4}" y="38" width="22" height="5" rx="2" fill="{Q["coral"]}"/>' for a in (8,46,84)) + '</svg>'
def barrels(x,y): return f'<svg width="112" height="92" style="position:absolute;left:{x}px;top:{y}px">' + ''.join(f'<rect x="{a}" y="{t}" width="32" height="42" rx="12" fill="{Q["orange"]}"/><rect x="{a+16}" y="{t}" width="16" height="42" rx="8" fill="{Q["orange2"]}"/><rect x="{a}" y="{t+11}" width="32" height="5" fill="{Q["orange2"]}"/><rect x="{a}" y="{t+27}" width="32" height="5" fill="{Q["orange2"]}"/>' for a,t in ((8,46),(42,46),(76,46),(25,6),(59,6))) + '</svg>'
torch=lambda x,y: f'<svg width="24" height="42" style="position:absolute;left:{x}px;top:{y}px"><rect x="8" y="18" width="8" height="22" rx="3" fill="{Q["brown2"]}"/><path d="M12 2 C4 10 6 18 12 18 C18 18 20 10 12 2 Z" fill="{Q["mustard"]}"/><path d="M12 8 C9 12 10 16 12 16 C14 16 15 12 12 8 Z" fill="{Q["coral"]}"/></svg>'
pan=lambda x,y: f'<svg width="30" height="46" style="position:absolute;left:{x}px;top:{y}px"><rect x="13" y="0" width="4" height="20" fill="{Q["ink"]}"/><circle cx="15" cy="32" r="13" fill="#4a4652"/><path d="M15 19 A13 13 0 0 1 28 32 A13 13 0 0 1 20 44 A13 13 0 0 0 23 32 Z" fill="#35323c"/></svg>'
b=f'''<div style="{SC}background:repeating-conic-gradient(#b5653a 0 25%,#a35a33 0 50%) 0 0/44px 44px">
  <div style="position:absolute;left:0;right:0;top:0;height:60px;background:{Q["purple"]}">
    {pill(14,10,98,40,Q["mustard"],Q["mustard2"],'Castle',16)}<div style="position:absolute;left:126px;top:14px;{TT};font-size:24px;color:{Q["cream"]}">Kitchens</div><b style="position:absolute;right:16px;top:20px;font:700 15px Fredoka,sans-serif;color:{Q["cream"]}">7/30</b></div>
  <div style="position:absolute;left:0;right:0;top:60px;height:150px;background:{Q["lav"]};box-shadow:inset 0 -12px 0 {Q["lav2"]}">
    <svg width="390" height="150"><rect x="30" y="20" width="44" height="64" rx="22" fill="#9cb8c8"/><rect x="52" y="20" width="22" height="64" rx="11" fill="#86a5b8"/><rect x="316" y="20" width="44" height="64" rx="22" fill="#9cb8c8"/><rect x="338" y="20" width="22" height="64" rx="11" fill="#86a5b8"/>
    <rect x="100" y="8" width="190" height="5" rx="2" fill="{Q["brown2"]}"/><path d="M166 150 L166 92 C166 64 224 64 224 92 L224 150 Z" fill="{Q["brown"]}"/><path d="M195 70 C212 72 224 80 224 92 L224 150 L195 150 Z" fill="{Q["brown2"]}"/><circle cx="208" cy="116" r="4" fill="{Q["mustard"]}"/></svg>
    {pan(118,12)}{pan(150,12)}{pan(236,12)}{pan(266,12)}</div>
  <svg width="390" height="844" style="position:absolute;left:0;top:0"><path d="{road}" fill="none" stroke="{Q["cream2"]}" stroke-width="40" stroke-linecap="round" transform="translate(0 4)"/><path d="{road}" fill="none" stroke="{Q["cream"]}" stroke-width="38" stroke-linecap="round"/></svg>
  {hearth(236,404)}{table(14,548)}{sacks(240,702)}{barrels(18,250)}{torch(10,330)}{torch(358,486)}{torch(10,646)}
  {nodes}
  <div style="position:absolute;left:76px;top:398px">{sv('mouse',36)}</div>
</div>'''
boards['MedRetro-kitchens.dc.html']=('41 · Two-tone: an indoor room (Kitchens)',b)
base='/home/claude/mockups/project'
for fn,(t,body) in boards.items():
    open(f'{base}/{fn}','w').write(HEADQ%t+body+'\n'+TAIL)
c=json.load(open(f'{base}/canvas.json'))
row=c['boards']['MedRetro-castle.dc.html']; x=row['x']+row['w']+80
for fn in boards:
    c['boards'].pop(fn,None); c['order']=[o for o in c['order'] if o!=fn]
    c['boards'][fn]={'x':x,'y':row['y'],'w':390,'h':844,'title':boards[fn][0]}; c['order'].append(fn); x+=470
json.dump(c,open(f'{base}/canvas.json','w'),ensure_ascii=False)
print('ok')
