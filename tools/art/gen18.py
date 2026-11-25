import json, math, random
g17=open('./gen17.py').read()
exec(g17[:g17.index("\nrooms={")])
# ================= Cellars, round 3: each room gets its own path shape and path material
def bez_pts(ps,steps=24):
    out=[]
    for i in range(len(ps)-1):
        a=ps[i-1] if i>0 else ps[i]; b=ps[i]; c=ps[i+1]; e=ps[i+2] if i+2<len(ps) else c
        p1=(b[0]+(c[0]-a[0])/6,b[1]+(c[1]-a[1])/6); p2=(c[0]-(e[0]-b[0])/6,c[1]-(e[1]-b[1])/6)
        for k in range(steps):
            t=k/steps; mt=1-t
            out.append((mt**3*b[0]+3*mt*mt*t*p1[0]+3*mt*t*t*p2[0]+t**3*c[0], mt**3*b[1]+3*mt*mt*t*p1[1]+3*mt*t*t*p2[1]+t**3*c[1]))
    out.append(ps[-1]); return out
def poly_pts(ps,steps=40):
    out=[]
    for i in range(len(ps)-1):
        for k in range(steps): t=k/steps; out.append((ps[i][0]+(ps[i+1][0]-ps[i][0])*t, ps[i][1]+(ps[i+1][1]-ps[i][1])*t))
    out.append(ps[-1]); return out
def sample(dense,n,f0,f1):
    L=[0]
    for i in range(1,len(dense)): L.append(L[-1]+math.dist(dense[i-1],dense[i]))
    res=[]
    for k in range(n):
        target=L[-1]*(f0+(f1-f0)*k/(n-1)); j=next(i for i in range(len(L)) if L[i]>=target)
        res.append((round(dense[j][0]),round(dense[j][1])))
    return res
def nodes_at(base,pts):
    return ''.join(G['node'](base+k,x,y,'done' if k<5 else 'cur' if k==5 else 'next' if k==6 else 'lock') for k,(x,y) in enumerate(pts))
def page2(name,count,base_n,bg,ground,wall,path,props,pts):
    mx,my=pts[5]
    return f'''<div style="{SC}background:{bg}">
  <svg width="390" height="844" style="position:absolute;left:0;top:0">{ground}{path}{wall}{STEP}<rect x="0" y="214" width="390" height="10" fill="#2a140a" opacity=".1"/>{props}</svg>
  <div style="position:absolute;left:0;right:0;top:0;height:56px;background:{Q["purple"]};z-index:4">
    {pill(14,8,98,40,Q["mustard"],Q["mustard2"],'Castle',16)}<div style="position:absolute;left:126px;top:12px;{TT};font-size:24px;color:{Q["cream"]}">{name}</div><b style="position:absolute;right:16px;top:18px;font:700 15px Fredoka,sans-serif;color:{Q["cream"]}">{count}</b></div>
  {nodes_at(base_n,pts)}
  <div style="position:absolute;left:{mx-18}px;top:{my-48}px;z-index:4">{sv('mouse',36)}</div>
</div>'''
# path materials
def path_rug(d):       # a woven runner: burgundy with gold borders
    return (f'<path d="{d}" fill="none" stroke="#2a140a" stroke-opacity=".18" stroke-width="46" stroke-linejoin="round" transform="translate(0 4)"/>'
            f'<path d="{d}" fill="none" stroke="#6e1f22" stroke-width="44" stroke-linejoin="round"/><path d="{d}" fill="none" stroke="{Q["mustard"]}" stroke-width="36" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="#a8353a" stroke-width="30" stroke-linejoin="round"/><path d="{d}" fill="none" stroke="#c4554a" stroke-width="6" stroke-dasharray="8 10" stroke-linejoin="round"/>')
def path_sand(d):      # big sandstone slabs
    return (f'<path d="{d}" fill="none" stroke="#7d6a48" stroke-width="44" stroke-linejoin="round" stroke-linecap="round" transform="translate(0 3)"/><path d="{d}" fill="none" stroke="#dcc28c" stroke-width="40" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="#b89e68" stroke-width="40" stroke-dasharray="2.5 30" stroke-linejoin="round"/><path d="{d}" fill="none" stroke="#e9d4a6" stroke-width="10" stroke-linejoin="round" stroke-linecap="round" transform="translate(-6 -4)" opacity=".7"/>')
def path_cobble(d):    # cool grey cobbles, square corners like a corridor
    return (f'<path d="{d}" fill="none" stroke="#1a1620" stroke-opacity=".5" stroke-width="46" stroke-linejoin="round" transform="translate(0 4)"/><path d="{d}" fill="none" stroke="#55515e" stroke-width="44" stroke-linejoin="round"/><path d="{d}" fill="none" stroke="#b9b6c2" stroke-width="38" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="#9a97a4" stroke-width="38" stroke-dasharray="2 13" stroke-linejoin="round"/><path d="{d}" fill="none" stroke="#9a97a4" stroke-width="2" stroke-linejoin="round"/>')
def dpoly(ps): return 'M '+' L '.join(f'{x} {y}' for x,y in ps)
# ---------- STOREROOM: switchbacks across the room, a red runner rug
def storeroom3():
    ctrl=[(320,880),(306,790),(220,742),(110,726),(58,676),(96,612),(196,594),(296,580),(334,518),(284,462),(186,452),(86,436),(56,372),(104,318),(170,290),(196,246),(195,196)]
    d=G['crd'](ctrl); dense=bez_pts(ctrl); pts=sample(dense,10,.09,.83)
    wall=indoor_wall(Q["lav"],Q["lav2"],21)
    wall+=wall_shelf(14,120,130,[('jar',Q["cream"],Q["cream2"]),('jar',Q["coral"],Q["coral2"]),('box',Q["tan"],Q["tan2"]),('cheese',0,0),('jar',Q["olive"],Q["olive2"])])
    wall+=wall_shelf(14,170,130,[('box',Q["tan"],Q["tan2"]),('box',WOOD[0],WOOD[1]),('jar',Q["navy"],Q["navy2"]),('jar',Q["mustard"],Q["mustard2"])])
    wall+=wall_shelf(248,120,130,[('bottle',Q["green"],Q["green2"]),('bottle',Q["coral"],Q["coral2"]),('box',Q["tan"],Q["tan2"]),('jar',Q["cream"],Q["cream2"]),('jar',Q["pink"],Q["pink2"])])
    wall+=wall_shelf(248,170,130,[('cheese',0,0),('cheese',0,0),('box',Q["tan"],Q["tan2"]),('jar',Q["olive"],Q["olive2"])])
    wall+=f'<rect x="152" y="106" width="86" height="108" fill="{Q["lav2"]}"/>'+iron_door()+mousehole(130,206)+cobweb(0,0)+cobweb(390,0,-1)
    floor=flag_floor(('#8e897d','#918c80','#8b8679'),3,'#77736a')+FLOORSHADE+SIDE(Q["lav2"])
    props=''.join([crate_closed(18,232,44), barrel(300,230,.75), sack(340,250,Q["cream"],.8),
        cheese_stack(196,358) if False else '', crate_closed(150,350,44), sack(206,362,Q["mustard"],.85), rope(264,380),
        barrel(14,452,.75), chest(196,482), crate_closed(120,500,40),
        sack(326,610,Q["cream"],.85) if False else '', cheese_stack(150,640), crate_closed(230,628,44),
        barrel(334,648,.75) if False else '',
        crate_closed(14,766,48), sack(70,782,Q["cream"],.85), barrel(140,780,.8), cheese_stack(220,800) if False else ''])
    return page2('Storeroom','5/20',101,'#77736a',floor,wall,path_rug(d),props,pts),pts
# ---------- WINE CELLAR: one long sweep up the left side and across the top, cellar furniture in the open middle
def wine3():
    ctrl=[(120,880),(84,780),(54,680),(52,580),(72,490),(118,412),(186,360),(256,326),(292,286),(244,244),(200,226),(195,196)]
    d=G['crd'](ctrl); dense=bez_pts(ctrl); pts=sample(dense,10,.1,.8)
    wall=brick_wall(5)
    for ax in (16,262):
        wall+=f'<path d="M{ax} 214 L{ax} 92 Q{ax} 52 {ax+56} 52 Q{ax+112} 52 {ax+112} 92 L{ax+112} 214 Z" fill="#3a2018"/><g transform="translate({ax+8} 74)">{bottle_rack_front(96,130,6,7)}</g>'
        wall+=f'<path d="M{ax-8} 214 L{ax-8} 92 Q{ax-8} 44 {ax+56} 44 Q{ax+120} 44 {ax+120} 92 L{ax+120} 214 L{ax+112} 214 L{ax+112} 92 Q{ax+112} 52 {ax+56} 52 Q{ax} 52 {ax} 92 L{ax} 214 Z" fill="{Q["lav"]}"/>'
    wall+=f'<rect x="150" y="100" width="90" height="114" fill="{Q["lav"]}"/><rect x="214" y="100" width="26" height="114" fill="{Q["lav2"]}"/>'+iron_door()
    floor=flag_floor(('#4f5562','#525866','#4c5260'),9,'#3e434e')+FLOORSHADE+SIDE(BRICK[2])
    rug=f'<g transform="translate(150 420)"><rect x="0" y="4" width="200" height="130" rx="8" fill="#2a140a" opacity=".2"/><rect x="0" y="0" width="200" height="130" rx="8" fill="{Q["navy"]}"/><rect x="10" y="10" width="180" height="110" rx="5" fill="{Q["navy2"]}"/><rect x="22" y="22" width="156" height="86" rx="4" fill="#5e3460"/><path d="M100 30 L150 65 L100 100 L50 65 Z" fill="{Q["mustard"]}" opacity=".85"/></g>'
    props=''.join([barrel(14,232,.75), barrel(56,240,.7), grapes(110,270) if False else '',
        rug, candle_table(224,452), rack(160,600,72,16,54), tun(240,580,.95),
        grapes(160,712), crate(214,736,'cabbage').replace(Q["green"],'#5e3460').replace(Q["green2"],'#4a2850').replace('#8fb85a','#7a4a7a'),
        barrel(300,750,.8), barrel(340,770,.75), rack(300,360,72,16,50) if False else '', barrel(334,380,.7), grapes(320,446)])
    return page2('Wine cellar','5/20',121,'#3e434e',floor,wall,path_sand(d),props,pts),pts
# ---------- DUNGEON: a corridor with square turns, cells sit between the corridors
def cell2(x,y,w,h,inside):
    d=26
    back=f'<rect x="0" y="0" width="{w}" height="{h}" fill="#55515e"/><rect x="0" y="0" width="{w}" height="10" fill="#45414e"/>'+''.join(f'<rect x="{6+(r%2)*14+k*28}" y="{14+r*22}" width="22" height="16" rx="3" fill="#605c6a"/>' for r in range(int(h/22)) for k in range(int(w/28)) if 6+(r%2)*14+k*28<w-20 and 14+r*22<h-18)
    bars=''.join(f'<rect x="{k*w/6-2}" y="-8" width="4" height="{h+8}" fill="#a8a5b2"/><rect x="{k*w/6+0.6}" y="-8" width="1.4" height="{h+8}" fill="#76737f"/>' for k in range(1,6))
    frame=f'<rect x="-3" y="-12" width="{w+6}" height="7" rx="2" fill="#a8a5b2"/><rect x="-3" y="{h-4}" width="{w+6}" height="7" rx="2" fill="#8a8794"/><rect x="-4" y="-12" width="7" height="{h+15}" fill="#a8a5b2"/><rect x="{w-3}" y="-12" width="7" height="{h+15}" fill="#76737f"/>'
    lock=f'<rect x="{w*0.5-7}" y="{h*0.42}" width="14" height="16" rx="2" fill="{Q["mustard"]}"/><rect x="{w*0.5-1}" y="{h*0.42+5}" width="2" height="6" fill="{DARK}"/><path d="M{w*0.5-4} {h*0.42} v-4 a4 4 0 0 1 8 0 v4" stroke="{Q["mustard2"]}" stroke-width="2.4" fill="none"/>'
    return f'<g transform="translate({x} {y})">{shadow(w/2,h+4,w/2+8,7)}{back}{inside}{bars}{frame}{lock}</g>'
def bed_inside(w,h):
    return f'''<g transform="translate(10 {h-46})"><rect x="0" y="6" width="64" height="34" rx="4" fill="#b8924a"/><rect x="0" y="0" width="64" height="30" rx="4" fill="#d9b46a"/>{''.join(f'<path d="M{6+k*8} 6 l6 3" stroke="#b8924a" stroke-width="1.6" stroke-linecap="round"/>' for k in range(7))}
      <rect x="4" y="4" width="18" height="14" rx="5" fill="{Q["cream"]}"/><rect x="26" y="2" width="38" height="30" rx="4" fill="{Q["coral"]}"/><rect x="26" y="24" width="38" height="8" rx="3" fill="{Q["coral2"]}"/><path d="M34 2 L34 32 M46 2 L46 32" stroke="{Q["coral2"]}" stroke-width="2"/></g>
      <g transform="translate({w-36} {h-24})"><ellipse cx="12" cy="12" rx="12" ry="5" fill="{WOOD[2]}"/><ellipse cx="12" cy="9" rx="12" ry="5" fill="{WOOD[1]}"/><ellipse cx="12" cy="8" rx="8" ry="3" fill="#6f9bb3"/></g>'''
def cheese_inside(w,h):
    return f'''<g transform="translate({w/2-36} {h-50})"><ellipse cx="36" cy="40" rx="36" ry="10" fill="{Q["cream2"]}"/><ellipse cx="36" cy="37" rx="34" ry="9" fill="{Q["cream"]}"/>
      <path d="M8 36 L8 14 L60 2 L60 24 Z" fill="{Q["mustard2"]}"/><path d="M8 14 L60 2 L68 8 L16 20 Z" fill="#f0d07a"/><path d="M8 14 L16 20 L16 42 L8 36 Z" fill="{Q["mustard"]}"/><path d="M60 2 L68 8 L68 30 L60 24 Z" fill="{Q["mustard"]}"/>
      <circle cx="26" cy="24" r="3.4" fill="#a87a24"/><circle cx="42" cy="20" r="2.6" fill="#a87a24"/><circle cx="36" cy="30" r="2.2" fill="#a87a24"/></g>'''
def dungeon3():
    poly=[(300,880),(300,724),(74,724),(74,544),(316,544),(316,368),(196,368),(196,196)]
    d=dpoly(poly); dense=poly_pts(poly); pts=sample(dense,10,.1,.84)
    wall=indoor_wall('#6a6672','#55515e',33).replace('fill="#978f83" opacity=".45"','fill="#7a7682" opacity=".8"')
    wall+=f'<g transform="translate(286 70)"><rect x="-6" y="-6" width="62" height="38" rx="4" fill="{DSTONE[2]}"/><rect x="0" y="0" width="50" height="26" fill="#9cb8c8"/>'+''.join(f'<rect x="{6+k*10}" y="0" width="3" height="26" fill="#3a3644"/>' for k in range(5))+'</g>'
    wall+=f'<path d="M290 96 L336 96 L380 214 L250 214 Z" fill="#f1e3c2" opacity=".08"/>'
    wall+=chains_wall(40,96)+chains_wall(100,120)+sconce(132,150)+sconce(246,150)
    wall+=f'<rect x="152" y="106" width="86" height="108" fill="{DSTONE[2]}"/>'+iron_door(164,62,('#5a5664','#4a4652'),True)
    floor=flag_floor(('#3e3a48','#403c4a','#3c3846'),17,'#2e2a36')+FLOORSHADE+SIDE(DSTONE[2])
    floor+=''.join(f'<path d="M{mx} {my} q6 -6 12 0 q6 -4 10 2" fill="{Q["green2"]}" opacity=".8"/>' for mx,my in ((24,500),(350,470),(150,690),(344,780),(20,660)))
    props=''.join([bench(22,246), bucket(110,300), barrel(240,236,.75), crate_closed(290,250,44),
        cell2(122,404,160,100,bed_inside(160,100)),
        cell2(118,592,148,96,cheese_inside(148,96)),
        rubble(342,420), bucket(344,600) if False else '', ball_chain(22,600),
        chest(130,768), barrel(14,770,.8), ball_chain(220,790), rubble(340,780)])
    return page2('Dungeon','5/20',141,'#2e2a36',floor,wall,path_cobble(d),props,pts),pts
out={}
for fn,t,fnc in (('Room-v2-storeroom.dc.html','C1 · Storeroom',storeroom3),('Room-v2-winecellar.dc.html','C2 · Wine cellar',wine3),('Room-v2-dungeon.dc.html','C3 · Dungeon',dungeon3)):
    body,pts=fnc(); print(fn,pts); out[fn]=(t,body)
base='/home/claude/mockups/project'
for fn,(t,body) in out.items(): open(f'{base}/{fn}','w').write(G['HEADQ']%t+body+'\n'+G['TAIL'])
print('ok')
