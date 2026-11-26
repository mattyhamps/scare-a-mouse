import json, math, re
# ================= Towers and roof: Battlements, Aviary (more rooms of this floor to follow)
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
H6={k:re.sub(r'\s+',' ',v).strip() for k,v in H6.items()}
json.dump({'heads':H6,'props':P6},open('./towers_art.json','w'),separators=(',',':'),ensure_ascii=False)
print({k:len(v) for k,v in H6.items()}, len(P6))
# No board walls on this floor (Matt).
