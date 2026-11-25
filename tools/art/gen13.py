import json, math, random
G={'random':random,'math':math,'json':json}
G["G"]=G
g12=open('./gen12.py').read()
exec(g12[g12.index("g7=open"):g12.index("out={}")], G)
exec("from builtins import *", G)
Q=G['Q']; sv=G['sv']; pill=G['pill']; TT=G['TT']; SC=G['SC']
INK=Q['ink']
# ---------- shared pieces, light from the top-left: every object's right side is its darker tone
def plate(n,x,y,state):
    rim={'done':(Q['mustard'],Q['mustard2']),'cur':(Q['cream'],Q['cream2']),'next':(Q['cream'],Q['cream2']),'lock':('#b9b2a6','#9d968a')}[state]
    ring=f'<circle cx="{x}" cy="{y}" r="27" fill="none" stroke="{Q["mustard"]}" stroke-width="5"/>' if state=='cur' else ''
    tick=f'<circle cx="{x+15}" cy="{y+14}" r="8" fill="{Q["green"]}"/><path d="M{x+11} {y+14} l3 3 l5 -6" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' if state=='done' else ''
    return f'''<g><ellipse cx="{x+2}" cy="{y+20}" rx="20" ry="5" fill="#000" opacity=".18"/><circle cx="{x}" cy="{y}" r="21" fill="{rim[1]}"/><circle cx="{x-1.5}" cy="{y-1.5}" r="19.5" fill="{rim[0]}"/><circle cx="{x-1}" cy="{y-1}" r="13" fill="none" stroke="{rim[1]}" stroke-width="2"/>{ring}
      <text x="{x-1}" y="{y+4.5}" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="14" fill="{INK}">{n}</text>{tick}</g>'''
def shelf(y,x0=18,x1=372,brk=True):
    return f'''<rect x="{x0}" y="{y}" width="{x1-x0}" height="12" fill="#a06a3e"/><rect x="{x0}" y="{y+12}" width="{x1-x0}" height="10" fill="#7d5030"/><rect x="{x0}" y="{y+22}" width="{x1-x0}" height="5" fill="#000" opacity=".12"/>
      {''.join(f'<path d="M{bx} {y+22} L{bx+20} {y+22} L{bx} {y+44} Z" fill="#7d5030"/><path d="M{bx} {y+22} L{bx+6} {y+22} L{bx} {y+30} Z" fill="#6a4228"/>' for bx in ((40,190,336) if brk else ()))}'''
def ladder(x,y_top,y_bot):
    rungs=''.join(f'<rect x="{x+4}" y="{yy}" width="28" height="6" rx="2" fill="#c08a52"/><rect x="{x+18}" y="{yy}" width="14" height="6" rx="2" fill="#a06a3e"/>' for yy in range(int(y_top)+14,int(y_bot)-4,20))
    return f'<rect x="{x}" y="{y_top}" width="6" height="{y_bot-y_top}" rx="3" fill="#c08a52"/><rect x="{x+30}" y="{y_top}" width="6" height="{y_bot-y_top}" rx="3" fill="#a06a3e"/>{rungs}'
def jar(x,y,c,c2,lab=None,h=34,w=24):
    return f'''<g transform="translate({x} {y-h})"><rect x="0" y="6" width="{w}" height="{h-6}" rx="7" fill="{c}"/><rect x="{w*0.58}" y="6" width="{w*0.42}" height="{h-6}" rx="6" fill="{c2}"/><rect x="2" y="0" width="{w-4}" height="8" rx="3" fill="#7d5030"/><rect x="{w*0.58}" y="0" width="{w*0.42-2}" height="8" rx="3" fill="#6a4228"/>
      {f'<rect x="4" y="{h*0.42}" width="{w-8}" height="{h*0.3}" rx="2" fill="{Q["cream"]}"/><rect x="{w*0.58}" y="{h*0.42}" width="{w*0.42-4}" height="{h*0.3}" rx="2" fill="{Q["cream2"]}"/>' if lab else ''}</g>'''
def pot(x,y,w=40,h=30):
    return f'''<g transform="translate({x} {y-h})"><rect x="-6" y="8" width="8" height="5" rx="2" fill="#7a4a2a"/><rect x="{w-2}" y="8" width="8" height="5" rx="2" fill="#6a3e22"/><path d="M0 6 L{w} 6 L{w-3} {h} L3 {h} Z" fill="#c2723a"/><path d="M{w*0.6} 6 L{w} 6 L{w-3} {h} L{w*0.6} {h} Z" fill="#a25a2a"/><rect x="-2" y="2" width="{w+4}" height="6" rx="3" fill="#d88a4a"/><rect x="{w*0.6}" y="2" width="{w*0.4+2}" height="6" rx="3" fill="#b86a34"/></g>'''
def bread(x,y):
    return f'''<g transform="translate({x} {y-20})"><path d="M0 20 C0 4 46 0 52 14 L52 20 Z" fill="#d9a35a"/><path d="M30 6 C44 6 52 10 52 14 L52 20 L30 20 Z" fill="#b8843e"/><path d="M14 8 l4 7 M24 5 l4 7 M34 5 l4 7" stroke="#b8843e" stroke-width="3" stroke-linecap="round"/></g>'''
def cheese(x,y):
    return f'''<g transform="translate({x} {y-24})"><path d="M0 24 L0 8 C0 2 44 2 44 8 L44 24 Z" fill="{Q["mustard"]}"/><path d="M30 3 C40 4 44 6 44 8 L44 24 L30 24 Z" fill="{Q["mustard2"]}"/><rect x="0" y="2" width="44" height="8" rx="4" fill="#ecc26a"/><path d="M44 24 L62 24 L62 12 Z" fill="{Q["mustard"]}"/><path d="M54 24 L62 24 L62 12 Z" fill="{Q["mustard2"]}"/></g>'''
def bottle(x,y,c,c2):
    return f'<g transform="translate({x} {y-40})"><rect x="6" y="0" width="8" height="12" rx="2" fill="{c2}"/><rect x="5" y="0" width="10" height="4" rx="1" fill="#7d5030"/><rect x="0" y="10" width="20" height="30" rx="6" fill="{c}"/><rect x="12" y="10" width="8" height="30" rx="4" fill="{c2}"/></g>'
def teapot(x,y):
    return f'''<g transform="translate({x} {y-28})"><path d="M-10 12 L2 14 L2 20 L-6 18 Z" fill="{Q["navy"]}"/><path d="M34 10 C44 10 44 24 34 24" fill="none" stroke="{Q["navy2"]}" stroke-width="4"/><rect x="0" y="6" width="36" height="22" rx="10" fill="{Q["navy"]}"/><rect x="20" y="6" width="16" height="22" rx="8" fill="{Q["navy2"]}"/><rect x="12" y="0" width="12" height="8" rx="4" fill="{Q["navy2"]}"/><rect x="6" y="14" width="18" height="4" rx="2" fill="{Q["cream"]}"/></g>'''
def ladle(x,y,l=40):
    return f'<g transform="translate({x} {y})"><rect x="-2" y="0" width="4" height="{l}" rx="2" fill="#8a8794"/><path d="M-10 {l} Q0 {l+16} 10 {l} Z" fill="#8a8794"/><path d="M0 {l} L10 {l} Q6 {l+10} 0 {l+12} Z" fill="#6e6b78"/></g>'
def pan(x,y):
    return f'<g transform="translate({x} {y})"><rect x="-2" y="0" width="4" height="26" rx="2" fill="#3a3644"/><rect x="-16" y="26" width="32" height="26" rx="13" fill="#4a4652"/><rect x="0" y="26" width="16" height="26" rx="8" fill="#35323c"/></g>'
def herbs(x,y):
    return f'<g transform="translate({x} {y})">' + ''.join(f'<rect x="{k*14+6}" y="0" width="2" height="10" fill="#7d5030"/><path d="M{k*14} 10 L{k*14+14} 10 L{k*14+7} 34 Z" fill="{c}"/><path d="M{k*14+7} 10 L{k*14+14} 10 L{k*14+7} 34 Z" fill="{c2}"/>' for k,(c,c2) in enumerate([(Q["green"],Q["green2"]),(Q["olive"],Q["olive2"]),(Q["green"],Q["green2"])])) + '</g>'
def onions(x,y):
    return f'<g transform="translate({x} {y})"><path d="M10 0 L10 46" stroke="#c9a46a" stroke-width="3"/>' + ''.join(f'<path d="M{10+dx} {8+k*12} C{dx-2} {14+k*12} {dx+2} {24+k*12} {10+dx} {24+k*12} C{18+dx} {24+k*12} {22+dx} {14+k*12} {10+dx} {8+k*12} Z" fill="#c9783a"/><path d="M{10+dx} {8+k*12} C{18+dx} {14+k*12} {20+dx} {22+k*12} {10+dx} {24+k*12} Z" fill="#a65e2a"/>' for k,dx in enumerate([-7,7,-7])) + '</g>'
# ---------- CONCEPT 1: side-view kitchen, the path runs along shelves and climbs ladders
W=390
def concept_shelves():
    rows=[714,588,462,336]
    xs=[92,166,240,314]
    gaps=[(xs[i]+xs[i+1])//2 for i in range(3)]   # object slots between plates
    out=[]
    out.append(f'<rect x="0" y="0" width="{W}" height="844" fill="#e6d3b0"/>')
    out.append(''.join(f'<rect x="{(i%2)*26-20+k*52}" y="{y}" width="48" height="24" rx="3" fill="#dcc6a0"/>' for i,y in enumerate(range(62,820,28)) for k in range(9)))
    # top: hearth + door + window
    out.append(f'''<rect x="22" y="76" width="126" height="176" rx="6" fill="{Q["lav"]}"/><rect x="112" y="76" width="36" height="176" rx="6" fill="{Q["lav2"]}"/>
      <rect x="10" y="66" width="150" height="20" rx="4" fill="#857e72"/><rect x="10" y="80" width="150" height="6" fill="#6e675d"/>
      <path d="M40 252 L40 168 C40 140 130 140 130 168 L130 252 Z" fill="#2e1c14"/><path d="M58 252 C54 230 70 218 78 206 C80 222 98 226 92 252 Z" fill="{Q["mustard"]}"/><path d="M72 252 C70 238 78 230 80 222 C86 232 90 240 86 252 Z" fill="{Q["coral"]}"/>
      <rect x="83" y="152" width="4" height="24" fill="#3a3644"/><path d="M60 180 L110 180 L104 214 L66 214 Z" fill="#4a4652"/><path d="M90 180 L110 180 L104 214 L90 214 Z" fill="#35323c"/><rect x="56" y="176" width="58" height="8" rx="4" fill="#5a5664"/>
      <ellipse cx="78" cy="166" rx="9" ry="6" fill="#fff" opacity=".7"/><ellipse cx="92" cy="152" rx="7" ry="5" fill="#fff" opacity=".5"/>''')
    out.append(f'''<path d="M188 252 L188 178 C188 146 246 146 246 178 L246 252 Z" fill="{Q["brown"]}"/><path d="M217 148 C234 150 246 160 246 178 L246 252 L217 252 Z" fill="{Q["brown2"]}"/><rect x="188" y="196" width="58" height="5" fill="{Q["brown2"]}"/><rect x="188" y="226" width="58" height="5" fill="{Q["brown2"]}"/><circle cx="234" cy="214" r="4" fill="{Q["mustard"]}"/>
      <rect x="182" y="140" width="70" height="10" rx="4" fill="#857e72"/>''')
    out.append(f'''<g transform="translate(286 96)"><rect x="-6" y="-6" width="74" height="104" rx="36" fill="#857e72"/><rect x="0" y="0" width="62" height="92" rx="31" fill="#9cb8c8"/><path d="M31 0 A31 31 0 0 1 62 31 L62 92 L44 92 L44 12 Z" fill="#86a5b8"/><rect x="29" y="0" width="4" height="92" fill="#857e72"/><rect x="0" y="44" width="62" height="4" fill="#857e72"/><rect x="-10" y="88" width="82" height="10" rx="4" fill="{Q["brown"]}"/></g>''')
    out.append(f'<rect x="0" y="252" width="{W}" height="10" fill="#857e72"/><rect x="0" y="258" width="{W}" height="4" fill="#6e675d"/>')
    # dresser uprights frame the shelves
    out.append(f'<rect x="56" y="272" width="10" height="548" fill="#8a5a34"/><rect x="340" y="272" width="10" height="548" fill="#7d5030"/>')
    for r in rows: out.append(shelf(r,56,350,False))
    # cornice on top of the dresser
    out.append(f'<rect x="46" y="272" width="314" height="12" rx="2" fill="#a06a3e"/><rect x="46" y="282" width="314" height="6" fill="#7d5030"/>')
    # cupboard base under the bottom shelf
    out.append(f'<rect x="66" y="741" width="274" height="79" fill="#a06a3e"/><rect x="66" y="741" width="274" height="6" fill="#000" opacity=".12"/>'
      + ''.join(f'<rect x="{dx}" y="752" width="124" height="58" rx="4" fill="#b5784a"/><rect x="{dx+70}" y="752" width="54" height="58" rx="4" fill="#9a6440"/><circle cx="{dx+(112 if j==0 else 12)}" cy="781" r="4" fill="{Q["mustard"]}"/>' for j,dx in enumerate((76,206))))
    # ladders outside the uprights, alternate sides
    out.append(ladder(352,rows[1]+4,rows[0]+20))
    out.append(ladder(18,rows[2]+4,rows[1]+12))
    out.append(ladder(352,rows[3]+4,rows[2]+12))
        # ledges the ladders land on
    for r,side in zip(rows,['L','R','L','R']):
        pass
    # objects only in the gaps between plates, narrow and low
    g=gaps
    out.append(jar(g[0]-11,rows[0],Q["coral"],Q["coral2"],1,30,22)+bottle(g[1]-10,rows[0],Q["green"],Q["green2"])+jar(g[2]-10,rows[0],Q["cream"],Q["cream2"],1,26,20))
    out.append(jar(g[0]-12,rows[1],Q["mustard"],Q["mustard2"],1,34,24)+bottle(g[1]-10,rows[1],Q["navy"],Q["navy2"])+jar(g[2]-11,rows[1],Q["olive"],Q["olive2"],1,30,22))
    out.append(bottle(g[0]-10,rows[2],Q["coral"],Q["coral2"])+jar(g[1]-11,rows[2],Q["pink"],Q["pink2"],1,28,22)+jar(g[2]-12,rows[2],Q["cream"],Q["cream2"],1,34,24))
    out.append(jar(g[0]-11,rows[3],Q["olive"],Q["olive2"],1,30,22)+jar(g[1]-12,rows[3],Q["mustard"],Q["mustard2"],1,34,24)+bottle(g[2]-10,rows[3],Q["green"],Q["green2"]))
    # bigger pieces sit at the ends of shelves, by the uprights' inner side? no: on the top of the dresser
    # hanging things: hooks under each shelf, aligned with gaps so they never sit over a plate
    hang=[            [herbs(g[0]-21,rows[1]+27),pan(g[1],rows[1]+27),onions(g[2]-10,rows[1]+27)],
           [pan(g[0],rows[2]+27),onions(g[1]-10,rows[2]+27),ladle(g[2],rows[2]+27,26)],
           [onions(g[0]-10,rows[3]+27),ladle(g[1],rows[3]+27,26),herbs(g[2]-21,rows[3]+27)] ]
    for h in hang: out.append(''.join(h))
    # floor
    out.append(f'<rect x="0" y="820" width="{W}" height="30" fill="#a35a33"/>'+''.join(f'<rect x="{k*56}" y="820" width="52" height="60" fill="#b5653a"/>' for k in range(0,8,2)))
    n=171; states=['done']*6+['cur','next']+['lock']*12
    plates=''; k=0; cur=None
    for i,r in enumerate(rows):
        order=xs if i%2==0 else xs[::-1]
        for x in order:
            if states[k]=='cur': cur=(x,r-20)
            plates+=plate(n+k,x,r-20,states[k]); k+=1
    svg=f'<svg width="{W}" height="844" style="position:absolute;left:0;top:0">{"".join(out)}{plates}</svg>'
    return svg+f'<div style="position:absolute;left:{cur[0]-18}px;top:{cur[1]-58}px">{sv("mouse",36)}</div>'
def page(title,inner,bg):
    return f'''<div style="{SC}background:{bg}">{inner}
  <div style="position:absolute;left:0;right:0;top:0;height:56px;background:{Q["purple"]};z-index:4">
    {pill(14,8,98,40,Q["mustard"],Q["mustard2"],'Castle',16)}<div style="position:absolute;left:126px;top:12px;{TT};font-size:24px;color:{Q["cream"]}">{title}</div><b style="position:absolute;right:16px;top:18px;font:700 15px Fredoka,sans-serif;color:{Q["cream"]}">6/30</b></div></div>'''
boards={'Kitchen-concept-shelves.dc.html':('K1 · Kitchens concept: shelves and ladders (side view)',page('Kitchens',concept_shelves(),'#e6d3b0'))}
base='/home/claude/mockups/project'
c=json.load(open(f'{base}/canvas.json'))
fs=c['boards']['Final-sheet.dc.html']; x=fs['x']+fs['w']+120
for fn,(t,body) in boards.items():
    open(f'{base}/{fn}','w').write(G['HEADQ']%t+body+'\n'+G['TAIL'])
    c['boards'].pop(fn,None); c['order']=[o for o in c['order'] if o!=fn]
    c['boards'][fn]={'x':x,'y':fs['y'],'w':390,'h':844,'title':t}; c['order'].append(fn); x+=470
json.dump(c,open(f'{base}/canvas.json','w'),ensure_ascii=False)
print('ok')
