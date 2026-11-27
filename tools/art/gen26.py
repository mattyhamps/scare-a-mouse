import json, math, re
# ================= Towers and roof: Battlements, Aviary, Watchtower, Belfry, Crown vault
# Builds on gen25.py's helpers (and so every floor before it), same flat style: the light half of each
# object on the left, a darker half on the right, one soft shadow under anything that stands on the floor.
# Run from this folder: python3 gen26.py && python3 export_towers.py
g25=open('./gen25.py',encoding='utf-8').read()
exec(g25[:g25.index("H5['Royal chambers']=")])
H6={}; P6={}
def add6(name,svg,box,sc=1): P6[name]=[[round(v*sc,1) for v in box],re.sub(r'\s+',' ',svg if sc==1 else f'<g transform="scale({sc})">{svg}</g>').strip()]
SKY=('#bcd8e8','#a9cbe0','#8fb6d0')
GREY=('#b9b6b0','#a09d97','#85827c')   # the castle's outer stone
SLATE=('#6e7a8c','#57627a')

# ---------- BATTLEMENTS (the defenders' wall)
def cloud(x,y,s=1): return f'<g transform="translate({x} {y}) scale({s})" fill="#fff"><ellipse cx="0" cy="0" rx="22" ry="9"/><ellipse cx="-12" cy="-5" rx="11" ry="9"/><ellipse cx="8" cy="-8" rx="13" ry="11"/></g>'
def far_tower(x,y,h,flag):
    return f'''<g transform="translate({x} {y})"><rect x="-18" y="0" width="36" height="{h}" fill="{GREY[1]}"/><rect x="2" y="0" width="16" height="{h}" fill="{GREY[2]}"/>
      <path d="M-24 2 L0 -40 L24 2 Z" fill="{SLATE[0]}"/><path d="M0 -40 L24 2 L0 2 Z" fill="{SLATE[1]}"/><rect x="-1" y="-58" width="2" height="20" fill="{IRON[2]}"/><path d="M1 -58 L18 -53 L1 -48 Z" fill="{flag}"/>
      <rect x="-5" y="24" width="10" height="18" rx="5" fill="#4a4652"/></g>'''
def merlons(x0,x1,y,h=12,w=16,gap=12,c=GREY[0]): return ''.join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"/>' for x in range(int(x0),int(x1),w+gap))
def battlements_head():
    w=f'<rect x="0" y="0" width="390" height="214" fill="{SKY[1]}"/><rect x="0" y="0" width="390" height="70" fill="{SKY[0]}"/>'
    w+=cloud(70,40,1.1)+cloud(300,28,0.9)+cloud(205,70,0.7)
    w+=f'<path d="M0 150 Q60 128 120 146 Q200 120 270 144 Q330 128 390 140 L390 214 L0 214 Z" fill="{Q["olive"]}" opacity=".55"/>'   # hills far below
    w+=far_tower(44,96,90,CRIM[0])+far_tower(346,90,96,Q["navy"])
    # the wall-walk's far end: a parapet with merlons, and the tower with the door in the middle
    w+=f'<rect x="0" y="172" width="390" height="42" fill="{GREY[1]}"/>'+merlons(0,390,160)+''.join(f'<rect x="{x}" y="{176+((x//44)%2)*12}" width="40" height="10" rx="2" fill="{GREY[2]}" opacity=".5"/>' for x in range(2,390,44))
    w+=f'<rect x="132" y="70" width="126" height="144" fill="{GREY[0]}"/><rect x="200" y="70" width="58" height="144" fill="{GREY[1]}"/>'+merlons(130,262,56,14,18,9)
    w+=''.join(f'<rect x="{136+(r%2)*22+k*44}" y="{80+r*22}" width="40" height="16" rx="2" fill="{GREY[1]}" opacity=".45"/>' for r in range(3) for k in range(3))
    w+=f'<rect x="146" y="100" width="98" height="114" fill="{GREY[2]}"/>'+gate_arch(164,62,(WOOD[1],WOOD[2]))+f'<circle cx="216" cy="172" r="3.4" fill="{GOLD[0]}"/>'
    w+=f'<rect x="194" y="24" width="2" height="34" fill="{IRON[2]}"/><path d="M196 24 L226 31 L196 38 Z" fill="{CRIM[0]}"/><path d="M196 31 L226 31 L196 38 Z" fill="{CRIM[1]}"/>'
    return w
def wheel(cx,cy,r,c=WOOD[2]): return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c}" stroke-width="{r*0.28:.1f}"/>' + ''.join(f'<path d="M{cx} {cy} L{cx+r*math.cos(math.radians(a)):.1f} {cy+r*math.sin(math.radians(a)):.1f}" stroke="{c}" stroke-width="{r*0.16:.1f}"/>' for a in range(0,360,60)) + f'<circle cx="{cx}" cy="{cy}" r="{r*0.25:.1f}" fill="{IRON[1]}"/>'
def cannon(x,y,s=1):   # an iron cannon on a wooden carriage, pointing left
    return f'''<g transform="translate({x} {y}) scale({s})"><path d="M18 30 L70 30 L80 44 L10 44 Z" fill="{WOOD[1]}"/><path d="M45 30 L70 30 L80 44 L45 44 Z" fill="{WOOD[2]}"/>
      <path d="M4 16 Q4 10 10 10 L62 6 Q74 6 74 18 Q74 30 62 30 L10 26 Q4 26 4 20 Z" fill="{IRON[1]}"/><path d="M40 8 L62 6 Q74 6 74 18 Q74 30 62 30 L40 28 Z" fill="{IRON[2]}"/>
      <rect x="0" y="10" width="7" height="16" rx="2" fill="{IRON[0]}"/><circle cx="76" cy="18" r="4" fill="{IRON[2]}"/><path d="M24 9 L24 27 M50 7 L50 29" stroke="{IRON[0]}" stroke-width="2"/>
      {wheel(26,44,11)}{wheel(64,44,11)}</g>'''
def cannon_s(x,y): return f'<g transform="translate({x} {y})">{shadow(44,56,42,5)}{cannon(0,0,1)}</g>'
def cannonballs(x,y):
    balls=[(14,40),(30,40),(46,40),(22,27),(38,27),(30,14)]
    return f'<g transform="translate({x} {y})">{shadow(30,50,28,4)}<rect x="2" y="46" width="56" height="5" rx="2" fill="{WOOD[2]}"/>'+''.join(f'<circle cx="{bx}" cy="{by}" r="8.5" fill="{IRON[2]}"/><circle cx="{bx-3}" cy="{by-3}" r="2.6" fill="{IRON[0]}"/>' for bx,by in balls)+'</g>'
def catapult(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(56,100,54,6)}<path d="M10 86 L100 86" stroke="{WOOD[2]}" stroke-width="8" stroke-linecap="round"/>
      <path d="M30 86 L50 40 L70 86" stroke="{WOOD[1]}" stroke-width="7" fill="none" stroke-linejoin="round"/><path d="M50 40 L70 86" stroke="{WOOD[2]}" stroke-width="7"/>
      <path d="M50 42 L96 6" stroke="{WOOD[1]}" stroke-width="6" stroke-linecap="round"/><path d="M50 42 L20 66" stroke="{WOOD[1]}" stroke-width="6" stroke-linecap="round"/>
      <path d="M86 2 Q98 -6 106 4 Q100 14 90 12 Z" fill="{WOOD[2]}"/><circle cx="96" cy="2" r="5" fill="{GREY[1]}"/>
      <rect x="10" y="62" width="20" height="16" rx="2" fill="{GREY[1]}"/><rect x="21" y="62" width="9" height="16" rx="2" fill="{GREY[2]}"/><path d="M20 62 L20 56" stroke="{Q["tan"]}" stroke-width="2"/>
      <circle cx="50" cy="42" r="4" fill="{IRON[1]}"/>{wheel(20,90,10)}{wheel(90,90,10)}</g>'''
def sentry_box(x,y):
    stripes=''.join(f'<path d="M{6+k*12} 24 L{18+k*12} 24 L{14+k*12} 8 L{10+k*12} 8 Z" fill="{CRIM[0] if k%2==0 else Q["cream"]}"/>' for k in range(4))
    return f'''<g transform="translate({x} {y})">{shadow(30,122,30,5)}{two(6,24,48,98,WOOD[1],WOOD[2],2)}<rect x="12" y="34" width="36" height="76" rx="2" fill="#3a2414"/>
      <path d="M2 26 L30 2 L58 26 Z" fill="{CRIM[0]}"/><path d="M30 2 L58 26 L30 26 Z" fill="{CRIM[1]}"/><path d="M10 26 L30 9 L50 26" stroke="{Q["cream"]}" stroke-width="3" fill="none"/>
      <rect x="29" y="-26" width="2" height="30" fill="{IRON[2]}"/><path d="M31 -26 L50 -21 L31 -16 Z" fill="{Q["mustard"]}"/>
      <rect x="2" y="112" width="56" height="10" rx="2" fill="{WOOD[2]}"/><path d="M18 60 L42 60" stroke="{WOOD[0]}" stroke-width="3"/><rect x="18" y="62" width="24" height="4" fill="{WOOD[1]}"/></g>'''
def brazier(x,y):
    return f'''<g transform="translate({x} {y})"><circle cx="26" cy="12" r="26" fill="{Q["mustard"]}" opacity=".16"/>{shadow(26,84,18,4)}<path d="M12 84 L22 40 M40 84 L30 40 M26 84 L26 40" stroke="{IRON[2]}" stroke-width="3" stroke-linecap="round"/>
      <path d="M6 30 Q26 50 46 30 Z" fill="{IRON[1]}"/><path d="M26 40 Q38 38 46 30 L26 30 Z" fill="{IRON[2]}"/><rect x="4" y="27" width="44" height="5" rx="2" fill="{IRON[0]}"/>
      <path d="M12 28 Q8 14 18 6 Q18 16 24 16 Q22 2 30 -6 Q32 10 38 12 Q44 18 40 28 Z" fill="{Q["orange"]}"/><path d="M18 28 Q16 18 22 14 Q24 22 28 22 Q28 14 32 10 Q36 20 34 28 Z" fill="{Q["mustard"]}"/></g>'''
def quiver_rack(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(42,96,40,5)}<rect x="4" y="10" width="6" height="86" fill="{WOOD[1]}"/><rect x="74" y="10" width="6" height="86" fill="{WOOD[2]}"/>{two(0,6,84,7,WOOD[1],WOOD[2],2)}<rect x="4" y="70" width="76" height="5" fill="{WOOD[2]}"/>
      <path d="M20 14 Q34 46 20 78" stroke="{WOOD[2]}" stroke-width="3.5" fill="none"/><path d="M20 14 L20 78" stroke="{Q["cream"]}" stroke-width="1"/>
      <path d="M38 14 Q52 46 38 78" stroke="{WOOD[2]}" stroke-width="3.5" fill="none"/><path d="M38 14 L38 78" stroke="{Q["cream"]}" stroke-width="1"/>
      <rect x="54" y="24" width="14" height="44" rx="3" fill="{Q["brown"]}"/><rect x="62" y="24" width="6" height="44" rx="3" fill="{Q["brown2"]}"/>{"".join(f'<path d="M{57+k*4} 24 L{57+k*4} 10" stroke="{WOOD[2]}" stroke-width="1.6"/><path d="M{55+k*4} 10 l2 -5 l2 5 Z" fill="{CRIM[0]}"/>' for k in range(3))}
      <path d="M6 96 L20 96 M66 96 L80 96" stroke="{WOOD[2]}" stroke-width="5" stroke-linecap="round"/></g>'''
def lookout_scope(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(28,100,24,4)}<path d="M28 50 L8 100 M28 50 L48 100 M28 50 L28 100" stroke="{WOOD[2]}" stroke-width="4" stroke-linecap="round"/>
      <g transform="rotate(-28 28 46)"><rect x="-6" y="38" width="62" height="12" rx="3" fill="{GOLD[1]}"/><rect x="-6" y="44" width="62" height="6" rx="3" fill="{GOLD[2]}"/><rect x="48" y="35" width="12" height="18" rx="3" fill="{GOLD[1]}"/>
        <rect x="-12" y="40" width="8" height="8" rx="2" fill="{GOLD[2]}"/><rect x="18" y="37" width="4" height="14" fill="{WOOD[2]}"/></g><circle cx="28" cy="48" r="4" fill="{IRON[1]}"/></g>'''
def flag_pole(x,y,c,c2):
    return f'''<g transform="translate({x} {y})">{shadow(14,124,12,3)}<rect x="12" y="0" width="4" height="124" fill="{IRON[1]}"/><circle cx="14" cy="-1" r="4" fill="{GOLD[1]}"/>
      <path d="M16 6 Q36 2 56 10 Q46 22 56 34 Q36 26 16 32 Z" fill="{c}"/><path d="M16 19 Q36 14 52 22 Q46 28 56 34 Q36 26 16 32 Z" fill="{c2}"/><path d="M8 124 L20 124" stroke="{GREY[2]}" stroke-width="6" stroke-linecap="round"/></g>'''

# ---------- AVIARY (a garden bird house)
def bird(x,y,c,c2,s=1,flip=False,beak=None):   # a little round songbird, facing left (flip: right)
    beak=beak or Q["mustard"]
    t=f'translate({x} {y}) scale({-s if flip else s} {s})'
    return f'''<g transform="{t}"><path d="M8 4 L20 0 L18 8 Z" fill="{c2}"/><ellipse cx="0" cy="4" rx="10" ry="8" fill="{c}"/><circle cx="-7" cy="-3" r="6" fill="{c}"/>
      <path d="M-2 2 Q6 0 10 6 Q4 10 -2 8 Z" fill="{c2}"/><circle cx="-9" cy="-4" r="1.5" fill="{DARK}"/><path d="M-13 -3 L-18 -1 L-13 0 Z" fill="{beak}"/>
      <path d="M-2 11 L-3 15 M2 11 L3 15" stroke="{Q["orange2"]}" stroke-width="1.4"/></g>'''
def flying_bird(x,y,c,c2,flip=False):
    t=f'translate({x} {y}) scale({-1 if flip else 1} 1)'
    return f'''<g transform="{t}"><path d="M-4 0 Q-14 -18 -26 -10 Q-16 -6 -10 4 Z" fill="{c2}"/><ellipse cx="0" cy="4" rx="12" ry="7" fill="{c}"/><circle cx="-10" cy="0" r="5.5" fill="{c}"/>
      <path d="M2 0 Q10 -20 24 -14 Q14 -6 8 4 Z" fill="{c}"/><path d="M11 4 L22 1 L20 9 Z" fill="{c2}"/><circle cx="-12" cy="-1" r="1.4" fill="{DARK}"/><path d="M-15 0 L-20 2 L-15 3 Z" fill="{Q["mustard"]}"/></g>'''
# bird colours that stand out on grass, leaves and the glass wall (Matt: some were hard to see)
BLUE=('#3f6fc4','#2d539a'); RED=('#d8463a','#a8302a'); YEL=('#ef8a2c','#c9661a'); GRN=('#8a52c0','#69389c')
def cage(x,y,w,h,inner=''):   # a domed brass birdcage
    bars=''.join(f'<path d="M{x+w*k/6:.1f} {y+h*0.2:.1f} L{x+w*k/6:.1f} {y+h}" stroke="{GOLD[1]}" stroke-width="1.6"/>' for k in range(1,6))
    return f'''{inner}<path d="M{x} {y+h} L{x} {y+h*0.3:.1f} Q{x} {y} {x+w/2:.1f} {y} Q{x+w} {y} {x+w} {y+h*0.3:.1f} L{x+w} {y+h}" fill="none" stroke="{GOLD[1]}" stroke-width="2.4"/>{bars}
      <path d="M{x+w/2:.1f} {y} L{x+w/2:.1f} {y+h}" stroke="{GOLD[1]}" stroke-width="1.6"/><rect x="{x-3}" y="{y+h-2}" width="{w+6}" height="6" rx="2" fill="{GOLD[2]}"/>
      <path d="M{x} {y+h*0.55:.1f} L{x+w} {y+h*0.55:.1f}" stroke="{GOLD[2]}" stroke-width="1.4"/><circle cx="{x+w/2:.1f}" cy="{y-4}" r="4" fill="none" stroke="{GOLD[2]}" stroke-width="2"/>'''
def tall_birdcage(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(30,128,24,5)}<rect x="28" y="70" width="5" height="56" fill="{GOLD[2]}"/><path d="M12 128 L30 118 L48 128" stroke="{GOLD[2]}" stroke-width="4" fill="none" stroke-linecap="round"/>
      {cage(4,4,52,68, bird(30,44,YEL[0],YEL[1],1) + f'<path d="M10 52 L50 52" stroke="{WOOD[2]}" stroke-width="2"/>')}</g>'''
def hook_cage(x,y):   # a cage hanging from a shepherd's hook
    return f'''<g transform="translate({x} {y})">{shadow(18,132,16,4)}<rect x="14" y="10" width="5" height="122" fill="{IRON[1]}"/><path d="M16 12 Q16 -4 32 -4 Q46 -4 46 10" stroke="{IRON[1]}" stroke-width="4" fill="none"/>
      <path d="M46 10 L46 18" stroke="{IRON[2]}" stroke-width="2"/>{cage(32,22,28,38, bird(46,44,BLUE[0],BLUE[1],0.8,True))}<path d="M8 132 L24 132" stroke="{IRON[2]}" stroke-width="5" stroke-linecap="round"/></g>'''
def parrot(x,y,flip=False):
    t=f'translate({x} {y}) scale({-1 if flip else 1} 1)'
    return f'''<g transform="{t}"><path d="M2 14 L8 40 L-2 40 Z" fill="{BLUE[1]}"/><path d="M6 16 L14 38 L6 38 Z" fill="{Q["mustard"]}"/><ellipse cx="0" cy="10" rx="9" ry="14" fill="{RED[0]}"/><path d="M0 0 Q12 8 6 22 Q0 18 0 10 Z" fill="{BLUE[0]}"/>
      <circle cx="-2" cy="-6" r="8" fill="{RED[0]}"/><circle cx="-5" cy="-8" r="3" fill="#fff"/><circle cx="-5" cy="-8" r="1.5" fill="{DARK}"/><path d="M-9 -6 Q-15 -4 -12 2 Q-9 0 -8 -3 Z" fill="{Q["cream2"]}"/></g>'''
def parrot_perch(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(36,124,30,5)}<rect x="33" y="40" width="6" height="84" fill="{WOOD[1]}"/><path d="M14 124 L36 114 L58 124" stroke="{WOOD[2]}" stroke-width="5" fill="none" stroke-linecap="round"/>
      <rect x="4" y="38" width="64" height="5" rx="2" fill="{WOOD[2]}"/><circle cx="6" cy="40" r="5" fill="{GRN[1]}"/><circle cx="66" cy="40" r="5" fill="{GRN[1]}"/>
      {parrot(20,10)}{parrot(54,10,True).replace(RED[0],GRN[0]).replace(BLUE[0],YEL[0])}<rect x="26" y="84" width="20" height="8" rx="3" fill="{Q["cream"]}"/></g>'''
def bird_bath(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(36,82,30,5)}<path d="M26 82 L30 40 L42 40 L46 82 Z" fill="{GREY[0]}"/><path d="M36 40 L42 40 L46 82 L36 82 Z" fill="{GREY[1]}"/><rect x="18" y="78" width="36" height="6" rx="2" fill="{GREY[1]}"/>
      <path d="M2 30 Q36 52 70 30 Z" fill="{GREY[0]}"/><path d="M36 41 Q56 38 70 30 L36 30 Z" fill="{GREY[1]}"/><ellipse cx="36" cy="30" rx="34" ry="6" fill="{GREY[0]}"/><ellipse cx="36" cy="30" rx="28" ry="4" fill="#a9cbe0"/>
      {bird(14,16,BLUE[0],BLUE[1],0.9,True)}{bird(58,18,RED[0],RED[1],0.9)}<path d="M40 30 q3 -3 6 0 M28 31 q2 -2 4 0" stroke="#fff" stroke-width="1.2" fill="none"/></g>'''
def nest_post(x,y):
    def house(hx,hy,c,c2): return f'<g transform="translate({hx} {hy})">{two(0,10,26,24,c,c2,2)}<path d="M-3 12 L13 0 L29 12 Z" fill="{WOOD[2]}"/><circle cx="13" cy="20" r="4" fill="#3a2414"/><rect x="12" y="27" width="2" height="5" fill="{WOOD[2]}"/></g>'
    return f'''<g transform="translate({x} {y})">{shadow(32,126,22,5)}<rect x="29" y="20" width="6" height="106" fill="{WOOD[1]}"/><path d="M14 126 L50 126" stroke="{WOOD[2]}" stroke-width="5" stroke-linecap="round"/>
      {house(0,0,Q["cream"],Q["cream2"])}{house(36,24,SAGE[0],SAGE[2])}{house(4,52,ROSE[0],ROSE[1])}{bird(48,20,YEL[0],YEL[1],0.7)}</g>'''
def feeder_table(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(44,80,42,5)}<rect x="40" y="36" width="8" height="44" fill="{WOOD[1]}"/><path d="M24 80 L44 72 L64 80" stroke="{WOOD[2]}" stroke-width="5" fill="none" stroke-linecap="round"/>
      {two(0,28,88,8,WOOD[1],WOOD[2],2)}<path d="M2 28 L2 22 L86 22 L86 28" stroke="{WOOD[2]}" stroke-width="2" fill="none"/>
      <ellipse cx="26" cy="24" rx="14" ry="3" fill="{Q["tan"]}"/>{"".join(f'<circle cx="{18+k*4}" cy="{23+(k%2)}" r="1.2" fill="{Q["brown"]}"/>' for k in range(5))}<ellipse cx="62" cy="24" rx="12" ry="3" fill="{Q["orange"]}"/>
      {bird(30,10,RED[0],RED[1],0.9,True)}{bird(68,8,GRN[0],GRN[1],0.9)}</g>'''
def bird_tree(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(40,130,30,5)}<path d="M36 130 L38 60 Q30 40 18 34 M38 70 Q52 52 62 48" stroke="{WOOD[2]}" stroke-width="7" fill="none" stroke-linecap="round"/>
      <circle cx="40" cy="36" r="34" fill="{Q["green"]}"/><path d="M40 2 A34 34 0 0 1 40 70 Z" fill="{Q["green2"]}"/><circle cx="24" cy="26" r="12" fill="#4f8a4a" opacity=".6"/>
      <path d="M26 126 L50 126 L46 112 L30 112 Z" fill="{Q["orange"]}"/><path d="M38 112 L46 112 L50 126 L38 126 Z" fill="{Q["orange2"]}"/>
      {bird(22,28,BLUE[0],BLUE[1],0.8,True)}{bird(56,40,YEL[0],YEL[1],0.8)}{bird(38,10,RED[0],RED[1],0.75)}</g>'''
def aviary_head():
    w=f'<rect x="0" y="0" width="390" height="214" fill="#d8ecd8"/>'
    # glass and iron: tall arched panes all along the back wall, greenery outside
    for k in range(5):
        x=8+k*78
        w+=f'<path d="M{x} 150 L{x} 40 Q{x} 8 {x+35} 8 Q{x+70} 8 {x+70} 40 L{x+70} 150 Z" fill="#cfe7ee"/><path d="M{x+4} 150 L{x+4} 110 Q{x+20} 96 {x+35} 106 Q{x+52} 92 {x+66} 104 L{x+66} 150 Z" fill="{Q["olive"]}" opacity=".55"/>'
        w+=f'<path d="M{x} 150 L{x} 40 Q{x} 8 {x+35} 8 Q{x+70} 8 {x+70} 40 L{x+70} 150" fill="none" stroke="{IRON[1]}" stroke-width="4"/><path d="M{x+35} 8 L{x+35} 150 M{x} 60 L{x+70} 60 M{x} 105 L{x+70} 105" stroke="{IRON[1]}" stroke-width="2.4"/>'
    w+=f'<rect x="0" y="150" width="390" height="64" fill="{Q["cream"]}"/>'+''.join(f'<rect x="{x+5}" y="158" width="38" height="50" rx="3" fill="none" stroke="{SAGE[1]}" stroke-width="2"/>' for x in range(0,390,48))+f'<rect x="0" y="146" width="390" height="7" fill="{IRON[1]}"/>'
    # ivy along the top and down the sides
    w+=''.join(f'<path d="M{lx} {ly} q-5 -5 0 -9 q5 4 0 9 Z" fill="{Q["green"] if k%2 else "#4f8a4a"}" transform="rotate({(k*53)%90-45} {lx} {ly})"/>' for k,(lx,ly) in enumerate([(x,10+(x*7)%14) for x in range(4,390,14)]+[(6+(y%3)*4,y) for y in range(24,140,12)]+[(384-(y%3)*4,y) for y in range(24,140,12)]))
    w+=f'<rect x="146" y="100" width="98" height="114" fill="{SAGE[2]}"/><path d="M146 100 Q195 78 244 100 Z" fill="{IRON[1]}"/>'+gate_arch(164,62,(SAGE[1],SAGE[2]))+f'<circle cx="216" cy="172" r="3.4" fill="{GOLD[0]}"/>'
    w+=f'<path d="M195 14 L195 40" stroke="{IRON[2]}" stroke-width="2"/>{cage(176,40,38,44, bird(195,66,RED[0],RED[1],0.9))}'
    w+=f'<path d="M60 150 L60 120" stroke="{WOOD[2]}" stroke-width="3"/>{bird(70,116,BLUE[0],BLUE[1],0.9,True)}<path d="M300 150 L300 124 L330 124" stroke="{WOOD[2]}" stroke-width="3" fill="none"/>{bird(318,114,YEL[0],YEL[1],0.9)}'
    return w
H6['Battlements']=battlements_head()+STEP
add6('cannon',cannon_s(0,0),(0,0,90,62)); add6('cannonballs',cannonballs(0,0),(0,4,60,52)); add6('catapult',catapult(0,0),(0,-6,112,112))
add6('sentry_box',sentry_box(0,0),(0,-28,60,154)); add6('signal_fire',brazier(0,0),(0,-8,52,94)); add6('quiver_rack',quiver_rack(0,0),(0,4,86,96))
add6('lookout_scope',lookout_scope(0,0),(-4,10,68,96)); add6('flag_pole',flag_pole(0,0,Q["navy"],Q["navy2"]),(0,-6,60,134))
H6['Aviary']=aviary_head()+STEP
add6('tall_birdcage',tall_birdcage(0,0),(0,-4,60,136)); add6('hook_cage',hook_cage(0,0),(0,-6,64,140)); add6('parrot_perch',parrot_perch(0,0),(0,-6,72,132))
add6('bird_bath',bird_bath(0,0),(0,4,72,84)); add6('nest_post',nest_post(0,0),(-4,0,68,130)); add6('feeder_table',feeder_table(0,0),(0,-6,88,90))
add6('bird_tree',bird_tree(0,0),(0,0,76,132))
add6('bird_fly_blue',flying_bird(26,20,BLUE[0],BLUE[1]),(0,0,52,34)); add6('bird_fly_red',flying_bird(26,20,RED[0],RED[1],True),(0,0,52,34))
# ---------- WATCHTOWER (the lookout room: a round sandstone room high up, windows over the countryside)
SAND=('#e3cfa4','#cdb382','#a88f62')
def wt_window(x,y,w=40,h=100):
    return f'''<path d="M{x} {y+h} L{x} {y+16} Q{x} {y} {x+w/2} {y} Q{x+w} {y} {x+w} {y+16} L{x+w} {y+h} Z" fill="{SAND[2]}"/>
      <path d="M{x+5} {y+h-4} L{x+5} {y+18} Q{x+5} {y+6} {x+w/2} {y+6} Q{x+w-5} {y+6} {x+w-5} {y+18} L{x+w-5} {y+h-4} Z" fill="{SKY[0]}"/>
      <path d="M{x+5} {y+h*0.62} Q{x+w*0.4} {y+h*0.55} {x+w-5} {y+h*0.6} L{x+w-5} {y+h-4} L{x+5} {y+h-4} Z" fill="{Q["olive"]}"/>
      <path d="M{x+5} {y+h*0.76} Q{x+w*0.6} {y+h*0.7} {x+w-5} {y+h*0.78} L{x+w-5} {y+h-4} L{x+5} {y+h-4} Z" fill="{Q["olive2"]}"/>
      <circle cx="{x+w*0.68}" cy="{y+h*0.56}" r="4" fill="{Q["green"]}"/><path d="M{x+5} {y+h*0.88} L{x+w-5} {y+h*0.84}" stroke="#6f9bb3" stroke-width="2.4"/>
      <rect x="{x-4}" y="{y+h-2}" width="{w+8}" height="7" rx="2" fill="{SAND[0]}"/>'''
def torch(x,y):
    return f'''<g transform="translate({x} {y})"><circle cx="0" cy="-10" r="14" fill="{Q["mustard"]}" opacity=".18"/><rect x="-2" y="0" width="4" height="18" fill="{IRON[2]}"/><path d="M-6 18 L6 18 L4 24 L-4 24 Z" fill="{IRON[1]}"/>
      <path d="M-5 0 Q-7 -10 0 -18 Q7 -10 5 0 Z" fill="{Q["orange"]}"/><path d="M-2.5 0 Q-3 -6 0 -11 Q3 -6 2.5 0 Z" fill="{Q["mustard"]}"/></g>'''
def watchtower_head():
    w=f'<rect x="0" y="0" width="390" height="214" fill="{SAND[1]}"/>'
    w+=''.join(f'<rect x="{x}" y="{y}" width="44" height="18" rx="2" fill="{SAND[0] if (x//48+r)%3 else SAND[2]}" opacity=".35"/>' for r,y in enumerate(range(4,214,22)) for x in range(-24+(r%2)*24,390,48))
    w+='<rect x="0" y="0" width="34" height="214" fill="#3a2a18" opacity=".14"/><rect x="356" y="0" width="34" height="214" fill="#3a2a18" opacity=".14"/>'   # the wall curves away
    w+=wt_window(22,46)+wt_window(84,46)+wt_window(266,46)+wt_window(328,46)
    w+=torch(135,92)+torch(255,92)
    # the map of the lands around the castle, pinned above the door
    w+=f'<rect x="150" y="24" width="90" height="62" rx="2" fill="{Q["cream2"]}"/><rect x="153" y="27" width="84" height="56" fill="{Q["cream"]}"/>'
    w+=f'<path d="M156 70 Q176 58 192 66 Q210 74 234 58" stroke="#6f9bb3" stroke-width="3" fill="none"/><path d="M164 50 l7 -10 l7 10 Z M178 48 l6 -8 l6 8 Z" fill="{Q["olive2"]}"/><circle cx="214" cy="40" r="5" fill="{GREY[1]}"/><rect x="211" y="33" width="6" height="7" fill="{GREY[2]}"/>'
    w+=f'<path d="M200 70 l6 6 M206 70 l-6 6" stroke="{CRIM[0]}" stroke-width="2.4"/>'+''.join(f'<circle cx="{px}" cy="{py}" r="2.6" fill="{c}"/>' for px,py,c in ((152,26,CRIM[0]),(238,26,BLUE[0]),(152,84,BLUE[0]),(238,84,CRIM[0])))
    w+=f'<rect x="146" y="100" width="98" height="114" fill="{SAND[2]}"/>'+gate_arch(164,62,(WOOD[1],WOOD[2]))+f'<circle cx="216" cy="172" r="3.4" fill="{GOLD[0]}"/>'
    return w
def watch_pillar(x,y):   # a round sandstone pillar in the middle of the room, with a torch
    return f'''<g transform="translate({x} {y})">{shadow(22,112,24,6)}<rect x="0" y="100" width="44" height="12" rx="2" fill="{SAND[2]}"/><rect x="5" y="8" width="34" height="94" fill="{SAND[0]}"/><rect x="25" y="8" width="14" height="94" fill="{SAND[1]}"/>
      {"".join(f'<rect x="5" y="{yy}" width="34" height="2" fill="{SAND[2]}" opacity=".6"/>' for yy in (30,54,78))}<rect x="0" y="0" width="44" height="10" rx="2" fill="{SAND[2]}"/>{torch(22,44)}</g>'''
def map_table(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(48,74,46,5)}<path d="M10 30 L10 74 M86 30 L86 74 M20 30 L20 68 M76 30 L76 68" stroke="{WOOD[2]}" stroke-width="5"/>{two(0,22,96,10,WOOD[1],WOOD[2],2)}
      <path d="M8 22 L14 4 L86 6 L90 22 Z" fill="{Q["cream"]}"/><path d="M60 5 L86 6 L90 22 L62 22 Z" fill="{Q["cream2"]}"/><path d="M18 18 Q34 8 50 14 Q66 20 82 10" stroke="#6f9bb3" stroke-width="2.4" fill="none"/>
      <path d="M26 12 l5 -6 l5 6 Z" fill="{Q["olive2"]}"/>{"".join(f'<circle cx="{px}" cy="{py}" r="2.4" fill="{c}"/>' for px,py,c in ((40,10,CRIM[0]),(70,16,BLUE[0]),(58,9,CRIM[0])))}
      <circle cx="80" cy="16" r="5" fill="{GOLD[1]}"/><circle cx="80" cy="16" r="3" fill="{Q["cream"]}"/><path d="M80 13 L80 19" stroke="{CRIM[0]}" stroke-width="1.4"/></g>'''
def spyglass_rack(x,y):
    def glass(gx,rot,l): return f'<g transform="translate({gx} 60) rotate({rot})"><rect x="-4" y="{-l}" width="8" height="{l}" rx="2" fill="{GOLD[1]}"/><rect x="0" y="{-l}" width="4" height="{l}" rx="2" fill="{GOLD[2]}"/><rect x="-5.5" y="{-l-6}" width="11" height="10" rx="2" fill="{GOLD[1]}"/><rect x="-4.5" y="{-l*0.5}" width="9" height="5" fill="{WOOD[2]}"/></g>'
    return f'''<g transform="translate({x} {y})">{shadow(30,104,26,5)}{glass(16,-12,54)}{glass(30,0,62)}{glass(44,12,50)}{two(4,56,52,48,WOOD[1],WOOD[2],3)}
      <rect x="0" y="52" width="60" height="8" rx="2" fill="{WOOD[2]}"/><rect x="12" y="70" width="36" height="20" rx="2" fill="none" stroke="{WOOD[0]}" stroke-width="2"/></g>'''
def signal_horn(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(40,100,32,5)}<path d="M40 100 L40 56 M24 100 L40 70 L56 100" stroke="{WOOD[2]}" stroke-width="5" fill="none" stroke-linecap="round"/>
      <path d="M6 30 Q4 6 30 8 Q60 10 68 34 Q72 46 60 50 Q50 52 46 42 Q42 26 26 28 Q16 30 14 40 Z" fill="{GOLD[1]}"/><path d="M48 18 Q62 24 68 34 Q72 46 60 50 Q50 52 46 42 Q44 30 40 26 Z" fill="{GOLD[2]}"/>
      <ellipse cx="9" cy="36" rx="8" ry="11" fill="{GOLD[2]}"/><ellipse cx="9" cy="36" rx="5" ry="8" fill="#5a3a12"/><path d="M58 46 L70 52" stroke="{GOLD[1]}" stroke-width="4" stroke-linecap="round"/>
      <path d="M22 16 Q40 6 56 20" stroke="{CRIM[0]}" stroke-width="3" fill="none"/><path d="M30 12 L30 22 M44 12 L44 22" stroke="{CRIM[1]}" stroke-width="2"/></g>'''
def beacon_lamp(x,y):
    return f'''<g transform="translate({x} {y})"><circle cx="26" cy="22" r="30" fill="{Q["mustard"]}" opacity=".2"/>{shadow(26,128,24,5)}{two(6,96,40,32,SAND[0],SAND[1],2)}<rect x="2" y="92" width="48" height="7" rx="2" fill="{SAND[2]}"/>
      <rect x="23" y="48" width="6" height="46" fill="{IRON[1]}"/><path d="M8 6 L26 -8 L44 6 Z" fill="{IRON[2]}"/><rect x="10" y="6" width="32" height="38" rx="3" fill="{Q["mustard"]}"/>
      <path d="M18 40 Q14 26 26 14 Q38 26 34 40 Z" fill="{Q["orange"]}"/><path d="M10 6 L10 44 M42 6 L42 44 M26 6 L26 44" stroke="{IRON[2]}" stroke-width="2.4"/><rect x="6" y="42" width="40" height="7" rx="2" fill="{IRON[2]}"/><circle cx="26" cy="-10" r="3" fill="{IRON[1]}"/></g>'''
def log_desk(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(30,110,24,5)}<rect x="26" y="40" width="8" height="70" fill="{WOOD[1]}"/><path d="M12 110 L30 100 L48 110" stroke="{WOOD[2]}" stroke-width="5" fill="none" stroke-linecap="round"/>
      <path d="M2 30 L58 22 L58 34 L2 42 Z" fill="{WOOD[2]}"/><path d="M6 30 L30 26 L30 36 L6 40 Z" fill="{Q["cream"]}"/><path d="M30 26 L54 23 L54 33 L30 36 Z" fill="{Q["cream2"]}"/>
      <path d="M10 33 L26 30 M10 36 L24 34 M34 30 L50 28 M34 33 L48 31" stroke="{Q["brown"]}" stroke-width="1"/>
      <g transform="translate(36 -6)"><rect x="0" y="0" width="16" height="3" fill="{WOOD[2]}"/><rect x="0" y="22" width="16" height="3" fill="{WOOD[2]}"/><path d="M2 3 L14 3 L8 12.5 L14 22 L2 22 L8 12.5 Z" fill="#cfe7ee"/><path d="M5 18 L11 18 L13 22 L3 22 Z M6 8 L10 8 L8 11 Z" fill="{Q["tan"]}"/></g></g>'''
def weathervane(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(36,132,16,4)}<rect x="34" y="20" width="4" height="112" fill="{GOLD[1]}"/><path d="M26 132 L46 132" stroke="{Q["cream"]}" stroke-width="6" stroke-linecap="round"/>
      <path d="M8 64 L64 64 M36 52 L36 76" stroke="{Q["cream"]}" stroke-width="2.4"/><path d="M2 60 L5 68 L7 63 L9 68 L12 60" stroke="{Q["cream"]}" stroke-width="1.8" fill="none"/><path d="M70 60 L64 60 L64 68 L70 68 M64 64 L69 64" stroke="{Q["cream"]}" stroke-width="1.8" fill="none"/>
      <path d="M14 18 L58 18" stroke="{Q["cream"]}" stroke-width="2.4"/><path d="M58 18 L66 12 L66 24 Z" fill="{Q["cream"]}"/><path d="M14 18 L8 12 L4 12 L8 18 L4 24 L8 24 Z" fill="{Q["cream"]}"/>
      <path d="M22 16 Q20 0 34 2 Q38 -6 42 0 Q44 6 40 8 Q52 6 54 16 Z" fill="{GOLD[1]}"/><path d="M38 2 Q46 4 48 8 L52 6 Q54 12 54 16 L40 16 Z" fill="{GOLD[2]}"/><path d="M34 -2 l2 -6 l3 5 l2 -5 l1 6 Z" fill="{CRIM[0]}"/><circle cx="37" cy="3" r="1.2" fill="{DARK}"/><circle cx="36" cy="18" r="3" fill="{GOLD[1]}"/></g>'''
def watch_bench(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(46,60,44,5)}<path d="M10 34 L8 60 M82 34 L84 60 M20 34 L20 56 M72 34 L72 56" stroke="{WOOD[2]}" stroke-width="5"/>{two(0,26,92,10,WOOD[1],WOOD[2],2)}
      <path d="M12 26 Q12 10 24 10 L50 10 Q60 10 60 26 Z" fill="{BLUE[0]}"/><path d="M12 18 L60 18" stroke="{Q["cream"]}" stroke-width="3"/><path d="M40 10 L50 10 Q60 10 60 26 L40 26 Z" fill="{BLUE[1]}"/>
      <rect x="70" y="10" width="14" height="16" rx="3" fill="{Q["cream"]}"/><path d="M84 14 Q90 18 84 22" stroke="{Q["cream2"]}" stroke-width="2.4" fill="none"/><rect x="70" y="10" width="14" height="4" rx="2" fill="{Q["brown"]}"/></g>'''

# ---------- BELFRY (the bell loft: bronze bells on oak beams, ropes, sleepy bats)
OAK=('#8c6440','#6e4c30','#523822')
BRONZE=('#d9a85a','#b8863a','#8a6024')
def bell(cx,top,w,h,crack=False):   # a bronze bell, light on the left, with a clapper showing under it
    x0,x1=cx-w/2,cx+w/2
    s=f'<path d="M{cx-w*0.26:.1f} {top+h*0.12:.1f} Q{cx-w*0.28:.1f} {top:.1f} {cx} {top} Q{cx+w*0.28:.1f} {top} {cx+w*0.26:.1f} {top+h*0.12:.1f} Q{cx+w*0.3:.1f} {top+h*0.6:.1f} {x1} {top+h*0.9:.1f} L{x1} {top+h} L{x0} {top+h} L{x0} {top+h*0.9:.1f} Q{cx-w*0.3:.1f} {top+h*0.6:.1f} {cx-w*0.26:.1f} {top+h*0.12:.1f} Z" fill="{BRONZE[0]}"/>'
    s+=f'<path d="M{cx} {top} Q{cx+w*0.28:.1f} {top} {cx+w*0.26:.1f} {top+h*0.12:.1f} Q{cx+w*0.3:.1f} {top+h*0.6:.1f} {x1} {top+h*0.9:.1f} L{x1} {top+h} L{cx+w*0.1:.1f} {top+h} Z" fill="{BRONZE[1]}"/>'
    s+=f'<rect x="{x0-2:.1f}" y="{top+h*0.84:.1f}" width="{w+4}" height="{h*0.1:.1f}" rx="2" fill="{BRONZE[2]}"/><circle cx="{cx}" cy="{top+h+h*0.08:.1f}" r="{w*0.08:.1f}" fill="{BRONZE[2]}"/><rect x="{cx-w*0.12:.1f}" y="{top-h*0.1:.1f}" width="{w*0.24:.1f}" height="{h*0.12:.1f}" rx="2" fill="{BRONZE[2]}"/>'
    if crack: s+=f'<path d="M{cx-w*0.1:.1f} {top+h:.1f} l4 -10 l-5 -8 l5 -9" stroke="{BRONZE[2]}" stroke-width="2" fill="none"/>'
    return s
def bat(x,y,s=1):   # a little bat hanging upside down, wings folded, fast asleep
    return f'''<g transform="translate({x} {y}) scale({s})"><path d="M-2 0 L-2 4 M2 0 L2 4" stroke="#3a2e3e" stroke-width="1.6"/><ellipse cx="0" cy="14" rx="7" ry="10" fill="#5a4a62"/><path d="M-7 8 Q-12 16 -6 24 Q0 20 0 14 Z M7 8 Q12 16 6 24 Q0 20 0 14 Z" fill="#46384e"/>
      <circle cx="0" cy="24" r="5" fill="#5a4a62"/><path d="M-4 29 L-3 25 L-1 28 Z M4 29 L3 25 L1 28 Z" fill="#5a4a62"/><path d="M-3 23 q1.4 1 2.6 0 M0.6 23 q1.4 1 2.6 0" stroke="#e6d6f0" stroke-width=".9" fill="none"/></g>'''
def belfry_head():
    w=f'<rect x="0" y="0" width="390" height="214" fill="{OAK[2]}"/>'
    w+=''.join(f'<rect x="{x}" y="0" width="28" height="214" fill="{OAK[1]}" opacity="{.5 if k%2 else .7}"/>' for k,x in enumerate(range(0,390,30)))
    for x in (12,322):   # louvred windows: slats with slivers of sky
        w+=f'<rect x="{x}" y="40" width="56" height="104" rx="3" fill="{OAK[0]}"/><rect x="{x+5}" y="45" width="46" height="94" fill="{SKY[0]}"/>'+''.join(f'<path d="M{x+5} {yy} L{x+51} {yy+8} L{x+51} {yy+14} L{x+5} {yy+6} Z" fill="{OAK[1]}"/>' for yy in range(45,134,12))
    w+=f'<rect x="0" y="8" width="390" height="16" fill="{OAK[0]}"/><rect x="0" y="20" width="390" height="4" fill="{OAK[2]}" opacity=".6"/>'
    w+=f'<rect x="124" y="24" width="12" height="190" fill="{OAK[0]}"/><rect x="254" y="24" width="12" height="190" fill="{OAK[0]}"/><path d="M136 70 L168 24 M254 70 L222 24" stroke="{OAK[0]}" stroke-width="9"/>'
    w+=f'<circle cx="195" cy="62" r="36" fill="none" stroke="{OAK[0]}" stroke-width="6"/>'+''.join(f'<path d="M195 62 L{195+36*math.cos(math.radians(a)):.1f} {62+36*math.sin(math.radians(a)):.1f}" stroke="{OAK[0]}" stroke-width="3"/>' for a in range(0,360,45))
    w+=f'<path d="M195 24 L195 30" stroke="{IRON[2]}" stroke-width="4"/>'+bell(195,30,58,56)
    w+=f'<path d="M98 24 L98 32 M290 24 L290 32" stroke="{IRON[2]}" stroke-width="3"/>'+bell(98,32,38,38)+bell(290,32,38,38)
    w+=f'<path d="M98 76 Q94 120 100 150 Q104 176 98 206" stroke="{Q["tan"]}" stroke-width="3" fill="none"/><path d="M290 76 Q294 120 288 150 Q284 176 290 206" stroke="{Q["tan"]}" stroke-width="3" fill="none"/>'
    w+=f'<rect x="94" y="150" width="9" height="20" rx="4" fill="{CRIM[0]}"/><rect x="286" y="150" width="9" height="20" rx="4" fill="{BLUE[0]}"/>'
    w+=bat(40,24)+bat(160,24,0.9)+bat(232,24,0.8)+bat(352,24)
    w+=f'<rect x="146" y="100" width="98" height="114" fill="{OAK[1]}"/>'+gate_arch(164,62,(WOOD[1],WOOD[2]))+f'<circle cx="216" cy="172" r="3.4" fill="{GOLD[0]}"/>'
    return w
def old_bell(x,y):
    return f'<g transform="translate({x} {y})">{shadow(40,78,40,6)}{bell(40,6,76,66,True)}<path d="M6 78 L74 78" stroke="{WOOD[1]}" stroke-width="5" stroke-linecap="round"/></g>'
def bell_frame(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(36,102,34,5)}<path d="M8 102 L22 10 M64 102 L50 10" stroke="{WOOD[0]}" stroke-width="7" stroke-linecap="round"/><path d="M50 10 L64 102" stroke="{WOOD[1]}" stroke-width="7" stroke-linecap="round"/>
      <rect x="14" y="4" width="44" height="9" rx="2" fill="{WOOD[0]}"/><path d="M36 13 L36 22" stroke="{IRON[2]}" stroke-width="3"/>{bell(36,22,34,34)}<path d="M14 90 L58 90" stroke="{WOOD[1]}" stroke-width="5"/>
      <path d="M50 46 Q58 70 54 92" stroke="{Q["tan"]}" stroke-width="2.4" fill="none"/></g>'''
def loft_ladder(x,y):
    rungs=''.join(f'<rect x="4" y="{yy}" width="24" height="5" rx="1" fill="{OAK[0]}"/>' for yy in range(10,122,16))
    return f'<g transform="translate({x} {y})">{shadow(20,130,22,5)}<g transform="rotate(8 16 130)"><rect x="0" y="0" width="6" height="130" rx="2" fill="{WOOD[0]}"/><rect x="26" y="0" width="6" height="130" rx="2" fill="{WOOD[1]}"/>{rungs}</g></g>'
def rope_coil(x,y):
    rings=''.join(f'<ellipse cx="36" cy="{30-k*5}" rx="{32-k*3}" ry="{11-k*0.8:.1f}" fill="none" stroke="{"#f3dcaa" if k%2 else "#d8b47a"}" stroke-width="6"/>' for k in range(4))
    return f'<g transform="translate({x} {y})">{shadow(36,40,34,5)}{rings}<path d="M64 32 Q76 36 80 30" stroke="{Q["tan2"]}" stroke-width="6" fill="none" stroke-linecap="round"/><ellipse cx="36" cy="14" rx="14" ry="4" fill="#2a1d14" opacity=".8"/></g>'
def bat_post(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(36,122,18,4)}<rect x="32" y="8" width="9" height="114" fill="{WOOD[0]}"/><rect x="37" y="8" width="4" height="114" fill="{WOOD[1]}"/><rect x="2" y="6" width="70" height="9" rx="2" fill="{WOOD[0]}"/>
      <path d="M22 122 L50 122" stroke="{WOOD[1]}" stroke-width="6" stroke-linecap="round"/>{bat(14,15)}{bat(60,15,0.85)}</g>'''
def handbell(hx,hy,s,c):
    return f'<g transform="translate({hx} {hy}) scale({s})"><rect x="-3" y="-20" width="6" height="12" rx="2" fill="{c}"/><path d="M-6 -8 Q-7 4 -11 10 L11 10 Q7 4 6 -8 Q0 -12 -6 -8 Z" fill="{BRONZE[0]}"/><path d="M1 -10 Q7 -8 6 -8 Q7 4 11 10 L2 10 Z" fill="{BRONZE[1]}"/><rect x="-12" y="9" width="24" height="3" rx="1" fill="{BRONZE[2]}"/></g>'
def handbell_table(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(46,72,44,5)}<path d="M10 40 L10 72 M82 40 L82 72" stroke="{WOOD[1]}" stroke-width="6"/>{two(0,32,92,10,CRIM[0],CRIM[1],2)}<path d="M2 42 L90 42" stroke="{GOLD[1]}" stroke-width="2"/>
      {handbell(16,22,1.15,CRIM[0])}{handbell(38,23,1,BLUE[0])}{handbell(58,24,0.85,Q["green"])}{handbell(76,25,0.7,Q["mustard"])}</g>'''
def clapper_crate(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(34,62,34,5)}{two(2,24,64,38,WOOD[1],WOOD[2],2)}<path d="M2 36 L66 36 M2 50 L66 50 M6 24 L62 62" stroke="{WOOD[2]}" stroke-width="2.4"/>
      <g transform="rotate(-24 30 18)"><rect x="27" y="-10" width="6" height="30" rx="2" fill="{IRON[1]}"/><circle cx="30" cy="22" r="8" fill="{IRON[2]}"/><circle cx="27" cy="19" r="2.4" fill="{IRON[0]}"/></g>
      <rect x="48" y="12" width="16" height="14" rx="2" fill="{IRON[1]}"/><rect x="48" y="10" width="16" height="4" rx="2" fill="{IRON[2]}"/><path d="M54 10 L52 2" stroke="{WOOD[1]}" stroke-width="3"/></g>'''

# ---------- CROWN VAULT (the crown jewels, behind a round steel vault door: the floor's last room)
STEEL=('#c9ced6','#a3aab4','#747c88')
VSTONE=('#4a3f38','#3d342e','#2e2722')
def crown(cx,base,w,c=None,gem=None):   # a king's crown, its band sitting on y=base
    c=c or GOLD[1]; gem=gem or CRIM[0]; h=w*0.62
    tips=' '.join(f'L{cx-w/2+w*k/4:.1f} {base-h*(1 if k%2==0 else 0.55):.1f}' for k in range(5))
    s=f'<path d="M{cx-w/2:.1f} {base:.1f} {tips} L{cx+w/2:.1f} {base:.1f} Z" fill="{c}"/>'
    s+=f'<path d="M{cx:.1f} {base-h*0.55:.1f} L{cx+w/4:.1f} {base-h:.1f} L{cx+w/2:.1f} {base-h*0.55:.1f} L{cx+w/2:.1f} {base:.1f} L{cx:.1f} {base:.1f} Z" fill="{GOLD[2]}" opacity=".55"/>'
    s+=f'<rect x="{cx-w/2-1:.1f}" y="{base-h*0.24:.1f}" width="{w+2:.1f}" height="{h*0.26:.1f}" rx="1.5" fill="{GOLD[2]}"/>'
    s+=''.join(f'<circle cx="{cx-w/2+w*k/4:.1f}" cy="{base-h-2:.1f}" r="{w*0.05+1:.1f}" fill="#fff4d0"/>' for k in (0,2,4))
    s+=f'<circle cx="{cx:.1f}" cy="{base-h*0.11:.1f}" r="{w*0.07+0.5:.1f}" fill="{gem}"/><circle cx="{cx-w*0.3:.1f}" cy="{base-h*0.11:.1f}" r="{w*0.05:.1f}" fill="{BLUE[0]}"/><circle cx="{cx+w*0.3:.1f}" cy="{base-h*0.11:.1f}" r="{w*0.05:.1f}" fill="{Q["green"]}"/>'
    return s
def vault_door():
    s=f'<circle cx="195" cy="160" r="60" fill="{VSTONE[2]}"/><circle cx="195" cy="160" r="54" fill="{STEEL[1]}"/><path d="M195 106 A54 54 0 0 1 195 214 Z" fill="{STEEL[2]}" opacity=".55"/>'
    s+=f'<circle cx="195" cy="160" r="44" fill="none" stroke="{STEEL[0]}" stroke-width="3"/>'+''.join(f'<circle cx="{195+49*math.cos(math.radians(a)):.1f}" cy="{160+49*math.sin(math.radians(a)):.1f}" r="2.6" fill="{STEEL[2]}"/>' for a in range(0,360,30))
    s+=''.join(f'<path d="M195 160 L{195+26*math.cos(math.radians(a)):.1f} {160+26*math.sin(math.radians(a)):.1f}" stroke="{GOLD[1]}" stroke-width="4" stroke-linecap="round"/>' for a in range(0,360,60))
    s+=f'<circle cx="195" cy="160" r="26" fill="none" stroke="{GOLD[1]}" stroke-width="3"/><circle cx="195" cy="160" r="8" fill="{GOLD[2]}"/><rect x="250" y="146" width="10" height="28" rx="3" fill="{STEEL[2]}"/>'
    return s
def niche(x,c,gem):
    return f'''<path d="M{x} 150 L{x} 74 Q{x} 46 {x+35} 46 Q{x+70} 46 {x+70} 74 L{x+70} 150 Z" fill="{GOLD[2]}"/><path d="M{x+5} 150 L{x+5} 76 Q{x+5} 52 {x+35} 52 Q{x+65} 52 {x+65} 76 L{x+65} 150 Z" fill="{CRIM[2]}"/>
      <circle cx="{x+35}" cy="102" r="26" fill="#fff4d0" opacity=".16"/>{two(x+18,120,34,30,MARBLE[0],MARBLE[1],2)}<rect x="{x+14}" y="116" width="42" height="6" rx="2" fill="{MARBLE[2]}"/>{crown(x+35,116,34,c,gem)}'''
def crown_vault_head():
    w=f'<rect x="0" y="0" width="390" height="214" fill="{VSTONE[1]}"/>'
    w+=''.join(f'<rect x="{x}" y="{y}" width="60" height="30" rx="2" fill="{VSTONE[0] if (x//64+r)%2 else VSTONE[2]}" opacity=".55"/>' for r,y in enumerate(range(2,214,34)) for x in range(-30+(r%2)*32,390,64))
    w+=f'<rect x="0" y="0" width="390" height="10" fill="{GOLD[2]}"/><rect x="0" y="10" width="390" height="3" fill="{GOLD[1]}"/>'
    w+=''.join(f'<path d="M{x} 13 Q{x+32} 40 {x+65} 13 Z" fill="{CRIM[0]}"/><path d="M{x+32} 26 Q{x+50} 24 {x+65} 13 L{x+32} 13 Z" fill="{CRIM[1]}"/><circle cx="{x}" cy="15" r="4" fill="{GOLD[1]}"/>' for x in range(0,390,65))
    w+=niche(26,GOLD[1],CRIM[0])+niche(294,'#e8e2d6',BLUE[0])
    w+=f'<rect x="0" y="150" width="390" height="64" fill="{VSTONE[2]}"/><rect x="0" y="148" width="390" height="5" fill="{GOLD[2]}"/>'
    w+=f'<path d="M171 40 L219 40 L219 70 Q219 92 195 100 Q171 92 171 70 Z" fill="{CRIM[0]}"/><path d="M195 40 L219 40 L219 70 Q219 92 195 100 Z" fill="{CRIM[1]}"/><path d="M171 40 L219 40 L219 70 Q219 92 195 100 Q171 92 171 70 Z" fill="none" stroke="{GOLD[1]}" stroke-width="3"/>'+crown(195,74,30)
    w+=vault_door()
    return w
def glow(cx,cy,r): return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff4d0" opacity=".18"/>'
def crown_plinth(x,y):
    return f'''<g transform="translate({x} {y})">{glow(30,30,30)}{shadow(30,122,26,5)}{two(10,48,40,66,MARBLE[0],MARBLE[1],2)}<rect x="4" y="112" width="52" height="10" rx="2" fill="{MARBLE[2]}"/><rect x="4" y="42" width="52" height="9" rx="2" fill="{GOLD[1]}"/>
      <rect x="14" y="62" width="32" height="36" rx="2" fill="none" stroke="{GOLD[1]}" stroke-width="2"/>{crown(30,42,46)}</g>'''
def orb_sceptre(x,y):
    return f'''<g transform="translate({x} {y})">{glow(36,30,30)}{shadow(36,92,32,5)}<path d="M14 54 L10 92 M58 54 L62 92" stroke="{GOLD[2]}" stroke-width="5"/>{two(2,46,68,10,CRIM[0],CRIM[1],3)}<path d="M4 56 L68 56" stroke="{GOLD[1]}" stroke-width="2"/>
      <circle cx="24" cy="32" r="14" fill="{GOLD[1]}"/><path d="M24 18 A14 14 0 0 1 24 46 Z" fill="{GOLD[2]}"/><path d="M10 32 L38 32 M24 18 L24 46" stroke="{Q["cream"]}" stroke-width="2"/><path d="M24 18 L24 8 M19 12 L29 12" stroke="{GOLD[1]}" stroke-width="3"/><circle cx="24" cy="32" r="3" fill="{CRIM[0]}"/>
      <g transform="rotate(28 52 30)"><rect x="49" y="4" width="6" height="44" rx="2" fill="{GOLD[1]}"/><circle cx="52" cy="2" r="6" fill="{BLUE[0]}"/><path d="M46 8 L58 8" stroke="{GOLD[2]}" stroke-width="3"/></g></g>'''
def sword_case(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(52,72,50,5)}<path d="M10 40 L8 72 M94 40 L96 72" stroke="{GOLD[2]}" stroke-width="5"/>{two(0,34,104,9,GOLD[1],GOLD[2],2)}
      <rect x="2" y="6" width="100" height="30" rx="3" fill="#cfe7ee" opacity=".75"/><rect x="2" y="6" width="100" height="30" rx="3" fill="none" stroke="{GOLD[1]}" stroke-width="2.4"/><rect x="4" y="26" width="96" height="9" fill="{CRIM[1]}"/>
      <path d="M14 22 L72 22 L80 25 L72 28 L14 28 Z" fill="{STEEL[0]}"/><path d="M14 25 L80 25 L72 28 L14 28 Z" fill="{STEEL[1]}"/><rect x="72" y="16" width="5" height="18" rx="2" fill="{GOLD[1]}"/><rect x="77" y="22" width="16" height="6" rx="2" fill="{GOLD[2]}"/><circle cx="95" cy="25" r="4" fill="{CRIM[0]}"/><circle cx="74.5" cy="25" r="2" fill="{BLUE[0]}"/>
      <path d="M10 10 L26 10" stroke="#fff" stroke-width="2" opacity=".7"/></g>'''
def tiara(tx,ty,c): return f'<path d="M{tx-12} {ty} Q{tx} {ty-14} {tx+12} {ty}" stroke="{GOLD[1]}" stroke-width="3" fill="none"/><path d="M{tx-6} {ty-5} L{tx} {ty-14} L{tx+6} {ty-5}" fill="{GOLD[1]}"/><circle cx="{tx}" cy="{ty-8}" r="2.6" fill="{c}"/>'
def tiara_cabinet(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(32,124,30,5)}{two(2,4,60,116,GOLD[1],GOLD[2],3)}<rect x="8" y="12" width="48" height="98" rx="2" fill="{CRIM[1]}"/><rect x="8" y="12" width="48" height="98" rx="2" fill="#cfe7ee" opacity=".22"/>
      {"".join(f'<rect x="8" y="{yy}" width="48" height="3" fill="{GOLD[2]}"/>' for yy in (42,74,106))}{tiara(32,40,BLUE[0])}{tiara(32,72,CRIM[0])}
      <path d="M16 90 Q32 106 48 90" stroke="{GOLD[1]}" stroke-width="2" fill="none"/>{"".join(f'<circle cx="{px}" cy="{py}" r="2.4" fill="{c}"/>' for px,py,c in ((22,97,Q["green"]),(32,101,CRIM[0]),(42,97,Q["green"])))}
      <path d="M14 18 L22 18" stroke="#fff" stroke-width="2" opacity=".7"/><rect x="0" y="118" width="64" height="6" rx="2" fill="{GOLD[2]}"/><circle cx="52" cy="62" r="2" fill="{GOLD[0]}"/></g>'''
def ring_tray(x,y):
    return f'''<g transform="translate({x} {y})">{glow(32,24,22)}{shadow(32,72,26,5)}<rect x="28" y="34" width="8" height="38" fill="{GOLD[2]}"/><path d="M16 72 L32 64 L48 72" stroke="{GOLD[2]}" stroke-width="5" fill="none" stroke-linecap="round"/>
      <ellipse cx="32" cy="32" rx="30" ry="8" fill="{GOLD[1]}"/><ellipse cx="32" cy="30" rx="26" ry="6" fill="{CRIM[1]}"/>
      {"".join(f'<ellipse cx="{rx}" cy="{ry}" rx="5" ry="3.4" fill="none" stroke="{GOLD[0]}" stroke-width="2"/><circle cx="{rx}" cy="{ry-3.6}" r="2.2" fill="{c}"/>' for rx,ry,c in ((18,30,BLUE[0]),(32,28,CRIM[0]),(46,30,Q["green"]),(26,33,'#fff4d0'),(40,33,GRN[0])))}</g>'''
def ermine_robe(x,y):
    spots=''.join(f'<path d="M{sx} {sy} l1.4 3 l-2.8 0 Z" fill="{DARK}"/>' for sx,sy in ((12,62),(14,86),(12,108),(48,62),(46,86),(48,108),(24,28),(36,28)))
    return f'''<g transform="translate({x} {y})">{shadow(30,124,26,5)}<rect x="27" y="4" width="6" height="16" fill="{WOOD[2]}"/><ellipse cx="30" cy="6" rx="8" ry="6" fill="{WOOD[1]}"/>
      <path d="M14 20 Q30 14 46 20 L56 118 L4 118 Z" fill="{CRIM[0]}"/><path d="M30 18 Q40 16 46 20 L56 118 L30 118 Z" fill="{CRIM[1]}"/>
      <path d="M8 18 Q30 10 52 18 L50 34 Q30 26 10 34 Z" fill="#fbf6ec"/><path d="M6 50 L18 52 L16 118 L4 118 Z M54 50 L42 52 L44 118 L56 118 Z" fill="#fbf6ec"/>{spots}
      <path d="M22 118 L38 118 L36 124 L24 124 Z" fill="{WOOD[2]}"/></g>'''
def crowned_bust(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(28,124,24,5)}{two(10,62,36,52,MARBLE[0],MARBLE[1],2)}<rect x="4" y="112" width="48" height="10" rx="2" fill="{MARBLE[2]}"/><rect x="6" y="58" width="44" height="7" rx="2" fill="{MARBLE[2]}"/>
      <path d="M8 58 Q8 40 28 40 Q48 40 48 58 Z" fill="{MARBLE[0]}"/><path d="M28 40 Q48 40 48 58 L28 58 Z" fill="{MARBLE[1]}"/><rect x="22" y="32" width="12" height="10" fill="{MARBLE[1]}"/>
      <ellipse cx="28" cy="24" rx="12" ry="14" fill="{MARBLE[0]}"/><path d="M28 10 Q40 12 40 24 Q40 36 28 38 Z" fill="{MARBLE[1]}"/><path d="M15 22 Q12 26 16 28" stroke="{MARBLE[2]}" stroke-width="2" fill="none"/>
      {crown(28,14,24)}<path d="M10 52 Q28 60 46 52" stroke="{GOLD[1]}" stroke-width="2.4" fill="none"/><circle cx="28" cy="56" r="3.4" fill="{GOLD[1]}"/></g>'''

H6['Watchtower']=watchtower_head()+STEP
add6('watch_pillar',watch_pillar(0,0),(0,0,44,114)); add6('map_table',map_table(0,0),(0,2,96,76)); add6('spyglass_rack',spyglass_rack(0,0),(-4,-8,68,114))
add6('signal_horn',signal_horn(0,0),(0,4,74,98)); add6('beacon_lamp',beacon_lamp(0,0),(0,-14,52,144)); add6('log_desk',log_desk(0,0),(0,-8,60,120))
add6('weathervane',weathervane(0,0),(0,-10,72,144)); add6('watch_bench',watch_bench(0,0),(0,8,92,54))
H6['Belfry']=belfry_head()+STEP
add6('old_bell',old_bell(0,0),(0,0,80,84)); add6('bell_frame',bell_frame(0,0),(0,2,72,102)); add6('loft_ladder',loft_ladder(0,0),(-2,-2,52,134))
add6('rope_coil',rope_coil(0,0),(0,10,84,34)); add6('bat_post',bat_post(0,0),(0,4,74,120)); add6('handbell_table',handbell_table(0,0),(0,0,92,74))
add6('clapper_crate',clapper_crate(0,0),(0,-4,68,68))
H6['Crown vault']=crown_vault_head()   # no step: the round vault door comes right down to the floor
add6('crown_plinth',crown_plinth(0,0),(0,0,60,124)); add6('orb_sceptre',orb_sceptre(0,0),(0,0,72,94)); add6('sword_case',sword_case(0,0),(0,4,104,70))
add6('tiara_cabinet',tiara_cabinet(0,0),(0,2,64,124)); add6('ring_tray',ring_tray(0,0),(0,2,64,72)); add6('ermine_robe',ermine_robe(0,0),(0,0,60,126))
add6('crowned_bust',crowned_bust(0,0),(0,-2,56,126))
H6={k:re.sub(r'\s+',' ',v).strip() for k,v in H6.items()}
json.dump({'heads':H6,'props':P6},open('./towers_art.json','w'),separators=(',',':'),ensure_ascii=False)
print({k:len(v) for k,v in H6.items()}, len(P6))
# No board walls on this floor (Matt).
