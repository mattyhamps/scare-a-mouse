import json, math, random, re
g19=open('./gen19.py').read()
exec(g19[:g19.index("\nrooms={")])
# ================= First floor: Library, Study, Great hall, Ballroom, Gallery
SP=[(Q["coral"],Q["coral2"]),(Q["navy"],Q["navy2"]),(Q["green"],Q["green2"]),(Q["mustard"],Q["mustard2"]),(Q["olive"],Q["olive2"]),(Q["cream"],Q["cream2"]),('#7a4a7a','#5e3460')]
def spines(w,h,seed,rows=3):
    r=random.Random(seed); s=''
    for row in range(rows):
        y0=row*h/rows; xx=3
        while xx<w-6:
            bw=r.choice((5,6,7,8)); bh=h/rows-r.choice((4,6,8)); c,c2=r.choice(SP)
            if xx+bw>w-3: break
            s+=f'<rect x="{xx}" y="{y0+h/rows-bh-2}" width="{bw}" height="{bh}" rx="1" fill="{c}"/><rect x="{xx+bw*0.6}" y="{y0+h/rows-bh-2}" width="{bw*0.4}" height="{bh}" fill="{c2}"/>'
            xx+=bw+1
        s+=f'<rect x="0" y="{y0+h/rows-2}" width="{w}" height="3" fill="{WOOD[2]}"/>'
    return s
def bookshelf(x,y,w=72,h=84,d=14,seed=1):
    return f'''<g transform="translate({x} {y})">{shadow(w/2+3,d+h,w/2+6,6)}<rect x="0" y="{d-2}" width="{w}" height="{h}" rx="2" fill="{WOOD[2]}"/><rect x="4" y="{d+2}" width="{w-8}" height="{h-8}" fill="#3a2418"/>
      <g transform="translate(4 {d+2})">{spines(w-8,h-8,seed)}</g><rect x="{w-5}" y="{d-2}" width="5" height="{h}" fill="#5a3a24"/><rect x="0" y="0" width="{w}" height="{d}" rx="2" fill="{WOOD[1]}"/><rect x="0" y="0" width="{w}" height="4" rx="2" fill="{WOOD[0]}"/></g>'''
def armchair(x,y,c=None,c2=None):
    c=c or Q["coral"]; c2=c2 or Q["coral2"]
    return f'''<g transform="translate({x} {y})">{shadow(26,50,28,6)}<rect x="6" y="0" width="40" height="30" rx="12" fill="{c}"/><rect x="30" y="0" width="16" height="30" rx="8" fill="{c2}"/>
      <rect x="4" y="22" width="44" height="22" rx="6" fill="{c2}"/><rect x="8" y="20" width="36" height="14" rx="5" fill="{c}"/><rect x="0" y="14" width="10" height="30" rx="5" fill="{c}"/><rect x="42" y="14" width="10" height="30" rx="5" fill="{c2}"/>
      <rect x="6" y="44" width="5" height="6" fill="{WOOD[2]}"/><rect x="41" y="44" width="5" height="6" fill="{WOOD[2]}"/></g>'''
def globe(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(20,62,18,5)}<rect x="18" y="40" width="4" height="18" fill="{WOOD[1]}"/><path d="M8 62 L20 54 L32 62 Z" fill="{WOOD[2]}"/>
      <circle cx="20" cy="22" r="17" fill="#6f9bb3"/><path d="M20 5 A17 17 0 0 1 37 22 A17 17 0 0 1 26 38 A18 18 0 0 0 30 22 Z" fill="#5a879f"/><path d="M10 14 q6 -4 10 2 q-2 6 -8 4 Z M22 24 q6 -2 8 4 q-4 6 -8 2 Z" fill="{Q["olive"]}"/>
      <path d="M3 22 A17 17 0 0 0 37 22" fill="none" stroke="{Q["mustard"]}" stroke-width="2.4" transform="rotate(-20 20 22)"/><circle cx="20" cy="22" r="20" fill="none" stroke="{Q["mustard2"]}" stroke-width="2.4" stroke-dasharray="40 200" transform="rotate(200 20 22)"/></g>'''
def books(x,y,n=3):
    s=f'<g transform="translate({x} {y})">{shadow(17,9,19,4)}'
    for k in range(n):
        c,c2=SP[(k*3+1)%len(SP)]; yy=-k*7; dx=(k%2)*3
        s+=f'<rect x="{dx}" y="{yy}" width="30" height="8" rx="1.5" fill="{c}"/><rect x="{dx+22}" y="{yy}" width="8" height="8" fill="{c2}"/><rect x="{dx}" y="{yy+3}" width="22" height="2" fill="{Q["cream"]}" opacity=".7"/>'
    return s+'</g>'
def reading_table(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(30,50,32,6)}<rect x="26" y="20" width="8" height="30" fill="{WOOD[2]}"/><rect x="12" y="46" width="36" height="5" rx="2" fill="{WOOD[2]}"/><ellipse cx="30" cy="20" rx="30" ry="10" fill="{WOOD[1]}"/><ellipse cx="30" cy="17" rx="30" ry="10" fill="{WOOD[0]}"/>
      <path d="M12 16 Q20 10 30 14 Q40 10 48 16 L48 20 Q40 15 30 19 Q20 15 12 20 Z" fill="{Q["cream"]}"/><path d="M30 14 L30 19" stroke="{Q["cream2"]}" stroke-width="1.5"/>
      <circle cx="46" cy="4" r="14" fill="{Q["mustard"]}" opacity=".16"/><rect x="43" y="2" width="6" height="12" rx="2" fill="{Q["cream"]}"/><path d="M46 -6 C43 -1 44 2 46 2 C48 2 49 -1 46 -6 Z" fill="{Q["mustard"]}"/></g>'''
def carpet(d,edge,body,border=None,inner=None,cap='round'):
    s=f'<path d="{d}" fill="none" stroke="#1a0c06" stroke-opacity=".2" stroke-width="46" stroke-linejoin="round" stroke-linecap="{cap}" transform="translate(0 4)"/><path d="{d}" fill="none" stroke="{edge}" stroke-width="44" stroke-linejoin="round" stroke-linecap="{cap}"/>'
    if border: s+=f'<path d="{d}" fill="none" stroke="{border}" stroke-width="36" stroke-linejoin="round" stroke-linecap="{cap}"/>'
    s+=f'<path d="{d}" fill="none" stroke="{body}" stroke-width="{30 if border else 40}" stroke-linejoin="round" stroke-linecap="{cap}"/>'
    if inner: s+=f'<path d="{d}" fill="none" stroke="{inner}" stroke-width="4" stroke-dasharray="3 9" stroke-linejoin="round"/>'
    return s
def wood_floor(c1,c2,seam,seed): return plank_floor(c1,c2,seam,seed)
def parquet(c1,c2,seed):
    g=f'<rect x="0" y="214" width="390" height="630" fill="{c1}"/>'
    for r_,yy in enumerate(range(214,844,20)):
        for k,xx in enumerate(range(-40+(r_%2)*20,400,40)):
            g+=f'<path d="M{xx} {yy} l20 0 l20 20 l-20 0 Z" fill="{c2}"/>'
    return g
def marble(c1,c2):
    return f'<rect x="0" y="214" width="390" height="630" fill="{c1}"/>'+''.join(f'<rect x="{c*48-12}" y="{214+r*48}" width="48" height="48" fill="{c2}"/>' for r in range(14) for c in range(10) if (r+c)%2)
# ---------- LIBRARY: stair-steps, navy rug, dark wood floor
def library():
    poly=[(60,880),(60,744),(150,744),(150,640),(240,640),(240,536),(330,536),(330,410),(196,410),(196,196)]
    d,dense=poly_road(poly); pts=sample(dense,10,.09,.87)
    wall=f'<rect x="0" y="0" width="390" height="214" fill="#5a3a24"/>'
    for sx in (8,82,250,324):
        wall+=f'<g transform="translate({sx} 40)"><rect x="0" y="0" width="64" height="168" fill="{WOOD[2]}"/><rect x="4" y="4" width="56" height="160" fill="#3a2418"/><g transform="translate(4 4)">{spines(56,160,sx,5)}</g><rect x="0" y="0" width="64" height="6" fill="{WOOD[1]}"/></g>'
    wall+=f'<rect x="146" y="60" width="98" height="154" fill="{WOOD[1]}"/><rect x="150" y="64" width="90" height="150" fill="{WOOD[2]}"/>'+gate_arch(164,62,(Q["navy"],Q["navy2"]))+sconce(150,130)+sconce(228,130)
    wall+=f'<rect x="0" y="0" width="390" height="40" fill="#4a2e1c"/><rect x="0" y="36" width="390" height="6" fill="{WOOD[1]}"/>'
    floor=flag_floor(('#4f5d58','#52605b','#4c5a55'),5,'#3e4a46')+FLOORSHADE+SIDE('#4a2e1c')
    props=[P(bookshelf(14,236,72,80,14,3),14,236,78,96), P(armchair(100,280,Q["navy"],Q["navy2"]),100,280,52,50), P(globe(280,236),280,236,40,62), P(books(336,300,4),336,278,36,34),
        P(reading_table(14,420),14,406,60,52), P(armchair(84,440),84,440,52,50), P(books(150,470,3),150,456,36,26),
        P(bookshelf(276,600,80,84,14,7),276,600,86,100), P(bookshelf(188,700,72,80,14,9),188,700,78,96), P(armchair(300,720,Q["green"],Q["green2"]),300,720,52,50) if False else P('',0,0,0,0),
        P(bookshelf(290,724,80,80,14,11),290,724,86,96), P(books(16,560,5),16,532,36,40), P(reading_table(90,560) if False else '',0,0,0,0), P(globe(110,800),110,800,40,62) if False else P('',0,0,0,0)]
    check('library',dense,pts,props)
    return page2('Library','5/30',201,'#3e4a46',floor,wall,carpet(d,'#16264a',Q["navy"],Q["mustard"],Q["navy2"]),J(props),pts)
# ---------- STUDY: a loop round the big desk (question mark), green carpet, honey parquet
def desk(x,y):
    w,d_=150,64
    return f'''<g transform="translate({x} {y})">{shadow(w/2,d_+30,w/2+8,8)}<rect x="0" y="{d_-4}" width="{w}" height="26" rx="3" fill="{WOOD[1]}"/>{''.join(f'<rect x="{dx}" y="{d_+2}" width="40" height="14" rx="2" fill="{WOOD[0]}"/><circle cx="{dx+20}" cy="{d_+9}" r="2.4" fill="{Q["mustard"]}"/>' for dx in (8,w-48))}<rect x="{w-12}" y="{d_-4}" width="12" height="26" fill="{WOOD[2]}"/>
      <rect x="0" y="0" width="{w}" height="{d_}" rx="4" fill="{WOOD[0]}"/><rect x="6" y="6" width="{w-12}" height="{d_-12}" rx="3" fill="{Q["green2"]}" opacity=".85"/>
      <g transform="translate(16 12) rotate(-6)"><rect x="0" y="0" width="60" height="38" rx="2" fill="{Q["cream"]}"/><path d="M6 10 q10 -6 20 2 t20 0 M8 24 q14 6 26 -2" stroke="{Q["tan2"]}" stroke-width="2" fill="none"/><circle cx="44" cy="26" r="4" fill="none" stroke="{Q["coral"]}" stroke-width="2"/></g>
      <rect x="88" y="14" width="22" height="28" rx="1" fill="{Q["cream"]}"/><rect x="92" y="20" width="14" height="2" fill="{Q["cream2"]}"/><rect x="92" y="26" width="12" height="2" fill="{Q["cream2"]}"/>
      <ellipse cx="124" cy="36" rx="7" ry="4" fill="{DARK}"/><path d="M124 34 L136 8 L130 30 Z" fill="{Q["cream"]}"/><circle cx="130" cy="16" r="10" fill="{Q["mustard"]}" opacity=".0"/>
      <g transform="translate(122 4)"><rect x="0" y="0" width="6" height="12" rx="2" fill="{Q["cream"]}"/><path d="M3 -8 C0 -3 1 0 3 0 C5 0 6 -3 3 -8 Z" fill="{Q["mustard"]}"/></g></g>'''
def telescope(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(24,70,22,5)}<path d="M24 40 L8 70 M24 40 L40 70 M24 40 L24 72" stroke="{WOOD[1]}" stroke-width="3.4" stroke-linecap="round"/>
      <g transform="rotate(-32 24 38)"><rect x="-6" y="32" width="56" height="12" rx="4" fill="{Q["mustard"]}"/><rect x="-6" y="38" width="56" height="6" rx="3" fill="{Q["mustard2"]}"/><rect x="46" y="30" width="10" height="16" rx="3" fill="{Q["mustard2"]}"/><rect x="-10" y="35" width="6" height="6" rx="2" fill="{DARK}"/></g></g>'''
def chair(x,y):
    return f'<g transform="translate({x} {y})">{shadow(18,46,18,5)}<rect x="4" y="0" width="28" height="22" rx="4" fill="{WOOD[1]}"/><rect x="9" y="5" width="18" height="12" rx="2" fill="{Q["green"]}"/><rect x="2" y="22" width="32" height="10" rx="3" fill="{WOOD[0]}"/><rect x="2" y="30" width="32" height="4" fill="{WOOD[2]}"/><rect x="4" y="34" width="4" height="12" fill="{WOOD[2]}"/><rect x="28" y="34" width="4" height="12" fill="{WOOD[2]}"/></g>'
def scrolls(x,y):
    rolls=''.join(f'<g transform="translate({6+k*9} {-4-(k%2)*6}) rotate({-8+k*6} 4 20)"><rect x="0" y="0" width="8" height="28" rx="3" fill="{Q["cream"]}"/><rect x="5" y="0" width="3" height="28" rx="1" fill="{Q["cream2"]}"/><rect x="0" y="6" width="8" height="2" fill="{Q["coral"]}"/></g>' for k in range(4))
    return f'<g transform="translate({x} {y})">{shadow(22,40,22,5)}{rolls}<path d="M2 18 L42 18 L38 40 L6 40 Z" fill="#c99a56"/><path d="M28 18 L42 18 L38 40 L28 40 Z" fill="#a87a42"/><ellipse cx="22" cy="18" rx="20" ry="5" fill="#d9b06a"/></g>'
def drawers(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(32,70,34,6)}<rect x="0" y="12" width="64" height="58" rx="3" fill="{WOOD[1]}"/>{''.join(f'<rect x="5" y="{17+k*17}" width="46" height="13" rx="2" fill="{WOOD[0]}"/><circle cx="28" cy="{23.5+k*17}" r="2.4" fill="{Q["mustard"]}"/>' for k in range(3))}<rect x="52" y="12" width="12" height="58" fill="{WOOD[2]}"/>
      <rect x="0" y="0" width="64" height="14" rx="3" fill="{WOOD[0]}"/><g transform="translate(40 -14)"><rect x="0" y="6" width="12" height="16" rx="5" fill="{Q["olive"]}"/><path d="M6 6 l-6 -10 M6 6 l2 -12 M6 6 l8 -8" stroke="{Q["green"]}" stroke-width="3" stroke-linecap="round"/></g></g>'''
def study():
    ctrl=[(195,880),(196,780),(212,690),(296,640),(338,540),(300,446),(200,410),(104,440),(60,520)][:0]
    ctrl=[(210,880),(214,780),(280,720),(336,630),(336,520),(280,430),(190,400),(100,420),(56,500),(52,400),(84,320),(150,276),(194,240),(195,196)]
    d,dense=ctrl_road(ctrl); pts=sample(dense,10,.08,.86)
    wall=f'<rect x="0" y="0" width="390" height="214" fill="{Q["navy2"]}"/>'+''.join(f'<path d="M{k*26} 0 l13 13 l-13 13 l-13 -13 Z" fill="{Q["navy"]}" transform="translate(0 {r*26+40})" opacity=".55"/>' for r in range(4) for k in range(16))
    wall+=f'<rect x="0" y="140" width="390" height="74" fill="{WOOD[1]}"/>'+''.join(f'<rect x="{6+k*48}" y="148" width="40" height="58" rx="3" fill="{WOOD[0]}" opacity=".55"/>' for k in range(9))+f'<rect x="0" y="136" width="390" height="6" fill="{WOOD[2]}"/>'
    wall+=f'<g transform="translate(18 52)"><rect x="0" y="0" width="112" height="76" rx="2" fill="{Q["mustard2"]}"/><rect x="5" y="5" width="102" height="66" fill="{Q["cream"]}"/><path d="M14 20 q14 -10 26 0 q8 10 22 2 q14 -8 30 4 M18 52 q20 -8 34 2 q12 6 40 -6" stroke="{Q["tan2"]}" stroke-width="3" fill="none"/><path d="M60 30 l10 8 l-10 8 l-10 -8 Z" fill="{Q["coral"]}"/><circle cx="90" cy="20" r="6" fill="none" stroke="{Q["navy"]}" stroke-width="2"/></g>'
    wall+=window(300,62)+f'<rect x="146" y="106" width="98" height="108" fill="{WOOD[2]}"/>'+gate_arch(164,62)
    floor=parquet('#b3ada2','#aaa499',3)+FLOORSHADE+SIDE(WOOD[2])
    rug=f'<g transform="translate(118 474)"><rect x="0" y="4" width="160" height="150" rx="10" fill="#2a140a" opacity=".18"/><rect x="0" y="0" width="160" height="150" rx="10" fill="{Q["coral2"]}"/><rect x="10" y="10" width="140" height="130" rx="6" fill="{Q["coral"]}"/><rect x="24" y="24" width="112" height="102" rx="4" fill="none" stroke="{Q["mustard"]}" stroke-width="3" stroke-dasharray="6 5"/></g>'
    props=[P(rug,118,474,160,154), P(desk(124,486),124,486,150,98), P(chair(180,540),180,540,36,46) if False else P('',0,0,0,0),
        P(globe(224,250),224,250,40,62), P(drawers(296,236),296,222,64,84),
        P(telescope(16,600),8,600,56,74), P(scrolls(20,700),20,690,44,52),
        P(armchair(296,760,Q["green"],Q["green2"]),296,760,52,50), P(books(110,800,4),110,778,36,34), P(chair(30,250),30,250,36,46), P(books(260,330,3),260,316,36,26) if False else P('',0,0,0,0)]
    check('study',dense,pts,props)
    return page2('Study','5/30',231,'#b3ada2',floor,wall,carpet(d,'#1f3a28',Q["green"],Q["mustard"],Q["green2"]),J(props),pts)
# ---------- GREAT HALL: one straight royal carpet up the middle between the feast tables
def feast_table(x,y,h=300):
    w=58
    items=''
    for k,yy in enumerate(range(18,h-30,46)):
        items+=f'<ellipse cx="18" cy="{yy}" rx="11" ry="8" fill="{Q["cream"]}"/><ellipse cx="18" cy="{yy}" rx="7" ry="5" fill="{Q["cream2"]}"/>'+f'<ellipse cx="40" cy="{yy+4}" rx="11" ry="8" fill="{Q["cream"]}"/><ellipse cx="40" cy="{yy+4}" rx="7" ry="5" fill="{Q["cream2"]}"/>'
        if k%3==0: items+=f'<g transform="translate(16 {yy+18})"><ellipse cx="12" cy="8" rx="13" ry="9" fill="#c88a3e"/><ellipse cx="10" cy="6" rx="10" ry="7" fill="#dca55a"/><rect x="20" y="0" width="10" height="5" rx="2" fill="{Q["cream"]}"/></g>'
        elif k%3==1: items+=f'<g transform="translate(18 {yy+18})">'+''.join(f'<circle cx="{ax}" cy="{ay}" r="5" fill="{c}"/>' for ax,ay,c in ((4,4,Q["coral"]),(14,6,Q["mustard"]),(9,12,Q["olive"]),(18,14,Q["coral2"])))+'</g>'
        else: items+=f'<g transform="translate(22 {yy+16})"><rect x="0" y="4" width="14" height="16" rx="3" fill="#8a8794"/><rect x="8" y="4" width="6" height="16" rx="2" fill="#6e6b78"/><ellipse cx="7" cy="4" rx="7" ry="2.6" fill="#a8353a"/></g>'
    return f'''<g transform="translate({x} {y})">{shadow(w/2,h+18,w/2+10,10)}<rect x="0" y="{h-6}" width="{w}" height="16" rx="3" fill="{WOOD[1]}"/><rect x="4" y="{h+8}" width="8" height="12" fill="{WOOD[2]}"/><rect x="{w-12}" y="{h+8}" width="8" height="12" fill="{WOOD[2]}"/>
      <rect x="0" y="0" width="{w}" height="{h}" rx="5" fill="{WOOD[0]}"/><rect x="8" y="0" width="{w-16}" height="{h}" fill="{Q["cream"]}" opacity=".9"/><rect x="{w-16}" y="0" width="8" height="{h}" fill="{Q["cream2"]}" opacity=".9"/>{items}</g>'''
def bench_v(x,y,h=300):
    return f'<g transform="translate({x} {y})">{shadow(9,h+8,12,6)}<rect x="0" y="0" width="18" height="{h}" rx="3" fill="{WOOD[1]}"/><rect x="12" y="0" width="6" height="{h}" rx="2" fill="{WOOD[2]}"/><rect x="0" y="{h-4}" width="18" height="8" fill="{WOOD[2]}"/></g>'
def armor(x,y):
    S='#a8a5b2'; S2='#7d7a86'
    return f'''<g transform="translate({x} {y})">{shadow(18,82,18,5)}<rect x="8" y="58" width="8" height="24" rx="2" fill="{S}"/><rect x="20" y="58" width="8" height="24" rx="2" fill="{S2}"/>
      <path d="M4 26 Q18 18 32 26 L30 58 L6 58 Z" fill="{S}"/><path d="M18 22 Q26 22 32 26 L30 58 L18 58 Z" fill="{S2}"/><rect x="0" y="26" width="7" height="26" rx="3" fill="{S}"/><rect x="29" y="26" width="7" height="26" rx="3" fill="{S2}"/>
      <rect x="8" y="2" width="20" height="22" rx="8" fill="{S}"/><rect x="18" y="2" width="10" height="22" rx="5" fill="{S2}"/><rect x="10" y="11" width="16" height="3" fill="{DARK}"/><path d="M18 2 Q20 -10 30 -8" stroke="{Q["coral"]}" stroke-width="4" fill="none" stroke-linecap="round"/>
      <rect x="34" y="-4" width="3" height="80" fill="{WOOD[1]}"/><path d="M30 -4 L35.5 -16 L41 -4 Z" fill="{S}"/></g>'''
def great_hall():
    poly=[(195,880),(195,196)]
    d,dense=poly_road(poly); pts=sample(dense,10,.3,.94)
    pts=[(195,y) for y in range(780,290,-54)][:10]
    wall=f'<rect x="0" y="0" width="390" height="214" fill="{Q["lav"]}"/>{stones(390,214,41)}'
    for bx,c,c2 in ((26,Q["coral"],Q["coral2"]),(86,Q["navy"],Q["navy2"]),(272,Q["navy"],Q["navy2"]),(332,Q["coral"],Q["coral2"])):
        wall+=f'<rect x="{bx-4}" y="44" width="40" height="5" rx="2" fill="{WOOD[2]}"/><rect x="{bx}" y="48" width="32" height="96" fill="{c}"/><rect x="{bx+20}" y="48" width="12" height="96" fill="{c2}"/><path d="M{bx} 144 L{bx+16} 158 L{bx+32} 144 Z" fill="{c}"/><path d="M{bx+16} 70 l8 12 l-8 12 l-8 -12 Z" fill="{Q["mustard"]}"/>'
    wall+=f'<g transform="translate(195 40)"><path d="M-22 0 L22 0 L22 22 Q22 40 0 48 Q-22 40 -22 22 Z" fill="{Q["coral"]}"/><path d="M0 0 L22 0 L22 22 Q22 40 0 48 Z" fill="{Q["coral2"]}"/><path d="M-30 -6 L30 54 M30 -6 L-30 54" stroke="#a8a5b2" stroke-width="4"/><path d="M-6 14 l6 -8 l6 8 l-6 14 Z" fill="{Q["mustard"]}"/></g>'
    wall+=f'<rect x="142" y="100" width="106" height="114" fill="{Q["lav2"]}"/><path d="M152 214 L152 146 C152 108 238 108 238 146 L238 214 Z" fill="{Q["brown"]}"/><path d="M195 110 L195 214" stroke="{Q["brown2"]}" stroke-width="3"/><path d="M195 110 C224 112 238 126 238 146 L238 214 L195 214 Z" fill="{Q["brown2"]}"/>'+''.join(f'<rect x="152" y="{yy}" width="86" height="4" fill="#4a4652"/>' for yy in (150,184))+f'<circle cx="186" cy="170" r="4" fill="{Q["mustard"]}"/><circle cx="204" cy="170" r="4" fill="{Q["mustard"]}"/>'+sconce(126,130)+sconce(252,130)
    floor=flag_floor(('#9c8f84','#a39589','#978a7f'),41,'#85786e')+FLOORSHADE+SIDE(Q["lav2"])
    props=[P(bench_v(36,300,300),36,300,18,310), P(feast_table(62,300,300),62,300,58,330), P(feast_table(270,300,300),270,300,58,330), P(bench_v(336,300,300),336,300,18,310),
        P(armor(8,230),0,214,44,96), P(armor(346,230),340,214,44,96), P(barrel(14,660,.8),14,660,40,46), P(barrel(336,670,.8),336,670,40,46),
        P(f'<g transform="translate(260 680)">{shadow(30,40,34,7)}<ellipse cx="30" cy="30" rx="30" ry="12" fill="#c99a56"/><ellipse cx="30" cy="27" rx="26" ry="10" fill="{Q["coral"]}"/></g><g transform="translate(266 640)">{sv("dog",46)}</g>',260,640,62,72),
        P(barrel(60,760,.75),60,760,36,44), P(armor(8,770),0,754,44,96) if False else P('',0,0,0,0)]
    check('greathall',dense,pts,props)
    return page2('Great hall','5/30',261,'#85786e',floor,wall,carpet('M 195 880 L 195 196','#5a1a1c','#a8353a',Q["mustard"],'#c4554a','butt'),J(props),pts)
# ---------- BALLROOM: a tight wiggle up the middle, gold path, rose marble checks
def pillar(x,y,h=110):
    return f'''<g transform="translate({x} {y})">{shadow(22,h+6,26,6)}<rect x="0" y="{h-14}" width="44" height="16" rx="2" fill="#e0d3cf"/><rect x="32" y="{h-14}" width="12" height="16" fill="#c4b6b2"/>
      <rect x="6" y="14" width="32" height="{h-28}" fill="#efe6e3"/>{''.join(f'<rect x="{10+k*7}" y="14" width="2.4" height="{h-28}" fill="#d6c8c4"/>' for k in range(4))}<rect x="26" y="14" width="12" height="{h-28}" fill="#d6c8c4"/>
      <rect x="0" y="2" width="44" height="14" rx="2" fill="#e0d3cf"/><rect x="32" y="2" width="12" height="14" fill="#c4b6b2"/><rect x="-2" y="-4" width="48" height="8" rx="2" fill="#efe6e3"/><path d="M0 4 q4 6 10 0 M34 4 q4 6 10 0" stroke="{Q["mustard"]}" stroke-width="2" fill="none"/></g>'''
def piano(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(50,96,54,8)}<rect x="10" y="78" width="6" height="18" fill="#1e1a24"/><rect x="84" y="78" width="6" height="18" fill="#1e1a24"/>
      <path d="M0 64 L0 10 Q0 0 14 0 L60 0 Q100 6 100 40 L100 64 Z" fill="#2e2a36"/><path d="M0 64 L100 64 L100 82 L0 82 Z" fill="#1e1a24"/><path d="M6 58 L6 14 Q6 6 16 6 L58 6 Q94 12 94 40 L94 58 Z" fill="#3e3a48"/>
      <path d="M40 8 L94 40 L94 58 L40 58 Z" fill="#4a4652" opacity=".6"/><rect x="4" y="64" width="92" height="10" fill="{Q["cream"]}"/>{''.join(f'<rect x="{8+k*7}" y="64" width="3.4" height="6" fill="#1e1a24"/>' for k in range(13) if k%7 not in (2,6))}
      <g transform="translate(32 96)">{shadow(16,10,16,3)}<rect x="0" y="0" width="34" height="9" rx="3" fill="#a8353a"/><rect x="2" y="9" width="4" height="6" fill="#1e1a24"/><rect x="28" y="9" width="4" height="6" fill="#1e1a24"/></g></g>'''
def harp(x,y):
    strings=''.join(f'<path d="M{10+k*5} {58-k*4} L{10+k*5} {14+k*2}" stroke="{Q["cream"]}" stroke-width="1.2"/>' for k in range(7))
    return f'<g transform="translate({x} {y})">{shadow(24,66,24,5)}<path d="M6 62 L44 62 L40 56 L10 56 Z" fill="{Q["mustard2"]}"/><path d="M8 58 L8 10 Q8 0 18 4 Q34 12 46 6 L46 14 Q34 24 14 14 L14 58 Z" fill="{Q["mustard"]}"/><path d="M44 8 L40 56" stroke="{Q["mustard2"]}" stroke-width="6" stroke-linecap="round"/>{strings}</g>'
def punch_table(x,y):
    cups=''.join(f'<g transform="translate({cx} {cy})"><rect x="0" y="0" width="7" height="9" rx="2" fill="#d6c8c4"/><ellipse cx="3.5" cy="1" rx="3.5" ry="1.6" fill="{Q["coral"]}"/></g>' for cx,cy in ((6,18),(46,20),(14,30),(38,32)))
    return f'''<g transform="translate({x} {y})">{shadow(30,52,34,6)}<rect x="26" y="22" width="8" height="30" fill="#c4b6b2"/><ellipse cx="30" cy="22" rx="30" ry="12" fill="#c4b6b2"/><ellipse cx="30" cy="19" rx="30" ry="12" fill="{Q["cream"]}"/>
      <path d="M14 14 Q30 34 46 14 Z" fill="#d6c8c4"/><ellipse cx="30" cy="14" rx="16" ry="5" fill="{Q["coral"]}"/><ellipse cx="26" cy="13" rx="6" ry="2" fill="{Q["pink"]}"/>{cups}</g>'''
def vase_flowers(x,y,c=None):
    c=c or Q["pink"]
    fl=''.join(f'<circle cx="{fx}" cy="{fy}" r="5" fill="{cc}"/><circle cx="{fx}" cy="{fy}" r="2" fill="{Q["mustard"]}"/>' for fx,fy,cc in ((8,4,c),(18,-2,Q["cream"]),(28,4,c),(14,8,Q["coral"]),(24,10,Q["cream"])))
    return f'<g transform="translate({x} {y})">{shadow(18,50,16,4)}<path d="M8 20 Q4 34 10 46 L26 46 Q32 34 28 20 Z" fill="{Q["navy"]}"/><path d="M20 20 L28 20 Q32 34 26 46 L20 46 Q24 32 20 20 Z" fill="{Q["navy2"]}"/><rect x="8" y="16" width="20" height="6" rx="3" fill="{Q["navy2"]}"/><path d="M12 16 L10 6 M18 16 L18 0 M24 16 L26 6" stroke="{Q["green2"]}" stroke-width="2.4"/>{fl}</g>'
def path_gold(d):
    return (f'<path d="{d}" fill="none" stroke="#5a3a24" stroke-opacity=".3" stroke-width="44" stroke-linecap="round" transform="translate(0 4)"/><path d="{d}" fill="none" stroke="{Q["mustard2"]}" stroke-width="42" stroke-linecap="round"/><path d="{d}" fill="none" stroke="{Q["mustard"]}" stroke-width="36" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="#f0d07a" stroke-width="10" stroke-linecap="round" transform="translate(-5 -4)" opacity=".8"/><path d="{d}" fill="none" stroke="{Q["mustard2"]}" stroke-width="36" stroke-dasharray="1.6 22"/>')
def ballroom():
    ctrl=[(195,880),(195,800)]+[(195+(56 if k%2==0 else -56),760-k*62) for k in range(9)]+[(195,236),(195,196)]
    d,dense=ctrl_road(ctrl); pts=sample(dense,10,.1,.88)
    wall=f'<rect x="0" y="0" width="390" height="214" fill="{Q["pink2"]}"/>'+''.join(f'<rect x="{k*30}" y="0" width="15" height="214" fill="{Q["pink"]}" opacity=".35"/>' for k in range(13))
    wall+=f'<rect x="0" y="150" width="390" height="64" fill="#e5d2d7"/><rect x="0" y="146" width="390" height="6" fill="{Q["mustard"]}"/>'+''.join(f'<rect x="{8+k*48}" y="160" width="38" height="44" rx="3" fill="none" stroke="{Q["mustard"]}" stroke-width="2"/>' for k in range(8))
    for wx in (24,306):
        wall+=f'<g transform="translate({wx} 44)"><rect x="-6" y="-6" width="72" height="112" rx="36" fill="{Q["mustard"]}"/><rect x="0" y="0" width="60" height="100" rx="30" fill="#9cb8c8"/><path d="M30 0 A30 30 0 0 1 60 30 L60 100 L42 100 L42 10 Z" fill="#86a5b8"/><rect x="28" y="0" width="4" height="100" fill="{Q["mustard"]}"/><rect x="0" y="44" width="60" height="4" fill="{Q["mustard"]}"/></g>'
    wall+=f'<g transform="translate(195 0)"><rect x="-1" y="0" width="2" height="34" fill="{Q["mustard2"]}"/><path d="M-40 44 Q0 70 40 44" stroke="{Q["mustard"]}" stroke-width="4" fill="none"/><path d="M-24 40 Q0 56 24 40" stroke="{Q["mustard"]}" stroke-width="3" fill="none"/><ellipse cx="0" cy="40" rx="14" ry="6" fill="{Q["mustard2"]}"/>'+''.join(f'<rect x="{cx-2}" y="{cy-10}" width="4" height="10" fill="{Q["cream"]}"/><path d="M{cx} {cy-16} c-3 4 -2 6 0 6 c2 0 3 -2 0 -6 Z" fill="{Q["mustard"]}"/>' for cx,cy in ((-40,44),(-24,40),(24,40),(40,44),(0,58)))+f'<circle cx="0" cy="46" r="56" fill="{Q["mustard"]}" opacity=".08"/></g>'
    wall+=f'<rect x="144" y="100" width="102" height="114" fill="{Q["mustard2"]}"/><path d="M152 214 L152 146 C152 108 238 108 238 146 L238 214 Z" fill="#f1e3c2"/><path d="M195 110 C224 112 238 126 238 146 L238 214 L195 214 Z" fill="#e0cb9c"/><path d="M195 110 L195 214" stroke="{Q["mustard"]}" stroke-width="3"/>'+''.join(f'<rect x="{160+k*44}" y="{yy}" width="26" height="30" rx="2" fill="none" stroke="{Q["mustard"]}" stroke-width="2"/>' for k in range(2) for yy in (130,170))
    floor=marble('#efe3e0','#d9c3c6')+FLOORSHADE+SIDE('#c4b6b2')
    props=[P(pillar(14,226,100),12,222,48,110), P(pillar(332,226,100),330,222,48,110), P(pillar(14,470,100),12,466,48,110), P(pillar(332,470,100),330,466,48,110),
        P(piano(10,664),10,664,104,112), P(harp(310,624),310,614,50,70), P(punch_table(306,764),306,764,62,56),
        P(vase_flowers(72,344),72,334,36,64), P(vase_flowers(282,350,Q["coral"]),282,340,36,64), P(vase_flowers(14,780),14,770,36,64) if False else P('',0,0,0,0)]
    check('ballroom',dense,pts,props)
    return page2('Ballroom','5/30',291,'#efe3e0',floor,wall,path_gold(d),J(props),pts)
# ---------- GALLERY: serpentine with cut corners, green carpet, dark parquet
def plinth(x,y,top):
    return f'''<g transform="translate({x} {y})">{shadow(22,76,26,6)}<rect x="0" y="32" width="44" height="44" rx="2" fill="#e0d3cf"/><rect x="32" y="32" width="12" height="44" fill="#c4b6b2"/><rect x="-3" y="26" width="50" height="10" rx="2" fill="#efe6e3"/><rect x="-3" y="72" width="50" height="6" rx="2" fill="#c4b6b2"/>{top}</g>'''
def bust_top(): return f'<g transform="translate(8 -8)"><path d="M0 34 Q2 20 14 18 Q26 20 28 34 Z" fill="#efe6e3"/><path d="M14 18 Q26 20 28 34 L18 34 Q22 24 14 18 Z" fill="#d6c8c4"/><ellipse cx="14" cy="10" rx="9" ry="11" fill="#efe6e3"/><path d="M14 -1 A9 11 0 0 1 23 10 A9 11 0 0 1 16 21 Q20 10 14 -1 Z" fill="#d6c8c4"/></g>'
def urn_top(): return f'<g transform="translate(8 -10)"><path d="M4 8 Q-4 22 6 34 L22 34 Q32 22 24 8 Z" fill="{Q["coral"]}"/><path d="M16 8 L24 8 Q32 22 22 34 L16 34 Q22 22 16 8 Z" fill="{Q["coral2"]}"/><rect x="6" y="2" width="16" height="8" rx="2" fill="{Q["coral2"]}"/><path d="M4 20 L24 20" stroke="{DARK}" stroke-width="2"/><path d="M6 26 L22 26" stroke="{Q["mustard"]}" stroke-width="2"/></g>'
def ropes(x,y,n=3,gap=40):
    posts=''.join(f'<g transform="translate({k*gap} 0)"><ellipse cx="5" cy="40" rx="9" ry="3.4" fill="#2e2a36"/><rect x="2.5" y="6" width="5" height="34" fill="#3e3a48"/><rect x="5" y="6" width="2.5" height="34" fill="#2e2a36"/><circle cx="5" cy="6" r="5" fill="{Q["mustard"]}"/><circle cx="3.6" cy="4.6" r="1.6" fill="#f0d07a"/></g>' for k in range(n))
    sw=''.join(f'<path d="M{k*gap+5} 10 Q{k*gap+5+gap/2} 30 {(k+1)*gap+5} 10" stroke="#842629" stroke-width="5" fill="none"/>' for k in range(n-1))
    return f'<g transform="translate({x} {y})">{shadow((n-1)*gap/2+5,42,(n-1)*gap/2+12,4)}{sw}{posts}</g>'
def easel(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(26,82,24,5)}<path d="M10 82 L24 0 M42 82 L28 0 M26 30 L34 84" stroke="{WOOD[1]}" stroke-width="4" stroke-linecap="round"/><rect x="2" y="48" width="48" height="5" rx="2" fill="{WOOD[2]}"/>
      <rect x="4" y="12" width="44" height="36" fill="{Q["cream"]}"/><rect x="7" y="15" width="38" height="30" fill="#9cb8c8"/><path d="M7 38 Q20 26 30 34 Q38 28 45 32 L45 45 L7 45 Z" fill="{Q["olive"]}"/><circle cx="36" cy="22" r="4" fill="{Q["mustard"]}"/></g>'''
def painting(x,y,w,h,kind):
    inner={'land':f'<rect x="0" y="0" width="{w}" height="{h}" fill="#9cb8c8"/><path d="M0 {h*0.7} Q{w*0.3} {h*0.45} {w*0.6} {h*0.65} Q{w*0.8} {h*0.55} {w} {h*0.62} L{w} {h} L0 {h} Z" fill="{Q["olive"]}"/><circle cx="{w*0.72}" cy="{h*0.28}" r="{h*0.1}" fill="{Q["mustard"]}"/>',
           'still':f'<rect x="0" y="0" width="{w}" height="{h}" fill="#5a3a24"/><rect x="0" y="{h*0.75}" width="{w}" height="{h*0.25}" fill="{WOOD[1]}"/><circle cx="{w*0.35}" cy="{h*0.66}" r="{h*0.12}" fill="{Q["coral"]}"/><circle cx="{w*0.55}" cy="{h*0.68}" r="{h*0.1}" fill="{Q["mustard"]}"/><path d="M{w*0.62} {h*0.75} L{w*0.66} {h*0.35} L{w*0.78} {h*0.35} L{w*0.82} {h*0.75} Z" fill="{Q["green"]}"/>',
           'sea':f'<rect x="0" y="0" width="{w}" height="{h}" fill="#cfe0e6"/><rect x="0" y="{h*0.55}" width="{w}" height="{h*0.45}" fill="{Q["navy"]}"/><path d="M{w*0.3} {h*0.55} L{w*0.5} {h*0.2} L{w*0.5} {h*0.55} Z" fill="{Q["cream"]}"/><path d="M{w*0.22} {h*0.58} L{w*0.6} {h*0.58} L{w*0.54} {h*0.66} L{w*0.28} {h*0.66} Z" fill="{WOOD[1]}"/>',
           'abstract':f'<rect x="0" y="0" width="{w}" height="{h}" fill="{Q["cream"]}"/><rect x="{w*0.1}" y="{h*0.12}" width="{w*0.4}" height="{h*0.5}" fill="{Q["coral"]}"/><circle cx="{w*0.68}" cy="{h*0.6}" r="{h*0.22}" fill="{Q["navy"]}"/><rect x="{w*0.15}" y="{h*0.7}" width="{w*0.3}" height="{h*0.12}" fill="{Q["mustard"]}"/>'}[kind]
    return f'<g transform="translate({x} {y})"><rect x="-6" y="-6" width="{w+12}" height="{h+12}" rx="2" fill="{Q["mustard2"]}"/><rect x="-3" y="-3" width="{w+6}" height="{h+6}" fill="{Q["mustard"]}"/><svg x="0" y="0" width="{w}" height="{h}">{inner}</svg><rect x="{w/2-10}" y="{h+10}" width="20" height="5" rx="1" fill="{Q["cream"]}"/></g>'
def gallery():
    poly=[(300,880),(300,764),(272,736),(98,736),(64,702),(64,612),(98,578),(292,578),(326,544),(326,446),(292,412),(120,412),(86,378),(86,320),(120,286),(196,286),(196,196)]
    d,dense=poly_road(poly); pts=sample(dense,10,.07,.84)
    wall=f'<rect x="0" y="0" width="390" height="214" fill="#3f6b3a"/><rect x="0" y="0" width="390" height="214" fill="#2f5530" opacity=".0"/>'+''.join(f'<rect x="{k*26}" y="0" width="2" height="214" fill="#2f5530" opacity=".6"/>' for k in range(16))
    wall+=f'<rect x="0" y="170" width="390" height="44" fill="{WOOD[1]}"/><rect x="0" y="166" width="390" height="6" fill="{Q["mustard"]}"/>'
    wall+=painting(20,58,70,54,'land')+painting(100,74,36,48,'abstract')+painting(254,58,52,66,'still')+painting(316,70,56,42,'sea')
    wall+=f'<rect x="146" y="104" width="98" height="110" fill="{Q["mustard2"]}"/>'+gate_arch(164,62,(Q["coral"],Q["coral2"]))
    floor=parquet('#d1ad7c','#c8a272',7)+FLOORSHADE+SIDE(WOOD[2])
    props=[P(plinth(20,226,bust_top()),17,212,50,90), P(ropes(250,240,3,42),250,240,94,46), P(plinth(330,236,urn_top()),327,222,50,90) if False else P('',0,0,0,0),
        P(plinth(150,450,urn_top()),147,436,50,90), P(easel(240,440),240,440,52,84), P(bench(130,640) if False else '',0,0,0,0),
        P(plinth(160,610,bust_top()),157,596,50,90) if False else P('',0,0,0,0), P(bench(120,624),120,624,72,34), P(ropes(212,626,3,38),212,626,86,46),
        P(plinth(14,780,urn_top()),11,766,50,90), P(easel(120,770),120,770,52,84), P(plinth(338,600,bust_top()),335,586,50,90) if False else P('',0,0,0,0)]
    check('gallery',dense,pts,props)
    return page2('Gallery','5/30',321,'#d1ad7c',floor,wall,carpet(d,'#1f3a28',Q["green"],Q["mustard"],Q["green2"]),J(props),pts)
rooms={'Room-v2-library.dc.html':('F1 · Library',library()),
       'Room-v2-study.dc.html':('F2 · Study',study()),
       'Room-v2-greathall.dc.html':('F3 · Great hall',great_hall()),
       'Room-v2-ballroom.dc.html':('F4 · Ballroom',ballroom()),
       'Room-v2-gallery.dc.html':('F5 · Gallery',gallery())}
base='/home/claude/mockups/project'
c=json.load(open(f'{base}/canvas.json'))
ref=c['boards']['Room-v2-storeroom.dc.html']; x=ref['x']; y=ref['y']+ref['h']+200
for fn,(t,body) in rooms.items():
    open(f'{base}/{fn}','w').write(G['HEADQ']%t+body+'\n'+G['TAIL'])
    c['boards'].pop(fn,None); c['order']=[o for o in c['order'] if o!=fn]
    c['boards'][fn]={'x':x,'y':y,'w':390,'h':844,'title':t}; c['order'].append(fn); x+=470
json.dump(c,open(f'{base}/canvas.json','w'),ensure_ascii=False)
print('ok')
