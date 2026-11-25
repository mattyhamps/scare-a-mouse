import json, math, random
src=open('./gen7.py').read()
exec(src[:src.index("lsv=lambda")])
def eyes2(x1,x2,y,r=4.6): return ''.join(f'<ellipse cx="{x}" cy="{y}" rx="3.6" ry="6.2" fill="#2b1d14"/>' for x in (x1,x2))
s4=open('./gen4.py').read(); exec(s4[s4.index("H={"):s4.index("def sv(k,size)")])
H['lion']=L2
rnd=random.Random(7)
def crd(ps):
    d=f'M {ps[0][0]} {ps[0][1]}'
    for i in range(len(ps)-1):
        a=ps[i-1] if i>0 else ps[i]; bb=ps[i]; c=ps[i+1]; e=ps[i+2] if i+2<len(ps) else c
        d+=f' C {bb[0]+(c[0]-a[0])/6:.1f} {bb[1]+(c[1]-a[1])/6:.1f}, {c[0]-(e[0]-bb[0])/6:.1f} {c[1]-(e[1]-bb[1])/6:.1f}, {c[0]} {c[1]}'
    return d
def node(n,x,y,state):
    bg={'done':Q['mustard'],'cur':Q['cream'],'next':Q['cream'],'lock':Q['lav']}[state]
    sh={'done':Q['mustard2'],'cur':Q['cream2'],'next':Q['cream2'],'lock':Q['lav2']}[state]
    ring=f'box-shadow:0 4px 0 {sh},0 0 0 6px {Q["coral"]};' if state=='cur' else f'box-shadow:0 4px 0 {sh};'
    tick=f'<b style="position:absolute;right:-6px;bottom:-6px;width:18px;height:18px;border-radius:50%;background:{Q["green"]};color:#fff;font:700 11px Fredoka;display:grid;place-items:center">✓</b>' if state=='done' else ''
    return f'<div style="position:absolute;left:{x-22}px;top:{y-22}px;width:44px;height:44px;border-radius:50%;background:{bg};{ring}display:grid;place-items:center;font:700 16px Fredoka,sans-serif;color:{Q["ink"]};z-index:3">{n}{tick}</div>'
pts=[(110,700),(180,665),(255,625),(290,560),(225,512),(140,478),(92,420),(150,372),(235,340),(290,282)]
road=crd([(195,860),(150,780)]+pts+[(240,220),(195,176)])
nodes=lambda base: ''.join(node(base+k,x,y,'done' if k<5 else 'cur' if k==5 else 'next' if k==6 else 'lock') for k,(x,y) in enumerate(pts))
# ---------- detailed meadow pieces (all two-tone, no outlines)
def tree(x,y,s=1,apples=True):
    g=f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="46" cy="104" rx="34" ry="8" fill="{Q["olive2"]}"/><path d="M38 60 L36 104 L58 104 L54 60 Z" fill="{Q["brown"]}"/><path d="M47 60 L50 104 L58 104 L54 60 Z" fill="{Q["brown2"]}"/><path d="M40 84 L30 74 M52 80 L62 70" stroke="{Q["brown2"]}" stroke-width="5" stroke-linecap="round"/>'
    g+=f'<circle cx="26" cy="46" r="24" fill="{Q["green"]}"/><circle cx="66" cy="46" r="24" fill="{Q["green2"]}"/><circle cx="46" cy="30" r="30" fill="{Q["green"]}"/><path d="M76 30 A30 30 0 0 1 60 56 A24 24 0 0 1 72 46 Z" fill="{Q["green2"]}"/><circle cx="34" cy="22" r="8" fill="#4f8a48" opacity=".7"/>'
    if apples: g+=''.join(f'<circle cx="{ax}" cy="{ay}" r="5" fill="{Q["coral"]}"/><circle cx="{ax+1.5}" cy="{ay-1.5}" r="1.6" fill="{Q["pink"]}"/>' for ax,ay in [(30,40),(56,24),(62,52),(20,58),(44,48)])
    return g+'</g>'
def bush(x,y,s=1,flowers=None):
    g=f'<g transform="translate({x} {y}) scale({s})"><circle cx="14" cy="20" r="14" fill="{Q["green"]}"/><circle cx="34" cy="16" r="16" fill="{Q["green"]}"/><circle cx="50" cy="22" r="12" fill="{Q["green2"]}"/><rect x="2" y="22" width="60" height="12" rx="6" fill="{Q["green2"]}"/>'
    if flowers: g+=''.join(f'<circle cx="{fx}" cy="{fy}" r="3" fill="{flowers}"/>' for fx,fy in [(12,14),(30,8),(42,18),(24,22)])
    return g+'</g>'
def flower(x,y,c,c2):
    return f'<g transform="translate({x} {y})"><rect x="-1.5" y="0" width="3" height="12" fill="{Q["green2"]}"/><circle cx="-4" cy="0" r="4" fill="{c}"/><circle cx="4" cy="0" r="4" fill="{c2}"/><circle cx="0" cy="-4" r="4" fill="{c}"/><circle cx="0" cy="4" r="4" fill="{c2}"/><circle cx="0" cy="0" r="2.6" fill="{Q["mustard"]}"/></g>'
def tuft(x,y): return f'<path d="M{x} {y} l4 -10 l3 10 l4 -8 l3 8" fill="none" stroke="{Q["olive2"]}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
def mush(x,y,c,c2,s=1): return f'<g transform="translate({x} {y}) scale({s})"><rect x="12" y="16" width="12" height="16" rx="5" fill="{Q["cream"]}"/><rect x="18" y="16" width="6" height="16" rx="3" fill="{Q["cream2"]}"/><path d="M0 20 Q18 -6 36 20 Z" fill="{c}"/><path d="M22 2 Q34 8 36 20 L26 20 Z" fill="{c2}"/><circle cx="12" cy="12" r="3" fill="{Q["cream"]}"/><circle cx="24" cy="8" r="2.4" fill="{Q["cream"]}"/></g>'
def fence(x,y,n):
    g=f'<g transform="translate({x} {y})"><rect x="0" y="10" width="{n*26}" height="6" rx="3" fill="{Q["tan"]}"/><rect x="0" y="24" width="{n*26}" height="6" rx="3" fill="{Q["tan2"]}"/>'
    g+=''.join(f'<path d="M{k*26} 4 L{k*26+5} 0 L{k*26+10} 4 L{k*26+10} 36 L{k*26} 36 Z" fill="{Q["tan"]}"/><rect x="{k*26+6}" y="4" width="4" height="32" fill="{Q["tan2"]}"/>' for k in range(n+1))
    return g+'</g>'
def pond(x,y):
    return f'''<g transform="translate({x} {y})"><ellipse cx="66" cy="46" rx="66" ry="36" fill="{Q["olive2"]}"/><ellipse cx="66" cy="42" rx="62" ry="32" fill="{Q["navy"]}"/><ellipse cx="66" cy="40" rx="58" ry="28" fill="{Q["slate"]}"/><path d="M28 40 Q40 34 52 40 M70 52 Q80 47 90 52" stroke="{Q["cream"]}" stroke-width="3" fill="none" stroke-linecap="round"/>
      <ellipse cx="96" cy="30" rx="13" ry="7" fill="{Q["olive"]}"/><path d="M96 30 L108 26 L106 32 Z" fill="{Q["slate"]}"/><circle cx="96" cy="28" r="3.4" fill="{Q["pink"]}"/>
      <g transform="translate(30 18)"><ellipse cx="12" cy="14" rx="14" ry="9" fill="{Q["cream"]}"/><circle cx="22" cy="6" r="6" fill="{Q["green"]}"/><path d="M27 6 L33 8 L27 10 Z" fill="{Q["mustard"]}"/><circle cx="23" cy="5" r="1.4" fill="{Q["ink"]}"/><path d="M4 12 Q12 8 18 14" fill="{Q["cream2"]}"/></g>
      <path d="M4 36 l2 -22 M10 38 l1 -26 M126 34 l-2 -22" stroke="{Q["green2"]}" stroke-width="3" stroke-linecap="round"/><ellipse cx="6" cy="14" rx="3" ry="7" fill="{Q["brown"]}"/><ellipse cx="11" cy="12" rx="3" ry="7" fill="{Q["brown2"]}"/><ellipse cx="124" cy="12" rx="3" ry="7" fill="{Q["brown"]}"/></g>'''
def picnic(x,y):
    return f'''<g transform="translate({x} {y}) rotate(-6 55 37)"><rect x="4" y="8" width="104" height="62" rx="8" fill="{Q["coral2"]}"/><rect x="4" y="4" width="104" height="60" rx="8" fill="{Q["coral"]}"/>
      <path d="M30 4 L30 64 M56 4 L56 64 M82 4 L82 64 M4 22 L108 22 M4 44 L108 44" stroke="{Q["cream"]}" stroke-width="7" opacity=".85"/>
      <g transform="translate(14 14)"><path d="M0 14 L36 14 L32 34 L4 34 Z" fill="{Q["tan"]}"/><path d="M18 14 L36 14 L32 34 L18 34 Z" fill="{Q["tan2"]}"/><path d="M4 14 Q18 -4 32 14" fill="none" stroke="{Q["brown"]}" stroke-width="3"/><circle cx="12" cy="12" r="5" fill="{Q["coral2"]}"/></g>
      <circle cx="74" cy="22" r="7" fill="{Q["coral2"]}"/><circle cx="75.5" cy="20.5" r="2" fill="{Q["pink"]}"/><path d="M62 42 L88 42 L80 54 L70 54 Z" fill="{Q["mustard"]}"/><path d="M75 42 L88 42 L80 54 L75 54 Z" fill="{Q["mustard2"]}"/></g>'''
def beehive(x,y):
    return f'''<g transform="translate({x} {y})"><rect x="22" y="40" width="8" height="40" fill="{Q["brown2"]}"/><rect x="6" y="38" width="40" height="6" rx="3" fill="{Q["brown"]}"/>
      <path d="M8 38 Q8 6 26 4 Q44 6 44 38 Z" fill="{Q["mustard"]}"/><path d="M26 4 Q44 6 44 38 L32 38 Q34 14 26 4 Z" fill="{Q["mustard2"]}"/>{''.join(f'<rect x="{9+i}" y="{12+i*7}" width="{34-2*i}" height="3" rx="1.5" fill="{Q["mustard2"]}"/>' for i in range(4))}
      <path d="M20 38 Q20 30 26 30 Q32 30 32 38 Z" fill="{Q["brown2"]}"/>
      {''.join(f'<g transform="translate({bx} {by})"><ellipse cx="0" cy="0" rx="5" ry="3.6" fill="{Q["mustard"]}"/><rect x="-1" y="-3.6" width="2" height="7.2" fill="{Q["ink"]}"/><ellipse cx="-1" cy="-4" rx="3" ry="2" fill="{Q["cream"]}" opacity=".9"/></g>' for bx,by in [(56,10),(-8,20),(60,30)])}</g>'''
def sign(x,y,txt):
    return f'<g transform="translate({x} {y})"><rect x="22" y="14" width="8" height="46" fill="{Q["brown2"]}"/><path d="M0 4 L50 4 L58 16 L50 28 L0 28 Z" fill="{Q["tan"]}"/><path d="M0 18 L54 18 L50 28 L0 28 Z" fill="{Q["tan2"]}"/><text x="25" y="21" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="11" fill="{Q["brown2"]}">{txt}</text></g>'
def butterfly(x,y,c,c2): return f'<g transform="translate({x} {y})"><ellipse cx="-5" cy="-3" rx="5" ry="6" fill="{c}"/><ellipse cx="5" cy="-3" rx="5" ry="6" fill="{c2}"/><ellipse cx="-4" cy="5" rx="3.6" ry="4" fill="{c}"/><ellipse cx="4" cy="5" rx="3.6" ry="4" fill="{c2}"/><rect x="-1" y="-6" width="2" height="14" rx="1" fill="{Q["ink"]}"/></g>'
def stones(path_pts):
    out=''
    for (x,y) in path_pts:
        out+=f'<ellipse cx="{x}" cy="{y}" rx="7" ry="4.5" fill="{Q["cream2"]}"/>'
    return out
# hills & head
head=f'''<rect x="0" y="0" width="390" height="190" fill="#9cb8c8"/><rect x="0" y="0" width="390" height="70" fill="#8aaabb"/>
  <circle cx="336" cy="86" r="20" fill="{Q["mustard"]}"/><circle cx="336" cy="86" r="28" fill="{Q["mustard"]}" opacity=".25"/>
  <g transform="translate(40 70)"><ellipse cx="0" cy="10" rx="18" ry="9" fill="{Q["cream"]}"/><ellipse cx="18" cy="6" rx="16" ry="12" fill="{Q["cream"]}"/><ellipse cx="36" cy="12" rx="14" ry="8" fill="{Q["cream2"]}"/></g>
  <g transform="translate(236 66) scale(.7)"><ellipse cx="0" cy="10" rx="18" ry="9" fill="{Q["cream"]}"/><ellipse cx="18" cy="6" rx="16" ry="12" fill="{Q["cream"]}"/><ellipse cx="36" cy="12" rx="14" ry="8" fill="{Q["cream2"]}"/></g>
  <path d="M-20 150 Q60 80 150 130 Q210 90 300 120 Q360 96 420 140 L420 190 L-20 190 Z" fill="#6f8f8a"/>
  <path d="M-20 170 Q90 100 200 160 Q300 110 420 150 L420 200 L-20 200 Z" fill="{Q["green"]}"/><path d="M200 160 Q300 110 420 150 L420 200 L240 200 Z" fill="{Q["green2"]}"/>
  {''.join(f'<g transform="translate({tx} {ty}) scale(.45)">{tree(0,0,1,False)}</g>' for tx,ty in [(20,104),(70,92),(300,100),(344,108)])}
  <rect x="150" y="104" width="90" height="80" rx="8" fill="{Q["lav"]}"/><rect x="210" y="104" width="30" height="80" rx="8" fill="{Q["lav2"]}"/>{''.join(f'<rect x="{150+k*20}" y="94" width="12" height="14" rx="2" fill="{Q["lav"]}"/>' for k in range(5))}
  <path d="M172 184 L172 144 C172 122 218 122 218 144 L218 184 Z" fill="{Q["brown"]}"/><path d="M195 124 C210 126 218 134 218 144 L218 184 L195 184 Z" fill="{Q["brown2"]}"/><circle cx="206" cy="156" r="3" fill="{Q["mustard"]}"/>
  {bush(-10,166,1,Q["pink"])}{bush(96,170,.9,Q["cream"])}{bush(240,168,.9,Q["mustard"])}{bush(330,166,1,Q["pink"])}'''
grass=''.join(tuft(rnd.randint(0,380),rnd.randint(200,840)) for _ in range(46))
flowers=''.join(flower(x,y,c,c2) for x,y,c,c2 in [(34,560,Q["pink"],Q["pink2"]),(56,584,Q["cream"],Q["cream2"]),(22,600,Q["mustard"],Q["mustard2"]),(330,640,Q["pink"],Q["pink2"]),(352,664,Q["cream"],Q["cream2"]),(310,676,Q["navy"],Q["navy2"]),(40,330,Q["cream"],Q["cream2"]),(344,234,Q["pink"],Q["pink2"]),(362,256,Q["mustard"],Q["mustard2"]),(200,770,Q["pink"],Q["pink2"]),(220,800,Q["cream"],Q["cream2"]),(30,800,Q["mustard"],Q["mustard2"])])
edge=stones([(76,760),(64,700),(150,640),(232,600),(324,566),(256,476),(172,452),(58,418),(120,350),(206,318),(322,300),(270,250)])
b=f'''<div style="{SC}background:{Q["olive"]}">
  <svg width="390" height="844" style="position:absolute;left:0;top:0">
    <rect x="0" y="190" width="390" height="660" fill="{Q["olive"]}"/>{''.join(f'<ellipse cx="{rnd.randint(0,390)}" cy="{rnd.randint(220,840)}" rx="{rnd.randint(30,60)}" ry="{rnd.randint(14,24)}" fill="#86a654" opacity=".55"/>' for _ in range(10))}
    {grass}
    {head}
    <path d="{road}" fill="none" stroke="{Q["tan2"]}" stroke-width="44" stroke-linecap="round" transform="translate(0 4)"/><path d="{road}" fill="none" stroke="{Q["tan"]}" stroke-width="42" stroke-linecap="round"/><path d="{road}" fill="none" stroke="#dcc08e" stroke-width="16" stroke-linecap="round"/>
    {fence(250,720,4)}{fence(-6,370,2)}
    {pond(222,392)}{picnic(20,214)}{beehive(30,470)}{tree(282,580,1)}{tree(-14,600,.9)}
    {mush(320,240,Q["coral"],Q["coral2"])}{mush(44,320,Q["mustard"],Q["mustard2"],.8)}{mush(330,780,Q["pink"],Q["pink2"],.9)}{mush(90,790,Q["coral"],Q["coral2"],.7)}
    {flowers}{sign(120,770,'MEADOW')}
    {butterfly(80,286,Q["pink"],Q["pink2"])}{butterfly(300,346,Q["mustard"],Q["mustard2"])}{butterfly(190,560,Q["cream"],Q["cream2"])}
  </svg>
  <div style="position:absolute;left:0;right:0;top:0;height:56px;background:{Q["purple"]};z-index:4">
    {pill(14,8,98,40,Q["mustard"],Q["mustard2"],'Castle',16)}<div style="position:absolute;left:126px;top:12px;{TT};font-size:24px;color:{Q["cream"]}">Meadow</div><b style="position:absolute;right:16px;top:18px;font:700 15px Fredoka,sans-serif;color:{Q["cream"]}">5/20</b></div>
  {nodes(21)}
  <div style="position:absolute;left:122px;top:430px;z-index:4">{sv('mouse',36)}</div>
</div>'''
boards={'Room-detailed-meadow.dc.html':('46 · Detailed room map: the Meadow',b)}
base='/home/claude/mockups/project'
for fn,(t,body) in boards.items():
    open(f'{base}/{fn}','w').write(HEADQ%t+body+'\n'+TAIL)
c=json.load(open(f'{base}/canvas.json'))
ey=c['boards']['Eyes-options.dc.html']; x=ey['x']+ey['w']+80
for fn,(t,body) in boards.items():
    c['boards'].pop(fn,None); c['order']=[o for o in c['order'] if o!=fn]
    c['boards'][fn]={'x':x,'y':ey['y'],'w':390,'h':844,'title':t}; c['order'].append(fn); x+=470
json.dump(c,open(f'{base}/canvas.json','w'),ensure_ascii=False)
print('ok')
