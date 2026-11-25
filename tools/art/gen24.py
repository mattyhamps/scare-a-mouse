import json, math, re
# ================= Fourth floor: Treasury, Music room, Sewing room, Guest bedrooms, Clock tower
# Builds on gen23.py's helpers (and so gen22.py's and the floors before), same flat style.
g23=open('./gen23.py').read()
exec(g23[:g23.index("heads={'Toy room'")])
H4={}; P4={}
def add4(name,svg,box): P4[name]=[list(box),re.sub(r'\s+',' ',svg).strip()]
GOLD=('#f0d07a',Q["mustard"],Q["mustard2"])
IRON=('#7a7e87','#5f636b','#45484f')
BRASS=('#d9b25a','#b8903e','#8f6c28')
def coin(x,y,r=6): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{GOLD[1]}"/><path d="M{x} {y-r} A{r} {r} 0 0 1 {x} {y+r} Z" fill="{GOLD[2]}"/><circle cx="{x}" cy="{y}" r="{r*0.55:.1f}" fill="none" stroke="{GOLD[0]}" stroke-width="1.4"/>'
def coin_stack(x,y,n): return f'<g transform="translate({x} {y})">'+''.join(f'<rect x="0" y="{-k*4}" width="16" height="5" rx="2" fill="{GOLD[1] if k%2 else GOLD[0]}"/><rect x="10" y="{-k*4}" width="6" height="5" rx="2" fill="{GOLD[2]}"/>' for k in range(n))+'</g>'
def gold_bar(x,y): return f'<g transform="translate({x} {y})"><path d="M0 12 L4 0 L28 0 L32 12 Z" fill="{GOLD[1]}"/><path d="M20 0 L28 0 L32 12 L20 12 Z" fill="{GOLD[2]}"/><path d="M4 0 L28 0 L26 3 L6 3 Z" fill="{GOLD[0]}"/></g>'
def gem(x,y,c,c2,s=1): return f'<g transform="translate({x} {y}) scale({s})"><path d="M0 6 L5 0 L15 0 L20 6 L10 18 Z" fill="{c}"/><path d="M10 0 L15 0 L20 6 L10 18 Z" fill="{c2}"/><path d="M0 6 L20 6" stroke="#fff" stroke-opacity=".45" stroke-width="1.4"/><path d="M5 2 L8 2 L6 5 Z" fill="#fff" opacity=".7"/></g>'
def crown(x,y,s=1): return f'<g transform="translate({x} {y}) scale({s})"><path d="M0 22 L0 4 L9 13 L16 0 L23 13 L32 4 L32 22 Z" fill="{GOLD[1]}"/><path d="M16 0 L23 13 L32 4 L32 22 L16 22 Z" fill="{GOLD[2]}"/><rect x="0" y="18" width="32" height="5" fill="{GOLD[2]}"/><circle cx="16" cy="12" r="2.6" fill="{Q["coral"]}"/><circle cx="7" cy="17" r="1.8" fill="#6fb3b8"/><circle cx="25" cy="17" r="1.8" fill="#6fb3b8"/></g>'
def wall_shelf4(x,y,w,c=WOOD): return f'<rect x="{x}" y="{y}" width="{w}" height="6" rx="2" fill="{c[1]}"/><rect x="{x+w*0.62:.1f}" y="{y}" width="{w*0.38:.1f}" height="6" rx="2" fill="{c[2]}"/><path d="M{x+8} {y+6} l0 8 l8 -8 Z M{x+w-8} {y+6} l0 8 l-8 -8 Z" fill="{c[2]}"/>'
# ---------- TREASURY
def money_sack(x,y,s=1):
    return f'<g transform="translate({x} {y}) scale({s})"><path d="M6 14 Q-2 40 12 46 L34 46 Q48 40 40 14 Z" fill="{Q["tan"]}"/><path d="M23 14 L40 14 Q48 40 34 46 L23 46 Z" fill="{Q["tan2"]}"/><path d="M10 8 L36 8 L30 16 L16 16 Z" fill="{Q["tan"]}"/><rect x="12" y="14" width="22" height="4" rx="2" fill="{Q["brown"]}"/>{coin(23,32,7)}</g>'
def medallion(x,y):
    rays=''.join(f'<path d="M0 -30 L4 -24 L-4 -24 Z" fill="{GOLD[2]}" transform="rotate({k*30})"/>' for k in range(12))
    return f'<g transform="translate({x} {y})">{rays}<circle cx="0" cy="0" r="25" fill="{GOLD[1]}"/><path d="M0 -25 A25 25 0 0 1 0 25 Z" fill="{GOLD[2]}"/><circle cx="0" cy="0" r="19" fill="none" stroke="{GOLD[0]}" stroke-width="2.4"/>{crown(-13,-10,.82)}</g>'
def treasury_head():
    w=f'<rect x="0" y="0" width="390" height="214" fill="#33504a"/>'
    for r in range(10):
        for k in range(-1,8): w+=f'<rect x="{k*56+(r%2)*28+2}" y="{r*22+2}" width="52" height="18" rx="3" fill="{"#3a5a53" if (r+k)%3 else "#37564f"}"/>'
    # left: gold bars on the top shelf, coin stacks on the lower one
    w+=wall_shelf4(16,96,112)+''.join(gold_bar(22+k*34,84) for k in range(3))+''.join(gold_bar(39+k*34,72) for k in range(2))+gold_bar(56,60)
    w+=wall_shelf4(16,152,112)+coin_stack(24,146,6)+coin_stack(46,146,4)+coin_stack(68,146,7)+gem(94,128,Q["coral"],Q["coral2"],1.1)
    # right: money sacks, then a crown and coins
    w+=wall_shelf4(262,96,112)+money_sack(268,50,1)+money_sack(318,56,.86)
    w+=wall_shelf4(262,152,112)+crown(272,128,1.1)+coin_stack(318,146,5)+coin_stack(340,146,3)+gem(352,134,'#6fb3b8','#3f8a8f',.8)
    w+=medallion(195,50)
    # the vault door: iron, riveted, with a wheel
    w+=f'<rect x="146" y="102" width="98" height="112" fill="#26403a"/>'+gate_arch(164,62,(IRON[0],IRON[1]))
    w+=''.join(f'<circle cx="{170 if k%2==0 else 220}" cy="{146+(k//2)*22}" r="2.4" fill="{IRON[2]}"/>' for k in range(6))
    w+=f'<circle cx="195" cy="170" r="13" fill="none" stroke="{GOLD[1]}" stroke-width="4"/><path d="M182 170 L208 170 M195 157 L195 183" stroke="{GOLD[1]}" stroke-width="3"/><circle cx="195" cy="170" r="4" fill="{GOLD[2]}"/>'
    return w
def coin_heap(x,y):
    coins=''.join(coin(cx,cy,6) for cx,cy in ((22,32),(36,24),(52,20),(68,26),(82,34),(30,42),(46,36),(62,38),(76,44),(16,48),(92,48),(56,48)))
    return f'''<g transform="translate({x} {y})">{shadow(54,58,56,7)}<path d="M2 56 Q10 30 34 18 Q54 8 74 18 Q98 30 106 56 Z" fill="{GOLD[1]}"/><path d="M54 10 Q74 14 88 28 Q100 40 106 56 L54 56 Z" fill="{GOLD[2]}"/>{coins}
      <g transform="translate(40 -6)"><path d="M0 0 L22 0 Q22 16 11 18 Q0 16 0 0 Z" fill="{GOLD[0]}"/><path d="M11 0 L22 0 Q22 16 11 18 Z" fill="{GOLD[1]}"/><rect x="9" y="18" width="4" height="8" fill="{GOLD[2]}"/></g>{gem(74,8,Q["coral"],Q["coral2"],.8)}</g>'''
def gold_stack(x,y):
    bars=''.join(gold_bar(4+k*32,30) for k in range(3))+''.join(gold_bar(20+k*32,18) for k in range(2))+gold_bar(36,6)
    return f'<g transform="translate({x} {y})">{shadow(52,52,54,6)}{two(0,42,104,10,WOOD[1],WOOD[2],2)}<rect x="6" y="52" width="10" height="4" fill="{WOOD[2]}"/><rect x="88" y="52" width="10" height="4" fill="{WOOD[2]}"/>{bars}</g>'
def strongbox(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(32,70,34,6)}{two(2,4,60,62,"#3f6b5a","#2f5547",5)}<rect x="8" y="10" width="48" height="50" rx="3" fill="none" stroke="{GOLD[2]}" stroke-width="2.4"/>
      <circle cx="26" cy="32" r="10" fill="{IRON[0]}"/><circle cx="26" cy="32" r="6" fill="{IRON[2]}"/><path d="M26 22 L26 26" stroke="#fff" stroke-width="2"/><rect x="42" y="24" width="6" height="18" rx="3" fill="{GOLD[1]}"/>
      <rect x="6" y="66" width="8" height="5" fill="{IRON[2]}"/><rect x="50" y="66" width="8" height="5" fill="{IRON[2]}"/></g>'''
def crown_cushion(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(28,84,26,5)}{two(10,44,36,40,Q["grey"],Q["grey2"],2)}<rect x="6" y="40" width="44" height="7" rx="2" fill="{Q["grey"]}"/><rect x="6" y="80" width="44" height="6" rx="2" fill="{Q["grey2"]}"/>
      <path d="M2 40 Q4 26 28 26 Q52 26 54 40 Z" fill="{Q["coral"]}"/><path d="M28 26 Q52 26 54 40 L28 40 Z" fill="{Q["coral2"]}"/>{"".join(f'<circle cx="{cx}" cy="40" r="3" fill="{GOLD[1]}"/>' for cx in (4,52))}{crown(12,4,1)}</g>'''
def scales(x,y):
    pan=lambda px,py,items: f'<g transform="translate({px} {py})"><path d="M0 -26 L-14 0 M0 -26 L14 0" stroke="{GOLD[2]}" stroke-width="1.4"/><path d="M-16 0 L16 0 Q12 8 0 8 Q-12 8 -16 0 Z" fill="{GOLD[1]}"/>{items}</g>'
    return f'''<g transform="translate({x} {y})">{shadow(38,84,34,5)}{two(16,74,44,10,WOOD[1],WOOD[2],2)}<rect x="35" y="14" width="6" height="62" fill="{GOLD[2]}"/><rect x="35" y="14" width="3" height="62" fill="{GOLD[1]}"/>
      <path d="M8 22 L68 16" stroke="{GOLD[1]}" stroke-width="4" stroke-linecap="round"/><circle cx="38" cy="18" r="5" fill="{GOLD[0]}"/>{pan(10,48,coin_stack(-8,-4,3))}{pan(66,42,gem(-8,-14,"#6fb3b8","#3f8a8f",.7))}</g>'''
def jewel_case(x,y):
    gems=gem(8,14,Q["coral"],Q["coral2"],.8)+gem(30,10,'#6fb3b8','#3f8a8f',.9)+gem(54,14,'#7a9a4a','#5f7d38',.8)+f'<circle cx="24" cy="30" r="5" fill="none" stroke="{GOLD[1]}" stroke-width="2.4"/><circle cx="24" cy="25" r="2" fill="#a9cbe0"/>'+coin(56,32,5)
    return f'''<g transform="translate({x} {y})">{shadow(40,66,42,6)}<rect x="6" y="40" width="6" height="26" fill="{WOOD[2]}"/><rect x="68" y="40" width="6" height="26" fill="{WOOD[2]}"/>{two(0,36,80,8,WOOD[1],WOOD[2],2)}
      <rect x="2" y="4" width="76" height="34" rx="3" fill="{Q["navy"]}"/>{gems}<rect x="2" y="4" width="76" height="34" rx="3" fill="#a9cbe0" opacity=".3"/><rect x="2" y="4" width="76" height="34" rx="3" fill="none" stroke="{GOLD[2]}" stroke-width="3"/><path d="M12 34 L28 6 L34 6 L18 34 Z" fill="#fff" opacity=".3"/></g>'''
def sacks_pile(x,y): return f'<g transform="translate({x} {y})">{shadow(40,50,42,6)}{money_sack(0,4,1)}{money_sack(34,10,.86)}{coin_stack(30,48,2)}</g>'
def gold_urn(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(22,74,20,5)}<path d="M8 0 L36 0 L32 10 Q46 24 40 50 Q36 64 30 66 L14 66 Q8 64 4 50 Q-2 24 12 10 Z" fill="{GOLD[1]}"/><path d="M22 0 L36 0 L32 10 Q46 24 40 50 Q36 64 30 66 L22 66 Z" fill="{GOLD[2]}"/>
      <rect x="10" y="66" width="24" height="8" rx="2" fill="{GOLD[2]}"/><path d="M6 32 L38 32" stroke="{Q["coral"]}" stroke-width="4"/><path d="M12 14 Q8 26 10 40" stroke="{GOLD[0]}" stroke-width="3" fill="none" stroke-linecap="round"/></g>'''
# ---------- MUSIC ROOM
def note(x,y,c,s=1,two_=False):
    if two_: return f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="4" cy="22" rx="5" ry="4" fill="{c}"/><ellipse cx="20" cy="18" rx="5" ry="4" fill="{c}"/><rect x="8" y="2" width="2.4" height="20" fill="{c}"/><rect x="24" y="-2" width="2.4" height="20" fill="{c}"/><path d="M8 2 L26 -2 L26 4 L8 8 Z" fill="{c}"/></g>'
    return f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="4" cy="22" rx="5" ry="4" fill="{c}"/><rect x="7" y="0" width="2.4" height="22" fill="{c}"/><path d="M9 0 Q18 6 14 14 Q14 8 9 6 Z" fill="{c}"/></g>'
def organ_pipes(x,y,n=7):
    pipes=''.join(f'<g transform="translate({k*14} {abs(k-n//2)*10})"><rect x="0" y="0" width="12" height="{120-abs(k-n//2)*10}" rx="2" fill="#c4c1cc"/><rect x="7" y="0" width="5" height="{120-abs(k-n//2)*10}" rx="2" fill="#9a97a4"/><path d="M2 {80-abs(k-n//2)*10} L10 {80-abs(k-n//2)*10} L6 {72-abs(k-n//2)*10} Z" fill="{DARK}"/></g>' for k in range(n))
    return f'<g transform="translate({x} {y})">{pipes}</g>'
def violin(x,y,s=1,rot=0):
    return f'''<g transform="translate({x} {y}) rotate({rot}) scale({s})"><path d="M12 20 Q2 20 3 32 Q4 38 8 40 Q2 44 3 54 Q4 64 16 64 Q28 64 29 54 Q30 44 24 40 Q28 38 29 32 Q30 20 20 20 Z" fill="{Q["orange"]}"/><path d="M16 20 L20 20 Q30 20 29 32 Q28 38 24 40 Q30 44 29 54 Q28 64 16 64 Z" fill="{Q["orange2"]}"/>
      <rect x="14" y="0" width="4" height="40" fill="{DARK}"/><circle cx="16" cy="0" r="3" fill="{DARK}"/><rect x="11" y="52" width="10" height="3" fill="{DARK}"/><path d="M9 36 q2 3 0 6 M23 36 q-2 3 0 6" stroke="{DARK}" stroke-width="1.4" fill="none"/></g>'''
def lute(x,y,s=1,rot=0):
    return f'''<g transform="translate({x} {y}) rotate({rot}) scale({s})"><ellipse cx="18" cy="44" rx="18" ry="22" fill="{WOOD[0]}"/><path d="M18 22 A18 22 0 0 1 18 66 Z" fill="{WOOD[1]}"/><circle cx="18" cy="40" r="5" fill="{DARK}"/>
      <rect x="15" y="0" width="6" height="26" fill="{WOOD[2]}"/><path d="M13 0 L23 0 L26 -10 L16 -8 Z" fill="{WOOD[2]}"/><rect x="12" y="56" width="12" height="3" fill="{DARK}"/></g>'''
def music_head():
    w=f'<rect x="0" y="0" width="390" height="214" fill="#5a4560"/>'+''.join(f'<rect x="{x}" y="0" width="2" height="146" fill="#64506a"/>' for x in range(20,390,40))
    w+=f'<rect x="0" y="146" width="390" height="68" fill="{WOOD[2]}"/>'+''.join(f'<rect x="{x+3}" y="152" width="50" height="56" rx="3" fill="{WOOD[1]}"/>' for x in range(0,390,56))+f'<rect x="0" y="142" width="390" height="8" fill="{GOLD[2]}"/>'
    w+=organ_pipes(16,14)+f'<rect x="10" y="132" width="110" height="14" rx="3" fill="{WOOD[1]}"/><rect x="78" y="132" width="42" height="14" rx="3" fill="{WOOD[2]}"/>'
    w+=f'<g transform="translate(276 30)"><rect x="0" y="0" width="90" height="62" rx="3" fill="{GOLD[1]}"/><rect x="5" y="5" width="80" height="52" fill="{Q["cream"]}"/>'+''.join(f'<rect x="10" y="{14+k*7}" width="70" height="1.4" fill="{Q["brown"]}"/>' for k in range(5))+note(18,10,DARK,.9)+note(44,14,DARK,.9,True)+f'</g>'
    w+=violin(282,96,.8,-16)+lute(336,104,.8,14)+f'<rect x="300" y="96" width="4" height="6" fill="{GOLD[2]}"/><rect x="348" y="96" width="4" height="6" fill="{GOLD[2]}"/>'
    w+=f'<g transform="translate(195 44)"><path d="M-22 -26 Q-30 0 -14 24 L14 24 Q30 0 22 -26 Q14 -10 0 -10 Q-14 -10 -22 -26 Z" fill="{GOLD[1]}"/><path d="M0 -10 Q14 -10 22 -26 Q30 0 14 24 L0 24 Z" fill="{GOLD[2]}"/><path d="M-8 -6 L-8 20 M0 -8 L0 20 M8 -6 L8 20" stroke="{Q["cream"]}" stroke-width="1.4"/><rect x="-16" y="22" width="32" height="5" rx="2" fill="{GOLD[2]}"/></g>'
    w+=f'<rect x="148" y="104" width="94" height="110" fill="#45324a"/>'+gate_arch(164,62,(Q["coral"],Q["coral2"]))+note(185,150,GOLD[1],.8)
    return w
def double_bass(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(30,130,26,5)}<path d="M30 40 Q14 40 14 56 Q14 66 20 70 Q8 76 8 96 Q8 122 30 122 Q52 122 52 96 Q52 76 40 70 Q46 66 46 56 Q46 40 30 40 Z" fill="{Q["orange"]}"/>
      <path d="M30 40 Q46 40 46 56 Q46 66 40 70 Q52 76 52 96 Q52 122 30 122 Z" fill="{Q["orange2"]}"/><rect x="27" y="4" width="6" height="94" rx="2" fill="{DARK}"/><circle cx="30" cy="2" r="6" fill="{WOOD[2]}"/><rect x="21" y="8" width="5" height="3" fill="{WOOD[2]}"/><rect x="34" y="12" width="5" height="3" fill="{WOOD[2]}"/>
      {"".join(f'<rect x="{27.6+k*1.6:.1f}" y="10" width="0.8" height="100" fill="{Q["cream"]}" opacity=".8"/>' for k in range(4))}<rect x="21" y="98" width="18" height="3" rx="1" fill="{Q["cream2"]}"/><path d="M26 104 L34 104 L32 118 L28 118 Z" fill="{DARK}"/>
      <path d="M18 80 q4 7 0 14 M42 80 q-4 7 0 14" stroke="{DARK}" stroke-width="2.4" fill="none" stroke-linecap="round"/><rect x="29" y="122" width="2" height="8" fill="{IRON[1]}"/>
      <path d="M56 26 L14 128" stroke="{WOOD[2]}" stroke-width="2.6" stroke-linecap="round"/><path d="M55 32 L17 124" stroke="{Q["cream"]}" stroke-width="1"/></g>'''
def gong(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(48,104,50,6)}<rect x="4" y="12" width="8" height="88" fill="{Q["coral"]}"/><rect x="84" y="12" width="8" height="88" fill="{Q["coral2"]}"/><rect x="0" y="96" width="16" height="7" rx="2" fill="{DARK}"/><rect x="80" y="96" width="16" height="7" rx="2" fill="{DARK}"/>
      <path d="M-4 16 Q-2 4 8 8 L88 8 Q98 4 100 16 L100 20 L-4 20 Z" fill="{Q["coral"]}"/><path d="M48 8 L88 8 Q98 4 100 16 L100 20 L48 20 Z" fill="{Q["coral2"]}"/><path d="M36 20 L40 32 M60 20 L56 32" stroke="{DARK}" stroke-width="1.6"/>
      <circle cx="48" cy="60" r="30" fill="{GOLD[1]}"/><path d="M48 30 A30 30 0 0 1 48 90 Z" fill="{GOLD[2]}"/><circle cx="48" cy="60" r="21" fill="none" stroke="{GOLD[0]}" stroke-width="2.4"/><circle cx="48" cy="60" r="9" fill="{GOLD[0]}"/><path d="M34 46 Q40 40 46 38" stroke="#fff" stroke-opacity=".5" stroke-width="3" fill="none" stroke-linecap="round"/>
      <g transform="rotate(18 104 100)"><rect x="102" y="58" width="4" height="44" rx="2" fill="{WOOD[1]}"/><circle cx="104" cy="56" r="7" fill="{Q["cream"]}"/><path d="M104 49 A7 7 0 0 1 104 63 Z" fill="{Q["cream2"]}"/></g></g>'''
def tuba(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(32,86,30,5)}<ellipse cx="32" cy="60" rx="22" ry="17" fill="none" stroke="{BRASS[1]}" stroke-width="9"/><ellipse cx="32" cy="60" rx="22" ry="17" fill="none" stroke="{BRASS[0]}" stroke-width="3" transform="translate(-2 -2)"/>
      <path d="M8 6 Q22 14 24 44 L40 44 Q42 14 56 6 Z" fill="{BRASS[0]}"/><path d="M32 8 L56 6 Q42 14 40 44 L32 44 Z" fill="{BRASS[1]}"/><ellipse cx="32" cy="6" rx="24" ry="6" fill="{BRASS[2]}"/><ellipse cx="32" cy="5" rx="19" ry="3.6" fill="#5a3a24"/>
      <path d="M24 44 L24 74 Q32 84 40 74 L40 44 Z" fill="{BRASS[0]}"/><path d="M32 44 L40 44 L40 74 Q36 80 32 80 Z" fill="{BRASS[1]}"/>
      {"".join(f'<rect x="{44+k*6}" y="46" width="5" height="14" rx="1" fill="{BRASS[1]}"/><rect x="{43.5+k*6}" y="42" width="6" height="4" rx="1" fill="{Q["cream"]}"/>' for k in range(3))}<path d="M12 56 Q4 50 4 40" stroke="{BRASS[2]}" stroke-width="4" fill="none" stroke-linecap="round"/><circle cx="4" cy="38" r="3" fill="{BRASS[2]}"/></g>'''
def timpani(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(38,78,38,6)}<path d="M6 22 L12 76 M70 22 L64 76 M38 50 L38 76" stroke="{IRON[1]}" stroke-width="4"/><path d="M2 20 L74 20 Q74 56 38 58 Q2 56 2 20 Z" fill="#c8743a"/><path d="M38 20 L74 20 Q74 56 38 58 Z" fill="#a85e2a"/>
      <path d="M12 28 Q14 42 24 50" stroke="#e39a5e" stroke-width="4" fill="none" stroke-linecap="round"/>{"".join(f'<rect x="{6+k*16}" y="20" width="4" height="10" rx="1" fill="{IRON[0]}"/>' for k in range(5))}
      <ellipse cx="38" cy="20" rx="36" ry="9" fill="{Q["cream"]}"/><path d="M38 11 A36 9 0 0 1 38 29 Z" fill="{Q["cream2"]}"/><ellipse cx="38" cy="20" rx="36" ry="9" fill="none" stroke="{IRON[0]}" stroke-width="3"/>
      <g transform="rotate(-28 30 16)"><rect x="28" y="-14" width="3.4" height="30" rx="1.5" fill="{WOOD[1]}"/><circle cx="29.7" cy="-16" r="5" fill="{Q["coral"]}"/></g><g transform="rotate(24 48 16)"><rect x="46" y="-14" width="3.4" height="30" rx="1.5" fill="{WOOD[1]}"/><circle cx="47.7" cy="-16" r="5" fill="{Q["coral"]}"/></g></g>'''
def bass_drum(x,y):
    rods=''.join(f'<rect x="-2" y="-34" width="4" height="7" rx="1" fill="{GOLD[1]}" transform="rotate({k*45})"/>' for k in range(8))
    return f'''<g transform="translate({x} {y})">{shadow(50,90,52,6)}<path d="M70 90 L84 62 L98 90" stroke="{IRON[1]}" stroke-width="3" fill="none"/><rect x="83" y="16" width="2.6" height="48" fill="{IRON[1]}"/><ellipse cx="84" cy="16" rx="20" ry="5" fill="{GOLD[1]}"/><path d="M84 11 A20 5 0 0 1 104 16 L84 16 Z" fill="{GOLD[0]}"/><circle cx="84" cy="12" r="2.4" fill="{GOLD[2]}"/>
      <g transform="translate(40 52)">{rods}<circle cx="0" cy="0" r="32" fill="{Q["coral"]}"/><path d="M0 -32 A32 32 0 0 1 0 32 Z" fill="{Q["coral2"]}"/><circle cx="0" cy="0" r="26" fill="{Q["cream"]}"/><path d="M0 -26 A26 26 0 0 1 0 26 Z" fill="{Q["cream2"]}"/>
      <circle cx="0" cy="0" r="29" fill="none" stroke="{GOLD[1]}" stroke-width="2"/>{note(-10,-14,Q["coral"],1.1)}</g><rect x="14" y="80" width="6" height="10" fill="{IRON[2]}"/><rect x="60" y="80" width="6" height="10" fill="{IRON[2]}"/></g>'''
def accordion_stool(x,y):
    folds=''.join(f'<path d="M{20+k*4} 14 L{22+k*4} 18 L{20+k*4} 22 L{22+k*4} 26 L{20+k*4} 30 L{22+k*4} 34 L{20+k*4} 38 L{22+k*4} 42 L{20+k*4} 46 L{22+k*4} 50 L{20+k*4} 54" stroke="{Q["coral2"] if k%2 else Q["cream"]}" stroke-width="3" fill="none"/>' for k in range(7))
    return f'''<g transform="translate({x} {y})">{shadow(32,90,30,5)}<rect x="12" y="62" width="6" height="28" fill="{WOOD[2]}"/><rect x="46" y="62" width="6" height="28" fill="{WOOD[2]}"/><rect x="16" y="78" width="32" height="4" fill="{WOOD[2]}"/><ellipse cx="32" cy="62" rx="26" ry="7" fill="{WOOD[1]}"/><ellipse cx="32" cy="60" rx="24" ry="5" fill="{WOOD[0]}"/>
      <rect x="18" y="14" width="32" height="42" fill="{Q["coral"]}"/>{folds}<rect x="4" y="10" width="16" height="48" rx="3" fill="{Q["cream"]}"/>{"".join(f'<rect x="6" y="{14+k*6}" width="12" height="5" fill="#fff"/><rect x="6" y="{17+k*6}" width="7" height="3" fill="{DARK}"/>' for k in range(7))}
      <rect x="48" y="10" width="14" height="48" rx="3" fill="{Q["navy"]}"/><rect x="56" y="10" width="6" height="48" rx="3" fill="{Q["navy2"]}"/>{"".join(f'<circle cx="{53+(k%2)*4}" cy="{16+k*5}" r="1.6" fill="{Q["cream"]}"/>' for k in range(8))}</g>'''
def music_stand(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(26,104,24,4)}<path d="M8 104 L26 82 L44 104" stroke="{BRASS[1]}" stroke-width="3.4" fill="none"/><rect x="24" y="34" width="4" height="50" fill="{BRASS[1]}"/><rect x="24" y="34" width="2" height="50" fill="{BRASS[0]}"/>
      <path d="M0 6 L52 6 L50 40 L2 40 Z" fill="{BRASS[2]}"/><rect x="2" y="38" width="48" height="4" rx="1" fill="{BRASS[1]}"/><rect x="4" y="0" width="22" height="36" fill="{Q["cream"]}" transform="rotate(-4 15 18)"/><rect x="26" y="0" width="22" height="36" fill="{Q["cream2"]}" transform="rotate(4 37 18)"/>
      {"".join(f'<rect x="6" y="{6+k*7}" width="18" height="1" fill="{Q["brown"]}" transform="rotate(-4 15 18)"/><rect x="28" y="{6+k*7}" width="18" height="1" fill="{Q["brown"]}" transform="rotate(4 37 18)"/>' for k in range(4))}{note(8,2,DARK,.55)}{note(32,4,DARK,.55,True)}</g>'''
def tambourine(x,y): return f'<g transform="translate({x} {y})">{shadow(14,24,14,3)}<circle cx="14" cy="12" r="12" fill="{WOOD[0]}"/><circle cx="14" cy="12" r="9" fill="{Q["cream"]}"/>'+''.join(f'<circle cx="{14+11*math.cos(a)}" cy="{12+11*math.sin(a)}" r="2.4" fill="{BRASS[0]}"/>' for a in (0.3,1.9,3.5,5.1))+'</g>'
def metronome(x,y): return f'<g transform="translate({x} {y})">{shadow(12,34,12,3)}<path d="M2 34 L8 0 L16 0 L22 34 Z" fill="{WOOD[1]}"/><path d="M12 0 L16 0 L22 34 L12 34 Z" fill="{WOOD[2]}"/><path d="M5 20 L19 20 L20 26 L4 26 Z" fill="{Q["cream"]}"/><path d="M12 28 L18 4" stroke="{IRON[2]}" stroke-width="1.6"/><rect x="14" y="10" width="5" height="4" fill="{BRASS[1]}"/></g>'
# ---------- SEWING ROOM
def flowers_wall():
    g=f'<rect x="0" y="0" width="390" height="214" fill="#e7c9c1"/>'
    for r in range(6):
        for k in range(10):
            cx=k*40+(r%2)*20+6; cy=16+r*28
            g+=f'<g transform="translate({cx} {cy})">'+''.join(f'<circle cx="{3*math.cos(a)}" cy="{3*math.sin(a)}" r="2.2" fill="#d9a59a"/>' for a in (0,1.26,2.51,3.77,5.03))+f'<circle cx="0" cy="0" r="1.4" fill="{Q["mustard"]}"/></g>'
    return g
def spool(x,y,c,c2,s=1): return f'<g transform="translate({x} {y}) scale({s})"><rect x="0" y="0" width="16" height="4" rx="1" fill="{WOOD[0]}"/><rect x="2" y="4" width="12" height="14" fill="{c}"/><rect x="9" y="4" width="5" height="14" fill="{c2}"/>{"".join(f"<rect x=\"2\" y=\"{6+k*4}\" width=\"12\" height=\"1\" fill=\"{c2}\"/>" for k in range(3))}<rect x="0" y="18" width="16" height="4" rx="1" fill="{WOOD[1]}"/></g>'
def bolt(x,y,c,c2,h=50): return f'<g transform="translate({x} {y})"><rect x="0" y="0" width="20" height="{h}" rx="3" fill="{c}"/><rect x="12" y="0" width="8" height="{h}" rx="3" fill="{c2}"/><ellipse cx="10" cy="2" rx="10" ry="3" fill="{c2}"/><circle cx="10" cy="2" r="2" fill="{WOOD[1]}"/></g>'
def scissors(x,y,s=1,rot=0): return f'<g transform="translate({x} {y}) rotate({rot}) scale({s})"><circle cx="6" cy="6" r="5" fill="none" stroke="{Q["coral"]}" stroke-width="3"/><circle cx="6" cy="20" r="5" fill="none" stroke="{Q["coral"]}" stroke-width="3"/><path d="M10 9 L36 16 L10 13 Z" fill="#c4c1cc"/><path d="M10 17 L36 12 L10 13 Z" fill="#9a97a4"/><circle cx="13" cy="13" r="1.6" fill="{IRON[2]}"/></g>'
def sewing_head():
    w=flowers_wall()+f'<rect x="0" y="160" width="390" height="54" fill="#c9a08f"/><rect x="0" y="156" width="390" height="6" fill="{Q["cream"]}"/>'
    # window with curtains, left
    w+=f'<g transform="translate(34 30)"><rect x="-4" y="-4" width="72" height="96" rx="4" fill="{Q["cream"]}"/><rect x="0" y="0" width="64" height="88" rx="2" fill="#a9cbe0"/><circle cx="46" cy="22" r="8" fill="{Q["mustard"]}"/><path d="M0 64 Q20 54 34 62 Q50 54 64 62 L64 88 L0 88 Z" fill="{Q["olive"]}"/><rect x="31" y="0" width="2" height="88" fill="{Q["cream"]}"/><rect x="0" y="42" width="64" height="2" fill="{Q["cream"]}"/>'
    w+=f'<path d="M-12 -10 L18 -10 Q8 40 -4 98 L-12 98 Z" fill="#7a9a4a"/>'+''.join(f'<rect x="{-12}" y="{-4+k*16}" width="22" height="4" fill="#cfe0a8" transform="skewX(-6)"/>' for k in range(6))
    w+=f'<path d="M76 -10 L46 -10 Q56 40 68 98 L76 98 Z" fill="#5f7d38"/><rect x="-16" y="-14" width="96" height="6" rx="3" fill="{WOOD[1]}"/></g>'
    # a shelf of fabric bolts over the window side, and a rack of thread spools, right
    w+=f'<g transform="translate(262 26)">{two(0,0,108,74,WOOD[1],WOOD[2],3)}<rect x="5" y="5" width="98" height="64" rx="2" fill="{Q["cream2"]}"/>'
    cols=[(Q["coral"],Q["coral2"]),(Q["navy"],Q["navy2"]),(Q["mustard"],Q["mustard2"]),(Q["olive"],Q["olive2"]),(Q["pink"],Q["pink2"]),("#7a4a7a","#5e3460")]
    w+=''.join(spool(12+k*16,8,*cols[k%6],.9) for k in range(6))+''.join(spool(12+k*16,40,*cols[(k+3)%6],.9) for k in range(6))+f'<rect x="5" y="32" width="98" height="3" fill="{WOOD[1]}"/></g>'
    w+=wall_shelf4(262,130,108)+bolt(270,82,Q["coral"],Q["coral2"],48)+bolt(294,90,Q["navy"],Q["navy2"],40)+bolt(318,84,"#cfe0a8","#a9c48a",46)+bolt(342,92,Q["pink"],Q["pink2"],38)
    # a hanging tape measure and big scissors by the door
    w+=f'<path d="M132 30 L132 120 Q132 130 140 130" stroke="{GOLD[0]}" stroke-width="7" fill="none"/>'+''.join(f'<rect x="129" y="{34+k*8}" width="3" height="1.4" fill="{Q["brown"]}"/>' for k in range(11))+f'<circle cx="132" cy="28" r="4" fill="{WOOD[2]}"/>'
    w+=scissors(242,40,1.1,70)
    # bunting of fabric scraps
    w+=f'<path d="M150 22 Q195 40 240 22" stroke="{Q["brown"]}" stroke-width="1.4" fill="none"/>'+''.join(f'<rect x="{152+k*17}" y="{24+[2,8,12,13,11,7][k]}" width="14" height="14" fill="{cols[k][0]}" transform="rotate({[-8,-4,0,0,4,8][k]} {159+k*17} {30+[2,8,12,13,11,7][k]})"/>' for k in range(6))
    w+=f'<rect x="148" y="104" width="94" height="110" fill="#c9a08f"/>'+gate_arch(164,62,(WOOD[1],WOOD[2]))+spool(187,140,Q["coral"],Q["coral2"])
    return w
def spinning_wheel(x,y):
    spokes=''.join(f'<path d="M30 34 L{30+26*math.cos(a):.1f} {34+26*math.sin(a):.1f}" stroke="{WOOD[1]}" stroke-width="2.4"/>' for a in [k*0.785 for k in range(8)])
    return f'''<g transform="translate({x} {y})">{shadow(44,88,44,6)}<path d="M8 88 L30 58 M60 88 L44 60 M80 88 L70 50" stroke="{WOOD[2]}" stroke-width="5" stroke-linecap="round"/>{two(20,56,64,10,WOOD[1],WOOD[2],3)}
      <circle cx="30" cy="34" r="28" fill="none" stroke="{WOOD[1]}" stroke-width="5"/>{spokes}<circle cx="30" cy="34" r="5" fill="{WOOD[2]}"/><rect x="66" y="22" width="6" height="36" fill="{WOOD[1]}"/><ellipse cx="69" cy="22" rx="9" ry="6" fill="{Q["cream"]}"/><path d="M30 6 L69 18" stroke="{Q["cream2"]}" stroke-width="1.4"/></g>'''
def sewing_table(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(46,80,48,6)}<path d="M10 40 L6 80 M82 40 L86 80" stroke="{IRON[2]}" stroke-width="4"/><path d="M14 66 L78 66" stroke="{IRON[2]}" stroke-width="3"/><circle cx="46" cy="62" r="10" fill="none" stroke="{IRON[2]}" stroke-width="3"/>{two(0,32,92,10,WOOD[1],WOOD[2],3)}
      <path d="M18 32 L18 4 Q18 0 22 0 L64 0 Q70 0 70 6 L70 14 L34 14 L34 32 Z" fill="{DARK}"/><path d="M50 0 L64 0 Q70 0 70 6 L70 14 L50 14 Z" fill="#45343a"/><rect x="64" y="14" width="4" height="14" fill="#9a97a4"/><circle cx="26" cy="12" r="5" fill="{GOLD[1]}"/><path d="M38 6 L62 6" stroke="{GOLD[1]}" stroke-width="2"/>{spool(40,-14,Q["coral"],Q["coral2"],.7)}
      <path d="M70 30 L84 30 L80 36 L66 36 Z" fill="{Q["pink"]}"/></g>'''
def dress_form(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(24,104,22,5)}<path d="M10 104 L24 90 L38 104" stroke="{WOOD[2]}" stroke-width="4" fill="none"/><rect x="22" y="66" width="4" height="26" fill="{WOOD[2]}"/>
      <path d="M10 6 Q24 0 38 6 Q42 18 36 30 Q44 46 40 66 L8 66 Q4 46 12 30 Q6 18 10 6 Z" fill="{Q["cream"]}"/><path d="M24 2 Q32 2 38 6 Q42 18 36 30 Q44 46 40 66 L24 66 Z" fill="{Q["cream2"]}"/>
      <path d="M12 30 Q24 36 36 30 Q44 46 40 66 L8 66 Q4 46 12 30 Z" fill="{Q["coral"]}"/><path d="M24 33 Q32 33 36 30 Q44 46 40 66 L24 66 Z" fill="{Q["coral2"]}"/><path d="M8 66 Q24 72 40 66" stroke="{Q["mustard"]}" stroke-width="2.4" fill="none" stroke-dasharray="3 3"/>
      <rect x="20" y="-4" width="8" height="8" rx="2" fill="{WOOD[1]}"/>{"".join(f'<circle cx="{14+k*5}" cy="{18+k%2*2}" r="1.6" fill="{Q["navy"]}"/>' for k in range(4))}</g>'''
def yarn_ball(x,y,c,c2,r=10): return f'<g transform="translate({x} {y})"><circle cx="0" cy="0" r="{r}" fill="{c}"/><path d="M0 {-r} A{r} {r} 0 0 1 0 {r} Z" fill="{c2}"/><path d="M{-r*0.7:.1f} {-r*0.5:.1f} Q0 {-r*0.1:.1f} {r*0.7:.1f} {r*0.6:.1f} M{-r*0.8:.1f} {r*0.2:.1f} Q0 {r*0.3:.1f} {r*0.4:.1f} {r*0.9:.1f}" stroke="#fff" stroke-opacity=".35" stroke-width="1.6" fill="none"/></g>'
def yarn_basket(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(30,46,30,5)}{yarn_ball(16,16,Q["coral"],Q["coral2"])}{yarn_ball(36,12,Q["navy"],Q["navy2"])}{yarn_ball(46,22,Q["mustard"],Q["mustard2"],9)}<path d="M28 -6 L22 22 M34 -8 L32 20" stroke="{WOOD[2]}" stroke-width="2.4" stroke-linecap="round"/>
      <path d="M2 20 L58 20 L52 46 L8 46 Z" fill="{Q["tan"]}"/><path d="M34 20 L58 20 L52 46 L34 46 Z" fill="{Q["tan2"]}"/>{"".join(f'<path d="M{6+k*2} {26+k*6} L{54-k*2} {26+k*6}" stroke="{Q["brown"]}" stroke-width="1.4" opacity=".6"/>' for k in range(3))}<path d="M50 44 Q60 50 66 44" stroke="{Q["coral"]}" stroke-width="2" fill="none"/></g>'''
def bolt_stand(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(36,82,38,6)}{two(0,70,72,12,WOOD[1],WOOD[2],2)}<g transform="rotate(-8 12 70)">{bolt(4,8,Q["navy"],Q["navy2"],64)}</g><g transform="rotate(-3 30 70)">{bolt(24,2,"#cfe0a8","#a9c48a",70)}</g><g transform="rotate(4 50 70)">{bolt(44,12,Q["coral"],Q["coral2"],60)}</g></g>'''
def loom(x,y):
    threads=''.join(f'<rect x="{12+k*6}" y="12" width="2" height="54" fill="{Q["cream"]}"/>' for k in range(12))
    woven=''.join(f'<rect x="10" y="{40+k*5}" width="76" height="4" fill="{[Q["coral"],Q["mustard"],Q["navy"],Q["olive"],Q["coral"]][k]}"/>' for k in range(5))
    return f'''<g transform="translate({x} {y})">{shadow(48,94,48,6)}<rect x="2" y="0" width="7" height="94" rx="2" fill="{WOOD[1]}"/><rect x="87" y="0" width="7" height="94" rx="2" fill="{WOOD[2]}"/><rect x="0" y="4" width="96" height="8" rx="2" fill="{WOOD[1]}"/><rect x="0" y="66" width="96" height="8" rx="2" fill="{WOOD[1]}"/>
      {threads}{woven}<rect x="6" y="32" width="84" height="5" rx="2" fill="{WOOD[0]}"/><path d="M4 86 L92 86" stroke="{WOOD[2]}" stroke-width="4"/></g>'''
def ironing_board(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(46,58,46,5)}<path d="M20 20 L70 58 M70 20 L20 58" stroke="{IRON[1]}" stroke-width="3"/><path d="M4 12 Q4 6 12 6 L84 6 Q96 6 96 14 Q96 20 84 20 L12 20 Q4 20 4 12 Z" fill="{Q["navy"]}"/><path d="M50 6 L84 6 Q96 6 96 14 Q96 20 84 20 L50 20 Z" fill="{Q["navy2"]}"/>
      {"".join(f'<circle cx="{14+k*12}" cy="13" r="2" fill="{Q["cream"]}" opacity=".7"/>' for k in range(7))}<path d="M20 4 L22 -6 L44 -6 Q46 0 44 4 Z" fill="#c4c1cc"/><path d="M26 -6 Q32 -16 40 -6" stroke="{DARK}" stroke-width="3" fill="none"/></g>'''
def spools_s(x,y): return f'<g transform="translate({x} {y})">{shadow(16,22,16,3)}{spool(0,0,Q["navy"],Q["navy2"])}{spool(16,2,Q["mustard"],Q["mustard2"],.9)}</g>'
def pincushion(x,y): return f'<g transform="translate({x} {y})">{shadow(12,22,12,3)}<ellipse cx="12" cy="14" rx="12" ry="8" fill="{Q["coral"]}"/><path d="M12 6 A12 8 0 0 1 12 22 Z" fill="{Q["coral2"]}"/><path d="M12 6 L12 22 M4 9 Q8 14 4 20 M20 9 Q16 14 20 20" stroke="{Q["coral2"]}" stroke-width="1.2" fill="none"/><path d="M9 6 L12 0 L15 6 Z" fill="{Q["olive"]}"/>'+''.join(f'<path d="M{px} {py} L{px+dx} {py-8}" stroke="#9a97a4" stroke-width="1.2"/><circle cx="{px+dx}" cy="{py-8}" r="2" fill="{c}"/>' for px,py,dx,c in ((6,10,-3,Q["mustard"]),(18,9,3,Q["navy"]),(13,8,0,"#fff")))+'</g>'
def scissors_s(x,y): return f'<g transform="translate({x} {y})">{shadow(18,24,18,3)}{scissors(0,0,1)}</g>'
def buttons(x,y): return f'<g transform="translate({x} {y})">'+''.join(f'<circle cx="{dx}" cy="{dy}" r="{r}" fill="{c}"/><circle cx="{dx-r*0.3:.1f}" cy="{dy}" r="1" fill="{DARK}"/><circle cx="{dx+r*0.3:.1f}" cy="{dy}" r="1" fill="{DARK}"/>' for dx,dy,r,c in ((7,8,6,Q["navy"]),(20,5,5,Q["mustard"]),(30,11,6,Q["coral"]),(17,15,4.5,Q["olive"])))+'</g>'
def yarn_s(x,y): return f'<g transform="translate({x} {y})">{shadow(12,22,12,3)}{yarn_ball(12,11,"#7a4a7a","#5e3460",11)}<path d="M22 16 Q30 20 34 14" stroke="#7a4a7a" stroke-width="2" fill="none"/></g>'
# ---------- GUEST BEDROOMS
def guest_door(x,y,num,c,c2):
    return f'''<g transform="translate({x} {y})"><rect x="-6" y="-6" width="58" height="104" rx="4" fill="{Q["cream"]}"/><path d="M0 98 L0 18 Q0 0 23 0 Q46 0 46 18 L46 98 Z" fill="{c}"/><path d="M23 0 Q46 0 46 18 L46 98 L23 98 Z" fill="{c2}"/>
      <rect x="6" y="26" width="34" height="26" rx="2" fill="{c2}" opacity=".6"/><rect x="6" y="60" width="34" height="30" rx="2" fill="{c2}" opacity=".6"/><circle cx="38" cy="56" r="3" fill="{GOLD[1]}"/>
      <rect x="13" y="6" width="20" height="16" rx="3" fill="{GOLD[1]}"/><text x="23" y="19" font-family="Fredoka,system-ui" font-weight="700" font-size="14" fill="{DARK}" text-anchor="middle">{num}</text></g>'''
def wall_lamp(x,y): return f'<g transform="translate({x} {y})"><circle cx="0" cy="0" r="22" fill="{Q["mustard"]}" opacity=".14"/><rect x="-2" y="2" width="4" height="16" fill="{GOLD[2]}"/><rect x="-8" y="16" width="16" height="5" rx="2" fill="{GOLD[2]}"/><path d="M-10 2 L10 2 L6 -14 L-6 -14 Z" fill="{Q["cream"]}"/><path d="M0 2 L10 2 L6 -14 L0 -14 Z" fill="{Q["cream2"]}"/></g>'
def landscape(x,y,w,h):
    return f'<g transform="translate({x} {y})"><rect x="0" y="0" width="{w}" height="{h}" rx="2" fill="{GOLD[1]}"/><rect x="4" y="4" width="{w-8}" height="{h-8}" fill="#a9cbe0"/><path d="M4 {h*0.62} L{w*0.3} {h*0.36} L{w*0.5} {h*0.56} L{w*0.7} {h*0.3} L{w-4} {h*0.6} L{w-4} {h-4} L4 {h-4} Z" fill="{Q["olive"]}"/><circle cx="{w*0.26}" cy="{h*0.26}" r="{h*0.1}" fill="{Q["cream"]}"/></g>'
def guest_head():
    w=f'<rect x="0" y="0" width="390" height="214" fill="#5c6f8a"/>'+''.join(f'<path d="M{x} {y} l5 -7 l5 7 l-5 7 Z" fill="#677b97"/>' for x in range(4,390,30) for y in range(16,150,30))
    w+=f'<rect x="0" y="148" width="390" height="66" fill="{WOOD[1]}"/>'+''.join(f'<rect x="{x+4}" y="154" width="40" height="54" rx="3" fill="{WOOD[0]}" opacity=".45"/>' for x in range(0,390,48))+f'<rect x="0" y="144" width="390" height="8" fill="{WOOD[2]}"/>'
    w+=guest_door(30,116,1,"#8a5432","#6e4126")+guest_door(314,116,2,"#8a5432","#6e4126")
    w+=landscape(26,26,58,44)+landscape(306,22,64,48)+wall_lamp(116,64)+wall_lamp(274,64)
    w+=f'<g transform="translate(96 120)">{two(0,0,40,6,WOOD[1],WOOD[2],2)}<path d="M8 6 L10 28 M32 6 L30 28" stroke="{WOOD[2]}" stroke-width="3"/><path d="M12 -2 Q10 -16 20 -18 Q30 -16 28 -2 Z" fill="#6fb3b8"/><path d="M14 -18 Q12 -30 18 -30 M20 -18 Q22 -32 28 -28 M24 -18 Q30 -26 32 -22" stroke="{Q["olive"]}" stroke-width="3" fill="none" stroke-linecap="round"/><circle cx="18" cy="-31" r="4" fill="{Q["pink"]}"/><circle cx="29" cy="-29" r="4" fill="{Q["coral"]}"/><circle cx="33" cy="-22" r="3.4" fill="{Q["mustard"]}"/></g>'
    w+=f'<g transform="translate(195 46)"><rect x="-40" y="-14" width="80" height="28" rx="4" fill="{Q["cream"]}"/><rect x="-36" y="-10" width="72" height="20" rx="3" fill="none" stroke="{GOLD[1]}" stroke-width="2"/><text x="0" y="6" font-family="Fredoka,system-ui" font-weight="700" font-size="14" fill="{Q["navy2"]}" text-anchor="middle">WELCOME</text></g>'
    w+=f'<rect x="148" y="104" width="94" height="110" fill="#4a5a72"/>'+gate_arch(164,62,(Q["navy"],Q["navy2"]))+f'<circle cx="216" cy="168" r="3" fill="{GOLD[1]}"/>'
    return w
def pillow(x,y,c,c2,w=26): return f'<g transform="translate({x} {y})"><rect x="0" y="0" width="{w}" height="14" rx="6" fill="{c}"/><rect x="{w*0.6:.1f}" y="0" width="{w*0.4:.1f}" height="14" rx="6" fill="{c2}"/></g>'
def four_poster(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(52,104,54,7)}<rect x="2" y="0" width="7" height="104" rx="2" fill="{WOOD[1]}"/><rect x="95" y="0" width="7" height="104" rx="2" fill="{WOOD[2]}"/><rect x="0" y="0" width="104" height="10" rx="3" fill="{WOOD[1]}"/>
      <path d="M6 10 Q18 22 30 10 Q42 22 54 10 Q66 22 78 10 Q90 22 100 10" stroke="{Q["coral"]}" stroke-width="6" fill="none"/><path d="M9 10 L22 10 Q14 50 9 62 Z" fill="{Q["coral"]}"/><path d="M95 10 L82 10 Q90 50 95 62 Z" fill="{Q["coral2"]}"/>
      <rect x="9" y="38" width="86" height="22" rx="4" fill="{WOOD[1]}"/>{pillow(14,42,Q["cream"],Q["cream2"],34)}{pillow(54,42,Q["cream"],Q["cream2"],34)}
      {two(9,54,86,34,Q["navy"],Q["navy2"],5)}<rect x="9" y="54" width="86" height="8" rx="4" fill="{Q["cream"]}"/>{"".join(f'<path d="M{20+k*20} 70 l5 5 l-5 5 l-5 -5 Z" fill="{GOLD[1]}"/>' for k in range(4))}<rect x="9" y="86" width="86" height="8" rx="2" fill="{WOOD[2]}"/></g>'''
def quilt_bed(x,y):
    patches=''.join(f'<rect x="{12+c*17}" y="{30+r*12}" width="17" height="12" fill="{[Q["coral"],Q["mustard"],"#cfe0a8",Q["pink"],"#a9cbe0"][(r*2+c)%5]}"/>' for r in range(3) for c in range(4))
    return f'''<g transform="translate({x} {y})">{shadow(48,74,50,6)}{two(0,0,10,74,WOOD[1],WOOD[2],3)}<rect x="0" y="0" width="10" height="74" rx="3" fill="{WOOD[1]}"/><rect x="86" y="30" width="8" height="44" rx="3" fill="{WOOD[2]}"/>
      <rect x="8" y="18" width="84" height="48" rx="4" fill="{Q["cream"]}"/>{pillow(12,16,"#fff",Q["cream2"],30)}{patches}<rect x="12" y="30" width="68" height="36" fill="none" stroke="{Q["cream"]}" stroke-width="1.4"/><rect x="80" y="30" width="12" height="36" rx="3" fill="{Q["coral2"]}"/></g>'''
def wardrobe(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(34,104,36,6)}<path d="M2 8 Q34 -6 66 8 L66 14 L2 14 Z" fill="{WOOD[1]}"/>{two(4,12,60,86,WOOD[1],WOOD[2],3)}<rect x="9" y="18" width="24" height="72" rx="3" fill="{WOOD[0]}" opacity=".5"/><rect x="35" y="18" width="24" height="72" rx="3" fill="{WOOD[2]}" opacity=".5"/>
      <circle cx="30" cy="54" r="2.6" fill="{GOLD[1]}"/><circle cx="38" cy="54" r="2.6" fill="{GOLD[1]}"/><rect x="8" y="98" width="8" height="6" fill="{WOOD[2]}"/><rect x="52" y="98" width="8" height="6" fill="{WOOD[2]}"/></g>'''
def washstand(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(30,76,30,5)}<rect x="6" y="40" width="5" height="36" fill="{WOOD[2]}"/><rect x="49" y="40" width="5" height="36" fill="{WOOD[2]}"/><rect x="10" y="62" width="40" height="4" fill="{WOOD[2]}"/>{two(0,34,60,9,WOOD[1],WOOD[2],3)}
      <path d="M6 34 Q6 24 30 24 Q54 24 54 34 Z" fill="{Q["cream"]}"/><path d="M30 24 Q54 24 54 34 L30 34 Z" fill="{Q["cream2"]}"/>
      <path d="M22 0 L36 0 L34 6 Q42 12 40 26 L18 26 Q16 12 24 6 Z" fill="#a9cbe0"/><path d="M29 0 L36 0 L34 6 Q42 12 40 26 L29 26 Z" fill="#7fa9c2"/><path d="M40 10 Q48 10 46 20 L40 22" stroke="#7fa9c2" stroke-width="3" fill="none"/><path d="M22 0 L16 -2 L22 4 Z" fill="#a9cbe0"/>
      <rect x="10" y="46" width="22" height="8" rx="2" fill="#fff"/><rect x="10" y="50" width="22" height="2" fill="{Q["coral"]}"/></g>'''
def nightstand(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(22,62,22,4)}{two(2,24,40,38,WOOD[1],WOOD[2],3)}<rect x="6" y="30" width="32" height="12" rx="2" fill="{WOOD[0]}" opacity=".5"/><circle cx="22" cy="36" r="2" fill="{GOLD[1]}"/><rect x="6" y="46" width="32" height="12" rx="2" fill="{WOOD[0]}" opacity=".5"/><circle cx="22" cy="52" r="2" fill="{GOLD[1]}"/>
      <circle cx="12" cy="6" r="14" fill="{Q["mustard"]}" opacity=".16"/><rect x="9" y="6" width="6" height="16" rx="1" fill="{Q["cream"]}"/><path d="M12 -2 C9 2 10 6 12 6 C14 6 15 2 12 -2 Z" fill="{Q["mustard"]}"/><path d="M4 22 Q12 18 20 22" stroke="{GOLD[2]}" stroke-width="3" fill="none"/>
      <rect x="24" y="14" width="16" height="10" rx="1" fill="{Q["navy"]}"/><rect x="24" y="12" width="16" height="3" fill="{Q["coral"]}"/></g>'''
def trunks(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(36,62,38,5)}{two(0,30,72,32,Q["brown"],Q["brown2"],4)}<rect x="0" y="38" width="72" height="4" fill="{GOLD[2]}"/><rect x="14" y="30" width="5" height="32" fill="{GOLD[2]}"/><rect x="52" y="30" width="5" height="32" fill="{GOLD[2]}"/><rect x="32" y="40" width="8" height="8" rx="1" fill="{GOLD[1]}"/>
      {two(8,6,54,24,Q["olive"],Q["olive2"],4)}<rect x="8" y="14" width="54" height="3" fill="{Q["cream"]}"/><path d="M26 6 Q35 -4 44 6" stroke="{Q["brown2"]}" stroke-width="3" fill="none"/></g>'''
def dressing_screen(x,y):
    panel=lambda dx,c,c2: f'<g transform="translate({dx} 0)"><path d="M0 10 Q13 0 26 10 L26 86 L0 86 Z" fill="{WOOD[1]}"/><path d="M3 12 Q13 4 23 12 L23 82 L3 82 Z" fill="{c}"/><path d="M13 4 Q20 6 23 12 L23 82 L13 82 Z" fill="{c2}"/><circle cx="13" cy="36" r="5" fill="{Q["cream"]}" opacity=".6"/><rect x="2" y="86" width="5" height="6" fill="{WOOD[2]}"/><rect x="19" y="86" width="5" height="6" fill="{WOOD[2]}"/></g>'
    return f'<g transform="translate({x} {y})">{shadow(42,92,44,5)}{panel(0,"#a9cbe0","#7fa9c2")}{panel(28,Q["pink"],Q["pink2"])}{panel(56,"#a9cbe0","#7fa9c2")}<path d="M60 6 Q70 2 76 14 L70 30 Q64 20 60 24 Z" fill="{Q["coral"]}"/></g>'
def slippers(x,y): return f'<g transform="translate({x} {y})">{shadow(16,16,16,3)}<path d="M0 8 Q0 2 8 2 L14 2 Q16 8 14 14 L6 14 Q0 14 0 8 Z" fill="{Q["coral"]}"/><path d="M8 2 L14 2 Q16 8 14 14 L8 14 Z" fill="{Q["coral2"]}"/><path d="M16 10 Q16 4 24 4 L30 4 Q32 10 30 16 L22 16 Q16 16 16 10 Z" fill="{Q["coral"]}"/><circle cx="11" cy="8" r="3" fill="#fff" opacity=".8"/><circle cx="27" cy="10" r="3" fill="#fff" opacity=".8"/></g>'
def pillow_s(x,y): return f'<g transform="translate({x} {y})">{shadow(16,18,16,3)}<rect x="0" y="2" width="32" height="16" rx="7" fill="{Q["pink"]}"/><rect x="18" y="2" width="14" height="16" rx="7" fill="{Q["pink2"]}"/><circle cx="16" cy="10" r="2" fill="{Q["cream"]}"/></g>'
def candle_s(x,y): return f'<g transform="translate({x} {y})">{shadow(10,30,10,3)}<circle cx="10" cy="4" r="12" fill="{Q["mustard"]}" opacity=".16"/><rect x="7" y="8" width="6" height="16" rx="1" fill="{Q["cream"]}"/><path d="M10 0 C7 4 8 8 10 8 C12 8 13 4 10 0 Z" fill="{Q["mustard"]}"/><path d="M0 26 Q10 20 20 26 L18 30 L2 30 Z" fill="{GOLD[1]}"/><path d="M20 24 q5 0 5 4" stroke="{GOLD[2]}" stroke-width="2" fill="none"/></g>'
def hatbox(x,y): return f'<g transform="translate({x} {y})">{shadow(16,28,16,3)}{two(2,8,28,20,"#a9cbe0","#7fa9c2",3)}<ellipse cx="16" cy="8" rx="15" ry="5" fill="#cfe3ea"/><path d="M16 3 L16 28" stroke="{Q["coral"]}" stroke-width="3"/><path d="M10 0 Q16 6 22 0" stroke="{Q["coral"]}" stroke-width="2.4" fill="none"/></g>'
# ---------- CLOCK TOWER
def gear(x,y,r,c,c2,teeth=10,hole=True,rot=0):
    t=''.join(f'<rect x="{-r*0.16:.1f}" y="{-r-r*0.22:.1f}" width="{r*0.32:.1f}" height="{r*0.4:.1f}" rx="1" fill="{c}" transform="rotate({rot+k*360/teeth:.1f})"/>' for k in range(teeth))
    return f'<g transform="translate({x} {y})">{t}<circle cx="0" cy="0" r="{r}" fill="{c}"/><path d="M0 {-r} A{r} {r} 0 0 1 0 {r} Z" fill="{c2}"/>{f"<circle cx=\"0\" cy=\"0\" r=\"{r*0.55:.1f}\" fill=\"none\" stroke=\"{c2}\" stroke-width=\"{max(1.4,r*0.08):.1f}\"/><circle cx=\"0\" cy=\"0\" r=\"{r*0.18:.1f}\" fill=\"{DARK}\"/>" if hole else ""}</g>'
def clock_face(x,y,r):
    ticks=''.join(f'<rect x="-1.6" y="{-r+6}" width="3.2" height="{10 if k%3==0 else 6}" fill="{DARK}" transform="rotate({k*30})"/>' for k in range(12))
    return f'''<g transform="translate({x} {y})"><circle cx="0" cy="0" r="{r+8}" fill="{GOLD[2]}"/><circle cx="0" cy="0" r="{r+4}" fill="{GOLD[1]}"/><circle cx="0" cy="0" r="{r}" fill="{Q["cream"]}"/><path d="M0 {-r} A{r} {r} 0 0 1 0 {r} Z" fill="{Q["cream2"]}" opacity=".5"/>{ticks}
      <path d="M0 0 L0 {-r*0.72:.1f}" stroke="{DARK}" stroke-width="4" stroke-linecap="round"/><path d="M0 0 L{r*0.46:.1f} {r*0.12:.1f}" stroke="{DARK}" stroke-width="5" stroke-linecap="round"/><circle cx="0" cy="0" r="5" fill="{GOLD[2]}"/></g>'''
def weight(x,y,len_,c,c2): return f'<g transform="translate({x} {y})"><path d="M0 0 L0 {len_}" stroke="{IRON[2]}" stroke-width="2.4" stroke-dasharray="4 2"/><path d="M-8 {len_} L8 {len_} L6 {len_+30} L-6 {len_+30} Z" fill="{c}"/><path d="M0 {len_} L8 {len_} L6 {len_+30} L0 {len_+30} Z" fill="{c2}"/><circle cx="0" cy="{len_}" r="3" fill="{IRON[2]}"/></g>'
def clock_head():
    w=f'<rect x="0" y="0" width="390" height="214" fill="#8f877a"/>'
    for r in range(10):
        for k in range(-1,8): w+=f'<rect x="{k*52+(r%2)*26+2}" y="{r*22+2}" width="48" height="18" rx="3" fill="{"#998f82" if (r+k)%2 else "#958b7e"}"/>'
    w+=f'<path d="M0 30 L130 140" stroke="{WOOD[2]}" stroke-width="12"/><path d="M390 30 L260 140" stroke="{WOOD[2]}" stroke-width="12"/><rect x="0" y="18" width="390" height="14" fill="{WOOD[1]}"/><rect x="0" y="28" width="390" height="4" fill="{WOOD[2]}"/>'
    w+=gear(58,92,34,IRON[0],IRON[1],12,True,6)+gear(104,58,20,BRASS[0],BRASS[1],9,True,10)+gear(332,98,28,BRASS[0],BRASS[1],11,True,0)+gear(294,62,18,IRON[0],IRON[1],9,True,14)
    w+=weight(128,32,80,IRON[1],IRON[2])+weight(262,32,64,IRON[1],IRON[2])
    w+=clock_face(195,72,40)
    w+=f'<rect x="148" y="118" width="94" height="96" fill="#6b645b"/>'+gate_arch(164,62,(WOOD[1],WOOD[2]))
    return w
def big_gear(x,y):
    return f'<g transform="translate({x} {y})">{shadow(42,94,40,6)}<path d="M14 94 L42 44 L70 94" stroke="{WOOD[2]}" stroke-width="7" fill="none"/>{two(8,86,68,8,WOOD[1],WOOD[2],2)}{gear(42,40,32,BRASS[0],BRASS[1],12,True,8)}</g>'
def gear_train(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(52,84,54,6)}<rect x="0" y="0" width="7" height="84" rx="2" fill="{WOOD[1]}"/><rect x="97" y="0" width="7" height="84" rx="2" fill="{WOOD[2]}"/><rect x="0" y="76" width="104" height="8" rx="2" fill="{WOOD[1]}"/>
      {gear(30,46,22,IRON[0],IRON[1],10,True,0)}{gear(66,30,15,BRASS[0],BRASS[1],8,True,20)}{gear(76,60,11,BRASS[0],BRASS[1],7,True,4)}<rect x="0" y="4" width="104" height="6" rx="2" fill="{WOOD[1]}"/></g>'''
def pendulum_case(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(26,112,28,5)}<path d="M4 16 Q26 -4 48 16 Z" fill="{WOOD[1]}"/>{two(4,14,44,98,WOOD[1],WOOD[2],3)}<rect x="10" y="44" width="32" height="60" rx="3" fill="#2f3a44"/>
      <path d="M26 46 L18 86" stroke="{BRASS[1]}" stroke-width="2.4"/><circle cx="18" cy="88" r="7" fill="{BRASS[0]}"/><path d="M18 81 A7 7 0 0 1 18 95 Z" fill="{BRASS[1]}"/>{clock_face(26,28,10).replace('r="18"','r="14"')}</g>'''
def hourglass(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(20,66,20,4)}{two(0,0,40,7,WOOD[1],WOOD[2],2)}{two(0,58,40,8,WOOD[1],WOOD[2],2)}<rect x="3" y="6" width="4" height="52" fill="{WOOD[1]}"/><rect x="33" y="6" width="4" height="52" fill="{WOOD[2]}"/>
      <path d="M9 8 L31 8 Q31 24 22 32 Q31 40 31 56 L9 56 Q9 40 18 32 Q9 24 9 8 Z" fill="#cfe3ea" opacity=".8"/><path d="M13 14 L27 14 Q25 24 20 28 Q15 24 13 14 Z" fill="{Q["tan"]}"/><path d="M11 56 Q20 42 29 56 Z" fill="{Q["tan"]}"/><rect x="19.4" y="30" width="1.4" height="20" fill="{Q["tan"]}"/></g>'''
def workbench(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(50,68,52,6)}<rect x="6" y="32" width="7" height="36" fill="{WOOD[2]}"/><rect x="88" y="32" width="7" height="36" fill="{WOOD[2]}"/><rect x="10" y="54" width="80" height="5" fill="{WOOD[2]}"/>{two(0,26,100,10,WOOD[0],WOOD[1],2)}
      {gear(22,16,10,BRASS[0],BRASS[1],8,True,0)}<rect x="40" y="18" width="24" height="8" rx="1" fill="{IRON[1]}"/><path d="M44 18 L44 10 L60 10 L60 18" stroke="{IRON[2]}" stroke-width="3" fill="none"/><g transform="rotate(-20 82 18)"><rect x="70" y="18" width="22" height="4" rx="2" fill="{WOOD[2]}"/><rect x="88" y="12" width="6" height="14" rx="1" fill="{IRON[0]}"/></g>{gear(70,48,6,IRON[0],IRON[1],6,False)}</g>'''
def weights_stand(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(28,62,30,5)}{two(0,54,56,8,WOOD[1],WOOD[2],2)}<rect x="2" y="0" width="5" height="56" fill="{WOOD[1]}"/><rect x="49" y="0" width="5" height="56" fill="{WOOD[2]}"/><rect x="0" y="0" width="56" height="6" rx="2" fill="{WOOD[1]}"/>
      {weight(16,6,10,IRON[1],IRON[2])}{weight(40,6,16,BRASS[0],BRASS[1])}</g>'''
def cog_crate(x,y):
    return f'<g transform="translate({x} {y})">{shadow(30,54,32,5)}{gear(20,14,10,BRASS[0],BRASS[1],8,True,0)}{gear(40,10,8,IRON[0],IRON[1],7,True,10)}{two(0,18,60,36,WOOD[1],WOOD[2],3)}<path d="M4 24 L56 48 M56 24 L4 48" stroke="{WOOD[2]}" stroke-width="3" opacity=".7"/><rect x="0" y="18" width="60" height="5" fill="{WOOD[2]}"/></g>'
def cog_s(x,y): return f'<g transform="translate({x} {y})">{shadow(12,24,12,3)}{gear(12,12,9,BRASS[0],BRASS[1],8,True,0)}</g>'
def cog_s2(x,y): return f'<g transform="translate({x} {y})">{shadow(14,24,14,3)}{gear(10,14,7,IRON[0],IRON[1],7,True,0)}{gear(22,8,5,BRASS[0],BRASS[1],6,False,0)}</g>'
def oilcan(x,y): return f'<g transform="translate({x} {y})">{shadow(14,28,14,3)}<path d="M2 12 L22 12 L20 28 L4 28 Z" fill="{Q["coral"]}"/><path d="M14 12 L22 12 L20 28 L14 28 Z" fill="{Q["coral2"]}"/><ellipse cx="12" cy="12" rx="10" ry="3" fill="{Q["coral2"]}"/><path d="M12 10 L10 4 L30 -2" stroke="{IRON[1]}" stroke-width="3" fill="none" stroke-linecap="round"/><path d="M22 16 Q30 18 28 26" stroke="{IRON[2]}" stroke-width="2.4" fill="none"/></g>'
# ---------- TREASURY, bigger pieces (v3)
def small_chest_svg(x,y,s=1,open_=False):
    lid=(f'<path d="M2 12 L6 -6 L42 -6 L46 12 Z" fill="{WOOD[2]}"/><rect x="6" y="-6" width="36" height="3" fill="{GOLD[2]}"/>' if open_ else
         f'<path d="M0 12 Q0 0 24 0 Q48 0 48 12 Z" fill="{WOOD[1]}"/><path d="M24 0 Q48 0 48 12 L24 12 Z" fill="{WOOD[2]}"/>')
    inside=f'<path d="M3 14 Q12 4 24 6 Q36 4 45 14 Z" fill="{GOLD[1]}"/>{coin(14,10,4)}{coin(28,8,4)}{coin(36,12,3.6)}' if open_ else ''
    return f'<g transform="translate({x} {y}) scale({s})">{lid}{inside}{two(0,12,48,24,WOOD[1],WOOD[2],3)}<rect x="0" y="16" width="48" height="4" fill="{GOLD[2]}"/><rect x="8" y="12" width="4" height="24" fill="{GOLD[2]}"/><rect x="36" y="12" width="4" height="24" fill="{GOLD[2]}"/><rect x="20" y="18" width="8" height="9" rx="1" fill="{GOLD[1]}"/></g>'
def hoard(x,y):
    coins=''.join(coin(cx,cy,r) for cx,cy,r in ((30,70,6),(46,60,6),(62,48,6),(78,40,6),(96,46,6),(112,58,6),(128,72,6),(40,80,5),(58,72,6),(74,60,6),(92,64,6),(108,76,6),(84,82,5),(20,84,5),(136,84,5),(66,86,5),(100,88,5)))
    sword=f'<g transform="rotate(12 92 30)"><rect x="89" y="2" width="6" height="34" fill="#dfe3e8"/><rect x="92" y="2" width="3" height="34" fill="#b9bfc7"/><rect x="80" y="-2" width="24" height="5" rx="2" fill="{GOLD[1]}"/><rect x="90" y="-16" width="4" height="14" rx="1" fill="{Q["brown"]}"/><circle cx="92" cy="-18" r="3.4" fill="{GOLD[1]}"/></g>'
    return f'''<g transform="translate({x} {y})">{shadow(76,94,78,8)}<path d="M0 94 Q14 58 44 46 Q62 24 82 28 Q106 32 120 52 Q146 64 152 94 Z" fill="{GOLD[1]}"/><path d="M82 28 Q106 32 120 52 Q146 64 152 94 L82 94 Z" fill="{GOLD[2]}"/>
      <path d="M30 60 Q50 44 66 40" stroke="{GOLD[0]}" stroke-width="5" fill="none" stroke-linecap="round" opacity=".8"/>{coins}{sword}<g transform="rotate(-14 56 40)">{crown(40,22,.9)}</g>
      {small_chest_svg(4,62,.7,True)}{gem(112,50,Q["coral"],Q["coral2"],1)}{gem(64,64,"#6fb3b8","#3f8a8f",.9)}<g transform="translate(124 70) rotate(70)"><path d="M0 0 L16 0 Q16 12 8 14 Q0 12 0 0 Z" fill="{GOLD[0]}"/><rect x="6" y="14" width="4" height="7" fill="{GOLD[2]}"/></g></g>'''
def armor_gold(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(26,114,26,5)}{two(4,104,44,10,WOOD[1],WOOD[2],2)}{two(14,70,11,36,GOLD[1],GOLD[2],3)}{two(27,70,11,36,GOLD[1],GOLD[2],3)}<rect x="12" y="102" width="14" height="5" rx="2" fill="{GOLD[2]}"/><rect x="26" y="102" width="14" height="5" rx="2" fill="{GOLD[2]}"/>
      <rect x="2" y="34" width="9" height="30" rx="4" fill="{GOLD[1]}"/><rect x="41" y="34" width="9" height="30" rx="4" fill="{GOLD[2]}"/><path d="M10 28 L42 28 L40 64 Q26 72 12 64 Z" fill="{GOLD[1]}"/><path d="M26 28 L42 28 L40 64 Q34 68 26 69 Z" fill="{GOLD[2]}"/>
      <path d="M16 36 Q26 44 36 36" stroke="{GOLD[0]}" stroke-width="2.4" fill="none"/><rect x="12" y="60" width="28" height="5" fill="{Q["coral"]}"/><ellipse cx="10" cy="32" rx="10" ry="7" fill="{GOLD[0]}"/><ellipse cx="42" cy="32" rx="10" ry="7" fill="{GOLD[2]}"/>
      {helmet(12,2,1,GOLD[1],GOLD[2])}<rect x="48" y="0" width="3" height="104" fill="{WOOD[2]}"/><path d="M49.5 -10 L54 2 L45 2 Z" fill="#dfe3e8"/></g>'''
def gem_dome(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(25,102,24,5)}{two(10,52,30,46,Q["grey"],Q["grey2"],2)}<rect x="5" y="48" width="40" height="7" rx="2" fill="{Q["grey"]}"/><rect x="5" y="96" width="40" height="7" rx="2" fill="{Q["grey2"]}"/>
      <ellipse cx="25" cy="47" rx="17" ry="5" fill="{Q["coral"]}"/>{gem(7,14,Q["coral"],Q["coral2"],1.8)}<path d="M5 48 Q5 4 25 4 Q45 4 45 48 Z" fill="#a9cbe0" opacity=".3"/><path d="M5 48 Q5 4 25 4 Q45 4 45 48" fill="none" stroke="#cfe3ea" stroke-width="2"/>
      <path d="M11 38 Q10 16 20 10" stroke="#fff" stroke-opacity=".7" stroke-width="3" fill="none" stroke-linecap="round"/><rect x="21" y="0" width="8" height="5" rx="2" fill="{GOLD[1]}"/></g>'''
def chest_open(x,y):
    pearls=''.join(f'<circle cx="{18+k*4.2:.1f}" cy="{40+12*math.sin(k*0.34):.1f}" r="2.6" fill="#f6f1e6"/>' for k in range(10))
    return f'''<g transform="translate({x} {y})">{shadow(42,74,44,6)}<path d="M4 34 L10 4 L74 4 L80 34 Z" fill="{WOOD[2]}"/><path d="M14 8 L70 8 L74 30 L10 30 Z" fill="#5a3a24"/><rect x="10" y="4" width="64" height="4" fill="{GOLD[2]}"/>
      <path d="M6 38 Q16 18 34 20 Q46 12 60 20 Q74 22 78 38 Z" fill="{GOLD[1]}"/><path d="M42 16 Q60 18 70 24 Q76 30 78 38 L42 38 Z" fill="{GOLD[2]}"/>{coin(20,30,5)}{coin(34,24,5)}{coin(50,22,5)}{coin(64,30,5)}{coin(42,32,5)}{gem(52,8,Q["coral"],Q["coral2"],.8)}
      {two(2,36,80,34,WOOD[1],WOOD[2],4)}<rect x="2" y="42" width="80" height="5" fill="{GOLD[2]}"/><rect x="12" y="36" width="5" height="34" fill="{GOLD[2]}"/><rect x="67" y="36" width="5" height="34" fill="{GOLD[2]}"/><rect x="36" y="44" width="12" height="12" rx="2" fill="{GOLD[1]}"/><circle cx="42" cy="50" r="2" fill="{DARK}"/>
      {pearls}{coin(90,70,4)}{coin(-2,68,4)}</g>'''
def lion_statue(x,y):
    mane=''.join(f'<circle cx="{30+17*math.cos(a):.1f}" cy="{30+17*math.sin(a):.1f}" r="7" fill="{GOLD[2]}"/>' for a in [k*0.628 for k in range(10)])
    return f'''<g transform="translate({x} {y})">{shadow(42,100,40,6)}{two(8,66,68,32,Q["grey"],Q["grey2"],2)}<rect x="4" y="62" width="76" height="7" rx="2" fill="{Q["grey"]}"/><rect x="4" y="96" width="76" height="6" rx="2" fill="{Q["grey2"]}"/>
      <path d="M70 52 Q86 46 80 30 Q78 24 74 26" stroke="{GOLD[2]}" stroke-width="5" fill="none" stroke-linecap="round"/><circle cx="74" cy="25" r="5" fill="{GOLD[2]}"/>
      <path d="M30 62 Q30 34 50 32 Q72 32 74 62 Z" fill="{GOLD[1]}"/><path d="M52 32 Q72 32 74 62 L52 62 Z" fill="{GOLD[2]}"/><rect x="26" y="44" width="10" height="20" rx="4" fill="{GOLD[1]}"/><rect x="38" y="46" width="10" height="18" rx="4" fill="{GOLD[0]}"/>
      {mane}<circle cx="30" cy="30" r="17" fill="{GOLD[2]}"/><circle cx="30" cy="31" r="12" fill="{GOLD[0]}"/><circle cx="25" cy="28" r="1.8" fill="{DARK}"/><circle cx="35" cy="28" r="1.8" fill="{DARK}"/><path d="M27 33 L33 33 L30 36 Z" fill="{Q["brown2"]}"/><path d="M30 36 Q27 39 24 37 M30 36 Q33 39 36 37" stroke="{Q["brown2"]}" stroke-width="1.4" fill="none"/>
      <circle cx="18" cy="18" r="4" fill="{GOLD[2]}"/><circle cx="42" cy="18" r="4" fill="{GOLD[2]}"/></g>'''
def vault_shelves(x,y):
    plate=lambda px,py: f'<ellipse cx="{px}" cy="{py}" rx="9" ry="10" fill="{GOLD[1]}"/><ellipse cx="{px}" cy="{py}" rx="5" ry="6" fill="{GOLD[0]}"/>'
    return f'''<g transform="translate({x} {y})">{shadow(50,106,52,6)}{two(0,0,100,104,WOOD[1],WOOD[2],3)}<rect x="5" y="5" width="90" height="94" rx="2" fill="#2a3f39"/>
      <rect x="5" y="34" width="90" height="4" fill="{WOOD[1]}"/><rect x="5" y="66" width="90" height="4" fill="{WOOD[1]}"/>
      {plate(18,22)}{plate(40,22)}{gold_bar(56,20)}{coin_stack(14,62,4)}{coin_stack(34,62,6)}<g transform="translate(58 40) scale(.9)"><path d="M0 0 L22 0 Q22 16 11 18 Q0 16 0 0 Z" fill="{GOLD[1]}"/><path d="M11 0 L22 0 Q22 16 11 18 Z" fill="{GOLD[2]}"/><rect x="9" y="18" width="4" height="6" fill="{GOLD[2]}"/><rect x="5" y="24" width="12" height="3" fill="{GOLD[1]}"/></g>
      {gold_bar(10,86)}{gold_bar(44,86)}{gold_bar(27,74)}<g transform="translate(80 76)">{coin(0,8,8)}</g><rect x="5" y="98" width="90" height="3" fill="{WOOD[2]}"/></g>'''
def coin_pile(x,y): return f'<g transform="translate({x} {y})">{shadow(18,20,20,3)}<path d="M0 20 Q6 6 18 4 Q30 6 36 20 Z" fill="{GOLD[1]}"/><path d="M18 4 Q30 6 36 20 L18 20 Z" fill="{GOLD[2]}"/>{coin(11,13,4)}{coin(22,9,4)}{coin(28,16,3.6)}{coin(40,20,3.4)}</g>'
def small_chest(x,y): return f'<g transform="translate({x} {y})">{shadow(17,30,18,3)}{small_chest_svg(0,0,.72)}</g>'
def coin_spill(x,y): return f'<g transform="translate({x} {y})">'+''.join(f'<ellipse cx="{cx}" cy="{cy}" rx="5.4" ry="3" fill="{GOLD[2]}"/><ellipse cx="{cx}" cy="{cy-1}" rx="5.4" ry="3" fill="{GOLD[1]}"/><ellipse cx="{cx}" cy="{cy-1}" rx="2.6" ry="1.2" fill="{GOLD[0]}"/>' for cx,cy in ((6,8),(16,4),(20,12),(30,7),(38,13)))+'</g>'

# ---------- MUSIC ROOM, set pieces (v3)
def m_chair(cx,cy,c=None,c2=None):
    c=c or Q["coral"]; c2=c2 or Q["coral2"]
    return f'<g transform="translate({cx} {cy})"><rect x="-11" y="-34" width="22" height="30" rx="4" fill="{WOOD[1]}"/><rect x="-7" y="-30" width="14" height="22" rx="3" fill="{c}"/><rect x="-12" y="-6" width="24" height="7" rx="3" fill="{c2}"/><rect x="-10" y="0" width="4" height="16" fill="{WOOD[2]}"/><rect x="6" y="0" width="4" height="16" fill="{WOOD[2]}"/></g>'
def m_stand(cx,cy):
    return f'<g transform="translate({cx} {cy})"><path d="M-8 30 L0 20 L8 30" stroke="{BRASS[1]}" stroke-width="2.4" fill="none"/><rect x="-1.2" y="0" width="2.4" height="22" fill="{BRASS[1]}"/><path d="M-14 -16 L14 -16 L13 2 L-13 2 Z" fill="{BRASS[2]}"/><rect x="-12" y="-20" width="11" height="19" fill="{Q["cream"]}" transform="rotate(-4 -6 -10)"/><rect x="1" y="-20" width="11" height="19" fill="{Q["cream2"]}" transform="rotate(4 6 -10)"/>{"".join(f"<rect x=\"-10\" y=\"{-16+k*4}\" width=\"8\" height=\".9\" fill=\"{Q['brown']}\"/><rect x=\"3\" y=\"{-16+k*4}\" width=\"8\" height=\".9\" fill=\"{Q['brown']}\"/>" for k in range(4))}</g>'
def quartet(x,y):
    return f'''<g transform="translate({x} {y})"><ellipse cx="72" cy="80" rx="72" ry="22" fill="{Q["coral2"]}"/><ellipse cx="72" cy="78" rx="68" ry="20" fill="{Q["coral"]}"/><ellipse cx="72" cy="78" rx="56" ry="14" fill="none" stroke="{GOLD[1]}" stroke-width="2.4"/>
      {m_chair(30,66)}{m_chair(72,60,Q["navy"],Q["navy2"])}{m_chair(114,66)}<g transform="translate(118 26) rotate(10)">{violin(0,0,.9)}</g>      {m_stand(46,72)}{m_stand(98,72)}</g>'''
def harpsichord(x,y):
    keys=''.join(f'<rect x="{3+k*3.6:.1f}" y="40" width="3" height="9" fill="#f6f1e6"/>' for k in range(9))+''.join(f'<rect x="{5.4+k*3.6:.1f}" y="40" width="2" height="5" fill="{DARK}"/>' for k in range(8) if k%3!=2)
    return f'''<g transform="translate({x} {y})">{shadow(60,88,60,6)}<path d="M8 56 L12 86 M58 56 L58 86 M108 54 L104 86" stroke="{WOOD[2]}" stroke-width="5" stroke-linecap="round"/>
      <path d="M2 2 L60 -14 L118 22 L118 30 L2 30 Z" fill="{GOLD[2]}"/><path d="M6 4 L60 -10 L112 22 L112 28 L6 28 Z" fill="#a9cbe0"/><path d="M6 20 Q30 8 56 18 Q80 10 112 24 L112 28 L6 28 Z" fill="{Q["olive"]}"/><circle cx="34" cy="6" r="5" fill="{Q["cream"]}"/><path d="M60 26 L60 -10" stroke="{GOLD[2]}" stroke-width="2"/>
      <path d="M0 32 L84 32 Q110 32 120 42 L120 58 L0 58 Z" fill="{Q["coral"]}"/><path d="M60 32 L84 32 Q110 32 120 42 L120 58 L60 58 Z" fill="{Q["coral2"]}"/><rect x="0" y="32" width="120" height="4" fill="{GOLD[1]}"/><rect x="0" y="54" width="120" height="4" fill="{GOLD[2]}"/>
      <rect x="2" y="38" width="36" height="12" rx="1" fill="{DARK}"/>{keys}<rect x="8" y="18" width="24" height="14" fill="{Q["cream"]}"/>{"".join(f'<rect x="10" y="{21+k*3}" width="20" height=".9" fill="{Q["brown"]}"/>' for k in range(3))}</g>'''
def conductor_podium(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(30,90,32,5)}{two(6,56,52,34,WOOD[1],WOOD[2],3)}<rect x="2" y="52" width="60" height="7" rx="2" fill="{Q["coral"]}"/><rect x="12" y="64" width="40" height="20" rx="2" fill="{WOOD[0]}" opacity=".4"/>{note(25,64,GOLD[1],.7)}
      <rect x="31" y="20" width="3" height="34" fill="{BRASS[1]}"/><path d="M4 4 L60 4 L58 22 L6 22 Z" fill="{BRASS[2]}"/><path d="M6 0 L32 4 L32 22 L8 20 Z" fill="{Q["cream"]}"/><path d="M58 0 L32 4 L32 22 L56 20 Z" fill="{Q["cream2"]}"/>
      {"".join(f'<path d="M10 {6+k*4} L30 {8+k*4} M34 {8+k*4} L54 {6+k*4}" stroke="{Q["brown"]}" stroke-width=".9"/>' for k in range(4))}<path d="M20 -2 L50 -10" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/><circle cx="20" cy="-2" r="2.4" fill="{WOOD[1]}"/></g>'''
def violin_case(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(30,30,30,3)}<path d="M2 16 Q2 4 16 4 L42 6 Q58 8 58 16 Q58 24 42 26 L16 28 Q2 28 2 16 Z" fill="{Q["brown2"]}"/><path d="M6 16 Q6 8 17 8 L41 10 Q54 11 54 16 Q54 21 41 22 L17 24 Q6 24 6 16 Z" fill="{Q["navy"]}"/>
      <g transform="translate(52 12) rotate(90) scale(.4)">{violin(0,0,1)}</g><path d="M16 2 L42 4" stroke="{Q["brown2"]}" stroke-width="3"/></g>'''
def instrument_case(x,y):
    return f'<g transform="translate({x} {y})">{shadow(28,26,30,3)}<path d="M2 14 Q2 2 14 2 Q22 2 26 8 L50 8 Q56 8 56 14 Q56 20 50 20 L26 20 Q22 26 14 26 Q2 26 2 14 Z" fill="{DARK}"/><path d="M2 14 Q2 2 14 2 Q22 2 26 8 L50 8 Q56 8 56 12 L2 12 Z" fill="#45343a"/><rect x="18" y="12" width="4" height="4" fill="{GOLD[1]}"/><rect x="40" y="12" width="4" height="4" fill="{GOLD[1]}"/><path d="M28 6 Q32 0 36 6" stroke="{Q["brown"]}" stroke-width="2.4" fill="none"/></g>'
def metronome_table(x,y): return f'<g transform="translate({x} {y})">{shadow(14,46,14,3)}<rect x="6" y="24" width="3" height="22" fill="{WOOD[2]}"/><rect x="19" y="24" width="3" height="22" fill="{WOOD[2]}"/><ellipse cx="14" cy="24" rx="14" ry="4" fill="{WOOD[1]}"/>{metronome(2,-12).replace(shadow(12,34,12,3),"")}</g>'
H4['Treasury']=treasury_head()+STEP
H4['Music room']=music_head()+STEP
H4['Sewing room']=sewing_head()+STEP
H4['Guest bedrooms']=guest_head()+STEP
H4['Clock tower']=clock_head()+STEP
# props: [box(x,y,w,h) relative to the drawing's origin, svg]
add4('coin_heap',coin_heap(0,0),(0,-8,108,72)); add4('gold_stack',gold_stack(0,0),(0,4,104,56)); add4('strongbox',strongbox(0,0),(0,2,64,72)); add4('crown_cushion',crown_cushion(0,0),(0,0,56,90))
add4('scales',scales(0,0),(-6,12,86,76)); add4('jewel_case',jewel_case(0,0),(0,2,80,68)); add4('sacks_pile',sacks_pile(0,0),(0,4,82,56)); add4('gold_urn',gold_urn(0,0),(0,0,44,80))
add4('double_bass',double_bass(0,0),(0,-6,60,138)); add4('gong',gong(0,0),(-4,0,116,106)); add4('tuba',tuba(0,0),(0,-2,64,90)); add4('timpani',timpani(0,0),(0,-26,76,106)); add4('music_stand',music_stand(0,0),(0,0,52,106))
add4('bass_drum',bass_drum(0,0),(0,10,104,82)); add4('accordion_stool',accordion_stool(0,0),(0,8,64,84)); 
add4('tambourine',tambourine(0,0),(0,0,28,28)); add4('metronome',metronome(0,0),(0,0,24,38)); 
add4('spinning_wheel',spinning_wheel(0,0),(0,4,90,90)); add4('sewing_table',sewing_table(0,0),(0,-14,94,98)); add4('dress_form',dress_form(0,0),(0,-4,48,112)); add4('yarn_basket',yarn_basket(0,0),(0,-8,68,58))
add4('bolt_stand',bolt_stand(0,0),(0,0,76,86)); add4('loom',loom(0,0),(0,0,96,98)); add4('ironing_board',ironing_board(0,0),(0,-16,98,78))
add4('spools_s',spools_s(0,0),(0,0,32,26)); add4('pincushion',pincushion(0,0),(0,-2,26,26)); add4('scissors_s',scissors_s(0,0),(0,0,38,28)); add4('buttons',buttons(0,0),(0,0,38,20)); add4('yarn_s',yarn_s(0,0),(0,0,36,26))
add4('four_poster',four_poster(0,0),(0,0,104,108)); add4('quilt_bed',quilt_bed(0,0),(0,0,96,78)); add4('wardrobe',wardrobe(0,0),(0,0,68,108)); add4('washstand',washstand(0,0),(0,-2,60,80))
add4('nightstand',nightstand(0,0),(0,-6,44,70)); add4('trunks',trunks(0,0),(0,-2,72,66)); add4('dressing_screen',dressing_screen(0,0),(0,0,84,96))
add4('slippers',slippers(0,0),(0,0,32,18)); add4('pillow_s',pillow_s(0,0),(0,0,32,20)); add4('candle_s',candle_s(0,0),(-2,-8,28,40)); add4('hatbox',hatbox(0,0),(0,-2,32,32))
add4('big_gear',big_gear(0,0),(0,0,84,98)); add4('gear_train',gear_train(0,0),(0,0,104,88)); add4('pendulum_case',pendulum_case(0,0),(0,0,52,116)); add4('hourglass',hourglass(0,0),(0,0,40,70))
add4('workbench',workbench(0,0),(0,0,100,72)); add4('weights_stand',weights_stand(0,0),(0,0,56,66)); add4('cog_crate',cog_crate(0,0),(0,0,60,58))
add4('cog_s',cog_s(0,0),(0,0,24,26)); add4('cog_s2',cog_s2(0,0),(0,0,30,26)); add4('oilcan',oilcan(0,0),(0,-4,32,34)); 
add4('hoard',hoard(0,0),(0,-22,154,118)); add4('armor_gold',armor_gold(0,0),(0,-12,56,128)); add4('gem_dome',gem_dome(0,0),(0,0,50,104)); add4('chest_open',chest_open(0,0),(-8,2,104,74)); add4('lion_statue',lion_statue(0,0),(0,8,86,96)); add4('vault_shelves',vault_shelves(0,0),(0,0,100,108))
add4('coin_pile',coin_pile(0,0),(0,2,44,22)); add4('small_chest',small_chest(0,0),(0,0,36,32)); add4('coin_spill',coin_spill(0,0),(0,0,44,16))
add4('quartet',quartet(0,0),(0,8,144,94)); add4('harpsichord',harpsichord(0,0),(0,-14,122,104)); add4('conductor_podium',conductor_podium(0,0),(0,-12,64,104)); add4('violin_case',violin_case(0,0),(0,0,60,32)); add4('instrument_case',instrument_case(0,0),(0,0,58,30)); add4('metronome_table',metronome_table(0,0),(0,-12,28,60))
H4={k:re.sub(r'\s+',' ',v).strip() for k,v in H4.items()}
json.dump({'heads':H4,'props':P4},open('./fourth_floor_art.json','w'),separators=(',',':'),ensure_ascii=False)
print({k:len(v) for k,v in H4.items()}, len(P4))
