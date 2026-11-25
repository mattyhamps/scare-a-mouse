import json, math, random
g14=open('./gen14.py').read()
exec(g14[:g14.index("# ----- floor")])
# ===== Meadow v2: same rules as Kitchens K2 (3/4 view, light top-left, one shadow per object, shared scale)
GR=('#86a654','#7a9a4a','#5f7d38')    # grass light / base / dark
def tree3(x,y,s=1,apples=False):
    canopy=f'''<circle cx="30" cy="40" r="26" fill="{Q["green2"]}"/><circle cx="66" cy="42" r="24" fill="{Q["green2"]}"/><circle cx="48" cy="28" r="30" fill="{Q["green"]}"/><circle cx="28" cy="36" r="20" fill="{Q["green"]}"/>
      <path d="M78 30 A30 30 0 0 1 72 56 Q60 66 44 64 Q66 54 70 32 Z" fill="{Q["green2"]}"/><circle cx="36" cy="18" r="11" fill="#5a9a52"/><circle cx="24" cy="30" r="7" fill="#5a9a52"/>'''
    ap=''.join(f'<circle cx="{ax}" cy="{ay}" r="5" fill="{Q["coral"]}"/><circle cx="{ax-1.5}" cy="{ay-1.5}" r="1.5" fill="{Q["pink"]}"/>' for ax,ay in [(30,44),(56,22),(64,48),(44,56),(20,32)]) if apples else ''
    fallen=''.join(f'<circle cx="{ax}" cy="{ay}" r="4.6" fill="{Q["coral"]}"/>' for ax,ay in [(14,108),(86,104)]) if apples else ''
    return f'''<g transform="translate({x} {y}) scale({s})">{shadow(52,104,44,11)}<path d="M40 60 L38 104 Q48 108 58 104 L56 60 Z" fill="{Q["brown"]}"/><path d="M50 60 L52 105 Q55 105 58 104 L56 60 Z" fill="{Q["brown2"]}"/>
      <path d="M38 104 Q30 106 28 108 L42 106 Z M58 104 Q66 106 68 108 L56 106 Z" fill="{Q["brown2"]}"/>{canopy}{ap}{fallen}</g>'''
def bush3(x,y,s=1,fl=None):
    f=''.join(f'<circle cx="{fx}" cy="{fy}" r="3" fill="{fl}"/>' for fx,fy in [(14,12),(30,6),(44,14),(24,20)]) if fl else ''
    return f'<g transform="translate({x} {y}) scale({s})">{shadow(30,34,32,7)}<circle cx="16" cy="20" r="14" fill="{Q["green"]}"/><circle cx="34" cy="16" r="16" fill="{Q["green"]}"/><circle cx="48" cy="22" r="12" fill="{Q["green2"]}"/><path d="M2 22 Q2 34 14 34 L50 34 Q60 32 60 22 Z" fill="{Q["green2"]}"/><circle cx="26" cy="10" r="6" fill="#5a9a52"/>{f}</g>'
def tuft3(x,y,s=1): return f'<g transform="translate({x} {y}) scale({s})"><path d="M0 10 L4 0 L7 10 Z" fill="{GR[0]}"/><path d="M5 10 L10 -3 L13 10 Z" fill="{GR[2]}"/><path d="M11 10 L15 2 L18 10 Z" fill="{GR[0]}"/></g>'
def rock(x,y,s=1):
    return f'<g transform="translate({x} {y}) scale({s})">{shadow(20,24,22,5)}<path d="M2 22 Q0 8 14 4 Q30 0 38 12 Q42 20 38 24 Z" fill="#a39c8f"/><path d="M26 3 Q34 4 38 12 Q42 20 38 24 L24 24 Q32 14 26 3 Z" fill="#857e72"/><path d="M8 10 Q14 6 20 7" stroke="#bdb6a9" stroke-width="3" fill="none" stroke-linecap="round"/></g>'
def flower_patch(x,y,c,c2):
    pts=[(0,6),(12,0),(24,8),(8,16),(20,18),(32,12)]
    return f'<g transform="translate({x} {y})"><ellipse cx="16" cy="14" rx="22" ry="9" fill="{GR[2]}" opacity=".35"/>'+''.join(f'<rect x="{px-1}" y="{py}" width="2" height="8" fill="{Q["green2"]}"/><circle cx="{px}" cy="{py}" r="4.2" fill="{c if i%2 else c2}"/><circle cx="{px-1}" cy="{py-1}" r="1.6" fill="{Q["cream"]}"/>' for i,(px,py) in enumerate(pts))+'</g>'
def mush3(x,y,c,c2):
    one=lambda dx,dy,s: f'<g transform="translate({dx} {dy}) scale({s})"><rect x="9" y="12" width="10" height="14" rx="4" fill="{Q["cream"]}"/><rect x="14" y="12" width="5" height="14" rx="2" fill="{Q["cream2"]}"/><path d="M0 15 Q14 -6 28 15 Z" fill="{c}"/><path d="M17 1 Q26 6 28 15 L20 15 Z" fill="{c2}"/><circle cx="9" cy="9" r="2.4" fill="{Q["cream"]}"/><circle cx="17" cy="6" r="2" fill="{Q["cream"]}"/></g>'
    return f'<g transform="translate({x} {y})">{shadow(24,28,26,5)}{one(0,0,1)}{one(26,8,.7)}{one(14,12,.55)}</g>'
def pond3(x,y):
    reeds=''.join(f'<rect x="{rx}" y="{ry}" width="3" height="22" rx="1.5" fill="{Q["green2"]}"/><ellipse cx="{rx+1.5}" cy="{ry+2}" rx="3" ry="7" fill="{Q["brown"]}"/>' for rx,ry in ((6,10),(14,4),(112,6)))
    duck=f'<g transform="translate(58 28)"><ellipse cx="12" cy="16" rx="15" ry="5" fill="#4f6f86"/><ellipse cx="12" cy="12" rx="14" ry="8" fill="{Q["cream"]}"/><path d="M4 10 Q12 6 18 12 Q12 16 4 14 Z" fill="{Q["cream2"]}"/><circle cx="23" cy="4" r="6" fill="{Q["green"]}"/><path d="M28 4 L34 6 L28 8 Z" fill="{Q["mustard"]}"/><circle cx="24" cy="3" r="1.4" fill="{Q["ink"]}"/></g>'
    return f'''<g transform="translate({x} {y})"><ellipse cx="62" cy="40" rx="64" ry="34" fill="{GR[2]}"/><ellipse cx="62" cy="38" rx="58" ry="29" fill="#4f6f86"/><ellipse cx="62" cy="40" rx="56" ry="26" fill="#6f9bb3"/><path d="M62 14 A56 26 0 0 1 118 40 A56 26 0 0 1 90 63 A60 28 0 0 0 104 40 Z" fill="#5a879f"/>
      <path d="M24 40 q7 -4 14 0 M78 54 q6 -3 12 0" stroke="#a9cbe0" stroke-width="2.4" fill="none" stroke-linecap="round"/><ellipse cx="96" cy="30" rx="11" ry="5" fill="{Q["olive"]}"/><path d="M96 30 L106 27 L105 32 Z" fill="#6f9bb3"/><circle cx="94" cy="28" r="3" fill="{Q["pink"]}"/>
      {rock(-4,40,.6)}{rock(104,46,.55)}{reeds}{duck}</g>'''
def blanket(x,y):
    w,d=112,64
    checks=''.join(f'<rect x="{6+c*20}" y="{4+r*20}" width="10" height="{d-8 if False else 10}" fill="{Q["cream"]}" opacity=".0"/>' for c in range(5) for r in range(3))
    stripes=''.join(f'<rect x="{18+c*24}" y="0" width="9" height="{d}" fill="{Q["cream"]}" opacity=".75"/>' for c in range(4))+''.join(f'<rect x="0" y="{12+r*20}" width="{w}" height="9" fill="{Q["cream"]}" opacity=".75"/>' for r in range(3))
    basket=f'''<g transform="translate(14 6)">{shadow(20,36,22,5)}<path d="M2 16 L38 16 L34 36 L6 36 Z" fill="#c99a56"/><path d="M24 16 L38 16 L34 36 L24 36 Z" fill="#a87a42"/>{''.join(f'<rect x="4" y="{20+k*6}" width="32" height="1.6" fill="#a87a42"/>' for k in range(3))}<ellipse cx="20" cy="16" rx="18" ry="5" fill="#d9b06a"/><circle cx="12" cy="13" r="5" fill="{Q["coral"]}"/><circle cx="22" cy="12" r="5" fill="{Q["coral2"]}"/><path d="M4 16 Q20 -8 36 16" fill="none" stroke="#a87a42" stroke-width="3"/></g>'''
    pie=f'<g transform="translate(66 22)"><ellipse cx="16" cy="12" rx="16" ry="7" fill="#c88a3e"/><ellipse cx="16" cy="9" rx="16" ry="7" fill="#dca55a"/><path d="M8 7 L24 11 M8 11 L24 7" stroke="#c88a3e" stroke-width="2"/></g>'
    cup=f'<g transform="translate(64 42)"><rect x="0" y="0" width="10" height="11" rx="3" fill="{Q["cream"]}"/><rect x="5" y="0" width="5" height="11" rx="2" fill="{Q["cream2"]}"/></g>'
    return f'''<g transform="translate({x} {y}) rotate(-5 {w/2} {d/2})"><rect x="2" y="6" width="{w}" height="{d}" rx="5" fill="#2a140a" opacity=".16"/><rect x="0" y="0" width="{w}" height="{d}" rx="5" fill="{Q["coral"]}"/>{stripes}{basket}{pie}{cup}</g>'''
def skep(x,y):
    bands=''.join(f'<path d="M{6+i*1.2} {16+i*7} Q24 {12+i*7} {42-i*1.2} {16+i*7}" stroke="{Q["mustard2"]}" stroke-width="2.4" fill="none"/>' for i in range(4))
    bees=''.join(f'<g transform="translate({bx} {by})"><ellipse cx="0" cy="0" rx="4.6" ry="3.4" fill="{Q["mustard"]}"/><rect x="-1" y="-3.4" width="2" height="6.8" fill="{Q["ink"]}"/><ellipse cx="-1" cy="-4" rx="2.8" ry="1.8" fill="#fff" opacity=".85"/></g>' for bx,by in ((58,8),(-10,18),(54,30)))
    return f'''<g transform="translate({x} {y})">{shadow(26,80,26,6)}<rect x="22" y="44" width="8" height="36" fill="{WOOD[2]}"/><rect x="2" y="38" width="48" height="8" rx="2" fill="{WOOD[1]}"/><ellipse cx="26" cy="38" rx="24" ry="5" fill="{WOOD[0]}"/>
      <path d="M6 38 Q4 4 26 2 Q48 4 46 38 Z" fill="{Q["mustard"]}"/><path d="M26 2 Q48 4 46 38 L32 38 Q36 14 26 2 Z" fill="{Q["mustard2"]}"/>{bands}<path d="M19 38 Q19 29 26 29 Q33 29 33 38 Z" fill="#4a2e1c"/>{bees}</g>'''
def fence3(x,y,n):
    rails=f'<rect x="0" y="12" width="{n*28}" height="6" rx="2" fill="{WOOD[0]}"/><rect x="0" y="16" width="{n*28}" height="2" fill="{WOOD[1]}"/><rect x="0" y="26" width="{n*28}" height="6" rx="2" fill="{WOOD[0]}"/><rect x="0" y="30" width="{n*28}" height="2" fill="{WOOD[1]}"/>'
    posts=''.join(f'<rect x="{k*28-4}" y="2" width="9" height="38" rx="2" fill="{WOOD[1]}"/><rect x="{k*28+1}" y="2" width="4" height="38" fill="{WOOD[2]}"/><ellipse cx="{k*28+0.5}" cy="3" rx="4.5" ry="2" fill="{WOOD[0]}"/>' for k in range(n+1))
    return f'<g transform="translate({x} {y})"><rect x="-6" y="38" width="{n*28+12}" height="6" rx="3" fill="#2a140a" opacity=".16"/>{rails}{posts}</g>'
def hay(x,y):   # round bale, flat end towards us
    return f'''<g transform="translate({x} {y})">{shadow(36,46,38,7)}<rect x="22" y="4" width="44" height="40" rx="12" fill="#d9b46a"/><rect x="46" y="4" width="20" height="40" rx="10" fill="#b8924a"/><path d="M30 8 l20 0 M30 18 l26 0 M30 30 l24 0" stroke="#b8924a" stroke-width="2" stroke-linecap="round"/>
      <circle cx="24" cy="24" r="20" fill="#e6c47a"/><circle cx="24" cy="24" r="13" fill="none" stroke="#c9a457" stroke-width="2"/><circle cx="24" cy="24" r="6" fill="none" stroke="#c9a457" stroke-width="2"/></g>'''
def signpost(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(12,58,14,4)}<rect x="8" y="10" width="8" height="48" fill="{WOOD[1]}"/><rect x="12" y="10" width="4" height="48" fill="{WOOD[2]}"/>
      <path d="M-2 6 L40 6 L50 16 L40 26 L-2 26 Z" fill="{WOOD[0]}"/><path d="M-2 20 L44 20 L40 26 L-2 26 Z" fill="{WOOD[1]}"/><path d="M8 16 L30 16 M24 11 L30 16 L24 21" stroke="{WOOD[2]}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>'''
def butterfly(x,y,c,c2): return f'<g transform="translate({x} {y})"><ellipse cx="-5" cy="-3" rx="5" ry="6" fill="{c}"/><ellipse cx="5" cy="-3" rx="5" ry="6" fill="{c2}"/><ellipse cx="-4" cy="5" rx="3.6" ry="4" fill="{c}"/><ellipse cx="4" cy="5" rx="3.6" ry="4" fill="{c2}"/><rect x="-1" y="-6" width="2" height="14" rx="1" fill="{Q["ink"]}"/></g>'
# ----- skyline (the outdoor version of the back wall)
def far_tree(x,y,s): return f'<g transform="translate({x} {y}) scale({s})"><rect x="10" y="22" width="5" height="16" fill="#4a5a4a"/><circle cx="12" cy="16" r="14" fill="#55786a"/><path d="M26 16 A14 14 0 0 1 14 30 Q22 22 22 10 Z" fill="#4a6a5e"/></g>'
def cloud(x,y,s=1): return f'<g transform="translate({x} {y}) scale({s})"><rect x="0" y="12" width="70" height="14" rx="7" fill="{Q["cream"]}"/><circle cx="22" cy="12" r="12" fill="{Q["cream"]}"/><circle cx="42" cy="8" r="14" fill="{Q["cream"]}"/><rect x="0" y="20" width="70" height="6" rx="3" fill="{Q["cream2"]}"/></g>'
SKY=f'''<rect x="0" y="0" width="390" height="214" fill="#a9c3cf"/><rect x="0" y="0" width="390" height="90" fill="#9cb8c8"/>
  <circle cx="334" cy="92" r="30" fill="{Q["mustard"]}" opacity=".22"/><circle cx="334" cy="92" r="20" fill="{Q["mustard"]}"/>{cloud(30,70)}{cloud(232,62,.7)}
  <path d="M-10 160 Q70 104 160 140 Q240 100 320 130 Q370 112 400 130 L400 214 L-10 214 Z" fill="#7d9a8c"/>
  {''.join(far_tree(tx,ty,s) for tx,ty,s in ((18,118,1),(52,108,.9),(290,110,.9),(326,116,1),(356,112,.8)))}
  <rect x="148" y="100" width="94" height="114" fill="{Q["lav"]}"/><rect x="214" y="100" width="28" height="114" fill="{Q["lav2"]}"/>{''.join(f'<rect x="{148+k*20}" y="88" width="13" height="16" rx="2" fill="{Q["lav"] if k<4 else Q["lav2"]}"/>' for k in range(5))}
  {''.join(f'<rect x="{152+(r%2)*12+k*24}" y="{110+r*18}" width="18" height="12" rx="2" fill="#978f83" opacity=".45"/>' for r in range(4) for k in range(4) if 152+(r%2)*12+k*24<228)}
  <path d="M164 214 L164 150 C164 118 226 118 226 150 L226 214 Z" fill="{Q["brown"]}"/><path d="M195 122 C214 124 226 136 226 150 L226 214 L195 214 Z" fill="{Q["brown2"]}"/><rect x="164" y="160" width="62" height="4" fill="{Q["brown2"]}"/><rect x="164" y="188" width="62" height="4" fill="{Q["brown2"]}"/><circle cx="212" cy="176" r="4" fill="{Q["mustard"]}"/>
  <rect x="190" y="70" width="3" height="30" fill="{DARK}"/><path d="M193 70 L216 76 L193 84 Z" fill="{Q["coral"]}"/>
  <path d="M-10 196 Q80 170 150 190 L150 214 L-10 214 Z" fill="{Q["green2"]}"/><path d="M240 192 Q320 168 400 186 L400 214 L240 214 Z" fill="{Q["green2"]}"/>
  {bush3(-6,176,1,Q["pink"])}{bush3(92,178,.85,Q["cream"])}{bush3(244,178,.85,Q["mustard"])}{bush3(330,174,1,Q["pink"])}'''
rg=random.Random(4)
ground=f'<rect x="0" y="214" width="390" height="630" fill="{GR[1]}"/>'
ground+=''.join(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{GR[0]}" opacity=".55"/>' for cx,cy,rx,ry in ((70,300,70,26),(300,420,60,20),(60,560,64,22),(330,700,56,20),(140,820,80,24),(200,460,40,14),(330,260,40,14)))
TUFTS=''.join(tuft3(tx,ty) for tx,ty in ((150,250),(172,262),(340,330),(352,346),(196,470),(30,438),(46,452),(160,604),(176,616),(256,820),(272,832),(32,708),(366,566),(124,840),(220,690)))
MPATH=f'''<path d="{road}" fill="none" stroke="{Q["tan2"]}" stroke-width="44" stroke-linecap="round" transform="translate(0 3)"/><path d="{road}" fill="none" stroke="{Q["tan"]}" stroke-width="40" stroke-linecap="round"/><path d="{road}" fill="none" stroke="#dcc08e" stroke-width="14" stroke-linecap="round"/>'''
MPROPS=''.join([
    blanket(22,236), mush3(326,234,Q["coral"],Q["coral2"]),
    fence3(-4,378,2), bush3(330,300,.8,Q["cream"]),
    pond3(250,392), rock(196,420,.8),
    skep(30,520), flower_patch(40,612,Q["pink"],Q["pink2"]), flower_patch(108,560,Q["cream"],Q["cream2"]),
    tree3(290,566,.95,True), flower_patch(316,676,Q["navy"],Q["navy2"]),
    hay(236,736), hay(300,766), fence3(250,700,0) if False else '',
    rock(30,690,.9), signpost(42,770), mush3(330,820,Q["pink"],Q["pink2"]) if False else '',
    tree3(-34,610,.8,False),
])
FLY=butterfly(98,330,Q["pink"],Q["pink2"])+butterfly(196,560,Q["cream"],Q["cream2"])+butterfly(352,470,Q["mustard"],Q["mustard2"])
mb=f'''<div style="{SC}background:{GR[1]}">
  <svg width="390" height="844" style="position:absolute;left:0;top:0">{ground}{MPATH}{SKY}{STEP}<rect x="0" y="214" width="390" height="10" fill="#2a140a" opacity=".1"/>
    {TUFTS}{MPROPS}{FLY}
  </svg>
  <div style="position:absolute;left:0;right:0;top:0;height:56px;background:{Q["purple"]};z-index:4">
    {pill(14,8,98,40,Q["mustard"],Q["mustard2"],'Castle',16)}<div style="position:absolute;left:126px;top:12px;{TT};font-size:24px;color:{Q["cream"]}">Meadow</div><b style="position:absolute;right:16px;top:18px;font:700 15px Fredoka,sans-serif;color:{Q["cream"]}">5/20</b></div>
  {nodes(21)}
  <div style="position:absolute;left:122px;top:430px;z-index:4">{sv('mouse',36)}</div>
</div>'''
base='/home/claude/mockups/project'; fn='Room-v2-meadow.dc.html'; t='M2 · Meadow: redrawn to the Kitchens K2 rules'
c=json.load(open(f'{base}/canvas.json'))
ref=c['boards']['Kitchen-v2-redrawn.dc.html']; x=ref['x']+ref['w']+80
open(f'{base}/{fn}','w').write(G['HEADQ']%t+mb+'\n'+G['TAIL'])
c['boards'].pop(fn,None); c['order']=[o for o in c['order'] if o!=fn]
c['boards'][fn]={'x':x,'y':ref['y'],'w':390,'h':844,'title':t}; c['order'].append(fn)
json.dump(c,open(f'{base}/canvas.json','w'),ensure_ascii=False)
print('ok')
