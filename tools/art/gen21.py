import json, math, random, re
g20=open('./gen20.py').read()
exec(g20[:g20.index("\nrooms={")])
# ================= Second floor: Chapel, Secret passage, Map room, Armory
# ---------- CHAPEL: a cross-shaped route (side aisle, across, other aisle, up the middle), purple carpet, pale stone
def pew(x,y,w=110):
    return f'''<g transform="translate({x} {y})">{shadow(w/2,40,w/2+6,6)}<rect x="0" y="0" width="{w}" height="22" rx="3" fill="{WOOD[1]}"/><rect x="{w-10}" y="0" width="10" height="22" rx="3" fill="{WOOD[2]}"/><rect x="0" y="0" width="{w}" height="5" rx="2" fill="{WOOD[0]}"/>
      <rect x="2" y="20" width="{w-4}" height="12" rx="2" fill="{WOOD[0]}"/><rect x="2" y="30" width="{w-4}" height="5" fill="{WOOD[2]}"/><rect x="4" y="34" width="6" height="7" fill="{WOOD[2]}"/><rect x="{w-10}" y="34" width="6" height="7" fill="{WOOD[2]}"/></g>'''
def candle_stand(x,y,n=3):
    c=''.join(f'<g transform="translate({4+k*10} {-(k%2)*4})"><rect x="0" y="0" width="6" height="14" rx="2" fill="{Q["cream"]}"/><path d="M3 -8 C0 -3 1 0 3 0 C5 0 6 -3 3 -8 Z" fill="{Q["mustard"]}"/></g>' for k in range(n))
    return f'<g transform="translate({x} {y})">{shadow(16,70,14,4)}<circle cx="16" cy="6" r="22" fill="{Q["mustard"]}" opacity=".12"/><rect x="14" y="16" width="4" height="52" fill="{Q["mustard2"]}"/><path d="M6 70 L16 62 L26 70 Z" fill="{Q["mustard2"]}"/><rect x="0" y="12" width="{n*10+4}" height="5" rx="2" fill="{Q["mustard"]}"/>{c}</g>'
def font(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(26,60,26,6)}<rect x="18" y="26" width="16" height="30" fill="#c4bdb2"/><rect x="26" y="26" width="8" height="30" fill="#a39c8f"/><rect x="10" y="54" width="32" height="8" rx="2" fill="#a39c8f"/>
      <path d="M0 12 Q2 30 26 30 Q50 30 52 12 Z" fill="#c4bdb2"/><path d="M34 29 Q50 26 52 12 L40 12 Q40 24 34 29 Z" fill="#a39c8f"/><ellipse cx="26" cy="12" rx="26" ry="8" fill="#d6cfc2"/><ellipse cx="26" cy="12" rx="20" ry="5.4" fill="#6f9bb3"/><path d="M18 11 q5 -2 10 0" stroke="#a9cbe0" stroke-width="2" fill="none"/></g>'''
def lectern(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(20,62,18,5)}<rect x="16" y="20" width="8" height="40" fill="{WOOD[1]}"/><rect x="20" y="20" width="4" height="40" fill="{WOOD[2]}"/><path d="M6 62 L20 54 L34 62 Z" fill="{WOOD[2]}"/>
      <path d="M0 10 L40 4 L40 20 L0 26 Z" fill="{WOOD[1]}"/><path d="M2 8 Q12 2 20 6 Q28 0 38 4 L38 8 Q28 4 20 10 Q12 6 2 12 Z" fill="{Q["cream"]}"/><rect x="18" y="16" width="4" height="22" fill="{Q["coral"]}"/></g>'''
def stained(x,y,w,h,seed):
    r=random.Random(seed); cols=[Q["coral"],Q["navy"],Q["mustard"],Q["green"],'#7a4a7a',Q["pink"]]
    cells=''.join(f'<rect x="{c*w/3}" y="{rr*h/5}" width="{w/3}" height="{h/5}" fill="{r.choice(cols)}"/>' for rr in range(5) for c in range(3))
    return f'<g transform="translate({x} {y})"><path d="M-5 {h+4} L-5 {w/2} Q{w/2} -14 {w+5} {w/2} L{w+5} {h+4} Z" fill="#857e72"/><clipPath id="sg{seed}"><path d="M0 {h} L0 {w/2} Q{w/2} -6 {w} {w/2} L{w} {h} Z"/></clipPath><g clip-path="url(#sg{seed})">{cells}{"".join(f"<rect x=\"{c*w/3-1}\" y=\"0\" width=\"2\" height=\"{h}\" fill=\"#3a3644\"/>" for c in (1,2))}{"".join(f"<rect x=\"0\" y=\"{rr*h/5-1}\" width=\"{w}\" height=\"2\" fill=\"#3a3644\"/>" for rr in range(1,5))}</g></g>'
def chapel():
    poly=[(300,880),(300,650),(90,650),(90,420),(196,420),(196,196)]
    d,dense=poly_road(poly); pts=sample(dense,10,.1,.84)
    wall=f'<rect x="0" y="0" width="390" height="214" fill="#d6cfc2"/>{stones(390,214,51).replace("#978f83","#c4bdb2")}'
    wall+=stained(28,60,46,120,1)+stained(96,72,36,100,2)+stained(258,72,36,100,3)+stained(316,60,46,120,4)
    wall+=f'<g transform="translate(195 54)"><circle r="26" fill="#857e72"/><circle r="21" fill="{Q["navy"]}"/>'+''.join(f'<path d="M0 0 L{21*math.cos(a)} {21*math.sin(a)} A21 21 0 0 1 {21*math.cos(a+0.785)} {21*math.sin(a+0.785)} Z" fill="{[Q["coral"],Q["mustard"],Q["green"],"#7a4a7a"][i%4]}"/>' for i,a in enumerate([k*0.785 for k in range(8)]))+f'<circle r="6" fill="{Q["mustard"]}"/></g>'
    wall+=f'<rect x="150" y="100" width="90" height="114" fill="#a39c8f"/>'+gate_arch(164,62,('#7a4a7a','#5e3460'))+candle_stand(132,150,2)+candle_stand(236,150,2)
    floor=flag_floor(('#c9c2d0','#c4bdcb','#cdc6d4'),51,'#ada6b5')+FLOORSHADE+SIDE('#a39c8f')
    props=[P(candle_stand(20,236),14,236,40,72), P(font(318,250),318,250,52,62), P(lectern(250,312),250,312,40,62) if False else P('',0,0,0,0),
        P(pew(126,470,140),126,470,146,44), P(pew(126,530,140),126,530,146,44), P(pew(126,580,140) if False else '',0,0,0,0),
        P(pew(14,700,100),14,700,106,44), P(pew(14,756,100),14,756,106,44), P(pew(144,700,120),144,700,126,44), P(pew(144,756,120),144,756,126,44),
        P(pew(240,300,120),240,300,126,44), P(pew(240,356,120),240,356,126,44), P(lectern(20,318),20,318,40,62), P(vase_flowers(338,470),338,460,36,64), P(vase_flowers(338,560,Q["cream"]),338,550,36,64),
        P(candle_stand(14,500),8,500,40,72)]
    check('chapel',dense,pts,props)
    return page2('Chapel','5/40',351,'#ada6b5',floor,wall,carpet(d,'#3a1e3c','#7a4a7a',Q["mustard"],'#5e3460'),J(props),pts)
# ---------- SECRET PASSAGE: a jagged tunnel, lantern-lit dirt path on dark rock
def brazier(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(22,62,22,5)}<circle cx="22" cy="10" r="30" fill="{Q["mustard"]}" opacity=".14"/><path d="M10 62 L22 36 L34 62" stroke="#3a3644" stroke-width="4" fill="none"/><path d="M2 26 L42 26 L36 40 L8 40 Z" fill="#4a4652"/><path d="M28 26 L42 26 L36 40 L28 40 Z" fill="#35323c"/><ellipse cx="22" cy="26" rx="20" ry="5" fill="#5a5664"/>
      <path d="M10 26 C6 12 16 8 18 -4 C22 8 30 10 26 26 Z" fill="{Q["mustard"]}"/><path d="M16 26 C14 16 20 12 20 6 C24 14 26 18 24 26 Z" fill="{Q["coral"]}"/><path d="M24 26 C24 18 30 14 30 10 C34 18 34 22 32 26 Z" fill="{Q["mustard"]}"/></g>'''
def glowshrooms(x,y):
    one=lambda dx,dy,s: f'<g transform="translate({dx} {dy}) scale({s})"><rect x="9" y="12" width="10" height="14" rx="4" fill="#cfe0e6"/><path d="M0 15 Q14 -6 28 15 Z" fill="#7fd0c0"/><path d="M17 1 Q26 6 28 15 L20 15 Z" fill="#5ab0a0"/></g>'
    return f'<g transform="translate({x} {y})"><ellipse cx="24" cy="18" rx="34" ry="18" fill="#7fd0c0" opacity=".14"/>{shadow(24,28,26,5)}{one(0,0,1)}{one(26,8,.7)}{one(14,12,.55)}</g>'
def puddle(x,y): return f'<g transform="translate({x} {y})"><ellipse cx="24" cy="8" rx="26" ry="9" fill="#3a5060"/><ellipse cx="22" cy="7" rx="20" ry="6" fill="#4f6f86"/><path d="M14 6 q5 -2 10 0" stroke="#86a5b8" stroke-width="2" fill="none"/></g>'
def bat(x,y): return f'<g transform="translate({x} {y})"><path d="M0 6 Q6 -2 12 4 Q14 0 16 4 Q22 -2 28 6 Q22 4 20 10 Q16 8 14 12 Q12 8 8 10 Q6 4 0 6 Z" fill="#1e1a24"/><circle cx="12" cy="6" r="1" fill="{Q["mustard"]}"/><circle cx="16" cy="6" r="1" fill="{Q["mustard"]}"/></g>'
def key_item(x,y): return f'<g transform="translate({x} {y})">{shadow(14,10,14,3)}<circle cx="6" cy="6" r="6" fill="none" stroke="{Q["mustard"]}" stroke-width="3"/><rect x="11" y="4.5" width="18" height="3.4" fill="{Q["mustard"]}"/><rect x="23" y="7" width="3" height="5" fill="{Q["mustard"]}"/><rect x="27" y="7" width="3" height="4" fill="{Q["mustard"]}"/></g>'
def lever(x,y): return f'<g transform="translate({x} {y})"><rect x="0" y="0" width="18" height="26" rx="3" fill="#4a4652"/><rect x="7" y="-14" width="4" height="22" rx="2" fill="#8a8794" transform="rotate(-30 9 8)"/><circle cx="2" cy="-12" r="4" fill="{Q["coral"]}"/></g>'
def cave_floor(seed):
    r=random.Random(seed); g=f'<rect x="0" y="214" width="390" height="630" fill="#2e2a34"/>'
    for _ in range(26):
        cx,cy=r.randint(0,390),r.randint(230,840); rx=r.randint(22,48)
        g+=f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{rx*0.45}" fill="#36323d"/>'
    return g
def passage():
    poly=[(110,880),(120,790),(70,730),(150,672),(290,690),(330,610),(250,560),(110,560),(60,480),(140,420),(300,430),(320,350),(250,300),(196,290),(196,196)]
    d,dense=poly_road(poly); pts=sample(dense,10,.08,.86)
    wall=f'<rect x="0" y="0" width="390" height="214" fill="#3e3a46"/>'
    rr=random.Random(61)
    for _ in range(40):
        cx,cy=rr.randint(0,390),rr.randint(40,210); w=rr.randint(30,70)
        wall+=f'<ellipse cx="{cx}" cy="{cy}" rx="{w/2}" ry="{w/3}" fill="{rr.choice(("#4a4652","#45414e","#524e5c"))}"/>'
    wall+=''.join(f'<path d="M{sx} 56 L{sx+8} {56+h} L{sx+16} 56 Z" fill="#4a4652"/><path d="M{sx+8} 56 L{sx+8} {56+h} L{sx+16} 56 Z" fill="#35323c"/>' for sx,h in ((20,26),(70,18),(120,30),(250,22),(300,34),(350,20)))
    wall+=f'<path d="M152 214 L152 150 Q152 104 195 104 Q238 104 238 150 L238 214 Z" fill="#2a2630"/><path d="M160 214 L160 152 Q160 112 195 112 Q230 112 230 152 L230 214 Z" fill="#8a8794"/><path d="M195 112 Q230 112 230 152 L230 214 L195 214 Z" fill="#76737f"/>'
    wall+=''.join(f'<path d="M{160+k*14} {128+(k%2)*10} l10 4 l-4 10" stroke="#6e6b78" stroke-width="2" fill="none"/>' for k in range(5))+f'<circle cx="195" cy="166" r="9" fill="{Q["mustard"]}"/><path d="M193 162 h4 v8 h3 v4 h-10 v-4 h3 Z" fill="{DARK}"/>'
    wall+=sconce(120,128)+sconce(258,128)+cobweb(0,40)+cobweb(390,40,-1)+lever(326,150)+bat(64,96)+bat(286,80)
    floor=cave_floor(61)+FLOORSHADE+SIDE('#2a2630')
    props=[P(rubble(16,236),16,236,40,30), P(chest(260,232) if False else '',0,0,0,0), P(barrel(330,236,.75),330,236,36,44), P(brazier(250,330) if False else '',0,0,0,0),
        P(glowshrooms(18,330),12,320,60,40), P(key_item(220,360),220,356,30,16), P(brazier(16,560),12,546,44,76) if False else P('',0,0,0,0),
        P(chest(170,470),170,470,72,56), P(puddle(280,494),280,494,52,18),
        P(brazier(20,600),16,580,44,82), P(glowshrooms(190,610),184,600,60,40), P(rubble(346,500),346,500,40,30),
        P(puddle(200,760),200,760,52,18), P(rock(290,760,1),290,760,42,28), P(glowshrooms(320,800),314,790,60,40), P(rubble(16,800),16,800,40,30), P(barrel(30,240,.7) if False else '',0,0,0,0)]
    check('passage',dense,pts,props)
    path=(f'<path d="{d}" fill="none" stroke="{Q["mustard"]}" stroke-opacity=".10" stroke-width="80" stroke-linejoin="round" stroke-linecap="round"/>'
          f'<path d="{d}" fill="none" stroke="#1a1620" stroke-width="46" stroke-linejoin="round" stroke-linecap="round" transform="translate(0 4)"/><path d="{d}" fill="none" stroke="#8f7a56" stroke-width="44" stroke-linejoin="round" stroke-linecap="round"/><path d="{d}" fill="none" stroke="#cdb487" stroke-width="38" stroke-linejoin="round" stroke-linecap="round"/><path d="{d}" fill="none" stroke="#dcc49a" stroke-width="12" stroke-linejoin="round" stroke-linecap="round" transform="translate(-4 -3)"/>')
    return page2('Secret passage','5/30',391,'#2e2a34',floor,wall,path,J(props),pts)
def sample_avoid(dense,n,f0,f1,clear=40,gapmin=52):
    L=[0]
    for i in range(1,len(dense)): L.append(L[-1]+math.dist(dense[i-1],dense[i]))
    T=L[-1]; ok=[]
    for j,p in enumerate(dense):
        good=all(math.dist(p,q)>=clear for i,q in enumerate(dense) if abs(L[i]-L[j])>110)
        ok.append(good)
    best=None
    for sp in [x*2 for x in range(20,120)]:
        pts=[]; lastL=-1e9; lastp=None
        for j,p in enumerate(dense):
            if L[j]<T*f0 or L[j]>T*f1 or not ok[j]: continue
            if L[j]-lastL>=sp and (lastp is None or math.dist(p,lastp)>=gapmin) and all(math.dist(p,q)>=gapmin for q in pts):
                pts.append((round(p[0]),round(p[1]))); lastL=L[j]; lastp=p
        if len(pts)>=n: best=pts[:n]
    return best

# ---------- MAP ROOM: the floor IS a map; the path is a treasure route with a loop-de-loop
def map_floor():
    g=f'<rect x="0" y="214" width="390" height="630" fill="#6f9bb3"/>'+''.join(f'<rect x="{k*48}" y="214" width="1.4" height="630" fill="#86a5b8"/>' for k in range(9))+''.join(f'<rect x="0" y="{214+k*48}" width="390" height="1.4" fill="#86a5b8"/>' for k in range(14))
    lands=[ 'M-10 260 Q60 230 120 270 Q150 330 90 360 Q40 380 -10 350 Z', 'M250 240 Q330 220 400 250 L400 380 Q340 400 300 360 Q240 320 250 240 Z',
            'M-10 520 Q70 480 130 540 Q160 610 100 650 Q40 680 -10 640 Z', 'M230 600 Q300 560 400 590 L400 760 Q330 790 280 740 Q220 680 230 600 Z', 'M80 760 Q150 730 190 780 Q200 830 140 850 L60 850 Q40 800 80 760 Z']
    for dd in lands:
        g+=f'<path d="{dd}" fill="#d9c08a" transform="translate(3 5)" opacity=".5"/><path d="{dd}" fill="#e3cf9e"/><path d="{dd}" fill="none" stroke="#a4bf6e" stroke-width="8" opacity=".7"/>'
    g+=''.join(f'<g transform="translate({tx} {ty})"><path d="M0 12 L7 0 L14 12 Z" fill="{Q["olive"]}"/><path d="M7 0 L14 12 L9 12 Z" fill="{Q["olive2"]}"/></g>' for tx,ty in ((30,290),(56,300),(320,280),(344,300),(30,580),(300,650),(330,680)))
    g+=f'<g transform="translate(200 470) rotate(8)" opacity=".85">'+''.join(f'<path d="M{k*16} 0 q8 -14 16 0" fill="{Q["green"]}"/><path d="M{k*16+8} -7 q4 -2 8 7 l-8 0 Z" fill="{Q["green2"]}"/>' for k in range(3))+f'<circle cx="54" cy="-8" r="7" fill="{Q["green"]}"/><circle cx="56" cy="-10" r="1.6" fill="{DARK}"/></g>'
    g+=f'<g transform="translate(330 470)"><circle r="26" fill="{Q["cream"]}" opacity=".6"/><path d="M0 -24 L5 0 L0 24 L-5 0 Z" fill="{Q["coral"]}"/><path d="M-24 0 L0 5 L24 0 L0 -5 Z" fill="{DARK}" opacity=".7"/><circle r="3" fill="{Q["mustard"]}"/></g>'
    g+=f'<g transform="translate(150 610)"><path d="M-8 -8 L8 8 M8 -8 L-8 8" stroke="{Q["coral2"]}" stroke-width="5" stroke-linecap="round"/></g>'
    return g
def ship_model(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(30,64,30,5)}<rect x="12" y="50" width="36" height="12" rx="2" fill="{WOOD[1]}"/><rect x="40" y="50" width="8" height="12" fill="{WOOD[2]}"/><rect x="28" y="40" width="4" height="12" fill="{WOOD[2]}"/>
      <path d="M2 30 L58 30 L50 42 L10 42 Z" fill="{WOOD[1]}"/><path d="M40 30 L58 30 L50 42 L40 42 Z" fill="{WOOD[2]}"/><rect x="28" y="0" width="3" height="30" fill="{WOOD[2]}"/><path d="M31 2 Q48 12 31 26 Z" fill="{Q["cream"]}"/><path d="M28 6 Q16 14 28 24 Z" fill="{Q["cream2"]}"/><path d="M31 0 L42 3 L31 6 Z" fill="{Q["coral"]}"/></g>'''
def chart_desk(x,y):
    w,d_=130,58
    return f'''<g transform="translate({x} {y})">{shadow(w/2,d_+28,w/2+8,8)}<rect x="0" y="{d_-4}" width="{w}" height="14" rx="3" fill="{WOOD[1]}"/><rect x="6" y="{d_+8}" width="8" height="18" fill="{WOOD[2]}"/><rect x="{w-14}" y="{d_+8}" width="8" height="18" fill="{WOOD[2]}"/>
      <rect x="0" y="0" width="{w}" height="{d_}" rx="4" fill="{WOOD[0]}"/><g transform="translate(10 6) rotate(-3)"><rect x="0" y="0" width="84" height="44" rx="2" fill="{Q["cream"]}"/><path d="M10 30 q12 -16 26 -4 q10 8 22 -6 q8 -8 18 0" stroke="{Q["tan2"]}" stroke-width="2.4" fill="none"/><path d="M14 14 l4 4 l-4 4 l-4 -4 Z" fill="{Q["coral"]}"/><path d="M56 10 l20 26" stroke="{Q["coral"]}" stroke-width="2" stroke-dasharray="3 3"/></g>
      <g transform="translate(104 14)"><circle cx="8" cy="8" r="9" fill="{Q["mustard"]}"/><circle cx="8" cy="8" r="6" fill="{Q["cream"]}"/><path d="M8 3 L10 8 L8 13 L6 8 Z" fill="{Q["coral"]}"/></g><path d="M100 40 L114 52 M108 38 L112 54" stroke="#8a8794" stroke-width="2"/></g>'''
def maproom():
    pts_c=[(330,880),(330,790),(296,710),(220,664),(130,610),(108,520),(160,456),(250,456),(300,520),(290,610),(236,668),(150,708),(76,670),(52,570),(60,440),(100,350),(160,290),(196,240),(195,196)]
    d,dense=ctrl_road(pts_c); pts=sample_avoid(dense,10,.05,.92)
    wall=f'<rect x="0" y="0" width="390" height="214" fill="#2f5530"/>'+''.join(f'<rect x="{k*20}" y="0" width="10" height="214" fill="#3f6b3a" opacity=".5"/>' for k in range(20))
    wall+=f'<rect x="0" y="150" width="390" height="64" fill="{WOOD[1]}"/><rect x="0" y="146" width="390" height="6" fill="{WOOD[2]}"/>'+''.join(f'<rect x="{6+k*48}" y="158" width="40" height="48" rx="3" fill="{WOOD[0]}" opacity=".5"/>' for k in range(9))
    wall+=f'<g transform="translate(20 50)"><rect x="0" y="0" width="100" height="70" rx="2" fill="{WOOD[2]}"/><rect x="5" y="5" width="90" height="60" fill="{Q["cream"]}"/><path d="M14 40 q16 -20 34 -6 q12 10 36 -10" stroke="{Q["tan2"]}" stroke-width="3" fill="none"/><path d="M20 22 l18 6 l14 -10 l20 14" stroke="{Q["coral"]}" stroke-width="2" stroke-dasharray="3 3" fill="none"/><path d="M72 30 l-6 -6 M66 30 l6 -6" stroke="{Q["coral2"]}" stroke-width="3"/></g>'
    wall+=f'<g transform="translate(316 92)"><circle r="34" fill="none" stroke="{WOOD[1]}" stroke-width="7"/><circle r="9" fill="{WOOD[1]}"/>'+''.join(f'<rect x="-3" y="-46" width="6" height="18" rx="3" fill="{WOOD[0]}" transform="rotate({k*45})"/><rect x="-1.5" y="-34" width="3" height="28" fill="{WOOD[1]}" transform="rotate({k*45})"/>' for k in range(8))+'</g>'
    wall+=f'<rect x="146" y="104" width="98" height="110" fill="{WOOD[2]}"/>'+gate_arch(164,62,(Q["navy"],Q["navy2"]))
    floor=map_floor()+FLOORSHADE+SIDE(WOOD[2])
    props=[P(globe(20,226),20,226,40,62), P(ship_model(300,230),300,230,60,64), P(scrolls(240,250) if False else '',0,0,0,0),
        P(chart_desk(150,446) if False else '',0,0,0,0), P(telescope(330,236) if False else '',0,0,0,0), P(scrolls(330,560),330,550,44,52),
        P(chart_desk(236,760) if False else '',0,0,0,0), P(chest(14,780),14,780,72,56), P(telescope(200,600),192,600,56,74) if False else P('',0,0,0,0), P(chart_desk(150,460) if False else '',0,0,0,0), P(scrolls(110,460) if False else '',0,0,0,0), P(ship_model(170,520),170,520,60,64)]
    check('maproom',dense,pts,props)
    path=(f'<path d="{d}" fill="none" stroke="#2a140a" stroke-opacity=".18" stroke-width="44" stroke-linecap="round" stroke-linejoin="round" transform="translate(0 4)"/><path d="{d}" fill="none" stroke="#c9a77a" stroke-width="42" stroke-linecap="round" stroke-linejoin="round"/><path d="{d}" fill="none" stroke="{Q["cream"]}" stroke-width="36" stroke-linecap="round" stroke-linejoin="round"/>'
          f'<path d="{d}" fill="none" stroke="{Q["coral"]}" stroke-width="4" stroke-dasharray="8 7" stroke-linecap="round"/>')
    return page2('Map room','5/40',421,'#6f9bb3',floor,wall,path,J(props),pts)
# ---------- ARMORY: square vertical serpentine, sand training track, cool grey flags
def weapon_rack(x,y,w=80):
    swords=''.join(f'<g transform="translate({10+k*16} 0)"><rect x="2" y="-30" width="4" height="44" fill="#c4c1cc"/><rect x="4" y="-30" width="2" height="44" fill="#9a97a4"/><path d="M2 -30 L4 -38 L6 -30 Z" fill="#c4c1cc"/><rect x="-3" y="14" width="14" height="3" rx="1" fill="{Q["mustard"]}"/><rect x="2" y="17" width="4" height="10" fill="{WOOD[1]}"/></g>' for k in range(3))
    spear=f'<g transform="translate({w-16} 0)"><rect x="2" y="-44" width="3" height="76" fill="{WOOD[1]}"/><path d="M0 -44 L3.5 -56 L7 -44 Z" fill="#c4c1cc"/></g><g transform="translate({w-28} 0)"><rect x="2" y="-36" width="3" height="68" fill="{WOOD[1]}"/><path d="M3 -36 Q-8 -30 3 -22 Z" fill="#c4c1cc"/><path d="M5 -36 Q14 -30 5 -22 Z" fill="#9a97a4"/></g>'
    return f'''<g transform="translate({x} {y})">{shadow(w/2,44,w/2+6,6)}<rect x="0" y="36" width="{w}" height="8" rx="2" fill="{WOOD[1]}"/><rect x="0" y="6" width="{w}" height="6" rx="2" fill="{WOOD[0]}"/><rect x="2" y="6" width="6" height="38" fill="{WOOD[1]}"/><rect x="{w-8}" y="6" width="6" height="38" fill="{WOOD[2]}"/><g transform="translate(0 16)">{swords}{spear}</g></g>'''
def anvil(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(28,46,30,6)}<rect x="14" y="26" width="28" height="20" rx="2" fill="{WOOD[1]}"/><rect x="34" y="26" width="8" height="20" fill="{WOOD[2]}"/>
      <path d="M0 6 Q10 4 16 2 L46 2 L50 8 L44 14 L40 22 L18 22 L14 14 Q6 14 0 6 Z" fill="#5a5664"/><path d="M0 6 Q10 4 16 2 L46 2 L50 8 L16 8 Z" fill="#76737f"/><path d="M40 22 L44 14 L50 8 L50 12 L44 20 Z" fill="#3a3644"/>
      <g transform="translate(26 -10) rotate(30)"><rect x="0" y="0" width="4" height="22" fill="{WOOD[0]}"/><rect x="-6" y="-6" width="16" height="8" rx="2" fill="#4a4652"/></g></g>'''
def target(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(26,72,26,5)}<path d="M8 72 L20 40 M44 72 L32 40" stroke="{WOOD[1]}" stroke-width="4"/>
      <circle cx="26" cy="28" r="26" fill="#d9b46a"/><circle cx="26" cy="28" r="20" fill="{Q["cream"]}"/><circle cx="26" cy="28" r="14" fill="{Q["coral"]}"/><circle cx="26" cy="28" r="8" fill="{Q["cream"]}"/><circle cx="26" cy="28" r="4" fill="{Q["mustard"]}"/>
      <g transform="translate(26 26) rotate(-24)"><rect x="0" y="-1" width="26" height="2.4" fill="{WOOD[1]}"/><path d="M22 -4 L30 0 L22 4 Z" fill="{Q["cream"]}"/></g><g transform="translate(18 34) rotate(18)"><rect x="0" y="-1" width="24" height="2.4" fill="{WOOD[1]}"/><path d="M20 -4 L28 0 L20 4 Z" fill="{Q["navy"]}"/></g></g>'''
def arrow_barrel(x,y):
    arr=''.join(f'<g transform="translate({10+k*7} 8) rotate({-10+k*6})"><rect x="0" y="-22" width="2" height="24" fill="{WOOD[0]}"/><path d="M-2 -22 L1 -28 L4 -22 Z" fill="{[Q["coral"],Q["cream"],Q["navy"]][k%3]}"/></g>' for k in range(4))
    return f'<g transform="translate({x} {y})">{arr}{barrel(0,0,.8)}</g>'
def armory():
    poly=[(330,880),(330,420),(196,420),(196,712),(60,712),(60,300),(196,300),(196,196)]
    d,dense=poly_road(poly); pts=sample(dense,10,.1,.88)
    wall=f'<rect x="0" y="0" width="390" height="214" fill="{Q["lav"]}"/>{stones(390,214,71)}'
    for rx in (14,262):
        wall+=f'<rect x="{rx}" y="66" width="114" height="8" rx="2" fill="{WOOD[1]}"/><rect x="{rx}" y="140" width="114" height="8" rx="2" fill="{WOOD[1]}"/>'
        wall+=''.join(f'<g transform="translate({rx+10+k*20} 50)"><rect x="3" y="0" width="4" height="96" fill="#c4c1cc"/><rect x="5" y="0" width="2" height="96" fill="#9a97a4"/><path d="M3 0 L5 -10 L7 0 Z" fill="#c4c1cc"/><rect x="-2" y="70" width="14" height="4" fill="{Q["mustard"]}"/><rect x="3" y="74" width="4" height="16" fill="{WOOD[1]}"/></g>' for k in range(5))
    for sx,c,c2 in ((54,Q["navy"],Q["navy2"]),(302,Q["coral"],Q["coral2"])):
        wall+=f'<g transform="translate({sx} 156)"><path d="M0 0 L32 0 L32 18 Q32 34 16 40 Q0 34 0 18 Z" fill="{c}"/><path d="M16 0 L32 0 L32 18 Q32 34 16 40 Z" fill="{c2}"/><path d="M6 8 L26 8 M16 4 L16 30" stroke="{Q["mustard"]}" stroke-width="3"/></g>'
    wall+=f'<g transform="translate(195 34)"><path d="M-34 -6 L34 54 M34 -6 L-34 54" stroke="{WOOD[1]}" stroke-width="5"/><path d="M-40 -14 Q-24 -16 -26 4 Q-36 0 -40 -14 Z M40 -14 Q24 -16 26 4 Q36 0 40 -14 Z" fill="#a8a5b2"/></g>'
    wall+=f'<rect x="148" y="104" width="94" height="110" fill="{Q["lav2"]}"/>'+iron_door(164,62,('#5a5664','#4a4652'))
    floor=flag_floor(('#8f949c','#94999f','#8a8f97'),71,'#767b83')+FLOORSHADE+SIDE(Q["lav2"])
    props=[P(weapon_rack(96,236,70),96,196,70,84), P(armor(130,344),124,328,44,96), P(target(290,226),290,226,52,74), P(arrow_barrel(240,250),240,226,44,70),
        P(shield_stand(94,470),94,470,70,50), P(anvil(100,580),100,570,52,52), P(weapon_rack(228,600,70),228,560,70,84), P(armor(244,450),238,434,44,96),
        P(target(14,770),14,770,52,74), P(arrow_barrel(90,790),90,766,44,70), P(barrel(240,780,.8),240,780,40,46), P(armor(352,450) if False else '',0,0,0,0)]
    check('armory',dense,pts,props)
    path=(f'<path d="{d}" fill="none" stroke="#5a4a32" stroke-opacity=".5" stroke-width="46" stroke-linejoin="round" transform="translate(0 4)"/><path d="{d}" fill="none" stroke="#b39a68" stroke-width="44" stroke-linejoin="round"/><path d="{d}" fill="none" stroke="#e3cf9e" stroke-width="38" stroke-linejoin="round"/>'
          f'<path d="{d}" fill="none" stroke="#d2bc88" stroke-width="18" stroke-dasharray="5 14" stroke-linejoin="round"/>')
    return page2('Armory','5/40',461,'#767b83',floor,wall,path,J(props),pts)
rooms={'Room-v2-chapel.dc.html':('S1 · Chapel',chapel()),
       'Room-v2-passage.dc.html':('S2 · Secret passage',passage()),
       'Room-v2-maproom.dc.html':('S3 · Map room',maproom()),
       'Room-v2-armory.dc.html':('S4 · Armory',armory())}
base='/home/claude/mockups/project'
c=json.load(open(f'{base}/canvas.json'))
ref=c['boards']['Room-v2-library.dc.html']; x=ref['x']; y=ref['y']+ref['h']+200
for fn,(t,body) in rooms.items():
    open(f'{base}/{fn}','w').write(G['HEADQ']%t+body+'\n'+G['TAIL'])
    c['boards'].pop(fn,None); c['order']=[o for o in c['order'] if o!=fn]
    c['boards'][fn]={'x':x,'y':y,'w':390,'h':844,'title':t}; c['order'].append(fn); x+=470
json.dump(c,open(f'{base}/canvas.json','w'),ensure_ascii=False)
print('ok')
