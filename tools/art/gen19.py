import json, math, random, sys
g18=open('./gen18.py').read()
exec(g18[:g18.index("\nout={}")])
# ================= round 4: dungeon cells hold animals; every other room gets its own path shape
def check(name,dense,pts,props):
    bad=[]
    for i,(svg,(x0,y0,x1,y1)) in enumerate(props):
        dmin=min(math.dist((min(max(px,x0),x1),min(max(py,y0),y1)),(px,py)) for px,py in dense if py>214)
        nmin=min(math.dist((min(max(px,x0),x1),min(max(py,y0),y1)),(px,py)) for px,py in pts)
        if dmin<22 or nmin<24: bad.append((i,round(dmin),round(nmin),(x0,y0,x1,y1)))
    if bad: print(name,'overlaps:',bad)
def P(svg,x,y,w,h): return (svg,(x,y,x+w,y+h))
def J(props): return ''.join(s for s,_ in props)
def ctrl_road(ctrl): return G['crd'](ctrl), bez_pts(ctrl)
def poly_road(poly): return dpoly(poly), poly_pts(poly)
# ---------- dungeon cells: a cat and a dog, wide gap in the bars so the animal is never covered
def animal_body(kind):
    m=re_fill(sv(kind,10))
    return m
import re
def re_fill(s): return re.findall(r'fill="(#[0-9a-fA-F]{6})"',s)
def caged(kind,w,h):
    c1,c2={'cat':('#b5622a','#954d1f'),'dog':None,'lion':('#d9a43a','#b8862a'),'bear':('#8a5432','#6e4126')}.get(kind) or re_fill(sv(kind,10))[:2]
    if kind=='lion':
        bed=f'<g transform="translate({w/2-52} {h-40})"><ellipse cx="52" cy="22" rx="54" ry="14" fill="{Q["coral2"]}"/><ellipse cx="50" cy="18" rx="50" ry="12" fill="{Q["coral"]}"/><ellipse cx="50" cy="18" rx="40" ry="8" fill="none" stroke="{Q["mustard"]}" stroke-width="2" stroke-dasharray="4 4"/></g>'
    else:
        bed=f'<g transform="translate({w/2-52} {h-40})"><ellipse cx="52" cy="22" rx="54" ry="14" fill="#b8924a"/><ellipse cx="50" cy="18" rx="50" ry="12" fill="#d9b46a"/>{"".join(f"<path d=\"M{14+k*12} {14+(k%2)*4} l9 -2\" stroke=\"#b8924a\" stroke-width=\"1.8\" stroke-linecap=\"round\"/>" for k in range(7))}</g>'
    body=f'<g transform="translate({w/2-40} {h-58})"><ellipse cx="44" cy="30" rx="34" ry="16" fill="{c1}"/><path d="M44 14 A34 16 0 0 1 78 30 A34 16 0 0 1 56 45 Q70 32 44 14 Z" fill="{c2}"/>{'' if kind=='bear' else f'<path d="M76 34 Q96 30 90 14" stroke="{c1}" stroke-width="7" fill="none" stroke-linecap="round"/>'}{'<circle cx="90" cy="12" r="6" fill="#954d1f"/>' if kind=='lion' else ''}</g>'
    head=f'<g transform="translate({w/2-46} {h-84})">{sv(kind,58)}</g>'
    honey=f'<g transform="translate({w-40} {h-34})"><path d="M2 10 Q0 30 12 32 L24 32 Q36 30 34 10 Z" fill="{Q["mustard"]}"/><path d="M22 10 L34 10 Q36 30 24 32 L20 32 Q26 22 22 10 Z" fill="{Q["mustard2"]}"/><rect x="0" y="4" width="36" height="8" rx="3" fill="{Q["cream"]}"/><path d="M8 12 q2 8 6 0" fill="{Q["mustard2"]}"/><rect x="10" y="16" width="16" height="9" rx="2" fill="{Q["cream"]}"/></g>'
    if kind=='bear': return bed+body+head+honey
    extra=(f'<g transform="translate({w-40} {h-22})"><ellipse cx="12" cy="10" rx="12" ry="5" fill="{WOOD[2]}"/><ellipse cx="12" cy="7" rx="12" ry="5" fill="{WOOD[1]}"/><ellipse cx="12" cy="6" rx="8" ry="3" fill="#6f9bb3"/></g>' if kind in ('cat','lion')
           else f'<g transform="translate({w-44} {h-18}) rotate(-12)"><rect x="4" y="2" width="22" height="6" rx="3" fill="{Q["cream"]}"/><circle cx="4" cy="2" r="4" fill="{Q["cream"]}"/><circle cx="4" cy="8" r="4" fill="{Q["cream"]}"/><circle cx="26" cy="2" r="4" fill="{Q["cream2"]}"/><circle cx="26" cy="8" r="4" fill="{Q["cream2"]}"/></g>')
    return bed+body+head+extra
def cell3(x,y,w,h,kind):
    back=f'<rect x="0" y="-10" width="{w}" height="{h+10}" fill="#6a6672"/><rect x="0" y="-10" width="{w}" height="12" fill="#55515e"/>'+''.join(f'<rect x="{6+(r%2)*14+k*28}" y="{6+r*22}" width="22" height="16" rx="3" fill="#77737f"/>' for r in range(int(h/22)) for k in range(int(w/28)+1) if 6+(r%2)*14+k*28<w-18 and 6+r*22<h-18)
    xs=[w*f for f in (1/7,2/7,5/7,6/7)]
    bars=''.join(f'<rect x="{bx-2}" y="-10" width="4" height="{h+10}" fill="#b4b1be"/><rect x="{bx+0.6}" y="-10" width="1.4" height="{h+10}" fill="#7d7a86"/>' for bx in xs)
    frame=f'<rect x="-3" y="-14" width="{w+6}" height="7" rx="2" fill="#b4b1be"/><rect x="-3" y="{h-3}" width="{w+6}" height="7" rx="2" fill="#8a8794"/><rect x="-4" y="-14" width="7" height="{h+15}" fill="#b4b1be"/><rect x="{w-3}" y="-14" width="7" height="{h+15}" fill="#7d7a86"/>'
    lock=f'<g transform="translate({xs[2]+6} {h*0.3})"><path d="M2 0 v-4 a5 5 0 0 1 10 0 v4" stroke="{Q["mustard2"]}" stroke-width="2.4" fill="none"/><rect x="0" y="0" width="14" height="14" rx="2" fill="{Q["mustard"]}"/><rect x="6" y="4" width="2" height="6" fill="{DARK}"/></g>'
    return f'<g transform="translate({x} {y})">{shadow(w/2,h+6,w/2+8,7)}{back}{caged(kind,w,h)}{bars}{frame}{lock}</g>'
def dungeon4():
    poly=[(300,880),(300,724),(74,724),(74,544),(316,544),(316,368),(196,368),(196,196)]
    d,dense=poly_road(poly); pts=sample(dense,10,.1,.84)
    wall=indoor_wall('#6a6672','#55515e',33).replace('fill="#978f83" opacity=".45"','fill="#7a7682" opacity=".8"')
    wall+=f'<g transform="translate(286 70)"><rect x="-6" y="-6" width="62" height="38" rx="4" fill="{DSTONE[2]}"/><rect x="0" y="0" width="50" height="26" fill="#9cb8c8"/>'+''.join(f'<rect x="{6+k*10}" y="0" width="3" height="26" fill="#3a3644"/>' for k in range(5))+'</g>'
    wall+=f'<path d="M290 96 L336 96 L380 214 L250 214 Z" fill="#f1e3c2" opacity=".08"/>'+chains_wall(40,96)+chains_wall(100,120)+sconce(132,150)+sconce(246,150)
    wall+=f'<rect x="152" y="106" width="86" height="108" fill="{DSTONE[2]}"/>'+iron_door(164,62,('#5a5664','#4a4652'),True)
    floor=flag_floor(('#3e3a48','#403c4a','#3c3846'),17,'#2e2a36')+FLOORSHADE+SIDE(DSTONE[2])
    floor+=''.join(f'<path d="M{mx} {my} q6 -6 12 0 q6 -4 10 2" fill="{Q["green2"]}" opacity=".8"/>' for mx,my in ((24,500),(350,470),(150,690),(344,780),(20,660)))
    props=[P(bench(22,246),22,246,72,32),P(bucket(110,300),110,300,28,34),P(barrel(240,236,.75),240,236,36,44),P(crate_closed(290,250,44),290,250,50,58),
        P(cell3(112,404,176,104,'lion'),112,390,176,118), P(cell3(112,590,164,100,'bear'),112,576,164,114),
        P(rubble(342,420),342,420,40,30),P(ball_chain(330,640),330,640,40,28),
        P(chest(130,768),130,768,72,56),P(barrel(14,770,.8),14,770,40,46),P(ball_chain(220,790),220,790,40,28),P(rubble(340,780),340,780,40,30)]
    check('dungeon',dense,pts,props)
    return page2('Dungeon','5/20',141,'#2e2a36',floor,wall,path_cobble(d),J(props),pts)
# ---------- MEADOW: two lazy waves (dirt)
def meadow4():
    ctrl=[(110,880),(84,770),(160,700),(296,664),(330,580),(252,512),(120,484),(60,410),(96,330),(170,290),(200,246),(195,196)]
    d,dense=ctrl_road(ctrl); pts=sample(dense,10,.1,.84)
    ground=f'<rect x="0" y="214" width="390" height="630" fill="{GR[1]}"/>'+''.join(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{GR[0]}" opacity=".55"/>' for cx,cy,rx,ry in ((290,300,70,26),(250,420,60,20),(60,600,64,22),(330,760,56,20),(140,820,80,24)))
    props=[P(blanket(236,246),236,240,116,74), P(mush3(326,330,Q["coral"],Q["coral2"]),326,330,50,34),
        P(pond3(184,364),178,364,134,82), P(rock(316,440,.8),316,440,34,22),
        P(skep(14,540),2,530,72,90), P(flower_patch(150,580,Q["pink"],Q["pink2"]),150,580,40,26),
        P(tree3(296,700,.85,True),296,700,82,96),
        P(hay(196,782),196,782,74,52), P(rock(20,690,.9),20,690,38,26), P(signpost(140,790),136,790,52,62), P(tree3(-34,600,.8,False),-34,600,80,90),
        P(flower_patch(186,594,Q["cream"],Q["cream2"]),186,594,40,26), P(bush3(16,240,.8,Q["cream"]),16,240,50,34)]
    check('meadow',dense,pts,props)
    T=tufts([(150,256),(176,262),(340,520),(352,536),(200,620),(30,470),(46,486),(160,690),(232,820),(30,640)])
    F=butterfly(98,620,Q["pink"],Q["pink2"])+butterfly(300,560,Q["cream"],Q["cream2"])
    return page2('Meadow','5/20',1,GR[1],ground+T,SKY,road_dirt_d(d),J(props)+F,pts)
def road_dirt_d(d): return f'<path d="{d}" fill="none" stroke="{Q["tan2"]}" stroke-width="44" stroke-linecap="round" transform="translate(0 3)"/><path d="{d}" fill="none" stroke="{Q["tan"]}" stroke-width="40" stroke-linecap="round"/><path d="{d}" fill="none" stroke="#dcc08e" stroke-width="14" stroke-linecap="round"/>'
def road_ruts(d):   # a mown track with two wheel ruts
    return (f'<path d="{d}" fill="none" stroke="{GR[2]}" stroke-width="46" stroke-linejoin="round" stroke-linecap="round" transform="translate(0 3)"/><path d="{d}" fill="none" stroke="#a4bf6e" stroke-width="42" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="{Q["tan"]}" stroke-width="30" stroke-linejoin="round" stroke-linecap="round"/><path d="{d}" fill="none" stroke="#a4bf6e" stroke-width="12" stroke-linejoin="round" stroke-linecap="round"/>')
def road_cobbles(d):
    return (f'<path d="{d}" fill="none" stroke="#5a5664" stroke-width="46" stroke-linecap="round" stroke-linejoin="round" transform="translate(0 3)"/><path d="{d}" fill="none" stroke="#a39c8f" stroke-width="42" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="#bdb6a9" stroke-width="34" stroke-dasharray="11 4" stroke-linejoin="round"/><path d="{d}" fill="none" stroke="#a39c8f" stroke-width="2" stroke-linejoin="round"/>')
def road_planks_d(d,rope=False):
    s=f'<path d="{d}" fill="none" stroke="#2a140a" stroke-opacity=".2" stroke-width="46" stroke-linejoin="round" transform="translate(0 6)"/><path d="{d}" fill="none" stroke="{WOOD[2]}" stroke-width="46" stroke-linejoin="round"/><path d="{d}" fill="none" stroke="{WOOD[0]}" stroke-width="40" stroke-linejoin="round"/><path d="{d}" fill="none" stroke="{WOOD[1]}" stroke-width="40" stroke-dasharray="2.5 11" stroke-linejoin="round"/>'
    if rope: s+=f'<path d="{d}" fill="none" stroke="#d8b878" stroke-width="48" stroke-dasharray="3 22" stroke-linejoin="round" opacity=".0"/>'
    return s
# ---------- ORCHARD: a farm track in straight diagonal legs (lightning bolt)
def orchard4():
    poly=[(96,880),(96,770),(312,654),(312,610),(80,500),(80,456),(300,350),(300,300),(196,252),(196,196)]
    d,dense=poly_road(poly); pts=sample(dense,10,.1,.86)
    s=SKYBASE+cloud(36,64)+cloud(236,58,.7)+f'<path d="M-10 170 Q90 136 200 156 Q300 130 400 150 L400 214 L-10 214 Z" fill="#7d9a8c"/>'
    s+=''.join(f'<g transform="translate({tx} {ty}) scale(.42)">{tree3(0,0,1,True)}</g>' for tx,ty in ((-6,124),(36,118),(78,126),(250,124),(292,118),(334,126)))
    s+=f'<rect x="150" y="122" width="90" height="92" fill="{Q["tan"]}"/>'+''.join(f'<rect x="{150+k*15}" y="122" width="11" height="92" rx="1" fill="{WOOD[0] if k%2==0 else WOOD[1]}"/>' for k in range(6))+f'<path d="M144 126 L195 100 L246 126 Z" fill="{Q["coral"]}"/><path d="M195 100 L246 126 L222 126 Z" fill="{Q["coral2"]}"/>'+gate_arch(166,58,(WOOD[1],WOOD[2]))
    s+=f'<path d="M-10 198 Q80 180 150 196 L150 214 L-10 214 Z" fill="{Q["green2"]}"/><path d="M240 196 Q320 176 400 192 L400 214 L240 214 Z" fill="{Q["green2"]}"/>'
    g=grass_ground(11)
    props=[P(tree3(14,228,.8,True),14,228,78,90), P(ladder3(96,250,58,12),92,250,30,62), P(apple_crate(120,320),120,320,50,46),
        P(apple_crate(330,236,(Q["mustard"],Q["mustard2"])),330,236,50,46),
        P(cart(222,452),222,452,140,80), P(rock(150,452,.7),150,452,30,20),
        P(pear_tree(-16,560,.7),-16,546,70,80), P(well(124,628),118,606,76,92),
        P(tree3(262,716,.8,True),262,716,78,90), P(apple_crate(320,800),320,800,50,46), P(flower_patch(12,800,Q["cream"],Q["cream2"]),12,800,40,26), P(apple_crate(330,660),330,660,50,46) if False else P('',0,0,0,0)]
    check('orchard',dense,pts,props)
    fallen=''.join(f'<circle cx="{ax}" cy="{ay}" r="4.6" fill="{Q["coral"]}"/><circle cx="{ax-1.4}" cy="{ay-1.4}" r="1.4" fill="{Q["pink"]}"/>' for ax,ay in ((70,334),(200,520),(150,740),(250,820),(354,560)))
    return page2('Orchard','5/20',21,GR[1],g,s,road_ruts(d),J(props)+fallen+butterfly(200,610,Q["cream"],Q["cream2"]),pts)
# ---------- STABLES: vertical hairpins (boardwalk)
def stables4():
    ctrl=[(64,880),(58,720),(56,520),(66,420),(110,382),(154,420),(160,560),(170,680),(214,720),(262,684),(270,540),(282,420),(320,340),(296,270),(236,240),(200,228),(195,196)]
    d,dense=ctrl_road(ctrl); pts=sample(dense,10,.08,.82)
    sky=SKYBASE+cloud(30,62,.8)+f'<path d="M-10 172 Q90 140 200 160 Q300 136 400 154 L400 214 L-10 214 Z" fill="#7d9a8c"/>'
    barn=f'<rect x="96" y="96" width="198" height="118" fill="{Q["coral"]}"/><rect x="250" y="96" width="44" height="118" fill="{Q["coral2"]}"/>'+''.join(f'<rect x="{100+k*14}" y="98" width="2" height="116" fill="{Q["coral2"]}" opacity=".6"/>' for k in range(11))
    barn+=f'<path d="M86 100 L195 46 L304 100 Z" fill="#6e3a2a"/><path d="M195 46 L304 100 L268 100 Z" fill="#552c20"/><rect x="84" y="96" width="222" height="7" rx="2" fill="{Q["cream"]}"/>'
    barn+=f'<rect x="176" y="62" width="38" height="28" fill="{Q["cream"]}"/><rect x="180" y="66" width="30" height="20" fill="#4a2e1c"/><path d="M180 66 L210 86 M210 66 L180 86" stroke="{Q["cream"]}" stroke-width="2.4"/>'
    barn+=f'<rect x="156" y="124" width="78" height="90" fill="{Q["cream"]}"/><rect x="161" y="129" width="68" height="85" fill="#4a2e1c"/>'
    barn+=f'<g transform="translate(161 129)"><rect x="0" y="0" width="22" height="85" fill="{WOOD[1]}"/><path d="M0 0 L22 40 M22 0 L0 40" stroke="{WOOD[2]}" stroke-width="3"/><rect x="46" y="0" width="22" height="85" fill="{WOOD[2]}"/><path d="M46 0 L68 40 M68 0 L46 40" stroke="#5a3a24" stroke-width="3"/></g>'
    barn+=f'<rect x="108" y="132" width="30" height="26" fill="{Q["cream"]}"/><rect x="112" y="136" width="22" height="18" fill="#4a2e1c"/><rect x="252" y="132" width="30" height="26" fill="{Q["cream2"]}"/><rect x="256" y="136" width="22" height="18" fill="#4a2e1c"/>'
    sky+=barn+f'{fence3(-4,180,3)}{fence3(312,180,3)}'
    g=yard_ground(21)
    props=[P(horse_stall(18,240),12,236,108,88), P(chicken(330,236),330,232,30,26), P(chicken(350,264,'#c9783a','#a65e2a'),350,260,30,26),
        P(square_bale(88,520,.68),88,520,39,28), P(pitchfork(196,470),192,470,30,80),
        P(trough(298,520),298,520,80,42), P(chicken(200,600),200,596,30,26),
        P(square_bale(316,420,.8),316,420,46,32), P(bucket(340,470),340,470,28,34), P(horse_stall(290,560,('#e6d3b0','#cdb48c'),'#857e72'),284,556,108,88) if False else P('',0,0,0,0),
        P(cart(240,760,'hay'),240,760,140,80), P(sack(96,766),96,766,44,56), P(sack(130,776,Q["mustard"],.9),130,776,40,50), P(chicken(330,640,'#c9783a','#a65e2a'),330,636,30,26), P(bucket(330,590),330,590,28,34)]
    check('stables',dense,pts,props)
    return page2('Stables','5/20',41,YARD[1],g,sky,road_planks_d(d),J(props),pts)
# ---------- MOAT: straight boardwalk legs that meet on islands
def moat4():
    poly=[(110,880),(110,770),(300,690),(300,560),(84,470),(84,360),(196,300),(196,196)]
    d,dense=poly_road(poly); pts=sample(dense,10,.1,.86)
    sky=SKYNOSUN+cloud(40,60,.8)+f'<path d="M-10 180 Q80 150 150 170 L150 214 L-10 214 Z" fill="#7d9a8c"/><path d="M240 170 Q320 150 400 166 L400 214 L240 214 Z" fill="#7d9a8c"/>'
    wall=f'<rect x="0" y="80" width="390" height="134" fill="{Q["lav"]}"/><g transform="translate(0 80)">{stones(390,134,9)}</g>'+''.join(f'<rect x="{k*30}" y="66" width="20" height="18" rx="2" fill="{Q["lav"]}"/>' for k in range(13))
    wall+=f'<rect x="300" y="40" width="70" height="174" fill="{Q["lav2"]}"/>'+''.join(f'<rect x="{300+k*18}" y="28" width="12" height="16" rx="2" fill="{Q["lav2"]}"/>' for k in range(4))+f'<rect x="326" y="80" width="12" height="22" rx="6" fill="{DARK}"/>'
    wall+=f'<rect x="20" y="40" width="70" height="174" fill="{Q["lav"]}"/><rect x="66" y="40" width="24" height="174" fill="{Q["lav2"]}"/>'+''.join(f'<rect x="{20+k*18}" y="28" width="12" height="16" rx="2" fill="{Q["lav"] if k<3 else Q["lav2"]}"/>' for k in range(4))+f'<rect x="48" y="80" width="12" height="22" rx="6" fill="{DARK}"/>'
    wall+=f'<rect x="156" y="108" width="78" height="106" fill="{Q["lav2"]}"/>'+gate_arch(164,62)+''.join(f'<rect x="{168+k*12}" y="124" width="3" height="40" fill="{DARK}" opacity=".7"/>' for k in range(5))
    wall+=f'<rect x="0" y="200" width="390" height="16" fill="#a39c8f"/><rect x="0" y="212" width="390" height="6" fill="#857e72"/>'+''.join(f'<rect x="{k*36}" y="200" width="2" height="12" fill="#857e72"/>' for k in range(11))
    g=f'<rect x="0" y="214" width="390" height="630" fill="{WATER[0]}"/>'+''.join(f'<path d="M{wx} {wy} q8 -4 16 0" stroke="#a9cbe0" stroke-width="2.4" fill="none" stroke-linecap="round"/>' for wx,wy in ((40,300),(300,330),(180,470),(60,580),(330,520),(240,790),(40,760),(140,690)))
    g+=''.join(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{WATER[1]}" opacity=".6"/>' for cx,cy,rx,ry in ((200,400,60,18),(200,620,70,20),(300,300,50,14)))
    # islands under every corner of the boardwalk
    isl=''.join(bank(cx-w/2,cy-h/2+6,w,h) for cx,cy,w,h in ((110,770,120,70),(300,690,110,64),(300,560,110,64),(84,470,120,70),(84,360,110,64)))
    posts=''.join(f'<rect x="{px-24}" y="{py+12}" width="6" height="14" fill="{WOOD[2]}"/><rect x="{px+18}" y="{py+12}" width="6" height="14" fill="{WOOD[2]}"/>' for px,py in sample(dense,16,.05,.95))
    props=[P(reeds3(30,746,.8),30,746,40,36), P(reeds3(330,664,.8),330,664,40,36), P(frog(330,590),330,590,22,18),
        P(reeds3(20,440,.8),20,440,40,36), P(rock(122,400,.7),122,400,30,20),
        P(rowboat(130,628),130,618,100,44), P(lily(200,420),200,420,26,16), P(lily(160,700,.9,False),160,700,24,14), P(fish(250,460),250,460,22,8),
        P(lily(300,260),300,260,26,16), P(lily(330,300,.8,False),330,300,22,14), P(bank(270,380,110,70),270,380,110,76), P(reeds3(300,384,.8),300,384,40,36), P(frog(290,420),290,420,22,18),
        P(lily(30,620),30,620,26,16), P(fish(40,560),40,560,22,8), P(bank(250,780,150,80),250,780,150,86), P(reeds3(320,780,.9),320,780,44,40), P(bush3(270,800,.7,Q["pink"]),270,800,42,28)]
    check('moat',dense,pts,props)
    return page2('Moat bridge','5/20',61,WATER[0],g+isl,sky+wall,posts+road_planks_d(d),J(props),pts)
# ---------- GATE: one big C hugging the edges, the camp in the middle (cobbles)
def gate4():
    ctrl=[(320,880),(300,780),(210,750),(100,740),(50,660),(50,540),(66,420),(120,350),(220,330),(310,320),(318,262),(246,240),(200,228),(195,196)]
    d,dense=ctrl_road(ctrl); pts=sample(dense,10,.08,.84)
    sky=SKYNOSUN+cloud(30,60,.7)
    gh=f'<rect x="0" y="96" width="390" height="118" fill="{Q["lav"]}"/><g transform="translate(0 96)">{stones(390,118,13)}</g>'+''.join(f'<rect x="{k*30}" y="82" width="20" height="18" rx="2" fill="{Q["lav"]}"/>' for k in range(13))
    for tx in (96,236):
        gh+=f'<rect x="{tx}" y="40" width="58" height="174" fill="{Q["lav"]}"/><rect x="{tx+38}" y="40" width="20" height="174" fill="{Q["lav2"]}"/>'+''.join(f'<rect x="{tx+k*16}" y="28" width="11" height="16" rx="2" fill="{Q["lav"] if k<3 else Q["lav2"]}"/>' for k in range(4))+f'<rect x="{tx+22}" y="66" width="12" height="24" rx="6" fill="{DARK}"/>'
        gh+=f'<rect x="{tx+27}" y="0" width="3" height="30" fill="{DARK}"/><path d="M{tx+30} 2 L{tx+54} 9 L{tx+30} 17 Z" fill="{Q["coral"]}"/>'
        gh+=f'<rect x="{tx+8}" y="104" width="34" height="58" fill="{Q["navy"]}"/><rect x="{tx+28}" y="104" width="14" height="58" fill="{Q["navy2"]}"/><path d="M{tx+8} 162 L{tx+25} 174 L{tx+42} 162 Z" fill="{Q["navy"]}"/><path d="M{tx+25} 116 l6 10 l-6 10 l-6 -10 Z" fill="{Q["mustard"]}"/>'
    gh+=f'<rect x="154" y="106" width="82" height="108" fill="{Q["lav2"]}"/><path d="M164 214 L164 150 C164 118 226 118 226 150 L226 214 Z" fill="#2e1c14"/>'+''.join(f'<rect x="{168+k*11}" y="126" width="3" height="56" fill="#5a5664"/>' for k in range(6))+''.join(f'<rect x="164" y="{136+k*14}" width="62" height="3" fill="#5a5664"/>' for k in range(4))+''.join(f'<path d="M{170+k*11} 182 l1.5 6 l1.5 -6 Z" fill="#5a5664"/>' for k in range(6))
    sky+=gh+f'{pine(-14,148,.9)}{pine(334,152,.85)}'
    g=grass_ground(31,('#9aa860','#8a9a52','#6f7d40'))
    props=[P(barrel(20,236,.8),20,236,40,46), P(tent(56,236,Q["coral"],Q["coral2"]),56,224,90,70),
        P(tent(110,420,Q["navy"],Q["navy2"]),110,408,90,70), P(campfire(200,520),200,516,46,36), P(tent(250,420,Q["coral"],Q["coral2"]),250,408,90,70),
        P(shield_stand(120,600),120,600,70,50), P(barrel(220,600,.8),220,600,40,46), P(apple_crate(270,610,(Q["mustard"],Q["mustard2"])),270,610,50,46),
        P(pine(330,420,.8),330,410,48,76), P(pine(330,560,.75),330,550,45,72), P(cart(170,780,'hay'),170,780,140,80) if False else P('',0,0,0,0),
        P(signpost(14,786),10,786,52,62), P(rock(150,800,.7),150,800,30,20), P(pine(-20,760,.7),-20,750,42,68) if False else P('',0,0,0,0), P(barrel(300,236,.75) if False else '',0,0,0,0)]
    check('gate',dense,pts,props)
    return page2('Gate','5/20',81,'#8a9a52',g+tufts([(170,316),(186,326),(206,480),(150,686),(232,686),(352,676),(140,460),(340,350)]),sky,road_cobbles(d),J(props),pts)
rooms={'Room-v2-dungeon.dc.html':('C3 · Dungeon',dungeon4()),
       'Room-v2-meadow.dc.html':('M2 · Meadow',meadow4()),
       'Room-v2-orchard.dc.html':('O2 · Orchard',orchard4()),
       'Room-v2-stables.dc.html':('S2 · Stables',stables4()),
       'Room-v2-moat.dc.html':('B2 · Moat bridge',moat4()),
       'Room-v2-gate.dc.html':('G2 · Gate',gate4())}
base='/home/claude/mockups/project'
for fn,(t,body) in rooms.items(): open(f'{base}/{fn}','w').write(G['HEADQ']%t+body+'\n'+G['TAIL'])
print('ok')
