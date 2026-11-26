import json, math, re
# ================= Royal floor: Royal chambers, Wardrobe, Sitting room, Tower stairs (the Throne room to follow)
# Builds on gen24.py's helpers (and so every floor before it), same flat style: the light half of each
# object on the left, a darker half on the right, one soft shadow under anything that stands on the floor.
# Run from this folder: python3 gen25.py && python3 export_royal.py
g24=open('./gen24.py').read()
exec(g24[:g24.index("H4['Treasury']=")])
H5={}; P5={}
def add5(name,svg,box,sc=1): P5[name]=[[round(v*sc,1) for v in box],re.sub(r'\s+',' ',svg if sc==1 else f'<g transform="scale({sc})">{svg}</g>').strip()]
CRIM=('#b0405a','#8e2a40','#6a1e2e')
ROSE=('#e3aab4','#cf8d9a','#b4707e')
LILAC=('#b9a0cf','#9a7fb6','#7a5f98')
ERMINE='#f6f1e6'
def ermine(x,y,w,h):   # white fur with little black tails
    spots=''.join(f'<path d="M{x+6+k*(10 if w>40 else 6)} {y+h*0.4:.1f} l1.6 3 l-3.2 0 Z" fill="{DARK}"/>' for k in range(int((w-8)//(10 if w>40 else 6))))
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2:.1f}" fill="{ERMINE}"/>{spots}'
def crown_s(x,y,s=1): return crown(x,y,s)
def tassel(x,y,c=None): c=c or GOLD[1]; return f'<path d="M{x} {y} L{x} {y+4}" stroke="{c}" stroke-width="1.6"/><path d="M{x-3} {y+10} L{x} {y+3} L{x+3} {y+10} Z" fill="{c}"/>'

# ---------- ROYAL CHAMBERS
def royal_window(x,y):
    return f'''<g transform="translate({x} {y})"><rect x="-4" y="-4" width="56" height="104" rx="26" fill="{GOLD[2]}"/><rect x="0" y="0" width="48" height="96" rx="24" fill="#a9cbe0"/>
      <path d="M24 0 A24 24 0 0 1 48 24 L48 96 L34 96 L34 6 Z" fill="#8fb6d0"/><path d="M6 76 Q16 64 26 72 Q36 60 48 70 L48 96 L0 96 L0 80 Z" fill="{Q["olive"]}" opacity=".8"/>
      <rect x="22.5" y="0" width="3" height="96" fill="{GOLD[2]}"/><rect x="0" y="34" width="48" height="3" fill="{GOLD[2]}"/><rect x="0" y="64" width="48" height="3" fill="{GOLD[2]}"/>
      <path d="M-10 -8 L58 -8 L58 6 Q46 14 34 6 Q24 14 14 6 Q2 14 -10 6 Z" fill="{CRIM[1]}"/><rect x="-12" y="-12" width="72" height="6" rx="3" fill="{GOLD[1]}"/>
      <path d="M-10 -6 L4 -6 Q10 40 2 98 L-10 98 Z" fill="{CRIM[0]}"/><path d="M58 -6 L44 -6 Q38 40 46 98 L58 98 Z" fill="{CRIM[1]}"/>
      <path d="M-10 50 Q0 46 8 52" stroke="{GOLD[1]}" stroke-width="3" fill="none"/>{tassel(8,52)}<path d="M58 50 Q48 46 40 52" stroke="{GOLD[1]}" stroke-width="3" fill="none"/>{tassel(40,52)}</g>'''
def crest(x,y,s=1):
    return f'''<g transform="translate({x} {y}) scale({s})"><path d="M-22 0 L22 0 L22 22 Q22 42 0 50 Q-22 42 -22 22 Z" fill="{CRIM[0]}"/><path d="M0 0 L22 0 L22 22 Q22 42 0 50 Z" fill="{Q["navy"]}"/>
      <path d="M-22 0 L22 0 L22 22 Q22 42 0 50 Q-22 42 -22 22 Z" fill="none" stroke="{GOLD[1]}" stroke-width="3"/><circle cx="-10" cy="16" r="4" fill="{GOLD[0]}"/><circle cx="10" cy="30" r="4" fill="{GOLD[0]}"/>
      {crown(-14,-26,0.88)}</g>'''
def sconce_r(x,y): return f'<g transform="translate({x} {y})"><circle cx="0" cy="-6" r="18" fill="{Q["mustard"]}" opacity=".16"/><path d="M-8 10 Q0 18 8 10" stroke="{GOLD[1]}" stroke-width="3" fill="none"/><rect x="-1.5" y="4" width="3" height="10" fill="{GOLD[2]}"/><rect x="-3" y="-6" width="6" height="11" rx="1" fill="{Q["cream"]}"/><path d="M0 -15 C-3 -11 -2 -7 0 -7 C2 -7 3 -11 0 -15 Z" fill="{Q["mustard"]}"/></g>'
def royal_head():
    w=f'<rect x="0" y="0" width="390" height="214" fill="#a35d6e"/>'
    w+=''.join(f'<g transform="translate({x+(y//36%2)*18} {y})"><circle cx="0" cy="-4" r="3.2" fill="#b16b7c"/><circle cx="-4" cy="0" r="3.2" fill="#b16b7c"/><circle cx="4" cy="0" r="3.2" fill="#b16b7c"/><circle cx="0" cy="4" r="3.2" fill="#b16b7c"/><circle cx="0" cy="0" r="1.6" fill="#c9a05a"/></g>' for x in range(8,400,36) for y in range(14,146,36))
    w+=f'<rect x="0" y="146" width="390" height="68" fill="{Q["cream"]}"/>'+''.join(f'<rect x="{x+5}" y="154" width="38" height="52" rx="3" fill="none" stroke="{GOLD[1]}" stroke-width="2"/>' for x in range(0,390,48))+f'<rect x="0" y="142" width="390" height="8" fill="{GOLD[1]}"/><rect x="0" y="146" width="390" height="4" fill="{GOLD[2]}"/>'
    w+=royal_window(28,34)+royal_window(314,34)
    w+=sconce_r(118,90)+sconce_r(272,90)
    w+=f'<rect x="146" y="100" width="98" height="114" fill="#7a3a4a"/><path d="M146 100 Q195 76 244 100 Z" fill="{GOLD[1]}"/><rect x="146" y="98" width="98" height="6" fill="{GOLD[2]}"/>'+gate_arch(164,62,(CRIM[1],CRIM[2]))+f'<circle cx="216" cy="172" r="3.4" fill="{GOLD[0]}"/>'
    w+=crest(195,30,0.95)
    return w
def royal_bed(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(64,124,66,8)}
      <rect x="4" y="16" width="8" height="108" rx="2" fill="{GOLD[1]}"/><rect x="116" y="16" width="8" height="108" rx="2" fill="{GOLD[2]}"/>
      <path d="M0 22 Q64 -2 128 22 L128 30 L0 30 Z" fill="{CRIM[1]}"/><path d="M0 30 Q16 42 32 30 Q48 42 64 30 Q80 42 96 30 Q112 42 128 30" stroke="{GOLD[1]}" stroke-width="4" fill="none"/>{crown(50,-12,1.25)}
      <path d="M12 30 L32 30 Q20 70 12 88 Z" fill="{CRIM[0]}"/><path d="M116 30 L96 30 Q108 70 116 88 Z" fill="{CRIM[1]}"/>{tassel(20,70)}{tassel(108,70)}
      <path d="M22 66 Q22 40 64 40 Q106 40 106 66 Z" fill="{GOLD[1]}"/><path d="M64 40 Q106 40 106 66 L64 66 Z" fill="{GOLD[2]}"/><path d="M30 64 Q30 48 64 48 Q98 48 98 64 Z" fill="{CRIM[1]}"/>
      {pillow(22,60,"#fff",Q["cream2"],40)}{pillow(66,60,"#fff",Q["cream2"],40)}
      {two(14,72,100,40,CRIM[0],CRIM[1],6)}{ermine(14,70,100,10)}{"".join(f'<circle cx="{34+k*20}" cy="96" r="3" fill="{GOLD[0]}"/>' for k in range(4))}
      <rect x="12" y="110" width="104" height="8" rx="2" fill="{GOLD[2]}"/></g>'''
def fireplace(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(50,98,52,6)}{two(0,12,100,86,Q["cream"],Q["cream2"],3)}<rect x="-4" y="8" width="108" height="10" rx="3" fill="{Q["cream"]}"/><rect x="62" y="8" width="42" height="10" rx="3" fill="{Q["cream2"]}"/>
      <path d="M18 98 L18 52 Q18 32 50 32 Q82 32 82 52 L82 98 Z" fill="#2a1a14"/><circle cx="50" cy="82" r="30" fill="{Q["mustard"]}" opacity=".14"/>
      <rect x="28" y="86" width="44" height="7" rx="3" fill="{WOOD[2]}" transform="rotate(-6 50 90)"/><rect x="30" y="88" width="40" height="7" rx="3" fill="{WOOD[1]}" transform="rotate(8 50 90)"/>
      <path d="M36 88 Q32 72 42 62 Q42 72 48 74 Q46 60 56 50 Q56 66 64 70 Q68 78 62 88 Z" fill="{Q["orange"]}"/><path d="M42 88 Q40 78 46 72 Q48 80 54 80 Q54 70 60 66 Q62 80 58 88 Z" fill="{Q["mustard"]}"/>
      <path d="M18 98 L18 52 Q18 32 50 32 Q82 32 82 52 L82 98" stroke="{GOLD[1]}" stroke-width="3" fill="none"/>
      <rect x="6" y="-8" width="5" height="16" rx="1" fill="{Q["cream"]}"/><path d="M8.5 -16 C6 -12 7 -8 8.5 -8 C10 -8 11 -12 8.5 -16 Z" fill="{Q["mustard"]}"/><rect x="2" y="6" width="13" height="3" rx="1" fill="{GOLD[1]}"/>
      <rect x="89" y="-8" width="5" height="16" rx="1" fill="{Q["cream"]}"/><path d="M91.5 -16 C89 -12 90 -8 91.5 -8 C93 -8 94 -12 91.5 -16 Z" fill="{Q["mustard"]}"/><rect x="85" y="6" width="13" height="3" rx="1" fill="{GOLD[1]}"/></g>'''
def cradle(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(38,68,38,5)}<path d="M4 62 Q38 76 72 62" stroke="{WOOD[2]}" stroke-width="5" fill="none" stroke-linecap="round"/>
      <rect x="12" y="44" width="5" height="20" fill="{WOOD[1]}"/><rect x="58" y="44" width="5" height="20" fill="{WOOD[2]}"/>
      <path d="M6 26 L70 26 L66 50 Q38 58 10 50 Z" fill="{WOOD[1]}"/><path d="M42 26 L70 26 L66 50 Q54 54 42 55 Z" fill="{WOOD[2]}"/>
      <path d="M2 30 Q2 0 26 0 L30 0 L30 30 Z" fill="{ROSE[0]}"/><path d="M14 2 Q26 -2 30 0 L30 30 L18 30 Z" fill="{ROSE[1]}"/><path d="M2 30 Q8 34 14 30 Q20 34 26 30 Q28 32 30 30" stroke="#fff" stroke-width="2.4" fill="none"/>
      {pillow(30,20,"#fff",Q["cream2"],18)}<path d="M30 28 L68 28 L66 38 L30 38 Z" fill="{ROSE[0]}"/><rect x="30" y="26" width="38" height="4" rx="2" fill="#fff"/>
      {crown(52,4,0.46)}</g>'''
def royal_armchair(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(30,88,30,5)}<path d="M6 40 L6 8 Q6 0 30 0 Q54 0 54 8 L54 40 Z" fill="{GOLD[1]}"/><path d="M30 0 Q54 0 54 8 L54 40 L30 40 Z" fill="{GOLD[2]}"/>
      <path d="M12 40 L12 12 Q12 6 30 6 Q48 6 48 12 L48 40 Z" fill="{CRIM[0]}"/><path d="M30 6 Q48 6 48 12 L48 40 L30 40 Z" fill="{CRIM[1]}"/>{"".join(f'<circle cx="{cx}" cy="{cy}" r="1.6" fill="{GOLD[0]}"/>' for cx,cy in ((22,18),(38,18),(30,28),(22,36),(38,36)))}
      {crown(18,-16,0.75)}<rect x="0" y="40" width="10" height="18" rx="4" fill="{GOLD[1]}"/><rect x="50" y="40" width="10" height="18" rx="4" fill="{GOLD[2]}"/>
      {two(4,48,52,14,CRIM[0],CRIM[1],5)}<rect x="6" y="60" width="48" height="6" rx="2" fill="{GOLD[2]}"/><path d="M10 66 Q8 78 12 86 M50 66 Q52 78 48 86" stroke="{GOLD[2]}" stroke-width="4" fill="none" stroke-linecap="round"/></g>'''
def rose_vase(x,y,s=1):
    roses=''.join(f'<circle cx="{cx}" cy="{cy}" r="5" fill="{c}"/><path d="M{cx-2} {cy} q2 -3 4 0" stroke="{CRIM[2]}" stroke-width="1" fill="none"/>' for cx,cy,c in ((-8,-10,CRIM[0]),(0,-16,ROSE[1]),(8,-10,CRIM[0]),(-3,-6,ROSE[0]),(5,-4,CRIM[1])))
    return f'<g transform="translate({x} {y}) scale({s})"><path d="M-10 -6 Q-14 -12 -12 -16 M10 -6 Q14 -12 12 -16" stroke="{Q["olive2"]}" stroke-width="2" fill="none"/><path d="M-6 0 L6 0 Q10 10 6 18 L-6 18 Q-10 10 -6 0 Z" fill="#a9cbe0"/><path d="M0 0 L6 0 Q10 10 6 18 L0 18 Z" fill="#7fa9c2"/>{roses}</g>'
def dresser(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(40,82,42,5)}{two(0,30,80,48,Q["cream"],Q["cream2"],3)}<rect x="-2" y="26" width="84" height="7" rx="3" fill="{GOLD[1]}"/>
      {"".join(f'<rect x="6" y="{38+k*13}" width="68" height="10" rx="2" fill="none" stroke="{GOLD[1]}" stroke-width="1.6"/><circle cx="26" cy="{43+k*13}" r="2" fill="{GOLD[2]}"/><circle cx="54" cy="{43+k*13}" r="2" fill="{GOLD[2]}"/>' for k in range(3))}
      <path d="M6 78 L4 84 M74 78 L76 84" stroke="{GOLD[2]}" stroke-width="3"/>{rose_vase(20,8,1)}
      <g transform="translate(46 14)">{two(0,0,24,12,Q["navy"],Q["navy2"],2)}<path d="M-1 0 Q12 -8 25 0 Z" fill="{Q["navy"]}"/><rect x="10" y="3" width="4" height="5" fill="{GOLD[1]}"/><circle cx="6" cy="-3" r="2" fill="{CRIM[0]}"/><circle cx="16" cy="-4" r="2" fill="#6fb3b8"/></g></g>'''
def orange_tree(x,y):
    fruit=''.join(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{Q["orange"]}"/><circle cx="{cx-1.2}" cy="{cy-1.2}" r="1.3" fill="#f0b43c"/>' for cx,cy in ((14,14),(32,10),(24,26),(40,24),(10,30),(30,36)))
    return f'''<g transform="translate({x} {y})">{shadow(26,92,22,5)}<rect x="23" y="38" width="5" height="34" fill="{WOOD[2]}"/>
      <circle cx="26" cy="24" r="24" fill="{Q["green"]}"/><path d="M26 0 A24 24 0 0 1 26 48 Z" fill="{Q["green2"]}"/><circle cx="16" cy="16" r="9" fill="#4f7f45" opacity=".6"/>{fruit}
      <path d="M10 70 L42 70 L38 92 L14 92 Z" fill="#f1ede4"/><path d="M26 70 L42 70 L38 92 L26 92 Z" fill="#d8d2c4"/><rect x="8" y="66" width="36" height="6" rx="2" fill="{Q["navy"]}"/>
      <path d="M16 78 q5 -4 10 0 t10 0 M18 86 q4 -3 8 0 t8 0" stroke="{Q["navy"]}" stroke-width="2" fill="none"/></g>'''
def pet_bed(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(32,40,32,5)}<path d="M0 22 Q0 40 32 40 Q64 40 64 22 Q64 10 32 10 Q0 10 0 22 Z" fill="{Q["tan"]}"/><path d="M32 10 Q64 10 64 22 Q64 40 32 40 Z" fill="{Q["tan2"]}"/>
      <path d="M2 22 q4 -3 8 0 t8 0 t8 0 t8 0 t8 0 t8 0 t8 0 t6 0" stroke="{Q["tan2"]}" stroke-width="1.6" fill="none"/>
      <ellipse cx="32" cy="24" rx="24" ry="8" fill="{CRIM[0]}"/><path d="M32 16 A24 8 0 0 1 32 32 Z" fill="{CRIM[1]}"/>{crown(24,8,0.5)}</g>'''
def writing_desk(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(44,82,46,6)}<rect x="6" y="40" width="6" height="42" fill="{WOOD[1]}"/><rect x="76" y="40" width="6" height="42" fill="{WOOD[2]}"/><rect x="10" y="66" width="68" height="4" fill="{WOOD[2]}"/>
      {two(2,6,84,14,WOOD[1],WOOD[2],3)}{"".join(f'<rect x="{8+k*14}" y="9" width="10" height="8" rx="1" fill="{WOOD[0]}" opacity=".6"/>' for k in range(6))}
      {two(0,32,88,10,WOOD[0],WOOD[1],3)}<rect x="0" y="30" width="88" height="4" rx="2" fill="{GOLD[1]}"/>
      <path d="M14 28 L42 24 L46 32 L18 34 Z" fill="{Q["cream"]}"/><circle cx="38" cy="29" r="3" fill="{CRIM[0]}"/>
      <rect x="58" y="22" width="10" height="9" rx="2" fill="{DARK}"/><path d="M64 22 Q70 6 82 0 Q76 12 66 23 Z" fill="#fff"/><path d="M66 23 L76 6" stroke="{Q["cream2"]}" stroke-width="1"/></g>'''
def footstool(x,y,s=1):
    return f'''<g transform="translate({x} {y}) scale({s})"><path d="M6 18 Q4 26 8 30 M34 18 Q36 26 32 30" stroke="{GOLD[2]}" stroke-width="3" fill="none" stroke-linecap="round"/>
      <rect x="2" y="10" width="36" height="10" rx="3" fill="{GOLD[1]}"/><path d="M2 12 Q2 0 20 0 Q38 0 38 12 Z" fill="{CRIM[0]}"/><path d="M20 0 Q38 0 38 12 L20 12 Z" fill="{CRIM[1]}"/>
      {tassel(5,18)}{tassel(35,18)}<circle cx="20" cy="6" r="1.6" fill="{GOLD[0]}"/></g>'''
def footstool_s(x,y): return f'<g transform="translate({x} {y})">{shadow(20,31,18,3)}{footstool(0,0)}</g>'
def tea_stand(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(18,44,16,3)}<rect x="16" y="16" width="4" height="26" fill="{GOLD[2]}"/><path d="M8 44 L18 38 L28 44" stroke="{GOLD[2]}" stroke-width="3" fill="none"/>
      <ellipse cx="18" cy="16" rx="18" ry="5" fill="{GOLD[1]}"/><path d="M8 14 Q8 4 16 4 Q24 4 24 14 Z" fill="#f1ede4"/><path d="M16 4 Q24 4 24 14 L16 14 Z" fill="#d8d2c4"/><path d="M24 8 Q30 6 30 2" stroke="#d8d2c4" stroke-width="2" fill="none"/><path d="M8 8 q-4 0 -4 4" stroke="#d8d2c4" stroke-width="2" fill="none"/><circle cx="16" cy="3" r="1.6" fill="{GOLD[1]}"/><path d="M12 10 l8 0" stroke="{Q["navy"]}" stroke-width="1.4"/>
      <path d="M26 12 L32 12 L31 15 L27 15 Z" fill="#f1ede4"/></g>'''
def floor_vase(x,y): return f'<g transform="translate({x} {y})">{shadow(14,44,13,3)}<path d="M6 22 Q2 34 8 44 L20 44 Q26 34 22 22 Z" fill="#f1ede4"/><path d="M14 22 L22 22 Q26 34 20 44 L14 44 Z" fill="#d8d2c4"/><path d="M8 32 q3 -3 6 0 t6 0" stroke="{Q["navy"]}" stroke-width="2" fill="none"/><rect x="5" y="20" width="18" height="4" rx="2" fill="{Q["navy"]}"/>{rose_vase(14,18,0.9).replace("#a9cbe0","none").replace("#7fa9c2","none")}</g>'

# ---------- WARDROBE
def folded(x,y,cols):   # a stack of folded clothes, bottom first
    return ''.join(f'<rect x="{x}" y="{y-k*7}" width="26" height="7" rx="2" fill="{c[0]}"/><rect x="{x+16}" y="{y-k*7}" width="10" height="7" rx="2" fill="{c[1]}"/><rect x="{x}" y="{y-k*7}" width="26" height="1.4" fill="#fff" opacity=".35"/>' for k,c in enumerate(cols))
PAIRS=[(CRIM[0],CRIM[1]),(Q["navy"],Q["navy2"]),(Q["olive"],Q["olive2"]),(Q["mustard"],Q["mustard2"]),(LILAC[0],LILAC[1]),(Q["cream"],Q["cream2"]),(Q["pink"],Q["pink2"]),("#6fb3b8","#4f9196")]
def hat_tricorn(x,y,c,c2): return f'<g transform="translate({x} {y})"><path d="M0 14 Q14 -2 28 14 Q14 8 0 14 Z" fill="{c}"/><path d="M14 4 Q22 4 28 14 Q20 10 14 10 Z" fill="{c2}"/><path d="M2 13 Q14 7 26 13" stroke="{GOLD[1]}" stroke-width="1.6" fill="none"/></g>'
def hat_feather(x,y,c,c2): return f'<g transform="translate({x} {y})"><ellipse cx="14" cy="14" rx="16" ry="4" fill="{c2}"/><path d="M4 14 Q4 0 14 0 Q24 0 24 14 Z" fill="{c}"/><path d="M14 0 Q24 0 24 14 L14 14 Z" fill="{c2}"/><rect x="4" y="9" width="20" height="3" fill="{GOLD[1]}"/><path d="M18 8 Q30 -6 34 -14 Q30 0 22 10 Z" fill="#fff"/><path d="M22 10 L32 -10" stroke="{Q["cream2"]}" stroke-width="1"/></g>'
def wardrobe_head():
    w=f'<rect x="0" y="0" width="390" height="214" fill="{LILAC[1]}"/>'+''.join(f'<rect x="{x}" y="0" width="13" height="214" fill="{LILAC[0]}" opacity=".55"/><rect x="{x+15}" y="0" width="2" height="214" fill="{GOLD[0]}" opacity=".5"/>' for x in range(0,390,26))
    w+=f'<rect x="0" y="150" width="390" height="64" fill="{Q["cream"]}"/>'+''.join(f'<rect x="{x+5}" y="158" width="38" height="50" rx="3" fill="none" stroke="{LILAC[1]}" stroke-width="2"/>' for x in range(0,390,48))+f'<rect x="0" y="146" width="390" height="7" fill="{GOLD[1]}"/>'
    # left: open shelves of folded clothes
    sh=f'<g transform="translate(14 18)">{two(0,0,108,128,WOOD[1],WOOD[2],3)}<rect x="6" y="6" width="96" height="116" fill="#5a3a2a"/>'
    for r in range(3): sh+=f'<rect x="4" y="{40+r*40}" width="100" height="6" fill="{WOOD[1]}"/>'+folded(10,32+r*40,PAIRS[r:r+3])+folded(40,32+r*40,PAIRS[r+3:r+5])+folded(70,32+r*40,PAIRS[(r+5)%8:(r+5)%8+3] or PAIRS[:2])
    w+=sh+'</g>'
    # right: a hat shelf, and capes hanging from a rail under it
    w+=f'<g transform="translate(266 20)">{two(0,24,112,7,WOOD[1],WOOD[2],2)}{hat_feather(2,8,CRIM[0],CRIM[1])}{hat_tricorn(42,10,Q["navy"],Q["navy2"])}{crown(78,0,0.9)}'
    w+=f'<rect x="4" y="54" width="104" height="5" rx="2" fill="{GOLD[1]}"/>'
    for k,(c,c2) in enumerate(((Q["green"],Q["green2"]),(CRIM[0],CRIM[1]),(LILAC[2],"#5e4680"))):
        cx=22+k*34; w+=f'<path d="M{cx} 56 l0 -4 q0 -4 4 -4" stroke="{GOLD[2]}" stroke-width="2" fill="none"/><path d="M{cx-14} 64 L{cx} 58 L{cx+14} 64 L{cx+18} 118 L{cx-18} 118 Z" fill="{c}"/><path d="M{cx} 58 L{cx+14} 64 L{cx+18} 118 L{cx} 118 Z" fill="{c2}"/>'
        if k==1: w+=f'<path d="M{cx-14} 64 L{cx} 58 L{cx+14} 64" stroke="{GOLD[1]}" stroke-width="3" fill="none"/>'
    w+='</g>'
    w+=f'<rect x="146" y="100" width="98" height="114" fill="#5e4680"/><path d="M146 100 Q195 78 244 100 Z" fill="{GOLD[1]}"/><rect x="146" y="98" width="98" height="6" fill="{GOLD[2]}"/>'+gate_arch(164,62,(LILAC[2],"#5e4680"))+f'<circle cx="216" cy="172" r="3.4" fill="{GOLD[0]}"/>'
    w+=f'<g transform="translate(195 50)"><ellipse cx="0" cy="0" rx="24" ry="30" fill="{GOLD[1]}"/><ellipse cx="0" cy="0" rx="18" ry="24" fill="#cfe3ea"/><path d="M-8 12 L8 -14 L12 -8 L-4 16 Z" fill="#fff" opacity=".7"/>{crown(-12,-50,0.75)}</g>'
    return w
def gown_stand(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(32,112,30,5)}<rect x="30" y="98" width="4" height="12" fill="{GOLD[2]}"/><path d="M18 112 L32 104 L46 112" stroke="{GOLD[2]}" stroke-width="3" fill="none"/>
      <rect x="29" y="0" width="6" height="10" rx="2" fill="{GOLD[1]}"/><circle cx="32" cy="0" r="4" fill="{GOLD[1]}"/>
      <path d="M20 10 Q32 6 44 10 L42 36 L22 36 Z" fill="{ROSE[0]}"/><path d="M32 8 Q38 7 44 10 L42 36 L32 36 Z" fill="{ROSE[1]}"/><path d="M24 12 Q32 18 40 12" stroke="#fff" stroke-width="2.4" fill="none"/>
      <path d="M22 36 Q6 70 2 100 Q32 108 62 100 Q58 70 42 36 Z" fill="{ROSE[0]}"/><path d="M32 36 L42 36 Q58 70 62 100 Q48 104 32 105 Z" fill="{ROSE[1]}"/>
      <path d="M22 36 Q32 40 42 36 L40 40 Q32 44 24 40 Z" fill="{GOLD[1]}"/><path d="M8 84 Q32 92 56 84" stroke="{GOLD[1]}" stroke-width="3" fill="none"/><path d="M3 98 q5 4 10 0 t10 0 t10 0 t10 0 t10 0 t10 0" stroke="#fff" stroke-width="2.4" fill="none"/>
      {"".join(f'<circle cx="{cx}" cy="{cy}" r="2" fill="{GOLD[0]}"/>' for cx,cy in ((20,60),(32,66),(44,60),(14,78),(50,78),(32,52)))}</g>'''
def robe_rail(x,y):
    robes=''
    for k,(c,c2,fur) in enumerate(((CRIM[0],CRIM[1],1),(Q["navy"],Q["navy2"],0),(Q["green"],Q["green2"],0),(LILAC[1],LILAC[2],1))):
        cx=22+k*28; robes+=f'<path d="M{cx} 14 q0 -4 4 -4" stroke="{GOLD[2]}" stroke-width="2" fill="none"/><path d="M{cx-12} 20 L{cx+12} 20 L{cx+16} 86 L{cx-16} 86 Z" fill="{c}"/><path d="M{cx} 20 L{cx+12} 20 L{cx+16} 86 L{cx} 86 Z" fill="{c2}"/><path d="M{cx-12} 20 L{cx} 15 L{cx+12} 20" stroke="{GOLD[2]}" stroke-width="2.4" fill="none"/>'
        robes+=ermine(cx-13,18,26,8) if fur else f'<rect x="{cx-1}" y="22" width="2" height="60" fill="{GOLD[1]}" opacity=".8"/>'
    return f'''<g transform="translate({x} {y})">{shadow(62,100,62,6)}<rect x="2" y="6" width="6" height="94" rx="2" fill="{GOLD[1]}"/><rect x="116" y="6" width="6" height="94" rx="2" fill="{GOLD[2]}"/><rect x="0" y="8" width="124" height="5" rx="2" fill="{GOLD[1]}"/>
      <path d="M-4 100 L14 100 M110 100 L128 100" stroke="{GOLD[2]}" stroke-width="4" stroke-linecap="round"/><circle cx="5" cy="5" r="4" fill="{GOLD[0]}"/><circle cx="119" cy="5" r="4" fill="{GOLD[1]}"/>{robes}</g>'''
def hat_stand(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(26,112,22,5)}<rect x="23" y="8" width="6" height="102" rx="2" fill="{WOOD[1]}"/><path d="M10 112 L26 102 L42 112" stroke="{WOOD[2]}" stroke-width="5" fill="none" stroke-linecap="round"/>
      <path d="M26 20 Q12 18 8 26 M26 20 Q40 18 44 26" stroke="{WOOD[2]}" stroke-width="3" fill="none" stroke-linecap="round"/>
      <path d="M32 24 Q48 26 50 70 L36 72 Q36 40 30 28 Z" fill="{Q["navy"]}"/><path d="M40 26 Q48 30 50 70 L42 71 Z" fill="{Q["navy2"]}"/>
      {hat_feather(10,-4,Q["olive"],Q["olive2"])}<path d="M4 26 Q2 40 6 48 Q10 40 8 28 Z" fill="{CRIM[0]}"/></g>'''
def shoe(x,y,c,c2,boot=False):
    if boot: return f'<g transform="translate({x} {y})"><path d="M2 0 L12 0 L12 14 L20 16 Q22 20 18 20 L2 20 Z" fill="{c}"/><path d="M8 0 L12 0 L12 14 L20 16 Q22 20 18 20 L8 20 Z" fill="{c2}"/></g>'
    return f'<g transform="translate({x} {y})"><path d="M0 10 Q2 4 8 6 L18 8 Q22 10 20 14 L4 14 Q0 14 0 10 Z" fill="{c}"/><path d="M10 6.5 L18 8 Q22 10 20 14 L10 14 Z" fill="{c2}"/><rect x="1" y="12" width="3" height="6" fill="{c2}"/><circle cx="12" cy="8" r="1.6" fill="{GOLD[0]}"/></g>'
def shoe_shelf(x,y):
    s=''
    rows=[[(CRIM[0],CRIM[1],0),(LILAC[0],LILAC[1],0),(Q["mustard"],Q["mustard2"],0)],[(Q["brown"],Q["brown2"],1),(DARK,"#1a100a",1)],[(Q["pink"],Q["pink2"],0),(Q["navy"],Q["navy2"],0),(Q["green"],Q["green2"],0)]]
    for r,row in enumerate(rows):
        yy=8+r*26; n=len(row); step=74/n
        for k,(c,c2,b) in enumerate(row):
            sx=6+k*step
            s+=shoe(sx,yy,c,c2,b)+(shoe(sx+8,yy+2,c2,c2,b) if not b else shoe(sx+10,yy,c,c2,b))
    return f'''<g transform="translate({x} {y})">{shadow(42,86,44,5)}{two(0,0,86,84,WOOD[1],WOOD[2],3)}<rect x="5" y="4" width="76" height="76" fill="#5a3a2a"/>
      {"".join(f'<rect x="3" y="{28+r*26}" width="80" height="5" fill="{WOOD[1]}"/>' for r in range(3))}{s}</g>'''
def cheval_mirror(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(30,108,30,5)}<rect x="2" y="30" width="5" height="76" rx="2" fill="{GOLD[1]}"/><rect x="53" y="30" width="5" height="76" rx="2" fill="{GOLD[2]}"/>
      <path d="M-4 108 L14 104 M46 104 L64 108" stroke="{GOLD[2]}" stroke-width="4" stroke-linecap="round"/><circle cx="4.5" cy="56" r="4" fill="{GOLD[0]}"/><circle cx="55.5" cy="56" r="4" fill="{GOLD[1]}"/>
      <ellipse cx="30" cy="56" rx="23" ry="46" fill="{GOLD[1]}"/><ellipse cx="30" cy="56" rx="18" ry="40" fill="#cfe3ea"/><path d="M30 16 A18 40 0 0 1 30 96 Z" fill="#b2d0da"/>
      <path d="M18 66 L36 26 L42 32 L24 72 Z" fill="#fff" opacity=".7"/>{crown(20,0,0.62)}</g>'''
def open_closet(x,y):
    hang=''.join(f'<path d="M{18+k*12} 24 L{24+k*12} 22 L{30+k*12} 24 L{29+k*12} 70 L{19+k*12} 70 Z" fill="{c}"/>' for k,c in enumerate((CRIM[0],Q["navy"],Q["mustard"],LILAC[1],Q["green"])))
    return f'''<g transform="translate({x} {y})">{shadow(48,112,50,6)}<path d="M14 8 Q48 -6 82 8 L82 14 L14 14 Z" fill="{WOOD[1]}"/>{two(14,12,68,96,WOOD[1],WOOD[2],3)}<rect x="18" y="16" width="60" height="88" fill="#4a2e22"/>
      <rect x="18" y="20" width="60" height="3" fill="{GOLD[1]}"/>{hang}<rect x="18" y="76" width="60" height="4" fill="{WOOD[1]}"/>{folded(22,96,PAIRS[4:6])}{folded(48,96,[PAIRS[0],PAIRS[3],PAIRS[6]])}
      <path d="M14 14 L0 20 L0 104 L14 108 Z" fill="{WOOD[0]}"/><rect x="3" y="30" width="7" height="60" rx="2" fill="{WOOD[1]}" opacity=".6"/><path d="M82 14 L96 20 L96 104 L82 108 Z" fill="{WOOD[2]}"/><rect x="86" y="30" width="7" height="60" rx="2" fill="#6a4228" opacity=".6"/>
      <circle cx="10" cy="62" r="2" fill="{GOLD[1]}"/><circle cx="86" cy="62" r="2" fill="{GOLD[1]}"/></g>'''
def cobbler_bench(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(46,66,46,5)}<rect x="8" y="34" width="6" height="32" fill="{WOOD[2]}"/><rect x="78" y="34" width="6" height="32" fill="{WOOD[2]}"/>{two(0,28,92,10,WOOD[1],WOOD[2],3)}
      <rect x="22" y="14" width="6" height="16" fill="{IRON[1]}"/><path d="M14 0 L28 0 L28 14 L40 16 Q42 22 36 22 L14 22 Z" fill="{CRIM[0]}"/><path d="M22 0 L28 0 L28 14 L40 16 Q42 22 36 22 L22 22 Z" fill="{CRIM[1]}"/>
      <g transform="rotate(-18 62 22)"><rect x="50" y="20" width="24" height="4" rx="2" fill="{WOOD[2]}"/><rect x="70" y="14" width="7" height="14" rx="1" fill="{IRON[0]}"/></g>
      <rect x="48" y="22" width="10" height="6" rx="1" fill="{Q["cream2"]}"/>{"".join(f'<circle cx="{82+k*4}" cy="25" r="1.4" fill="{IRON[2]}"/>' for k in range(2))}</g>'''
def folded_s(x,y): return f'<g transform="translate({x} {y})">{shadow(16,40,16,3)}<rect x="4" y="22" width="4" height="18" fill="{WOOD[2]}"/><rect x="24" y="22" width="4" height="18" fill="{WOOD[2]}"/>{two(0,18,32,6,WOOD[1],WOOD[2],2)}{folded(3,11,[PAIRS[1],PAIRS[3],PAIRS[0]])}</g>'
# bigger pieces in place of the little slippers and the parasol pot (Matt's review of #59)
def hat_boxes(x,y):
    def box(bx,by,w,h,c,c2,stripe):
        st=''.join(f'<rect x="{bx+4+k*9}" y="{by+4}" width="4" height="{h-4}" fill="{stripe}" opacity=".7"/>' for k in range(int((w-6)//9)))
        return f'<rect x="{bx}" y="{by}" width="{w}" height="{h}" rx="3" fill="{c}"/>{st}<rect x="{bx+w*0.62:.1f}" y="{by}" width="{w*0.38:.1f}" height="{h}" rx="3" fill="{c2}" opacity=".55"/><rect x="{bx-3}" y="{by-4}" width="{w+6}" height="7" rx="3" fill="{c2}"/>'
    return f'''<g transform="translate({x} {y})">{shadow(36,96,36,5)}{box(4,64,64,32,Q["cream"],Q["cream2"],ROSE[0])}{box(10,36,52,26,"#a9cbe0","#7fa9c2","#fff")}{box(16,12,40,22,ROSE[0],ROSE[1],Q["cream"])}
      <rect x="34" y="8" width="4" height="88" fill="{CRIM[0]}"/><rect x="36" y="8" width="2" height="88" fill="{CRIM[1]}"/>
      <path d="M36 8 Q24 -4 22 4 Q24 10 36 8 Q48 -4 50 4 Q48 10 36 8 Z" fill="{CRIM[0]}"/><path d="M36 8 Q48 -4 50 4 Q48 10 36 8 Z" fill="{CRIM[1]}"/><circle cx="36" cy="7" r="3" fill="{CRIM[2]}"/>
      <path d="M33 9 L28 20 M39 9 L44 20" stroke="{CRIM[0]}" stroke-width="3" stroke-linecap="round"/></g>'''
def travel_trunk(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(48,74,48,6)}<path d="M4 26 Q4 2 48 2 Q92 2 92 26 Z" fill="{Q["navy"]}"/><path d="M48 2 Q92 2 92 26 L48 26 Z" fill="{Q["navy2"]}"/>
      {two(2,24,92,48,Q["navy"],Q["navy2"],3)}<rect x="0" y="24" width="96" height="6" rx="2" fill="{WOOD[1]}"/><rect x="0" y="66" width="96" height="6" rx="2" fill="{WOOD[2]}"/>
      <rect x="22" y="4" width="8" height="68" fill="{Q["brown"]}"/><rect x="66" y="4" width="8" height="68" fill="{Q["brown2"]}"/><rect x="22" y="44" width="8" height="5" fill="{GOLD[1]}"/><rect x="66" y="44" width="8" height="5" fill="{GOLD[2]}"/>
      <rect x="42" y="30" width="12" height="14" rx="2" fill="{GOLD[1]}"/><circle cx="48" cy="36" r="2" fill="{DARK}"/>
      <rect x="2" y="24" width="8" height="10" fill="{GOLD[1]}"/><rect x="86" y="24" width="8" height="10" fill="{GOLD[2]}"/><rect x="2" y="62" width="8" height="10" fill="{GOLD[1]}"/><rect x="86" y="62" width="8" height="10" fill="{GOLD[2]}"/>
      <circle cx="12" cy="50" r="7" fill="{Q["mustard"]}"/><circle cx="12" cy="50" r="4" fill="none" stroke="{CRIM[0]}" stroke-width="1.6"/><rect x="34" y="52" width="16" height="10" rx="2" fill="{ROSE[0]}" transform="rotate(-8 42 57)"/><rect x="78" y="34" width="10" height="14" rx="2" fill="{Q["cream"]}" transform="rotate(6 83 41)"/>
      <path d="M40 2 Q48 -8 56 2" stroke="{WOOD[2]}" stroke-width="3" fill="none"/></g>'''

# ---------- SITTING ROOM (tea and games)
SAGE=('#a9c4b0','#8fae98','#6f8f7a')
ANIMALS=json.load(open('./animals.json',encoding='utf-8'))
def head(name,x,y,s): return f'<g transform="translate({x} {y}) scale({s})">{ANIMALS[name]}</g>'   # a 100x100 animal face
def sitting_window(x,y):
    return f'''<g transform="translate({x} {y})"><rect x="-6" y="-6" width="112" height="116" rx="50" fill="{Q["cream"]}"/><rect x="0" y="0" width="100" height="104" rx="46" fill="#a9cbe0"/>
      <path d="M50 0 A46 46 0 0 1 100 46 L100 104 L70 104 L70 4 Z" fill="#8fb6d0"/><path d="M0 80 Q20 64 40 74 Q60 58 100 72 L100 104 L0 104 Z" fill="{Q["olive"]}" opacity=".85"/><circle cx="26" cy="66" r="10" fill="{Q["green"]}"/><circle cx="80" cy="60" r="8" fill="{Q["green"]}"/>
      <rect x="31" y="0" width="3" height="104" fill="{Q["cream"]}"/><rect x="66" y="0" width="3" height="104" fill="{Q["cream"]}"/><rect x="0" y="48" width="100" height="3" fill="{Q["cream"]}"/>
      <path d="M-12 -8 L8 -8 Q14 50 4 112 L-12 112 Z" fill="{SAGE[1]}"/><path d="M112 -8 L92 -8 Q86 50 96 112 L112 112 Z" fill="{SAGE[2]}"/><rect x="-14" y="-12" width="128" height="6" rx="3" fill="{GOLD[1]}"/>
      <path d="M-14 104 L114 104 L114 128 L-14 128 Z" fill="{WOOD[1]}"/><path d="M60 104 L114 104 L114 128 L60 128 Z" fill="{WOOD[2]}"/>{two(-12,92,124,14,ROSE[0],ROSE[1],6)}
      {pillow(-6,80,Q["mustard"],Q["mustard2"],26)}{pillow(82,80,SAGE[0],SAGE[2],26)}</g>'''
def plate_shelf(x,y):
    def plate(px,py,c): return f'<circle cx="{px}" cy="{py}" r="11" fill="#f1ede4"/><circle cx="{px}" cy="{py}" r="7.5" fill="none" stroke="{c}" stroke-width="2.4"/><circle cx="{px}" cy="{py}" r="3" fill="{c}"/>'
    teapot=f'<path d="M0 14 Q0 0 12 0 Q24 0 24 14 Z" fill="#f1ede4"/><path d="M12 0 Q24 0 24 14 L12 14 Z" fill="#d8d2c4"/><path d="M24 6 Q31 4 31 -2" stroke="#d8d2c4" stroke-width="2.4" fill="none"/><path d="M0 4 q-5 1 -4 7" stroke="#d8d2c4" stroke-width="2.4" fill="none"/><circle cx="12" cy="-1" r="2" fill="{SAGE[2]}"/><path d="M4 8 q8 -4 16 0" stroke="{SAGE[2]}" stroke-width="2" fill="none"/>'
    cup=lambda cx,cy:f'<path d="M{cx} {cy} L{cx+10} {cy} L{cx+8} {cy+8} L{cx+2} {cy+8} Z" fill="#f1ede4"/><path d="M{cx+10} {cy+2} q3 0 2 4" stroke="#d8d2c4" stroke-width="1.6" fill="none"/><rect x="{cx-2}" y="{cy+8}" width="14" height="2" rx="1" fill="#d8d2c4"/>'
    return f'''<g transform="translate({x} {y})">{two(0,0,112,8,WOOD[1],WOOD[2],2)}{two(0,52,112,8,WOOD[1],WOOD[2],2)}<path d="M6 8 L14 18 M106 8 L98 18 M6 60 L14 70 M106 60 L98 70" stroke="{WOOD[2]}" stroke-width="3"/>
      {plate(18,-11,SAGE[2])}{plate(44,-11,ROSE[1])}{plate(70,-11,Q["navy"])}{plate(96,-11,SAGE[2])}
      <g transform="translate(12 38)">{teapot}</g>{cup(48,44)}{cup(66,44)}{cup(84,44)}</g>'''
def sitting_head():
    w=f'<rect x="0" y="0" width="390" height="214" fill="{SAGE[1]}"/>'
    w+=''.join(f'<path d="M{x} {y-14} L{x+14} {y} L{x} {y+14} L{x-14} {y} Z" fill="none" stroke="{SAGE[0]}" stroke-width="1.6"/><circle cx="{x}" cy="{y}" r="2" fill="{Q["cream"]}" opacity=".7"/>' for x in range(0,404,28) for y in range(14,146,28))
    w+=f'<rect x="0" y="146" width="390" height="68" fill="{Q["cream"]}"/>'+''.join(f'<rect x="{x+5}" y="154" width="38" height="52" rx="3" fill="none" stroke="{SAGE[1]}" stroke-width="2"/>' for x in range(0,390,48))+f'<rect x="0" y="142" width="390" height="8" fill="{GOLD[1]}"/><rect x="0" y="146" width="390" height="4" fill="{GOLD[2]}"/>'
    w+=sitting_window(22,26)
    w+=plate_shelf(262,58)+sconce_r(318,30)
    w+=f'<rect x="146" y="100" width="98" height="114" fill="{SAGE[2]}"/><path d="M146 100 Q195 78 244 100 Z" fill="{GOLD[1]}"/><rect x="146" y="98" width="98" height="6" fill="{GOLD[2]}"/>'+gate_arch(164,62,(SAGE[2],'#4f6f5c'))+f'<circle cx="216" cy="172" r="3.4" fill="{GOLD[0]}"/>'
    w+=f'''<g transform="translate(195 46)"><ellipse cx="0" cy="0" rx="34" ry="26" fill="{GOLD[1]}"/><ellipse cx="0" cy="0" rx="28" ry="20" fill="#cfe3ea"/><path d="M-28 6 Q-12 -6 0 4 Q12 -8 28 2 L28 6 Q20 20 0 20 Q-20 20 -28 6 Z" fill="{Q["olive"]}"/>
      <path d="M-6 4 L4 -12 L14 4 Z" fill="{Q["cream"]}"/><path d="M4 -12 L14 4 L4 4 Z" fill="{Q["cream2"]}"/><circle cx="-14" cy="-8" r="5" fill="{Q["mustard"]}"/></g>'''
    return w
def sofa(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(66,74,66,7)}<path d="M8 40 Q6 8 34 10 Q50 0 66 8 Q82 0 98 10 Q126 8 124 40 Z" fill="{SAGE[0]}"/><path d="M66 8 Q82 0 98 10 Q126 8 124 40 L66 40 Z" fill="{SAGE[1]}"/>
      <path d="M8 38 Q6 8 34 10 Q50 0 66 8 Q82 0 98 10 Q126 8 124 38" stroke="{GOLD[1]}" stroke-width="3" fill="none"/>{"".join(f'<circle cx="{cx}" cy="26" r="1.8" fill="{SAGE[2]}"/>' for cx in (30,48,66,84,102))}
      {pillow(20,30,ROSE[0],ROSE[1],30)}{pillow(84,30,Q["mustard"],Q["mustard2"],30)}
      {two(12,40,108,18,SAGE[0],SAGE[1],6)}<path d="M66 40 L66 58" stroke="{SAGE[2]}" stroke-width="1.6"/>
      <path d="M0 34 Q0 26 8 26 Q16 26 16 34 L16 60 L0 60 Z" fill="{SAGE[0]}"/><path d="M116 34 Q116 26 124 26 Q132 26 132 34 L132 60 L116 60 Z" fill="{SAGE[1]}"/><circle cx="8" cy="32" r="4" fill="{SAGE[1]}"/><circle cx="124" cy="32" r="4" fill="{SAGE[2]}"/>
      <rect x="2" y="58" width="128" height="6" rx="2" fill="{GOLD[2]}"/><path d="M8 64 L6 72 M124 64 L126 72 M50 64 L50 70 M82 64 L82 70" stroke="{GOLD[2]}" stroke-width="4" stroke-linecap="round"/>{tassel(8,46)}{tassel(124,46)}</g>'''
def tea_table(x,y):
    cake=lambda cx,cy,c: f'<path d="M{cx-5} {cy} L{cx+5} {cy} L{cx+4} {cy-6} L{cx-4} {cy-6} Z" fill="{Q["tan"]}"/><path d="M{cx-4.5} {cy-6} Q{cx} {cy-11} {cx+4.5} {cy-6} Z" fill="{c}"/><circle cx="{cx}" cy="{cy-10}" r="1.6" fill="{CRIM[0]}"/>'
    tiers=''.join(f'<ellipse cx="40" cy="{yy}" rx="{rx}" ry="3" fill="#f1ede4"/><path d="M{40} {yy} m{-rx} 0 a{rx} 3 0 0 0 {2*rx} 0" fill="#d8d2c4"/>'+''.join(cake(40+dx,yy-1,c) for dx,c in cs) for yy,rx,cs in ((44,26,((-16,ROSE[0]),(0,"#f6f1e6"),(16,Q["mustard"]))),(28,19,((-9,"#f6f1e6"),(9,ROSE[0]))),(12,12,((0,ROSE[1]),))))
    return f'''<g transform="translate({x} {y})">{shadow(40,90,34,5)}<rect x="37" y="54" width="6" height="30" fill="{WOOD[1]}"/><path d="M22 90 Q40 76 58 90" stroke="{WOOD[2]}" stroke-width="5" fill="none" stroke-linecap="round"/>
      <ellipse cx="40" cy="52" rx="40" ry="8" fill="{WOOD[1]}"/><path d="M40 44 A40 8 0 0 1 80 52 A40 8 0 0 1 40 60 Z" fill="{WOOD[2]}"/><ellipse cx="40" cy="50" rx="36" ry="6" fill="#f6f1e6"/><path d="M4 52 q4 4 8 0 t8 0 t8 0 t8 0 t8 0 t8 0 t8 0 t8 0 t8 0" stroke="#f6f1e6" stroke-width="2.4" fill="none"/>
      <rect x="39" y="4" width="2" height="42" fill="{GOLD[2]}"/><circle cx="40" cy="3" r="3" fill="{GOLD[1]}"/>{tiers}
      <g transform="translate(64 34)"><path d="M0 12 Q0 0 8 0 Q16 0 16 12 Z" fill="#f1ede4"/><path d="M8 0 Q16 0 16 12 L8 12 Z" fill="#d8d2c4"/><path d="M0 4 q-6 0 -6 -6" stroke="#d8d2c4" stroke-width="2" fill="none"/><circle cx="8" cy="-1" r="1.6" fill="{SAGE[2]}"/></g>
      <g transform="translate(2 42)"><path d="M0 0 L10 0 L8 7 L2 7 Z" fill="#f1ede4"/><path d="M10 2 q3 0 2 4" stroke="#d8d2c4" stroke-width="1.6" fill="none"/></g></g>'''
def chess_table(x,y):
    sq=''
    for r in range(4):
        y0=12+r*5; y1=y0+5; xl0=10-r*3; xr0=90+r*3; xl1=xl0-3; xr1=xr0+3
        for c in range(8):
            a0=xl0+(xr0-xl0)*c/8; b0=xl0+(xr0-xl0)*(c+1)/8; a1=xl1+(xr1-xl1)*c/8; b1=xl1+(xr1-xl1)*(c+1)/8
            sq+=f'<path d="M{a0:.1f} {y0} L{b0:.1f} {y0} L{b1:.1f} {y1} L{a1:.1f} {y1} Z" fill="{"#f1e3c2" if (r+c)%2 else WOOD[2]}"/>'
    def piece(px,py,kind,c,c2):
        base=f'<path d="M-9 0 L9 0 L7 -5 L-7 -5 Z" fill="{c}"/><path d="M0 -5 L7 -5 L9 0 L0 0 Z" fill="{c2}"/>'
        if kind=='pawn': top=f'<path d="M-4 -5 L4 -5 L3 -16 L-3 -16 Z" fill="{c}"/><path d="M0 -5 L4 -5 L3 -16 L0 -16 Z" fill="{c2}"/><rect x="-6" y="-18" width="12" height="3" rx="1.5" fill="{c}"/><circle cx="0" cy="-23" r="6" fill="{c}"/><path d="M0 -29 A6 6 0 0 1 0 -17 Z" fill="{c2}"/>'
        elif kind=='king': top=f'<path d="M-5 -5 L5 -5 L3 -26 L-3 -26 Z" fill="{c}"/><path d="M0 -5 L5 -5 L3 -26 L0 -26 Z" fill="{c2}"/><rect x="-7" y="-28" width="14" height="3" rx="1.5" fill="{c}"/><path d="M-6 -28 Q-8 -36 0 -37 Q8 -36 6 -28 Z" fill="{c}"/><path d="M0 -37 Q8 -36 6 -28 L0 -28 Z" fill="{c2}"/><rect x="-1.2" y="-46" width="2.4" height="10" fill="{c}"/><rect x="-4" y="-43" width="8" height="2.4" fill="{c}"/>'
        else: top=f'<path d="M-5 -5 L5 -5 L3 -24 L-3 -24 Z" fill="{c}"/><path d="M0 -5 L5 -5 L3 -24 L0 -24 Z" fill="{c2}"/><rect x="-7" y="-26" width="14" height="3" rx="1.5" fill="{c}"/><path d="M-7 -26 L-8 -35 L-4 -31 L0 -37 L4 -31 L8 -35 L7 -26 Z" fill="{c}"/><path d="M0 -37 L4 -31 L8 -35 L7 -26 L0 -26 Z" fill="{c2}"/><circle cx="0" cy="-39" r="2.4" fill="{c}"/>'
        return f'<g transform="translate({px} {py})">{base}{top}</g>'
    return f'''<g transform="translate({x} {y})">{shadow(50,82,46,5)}<rect x="10" y="38" width="6" height="44" fill="{WOOD[1]}"/><rect x="84" y="38" width="6" height="44" fill="{WOOD[2]}"/><rect x="14" y="66" width="72" height="4" fill="{WOOD[2]}"/>
      <path d="M6 10 L94 10 L102 34 L-2 34 Z" fill="{WOOD[1]}"/>{sq}<path d="M-2 34 L102 34 L102 40 L-2 40 Z" fill="{WOOD[1]}"/><path d="M60 34 L102 34 L102 40 L60 40 Z" fill="{WOOD[2]}"/>
      {piece(22,22,"pawn","#f1e3c2",Q["cream2"])}{piece(40,16,"queen","#f1e3c2",Q["cream2"])}{piece(62,18,"king",Q["ink"],"#1a100a")}{piece(80,26,"pawn",Q["ink"],"#1a100a")}</g>'''
def rocking_chair(x,y):
    yarn=lambda cx,cy,c,c2: f'<circle cx="{cx}" cy="{cy}" r="7" fill="{c}"/><path d="M{cx-5} {cy-3} q5 3 10 0 M{cx-6} {cy+2} q6 3 12 0" stroke="{c2}" stroke-width="1.4" fill="none"/>'
    return f'''<g transform="translate({x} {y})">{shadow(40,94,42,5)}<path d="M2 88 Q36 100 70 84" stroke="{WOOD[2]}" stroke-width="5" fill="none" stroke-linecap="round"/>
      <path d="M12 56 L10 88 M56 56 L58 86" stroke="{WOOD[2]}" stroke-width="4"/><path d="M14 4 L20 0 L46 0 L52 4 L50 56 L16 56 Z" fill="{WOOD[1]}"/><path d="M33 0 L46 0 L52 4 L50 56 L33 56 Z" fill="{WOOD[2]}"/>
      {"".join(f'<rect x="{x0}" y="8" width="4" height="40" rx="1" fill="{WOOD[0]}" opacity=".6"/>' for x0 in (22,30,38,44))}
      <path d="M18 14 L48 14 L46 50 L20 54 Z" fill="{ROSE[0]}"/><path d="M33 14 L48 14 L46 50 L33 52 Z" fill="{ROSE[1]}"/><path d="M18 22 L48 22 M19 32 L47 32 M19 42 L47 42" stroke="#fff" stroke-width="1.4" opacity=".6"/>
      {two(6,52,56,8,WOOD[1],WOOD[2],3)}<rect x="2" y="36" width="10" height="4" rx="2" fill="{WOOD[1]}"/><rect x="56" y="36" width="10" height="4" rx="2" fill="{WOOD[2]}"/><path d="M6 40 L8 54 M62 40 L60 54" stroke="{WOOD[2]}" stroke-width="3"/>
      <g transform="translate(58 66)"><path d="M0 8 L26 8 L23 28 L3 28 Z" fill="{Q["tan"]}"/><path d="M13 8 L26 8 L23 28 L13 28 Z" fill="{Q["tan2"]}"/><path d="M1 14 L25 14 M2 20 L24 20" stroke="{Q["brown"]}" stroke-width="1.4"/>
        {yarn(8,6,CRIM[0],CRIM[1])}{yarn(19,4,SAGE[0],SAGE[2])}<path d="M12 4 L26 -10 M16 4 L30 -8" stroke="{GOLD[2]}" stroke-width="1.8" stroke-linecap="round"/><circle cx="26" cy="-10" r="1.6" fill="{GOLD[1]}"/><circle cx="30" cy="-8" r="1.6" fill="{GOLD[1]}"/></g></g>'''
def fish_tank(x,y):
    fish=lambda fx,fy,c,d=1: f'<g transform="translate({fx} {fy}) scale({d} 1)"><ellipse cx="0" cy="0" rx="7" ry="4.4" fill="{c}"/><path d="M6 0 L12 -5 L12 5 Z" fill="{c}"/><circle cx="-3.5" cy="-1" r="1.2" fill="{DARK}"/></g>'
    return f'''<g transform="translate({x} {y})">{shadow(42,100,42,5)}<rect x="6" y="64" width="6" height="36" fill="{WOOD[1]}"/><rect x="72" y="64" width="6" height="36" fill="{WOOD[2]}"/><rect x="10" y="86" width="64" height="4" fill="{WOOD[2]}"/>
      {two(0,58,84,8,WOOD[1],WOOD[2],2)}<rect x="2" y="4" width="80" height="54" rx="3" fill="{GOLD[2]}"/><rect x="5" y="6" width="74" height="50" fill="#bfe0ea"/><rect x="5" y="14" width="74" height="42" fill="#7fb8cc"/><rect x="50" y="14" width="29" height="42" fill="#6aa6bc"/>
      <path d="M5 56 Q20 48 40 54 Q60 48 79 56 Z" fill="{Q["tan"]}"/><path d="M16 54 Q12 40 18 30 Q20 42 22 54 Z M62 54 Q66 36 60 24 Q58 40 58 54 Z" fill="{Q["green"]}"/><path d="M24 54 Q26 44 22 38" stroke="{Q["olive"]}" stroke-width="3" fill="none"/>
      {fish(34,28,Q["orange"])}{fish(56,40,Q["mustard"],-1)}{fish(28,44,Q["coral"])}{"".join(f'<circle cx="{bx}" cy="{by}" r="{br}" fill="none" stroke="#fff" stroke-width="1.2"/>' for bx,by,br in ((24,22,2),(26,16,1.4),(48,30,1.6),(50,22,2)))}
      <rect x="0" y="0" width="84" height="6" rx="2" fill="{WOOD[1]}"/><rect x="52" y="0" width="32" height="6" rx="2" fill="{WOOD[2]}"/><path d="M8 12 L8 50" stroke="#fff" stroke-width="2.4" opacity=".6"/></g>'''
def curio_cabinet(x,y):
    plate=lambda px,py,c: f'<circle cx="{px}" cy="{py}" r="8" fill="#f1ede4"/><circle cx="{px}" cy="{py}" r="5" fill="none" stroke="{c}" stroke-width="2"/>'
    return f'''<g transform="translate({x} {y})">{shadow(32,124,34,5)}<path d="M4 12 Q32 -6 60 12 Z" fill="{WOOD[1]}"/><path d="M32 3 Q46 4 60 12 L32 12 Z" fill="{WOOD[2]}"/>{two(2,10,60,108,WOOD[1],WOOD[2],3)}<rect x="8" y="16" width="48" height="96" fill="#d8ecf0"/><rect x="34" y="16" width="22" height="96" fill="#c4e0e6"/>
      {"".join(f'<rect x="8" y="{yy}" width="48" height="3" fill="{WOOD[1]}"/>' for yy in (44,76))}
      {plate(20,34,SAGE[2])}{plate(42,34,ROSE[1])}<path d="M14 72 Q12 60 18 56 L26 56 Q32 60 30 72 Z" fill="{Q["navy"]}"/><path d="M22 56 L26 56 Q32 60 30 72 L22 72 Z" fill="{Q["navy2"]}"/><rect x="16" y="52" width="12" height="4" rx="1" fill="{Q["navy"]}"/>
      <path d="M36 70 L52 70 Q54 64 50 58 L38 58 Q34 64 36 70 Z" fill="#f1ede4" opacity=".9"/><path d="M40 68 L44 60 L48 68 Z" fill="#fff"/><path d="M38 68 L50 68" stroke="{WOOD[2]}" stroke-width="2"/><rect x="42" y="54" width="4" height="4" fill="{WOOD[2]}"/>
      <path d="M14 108 L14 96 L24 96 L24 108 Z" fill="{GOLD[1]}"/><path d="M12 96 Q19 88 26 96 Z" fill="{GOLD[1]}"/><circle cx="44" cy="100" r="8" fill="#f1ede4"/><path d="M40 100 q4 -4 8 0" stroke="{CRIM[0]}" stroke-width="2" fill="none"/>
      <rect x="31" y="16" width="2" height="96" fill="{WOOD[1]}"/><path d="M12 22 L12 104" stroke="#fff" stroke-width="2" opacity=".6"/><circle cx="28" cy="66" r="1.8" fill="{GOLD[1]}"/><circle cx="36" cy="66" r="1.8" fill="{GOLD[1]}"/>
      <rect x="0" y="116" width="64" height="6" rx="2" fill="{WOOD[2]}"/><path d="M6 122 L4 128 M58 122 L60 128" stroke="{WOOD[2]}" stroke-width="4" stroke-linecap="round"/></g>'''
def fern_stand(x,y):
    leaf=lambda a,l: f'<path d="M24 34 Q{24+l*0.5*math.cos(math.radians(a))-4:.1f} {34-l*0.8*math.sin(math.radians(a)):.1f} {24+l*math.cos(math.radians(a)):.1f} {34-l*math.sin(math.radians(a)):.1f}" stroke="{Q["green"]}" stroke-width="7" fill="none" stroke-linecap="round"/>'
    return f'''<g transform="translate({x} {y})">{shadow(24,82,16,4)}{"".join(leaf(a,l) for a,l in ((160,24),(130,28),(100,30),(75,30),(50,28),(20,24)))}
      <path d="M10 32 L38 32 L34 50 L14 50 Z" fill="{Q["cream"]}"/><path d="M24 32 L38 32 L34 50 L24 50 Z" fill="{Q["cream2"]}"/><rect x="8" y="30" width="32" height="5" rx="2" fill="{SAGE[2]}"/>
      <path d="M16 50 L12 80 M32 50 L36 80 M24 50 L24 80" stroke="{WOOD[2]}" stroke-width="3" stroke-linecap="round"/><path d="M14 66 L34 66" stroke="{WOOD[2]}" stroke-width="2"/></g>'''
def lamp_table(x,y):
    return f'''<g transform="translate({x} {y})"><circle cx="20" cy="10" r="20" fill="{Q["mustard"]}" opacity=".14"/>{shadow(20,66,18,4)}<path d="M8 34 L6 66 M32 34 L34 66" stroke="{WOOD[2]}" stroke-width="3" stroke-linecap="round"/><path d="M8 54 L32 54" stroke="{WOOD[2]}" stroke-width="2"/>
      <ellipse cx="20" cy="34" rx="18" ry="4" fill="{WOOD[1]}"/><path d="M20 30 A18 4 0 0 1 38 34 A18 4 0 0 1 20 38 Z" fill="{WOOD[2]}"/>
      <path d="M14 30 Q12 22 20 20 Q28 22 26 30 Z" fill="{SAGE[1]}"/><rect x="18" y="8" width="4" height="12" fill="{GOLD[1]}"/><path d="M8 10 L32 10 L26 -4 L14 -4 Z" fill="{ROSE[0]}"/><path d="M20 -4 L26 -4 L32 10 L20 10 Z" fill="{ROSE[1]}"/><path d="M8 10 q3 3 6 0 t6 0 t6 0 t6 0" stroke="{GOLD[1]}" stroke-width="1.6" fill="none"/></g>'''

# ---------- TOWER STAIRS (hoist and portraits)
STONE=('#8a8392','#746d7c','#5e5866')
def tower_head():
    w=f'<rect x="0" y="0" width="390" height="214" fill="{STONE[1]}"/>'
    w+=''.join(''.join(f'<rect x="{(r%2)*24+k*48-22}" y="{6+r*24}" width="44" height="20" rx="3" fill="{STONE[0] if (r*3+k)%4 else "#7e7787"}" opacity=".7"/>' for k in range(10)) for r in range(9))
    for sx in (40,350):
        w+=f'<g transform="translate({sx} 30)"><rect x="-16" y="-6" width="32" height="96" rx="16" fill="{STONE[2]}"/><rect x="-6" y="4" width="12" height="80" rx="6" fill="#cfe3ea"/><rect x="-6" y="40" width="12" height="44" fill="#a9cbe0"/></g>'
    for bx,c,c2 in ((84,CRIM[0],CRIM[1]),(306,Q["navy"],Q["navy2"])):
        w+=f'''<g transform="translate({bx} 14)"><rect x="-26" y="0" width="52" height="5" rx="2" fill="{GOLD[1]}"/><circle cx="-26" cy="2.5" r="4" fill="{GOLD[0]}"/><circle cx="26" cy="2.5" r="4" fill="{GOLD[1]}"/>
          <path d="M-20 4 L20 4 L20 112 L0 98 L-20 112 Z" fill="{c}"/><path d="M4 4 L20 4 L20 112 L4 100 Z" fill="{c2}"/><path d="M-20 12 L20 12 M-20 92 L0 80 L20 92" stroke="{GOLD[1]}" stroke-width="2.4" fill="none"/>{crown(-12,38,0.75)}</g>'''
    w+=sconce_r(126,92)+sconce_r(264,92)
    # the last few steps up to the door
    w+=f'<rect x="146" y="100" width="98" height="114" fill="{STONE[2]}"/><path d="M146 100 Q195 76 244 100 Z" fill="{STONE[0]}"/>'+gate_arch(164,62,(WOOD[2],'#5a3a24'))+f'<circle cx="216" cy="172" r="3.4" fill="{GOLD[0]}"/>'
    w+=f'<g transform="translate(195 46)"><circle cx="0" cy="0" r="26" fill="{STONE[0]}"/><circle cx="0" cy="0" r="20" fill="#a9cbe0"/>'+''.join(f'<path d="M0 0 L{20*math.cos(math.radians(a)):.1f} {20*math.sin(math.radians(a)):.1f}" stroke="{STONE[0]}" stroke-width="2.4"/>' for a in range(0,360,45))+f'<circle cx="0" cy="0" r="6" fill="{CRIM[0]}"/><circle cx="0" cy="0" r="6" fill="none" stroke="{STONE[0]}" stroke-width="2"/></g>'
    w+=f'<rect x="0" y="196" width="390" height="18" fill="{STONE[2]}"/>'+''.join(f'<rect x="{x}" y="198" width="46" height="14" rx="2" fill="{STONE[1]}"/>' for x in range(2,390,48))
    return w
def hoist(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(40,132,42,6)}<rect x="8" y="10" width="8" height="122" fill="{WOOD[1]}"/><rect x="64" y="10" width="8" height="122" fill="{WOOD[2]}"/>{two(2,6,76,9,WOOD[1],WOOD[2],2)}<path d="M16 24 L30 12 M64 24 L50 12" stroke="{WOOD[2]}" stroke-width="4"/>
      <circle cx="40" cy="22" r="11" fill="{IRON[1]}"/><circle cx="40" cy="22" r="7" fill="{IRON[0]}"/><circle cx="40" cy="22" r="2.4" fill="{IRON[2]}"/><rect x="38" y="10" width="4" height="8" fill="{IRON[2]}"/>
      <path d="M29 22 L29 128 M51 22 L51 70" stroke="{Q["tan"]}" stroke-width="2.6"/><path d="M29 114 Q20 118 22 124 Q28 128 32 122" stroke="{Q["tan"]}" stroke-width="2.6" fill="none"/>{"".join(f'<path d="M29 {yy} l2 3" stroke="{Q["tan2"]}" stroke-width="1"/>' for yy in range(30,110,8))}
      <path d="M51 70 L40 78 M51 70 L62 78" stroke="{Q["tan"]}" stroke-width="2"/><path d="M36 78 L66 78 L62 102 L40 102 Z" fill="{Q["tan"]}"/><path d="M51 78 L66 78 L62 102 L51 102 Z" fill="{Q["tan2"]}"/>
      <path d="M37 84 L65 84 M38 90 L64 90 M39 96 L63 96" stroke="{Q["brown"]}" stroke-width="1.4"/><rect x="40" y="72" width="22" height="7" rx="3" fill="{WOOD[2]}" transform="rotate(-10 51 75)"/><rect x="42" y="70" width="20" height="7" rx="3" fill="{WOOD[1]}" transform="rotate(14 52 73)"/>
      <path d="M0 132 L24 132 M56 132 L80 132" stroke="{WOOD[2]}" stroke-width="5" stroke-linecap="round"/></g>'''
def portrait(x,y,animal,bg,bg2,frame='rect'):
    if frame=='oval': fr=f'<ellipse cx="30" cy="34" rx="30" ry="36" fill="{GOLD[1]}"/><ellipse cx="30" cy="34" rx="24" ry="30" fill="{bg}"/><path d="M30 4 A24 30 0 0 1 30 64 Z" fill="{bg2}"/>'
    elif frame=='arch': fr=f'<path d="M0 70 L0 26 Q0 -4 30 -4 Q60 -4 60 26 L60 70 Z" fill="{GOLD[1]}"/><path d="M6 64 L6 26 Q6 2 30 2 Q54 2 54 26 L54 64 Z" fill="{bg}"/><path d="M30 2 Q54 2 54 26 L54 64 L30 64 Z" fill="{bg2}"/>'
    else: fr=f'<rect x="0" y="-2" width="60" height="72" rx="3" fill="{GOLD[1]}"/><rect x="6" y="4" width="48" height="60" fill="{bg}"/><rect x="30" y="4" width="24" height="60" fill="{bg2}"/>'
    return f'''<g transform="translate({x} {y})">{shadow(30,118,24,5)}<path d="M30 60 L30 116 M14 116 L24 70 M46 116 L36 70" stroke="{WOOD[2]}" stroke-width="4" stroke-linecap="round"/><rect x="4" y="68" width="52" height="5" rx="2" fill="{WOOD[1]}"/>
      {fr}<path d="M10 64 Q30 46 50 64 Z" fill="{CRIM[0]}"/>{ermine(13,56,34,7)}{head(animal,13,24,0.34)}{crown(20,10,0.62)}<path d="M0 0" /></g>'''
def banner_stand(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(22,132,18,4)}<rect x="19" y="4" width="5" height="128" rx="2" fill="{WOOD[2]}"/><path d="M8 132 L22 124 L36 132" stroke="{WOOD[2]}" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M21.5 -6 L25 2 L18 2 Z" fill="{GOLD[1]}"/>
      <rect x="4" y="8" width="36" height="4" rx="2" fill="{GOLD[1]}"/><path d="M6 12 L38 12 L38 78 L22 66 L6 78 Z" fill="{Q["green"]}"/><path d="M22 12 L38 12 L38 78 L22 66 Z" fill="{Q["green2"]}"/>
      <path d="M6 18 L38 18 M6 64 L22 54 L38 64" stroke="{GOLD[1]}" stroke-width="2" fill="none"/><path d="M22 26 L30 36 L22 46 L14 36 Z" fill="{GOLD[1]}"/><circle cx="22" cy="36" r="3" fill="{CRIM[0]}"/></g>'''
def landing_bench(x,y):   # a high-backed wooden settle with a long cushion, for a rest on the way up
    return f'''<g transform="translate({x} {y})">{shadow(52,74,52,5)}{two(6,0,92,44,WOOD[1],WOOD[2],3)}<path d="M6 4 Q52 -10 98 4 L98 8 L6 8 Z" fill="{WOOD[1]}"/>
      {"".join(f'<path d="M{px} 40 L{px} 20 Q{px} 10 {px+12} 10 Q{px+24} 10 {px+24} 20 L{px+24} 40 Z" fill="{WOOD[2]}" opacity=".55"/>' for px in (14,40,66))}
      {two(0,44,104,10,WOOD[1],WOOD[2],3)}{two(4,36,96,10,CRIM[0],CRIM[1],5)}{"".join(f'<circle cx="{cx}" cy="41" r="1.8" fill="{GOLD[0]}"/>' for cx in (20,40,60,80))}{pillow(10,26,Q["mustard"],Q["mustard2"],26)}{pillow(68,26,Q["navy"],Q["navy2"],26)}
      <rect x="-2" y="30" width="10" height="26" rx="3" fill="{WOOD[1]}"/><rect x="96" y="30" width="10" height="26" rx="3" fill="{WOOD[2]}"/>
      <rect x="2" y="54" width="100" height="12" fill="{WOOD[2]}"/><path d="M6 66 L6 74 M98 66 L98 74" stroke="{WOOD[2]}" stroke-width="5" stroke-linecap="round"/>{"".join(f'<rect x="{px}" y="57" width="18" height="6" rx="2" fill="{WOOD[1]}" opacity=".7"/>' for px in (14,44,72))}</g>'''
def lantern(x,y,s=1):
    return f'''<g transform="translate({x} {y}) scale({s})"><circle cx="20" cy="26" r="20" fill="{Q["mustard"]}" opacity=".18"/><path d="M14 4 Q20 -4 26 4" stroke="{IRON[2]}" stroke-width="2.4" fill="none"/>
      <path d="M8 12 L20 4 L32 12 Z" fill="{IRON[1]}"/><path d="M20 4 L32 12 L20 12 Z" fill="{IRON[2]}"/><rect x="8" y="12" width="24" height="3" fill="{IRON[2]}"/>
      <path d="M10 15 L30 15 L28 38 L12 38 Z" fill="#f6dc8c"/><path d="M20 15 L30 15 L28 38 L20 38 Z" fill="#ecc463"/><rect x="18" y="26" width="4" height="10" rx="1" fill="{Q["cream"]}"/><path d="M20 18 C17 22 18 26 20 26 C22 26 23 22 20 18 Z" fill="{Q["orange"]}"/>
      <path d="M10 15 L12 38 M30 15 L28 38 M20 15 L20 20" stroke="{IRON[2]}" stroke-width="2"/><rect x="9" y="38" width="22" height="4" rx="1" fill="{IRON[1]}"/><rect x="14" y="42" width="12" height="3" fill="{IRON[2]}"/></g>'''
def lantern_post(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(20,134,14,4)}<rect x="17" y="40" width="6" height="94" rx="2" fill="{IRON[1]}"/><rect x="20" y="40" width="3" height="94" fill="{IRON[2]}"/><path d="M8 134 L20 126 L32 134" stroke="{IRON[2]}" stroke-width="4" fill="none" stroke-linecap="round"/>
      <path d="M12 60 Q20 54 28 60" stroke="{IRON[1]}" stroke-width="2.4" fill="none"/>{lantern(0,-4,1)}</g>'''
def statue_niche(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(36,130,38,5)}<path d="M0 130 L0 28 Q0 -2 36 -2 Q72 -2 72 28 L72 130 Z" fill="{STONE[0]}"/><path d="M36 -2 Q72 -2 72 28 L72 130 L36 130 Z" fill="{STONE[1]}"/><path d="M10 118 L10 32 Q10 8 36 8 Q62 8 62 32 L62 118 Z" fill="#4a4452"/>
      <rect x="18" y="104" width="36" height="14" fill="#b9b3be"/><rect x="36" y="104" width="18" height="14" fill="#a39cab"/>
      <path d="M26 104 L28 70 L44 70 L46 104 Z" fill="#c9c3cd"/><path d="M36 70 L44 70 L46 104 L36 104 Z" fill="#b2acb6"/><path d="M24 44 Q36 34 48 44 L46 72 L26 72 Z" fill="#c9c3cd"/><path d="M36 38 Q44 40 48 44 L46 72 L36 72 Z" fill="#b2acb6"/>
      <path d="M26 30 Q26 16 36 16 Q46 16 46 30 L46 40 L26 40 Z" fill="#c9c3cd"/><path d="M36 16 Q46 16 46 30 L46 40 L36 40 Z" fill="#b2acb6"/><rect x="28" y="28" width="16" height="3" fill="#6e6876"/><path d="M36 16 Q40 6 46 6" stroke="#c9c3cd" stroke-width="4" fill="none" stroke-linecap="round"/>
      <path d="M16 48 L32 48 L32 64 Q24 72 16 64 Z" fill="#d6d0da"/><path d="M24 48 L32 48 L32 64 Q28 68 24 69 Z" fill="#c0bac4"/><path d="M24 52 L24 64 M19 57 L29 57" stroke="#9a94a0" stroke-width="2"/>
      <rect x="50" y="34" width="3" height="56" fill="#d6d0da"/><rect x="45" y="52" width="13" height="3" fill="#c0bac4"/>
      <rect x="-4" y="126" width="80" height="6" rx="2" fill="{STONE[2]}"/></g>'''
def ivy_pot(x,y):
    leaves=''.join(f'<path d="M{lx} {ly} q-5 -5 0 -9 q5 4 0 9 Z" fill="{Q["green"] if k%2 else "#4f8a4a"}" transform="rotate({(k*47)%80-40} {lx} {ly})"/>' for k,(lx,ly) in enumerate(((10,12),(20,6),(30,14),(38,4),(8,30),(28,32),(40,26),(14,48),(34,50),(22,64),(6,70),(40,72),(16,86),(32,90))))
    return f'''<g transform="translate({x} {y})">{shadow(24,124,20,5)}<path d="M4 100 L4 0 M24 100 L24 -6 M44 100 L44 0 M4 20 L44 60 M44 20 L4 60 M4 60 L44 100 M44 60 L4 100" stroke="{WOOD[1]}" stroke-width="3" stroke-linecap="round"/>
      <path d="M24 96 Q12 70 22 50 Q32 30 18 8" stroke="{Q["green2"]}" stroke-width="2" fill="none"/>{leaves}
      <path d="M2 94 L46 94 L40 124 L8 124 Z" fill="{Q["orange"]}"/><path d="M24 94 L46 94 L40 124 L24 124 Z" fill="{Q["orange2"]}"/><rect x="0" y="90" width="48" height="7" rx="2" fill="{Q["orange"]}"/><rect x="28" y="90" width="20" height="7" rx="2" fill="{Q["orange2"]}"/></g>'''
def tea_chest(x,y,s=1):   # the Sitting room's board wall
    return f'''<g transform="translate({x} {y}) scale({s})"><rect x="0" y="6" width="40" height="34" rx="2" fill="{WOOD[1]}"/><rect x="25" y="6" width="15" height="34" rx="2" fill="{WOOD[2]}"/>
      <rect x="-1" y="2" width="42" height="7" rx="2" fill="{WOOD[0]}"/><rect x="25" y="2" width="16" height="7" rx="2" fill="{WOOD[1]}"/>
      <path d="M0 2 L7 2 L7 6 L4 6 L4 12 L0 12 Z M41 2 L34 2 L34 6 L37 6 L37 12 L41 12 Z M0 40 L7 40 L7 36 L4 36 L4 30 L0 30 Z M41 40 L34 40 L34 36 L37 36 L37 30 L41 30 Z" fill="{GOLD[1]}"/>
      <rect x="9" y="15" width="22" height="16" rx="2" fill="{Q["cream"]}"/><rect x="9" y="15" width="22" height="16" rx="2" fill="none" stroke="{SAGE[2]}" stroke-width="1.4"/>
      <path d="M20 28 Q13 23 20 18 Q27 23 20 28 Z" fill="{SAGE[2]}"/><path d="M20 28 L20 18" stroke="{Q["cream"]}" stroke-width="1"/></g>'''
def stone_block(x,y,s=1):   # the Tower stairs' board wall: a rough block of the tower's stone
    return f'''<g transform="translate({x} {y}) scale({s})"><path d="M3 10 L10 3 L32 2 L39 8 L40 34 L34 40 L6 40 L1 33 Z" fill="{STONE[0]}"/><path d="M24 2 L32 2 L39 8 L40 34 L34 40 L24 40 Z" fill="{STONE[2]}"/>
      <path d="M3 10 L10 3 L32 2 L39 8 L30 11 L9 12 Z" fill="#a39cab"/><path d="M24 2 L32 2 L39 8 L30 11 L24 11.5 Z" fill="{STONE[0]}"/>
      <path d="M12 18 L16 24 L13 30 M30 20 L27 27" stroke="{STONE[2]}" stroke-width="1.6" fill="none" stroke-linecap="round"/><path d="M33 16 L36 22" stroke="#4a4452" stroke-width="1.6" stroke-linecap="round"/>
      <circle cx="9" cy="34" r="1.6" fill="{STONE[1]}"/><circle cx="20" cy="15" r="1.2" fill="{STONE[1]}"/></g>'''

H5['Royal chambers']=royal_head()+STEP
H5['Wardrobe']=wardrobe_head()+STEP
# props: [box(x,y,w,h) relative to the drawing's origin, svg]
add5('royal_bed',royal_bed(0,0),(0,-14,128,142),0.8); add5('fireplace',fireplace(0,0),(-4,-16,108,118)); add5('cradle',cradle(0,0),(0,0,76,72))
add5('royal_armchair',royal_armchair(0,0),(0,-16,60,108)); add5('dresser',dresser(0,0),(0,-10,84,96)); add5('orange_tree',orange_tree(0,0),(0,0,52,96))
add5('pet_bed',pet_bed(0,0),(0,4,64,40)); add5('writing_desk',writing_desk(0,0),(0,0,88,84))
add5('footstool_s',footstool_s(0,0),(0,0,40,34)); add5('tea_stand',tea_stand(0,0),(0,0,36,46)); add5('floor_vase',floor_vase(0,0),(0,0,28,46))
add5('gown_stand',gown_stand(0,0),(0,-4,64,118)); add5('robe_rail',robe_rail(0,0),(-4,0,132,104),0.78); add5('hat_stand',hat_stand(0,0),(0,-18,54,132))
add5('shoe_shelf',shoe_shelf(0,0),(0,0,86,90)); add5('cheval_mirror',cheval_mirror(0,0),(-4,0,68,112)); add5('open_closet',open_closet(0,0),(0,0,96,114))
add5('cobbler_bench',cobbler_bench(0,0),(0,0,92,68))
add5('folded_s',folded_s(0,0),(0,-6,32,46)); add5('hat_boxes',hat_boxes(0,0),(0,-4,72,104),0.9); add5('travel_trunk',travel_trunk(0,0),(0,-8,96,86),0.9)
H5['Sitting room']=sitting_head()+STEP
add5('sofa',sofa(0,0),(0,0,132,78)); add5('tea_table',tea_table(0,0),(0,0,80,96)); add5('chess_table',chess_table(0,0),(-4,-24,108,110))
add5('rocking_chair',rocking_chair(0,0),(0,-10,88,108)); add5('fish_tank',fish_tank(0,0),(0,0,84,104)); add5('curio_cabinet',curio_cabinet(0,0),(0,-4,64,132))
add5('fern_stand',fern_stand(0,0),(0,0,48,86)); add5('lamp_table',lamp_table(0,0),(0,-10,40,80))
H5['Tower stairs']=tower_head()+STEP
add5('hoist',hoist(0,0),(0,0,80,138)); add5('portrait_mouse',portrait(0,0,'mouse',CRIM[0],CRIM[1],'oval'),(0,-4,60,126)); add5('portrait_lion',portrait(0,0,'lion',Q["navy"],Q["navy2"]),(0,-2,60,124))
add5('portrait_elephant',portrait(0,0,'elephant',Q["green"],Q["green2"],'arch'),(0,-4,60,126)); add5('banner_stand',banner_stand(0,0),(0,-6,44,142))
add5('landing_bench',landing_bench(0,0),(-2,-6,108,82)); add5('lantern_post',lantern_post(0,0),(0,-8,40,146)); add5('statue_niche',statue_niche(0,0),(-4,-2,80,136),0.9); add5('ivy_pot',ivy_pot(0,0),(0,-8,48,136))
H5={k:re.sub(r'\s+',' ',v).strip() for k,v in H5.items()}
json.dump({'heads':H5,'props':P5},open('./royal_floor_art.json','w'),separators=(',',':'),ensure_ascii=False)
print({k:len(v) for k,v in H5.items()}, len(P5))
# Board walls (48x48) for the game's CSS: printed for index.html
FOOTSTOOL_TILE=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">{footstool(4,8,1)}</svg>'
CHEST_TILE=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">{tea_chest(3.5,3,1)}</svg>'
BLOCK_TILE=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">{stone_block(3.5,3,1)}</svg>'
open('./royal_tiles.json','w').write(json.dumps({k:re.sub(r'\s+',' ',v) for k,v in (('footstool',FOOTSTOOL_TILE),('teachest',CHEST_TILE),('stoneblock',BLOCK_TILE))}))
