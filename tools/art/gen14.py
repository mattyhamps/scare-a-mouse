import json, math, random
G0={'random':random,'math':math,'json':json}; G0['G']=G0
g12=open('./gen12.py').read()
exec(g12[:g12.index("# ---------- detailed Kitchens")], G0)
G=G0['G']
Q=G['Q']; sv=G['sv']; pill=G['pill']; TT=G['TT']; SC=G['SC']; nodes=G['nodes']
# the path now ends square at the doorway: it is drawn under the back wall, and a stone step sits at the threshold
road=G['crd']([(195,860),(150,780)]+G['pts']+[(222,250),(198,226),(195,196)])
STEP='<rect x="152" y="208" width="86" height="9" rx="3" fill="#a39c8f"/><rect x="152" y="214" width="86" height="5" rx="2" fill="#857e72"/>'
# ===== Kitchens v2: same layout and path as F3, every prop redrawn in one 3/4 top-down view.
# Rules: top faces lightest, front faces mid, right-hand side darkest (light from top-left);
# every floor object sits on one soft shadow; props share one scale (mouse = 36px).
WOOD=('#c58a55','#a06a3e','#7d5030'); DARK='#2e1c14'
def shadow(cx,cy,rx,ry=None): return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry or rx*0.32}" fill="#2a140a" opacity=".22"/>'
def barrel(x,y,s=1):
    return f'''<g transform="translate({x} {y}) scale({s})">{shadow(24,52,24,7)}
      <path d="M2 10 Q0 30 4 48 Q24 56 44 48 Q48 30 46 10 Z" fill="{Q["orange"]}"/><path d="M32 12 Q40 12 46 10 Q48 30 44 48 Q38 51 32 52 Q36 30 32 12 Z" fill="{Q["orange2"]}"/>
      <path d="M2 20 Q24 26 46 20 L46 25 Q24 31 2 25 Z" fill="#6a4228"/><path d="M3 38 Q24 44 45 38 L44 43 Q24 49 4 43 Z" fill="#6a4228"/>
      <ellipse cx="24" cy="10" rx="22" ry="8" fill="{WOOD[0]}"/><ellipse cx="24" cy="10" rx="17" ry="5.5" fill="none" stroke="{WOOD[1]}" stroke-width="2"/><path d="M14 6 L14 14 M24 5 L24 15 M34 6 L34 14" stroke="{WOOD[1]}" stroke-width="1.5"/></g>'''
def keg(x,y):   # a barrel lying on its side, end facing us
    return f'''<g transform="translate({x} {y})">{shadow(30,40,32,7)}<rect x="10" y="4" width="44" height="34" rx="14" fill="{Q["orange"]}"/><rect x="36" y="4" width="18" height="34" rx="10" fill="{Q["orange2"]}"/><rect x="22" y="4" width="5" height="34" fill="#6a4228"/><rect x="40" y="4" width="5" height="34" fill="#6a4228"/>
      <ellipse cx="12" cy="21" rx="10" ry="17" fill="{WOOD[0]}"/><ellipse cx="12" cy="21" rx="6" ry="11" fill="none" stroke="{WOOD[1]}" stroke-width="2"/><rect x="2" y="19" width="6" height="5" rx="1" fill="{Q["lav2"]}"/></g>'''
def table(x,y,w=124,d=62):
    top=f'<rect x="0" y="0" width="{w}" height="{d}" rx="5" fill="{WOOD[0]}"/>'+''.join(f'<rect x="0" y="{k*d/4}" width="{w}" height="1.6" fill="{WOOD[1]}" opacity=".55"/>' for k in (1,2,3))+f'<rect x="{w-10}" y="0" width="10" height="{d}" rx="4" fill="{WOOD[1]}" opacity=".45"/>'
    front=f'<rect x="0" y="{d-4}" width="{w}" height="14" rx="3" fill="{WOOD[1]}"/><rect x="6" y="{d+8}" width="9" height="18" fill="{WOOD[2]}"/><rect x="{w-15}" y="{d+8}" width="9" height="18" fill="{WOOD[2]}"/>'
    # food on top, each in the same 3/4 view
    board=f'<rect x="8" y="10" width="52" height="30" rx="6" fill="#d9b07a"/><rect x="8" y="34" width="52" height="6" rx="3" fill="#b8884f"/><circle cx="56" cy="25" r="3" fill="#b8884f"/>'
    loaf=f'<ellipse cx="30" cy="26" rx="18" ry="10" fill="#c88a3e"/><ellipse cx="28" cy="23" rx="16" ry="7.5" fill="#dca55a"/><path d="M20 19 l5 7 M28 17 l5 7 M36 18 l4 6" stroke="#b5762f" stroke-width="2.4" stroke-linecap="round"/>'
    knife=f'<rect x="64" y="34" width="22" height="4" rx="2" fill="#b9b6c2"/><rect x="84" y="33" width="12" height="6" rx="2" fill="{WOOD[2]}"/>'
    cheese=f'<ellipse cx="{w-34}" cy="22" rx="18" ry="8" fill="{Q["mustard"]}"/><path d="M{w-52} 22 L{w-52} 30 A18 8 0 0 0 {w-16} 30 L{w-16} 22 A18 8 0 0 1 {w-52} 22 Z" fill="{Q["mustard2"]}"/><path d="M{w-34} 22 L{w-20} 17 A18 8 0 0 1 {w-16} 22 Z" fill="#f0d07a"/>'
    apples=''.join(f'<circle cx="{ax}" cy="{ay}" r="6" fill="{Q["coral"]}"/><path d="M{ax} {ay-6} A6 6 0 0 1 {ax+6} {ay} A6 6 0 0 1 {ax+2} {ay+5.6} A7 7 0 0 0 {ax+3} {ay} Z" fill="{Q["coral2"]}"/><circle cx="{ax-2}" cy="{ay-2}" r="1.6" fill="{Q["pink"]}"/>' for ax,ay in ((w-46,44),(w-34,47),(w-40,40)))
    jug=f'<g transform="translate({w-22} 30)"><path d="M14 6 C22 6 22 18 14 18" fill="none" stroke="{Q["navy2"]}" stroke-width="3"/><rect x="0" y="2" width="16" height="22" rx="6" fill="{Q["navy"]}"/><rect x="9" y="2" width="7" height="22" rx="3" fill="{Q["navy2"]}"/><ellipse cx="8" cy="3" rx="8" ry="3" fill="#1c2d52"/></g>'
    return f'<g transform="translate({x} {y})">{shadow(w/2,d+26,w/2+6,8)}{front}{top}{board}{loaf}{knife}{cheese}{apples}{jug}</g>'
def basket_bed(x,y):
    weave=''.join(f'<path d="M{8+k*8} 26 l4 8" stroke="#a87a42" stroke-width="2" stroke-linecap="round"/>' for k in range(8))
    return f'''<g transform="translate({x} {y})">{shadow(40,42,40,9)}<ellipse cx="40" cy="28" rx="38" ry="16" fill="#b9874a"/><path d="M2 28 A38 16 0 0 0 78 28 L78 32 A38 16 0 0 1 2 32 Z" fill="#9a6c36"/>{weave}
      <ellipse cx="40" cy="22" rx="32" ry="12" fill="#d8a964"/><ellipse cx="40" cy="22" rx="26" ry="9" fill="{Q["coral"]}"/><path d="M40 13 A26 9 0 0 1 66 22 A26 9 0 0 1 52 30 A30 10 0 0 0 58 22 Z" fill="{Q["coral2"]}"/></g>'''
def sack(x,y,top=None,s=1):
    top=top or Q['cream']
    return f'''<g transform="translate({x} {y}) scale({s})">{shadow(22,50,22,6)}<path d="M4 48 C-2 34 2 20 10 14 L34 14 C42 20 46 34 40 48 Z" fill="{Q["tan"]}"/><path d="M28 14 L34 14 C42 20 46 34 40 48 L30 48 C36 34 34 22 28 14 Z" fill="{Q["tan2"]}"/>
      <path d="M10 14 C10 8 34 8 34 14 C34 18 10 18 10 14 Z" fill="#c9a777"/><ellipse cx="22" cy="12" rx="10" ry="3.6" fill="{top}"/><rect x="6" y="28" width="32" height="5" rx="2" fill="{Q["coral"]}" opacity=".85"/></g>'''
def spill(x,y): return f'<g transform="translate({x} {y})"><ellipse cx="0" cy="0" rx="16" ry="5" fill="{Q["cream"]}"/><circle cx="20" cy="2" r="2" fill="{Q["cream"]}"/><circle cx="26" cy="-1" r="1.4" fill="{Q["cream"]}"/></g>'
def crate(x,y,kind):
    w,d,h=66,34,22
    box=f'<rect x="0" y="{d-2}" width="{w}" height="{h}" rx="2" fill="{WOOD[1]}"/><rect x="0" y="{d+8}" width="{w}" height="3" fill="{WOOD[2]}"/><rect x="{w-10}" y="{d-2}" width="10" height="{h}" fill="{WOOD[2]}"/><rect x="0" y="0" width="{w}" height="{d}" rx="3" fill="{WOOD[2]}"/><rect x="4" y="4" width="{w-8}" height="{d-8}" rx="2" fill="#4a2e1c"/>'
    if kind=='cabbage':
        fill=''.join(f'<circle cx="{cx}" cy="{cy}" r="10" fill="{Q["green"]}"/><path d="M{cx} {cy-10} A10 10 0 0 1 {cx+10} {cy} A10 10 0 0 1 {cx+3} {cy+9.5} A11 11 0 0 0 {cx+4} {cy} Z" fill="{Q["green2"]}"/><path d="M{cx-5} {cy-2} Q{cx} {cy-6} {cx+4} {cy-1}" stroke="#8fb85a" stroke-width="2" fill="none"/>' for cx,cy in ((14,14),(33,12),(52,15),(24,24),(44,24)))
    else:
        fill=''.join(f'<path d="M{cx} {cy} L{cx+22} {cy-4} L{cx+22} {cy+4} Z" fill="{Q["orange"]}"/><path d="M{cx} {cy} L{cx+22} {cy+1} L{cx+22} {cy+4} Z" fill="{Q["orange2"]}"/><path d="M{cx+22} {cy} l6 -5 M{cx+22} {cy} l7 0 M{cx+22} {cy} l6 5" stroke="{Q["green"]}" stroke-width="2.4" stroke-linecap="round"/>' for cx,cy in ((6,10),(30,12),(10,20),(32,22),(16,28)))
    return f'<g transform="translate({x} {y})">{shadow(w/2,d+h+2,w/2+4,7)}{box}<g>{fill}</g></g>'
def tub(x,y):
    staves=''.join(f'<rect x="{6+k*10}" y="22" width="1.6" height="22" fill="{WOOD[2]}" opacity=".6"/>' for k in range(6))
    return f'''<g transform="translate({x} {y})">{shadow(36,48,38,8)}<path d="M2 20 L8 44 Q36 52 64 44 L70 20 Z" fill="{WOOD[1]}"/><path d="M52 21 L70 20 L64 44 Q58 46 50 47 Z" fill="{WOOD[2]}"/>{staves}<path d="M4 28 Q36 36 68 28 L67 33 Q36 41 5 33 Z" fill="{Q["lav2"]}"/>
      <ellipse cx="36" cy="20" rx="34" ry="12" fill="{WOOD[0]}"/><ellipse cx="36" cy="21" rx="28" ry="8.5" fill="#6f9bb3"/><path d="M36 12.5 A28 8.5 0 0 1 64 21 A28 8.5 0 0 1 50 28.5 A30 9 0 0 0 56 21 Z" fill="#5a879f"/><path d="M22 19 q6 -3 12 0 M40 23 q5 -2 10 0" stroke="#a9cbe0" stroke-width="2" fill="none" stroke-linecap="round"/></g>'''
def bucket(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(14,30,15,5)}<path d="M2 8 L5 28 Q14 32 23 28 L26 8 Z" fill="{WOOD[1]}"/><path d="M18 9 L26 8 L23 28 Q20 29.6 17 30 Z" fill="{WOOD[2]}"/><rect x="2" y="16" width="24" height="3" fill="{Q["lav2"]}"/><ellipse cx="14" cy="8" rx="12" ry="4.5" fill="{WOOD[0]}"/><ellipse cx="14" cy="8.5" rx="9" ry="3" fill="#6f9bb3"/><path d="M2 8 Q14 -10 26 8" fill="none" stroke="{Q["lav2"]}" stroke-width="2"/></g>'''
def broom(x,y):
    return f'<g transform="translate({x} {y}) rotate(-18)">{shadow(6,96,16,4)}<rect x="4" y="0" width="5" height="70" rx="2" fill="{WOOD[1]}"/><path d="M-6 68 L19 68 L24 96 L-11 96 Z" fill="#d9b46a"/><path d="M8 68 L19 68 L24 96 L10 96 Z" fill="#b8924a"/><rect x="-6" y="70" width="25" height="4" fill="{Q["coral2"]}"/></g>'
def logs(x,y):
    def end(cx,cy): return f'<circle cx="{cx}" cy="{cy}" r="10" fill="#d9b07a"/><circle cx="{cx}" cy="{cy}" r="6" fill="none" stroke="#b8884f" stroke-width="1.6"/><path d="M{cx} {cy-10} A10 10 0 0 1 {cx+10} {cy} A10 10 0 0 1 {cx+3} {cy+9.5} A11 11 0 0 0 {cx+5} {cy} Z" fill="{WOOD[2]}"/>'
    body=''.join(f'<rect x="{cx}" y="{cy-10}" width="40" height="20" rx="4" fill="{WOOD[1]}"/><rect x="{cx}" y="{cy+2}" width="40" height="8" rx="3" fill="{WOOD[2]}"/>' for cx,cy in ((10,40),(30,40),(20,22)))
    return f'<g transform="translate({x} {y})">{shadow(40,52,40,7)}{body}{end(10,40)}{end(30,40)}{end(20,22)}<rect x="40" y="30" width="34" height="20" rx="4" fill="{WOOD[1]}"/><rect x="40" y="42" width="34" height="8" rx="3" fill="{WOOD[2]}"/>{end(50,40)}</g>'
def stool(x,y):
    return f'<g transform="translate({x} {y})">{shadow(16,34,18,5)}<rect x="4" y="12" width="5" height="20" fill="{WOOD[2]}"/><rect x="23" y="12" width="5" height="20" fill="{WOOD[2]}"/><ellipse cx="16" cy="14" rx="16" ry="6" fill="{WOOD[1]}"/><ellipse cx="16" cy="11" rx="16" ry="6" fill="{WOOD[0]}"/></g>'
def sconce(x,y,flip=False):
    return f'''<g transform="translate({x} {y})"><rect x="0" y="16" width="12" height="18" rx="2" fill="{Q["lav2"]}"/><rect x="4" y="10" width="5" height="14" rx="2" fill="{WOOD[2]}"/>
      <circle cx="6" cy="4" r="16" fill="{Q["mustard"]}" opacity=".16"/><path d="M6 -6 C0 0 1 9 6 9 C11 9 12 0 6 -6 Z" fill="{Q["mustard"]}"/><path d="M6 0 C4 3 4.5 7 6 7 C7.5 7 8 3 6 0 Z" fill="{Q["coral"]}"/></g>'''
# ----- back wall (elevation) — hearth built into the wall, door, window, pot rail
def stones(w,h,seed):
    r=random.Random(seed); out=''
    for row,yy in enumerate(range(6,h,22)):
        xx=-(row%2)*18
        while xx<w:
            ww=r.choice((30,36,42)); out+=f'<rect x="{xx+2}" y="{yy}" width="{ww-4}" height="17" rx="3" fill="#978f83" opacity=".45"/>'; xx+=ww
    return out
def pot_hanging(x,y,c,c2,r=12):
    return f'<g transform="translate({x} {y})"><rect x="-1" y="0" width="2" height="10" fill="{DARK}"/><rect x="-{r}" y="10" width="{2*r}" height="{r+4}" rx="{r*0.6}" fill="{c}"/><rect x="2" y="10" width="{r-2}" height="{r+4}" rx="{r*0.5}" fill="{c2}"/><rect x="-{r+3}" y="9" width="{2*r+6}" height="4" rx="2" fill="{c2}"/></g>'
def hearth_wall():
    return f'''<g>
      <rect x="18" y="58" width="134" height="156" fill="#8f877a"/><rect x="122" y="58" width="30" height="156" fill="#7a7266"/>
      {''.join(f'<rect x="{22+(r%2)*16+k*32}" y="{64+r*18}" width="26" height="13" rx="2" fill="#a39b8e"/>' for r in range(3) for k in range(4) if 22+(r%2)*16+k*32<120)}
      <rect x="8" y="112" width="154" height="14" rx="3" fill="{WOOD[1]}"/><rect x="8" y="122" width="154" height="4" fill="{WOOD[2]}"/>
      {''.join(f'<g transform="translate({jx} 92)"><rect x="0" y="{20-h}" width="14" height="{h}" rx="4" fill="{c}"/><rect x="8" y="{20-h}" width="6" height="{h}" rx="3" fill="{c2}"/></g>' for jx,h,c,c2 in ((20,18,Q["cream"],Q["cream2"]),(40,14,Q["coral"],Q["coral2"]),(60,20,Q["olive"],Q["olive2"]),(118,16,Q["navy"],Q["navy2"]),(138,12,Q["mustard"],Q["mustard2"])))}
      <path d="M36 214 L36 160 C36 134 134 134 134 160 L134 214 Z" fill="{DARK}"/>
      <path d="M54 210 C50 192 64 184 70 172 C72 186 86 190 80 210 Z" fill="{Q["mustard"]}"/><path d="M66 210 C64 198 70 192 72 186 C77 194 80 200 76 210 Z" fill="{Q["coral"]}"/><path d="M86 210 C84 198 92 192 94 186 C97 196 102 200 98 210 Z" fill="{Q["mustard"]}"/>
      <rect x="44" y="206" width="82" height="8" rx="2" fill="#4a3226"/>
      <rect x="83" y="138" width="3" height="22" fill="{DARK}"/><path d="M60 160 L110 160 Q112 184 85 190 Q58 184 60 160 Z" fill="#4a4652"/><path d="M92 160 L110 160 Q112 184 90 190 Q100 180 92 160 Z" fill="#35323c"/><rect x="56" y="156" width="58" height="7" rx="3" fill="#5a5664"/><ellipse cx="85" cy="158" rx="25" ry="3" fill="{Q["olive"]}"/>
      <ellipse cx="78" cy="146" rx="8" ry="5" fill="#fff" opacity=".55"/><ellipse cx="88" cy="134" rx="6" ry="4" fill="#fff" opacity=".35"/></g>'''
def window(x,y):
    return f'<g transform="translate({x} {y})"><rect x="-6" y="-6" width="58" height="82" rx="29" fill="#7a7266"/><rect x="0" y="0" width="46" height="70" rx="23" fill="#9cb8c8"/><path d="M23 0 A23 23 0 0 1 46 23 L46 70 L32 70 L32 8 Z" fill="#86a5b8"/><rect x="21" y="0" width="4" height="70" fill="#7a7266"/><rect x="0" y="32" width="46" height="4" fill="#7a7266"/><rect x="-10" y="66" width="66" height="9" rx="3" fill="{WOOD[1]}"/><rect x="-4" y="56" width="12" height="12" rx="3" fill="{Q["coral"]}"/><path d="M-2 56 l4 -8 l4 8" fill="{Q["green"]}"/></g>'
def door():
    return f'''<rect x="158" y="114" width="74" height="100" rx="4" fill="#7a7266"/><path d="M164 214 L164 150 C164 118 226 118 226 150 L226 214 Z" fill="{Q["brown"]}"/><path d="M195 122 C214 124 226 136 226 150 L226 214 L195 214 Z" fill="{Q["brown2"]}"/><rect x="164" y="160" width="62" height="5" fill="{Q["brown2"]}"/><rect x="164" y="188" width="62" height="5" fill="{Q["brown2"]}"/><circle cx="212" cy="176" r="4" fill="{Q["mustard"]}"/>'''
def pot_rail():
    return f'<rect x="246" y="64" width="130" height="5" rx="2" fill="{DARK}"/>'+pot_hanging(262,67,'#c2723a','#a25a2a',11)+pot_hanging(292,67,'#4a4652','#35323c',13)+pot_hanging(324,67,'#c2723a','#a25a2a',10)+pot_hanging(354,67,'#8a8794','#6e6b78',12)
def herbs_hang(x,y):
    return f'<g transform="translate({x} {y})"><rect x="0" y="0" width="56" height="4" rx="2" fill="{WOOD[2]}"/>'+''.join(f'<rect x="{6+k*16}" y="4" width="2" height="8" fill="{WOOD[2]}"/><path d="M{1+k*16} 12 L{13+k*16} 12 L{7+k*16} 32 Z" fill="{c}"/><path d="M{7+k*16} 12 L{13+k*16} 12 L{7+k*16} 32 Z" fill="{c2}"/>' for k,(c,c2) in enumerate([(Q["green"],Q["green2"]),(Q["olive"],Q["olive2"]),(Q["green"],Q["green2"])]))+'</g>'
# ----- floor: large flagstones, low contrast
fr=random.Random(5)
floor=f'<rect x="0" y="214" width="390" height="630" fill="#a85e36"/>'
for row,yy in enumerate(range(214,844,46)):
    xx=-(row%2)*30
    while xx<390:
        ww=fr.choice((52,60,68)); floor+=f'<rect x="{xx+2}" y="{yy+2}" width="{ww-4}" height="42" rx="5" fill="{"#b2673d" if fr.random()<.5 else "#ad633a"}"/>'; xx+=ww
WALL=f'''<rect x="0" y="0" width="390" height="214" fill="{Q["lav"]}"/>{stones(390,214,3)}
  {hearth_wall()}{door()}{window(290,108)}{pot_rail()}{herbs_hang(240,60) if False else ''}
  <rect x="0" y="206" width="390" height="8" fill="{Q["lav2"]}"/><rect x="0" y="214" width="390" height="14" fill="#2a140a" opacity=".14"/>
  <rect x="34" y="214" width="102" height="16" rx="3" fill="#8f877a"/><rect x="34" y="226" width="102" height="4" fill="#7a7266"/>'''
PATH=f'''<path d="{road}" fill="none" stroke="#c9a77a" stroke-width="44" stroke-linecap="round" transform="translate(0 3)"/><path d="{road}" fill="none" stroke="{Q["cream"]}" stroke-width="40" stroke-linecap="round"/><path d="{road}" fill="none" stroke="#f6ecd4" stroke-width="14" stroke-linecap="round"/>'''
PROPS=''.join([
    # upper left: barrels and a keg
    barrel(22,238), barrel(66,232), barrel(44,270,.95), keg(104,286),
    # right of the top bend
    bucket(338,300),
    # work table on the right
    table(252,398),
    stool(196,424),
    # cat basket and sacks lower left
    basket_bed(14,520), sack(10,586), sack(48,596,Q["mustard"],.9), spill(100,654),
    # bottom right: crates, washtub, broom
    crate(304,606,'cabbage'), crate(236,716,'carrot'), tub(306,712), bucket(338,780),
    # bottom left: firewood
    logs(8,770),
])
SCONCES=sconce(0,330)+sconce(378,520)+sconce(0,690)
b=f'''<div style="{SC}background:#a85e36">
  <svg width="390" height="844" style="position:absolute;left:0;top:0">{floor}{PATH}{WALL}{STEP}
    <rect x="0" y="214" width="10" height="630" fill="{Q["lav2"]}"/><rect x="380" y="214" width="10" height="630" fill="{Q["lav2"]}"/>
    {PROPS}{SCONCES}
  </svg>
  <div style="position:absolute;left:0;right:0;top:0;height:56px;background:{Q["purple"]};z-index:4">
    {pill(14,8,98,40,Q["mustard"],Q["mustard2"],'Castle',16)}<div style="position:absolute;left:126px;top:12px;{TT};font-size:24px;color:{Q["cream"]}">Kitchens</div><b style="position:absolute;right:16px;top:18px;font:700 15px Fredoka,sans-serif;color:{Q["cream"]}">7/30</b></div>
  {nodes(171)}
  <div style="position:absolute;left:122px;top:430px;z-index:4">{sv('mouse',36)}</div>
  <div style="position:absolute;left:36px;top:506px;z-index:2">{sv('cat',38)}</div>
</div>'''
if __name__=="__main__" and "KMAIN" not in globals():
  pass
base="/home/claude/mockups/project"; fn="Kitchen-v2-redrawn.dc.html"; t='K2 · Kitchens: F3 layout, props redrawn'
c=json.load(open(f'{base}/canvas.json'))
ref=c['boards']['Kitchen-concept-shelves.dc.html']; x=ref['x']+ref['w']+80
open(f'{base}/{fn}','w').write(G['HEADQ']%t+b+'\n'+G['TAIL'])
c['boards'].pop(fn,None); c['order']=[o for o in c['order'] if o!=fn]
c['boards'][fn]={'x':x,'y':ref['y'],'w':390,'h':844,'title':t}; c['order'].append(fn)
json.dump(c,open(f'{base}/canvas.json','w'),ensure_ascii=False)
print('ok')
