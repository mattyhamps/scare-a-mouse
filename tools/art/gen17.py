import json, math, random
g16=open('./gen16.py').read()
exec(g16[:g16.index("rooms={")])
# ================= Cellars floor: Storeroom, Wine cellar, Dungeon (Kitchens = K2)
def plank_floor(c1,c2,seam,seed):
    r=random.Random(seed); g=f'<rect x="0" y="214" width="390" height="630" fill="{c1}"/>'
    for row,yy in enumerate(range(214,844,24)):
        g+=f'<rect x="0" y="{yy}" width="390" height="2" fill="{seam}"/>'
        if row%2: g+=f'<rect x="0" y="{yy+2}" width="390" height="22" fill="{c2}"/>'
        xx=r.randint(-60,0)
        while xx<390:
            xx+=r.choice((90,120,150)); g+=f'<rect x="{xx}" y="{yy}" width="2" height="24" fill="{seam}"/>'
    return g
def flag_floor(cs,seed,base):
    r=random.Random(seed); g=f'<rect x="0" y="214" width="390" height="630" fill="{base}"/>'
    for row,yy in enumerate(range(214,844,46)):
        xx=-(row%2)*30
        while xx<390:
            ww=r.choice((52,60,68)); g+=f'<rect x="{xx+2}" y="{yy+2}" width="{ww-4}" height="42" rx="5" fill="{r.choice(cs)}"/>'; xx+=ww
    return g
def road_stone(c,c2,edge):
    return f'<path d="{road}" fill="none" stroke="{edge}" stroke-width="44" stroke-linecap="round" transform="translate(0 3)"/><path d="{road}" fill="none" stroke="{c}" stroke-width="40" stroke-linecap="round"/><path d="{road}" fill="none" stroke="{c2}" stroke-width="40" stroke-dasharray="2 24"/>'
def iron_door(x=164,w=62,wood=None,grille=False):
    wood=wood or (Q["brown"],Q["brown2"])
    d=gate_arch(x,w,wood)
    d+=''.join(f'<rect x="{x}" y="{yy}" width="{w}" height="5" fill="#4a4652"/>' for yy in (146,176,202))+''.join(f'<circle cx="{x+6+k*12.5}" cy="{yy+2.5}" r="1.6" fill="#8a8794"/>' for yy in (146,176,202) for k in range(5))
    if grille: d+=f'<rect x="{x+19}" y="134" width="24" height="10" rx="2" fill="#2e1c14"/>'+''.join(f'<rect x="{x+22+k*7}" y="134" width="2" height="10" fill="#8a8794"/>' for k in range(3))
    return d+f'<circle cx="{x+w-10}" cy="168" r="4" fill="{Q["mustard"]}"/>'
def lantern(x,y,chain=20):
    return f'''<g transform="translate({x} {y})"><rect x="-1" y="0" width="2" height="{chain}" fill="{DARK}"/><circle cx="0" cy="{chain+16}" r="26" fill="{Q["mustard"]}" opacity=".14"/>
      <path d="M-8 {chain} L8 {chain} L5 {chain+4} L-5 {chain+4} Z" fill="#3a3644"/><rect x="-8" y="{chain+4}" width="16" height="20" rx="3" fill="#3a3644"/><rect x="-5" y="{chain+7}" width="10" height="14" rx="2" fill="{Q["mustard"]}"/><rect x="0" y="{chain+7}" width="5" height="14" rx="1" fill="#e0b85a"/><rect x="-9" y="{chain+23}" width="18" height="4" rx="2" fill="#3a3644"/></g>'''
def crate_closed(x,y,w=48,d=22,h=34,s=1):
    planks=''.join(f'<rect x="0" y="{d-2+k*h/3}" width="{w}" height="1.6" fill="{WOOD[2]}"/>' for k in (1,2))
    top=f'<rect x="0" y="0" width="{w}" height="{d}" rx="2" fill="{WOOD[0]}"/>'+''.join(f'<rect x="{k*w/4}" y="0" width="1.4" height="{d}" fill="{WOOD[1]}"/>' for k in (1,2,3))
    return f'<g transform="translate({x} {y}) scale({s})">{shadow(w/2+3,d+h,w/2+6,6)}<rect x="0" y="{d-2}" width="{w}" height="{h}" rx="2" fill="{WOOD[1]}"/>{planks}<path d="M3 {d+1} L{w-12} {d+h-4} M3 {d+h-4} L{w-12} {d+1}" stroke="{WOOD[2]}" stroke-width="3"/><rect x="{w-10}" y="{d-2}" width="10" height="{h}" fill="{WOOD[2]}"/>{top}</g>'
def chest(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(36,56,40,7)}<rect x="0" y="22" width="72" height="34" rx="3" fill="{WOOD[1]}"/><rect x="54" y="22" width="18" height="34" rx="3" fill="{WOOD[2]}"/>
      <path d="M0 24 L0 14 Q36 -6 72 14 L72 24 Z" fill="{WOOD[0]}"/><path d="M54 4 Q66 8 72 14 L72 24 L54 24 Z" fill="{WOOD[1]}"/>
      {''.join(f'<rect x="{bx}" y="4" width="6" height="52" fill="#4a4652"/>' for bx in (10,56))}<rect x="0" y="22" width="72" height="4" fill="#4a4652"/>
      <rect x="31" y="22" width="12" height="14" rx="2" fill="{Q["mustard"]}"/><rect x="36" y="27" width="2" height="5" fill="{DARK}"/></g>'''
def cheese_stack(x,y):
    def wheel(dy,w=44): return f'<path d="M0 {dy+8} L0 {dy+18} A{w/2} 7 0 0 0 {w} {dy+18} L{w} {dy+8} Z" fill="{Q["mustard2"]}"/><ellipse cx="{w/2}" cy="{dy+8}" rx="{w/2}" ry="7" fill="{Q["mustard"]}"/><path d="M{w*0.7} {dy+12} L{w} {dy+12} L{w} {dy+18} A{w/2} 7 0 0 1 {w*0.7} {dy+24} Z" fill="#a87a24" opacity=".35"/>'
    wedge=f'<g transform="translate(46 22)"><path d="M0 18 L0 8 L24 0 L24 10 Z" fill="{Q["mustard2"]}"/><path d="M0 8 L24 0 L30 4 L6 12 Z" fill="#f0d07a"/><path d="M0 8 L6 12 L6 22 L0 18 Z" fill="{Q["mustard"]}"/><circle cx="12" cy="12" r="2" fill="#a87a24"/></g>'
    return f'<g transform="translate({x} {y})">{shadow(30,44,36,6)}{wheel(18)}{wheel(4)}{wheel(-10,40).replace("cx=\"22.0\"","cx=\"22\"")}{wedge}</g>'
def rope(x,y):
    return f'<g transform="translate({x} {y})">{shadow(20,20,22,5)}<ellipse cx="20" cy="14" rx="20" ry="8" fill="#b9874a"/><ellipse cx="20" cy="12" rx="20" ry="8" fill="#d8a964"/>'+''.join(f'<ellipse cx="20" cy="12" rx="{r}" ry="{r*0.4}" fill="none" stroke="#b9874a" stroke-width="2"/>' for r in (15,10,5))+'<path d="M38 14 q10 4 12 12" stroke="#d8a964" stroke-width="4" fill="none" stroke-linecap="round"/></g>'
def mousehole(x,y): return f'<path d="M{x} {y} L{x} {y-12} A9 9 0 0 1 {x+18} {y-12} L{x+18} {y} Z" fill="{DARK}"/><rect x="{x-2}" y="{y-1}" width="22" height="2" fill="#6e675d"/>'
def cobweb(x,y,flip=1):
    s=f'<g transform="translate({x} {y}) scale({flip} 1)" stroke="{Q["cream"]}" stroke-width="1.2" fill="none" opacity=".55">'
    s+=''.join(f'<path d="M0 0 L{40*math.cos(a)} {40*math.sin(a)}"/>' for a in (0.1,0.6,1.1,1.5))
    s+=''.join(f'<path d="M{r*math.cos(.1)} {r*math.sin(.1)} Q{r*0.7} {r*0.4} {r*math.cos(.6)} {r*math.sin(.6)} Q{r*0.5} {r*0.8} {r*math.cos(1.1)} {r*math.sin(1.1)} Q{r*0.2} {r*0.95} {r*math.cos(1.5)} {r*math.sin(1.5)}"/>' for r in (14,26,38))
    return s+'</g>'
def wall_shelf(x,y,w,items):
    s=f'<g transform="translate({x} {y})"><rect x="0" y="0" width="{w}" height="8" rx="2" fill="{WOOD[1]}"/><rect x="0" y="6" width="{w}" height="3" fill="{WOOD[2]}"/><path d="M8 9 L20 9 L8 22 Z M{w-8} 9 L{w-20} 9 L{w-8} 22 Z" fill="{WOOD[2]}"/>'
    xx=6
    for kind,c,c2 in items:
        if kind=='jar': s+=f'<rect x="{xx}" y="-18" width="14" height="18" rx="4" fill="{c}"/><rect x="{xx+8}" y="-18" width="6" height="18" rx="3" fill="{c2}"/><rect x="{xx+1}" y="-21" width="12" height="4" rx="1" fill="{WOOD[2]}"/>'; xx+=18
        elif kind=='box': s+=f'<rect x="{xx}" y="-16" width="22" height="16" rx="2" fill="{c}"/><rect x="{xx+15}" y="-16" width="7" height="16" fill="{c2}"/>'; xx+=26
        elif kind=='bottle': s+=f'<rect x="{xx+3}" y="-26" width="4" height="8" fill="{c2}"/><rect x="{xx}" y="-20" width="10" height="20" rx="4" fill="{c}"/><rect x="{xx+6}" y="-20" width="4" height="20" rx="2" fill="{c2}"/>'; xx+=14
        elif kind=='cheese': s+=f'<path d="M{xx} 0 L{xx} -10 L{xx+22} -16 L{xx+22} 0 Z" fill="{Q["mustard"]}"/><path d="M{xx+14} -14 L{xx+22} -16 L{xx+22} 0 L{xx+14} 0 Z" fill="{Q["mustard2"]}"/>'; xx+=26
    return s+'</g>'
def indoor_wall(base,shade,seed,h=214):
    return f'<rect x="0" y="0" width="390" height="{h}" fill="{base}"/>{stones(390,h,seed)}<rect x="0" y="{h-8}" width="390" height="8" fill="{shade}"/>'
FLOORSHADE='<rect x="0" y="214" width="390" height="16" fill="#1a0c06" opacity=".18"/>'
SIDE=lambda c: f'<rect x="0" y="214" width="10" height="630" fill="{c}"/><rect x="380" y="214" width="10" height="630" fill="{c}"/>'
# ---------- STOREROOM
def storeroom():
    wall=indoor_wall(Q["lav"],Q["lav2"],21)
    wall+=wall_shelf(14,120,130,[('jar',Q["cream"],Q["cream2"]),('jar',Q["coral"],Q["coral2"]),('box',Q["tan"],Q["tan2"]),('cheese',0,0),('jar',Q["olive"],Q["olive2"])])
    wall+=wall_shelf(14,170,130,[('box',Q["tan"],Q["tan2"]),('box',WOOD[0],WOOD[1]),('jar',Q["navy"],Q["navy2"]),('jar',Q["mustard"],Q["mustard2"])])
    wall+=wall_shelf(248,120,130,[('bottle',Q["green"],Q["green2"]),('bottle',Q["coral"],Q["coral2"]),('box',Q["tan"],Q["tan2"]),('jar',Q["cream"],Q["cream2"]),('jar',Q["pink"],Q["pink2"])])
    wall+=wall_shelf(248,170,130,[('cheese',0,0),('cheese',0,0),('box',Q["tan"],Q["tan2"]),('jar',Q["olive"],Q["olive2"])])
    wall+=f'<rect x="152" y="106" width="86" height="108" fill="{Q["lav2"]}"/>'+iron_door()+mousehole(130,206)+cobweb(0,0)+cobweb(390,0,-1)
    floor=flag_floor(('#8e897d','#918c80','#8b8679'),3,'#77736a')+FLOORSHADE+SIDE(Q["lav2"])
    props=''.join([crate_closed(18,250), crate_closed(70,244,44), crate_closed(40,226,40,20,26,.9) if False else '', sack(118,276,Q["cream"],.9),
        barrel(330,232,.8),
        chest(286,410), cheese_stack(204,410) if False else '', rope(200,430),
        sack(14,520), sack(48,532,Q["mustard"],.9), cheese_stack(20,590),
        crate_closed(306,600,52), crate_closed(312,566,40,18,26,.85) if False else '',
        barrel(238,720,.9), barrel(286,736,.9), crate_closed(330,720,40), cheese_stack(250,786) if False else '',
        crate_closed(14,760,48), sack(70,784,Q["cream"],.85)])
    return page('Storeroom','5/20',101,'#77736a',floor,wall,road_stone('#ecdcb4','#d9c393','#a8926a'),props)
# ---------- WINE CELLAR
BRICK=('#9a5a44','#7d4636','#6a3a2c')
def brick_wall(seed):
    r=random.Random(seed); s=f'<rect x="0" y="0" width="390" height="214" fill="{BRICK[1]}"/>'
    for row,yy in enumerate(range(0,214,14)):
        xx=-(row%2)*14
        while xx<390: s+=f'<rect x="{xx+1.5}" y="{yy+1.5}" width="25" height="11" rx="1.5" fill="{r.choice((BRICK[0],BRICK[0],"#a3634c"))}"/>'; xx+=28
    return s
def bottle_rack_front(w,h,rows,cols):
    s=''
    for r_ in range(rows):
        for c_ in range(cols):
            cx=8+c_*(w-16)/(cols-1); cy=8+r_*(h-16)/(rows-1)
            s+=f'<circle cx="{cx}" cy="{cy}" r="5.6" fill="#2e1c14"/><circle cx="{cx}" cy="{cy}" r="3.6" fill="{Q["green2"] if (r_+c_)%3 else BRICK[2]}"/><circle cx="{cx-1}" cy="{cy-1}" r="1.2" fill="{Q["cream"]}" opacity=".6"/>'
    return s
def rack(x,y,w=70,d=18,h=64):
    return f'''<g transform="translate({x} {y})">{shadow(w/2+4,d+h+2,w/2+8,7)}<rect x="0" y="{d-2}" width="{w}" height="{h}" rx="2" fill="{WOOD[2]}"/><g transform="translate(2 {d})">{bottle_rack_front(w-4,h-4,4,5)}</g><rect x="{w-6}" y="{d-2}" width="6" height="{h}" fill="#4a2e1c"/>
      <rect x="0" y="0" width="{w}" height="{d}" rx="2" fill="{WOOD[1]}"/>{''.join(f'<circle cx="{8+k*13}" cy="{d/2}" r="3.4" fill="{Q["green2"]}"/>' for k in range(5))}</g>'''
def tun(x,y,s=1):
    return f'''<g transform="translate({x} {y}) scale({s})">{shadow(56,82,58,9)}<rect x="30" y="6" width="80" height="70" rx="22" fill="{Q["orange"]}"/><rect x="80" y="6" width="30" height="70" rx="16" fill="{Q["orange2"]}"/>{''.join(f'<rect x="{bx}" y="6" width="6" height="70" fill="#6a4228"/>' for bx in (52,84))}
      <rect x="40" y="72" width="8" height="12" fill="{WOOD[2]}"/><rect x="92" y="72" width="8" height="12" fill="{WOOD[2]}"/>
      <ellipse cx="34" cy="41" rx="24" ry="35" fill="{WOOD[0]}"/><ellipse cx="34" cy="41" rx="17" ry="27" fill="none" stroke="{WOOD[1]}" stroke-width="2.4"/><ellipse cx="34" cy="41" rx="24" ry="35" fill="none" stroke="#6a4228" stroke-width="4"/>
      <rect x="28" y="54" width="12" height="6" rx="2" fill="{Q["mustard"]}"/><rect x="31" y="58" width="5" height="8" fill="{Q["mustard2"]}"/><ellipse cx="34" cy="86" rx="8" ry="3" fill="{BRICK[2]}" opacity=".8"/></g>'''
def grapes(x,y):
    bunch=lambda bx,by,c,c2: ''.join(f'<circle cx="{bx+dx}" cy="{by+dy}" r="4.4" fill="{c if (dx+dy)%2 else c2}"/>' for dx,dy in ((0,0),(8,0),(16,0),(4,7),(12,7),(8,14)))
    return f'<g transform="translate({x} {y})">{shadow(22,34,24,5)}<path d="M2 14 L42 14 L38 34 L6 34 Z" fill="#c99a56"/><path d="M28 14 L42 14 L38 34 L28 34 Z" fill="#a87a42"/><ellipse cx="22" cy="14" rx="20" ry="5" fill="#d9b06a"/>{bunch(6,4,"#7a4a7a","#5e3460")}{bunch(20,6,Q["olive"],Q["olive2"])}<path d="M18 2 l3 -5" stroke="{Q["green2"]}" stroke-width="2"/></g>'
def candle_table(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(26,46,28,6)}<rect x="22" y="18" width="8" height="28" fill="{WOOD[2]}"/><rect x="10" y="42" width="32" height="5" rx="2" fill="{WOOD[2]}"/><ellipse cx="26" cy="18" rx="26" ry="9" fill="{WOOD[1]}"/><ellipse cx="26" cy="15" rx="26" ry="9" fill="{WOOD[0]}"/>
      <circle cx="18" cy="2" r="18" fill="{Q["mustard"]}" opacity=".16"/><rect x="14" y="2" width="8" height="14" rx="2" fill="{Q["cream"]}"/><path d="M18 -8 C14 -2 16 2 18 2 C20 2 22 -2 18 -8 Z" fill="{Q["mustard"]}"/>
      <g transform="translate(30 0)"><rect x="3" y="-6" width="4" height="8" fill="{BRICK[2]}"/><rect x="0" y="0" width="10" height="14" rx="4" fill="#5e3460"/></g></g>'''
def wine_cellar():
    wall=brick_wall(5)
    for ax in (16,262):
        wall+=f'<path d="M{ax} 214 L{ax} 92 Q{ax} 52 {ax+56} 52 Q{ax+112} 52 {ax+112} 92 L{ax+112} 214 Z" fill="#3a2018"/><g transform="translate({ax+8} 74)">{bottle_rack_front(96,130,6,7)}</g>'
        wall+=f'<path d="M{ax-8} 214 L{ax-8} 92 Q{ax-8} 44 {ax+56} 44 Q{ax+120} 44 {ax+120} 92 L{ax+120} 214 L{ax+112} 214 L{ax+112} 92 Q{ax+112} 52 {ax+56} 52 Q{ax} 52 {ax} 92 L{ax} 214 Z" fill="{Q["lav"]}"/>'
    wall+=f'<rect x="150" y="100" width="90" height="114" fill="{Q["lav"]}"/><rect x="214" y="100" width="26" height="114" fill="{Q["lav2"]}"/>'+iron_door()
    floor=flag_floor(('#4f5562','#525866','#4c5260'),9,'#3e434e')+FLOORSHADE+SIDE(BRICK[2])
    props=''.join([tun(4,236,.9), barrel(122,282,.75),
        barrel(330,234,.75),
        rack(270,398,90,18,58), candle_table(196,420),
        grapes(18,522), crate(48,580,'cabbage').replace(Q["green"],'#5e3460').replace(Q["green2"],'#4a2850').replace('#8fb85a','#7a4a7a'),
        tun(258,566,.85) if False else '', rack(306,600,64,16,50),
        tun(232,712,.95), barrel(14,760,.8), barrel(56,780,.75)])
    return page('Wine cellar','5/20',121,'#3e434e',floor,wall,road_stone('#e0cca0','#cbb486','#8f7a56'),props)
# ---------- DUNGEON
DSTONE=('#6e6a76','#5e5a66','#4a4652')
def straw(x,y,w=70):
    return f'<g transform="translate({x} {y})"><ellipse cx="{w/2}" cy="10" rx="{w/2}" ry="11" fill="#b8924a"/><ellipse cx="{w/2-4}" cy="7" rx="{w/2-6}" ry="8" fill="#d9b46a"/>'+''.join(f'<path d="M{8+k*9} {4+(k%3)*3} l9 -2" stroke="#b8924a" stroke-width="1.8" stroke-linecap="round"/>' for k in range(int(w/10)))+'</g>'
def cell(x,y,w=110,d=40,h=70):
    bars=''.join(f'<rect x="{k*w/9-1.5}" y="{d-4}" width="3.4" height="{h}" fill="#9a97a4"/><rect x="{k*w/9+0.6}" y="{d-4}" width="1.3" height="{h}" fill="#6e6b78"/>' for k in range(1,9))
    side=''.join(f'<rect x="{w+2+k*7}" y="{d-4-k*6}" width="3" height="{h}" fill="#4a4652"/>' for k in range(0,0))
    return f'''<g transform="translate({x} {y})">{shadow(w/2,d+h,w/2+6,7)}<rect x="0" y="0" width="{w}" height="{d+h-4}" fill="#1e1a24" opacity=".75"/>{straw(10,d+h-30,60)}
      {bars}<rect x="0" y="{d-6}" width="{w}" height="6" fill="#9a97a4"/><rect x="0" y="{d+h-6}" width="{w}" height="6" fill="#8a8794"/><rect x="-2" y="{d-6}" width="6" height="{h}" fill="#9a97a4"/><rect x="{w-4}" y="{d-6}" width="6" height="{h}" fill="#6e6b78"/>
      <rect x="{w*0.62}" y="{d+h/2-8}" width="12" height="14" rx="2" fill="{Q["mustard"]}"/><rect x="{w*0.62+5}" y="{d+h/2-4}" width="2" height="6" fill="{DARK}"/></g>'''
def bench(x,y):
    return f'<g transform="translate({x} {y})">{shadow(36,32,38,5)}<rect x="6" y="14" width="7" height="18" fill="{WOOD[2]}"/><rect x="58" y="14" width="7" height="18" fill="{WOOD[2]}"/><rect x="0" y="10" width="72" height="8" rx="2" fill="{WOOD[1]}"/><rect x="0" y="2" width="72" height="10" rx="2" fill="{WOOD[0]}"/></g>'
def ball_chain(x,y):
    links=''.join(f'<ellipse cx="{8+k*8}" cy="{18-k*1.4}" rx="4.6" ry="3" fill="none" stroke="#9a97a4" stroke-width="2.4"/>' for k in range(5))
    return f'<g transform="translate({x} {y})">{shadow(14,26,16,4)}{links}<circle cx="12" cy="16" r="11" fill="#6e6b78"/><path d="M12 5 A11 11 0 0 1 23 16 A11 11 0 0 1 16 26 A12 12 0 0 0 18 16 Z" fill="#4a4652"/><circle cx="8" cy="12" r="3" fill="#9a97a4"/></g>'
def chains_wall(x,y):
    return f'<g transform="translate({x} {y})"><rect x="0" y="0" width="10" height="8" rx="2" fill="#3a3644"/><rect x="30" y="0" width="10" height="8" rx="2" fill="#3a3644"/>'+''.join(f'<ellipse cx="{5+k*1.2}" cy="{12+k*7}" rx="3" ry="4.4" fill="none" stroke="#5a5664" stroke-width="2"/><ellipse cx="{35-k*1.2}" cy="{12+k*7}" rx="3" ry="4.4" fill="none" stroke="#5a5664" stroke-width="2"/>' for k in range(5))+f'<rect x="2" y="44" width="14" height="8" rx="4" fill="none" stroke="#5a5664" stroke-width="3"/><rect x="24" y="44" width="14" height="8" rx="4" fill="none" stroke="#5a5664" stroke-width="3"/></g>'
def rubble(x,y): return rock(x,y,.55)+rock(x+20,y+8,.45)+rock(x+8,y+14,.4)
def dungeon():
    wall=indoor_wall('#6a6672','#55515e',33).replace('fill="#978f83" opacity=".45"','fill="#7a7682" opacity=".8"')
    wall+=f'<g transform="translate(286 70)"><rect x="-6" y="-6" width="62" height="38" rx="4" fill="{DSTONE[2]}"/><rect x="0" y="0" width="50" height="26" fill="#9cb8c8"/>'+''.join(f'<rect x="{6+k*10}" y="0" width="3" height="26" fill="#3a3644"/>' for k in range(5))+'</g>'
    wall+=f'<path d="M290 96 L336 96 L380 214 L250 214 Z" fill="#f1e3c2" opacity=".08"/>'
    wall+=chains_wall(40,96)+chains_wall(100,120)+sconce(132,150)+sconce(246,150)
    wall+=f'<rect x="152" y="106" width="86" height="108" fill="{DSTONE[2]}"/>'+iron_door(164,62,('#5a5664','#4a4652'),True)
    floor=flag_floor(('#3e3a48','#403c4a','#3c3846'),17,'#2e2a36')+FLOORSHADE+SIDE(DSTONE[2])
    floor+=''.join(f'<path d="M{mx} {my} q6 -6 12 0 q6 -4 10 2" fill="{Q["green2"]}" opacity=".8"/>' for mx,my in ((24,500),(350,470),(150,690),(344,780),(20,660)))
    props=''.join([cell(14,224,124,30,74), bucket(150,300),
        barrel(334,234,.75),
        cell(256,384,118,28,66), bench(188,430) if False else '', ball_chain(206,430),
        bench(16,528), bucket(90,520) if False else '', chest(20,592),
        rubble(316,606), crate_closed(330,640,40),
        barrel(236,724,.85), crate_closed(286,738,48), rubble(330,800),
        bucket(30,780), ball_chain(72,800)])
    return page('Dungeon','5/20',141,'#2e2a36',floor,wall,road_stone('#d6c8a4','#bfb08a','#7d7260'),props)
rooms={'Room-v2-storeroom.dc.html':('C1 · Storeroom',storeroom()),
       'Room-v2-winecellar.dc.html':('C2 · Wine cellar',wine_cellar()),
       'Room-v2-dungeon.dc.html':('C3 · Dungeon',dungeon())}
base='/home/claude/mockups/project'
c=json.load(open(f'{base}/canvas.json'))
ref=c['boards']['Room-v2-meadow.dc.html']; x=ref['x']; y=ref['y']+ref['h']+200
for fn,(t,body) in rooms.items():
    open(f'{base}/{fn}','w').write(G['HEADQ']%t+body+'\n'+G['TAIL'])
    c['boards'].pop(fn,None); c['order']=[o for o in c['order'] if o!=fn]
    c['boards'][fn]={'x':x,'y':y,'w':390,'h':844,'title':t}; c['order'].append(fn); x+=470
json.dump(c,open(f'{base}/canvas.json','w'),ensure_ascii=False)
print('ok')
