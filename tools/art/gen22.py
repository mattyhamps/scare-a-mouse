import json, math, random, re
g21=open('./gen21.py').read()
exec(g21[:g21.index("\nrooms={")])
# ================= Third floor: Guard room, Toy room, Hall of mirrors, Bathhouse, Trophy room
HEADS={}; PROPS={}
def addp(name,svg,box): PROPS[name]=[list(box),re.sub(r'\s+',' ',svg).strip()]
def two(x,y,w,h,c,c2,r=3): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{c}"/><rect x="{x+w*0.62:.1f}" y="{y}" width="{w*0.38:.1f}" height="{h}" rx="{r}" fill="{c2}"/>'
def torch_w(x,y):
    return f'<g transform="translate({x} {y})"><circle cx="0" cy="-6" r="20" fill="{Q["mustard"]}" opacity=".16"/><rect x="-3" y="4" width="6" height="18" rx="2" fill="{WOOD[2]}"/><path d="M0 -14 C-7 -6 -5 4 0 4 C5 4 7 -6 0 -14 Z" fill="{Q["mustard"]}"/><path d="M0 -6 C-3 -2 -2 3 0 3 C2 3 3 -2 0 -6 Z" fill="{Q["coral"]}"/></g>'
# ---------- GUARD ROOM
def banner(x,y,c,c2,h=110):
    return f'<g transform="translate({x} {y})"><rect x="-4" y="0" width="44" height="5" rx="2" fill="{WOOD[2]}"/><path d="M0 4 L36 4 L36 {h} L18 {h-16} L0 {h} Z" fill="{c}"/><path d="M18 4 L36 4 L36 {h} L18 {h-16} Z" fill="{c2}"/><g transform="translate(8 34)"><path d="M0 0 L20 0 L20 12 Q20 24 10 28 Q0 24 0 12 Z" fill="{Q["mustard"]}"/><path d="M10 0 L20 0 L20 12 Q20 24 10 28 Z" fill="{Q["mustard2"]}"/><circle cx="10" cy="11" r="3.4" fill="{c2}"/><rect x="9" y="12" width="2" height="8" fill="{c2}"/></g></g>'
def key_board(x,y):
    keys=''.join(f'<g transform="translate({10+k*13} 14)"><rect x="-1" y="-4" width="2" height="6" fill="{DARK}"/><circle cx="0" cy="6" r="4" fill="none" stroke="{Q["mustard"]}" stroke-width="2.4"/><rect x="-1.2" y="10" width="2.4" height="{12+(k%2)*5}" fill="{Q["mustard"]}"/><rect x="0" y="{18+(k%2)*5}" width="5" height="2.4" fill="{Q["mustard"]}"/></g>' for k in range(5))
    return f'<g transform="translate({x} {y})">{two(0,0,72,52,WOOD[1],WOOD[2],4)}<rect x="4" y="4" width="64" height="44" rx="3" fill="{WOOD[0]}" opacity=".35"/>{keys}</g>'
def helmet(x,y,s=1,c="#a8a5b2",c2="#8a8794"):
    return f'<g transform="translate({x} {y}) scale({s})"><path d="M0 22 L0 12 Q0 0 14 0 Q28 0 28 12 L28 22 Z" fill="{c}"/><path d="M14 0 Q28 0 28 12 L28 22 L14 22 Z" fill="{c2}"/><rect x="4" y="12" width="20" height="3" rx="1" fill="#3a3644"/><rect x="12" y="15" width="4" height="7" fill="#3a3644"/><path d="M14 0 L14 -6" stroke="{Q["coral"]}" stroke-width="5" stroke-linecap="round"/></g>'
def guard_room_head():
    w=f'<rect x="0" y="0" width="390" height="214" fill="{Q["lav"]}"/>{stones(390,214,81)}'
    w+=key_board(22,74)+f'<rect x="270" y="96" width="102" height="6" rx="2" fill="{WOOD[2]}"/>'+''.join(helmet(276+k*34,72) for k in range(3))
    w+=f'<rect x="24" y="150" width="96" height="6" rx="2" fill="{WOOD[2]}"/>'+''.join(f'<g transform="translate({32+k*28} 132)"><rect x="0" y="0" width="16" height="18" rx="3" fill="{Q["cream"]}"/><rect x="10" y="0" width="6" height="18" rx="2" fill="{Q["cream2"]}"/><path d="M16 4 q8 0 8 6 q0 6 -8 6" stroke="{Q["cream2"]}" stroke-width="3" fill="none"/></g>' for k in range(3))
    w+=banner(116,12,Q["navy"],Q["navy2"])+banner(238,12,Q["coral"],Q["coral2"])
    w+=torch_w(146,110)+torch_w(246,110)
    w+=f'<rect x="148" y="104" width="94" height="110" fill="{Q["lav2"]}"/>'+iron_door(164,62,(Q["brown"],Q["brown2"]),grille=True)
    return w
def bunk_bed(x,y):
    def bunk(yy,c,c2): return f'<rect x="4" y="{yy}" width="86" height="10" rx="3" fill="{Q["cream"]}"/><rect x="4" y="{yy+6}" width="86" height="12" rx="3" fill="{c}"/><rect x="58" y="{yy+6}" width="32" height="12" rx="3" fill="{c2}"/><rect x="8" y="{yy-6}" width="20" height="10" rx="4" fill="{Q["cream"]}"/>'
    return f'''<g transform="translate({x} {y})">{shadow(48,92,52,7)}<rect x="0" y="0" width="6" height="92" rx="2" fill="{WOOD[1]}"/><rect x="88" y="0" width="6" height="92" rx="2" fill="{WOOD[2]}"/>
      {bunk(14,Q["navy"],Q["navy2"])}{bunk(58,Q["coral"],Q["coral2"])}<rect x="0" y="34" width="94" height="5" rx="2" fill="{WOOD[1]}"/><rect x="0" y="78" width="94" height="5" rx="2" fill="{WOOD[1]}"/>
      <g transform="translate(72 0)">{''.join(f'<rect x="0" y="{8+k*10}" width="12" height="3" fill="{WOOD[0]}"/>' for k in range(3))}</g></g>'''
def mug(x,y): return f'<g transform="translate({x} {y})"><rect x="0" y="0" width="10" height="12" rx="2" fill="{WOOD[0]}"/><rect x="6" y="0" width="4" height="12" rx="1" fill="{WOOD[2]}"/><path d="M10 3 q5 0 5 3 q0 3 -5 3" stroke="{WOOD[2]}" stroke-width="2" fill="none"/><ellipse cx="5" cy="1" rx="5" ry="2" fill="{Q["cream"]}"/></g>'
def stool(x,y,s=1): return f'<g transform="translate({x} {y}) scale({s})">{shadow(12,24,14,4)}<rect x="3" y="6" width="4" height="18" fill="{WOOD[2]}"/><rect x="17" y="6" width="4" height="18" fill="{WOOD[2]}"/><ellipse cx="12" cy="6" rx="12" ry="5" fill="{WOOD[1]}"/><ellipse cx="12" cy="5" rx="10" ry="3.5" fill="{WOOD[0]}"/></g>'
def card_table(x,y):
    cards=''.join(f'<rect x="{30+k*9}" y="{16+(k%2)*3}" width="8" height="11" rx="1.5" fill="{Q["cream"]}" transform="rotate({-12+k*9} {34+k*9} {22})"/><rect x="{32+k*9}" y="{19+(k%2)*3}" width="4" height="4" fill="{[Q["coral"],DARK,Q["coral"],DARK][k]}" transform="rotate({-12+k*9} {34+k*9} {22})"/>' for k in range(4))
    return f'''<g transform="translate({x} {y})">{shadow(50,64,52,8)}{stool(-6,30,.9)}{stool(84,30,.9)}<rect x="24" y="30" width="8" height="32" fill="{WOOD[2]}"/><rect x="68" y="30" width="8" height="32" fill="{WOOD[2]}"/>
      <ellipse cx="50" cy="28" rx="44" ry="16" fill="{WOOD[1]}"/><ellipse cx="50" cy="25" rx="42" ry="14" fill="{WOOD[0]}"/>{cards}{mug(16,12)}{mug(74,10)}
      <g transform="translate(62 26)"><rect x="0" y="0" width="8" height="8" rx="1.5" fill="{Q["cream"]}"/><circle cx="4" cy="4" r="1.2" fill="{DARK}"/></g></g>'''
def halberds(x,y):
    one=lambda dx,c,c2: f'<g transform="translate({dx} 0)"><rect x="0" y="0" width="4" height="96" rx="1" fill="{WOOD[1]}"/><path d="M2 0 L6 -14 L10 0 Z" fill="#c4c1cc"/><path d="M4 6 Q18 8 20 20 Q14 24 4 22 Z" fill="#c4c1cc"/><path d="M4 14 Q14 16 20 20 Q14 24 4 22 Z" fill="#9a97a4"/><path d="M0 10 L-8 6 L-8 14 L0 16 Z" fill="#9a97a4"/><path d="M0 28 L-6 34 L0 40" fill="{c}"/></g>'
    return f'<g transform="translate({x} {y})">{shadow(30,98,32,5)}<rect x="0" y="82" width="62" height="16" rx="3" fill="{WOOD[1]}"/><rect x="38" y="82" width="24" height="16" rx="3" fill="{WOOD[2]}"/>{one(14,Q["coral"],Q["coral2"])}{one(40,Q["navy"],Q["navy2"])}</g>'
def drum(x,y):
    zig=''.join(f'<path d="M{4+k*8} 10 L{8+k*8} 26 L{12+k*8} 10" stroke="{Q["mustard"]}" stroke-width="2" fill="none"/>' for k in range(4))
    return f'<g transform="translate({x} {y})">{shadow(22,36,24,5)}<rect x="2" y="6" width="40" height="28" rx="3" fill="{Q["coral"]}"/><rect x="26" y="6" width="16" height="28" rx="3" fill="{Q["coral2"]}"/>{zig}<ellipse cx="22" cy="6" rx="20" ry="6" fill="{Q["cream"]}"/><ellipse cx="22" cy="6" rx="20" ry="6" fill="none" stroke="{Q["mustard2"]}" stroke-width="2"/><rect x="20" y="-14" width="3" height="18" fill="{WOOD[2]}" transform="rotate(-30 22 0)"/><circle cx="14" cy="-12" r="3" fill="{Q["cream"]}"/></g>'
def weapon_chest(x,y): return chest(x,y)
def boots(x,y): return f'<g transform="translate({x} {y})">{shadow(16,22,18,4)}<path d="M2 0 L12 0 L12 16 L18 16 Q20 22 14 22 L2 22 Z" fill="{WOOD[2]}"/><path d="M16 2 L26 2 L26 16 L32 16 Q34 22 28 22 L16 22 Z" fill="{Q["brown2"]}"/></g>'
# ---------- TOY ROOM
PASTEL=('#f1e3c2','#e8b8a8','#a9c4dc','#cfe0a8','#f0d07a')
def wallpaper(seed):
    g=f'<rect x="0" y="0" width="390" height="214" fill="#e8c9bd"/>'+''.join(f'<rect x="{x}" y="0" width="13" height="214" fill="#f0dacf"/>' for x in range(0,390,26))
    return g+''.join(f'<circle cx="{13+x}" cy="{20+(x//26%2)*30+y}" r="2.6" fill="#d4917f" opacity=".5"/>' for x in range(0,390,26) for y in range(0,200,60))
def block(x,y,c,c2,letter='',s=22):
    return f'<g transform="translate({x} {y})"><rect x="0" y="0" width="{s}" height="{s}" rx="3" fill="{c}"/><rect x="{s*.62:.1f}" y="0" width="{s*.38:.1f}" height="{s}" rx="3" fill="{c2}"/><rect x="0" y="0" width="{s}" height="{s*0.22:.1f}" rx="2" fill="#fff" opacity=".25"/>{f"<text x=\"{s*.42:.1f}\" y=\"{s*.74:.1f}\" font-family=\"Fredoka,system-ui\" font-weight=\"700\" font-size=\"{s*.62:.1f}\" fill=\"#fff\" text-anchor=\"middle\">{letter}</text>" if letter else ""}</g>'
def kite(x,y): return f'<g transform="translate({x} {y})"><path d="M20 0 L40 26 L20 60 L0 26 Z" fill="{Q["coral"]}"/><path d="M20 0 L40 26 L20 26 Z" fill="{Q["mustard"]}"/><path d="M20 26 L20 60 L0 26 Z" fill="{Q["navy"]}"/><path d="M20 60 q-8 14 2 26 q8 12 -2 26" stroke="{DARK}" stroke-width="1.6" fill="none"/>{"".join(f"<path d=\"M{14+(k%2)*8} {74+k*14} l6 -4 l0 8 Z\" fill=\"{[Q['coral'],Q['mustard'],Q['navy']][k]}\"/>" for k in range(3))}</g>'
def toy_window(x,y):
    return f'''<g transform="translate({x} {y})"><rect x="-6" y="-6" width="76" height="92" rx="36" fill="{Q["cream"]}"/><rect x="0" y="0" width="64" height="80" rx="32" fill="#a9cbe0"/><circle cx="44" cy="22" r="9" fill="{Q["mustard"]}"/><path d="M0 60 Q16 50 32 58 Q48 50 64 58 L64 80 L0 80 Z" fill="{Q["olive"]}"/><rect x="31" y="0" width="2" height="80" fill="{Q["cream"]}"/><rect x="0" y="40" width="64" height="2" fill="{Q["cream"]}"/>
      <path d="M-10 -10 L18 -10 Q10 40 -4 86 L-10 86 Z" fill="{Q["pink"]}"/><path d="M74 -10 L46 -10 Q54 40 68 86 L74 86 Z" fill="{Q["pink2"]}"/><rect x="-14" y="-14" width="92" height="7" rx="3" fill="{WOOD[1]}"/></g>'''
def toy_shelf(x,y):
    return f'''<g transform="translate({x} {y})"><rect x="0" y="40" width="96" height="7" rx="2" fill="{WOOD[1]}"/><rect x="66" y="40" width="30" height="7" rx="2" fill="{WOOD[2]}"/>{block(4,18,Q["navy"],Q["navy2"],"A")}{block(28,18,Q["coral"],Q["coral2"],"B")}{block(16,-4,Q["mustard"],Q["mustard2"],"C")}
      <circle cx="70" cy="26" r="13" fill="{Q["coral"]}"/><path d="M57 26 A13 13 0 0 0 83 26 Z" fill="{Q["cream"]}"/><path d="M70 13 A13 13 0 0 1 83 26 L70 26 Z" fill="{Q["coral2"]}"/></g>'''
def toy_room_head():
    w=wallpaper(3)+f'<rect x="0" y="176" width="390" height="38" fill="#c58a55"/><rect x="0" y="176" width="390" height="6" fill="#a06a3e"/>'
    w+=toy_window(28,46)+kite(300,20)+toy_shelf(270,128)+toy_shelf(96,128)
    w+=''.join(f'<path d="M{150+k*18} {28+(k%2)*8} l9 -14 l9 14 Z" fill="{PASTEL[k%5]}"/>' for k in range(5))+f'<path d="M140 30 Q195 46 250 30" stroke="{DARK}" stroke-width="1.4" fill="none"/>'
    w+=f'<rect x="150" y="104" width="90" height="110" fill="#e0b0a4"/>'+gate_arch(164,62,(Q["navy"],Q["navy2"]))+f'<g transform="translate(195 140)"><path d="M0 -10 L3 -3 L10 -3 L4 2 L6 9 L0 5 L-6 9 L-4 2 L-10 -3 L-3 -3 Z" fill="{Q["mustard"]}"/></g>'
    return w
def rocking_horse(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(44,72,46,6)}<path d="M0 64 Q44 84 88 64" stroke="{WOOD[2]}" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M14 66 L22 40 M70 66 L64 40" stroke="{WOOD[1]}" stroke-width="6"/>
      <ellipse cx="44" cy="36" rx="30" ry="14" fill="{Q["cream"]}"/><path d="M44 22 A30 14 0 0 1 74 36 A30 14 0 0 1 44 50 Z" fill="{Q["cream2"]}"/><rect x="30" y="20" width="24" height="10" rx="3" fill="{Q["coral"]}"/>
      <path d="M66 30 L74 4 Q80 -4 90 4 L94 14 Q90 18 84 14 L80 30 Z" fill="{Q["cream"]}"/><path d="M70 6 Q66 -2 62 10 L68 26" fill="{Q["coral"]}"/><circle cx="84" cy="6" r="2" fill="{DARK}"/><path d="M14 32 Q2 30 4 44" stroke="{Q["coral"]}" stroke-width="5" fill="none" stroke-linecap="round"/></g>'''
def block_tower(x,y):
    return f'<g transform="translate({x} {y})">{shadow(28,70,30,5)}{block(0,44,Q["navy"],Q["navy2"],"S")}{block(26,44,Q["olive"],Q["olive2"],"A")}{block(13,20,Q["coral"],Q["coral2"],"M")}{block(16,-4,Q["mustard"],Q["mustard2"],"")}</g>'
def toy_castle(x,y):
    tower=lambda tx,c,c2: f'<g transform="translate({tx} 0)"><rect x="0" y="14" width="22" height="46" fill="{Q["grey"]}"/><rect x="14" y="14" width="8" height="46" fill="{Q["grey2"]}"/><path d="M-3 16 L11 -4 L25 16 Z" fill="{c}"/><path d="M11 -4 L25 16 L17 16 Z" fill="{c2}"/></g>'
    return f'''<g transform="translate({x} {y})">{shadow(40,64,44,6)}<rect x="10" y="28" width="60" height="34" fill="{Q["grey"]}"/><rect x="48" y="28" width="22" height="34" fill="{Q["grey2"]}"/>{"".join(f"<rect x=\"{12+k*12}\" y=\"22\" width=\"7\" height=\"8\" fill=\"{Q['grey']}\"/>" for k in range(5))}
      <path d="M32 62 L32 46 Q40 36 48 46 L48 62 Z" fill="{WOOD[2]}"/>{tower(0,Q["coral"],Q["coral2"])}{tower(58,Q["navy"],Q["navy2"])}<path d="M11 -4 L11 -16 L22 -12 L11 -8" fill="{Q["mustard"]}"/></g>'''
def toy_chest(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(36,58,40,6)}<rect x="0" y="22" width="72" height="36" rx="4" fill="{Q["navy"]}"/><rect x="44" y="22" width="28" height="36" rx="4" fill="{Q["navy2"]}"/>
      <rect x="6" y="-4" width="12" height="30" rx="2" fill="{Q["mustard"]}" transform="rotate(-20 12 20)"/><circle cx="36" cy="16" r="11" fill="{Q["coral"]}"/><path d="M25 16 A11 11 0 0 0 47 16 Z" fill="{Q["cream"]}"/>{block(46,4,Q["olive"],Q["olive2"],"",18)}
      <rect x="-2" y="20" width="76" height="8" rx="3" fill="{Q["navy2"]}"/><path d="M6 36 L18 46 L30 36 L42 46 L54 36 L66 46" stroke="{Q["mustard"]}" stroke-width="3" fill="none"/></g>'''
def ball(x,y,s=1): return f'<g transform="translate({x} {y}) scale({s})">{shadow(14,27,14,4)}<circle cx="14" cy="14" r="14" fill="{Q["coral"]}"/><path d="M0 14 A14 14 0 0 0 28 14 Z" fill="{Q["cream"]}"/><path d="M14 0 A14 14 0 0 1 28 14 L14 14 Z" fill="{Q["coral2"]}"/><path d="M14 14 L28 14 A14 14 0 0 1 14 28 Z" fill="{Q["cream2"]}"/></g>'
def spin_top(x,y): return f'<g transform="translate({x} {y})">{shadow(14,32,12,3)}<path d="M0 14 Q14 2 28 14 L14 32 Z" fill="{Q["mustard"]}"/><path d="M14 8 Q22 8 28 14 L14 32 Z" fill="{Q["mustard2"]}"/><path d="M2 16 L26 16" stroke="{Q["coral"]}" stroke-width="4"/><rect x="12" y="-2" width="4" height="10" rx="2" fill="{WOOD[1]}"/></g>'
def toy_train(x,y):
    car=lambda dx,c,c2: f'<g transform="translate({dx} 0)">{two(0,8,30,18,c,c2,3)}<circle cx="7" cy="28" r="5" fill="{DARK}"/><circle cx="23" cy="28" r="5" fill="{DARK}"/></g>'
    return f'<g transform="translate({x} {y})">{shadow(50,34,54,5)}{car(0,Q["coral"],Q["coral2"])}{car(34,Q["olive"],Q["olive2"])}<g transform="translate(68 0)">{two(0,8,32,18,Q["navy"],Q["navy2"],3)}<rect x="4" y="-4" width="12" height="14" fill="{Q["navy"]}"/><rect x="22" y="0" width="7" height="10" fill="{DARK}"/><circle cx="8" cy="28" r="5" fill="{DARK}"/><circle cx="24" cy="28" r="5" fill="{DARK}"/></g></g>'
# ---------- HALL OF MIRRORS
MIR=('#cfe3ea','#a9cbe0','#e6f1f4')
def mirror_shape(w,h,oval=False):
    if oval: return f'<ellipse cx="{w/2}" cy="{h/2}" rx="{w/2}" ry="{h/2}" fill="{Q["mustard"]}"/><ellipse cx="{w/2}" cy="{h/2}" rx="{w/2-5}" ry="{h/2-5}" fill="{MIR[1]}"/><clipPath id="mo{w}{h}"><ellipse cx="{w/2}" cy="{h/2}" rx="{w/2-5}" ry="{h/2-5}"/></clipPath><g clip-path="url(#mo{w}{h})"><path d="M0 {h*0.7} L{w} {h*0.2} L{w} {h*0.42} L0 {h*0.92} Z" fill="{MIR[2]}" opacity=".7"/><path d="M0 {h*0.45} L{w} {h*0.02} L{w} {h*0.1} L0 {h*0.53} Z" fill="{MIR[2]}" opacity=".5"/></g><path d="M{w/2} 0 A{w/2} {h/2} 0 0 1 {w/2} {h} " stroke="{Q["mustard2"]}" stroke-width="5" fill="none"/>'
    return f'<rect x="0" y="0" width="{w}" height="{h}" rx="6" fill="{Q["mustard"]}"/><rect x="{w*.62:.1f}" y="0" width="{w*.38:.1f}" height="{h}" rx="6" fill="{Q["mustard2"]}"/><rect x="5" y="5" width="{w-10}" height="{h-10}" rx="3" fill="{MIR[1]}"/><clipPath id="mr{w}{h}"><rect x="5" y="5" width="{w-10}" height="{h-10}"/></clipPath><g clip-path="url(#mr{w}{h})"><path d="M0 {h*0.75} L{w} {h*0.25} L{w} {h*0.45} L0 {h*0.95} Z" fill="{MIR[2]}" opacity=".7"/><path d="M0 {h*0.45} L{w} 0 L{w} {h*0.08} L0 {h*0.53} Z" fill="{MIR[2]}" opacity=".5"/></g>'
def chandelier(x,y):
    arms=''.join(f'<g transform="translate({dx} 0)"><rect x="-2" y="-8" width="4" height="10" fill="{Q["cream"]}"/><path d="M0 -16 C-4 -11 -3 -8 0 -8 C3 -8 4 -11 0 -16 Z" fill="{Q["mustard"]}"/></g>' for dx in (-34,-17,0,17,34))
    return f'<g transform="translate({x} {y})"><rect x="-1" y="-40" width="2" height="34" fill="{Q["mustard2"]}"/><circle cx="0" cy="0" r="40" fill="{Q["mustard"]}" opacity=".12"/><path d="M-38 4 Q0 22 38 4" stroke="{Q["mustard"]}" stroke-width="4" fill="none"/>{arms}{"".join(f"<path d=\"M{dx} 8 l3 6 l-3 6 l-3 -6 Z\" fill=\"#e6f1f4\"/>" for dx in (-24,-8,8,24))}</g>'
def mirrors_head():
    w=f'<rect x="0" y="0" width="390" height="214" fill="#2f5560"/>'+''.join(f'<rect x="{x}" y="0" width="10" height="214" fill="#284a54"/>' for x in (6,128,252,374))
    w+=''.join(f'<rect x="{x}" y="0" width="4" height="214" fill="{Q["mustard2"]}" opacity=".7"/>' for x in (9,131,255,377))
    for mx,my,mw,mh in ((24,44,44,120),(78,60,34,92),(278,60,34,92),(322,44,44,120)):
        w+=f'<g transform="translate({mx} {my})">{mirror_shape(mw,mh)}</g>'
    w+=chandelier(195,52)
    w+=f'<rect x="146" y="102" width="98" height="112" fill="#244650"/>'+gate_arch(164,62,(Q["mustard"],Q["mustard2"]))+f'<path d="M172 150 C172 128 210 128 210 150" stroke="#fff" stroke-opacity=".35" stroke-width="3" fill="none"/>'
    return w
def stand_mirror(x,y):
    return f'<g transform="translate({x} {y})">{shadow(24,96,28,5)}<path d="M8 96 L24 74 L40 96" stroke="{Q["mustard2"]}" stroke-width="4" fill="none"/><g transform="translate(2 0)">{mirror_shape(44,80,True)}</g></g>'
def wide_mirror(x,y):
    return f'<g transform="translate({x} {y})">{shadow(40,80,44,5)}<rect x="8" y="60" width="5" height="20" fill="{Q["mustard2"]}"/><rect x="66" y="60" width="5" height="20" fill="{Q["mustard2"]}"/><g>{mirror_shape(80,64)}</g></g>'
def candelabra(x,y):
    cand=''.join(f'<g transform="translate({dx} {-(dx==16)*8})"><rect x="-2" y="0" width="4" height="12" fill="{Q["cream"]}"/><path d="M0 -8 C-4 -3 -3 0 0 0 C3 0 4 -3 0 -8 Z" fill="{Q["mustard"]}"/></g>' for dx in (4,16,28))
    return f'<g transform="translate({x} {y})">{shadow(16,72,14,4)}<circle cx="16" cy="6" r="22" fill="{Q["mustard"]}" opacity=".14"/><rect x="14" y="16" width="4" height="54" fill="{Q["mustard"]}"/><path d="M4 16 Q16 26 28 16" stroke="{Q["mustard"]}" stroke-width="3" fill="none"/><path d="M6 72 L16 62 L26 72 Z" fill="{Q["mustard2"]}"/><g transform="translate(0 8)">{cand}</g></g>'
def ottoman(x,y,c=None,c2=None):
    c=c or Q["coral"]; c2=c2 or Q["coral2"]
    return f'<g transform="translate({x} {y})">{shadow(24,34,26,5)}<rect x="4" y="22" width="4" height="12" fill="{Q["mustard2"]}"/><rect x="40" y="22" width="4" height="12" fill="{Q["mustard2"]}"/>{two(0,6,48,20,c,c2,8)}<ellipse cx="24" cy="7" rx="24" ry="6" fill="{c}"/><circle cx="24" cy="8" r="2" fill="{Q["mustard"]}"/></g>'
def palm(x,y):
    leaves=''.join(f'<path d="M26 26 Q{26+dx*0.5} {6+dy} {26+dx} {20+dy}" stroke="{Q["green"] if k%2 else Q["olive"]}" stroke-width="7" fill="none" stroke-linecap="round"/>' for k,(dx,dy) in enumerate(((-26,0),(-16,-16),(0,-22),(16,-16),(26,0))))
    return f'<g transform="translate({x} {y})">{shadow(26,72,22,5)}{leaves}<rect x="24" y="24" width="4" height="22" fill="{WOOD[2]}"/><path d="M10 44 L42 44 L36 72 L16 72 Z" fill="{Q["coral"]}"/><path d="M26 44 L42 44 L36 72 L26 72 Z" fill="{Q["coral2"]}"/><rect x="8" y="42" width="36" height="6" rx="2" fill="{Q["mustard"]}"/></g>'
def sparkle(x,y,s=1): return f'<g transform="translate({x} {y}) scale({s})"><path d="M8 0 L10 6 L16 8 L10 10 L8 16 L6 10 L0 8 L6 6 Z" fill="#e6f1f4"/></g>'
# ---------- BATHHOUSE
def tiles_wall(c,c2,seed):
    g=f'<rect x="0" y="0" width="390" height="214" fill="{c}"/>'
    g+=''.join(f'<rect x="{x+1}" y="{y+1}" width="18" height="18" rx="2" fill="{c2}"/>' for x in range(0,390,20) for y in range(0,214,20) if (x//20+y//20)%2==0)
    return g
def spout(x,y):
    return f'''<g transform="translate({x} {y})"><path d="M0 0 Q30 -26 60 0 Q30 14 0 0 Z" fill="{Q["cream"]}"/><path d="M30 -13 Q46 -12 60 0 Q46 8 30 7 Z" fill="{Q["cream2"]}"/>{"".join(f"<path d=\"M30 -11 L{6+k*12} {-2+abs(k-2)*2}\" stroke=\"{Q['cream2']}\" stroke-width=\"1.6\"/>" for k in range(5))}
      <rect x="24" y="6" width="12" height="10" rx="2" fill="{Q["mustard"]}"/><path d="M28 16 L28 60 M32 16 L32 60" stroke="#a9cbe0" stroke-width="3"/><ellipse cx="30" cy="66" rx="40" ry="10" fill="{Q["grey"]}"/><ellipse cx="30" cy="64" rx="34" ry="7" fill="#6f9bb3"/><path d="M18 62 q6 -3 12 0 q6 3 12 0" stroke="#a9cbe0" stroke-width="2" fill="none"/></g>'''
def steam(x,y,s=1): return f'<g transform="translate({x} {y}) scale({s})" opacity=".55"><path d="M0 30 q-8 -8 0 -15 q8 -7 0 -15" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M14 34 q-8 -8 0 -15 q8 -7 0 -15" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/></g>'
def bathhouse_head():
    w=tiles_wall('#cfe6e8','#b6d6da',1)+f'<rect x="0" y="150" width="390" height="64" fill="#3f8a8f"/>'+''.join(f'<rect x="{x+1}" y="{150+y+1}" width="18" height="18" rx="2" fill="#4f9a9f"/>' for x in range(0,390,20) for y in range(0,64,20) if (x//20+y//20)%2)
    w+=f'<rect x="0" y="146" width="390" height="6" fill="{Q["cream"]}"/>'
    for wx in (30,300):
        w+=f'<g transform="translate({wx} 34)"><rect x="-6" y="-6" width="72" height="96" rx="34" fill="{Q["cream"]}"/><rect x="0" y="0" width="60" height="84" rx="30" fill="#a9cbe0"/><rect x="29" y="0" width="2" height="84" fill="{Q["cream"]}"/>{steam(14,24,1)}</g>'
    w+=spout(104,96)+spout(226,96)
    w+=''.join(f'<g transform="translate({x} 20)"><circle cx="0" cy="0" r="4" fill="{Q["mustard"]}"/><rect x="-10" y="4" width="20" height="40" rx="4" fill="{c}"/><rect x="-10" y="34" width="20" height="4" fill="#fff" opacity=".5"/></g>' for x,c in ((140,Q["coral"]),(250,Q["navy"])))
    w+=f'<rect x="148" y="104" width="94" height="110" fill="#9cc6ca"/>'+gate_arch(164,62,(WOOD[1],WOOD[2]))
    return w
def pool(x,y,w=150,h=84):
    return f'''<g transform="translate({x} {y})"><rect x="0" y="0" width="{w}" height="{h}" rx="16" fill="{Q["cream"]}"/><rect x="0" y="{h-8}" width="{w}" height="8" rx="4" fill="{Q["cream2"]}"/><rect x="8" y="8" width="{w-16}" height="{h-18}" rx="10" fill="#3f8a8f"/><rect x="8" y="16" width="{w-16}" height="{h-26}" rx="10" fill="#6fb3b8"/>
      {"".join(f'<path d="M{20+k*30} {30+(k%2)*16} q7 -4 14 0" stroke="#bfe0e2" stroke-width="2.4" fill="none" stroke-linecap="round"/>' for k in range(int((w-40)/30)))}
      <g transform="translate({w-34} 8)">{"".join(f'<rect x="{k*8}" y="0" width="6" height="{h-18}" fill="{Q["grey"]}" opacity=".5"/>' for k in range(3))}</g>{steam(20,-26,.8)}</g>'''
def tub(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(40,58,44,6)}<path d="M8 50 L4 58 M72 50 L76 58" stroke="{Q["mustard"]}" stroke-width="5" stroke-linecap="round"/><path d="M0 16 L80 16 Q80 52 40 52 Q0 52 0 16 Z" fill="{Q["cream"]}"/><path d="M50 16 L80 16 Q80 52 40 52 Q48 40 50 16 Z" fill="{Q["cream2"]}"/>
      {"".join(f'<circle cx="{10+k*10}" cy="{14-(k%3)*4}" r="{6+(k%2)*2}" fill="#fff"/>' for k in range(7))}<rect x="70" y="-8" width="4" height="22" fill="{Q["grey2"]}"/><path d="M72 -8 Q62 -10 62 0" stroke="{Q["grey2"]}" stroke-width="4" fill="none"/></g>'''
def towel_rack(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(28,72,30,5)}<rect x="2" y="0" width="5" height="72" rx="2" fill="{WOOD[1]}"/><rect x="50" y="0" width="5" height="72" rx="2" fill="{WOOD[2]}"/><rect x="0" y="10" width="57" height="5" rx="2" fill="{WOOD[1]}"/><rect x="0" y="40" width="57" height="5" rx="2" fill="{WOOD[1]}"/>
      <path d="M8 10 L26 10 L26 40 L8 40 Z" fill="{Q["coral"]}"/><rect x="8" y="30" width="18" height="4" fill="#fff" opacity=".5"/><path d="M30 10 L48 10 L48 46 L30 46 Z" fill="{Q["navy"]}"/><rect x="30" y="36" width="18" height="4" fill="#fff" opacity=".5"/><path d="M14 40 L44 40 L44 60 L14 60 Z" fill="{Q["cream"]}"/></g>'''
def bucket_brush(x,y): return f'<g transform="translate({x} {y})">{shadow(18,30,18,4)}<path d="M2 6 L32 6 L28 30 L6 30 Z" fill="{WOOD[1]}"/><path d="M20 6 L32 6 L28 30 L20 30 Z" fill="{WOOD[2]}"/><rect x="2" y="12" width="30" height="3" fill="#5a5664"/><rect x="4" y="22" width="26" height="3" fill="#5a5664"/><ellipse cx="17" cy="6" rx="15" ry="4" fill="#6fb3b8"/><rect x="24" y="-12" width="6" height="18" rx="2" fill="{Q["mustard"]}" transform="rotate(20 27 0)"/></g>'
def fern(x,y):
    leaves=''.join(f'<path d="M20 30 Q{20+dx*0.6} {10+dy} {20+dx} {18+dy}" stroke="{Q["green"] if k%2 else Q["olive"]}" stroke-width="6" fill="none" stroke-linecap="round"/>' for k,(dx,dy) in enumerate(((-20,4),(-12,-10),(0,-16),(12,-10),(20,4))))
    return f'<g transform="translate({x} {y})">{shadow(20,52,18,4)}{leaves}<path d="M6 30 L34 30 L30 52 L10 52 Z" fill="{Q["cream"]}"/><path d="M20 30 L34 30 L30 52 L20 52 Z" fill="{Q["cream2"]}"/></g>'
def duck(x,y): return f'<g transform="translate({x} {y})">{shadow(12,18,12,3)}<path d="M0 10 Q2 18 12 18 Q22 18 22 10 Q14 12 10 8 Z" fill="{Q["mustard"]}"/><circle cx="16" cy="5" r="5" fill="{Q["mustard"]}"/><path d="M20 4 L26 5 L20 7 Z" fill="{Q["orange"]}"/><circle cx="17" cy="4" r="1" fill="{DARK}"/></g>'
def soap(x,y): return f'<g transform="translate({x} {y})"><rect x="0" y="0" width="18" height="10" rx="4" fill="{Q["pink"]}"/><rect x="10" y="0" width="8" height="10" rx="3" fill="{Q["pink2"]}"/>{"".join(f"<circle cx=\"{4+k*6}\" cy=\"{-4-k%2*4}\" r=\"{2+k%2}\" fill=\"#fff\" opacity=\".9\"/>" for k in range(3))}</g>'
def bubbles(x,y): return f'<g transform="translate({x} {y})">{"".join(f"<circle cx=\"{dx}\" cy=\"{dy}\" r=\"{r}\" fill=\"#e6f1f4\" opacity=\".85\"/><circle cx=\"{dx-r*.35}\" cy=\"{dy-r*.35}\" r=\"{r*.3}\" fill=\"#fff\"/>" for dx,dy,r in ((6,10,6),(18,4,4),(20,16,5),(30,8,3)))}</g>'
def bench_bath(x,y): return f'<g transform="translate({x} {y})">{shadow(36,30,38,4)}{two(0,6,72,10,WOOD[0],WOOD[1],3)}<rect x="6" y="16" width="6" height="14" fill="{WOOD[2]}"/><rect x="60" y="16" width="6" height="14" fill="{WOOD[2]}"/><path d="M14 0 L30 0 L30 6 L14 6 Z" fill="{Q["navy"]}"/></g>'
# ---------- TROPHY ROOM
def cup(x,y,s=1,c=None,c2=None):
    c=c or Q["mustard"]; c2=c2 or Q["mustard2"]
    return f'<g transform="translate({x} {y}) scale({s})"><path d="M4 0 L36 0 Q36 26 20 30 Q4 26 4 0 Z" fill="{c}"/><path d="M20 0 L36 0 Q36 26 20 30 Z" fill="{c2}"/><path d="M4 4 Q-6 4 -4 14 Q-2 20 8 20" stroke="{c}" stroke-width="3" fill="none"/><path d="M36 4 Q46 4 44 14 Q42 20 32 20" stroke="{c2}" stroke-width="3" fill="none"/><rect x="17" y="30" width="6" height="8" fill="{c2}"/><rect x="8" y="38" width="24" height="6" rx="1" fill="{WOOD[2]}"/><path d="M12 6 L12 16" stroke="#fff" stroke-opacity=".5" stroke-width="3" stroke-linecap="round"/></g>'
def plaque(x,y,c=None):
    return f'<g transform="translate({x} {y})"><path d="M0 0 L36 0 L36 24 Q36 40 18 46 Q0 40 0 24 Z" fill="{WOOD[1]}"/><path d="M18 0 L36 0 L36 24 Q36 40 18 46 Z" fill="{WOOD[2]}"/><circle cx="18" cy="20" r="10" fill="{c or Q["mustard"]}"/><path d="M18 13 L20 18 L25 18 L21 21 L23 26 L18 23 L13 26 L15 21 L11 18 L16 18 Z" fill="{Q["mustard2"]}"/></g>'
def medal_ribbon(x,y,c,c2):
    return f'<g transform="translate({x} {y})"><path d="M0 0 L8 0 L16 26 L8 26 Z" fill="{c}"/><path d="M24 0 L16 0 L8 26 L16 26 Z" fill="{c2}"/><circle cx="12" cy="32" r="9" fill="{Q["mustard"]}"/><path d="M12 23 A9 9 0 0 1 12 41 Z" fill="{Q["mustard2"]}"/></g>'
def trophy_head():
    w=f'<rect x="0" y="0" width="390" height="214" fill="#2f5530"/>'+''.join(f'<rect x="{x}" y="0" width="22" height="214" fill="#2a4c2b"/>' for x in range(0,390,44))
    w+=f'<rect x="0" y="150" width="390" height="64" fill="{WOOD[2]}"/>'+''.join(f'<rect x="{x+2}" y="154" width="{40}" height="56" rx="3" fill="{WOOD[1]}"/>' for x in range(0,390,44))+f'<rect x="0" y="146" width="390" height="8" fill="{Q["mustard2"]}"/>'
    for sx in (18,276):
        w+=f'<rect x="{sx}" y="64" width="96" height="6" rx="2" fill="{WOOD[1]}"/><rect x="{sx}" y="122" width="96" height="6" rx="2" fill="{WOOD[1]}"/>'
        w+=cup(sx+6,20,.9)+cup(sx+56,30,.7,"#c4c1cc","#9a97a4")+cup(sx+10,90,.65,"#c58a55","#a06a3e")+medal_ribbon(sx+60,76,Q["coral"],Q["navy"])
    w+=plaque(126,40)+plaque(228,40,Q["grey"])
    w+=f'<g transform="translate(195 30)"><path d="M-46 0 L46 0 L40 14 L46 28 L-46 28 L-40 14 Z" fill="{Q["coral"]}"/><path d="M0 0 L46 0 L40 14 L46 28 L0 28 Z" fill="{Q["coral2"]}"/><rect x="-30" y="12" width="60" height="4" rx="2" fill="{Q["mustard"]}"/></g>'
    w+=f'<rect x="148" y="104" width="94" height="110" fill="#244a25"/>'+gate_arch(164,62,(Q["coral"],Q["coral2"]))+''.join(f'<circle cx="{170+k*12.5}" cy="132" r="2" fill="{Q["mustard"]}"/>' for k in range(5))
    return w
def podium(x,y):
    step=lambda dx,h,n,c,c2: f'<g transform="translate({dx} {60-h})">{two(0,0,34,h,c,c2,2)}<text x="13" y="{h*0.62}" font-family="Fredoka,system-ui" font-weight="700" font-size="14" fill="#fff" text-anchor="middle">{n}</text></g>'
    return f'<g transform="translate({x} {y})">{shadow(52,62,56,6)}{step(0,30,2,"#c4c1cc","#9a97a4")}{step(34,46,1,Q["mustard"],Q["mustard2"])}{step(68,22,3,"#c58a55","#a06a3e")}{cup(39,-12,.6)}</g>'
def display_case(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(36,86,40,6)}<rect x="0" y="56" width="72" height="30" rx="3" fill="{WOOD[1]}"/><rect x="44" y="56" width="28" height="30" rx="3" fill="{WOOD[2]}"/><rect x="2" y="0" width="68" height="58" rx="3" fill="#a9cbe0" opacity=".55"/>
      <rect x="2" y="0" width="68" height="58" rx="3" fill="none" stroke="{Q["mustard2"]}" stroke-width="3"/><path d="M10 50 L30 8 L36 8 L16 50 Z" fill="#fff" opacity=".35"/>{cup(16,12,.7)}{medal_ribbon(44,10,Q["navy"],Q["coral"])}</g>'''
def statue(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(24,104,26,5)}<rect x="4" y="76" width="40" height="28" rx="2" fill="{Q["grey"]}"/><rect x="28" y="76" width="16" height="28" rx="2" fill="{Q["grey2"]}"/>
      <path d="M12 76 L14 40 Q24 32 34 40 L36 76 Z" fill="#c58a55"/><path d="M24 34 Q34 40 36 76 L24 76 Z" fill="#a06a3e"/><circle cx="24" cy="26" r="9" fill="#c58a55"/><path d="M24 17 A9 9 0 0 1 24 35 Z" fill="#a06a3e"/>
      <path d="M34 44 L46 18" stroke="#c58a55" stroke-width="6" stroke-linecap="round"/>{cup(36,0,.45)}</g>'''
def crossed_oars(x,y):
    return f'<g transform="translate({x} {y})">{shadow(30,64,32,4)}<g transform="rotate(30 30 30)"><rect x="28" y="-6" width="4" height="70" fill="{WOOD[1]}"/><ellipse cx="30" cy="58" rx="7" ry="14" fill="{Q["navy"]}"/></g><g transform="rotate(-30 30 30)"><rect x="28" y="-6" width="4" height="70" fill="{WOOD[2]}"/><ellipse cx="30" cy="58" rx="7" ry="14" fill="{Q["coral"]}"/></g></g>'
def trophy_rug(x,y): return f'<g transform="translate({x} {y})"><rect x="0" y="0" width="90" height="56" rx="6" fill="{Q["coral2"]}"/><rect x="5" y="5" width="80" height="46" rx="4" fill="{Q["coral"]}"/><rect x="11" y="11" width="68" height="34" rx="3" fill="none" stroke="{Q["mustard"]}" stroke-width="2.4"/><path d="M45 18 L48 25 L56 25 L50 30 L52 37 L45 33 L38 37 L40 30 L34 25 L42 25 Z" fill="{Q["mustard"]}"/></g>'
def medal(x,y): return f'<g transform="translate({x} {y})">{medal_ribbon(0,0,Q["navy"],Q["coral"])}</g>'
def small_cup(x,y): return cup(x,y,.55)

STEP_=STEP
HEADS['Guard room']=guard_room_head()+STEP_
HEADS['Toy room']=toy_room_head()+STEP_
HEADS['Hall of mirrors']=mirrors_head()+STEP_
HEADS['Bathhouse']=bathhouse_head()+STEP_
HEADS['Trophy room']=trophy_head()+STEP_
# props: [box(x,y,w,h) relative to the drawing's origin, svg]
addp('bunk_bed',bunk_bed(0,0),(0,-8,96,104)); addp('card_table',card_table(0,0),(-8,0,116,72)); addp('halberds',halberds(0,0),(-8,-16,74,116))
addp('drum',drum(0,0),(0,-18,46,58)); addp('boots',boots(0,0),(0,0,36,26)); addp('mug',mug(0,0),(0,0,16,14)); addp('helmet_s',f'<g>{shadow(14,22,14,3)}{helmet(0,0,1)}</g>',(0,-6,30,30))
addp('stool',stool(0,0),(0,0,26,28))
addp('rocking_horse',rocking_horse(0,0),(0,-6,98,82)); addp('block_tower',block_tower(0,0),(0,-6,52,78)); addp('toy_castle',toy_castle(0,0),(-4,-18,88,86))
addp('toy_chest',toy_chest(0,0),(-2,-8,78,68)); addp('ball',ball(0,0),(0,0,30,32)); addp('spin_top',spin_top(0,0),(0,-4,30,38)); addp('toy_train',toy_train(0,0),(0,-6,102,42))
addp('blocks_s',f'<g>{shadow(24,24,24,4)}{block(0,4,Q["coral"],Q["coral2"],"",20)}{block(24,6,Q["navy"],Q["navy2"],"",18)}</g>',(0,0,46,28))
addp('stand_mirror',stand_mirror(0,0),(0,0,50,100)); addp('wide_mirror',wide_mirror(0,0),(0,0,82,84)); addp('candelabra',candelabra(0,0),(-6,-8,44,82))
addp('ottoman',ottoman(0,0),(0,0,50,38)); addp('ottoman_navy',ottoman(0,0,Q["navy"],Q["navy2"]),(0,0,50,38)); addp('palm',palm(0,0),(-2,-2,56,76)); addp('sparkle',sparkle(0,0),(0,0,16,16)); addp('sparkle_s',sparkle(0,0,.7),(0,0,12,12))
addp('pool',pool(0,0),(0,-26,150,110)); addp('pool_s',pool(0,0,110,70),(0,-26,110,96)); addp('tub',tub(0,0),(-2,-10,84,70)); addp('towel_rack',towel_rack(0,0),(0,0,58,76))
addp('bucket_brush',bucket_brush(0,0),(0,-12,36,44)); addp('fern',fern(0,0),(-2,-2,44,56)); addp('duck',duck(0,0),(0,0,26,20)); addp('soap',soap(0,0),(0,-8,20,18)); addp('bubbles',bubbles(0,0),(0,0,34,22)); addp('bench_bath',bench_bath(0,0),(0,0,72,32))
addp('podium',podium(0,0),(0,-32,104,96)); addp('display_case',display_case(0,0),(0,0,72,90)); addp('statue',statue(0,0),(0,0,50,108)); addp('crossed_oars',crossed_oars(0,0),(0,-6,62,72))
addp('trophy_rug',trophy_rug(0,0),(0,0,90,56)); addp('medal',medal(0,0),(0,0,24,42)); addp('small_cup',small_cup(0,0),(-2,0,26,26))
def clean(s): return re.sub(r'\s+',' ',s).strip()
HEADS={k:clean(v) for k,v in HEADS.items()}
json.dump({'heads':HEADS,'props':PROPS},open('./third_floor_art.json','w'),separators=(',',':'),ensure_ascii=False)
print({k:len(v) for k,v in HEADS.items()}, len(PROPS))
