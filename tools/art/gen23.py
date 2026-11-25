import json, re
g22=open('./gen22.py').read()
exec(g22[:g22.index("STEP_=STEP")])
NEW={}
def addn(name,svg,box): NEW[name]=[list(box),re.sub(r'\s+',' ',svg).strip()]
# ---------- Toy room: words in blocks, more toys
COLS=[(Q["navy"],Q["navy2"]),(Q["coral"],Q["coral2"]),(Q["olive"],Q["olive2"]),(Q["mustard"],Q["mustard2"]),(Q["orange"],Q["orange2"])]
def word_row(word,s=22,seed=0):
    return ''.join(block(k*(s+2),0,*COLS[(k+seed)%5],ch,s) for k,ch in enumerate(word))
def word_blocks(word,seed=0,s=22):
    w=len(word)*(s+2)
    return f'<g>{shadow(w/2,s+3,w/2+4,4)}{word_row(word,s,seed)}</g>', (0,-2,w,s+8)
def play_pyramid():
    s=22; g=f'<g>{shadow(48,48,50,5)}'+word_row("PLAY",s,1).replace('<g transform="translate(','<g transform="translate(',1)
    g=f'<g>{shadow(48,48,50,5)}<g transform="translate(0 24)">{word_row("PLAY",s,1)}</g><g transform="translate(24 0)">{word_row("!!",s,3)}</g></g>'
    return g,(0,-2,96,52)
def jack_box(x,y):
    spring=''.join(f'<path d="M14 {30-k*6} q8 -3 16 0" stroke="#9a97a4" stroke-width="2.4" fill="none"/>' for k in range(4))
    return f'''<g transform="translate({x} {y})">{shadow(22,62,24,5)}{two(2,32,40,30,Q["coral"],Q["coral2"],3)}<path d="M8 36 L18 46 L8 56 M28 36 L38 46 L28 56" stroke="{Q["mustard"]}" stroke-width="2.4" fill="none"/>
      <rect x="0" y="28" width="44" height="6" rx="2" fill="{Q["coral2"]}"/><rect x="0" y="6" width="6" height="26" rx="2" fill="{Q["coral"]}" transform="rotate(-25 3 30)"/>{spring}
      <circle cx="22" cy="2" r="9" fill="{Q["cream"]}"/><circle cx="19" cy="1" r="1.4" fill="{DARK}"/><circle cx="25" cy="1" r="1.4" fill="{DARK}"/><path d="M18 5 q4 3 8 0" stroke="{Q["coral"]}" stroke-width="1.6" fill="none"/>
      <path d="M12 -4 L22 -18 L32 -4 Z" fill="{Q["navy"]}"/><circle cx="22" cy="-18" r="3" fill="{Q["mustard"]}"/><path d="M42 44 L50 44" stroke="{Q["mustard2"]}" stroke-width="3"/><circle cx="51" cy="44" r="3" fill="{Q["mustard"]}"/></g>'''
def dollhouse(x,y):
    win=lambda wx,wy: f'<rect x="{wx}" y="{wy}" width="14" height="14" rx="2" fill="#a9cbe0"/><rect x="{wx+6}" y="{wy}" width="2" height="14" fill="{Q["cream"]}"/>'
    return f'''<g transform="translate({x} {y})">{shadow(40,88,44,6)}<path d="M2 30 L40 0 L78 30 Z" fill="{Q["coral"]}"/><path d="M40 0 L78 30 L60 30 Z" fill="{Q["coral2"]}"/>{two(8,28,64,60,Q["cream"],Q["cream2"],2)}
      {win(16,38)}{win(50,38)}{win(16,62)}<path d="M50 88 L50 66 Q57 58 64 66 L64 88 Z" fill="{Q["navy"]}"/><rect x="34" y="12" width="12" height="12" rx="6" fill="#a9cbe0"/><rect x="58" y="4" width="8" height="16" fill="{Q["brown"]}"/></g>'''
def xylophone(x,y):
    bars=''.join(f'<rect x="{6+k*11}" y="{2+k*2}" width="9" height="{30-k*4}" rx="2" fill="{COLS[k%5][0]}"/><circle cx="{10.5+k*11}" cy="{6+k*2}" r="1.2" fill="#fff" opacity=".7"/>' for k in range(6))
    return f'''<g transform="translate({x} {y})">{shadow(38,50,40,5)}<path d="M4 34 L10 50 M72 28 L66 50" stroke="{WOOD[2]}" stroke-width="4" stroke-linecap="round"/><rect x="8" y="46" width="60" height="4" rx="2" fill="{WOOD[2]}"/>
      <path d="M0 2 L76 10 L76 30 L0 36 Z" fill="{WOOD[1]}"/><path d="M40 6 L76 10 L76 30 L40 33 Z" fill="{WOOD[2]}"/>{bars}<g transform="rotate(30 64 -6)"><rect x="62" y="-20" width="3" height="24" fill="{WOOD[0]}"/><circle cx="63.5" cy="-21" r="4" fill="{Q["coral"]}"/></g></g>'''
def toy_boat(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(32,54,34,5)}<path d="M0 30 L64 30 L54 46 L10 46 Z" fill="{Q["navy"]}"/><path d="M32 30 L64 30 L54 46 L32 46 Z" fill="{Q["navy2"]}"/><rect x="0" y="28" width="64" height="5" fill="{Q["cream"]}"/>
      <rect x="30" y="-6" width="3" height="36" fill="{WOOD[2]}"/><path d="M33 -4 L56 24 L33 24 Z" fill="{Q["cream"]}"/><path d="M30 0 L10 24 L30 24 Z" fill="{Q["coral"]}"/><path d="M33 -6 L44 -2 L33 2 Z" fill="{Q["mustard"]}"/>
      <circle cx="14" cy="50" r="5" fill="{DARK}"/><circle cx="50" cy="50" r="5" fill="{DARK}"/></g>'''
def pull_duck(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(24,40,26,4)}<path d="M4 20 Q6 34 22 34 Q38 34 40 22 Q28 24 22 16 Z" fill="{Q["mustard"]}"/><path d="M22 34 Q38 34 40 22 Q30 26 26 22 Z" fill="{Q["mustard2"]}"/><circle cx="30" cy="12" r="8" fill="{Q["mustard"]}"/>
      <path d="M37 10 L46 12 L37 15 Z" fill="{Q["orange"]}"/><circle cx="31" cy="10" r="1.5" fill="{DARK}"/><circle cx="12" cy="38" r="4" fill="{Q["coral"]}"/><circle cx="32" cy="38" r="4" fill="{Q["coral"]}"/><path d="M4 30 Q-10 34 -16 44" stroke="{DARK}" stroke-width="1.4" fill="none"/></g>'''
def marbles(x,y): return f'<g transform="translate({x} {y})">'+''.join(f'<circle cx="{dx}" cy="{dy}" r="4.5" fill="{c}"/><circle cx="{dx-1.4}" cy="{dy-1.4}" r="1.4" fill="#fff" opacity=".8"/>' for dx,dy,c in ((6,8,Q["navy"]),(16,4,Q["coral"]),(18,13,Q["olive"]),(28,9,Q["mustard"])))+'</g>'
def toy_soldier(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(10,50,10,3)}<rect x="3" y="-10" width="14" height="14" rx="2" fill="{DARK}"/><circle cx="10" cy="8" r="6" fill="{Q["cream"]}"/><circle cx="8" cy="7" r="1" fill="{DARK}"/><circle cx="12" cy="7" r="1" fill="{DARK}"/>
      {two(2,14,16,18,Q["coral"],Q["coral2"],2)}<path d="M4 18 L16 18 M4 23 L16 23" stroke="{Q["mustard"]}" stroke-width="1.6"/>{two(3,32,6,16,Q["navy"],Q["navy2"],1)}{two(11,32,6,16,Q["navy"],Q["navy2"],1)}</g>'''
def pinwheel(x,y):
    blades=''.join(f'<path d="M0 0 L0 -16 Q10 -12 0 0 Z" fill="{COLS[k][0]}" transform="rotate({k*90})"/>' for k in range(4))
    return f'<g transform="translate({x} {y})">{shadow(4,52,8,3)}<rect x="-1.5" y="0" width="3" height="52" fill="{WOOD[1]}"/>{blades}<circle cx="0" cy="0" r="2.4" fill="{Q["mustard"]}"/></g>'
def toy_room_head2():
    w=wallpaper(3)+f'<rect x="0" y="176" width="390" height="38" fill="#c58a55"/><rect x="0" y="176" width="390" height="6" fill="#a06a3e"/>'
    w+=toy_window(28,46)+kite(300,20)
    w+=f'<g transform="translate(96 128)"><rect x="0" y="40" width="96" height="7" rx="2" fill="{WOOD[1]}"/><g transform="translate(4 18)">{word_row("HI",22,0)}</g></g>'
    w+=f'<g transform="translate(270 128)"><rect x="0" y="40" width="96" height="7" rx="2" fill="{WOOD[1]}"/><g transform="translate(4 18)">{word_row("TOY",22,2)}</g><circle cx="86" cy="24" r="9" fill="{Q["coral"]}"/><path d="M77 24 A9 9 0 0 0 95 24 Z" fill="{Q["cream"]}"/></g>'
    w+=''.join(f'<path d="M{150+k*18} {28+(k%2)*8} l9 -14 l9 14 Z" fill="{PASTEL[k%5]}"/>' for k in range(5))+f'<path d="M140 30 Q195 46 250 30" stroke="{DARK}" stroke-width="1.4" fill="none"/>'
    w+=f'<rect x="150" y="104" width="90" height="110" fill="#e0b0a4"/>'+gate_arch(164,62,(Q["navy"],Q["navy2"]))+f'<g transform="translate(195 140)"><path d="M0 -10 L3 -3 L10 -3 L4 2 L6 9 L0 5 L-6 9 L-4 2 L-10 -3 L-3 -3 Z" fill="{Q["mustard"]}"/></g>'
    return w
for word,seed in (("CAT",0),("DOG",1),("LION",2),("BEAR",3),("MOUSE",4),("FUN",0),("EEK!",1),("TOY",2),("YAY",3)):
    svg,box=word_blocks(word,seed); addn('blocks_'+word.strip('!').lower(),svg,box)
svg,box=play_pyramid(); addn('blocks_play',svg,box)
addn('jack_box',jack_box(0,0),(0,-20,56,84)); addn('dollhouse',dollhouse(0,0),(0,0,80,94)); addn('xylophone',xylophone(0,0),(0,-26,78,80))
addn('toy_boat',toy_boat(0,0),(0,-8,66,64)); addn('pull_duck',pull_duck(0,0),(-18,0,66,44)); addn('marbles',marbles(0,0),(0,0,34,18)); addn('toy_soldier',toy_soldier(0,0),(0,-10,20,62)); addn('pinwheel',pinwheel(0,0),(-16,-16,32,70))
# ---------- Hall of mirrors: more kinds of things
def triple_mirror(x,y):
    p=lambda dx,w,h,dy: f'<g transform="translate({dx} {dy})">{mirror_shape(w,h)}</g>'
    return f'<g transform="translate({x} {y})">{shadow(46,96,48,5)}{p(0,26,70,14)}{p(28,36,84,0)}{p(66,26,70,14)}<rect x="6" y="84" width="80" height="8" rx="2" fill="{Q["mustard2"]}"/></g>'
def chaise(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(50,46,52,6)}<rect x="10" y="34" width="4" height="12" fill="{Q["mustard2"]}"/><rect x="86" y="34" width="4" height="12" fill="{Q["mustard2"]}"/>
      <path d="M0 20 Q0 6 14 4 Q24 4 24 16 L100 16 L100 36 L0 36 Z" fill="#7a4a7a"/><path d="M60 16 L100 16 L100 36 L60 36 Z" fill="#5e3460"/><rect x="24" y="14" width="76" height="8" rx="4" fill="#9a6a9a"/>{"".join(f"<circle cx=\"{34+k*16}\" cy=\"28\" r=\"1.8\" fill=\"{Q['mustard']}\"/>" for k in range(4))}</g>'''
def vanity(x,y):
    bottles=''.join(f'<g transform="translate({8+k*14} {-12-(k%2)*4})"><rect x="0" y="4" width="10" height="12" rx="3" fill="{c}"/><rect x="3" y="0" width="4" height="5" fill="{Q["mustard"]}"/></g>' for k,c in enumerate((Q["pink"],"#a9cbe0",Q["coral"],"#cfe0a8")))
    return f'<g transform="translate({x} {y})">{shadow(36,48,38,5)}<rect x="4" y="10" width="4" height="38" fill="{Q["mustard2"]}"/><rect x="64" y="10" width="4" height="38" fill="{Q["mustard2"]}"/>{two(0,4,72,10,Q["cream"],Q["cream2"],3)}<path d="M4 14 Q36 26 68 14" stroke="{Q["pink"]}" stroke-width="3" fill="none"/>{bottles}</g>'
def gold_clock(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(18,104,20,5)}{two(4,24,28,80,Q["mustard"],Q["mustard2"],4)}<path d="M2 26 Q18 -6 34 26 Z" fill="{Q["mustard"]}"/><path d="M18 2 Q30 8 34 26 L18 26 Z" fill="{Q["mustard2"]}"/>
      <circle cx="18" cy="22" r="11" fill="{Q["cream"]}"/><path d="M18 22 L18 14 M18 22 L24 24" stroke="{DARK}" stroke-width="1.8" stroke-linecap="round"/><rect x="10" y="44" width="16" height="44" rx="3" fill="#a9cbe0"/><path d="M18 46 L18 72" stroke="{Q["mustard2"]}" stroke-width="1.6"/><circle cx="18" cy="76" r="5" fill="{Q["mustard"]}"/></g>'''
def fan(x,y):
    ribs=''.join(f'<path d="M14 18 L{14+22*__import__("math").cos(a)} {18-22*__import__("math").sin(a)}" stroke="{Q["coral2"]}" stroke-width="1"/>' for a in [0.35+k*0.3 for k in range(9)])
    return f'<g transform="translate({x} {y})"><path d="M14 18 L{14+22*0.94} {18-22*0.34} A22 22 0 0 0 {14-22*0.94} {18-22*0.34} Z" fill="{Q["pink"]}"/>{ribs}<circle cx="14" cy="18" r="2.4" fill="{Q["mustard"]}"/></g>'
def petals(x,y): return f'<g transform="translate({x} {y})">'+''.join(f'<ellipse cx="{dx}" cy="{dy}" rx="4" ry="2.4" fill="{Q["coral"]}" transform="rotate({r} {dx} {dy})"/>' for dx,dy,r in ((4,6,20),(14,2,-30),(20,10,60),(9,13,-10)))+'</g>'
def perfume(x,y): return f'<g transform="translate({x} {y})">{shadow(8,18,8,2)}<path d="M2 6 Q8 2 14 6 L14 16 Q8 20 2 16 Z" fill="#a9cbe0"/><rect x="6" y="0" width="4" height="6" fill="{Q["mustard"]}"/><circle cx="8" cy="-2" r="3" fill="{Q["pink"]}"/></g>'
def mirrors_head2():
    w=f'<rect x="0" y="0" width="390" height="214" fill="#2f5560"/>'+''.join(f'<rect x="{x}" y="0" width="10" height="214" fill="#284a54"/>' for x in (6,128,252,374))
    w+=''.join(f'<rect x="{x}" y="0" width="4" height="214" fill="{Q["mustard2"]}" opacity=".7"/>' for x in (9,131,255,377))
    w+=f'<g transform="translate(22 40)">{mirror_shape(48,124)}</g><g transform="translate(80 70)">{mirror_shape(34,34,True)}</g><g transform="translate(276 56)">{mirror_shape(38,62,True)}</g><g transform="translate(326 40)">{mirror_shape(44,124)}</g>'
    w+=f'<g transform="translate(80 120)">{candelabra(0,0)}</g><g transform="translate(276 128)">{vanity(0,0)}</g>'
    w+=chandelier(195,52)
    w+=f'<rect x="146" y="102" width="98" height="112" fill="#244650"/>'+gate_arch(164,62,(Q["mustard"],Q["mustard2"]))+f'<path d="M172 150 C172 128 210 128 210 150" stroke="#fff" stroke-opacity=".35" stroke-width="3" fill="none"/>'
    return w
addn('triple_mirror',triple_mirror(0,0),(0,0,94,100)); addn('chaise',chaise(0,0),(0,0,102,52)); addn('vanity',vanity(0,0),(0,-18,72,68)); addn('gold_clock',gold_clock(0,0),(0,0,38,108))
addn('fan',fan(0,0),(-8,-6,44,26)); addn('petals',petals(0,0),(0,0,26,18)); addn('perfume',perfume(0,0),(0,-6,18,26))
# ---------- Trophy room: more kinds of things
def trophy_cabinet(x,y):
    shelf=lambda yy,items: f'<rect x="4" y="{yy}" width="72" height="4" fill="{WOOD[2]}"/>{items}'
    return f'''<g transform="translate({x} {y})">{shadow(40,104,44,6)}{two(0,0,80,104,WOOD[1],WOOD[2],4)}<rect x="5" y="5" width="70" height="94" rx="2" fill="#2f5530"/>
      {shelf(34,cup(10,6,.6)+cup(42,10,.5,"#c4c1cc","#9a97a4"))}{shelf(66,medal_ribbon(12,36,Q["navy"],Q["coral"])+cup(40,40,.6,"#c58a55","#a06a3e"))}{shelf(96,f'<g transform="translate(14 72)">{plaque(0,0)}</g>'.replace("translate(0 0)","translate(0 0) scale(.6)"))}
      <rect x="5" y="5" width="70" height="94" rx="2" fill="#a9cbe0" opacity=".18"/><path d="M14 90 L40 10 L46 10 L20 90 Z" fill="#fff" opacity=".12"/></g>'''
def cup_plinth(x,y):
    return f'<g transform="translate({x} {y})">{shadow(26,100,28,5)}{two(6,60,40,40,Q["grey"],Q["grey2"],2)}<rect x="2" y="56" width="48" height="8" rx="2" fill="{Q["grey"]}"/><rect x="10" y="74" width="32" height="10" rx="2" fill="{Q["mustard"]}"/>{cup(2,0,1.2)}</g>'
def crest_stand(x,y):
    return f'''<g transform="translate({x} {y})">{shadow(26,90,26,5)}<path d="M12 90 L26 60 L40 90" stroke="{WOOD[2]}" stroke-width="4" fill="none"/>
      <path d="M2 0 L50 0 L50 30 Q50 56 26 66 Q2 56 2 30 Z" fill="{Q["navy"]}"/><path d="M26 0 L50 0 L50 30 Q50 56 26 66 Z" fill="{Q["navy2"]}"/><path d="M26 0 L26 66 M2 28 L50 28" stroke="{Q["mustard"]}" stroke-width="3"/>
      <circle cx="14" cy="14" r="5" fill="{Q["mustard"]}"/><path d="M38 40 L41 47 L48 47 L42 51 L44 58 L38 54 L32 58 L34 51 L28 47 L35 47 Z" fill="{Q["mustard"]}"/></g>'''
def pennants(x,y):
    flags=''.join(f'<path d="M{k*20} 4 L{k*20+18} 4 L{k*20+9} 26 Z" fill="{c}"/>' for k,c in enumerate((Q["coral"],Q["mustard"],Q["navy"],Q["olive"],Q["coral"])))
    return f'<g transform="translate({x} {y})">{shadow(50,62,48,4)}<rect x="0" y="0" width="4" height="62" fill="{WOOD[2]}"/><rect x="96" y="0" width="4" height="62" fill="{WOOD[2]}"/><path d="M2 4 Q50 14 98 4" stroke="{DARK}" stroke-width="1.4" fill="none"/><g transform="translate(2 0)">{flags}</g></g>'
def rosette(x,y,c=None):
    c=c or Q["navy"]
    petals=''.join(f'<circle cx="{10+7*__import__("math").cos(a*0.785)}" cy="{10+7*__import__("math").sin(a*0.785)}" r="4" fill="{c}"/>' for a in range(8))
    return f'<g transform="translate({x} {y})"><path d="M6 14 L2 30 L8 26 L10 32 L12 16 Z" fill="{c}"/><path d="M14 14 L18 30 L12 26 L10 32 L8 16 Z" fill="{Q["coral"]}"/>{petals}<circle cx="10" cy="10" r="5" fill="{Q["mustard"]}"/></g>'
def laurel(x,y):
    leaves=''.join(f'<ellipse cx="{18+15*__import__("math").cos(a)}" cy="{18+15*__import__("math").sin(a)}" rx="4" ry="2" fill="{Q["olive"] if k%2 else Q["green"]}" transform="rotate({a*57.3+90} {18+15*__import__("math").cos(a)} {18+15*__import__("math").sin(a)})"/>' for k,a in enumerate([0.6+i*0.42 for i in range(12)]))
    return f'<g transform="translate({x} {y})">{leaves}<path d="M14 34 L18 30 L22 34" stroke="{Q["coral"]}" stroke-width="3" fill="none"/></g>'
def sport_ball(x,y): return f'<g transform="translate({x} {y})">{shadow(11,21,11,3)}<circle cx="11" cy="11" r="10" fill="{Q["cream"]}"/><path d="M11 1 A10 10 0 0 1 11 21 Z" fill="{Q["cream2"]}"/><path d="M3 5 Q11 11 3 17 M19 5 Q11 11 19 17" stroke="{Q["coral"]}" stroke-width="1.6" fill="none"/></g>'
def trophy_head2():
    w=f'<rect x="0" y="0" width="390" height="214" fill="#2f5530"/>'+''.join(f'<rect x="{x}" y="0" width="22" height="214" fill="#2a4c2b"/>' for x in range(0,390,44))
    w+=f'<rect x="0" y="150" width="390" height="64" fill="{WOOD[2]}"/>'+''.join(f'<rect x="{x+2}" y="154" width="40" height="56" rx="3" fill="{WOOD[1]}"/>' for x in range(0,390,44))+f'<rect x="0" y="146" width="390" height="8" fill="{Q["mustard2"]}"/>'
    w+=f'<rect x="18" y="64" width="96" height="6" rx="2" fill="{WOOD[1]}"/><rect x="18" y="122" width="96" height="6" rx="2" fill="{WOOD[1]}"/>'+cup(24,20,.9)+f'<g transform="translate(68 28) scale(.7)">{crest_stand(0,0)}</g>'.replace(shadow(26,90,26,5),'')+laurel(28,84)+rosette(80,88,Q["coral"])
    w+=f'<rect x="276" y="64" width="96" height="6" rx="2" fill="{WOOD[1]}"/><rect x="276" y="122" width="96" height="6" rx="2" fill="{WOOD[1]}"/>'+cup(282,30,.7,"#c4c1cc","#9a97a4")+cup(326,20,.9,"#c58a55","#a06a3e")+medal_ribbon(286,76,Q["navy"],Q["coral"])+f'<g transform="translate(320 84)">{sport_ball(0,0)}</g>'.replace(shadow(11,21,11,3),'')
    w+=plaque(126,40)+plaque(228,40,Q["grey"])
    w+=f'<g transform="translate(195 30)"><path d="M-46 0 L46 0 L40 14 L46 28 L-46 28 L-40 14 Z" fill="{Q["coral"]}"/><path d="M0 0 L46 0 L40 14 L46 28 L0 28 Z" fill="{Q["coral2"]}"/><rect x="-30" y="12" width="60" height="4" rx="2" fill="{Q["mustard"]}"/></g>'
    w+=f'<rect x="148" y="104" width="94" height="110" fill="#244a25"/>'+gate_arch(164,62,(Q["coral"],Q["coral2"]))+''.join(f'<circle cx="{170+k*12.5}" cy="132" r="2" fill="{Q["mustard"]}"/>' for k in range(5))
    return w
addn('trophy_cabinet',trophy_cabinet(0,0),(0,0,80,108)); addn('cup_plinth',cup_plinth(0,0),(0,-2,54,104)); addn('crest_stand',crest_stand(0,0),(0,0,52,94)); addn('pennants',pennants(0,0),(0,0,100,66))
addn('rosette',rosette(0,0),(0,0,20,32)); addn('rosette_red',rosette(0,0,Q["coral"]),(0,0,20,32)); addn('laurel',laurel(0,0),(0,0,36,36)); addn('sport_ball',sport_ball(0,0),(0,0,22,24))
heads={'Toy room':toy_room_head2()+STEP,'Hall of mirrors':mirrors_head2()+STEP,'Trophy room':trophy_head2()+STEP}
heads={k:re.sub(r'\s+',' ',v).strip() for k,v in heads.items()}
json.dump({'heads':heads,'props':NEW},open('./third_floor_art2.json','w'),separators=(',',':'),ensure_ascii=False)
print(len(NEW), sorted(NEW))
