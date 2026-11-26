import json, math, re
# ================= Royal floor: Royal chambers, Wardrobe (more rooms of this floor to follow)
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
def shoes_s(x,y): return f'<g transform="translate({x} {y})">{shadow(16,20,16,3)}{shoe(0,4,CRIM[0],CRIM[1])}{shoe(12,6,CRIM[0],CRIM[1])}</g>'
def folded_s(x,y): return f'<g transform="translate({x} {y})">{shadow(16,40,16,3)}<rect x="4" y="22" width="4" height="18" fill="{WOOD[2]}"/><rect x="24" y="22" width="4" height="18" fill="{WOOD[2]}"/>{two(0,18,32,6,WOOD[1],WOOD[2],2)}{folded(3,11,[PAIRS[1],PAIRS[3],PAIRS[0]])}</g>'
def parasol_stand(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(14,50,13,3)}<path d="M6 4 L10 30 M20 0 L16 30 M14 -6 L13 30" stroke="{WOOD[2]}" stroke-width="2"/>
      <path d="M2 4 Q6 -2 10 4 L8 22 Z" fill="{Q["pink"]}"/><path d="M16 0 Q22 -6 26 0 L18 20 Z" fill="{LILAC[0]}"/><path d="M10 -6 Q14 -12 18 -6 L14 16 Z" fill="#a9cbe0"/>
      <path d="M4 26 L24 26 L22 50 L6 50 Z" fill="{Q["navy"]}"/><path d="M14 26 L24 26 L22 50 L14 50 Z" fill="{Q["navy2"]}"/><rect x="3" y="24" width="22" height="4" rx="2" fill="{GOLD[1]}"/></g>'''

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
add5('shoes_s',shoes_s(0,0),(0,0,34,22)); add5('folded_s',folded_s(0,0),(0,-6,32,46)); add5('parasol_stand',parasol_stand(0,0),(0,-12,28,64))
H5={k:re.sub(r'\s+',' ',v).strip() for k,v in H5.items()}
json.dump({'heads':H5,'props':P5},open('./royal_floor_art.json','w'),separators=(',',':'),ensure_ascii=False)
print({k:len(v) for k,v in H5.items()}, len(P5))
# Board walls (48x48) for the game's CSS: printed for index.html
FOOTSTOOL_TILE=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">{footstool(4,8,1)}</svg>'
open('./royal_tiles.json','w').write(json.dumps({'footstool':re.sub(r'\s+',' ',FOOTSTOOL_TILE)}))
