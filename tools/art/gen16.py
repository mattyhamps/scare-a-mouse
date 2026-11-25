import json, math, random
g15=open('./gen15.py').read()
exec(g15[:g15.index("rg=random.Random(4)")])
# ================= Outside floor: Orchard, Stables, Moat bridge, Gate (same rules as K2 / M2)
def road_dirt(): return f'<path d="{road}" fill="none" stroke="{Q["tan2"]}" stroke-width="44" stroke-linecap="round" transform="translate(0 3)"/><path d="{road}" fill="none" stroke="{Q["tan"]}" stroke-width="40" stroke-linecap="round"/><path d="{road}" fill="none" stroke="#dcc08e" stroke-width="14" stroke-linecap="round"/>'
def road_planks(posts=False):
    s=f'<path d="{road}" fill="none" stroke="#2a140a" stroke-opacity=".2" stroke-width="46" transform="translate(0 6)"/><path d="{road}" fill="none" stroke="{WOOD[2]}" stroke-width="46"/><path d="{road}" fill="none" stroke="{WOOD[0]}" stroke-width="40"/><path d="{road}" fill="none" stroke="{WOOD[1]}" stroke-width="40" stroke-dasharray="2.5 11"/>'
    return s
def page(name,count,base_n,bg,ground,sky,path,props,extra=''):
    return f'''<div style="{SC}background:{bg}">
  <svg width="390" height="844" style="position:absolute;left:0;top:0">{ground}{path}{sky}{STEP}<rect x="0" y="214" width="390" height="10" fill="#2a140a" opacity=".1"/>{props}{extra}</svg>
  <div style="position:absolute;left:0;right:0;top:0;height:56px;background:{Q["purple"]};z-index:4">
    {pill(14,8,98,40,Q["mustard"],Q["mustard2"],'Castle',16)}<div style="position:absolute;left:126px;top:12px;{TT};font-size:24px;color:{Q["cream"]}">{name}</div><b style="position:absolute;right:16px;top:18px;font:700 15px Fredoka,sans-serif;color:{Q["cream"]}">{count}</b></div>
  {nodes(base_n)}
  <div style="position:absolute;left:122px;top:430px;z-index:4">{sv('mouse',36)}</div>
</div>'''
def grass_ground(seed,col=GR):
    r=random.Random(seed)
    g=f'<rect x="0" y="214" width="390" height="630" fill="{col[1]}"/>'
    g+=''.join(f'<ellipse cx="{r.randint(0,390)}" cy="{r.randint(240,830)}" rx="{r.randint(40,74)}" ry="{r.randint(14,24)}" fill="{col[0]}" opacity=".5"/>' for _ in range(7))
    return g
def tufts(pts): return ''.join(tuft3(x,y) for x,y in pts)
SKYNOSUN=f'<rect x="0" y="0" width="390" height="214" fill="#a9c3cf"/><rect x="0" y="0" width="390" height="90" fill="#9cb8c8"/>'
SKYBASE=f'<rect x="0" y="0" width="390" height="214" fill="#a9c3cf"/><rect x="0" y="0" width="390" height="90" fill="#9cb8c8"/><circle cx="334" cy="92" r="30" fill="{Q["mustard"]}" opacity=".22"/><circle cx="334" cy="92" r="20" fill="{Q["mustard"]}"/>'
def gate_arch(x=164,w=62,col=None):
    col=col or (Q["brown"],Q["brown2"])
    return f'<path d="M{x} 214 L{x} 150 C{x} 118 {x+w} 118 {x+w} 150 L{x+w} 214 Z" fill="{col[0]}"/><path d="M{x+w/2} 122 C{x+w-12} 124 {x+w} 136 {x+w} 150 L{x+w} 214 L{x+w/2} 214 Z" fill="{col[1]}"/><rect x="{x}" y="160" width="{w}" height="4" fill="{col[1]}"/><rect x="{x}" y="188" width="{w}" height="4" fill="{col[1]}"/>'
# ---------- ORCHARD
def ladder3(x,y,h=70,rot=12):
    rungs=''.join(f'<rect x="2" y="{yy}" width="20" height="4" rx="1" fill="{WOOD[1]}"/>' for yy in range(8,h-4,13))
    return f'<g transform="translate({x} {y}) rotate({rot})">{shadow(12,h+2,16,4)}<rect x="0" y="0" width="5" height="{h}" rx="2" fill="{WOOD[0]}"/><rect x="19" y="0" width="5" height="{h}" rx="2" fill="{WOOD[1]}"/>{rungs}</g>'
def apple_crate(x,y,c=None):
    c=c or (Q["coral"],Q["coral2"])
    w,d,h=46,24,18
    fill=''.join(f'<circle cx="{ax}" cy="{ay}" r="5.5" fill="{c[0]}"/><path d="M{ax} {ay-5.5} A5.5 5.5 0 0 1 {ax+5.5} {ay} A5.5 5.5 0 0 1 {ax+2} {ay+5} A6 6 0 0 0 {ax+3} {ay} Z" fill="{c[1]}"/>' for ax,ay in ((9,8),(20,7),(31,8),(40,10),(14,16),(26,16),(37,17)))
    return f'<g transform="translate({x} {y})">{shadow(w/2,d+h+1,w/2+4,6)}<rect x="0" y="{d-2}" width="{w}" height="{h}" rx="2" fill="{WOOD[1]}"/><rect x="0" y="{d+6}" width="{w}" height="2.5" fill="{WOOD[2]}"/><rect x="{w-8}" y="{d-2}" width="8" height="{h}" fill="{WOOD[2]}"/><rect x="0" y="0" width="{w}" height="{d}" rx="3" fill="{WOOD[2]}"/><rect x="3" y="3" width="{w-6}" height="{d-6}" rx="2" fill="#4a2e1c"/>{fill}</g>'
def cart(x,y,load='apples'):
    w,d=96,40
    wheel=lambda cx,cy: f'<circle cx="{cx}" cy="{cy}" r="17" fill="{WOOD[2]}"/><circle cx="{cx}" cy="{cy}" r="12" fill="{WOOD[1]}"/><path d="M{cx-12} {cy} L{cx+12} {cy} M{cx} {cy-12} L{cx} {cy+12}" stroke="{WOOD[2]}" stroke-width="3"/><circle cx="{cx}" cy="{cy}" r="4" fill="{WOOD[2]}"/>'
    if load=='apples':
        top=''.join(f'<circle cx="{ax}" cy="{ay}" r="7" fill="{Q["coral"] if (ax+ay)%3 else Q["mustard"]}"/><path d="M{ax} {ay-7} A7 7 0 0 1 {ax+7} {ay} A7 7 0 0 1 {ax+2} {ay+6.6} A8 8 0 0 0 {ax+3} {ay} Z" fill="{Q["coral2"] if (ax+ay)%3 else Q["mustard2"]}"/>' for ax,ay in ((14,12),(28,8),(42,12),(56,8),(70,12),(82,14),(20,24),(36,22),(50,24),(64,22),(78,26)))
    else:
        top=f'<rect x="6" y="2" width="{w-12}" height="{d-6}" rx="4" fill="#e6c47a"/><rect x="{w-30}" y="2" width="24" height="{d-6}" rx="4" fill="#c9a457"/>'+''.join(f'<path d="M{10+k*12} 8 l6 4" stroke="#c9a457" stroke-width="2" stroke-linecap="round"/>' for k in range(6))
    return f'''<g transform="translate({x} {y})">{shadow(w/2+4,d+30,w/2+14,8)}<rect x="{w-2}" y="{d-4}" width="40" height="5" rx="2" fill="{WOOD[1]}" transform="rotate(8 {w} {d})"/>
      <rect x="0" y="{d-6}" width="{w}" height="18" rx="2" fill="{WOOD[1]}"/><rect x="0" y="{d+2}" width="{w}" height="3" fill="{WOOD[2]}"/><rect x="0" y="0" width="{w}" height="{d}" rx="4" fill="{WOOD[2]}"/><rect x="4" y="4" width="{w-8}" height="{d-8}" rx="3" fill="#4a2e1c"/>{top}{wheel(22,d+16)}{wheel(w-22,d+16)}</g>'''
def well(x,y):
    stones=''.join(f'<rect x="{2+(r%2)*8+k*16}" y="{40+r*11}" width="13" height="9" rx="2" fill="#a39c8f"/>' for r in range(2) for k in range(4) if 2+(r%2)*8+k*16<58)
    return f'''<g transform="translate({x} {y})">{shadow(32,66,38,8)}<rect x="0" y="36" width="64" height="28" rx="4" fill="#857e72"/>{stones}<rect x="44" y="36" width="20" height="28" rx="4" fill="#6e675d" opacity=".8"/>
      <ellipse cx="32" cy="36" rx="32" ry="10" fill="#a39c8f"/><ellipse cx="32" cy="36" rx="24" ry="6.5" fill="#2e3a40"/>
      <rect x="4" y="-4" width="6" height="42" fill="{WOOD[1]}"/><rect x="54" y="-4" width="6" height="42" fill="{WOOD[2]}"/><rect x="8" y="10" width="48" height="4" fill="{WOOD[2]}"/>
      <path d="M-6 0 L32 -22 L70 0 Z" fill="{Q["coral"]}"/><path d="M32 -22 L70 0 L50 0 Z" fill="{Q["coral2"]}"/><rect x="-6" y="-2" width="76" height="5" rx="2" fill="{WOOD[2]}"/>
      <rect x="29" y="14" width="2" height="12" fill="{DARK}"/><path d="M24 26 L38 26 L36 36 L26 36 Z" fill="{WOOD[1]}"/></g>'''
def pear_tree(x,y,s=1):
    t=tree3(0,0,1,False).replace(Q['green'],'#6a9a4a').replace(Q['green2'],'#557d3a')
    pears=''.join(f'<path d="M{px} {py} q-5 6 0 10 q5 -4 0 -10 Z" fill="{Q["mustard"]}"/><ellipse cx="{px}" cy="{py+7}" rx="4.6" ry="5" fill="{Q["mustard"]}"/><ellipse cx="{px+2}" cy="{py+7}" rx="2.6" ry="5" fill="{Q["mustard2"]}"/>' for px,py in ((28,36),(58,18),(66,44),(44,52)))
    return f'<g transform="translate({x} {y}) scale({s})">{t}{pears}</g>'
def orchard():
    sky=SKYBASE+cloud(36,64)+cloud(236,58,.7)+f'<path d="M-10 170 Q90 136 200 156 Q300 130 400 150 L400 214 L-10 214 Z" fill="#7d9a8c"/>'
    sky+=''.join(f'<g transform="translate({tx} {ty}) scale(.42)">{tree3(0,0,1,True)}</g>' for tx,ty in ((-6,124),(36,118),(78,126),(250,124),(292,118),(334,126)))
    sky+=f'<rect x="150" y="122" width="90" height="92" fill="{Q["tan"]}"/>'+''.join(f'<rect x="{150+k*15}" y="122" width="11" height="92" rx="1" fill="{WOOD[0] if k%2==0 else WOOD[1]}"/>' for k in range(6))+f'<path d="M144 126 L195 100 L246 126 Z" fill="{Q["coral"]}"/><path d="M195 100 L246 126 L222 126 Z" fill="{Q["coral2"]}"/>'+gate_arch(166,58,(WOOD[1],WOOD[2]))
    sky+=f'<path d="M-10 198 Q80 180 150 196 L150 214 L-10 214 Z" fill="{Q["green2"]}"/><path d="M240 196 Q320 176 400 192 L400 214 L240 214 Z" fill="{Q["green2"]}"/>'
    g=grass_ground(11)
    props=''.join([tree3(10,214,.82,True), ladder3(96,250,64,14), apple_crate(140,270),
        apple_crate(326,236,(Q["mustard"],Q["mustard2"])),
        cart(262,404), rock(198,424,.75),
        pear_tree(-10,494,.8), apple_crate(78,600), apple_crate(30,626),
        tree3(292,562,.9,True), well(290,700) if False else '', well(298,730),
        tree3(-20,690,.85,True), flower_patch(220,760,Q["cream"],Q["cream2"])])
    fallen=''.join(f'<circle cx="{ax}" cy="{ay}" r="4.6" fill="{Q["coral"]}"/><circle cx="{ax-1.4}" cy="{ay-1.4}" r="1.4" fill="{Q["pink"]}"/>' for ax,ay in ((70,334),(186,250),(110,474),(240,672),(354,516)))
    return page('Orchard','5/20',21,GR[1],g,sky,road_dirt(),tufts([(160,316),(176,326),(342,316),(206,480),(30,440),(150,606),(232,806),(250,816),(352,676)])+props+fallen,
                butterfly(206,560,Q["cream"],Q["cream2"])+butterfly(112,380,Q["pink"],Q["pink2"]))
# ---------- STABLES
YARD=('#d6b27a','#c9a46a','#b08c56')
def yard_ground(seed):
    r=random.Random(seed)
    g=f'<rect x="0" y="214" width="390" height="630" fill="{YARD[1]}"/>'
    g+=''.join(f'<ellipse cx="{r.randint(0,390)}" cy="{r.randint(240,830)}" rx="{r.randint(30,60)}" ry="{r.randint(10,18)}" fill="{YARD[0]}" opacity=".7"/>' for _ in range(8))
    g+=''.join(f'<path d="M{x} {y} l9 -3 M{x+4} {y+4} l10 1 M{x+2} {y-4} l8 4" stroke="#e6c47a" stroke-width="2" stroke-linecap="round"/>' for x,y in ((60,330),(200,470),(330,560),(50,700),(250,800),(320,300),(150,620)))
    return g
def horse_stall(x,y,coat=('#9a6a42','#7d5030'),mane='#4a2e1c'):
    w=96
    door=f'<rect x="0" y="40" width="{w}" height="40" fill="{WOOD[1]}"/><rect x="{w-14}" y="40" width="14" height="40" fill="{WOOD[2]}"/>'+''.join(f'<rect x="{6+k*18}" y="44" width="2" height="34" fill="{WOOD[2]}"/>' for k in range(5))+f'<path d="M4 44 L{w-18} 76 M4 76 L{w-18} 44" stroke="{WOOD[2]}" stroke-width="3"/>'
    head=f'''<g transform="translate(32 6)"><path d="M6 36 L10 8 Q18 -2 28 6 L34 36 Z" fill="{coat[0]}"/><path d="M22 2 Q30 4 30 12 L34 36 L24 36 Z" fill="{coat[1]}"/><path d="M4 10 Q10 -6 20 0 L10 22 Z" fill="{mane}"/>
      <path d="M12 0 L14 -8 L18 0 Z" fill="{coat[1]}"/><path d="M22 2 L26 -6 L28 4 Z" fill="{coat[1]}"/><rect x="12" y="24" width="18" height="14" rx="7" fill="#c9a07a"/><circle cx="17" cy="31" r="1.6" fill="{DARK}"/><circle cx="25" cy="31" r="1.6" fill="{DARK}"/><ellipse cx="14" cy="14" rx="2.4" ry="3.6" fill="{DARK}"/><ellipse cx="26" cy="14" rx="2.4" ry="3.6" fill="{DARK}"/></g>'''
    return f'<g transform="translate({x} {y})">{shadow(w/2,82,w/2+6,7)}<rect x="0" y="0" width="{w}" height="44" fill="#4a2e1c"/><rect x="-4" y="-4" width="{w+8}" height="8" rx="2" fill="{WOOD[0]}"/>{head}{door}<rect x="-6" y="38" width="{w+12}" height="6" rx="2" fill="{WOOD[0]}"/></g>'
def square_bale(x,y,s=1):
    return f'''<g transform="translate({x} {y}) scale({s})">{shadow(30,36,32,6)}<rect x="0" y="12" width="56" height="22" rx="3" fill="#c9a457"/><rect x="40" y="12" width="16" height="22" rx="3" fill="#b08c40"/><rect x="0" y="0" width="56" height="16" rx="3" fill="#e6c47a"/>
      <rect x="14" y="0" width="3" height="34" fill="#a87a42"/><rect x="38" y="0" width="3" height="34" fill="#a87a42"/>{''.join(f'<path d="M{6+k*8} 6 l5 3" stroke="#c9a457" stroke-width="1.6" stroke-linecap="round"/>' for k in range(6))}</g>'''
def trough(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(40,40,44,6)}<rect x="6" y="28" width="6" height="12" fill="{WOOD[2]}"/><rect x="68" y="28" width="6" height="12" fill="{WOOD[2]}"/><path d="M0 8 L80 8 L74 30 L6 30 Z" fill="{WOOD[1]}"/><path d="M62 8 L80 8 L74 30 L60 30 Z" fill="{WOOD[2]}"/>
      <rect x="0" y="2" width="80" height="12" rx="3" fill="{WOOD[0]}"/><rect x="4" y="5" width="72" height="7" rx="2" fill="#6f9bb3"/><rect x="50" y="5" width="26" height="7" rx="2" fill="#5a879f"/></g>'''
def chicken(x,y,c='#f1e3c2',c2='#e0cb9c'):
    return f'''<g transform="translate({x} {y})">{shadow(12,22,11,3)}<rect x="9" y="16" width="2" height="6" fill="{Q["mustard2"]}"/><rect x="14" y="16" width="2" height="6" fill="{Q["mustard2"]}"/><ellipse cx="12" cy="11" rx="11" ry="8" fill="{c}"/><path d="M12 4 Q22 6 22 12 Q20 18 12 19 Q18 12 12 4 Z" fill="{c2}"/><path d="M0 6 L-2 0 L4 4 Z" fill="{c2}"/>
      <circle cx="21" cy="3" r="5" fill="{c}"/><path d="M19 -2 l2 -3 l2 3 Z" fill="{Q["coral"]}"/><path d="M25 3 L29 4 L25 6 Z" fill="{Q["mustard"]}"/><circle cx="22" cy="2" r="1.2" fill="{DARK}"/></g>'''
def pitchfork(x,y): return f'<g transform="translate({x} {y}) rotate(16)">{shadow(8,72,12,3)}<rect x="6" y="14" width="4" height="58" rx="2" fill="{WOOD[0]}"/><path d="M0 0 L0 14 L16 14 L16 0 M8 0 L8 14" stroke="#8a8794" stroke-width="2.6" fill="none"/></g>'
def stables():
    sky=SKYBASE+cloud(30,62,.8)
    sky+=f'<path d="M-10 172 Q90 140 200 160 Q300 136 400 154 L400 214 L-10 214 Z" fill="#7d9a8c"/>'
    barn=f'<rect x="96" y="96" width="198" height="118" fill="{Q["coral"]}"/><rect x="250" y="96" width="44" height="118" fill="{Q["coral2"]}"/>'+''.join(f'<rect x="{100+k*14}" y="98" width="2" height="116" fill="{Q["coral2"]}" opacity=".6"/>' for k in range(11))
    barn+=f'<path d="M86 100 L195 46 L304 100 Z" fill="#6e3a2a"/><path d="M195 46 L304 100 L268 100 Z" fill="#552c20"/><rect x="84" y="96" width="222" height="7" rx="2" fill="{Q["cream"]}"/>'
    barn+=f'<rect x="176" y="62" width="38" height="28" fill="{Q["cream"]}"/><rect x="180" y="66" width="30" height="20" fill="#4a2e1c"/><path d="M180 66 L210 86 M210 66 L180 86" stroke="{Q["cream"]}" stroke-width="2.4"/>'
    barn+=f'<rect x="156" y="124" width="78" height="90" fill="{Q["cream"]}"/><rect x="161" y="129" width="68" height="85" fill="#4a2e1c"/><path d="M161 129 L229 214 M229 129 L161 214" stroke="{Q["cream2"]}" stroke-width="3" opacity=".0"/>'
    barn+=f'<g transform="translate(161 129)"><rect x="0" y="0" width="22" height="85" fill="{WOOD[1]}"/><path d="M0 0 L22 40 M22 0 L0 40" stroke="{WOOD[2]}" stroke-width="3"/><rect x="46" y="0" width="22" height="85" fill="{WOOD[2]}"/><path d="M46 0 L68 40 M68 0 L46 40" stroke="#5a3a24" stroke-width="3"/></g>'
    barn+=f'<rect x="108" y="132" width="30" height="26" fill="{Q["cream"]}"/><rect x="112" y="136" width="22" height="18" fill="#4a2e1c"/><rect x="252" y="132" width="30" height="26" fill="{Q["cream2"]}"/><rect x="256" y="136" width="22" height="18" fill="#4a2e1c"/>'
    sky+=barn+f'{fence3(-4,180,3)}{fence3(312,180,3)}'
    g=yard_ground(21)
    props=''.join([horse_stall(18,236), square_bale(130,282,.9),
        chicken(330,240), chicken(350,262,'#c9783a','#a65e2a'),
        trough(268,412), pitchfork(236,402),
        square_bale(16,520), square_bale(60,548,.9), square_bale(30,500,.85) if False else '', chicken(110,540,'#c9783a','#a65e2a'),
        horse_stall(282,580,('#e6d3b0','#cdb48c'),'#857e72') if False else '', cart(286,606,'hay') if False else '',
        trough(300,610) if False else '', well(306,600) if False else '',
        cart(262,720,'hay'), sack(14,610), sack(46,624,Q["mustard"],.9),
        bucket(330,620), chicken(318,664), fence3(-4,770,3)])
    return page('Stables','5/20',41,YARD[1],g,sky,road_planks(),props)
# ---------- MOAT BRIDGE: the ground is water, the path is a boardwalk on posts, banks are islands of reeds
WATER=('#6f9bb3','#5a879f','#4f6f86')
def lily(x,y,s=1,flower=True):
    f=f'<circle cx="10" cy="4" r="4" fill="{Q["pink"]}"/><circle cx="10" cy="4" r="1.6" fill="{Q["mustard"]}"/>' if flower else ''
    return f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="10" cy="8" rx="13" ry="7" fill="{Q["green"]}"/><path d="M10 8 L23 6 L22 11 Z" fill="{WATER[0]}"/><path d="M10 8 A13 7 0 0 0 20 13 L10 8 Z" fill="{Q["green2"]}"/>{f}</g>'
def reeds3(x,y,s=1):
    stems=''.join(f'<rect x="{rx}" y="{ry}" width="3" height="{36-ry}" rx="1.5" fill="{Q["green2"] if i%2 else Q["green"]}"/><ellipse cx="{rx+1.5}" cy="{ry+3}" rx="3.2" ry="8" fill="{Q["brown"] if i%2 else Q["brown2"]}"/>' for i,(rx,ry) in enumerate(((4,6),(12,0),(20,8),(28,2),(36,10))))
    return f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="22" cy="38" rx="26" ry="7" fill="{GR[2]}"/><ellipse cx="22" cy="36" rx="24" ry="6" fill="{GR[1]}"/>{stems}</g>'
def bank(x,y,w,h):
    return f'<g transform="translate({x} {y})"><ellipse cx="{w/2}" cy="{h/2+5}" rx="{w/2}" ry="{h/2}" fill="#3f5f6a"/><ellipse cx="{w/2}" cy="{h/2}" rx="{w/2}" ry="{h/2}" fill="{GR[1]}"/><ellipse cx="{w/2-8}" cy="{h/2-4}" rx="{w/2-16}" ry="{h/2-8}" fill="{GR[0]}" opacity=".55"/></g>'
def rowboat(x,y):
    return f'''<g transform="translate({x} {y}) rotate(-14 40 16)"><ellipse cx="40" cy="22" rx="42" ry="9" fill="{WATER[2]}"/><path d="M0 12 Q40 -2 80 12 Q74 30 40 32 Q6 30 0 12 Z" fill="{WOOD[1]}"/><path d="M40 32 Q74 30 80 12 L70 14 Q66 26 40 28 Z" fill="{WOOD[2]}"/>
      <path d="M6 13 Q40 2 74 13 Q68 24 40 25 Q12 24 6 13 Z" fill="{WOOD[0]}"/><rect x="34" y="6" width="8" height="20" fill="{WOOD[1]}"/><rect x="58" y="14" width="40" height="3" rx="1.5" fill="{WOOD[2]}" transform="rotate(20 58 14)"/></g>'''
def fish(x,y): return f'<g transform="translate({x} {y})"><ellipse cx="8" cy="4" rx="8" ry="4" fill="{Q["orange"]}" opacity=".8"/><path d="M15 4 L22 0 L22 8 Z" fill="{Q["orange2"]}" opacity=".8"/></g>'
def frog(x,y):
    return f'<g transform="translate({x} {y})"><ellipse cx="10" cy="10" rx="10" ry="7" fill="{Q["green"]}"/><path d="M10 3 A10 7 0 0 1 20 10 A10 7 0 0 1 14 16 Q18 10 10 3 Z" fill="{Q["green2"]}"/><circle cx="5" cy="3" r="3.4" fill="{Q["green"]}"/><circle cx="14" cy="3" r="3.4" fill="{Q["green"]}"/><circle cx="5" cy="3" r="1.4" fill="{DARK}"/><circle cx="14" cy="3" r="1.4" fill="{DARK}"/></g>'
def moat():
    sky=SKYNOSUN+cloud(40,60,.8)
    sky+=f'<path d="M-10 180 Q80 150 150 170 L150 214 L-10 214 Z" fill="#7d9a8c"/><path d="M240 170 Q320 150 400 166 L400 214 L240 214 Z" fill="#7d9a8c"/>'
    wall=f'<rect x="0" y="70" width="390" height="144" fill="{Q["lav"]}"/>'+stones(390,144,9).replace('<rect','<rect transform="translate(0 70)"',0)
    wall=f'<rect x="0" y="80" width="390" height="134" fill="{Q["lav"]}"/><g transform="translate(0 80)">{stones(390,134,9)}</g>'+''.join(f'<rect x="{k*30}" y="66" width="20" height="18" rx="2" fill="{Q["lav"]}"/>' for k in range(13))
    wall+=f'<rect x="300" y="40" width="70" height="174" fill="{Q["lav2"]}"/>'+''.join(f'<rect x="{300+k*18}" y="28" width="12" height="16" rx="2" fill="{Q["lav2"]}"/>' for k in range(4))+f'<rect x="326" y="80" width="12" height="22" rx="6" fill="{DARK}"/>'
    wall+=f'<rect x="20" y="40" width="70" height="174" fill="{Q["lav"]}"/><rect x="66" y="40" width="24" height="174" fill="{Q["lav2"]}"/>'+''.join(f'<rect x="{20+k*18}" y="28" width="12" height="16" rx="2" fill="{Q["lav"] if k<3 else Q["lav2"]}"/>' for k in range(4))+f'<rect x="48" y="80" width="12" height="22" rx="6" fill="{DARK}"/>'
    wall+=f'<rect x="156" y="108" width="78" height="106" fill="{Q["lav2"]}"/>'+gate_arch(164,62)+''.join(f'<rect x="{168+k*12}" y="124" width="3" height="40" fill="{DARK}" opacity=".7"/>' for k in range(5))
    wall+=f'<rect x="0" y="200" width="390" height="16" fill="#a39c8f"/><rect x="0" y="212" width="390" height="6" fill="#857e72"/>'+''.join(f'<rect x="{k*36}" y="200" width="2" height="12" fill="#857e72"/>' for k in range(11))
    g=f'<rect x="0" y="214" width="390" height="630" fill="{WATER[0]}"/>'+''.join(f'<path d="M{wx} {wy} q8 -4 16 0" stroke="#a9cbe0" stroke-width="2.4" fill="none" stroke-linecap="round"/>' for wx,wy in ((40,300),(300,330),(180,470),(60,580),(330,520),(240,790),(40,760),(140,690)))
    g+=''.join(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{WATER[1]}" opacity=".6"/>' for cx,cy,rx,ry in ((80,400,60,18),(300,700,70,20),(200,300,50,14)))
    posts=''
    for k in range(0,len(G['pts'])):
        px,py=G['pts'][k]; posts+=f'<rect x="{px-26}" y="{py+8}" width="6" height="16" fill="{WOOD[2]}"/><rect x="{px+20}" y="{py+8}" width="6" height="16" fill="{WOOD[2]}"/>'
    props=''.join([bank(4,232,150,86), reeds3(16,236), rock(100,276,.8), frog(70,290),
        lily(330,244), lily(350,276,.8,False), bank(300,302,100,60), reeds3(330,300,.8),
        rowboat(262,420), lily(220,452,.9), fish(330,470),
        bank(-20,520,140,96), reeds3(6,520), rock(70,572,.9), flower_patch(30,590,Q["cream"],Q["cream2"]),
        lily(120,640,.9), lily(296,640), fish(340,602), frog(304,636),
        bank(240,720,170,110), reeds3(330,724), rock(270,770,.8), bush3(300,770,.8,Q["pink"]),
        bank(-30,760,140,90), reeds3(10,772,.9), lily(140,820,.8)])
    return page('Moat bridge','5/20',61,WATER[0],g,sky+wall,posts+road_planks(),props)
# ---------- GATE: a camp in front of the gatehouse
def tent(x,y,c,c2):
    return f'''<g transform="translate({x} {y})">{shadow(44,62,50,9)}<path d="M0 60 L40 2 L44 2 L88 60 Z" fill="{c}"/><path d="M44 2 L88 60 L60 60 Z" fill="{c2}"/>{''.join(f'<path d="M{8+k*16} 60 L42 2" stroke="{Q["cream"]}" stroke-width="5" opacity=".75"/>' for k in range(0,3))}
      <path d="M30 60 L42 24 L54 60 Z" fill="#4a2e1c"/><path d="M42 24 L54 60 L46 60 Z" fill="#2e1c14"/><rect x="41" y="-12" width="2.4" height="16" fill="{DARK}"/><path d="M43 -12 L58 -7 L43 -2 Z" fill="{Q["mustard"]}"/></g>'''
def shield_stand(x,y):
    sh=lambda sx,c,c2: f'<g transform="translate({sx} 6)"><path d="M0 0 L22 0 L22 14 Q22 26 11 30 Q0 26 0 14 Z" fill="{c}"/><path d="M11 0 L22 0 L22 14 Q22 26 11 30 Z" fill="{c2}"/><rect x="9" y="4" width="4" height="20" fill="{Q["cream"]}" opacity=".85"/></g>'
    return f'<g transform="translate({x} {y})">{shadow(36,46,40,6)}<rect x="2" y="4" width="66" height="5" rx="2" fill="{WOOD[0]}"/><rect x="4" y="4" width="5" height="42" fill="{WOOD[1]}"/><rect x="60" y="4" width="5" height="42" fill="{WOOD[2]}"/>{sh(8,Q["navy"],Q["navy2"])}{sh(36,Q["coral"],Q["coral2"])}</g>'
def campfire(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(22,30,26,6)}{''.join(f'<ellipse cx="{22+18*math.cos(a)}" cy="{22+8*math.sin(a)}" rx="5" ry="3.6" fill="#a39c8f"/>' for a in [i*math.pi/4 for i in range(8)])}
      <rect x="8" y="18" width="28" height="6" rx="3" fill="{WOOD[1]}" transform="rotate(20 22 21)"/><rect x="8" y="18" width="28" height="6" rx="3" fill="{WOOD[2]}" transform="rotate(-20 22 21)"/>
      <path d="M14 22 C10 10 20 6 22 -4 C26 8 34 10 30 22 Z" fill="{Q["mustard"]}"/><path d="M18 22 C16 14 22 10 22 6 C26 12 28 16 26 22 Z" fill="{Q["coral"]}"/></g>'''
def pine(x,y,s=1):
    return f'''<g transform="translate({x} {y}) scale({s})">{shadow(30,92,30,8)}<rect x="26" y="70" width="8" height="22" fill="{Q["brown"]}"/><rect x="30" y="70" width="4" height="22" fill="{Q["brown2"]}"/>
      <path d="M0 76 L30 30 L60 76 Z" fill="{Q["green"]}"/><path d="M30 30 L60 76 L40 76 Z" fill="{Q["green2"]}"/><path d="M6 52 L30 12 L54 52 Z" fill="{Q["green"]}"/><path d="M30 12 L54 52 L38 52 Z" fill="{Q["green2"]}"/><path d="M12 30 L30 0 L48 30 Z" fill="{Q["green"]}"/><path d="M30 0 L48 30 L36 30 Z" fill="{Q["green2"]}"/></g>'''
def gate():
    sky=SKYNOSUN+cloud(30,60,.7)
    gh=f'<rect x="0" y="96" width="390" height="118" fill="{Q["lav"]}"/><g transform="translate(0 96)">{stones(390,118,13)}</g>'+''.join(f'<rect x="{k*30}" y="82" width="20" height="18" rx="2" fill="{Q["lav"]}"/>' for k in range(13))
    for tx in (96,236):
        gh+=f'<rect x="{tx}" y="40" width="58" height="174" fill="{Q["lav"]}"/><rect x="{tx+38}" y="40" width="20" height="174" fill="{Q["lav2"]}"/>'+''.join(f'<rect x="{tx+k*16}" y="28" width="11" height="16" rx="2" fill="{Q["lav"] if k<3 else Q["lav2"]}"/>' for k in range(4))+f'<rect x="{tx+22}" y="66" width="12" height="24" rx="6" fill="{DARK}"/>'
        gh+=f'<rect x="{tx+27}" y="0" width="3" height="30" fill="{DARK}"/><path d="M{tx+30} 2 L{tx+54} 9 L{tx+30} 17 Z" fill="{Q["coral"]}"/>'
        gh+=f'<rect x="{tx+8}" y="104" width="34" height="58" fill="{Q["navy"]}"/><rect x="{tx+28}" y="104" width="14" height="58" fill="{Q["navy2"]}"/><path d="M{tx+8} 162 L{tx+25} 174 L{tx+42} 162 Z" fill="{Q["navy"]}"/><path d="M{tx+25} 116 l6 10 l-6 10 l-6 -10 Z" fill="{Q["mustard"]}"/>'
    gh+=f'<rect x="154" y="106" width="82" height="108" fill="{Q["lav2"]}"/><path d="M164 214 L164 150 C164 118 226 118 226 150 L226 214 Z" fill="#2e1c14"/>'+''.join(f'<rect x="{168+k*11}" y="126" width="3" height="56" fill="#5a5664"/>' for k in range(6))+''.join(f'<rect x="164" y="{136+k*14}" width="62" height="3" fill="#5a5664"/>' for k in range(4))+''.join(f'<path d="M{170+k*11} 182 l1.5 6 l1.5 -6 Z" fill="#5a5664"/>' for k in range(6))
    sky+=gh+f'{pine(-14,148,.9)}{pine(334,152,.85)}'
    g=grass_ground(31,('#9aa860','#8a9a52','#6f7d40'))
    g+=f'<ellipse cx="195" cy="500" rx="190" ry="300" fill="#b39a68" opacity=".18"/>'
    props=''.join([tent(16,236,Q["coral"],Q["coral2"]), barrel(122,272,.85),
        shield_stand(310,226) if False else '', barrel(330,238,.8), keg(320,300) if False else '',
        tent(280,394,Q["navy"],Q["navy2"]), campfire(198,424),
        shield_stand(22,522), apple_crate(92,600,(Q["mustard"],Q["mustard2"])), barrel(30,590,.8),
        pine(300,560,.9), crate(300,648,'carrot') if False else '',
        cart(258,720,'hay'), signpost(42,770), pine(-20,640,.8), rock(340,820,.7)])
    return page('Gate','5/20',81,'#8a9a52',g,sky,road_dirt(),tufts([(160,316),(176,326),(206,480),(150,606),(232,806),(352,676),(40,440),(340,350)])+props)
rooms={'Room-v2-orchard.dc.html':('O2 · Orchard (Kitchens rules)',orchard()),
       'Room-v2-stables.dc.html':('S2 · Stables (Kitchens rules)',stables()),
       'Room-v2-moat.dc.html':('B2 · Moat bridge (Kitchens rules)',moat()),
       'Room-v2-gate.dc.html':('G2 · Gate (Kitchens rules)',gate())}
base='/home/claude/mockups/project'
c=json.load(open(f'{base}/canvas.json'))
ref=c['boards']['Room-v2-meadow.dc.html']; x=ref['x']+ref['w']+80
for fn,(t,body) in rooms.items():
    open(f'{base}/{fn}','w').write(G['HEADQ']%t+body+'\n'+G['TAIL'])
    c['boards'].pop(fn,None); c['order']=[o for o in c['order'] if o!=fn]
    c['boards'][fn]={'x':x,'y':ref['y'],'w':390,'h':844,'title':t}; c['order'].append(fn); x+=470
json.dump(c,open(f'{base}/canvas.json','w'),ensure_ascii=False)
print('ok')
