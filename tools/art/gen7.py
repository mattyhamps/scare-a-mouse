import json, math
src=open('./gen6.py').read()
exec(src[:src.index("# ---- 38 floor plan")])
def two(x,y,w,h,c,c2,r=10,side='r',k=.28):
    if side=='r': sh=f'<rect x="{x+w*(1-k)}" y="{y}" width="{w*k}" height="{h}" rx="{r}" fill="{c2}"/><rect x="{x+w*(1-k)}" y="{y}" width="{min(r,w*k)}" height="{h}" fill="{c2}"/>'
    else: sh=f'<rect x="{x}" y="{y+h*(1-k)}" width="{w}" height="{h*k}" rx="{r}" fill="{c2}"/>'
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{c}"/>{sh}'
# ---------- lions
L1=f'''{''.join(f'<ellipse cx="{50+30*math.cos(a):.1f}" cy="{50+30*math.sin(a):.1f}" rx="14" ry="12" transform="rotate({math.degrees(a)+90:.0f} {50+30*math.cos(a):.1f} {50+30*math.sin(a):.1f})" fill="{Q["orange2"] if math.cos(a)>0.2 else Q["orange"]}"/>' for a in [math.pi*(1.0+0.2*i) for i in range(6)])}
  <circle cx="30" cy="28" r="8" fill="{Q["mustard"]}"/><circle cx="70" cy="28" r="8" fill="{Q["mustard2"]}"/><circle cx="30" cy="28" r="4" fill="{Q["pink"]}"/><circle cx="70" cy="28" r="4" fill="{Q["pink2"]}"/>
  <circle cx="50" cy="56" r="28" fill="{Q["mustard"]}"/><path d="M78 56 A28 28 0 0 1 50 84 A28 28 0 0 0 72 56 Z" fill="{Q["mustard2"]}"/><path d="M38 64 Q50 56 62 64 Q62 78 50 80 Q38 78 38 64 Z" fill="{Q["cream"]}"/>{eyes2(40,60,52)}{blush(32,68,63)}<path d="M45 61 L55 61 L50 66 Z" fill="{Q["coral"]}"/><path d="M44 26 L47 32 L50 24 L53 32 L56 26 L56 34 L44 34 Z" fill="{Q["orange"]}"/>'''
L2=f'''<path d="M50 10 C78 10 94 30 92 54 C90 76 74 92 50 92 C26 92 10 76 8 54 C6 30 22 10 50 10 Z" fill="{Q["orange"]}"/><path d="M50 10 C78 10 94 30 92 54 C90 76 74 92 50 92 C66 84 80 72 80 52 C80 30 68 16 50 10 Z" fill="{Q["orange2"]}"/>
  <path d="M14 40 L6 46 L14 50 M86 40 L94 46 L86 50 M22 76 L14 84 L26 82 M78 76 L86 84 L74 82" fill="{Q["orange"]}"/>
  <circle cx="30" cy="30" r="7" fill="{Q["mustard"]}"/><circle cx="70" cy="30" r="7" fill="{Q["mustard2"]}"/>
  <circle cx="50" cy="55" r="27" fill="{Q["mustard"]}"/><path d="M77 55 A27 27 0 0 1 50 82 A27 27 0 0 0 71 55 Z" fill="{Q["mustard2"]}"/><path d="M38 63 Q50 55 62 63 Q62 77 50 79 Q38 77 38 63 Z" fill="{Q["cream"]}"/>{eyes2(40,60,51)}{blush(32,68,62)}<path d="M45 60 L55 60 L50 65 Z" fill="{Q["coral"]}"/>'''
L3=f'''<circle cx="26" cy="30" r="12" fill="{Q["mustard"]}"/><circle cx="74" cy="30" r="12" fill="{Q["mustard2"]}"/><circle cx="26" cy="31" r="6" fill="{Q["pink"]}"/><circle cx="74" cy="31" r="6" fill="{Q["pink2"]}"/>
  <ellipse cx="50" cy="58" rx="32" ry="29" fill="{Q["mustard"]}"/><path d="M82 58 A32 29 0 0 1 50 87 A32 29 0 0 0 75 58 Z" fill="{Q["mustard2"]}"/>
  <path d="M38 34 C40 22 48 26 50 20 C52 26 60 22 62 34 C56 30 44 30 38 34 Z" fill="{Q["orange"]}"/><path d="M18 58 L8 54 L14 62 L8 66 L20 66 Z M82 58 L92 54 L86 62 L92 66 L80 66 Z" fill="{Q["orange"]}"/>
  <path d="M36 66 Q50 58 64 66 Q64 82 50 84 Q36 82 36 66 Z" fill="{Q["cream"]}"/>{eyes2(39,61,54)}{blush(30,70,65)}<path d="M45 63 L55 63 L50 68 Z" fill="{Q["coral"]}"/><path d="M50 68 L50 72 M45 73 Q50 76 55 73" stroke="{Q["ink"]}" stroke-width="2" fill="none" stroke-linecap="round"/>'''
lsv=lambda inner,s: f'<svg viewBox="0 0 100 100" width="{s}" height="{s}" style="overflow:visible">{inner}</svg>'
def lrow(top,label,sub,inner):
    others=''.join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:4px">{sv(k,70)}<span style="font:600 12px Fredoka;color:{Q["cream2"]}">{k}</span></div>' for k in ['mouse','cat','dog','bear'])
    return f'''<div style="position:absolute;left:24px;top:{top}px;{TT};font-size:22px;color:{Q["cream"]}">{label} <span style="font:600 14px Fredoka;color:{Q["cream2"]}">{sub}</span></div>
      <div style="position:absolute;left:24px;top:{top+36}px;width:250px;height:190px;border-radius:22px;background:{Q["lav2"]};display:grid;place-items:center">{lsv(inner,150)}</div>
      <div style="position:absolute;left:290px;top:{top+36}px;width:466px;height:190px;border-radius:22px;background:{Q["lav2"]};display:flex;align-items:center;justify-content:space-around">{others}<div style="display:flex;flex-direction:column;align-items:center;gap:4px">{lsv(inner,70)}<span style="font:600 12px Fredoka;color:{Q["mustard"]}">lion</span></div></div>'''
b=f'''<div style="width:780px;height:844px;position:relative;overflow:hidden;background:{Q["purple"]};font-family:Fredoka,sans-serif">{deco(780,844,13,20)}
  <div style="position:absolute;left:24px;top:14px;{TT};font-size:28px;color:{Q["cream"]}">The lion, without the sunflower mane</div>
  {lrow(60,'A · Mane tufts','a crown of tufts on top, face and ears showing',L1)}
  {lrow(320,'B · Mane hood','one smooth mane shape, a bit bigger than the head',L2)}
  {lrow(580,'C · Young lion','no mane: a tuft on top and cheek fluff',L3)}
</div>'''
boards={'Lion-options.dc.html':('42 · Lion options (no full mane)',b,780)}
# ---------- detailed castle cutaway
def stonewall(x,y,w,h):
    out=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{Q["lav"]}"/>'
    for r in range(int(h//16)):
        off=0 if r%2 else 14
        for cx in range(int(x)-off, int(x+w), 28):
            if cx+26> x and cx < x+w:
                xx=max(cx,x); ww=min(cx+26,x+w)-xx
                out+=f'<rect x="{xx}" y="{y+r*16+2}" width="{ww}" height="12" rx="3" fill="{Q["lav2"] if (r+cx//28)%3==0 else "#978f83"}" opacity=".55"/>'
    return out
def floor_room(y,h,wall,wall2,floorc,content,label,sub,state):
    x0,x1=58,332
    body=f'<rect x="{x0}" y="{y}" width="{x1-x0}" height="{h}" fill="{wall}"/><rect x="{x0}" y="{y+h-14}" width="{x1-x0}" height="14" fill="{floorc}"/><rect x="{x0}" y="{y}" width="{x1-x0}" height="8" fill="{wall2}"/>'
    if state=='lock':
        planks=''.join(f'<g transform="rotate({ang} {(x0+x1)/2} {y+py})"><rect x="{x0-6}" y="{y+py-9}" width="{x1-x0+12}" height="18" rx="4" fill="{Q["brown"]}"/><rect x="{x0-6}" y="{y+py+2}" width="{x1-x0+12}" height="7" rx="3" fill="{Q["brown2"]}"/><rect x="{x0+8}" y="{y+py-3}" width="4" height="4" fill="{Q["ink"]}" opacity=".6"/><rect x="{x1-12}" y="{y+py-3}" width="4" height="4" fill="{Q["ink"]}" opacity=".6"/></g>' for py,ang in [(h*0.28,-2.5),(h*0.72,2)])
        body=f'<clipPath id="lk{y}"><rect x="{x0}" y="{y}" width="{x1-x0}" height="{h}"/></clipPath><g clip-path="url(#lk{y})"><rect x="{x0}" y="{y}" width="{x1-x0}" height="{h}" fill="#2e2830"/>'+planks+'</g>'+f'<g transform="translate({(x0+x1)/2-14} {y+h/2-16})"><path d="M8 14 L8 9 C8 1 20 1 20 9 L20 14" fill="none" stroke="{Q["lav"]}" stroke-width="4"/><rect x="2" y="13" width="24" height="18" rx="5" fill="{Q["mustard"]}"/><rect x="14" y="13" width="12" height="18" rx="5" fill="{Q["mustard2"]}"/></g>'
        return body
    plaque=f'<g transform="translate({x0+8} {y+10})"><rect width="{len(label)*9+(len(sub)*7 if sub else 0)+26}" height="24" rx="8" fill="{Q["cream"]}"/><text x="10" y="17" font-family="Fredoka" font-weight="700" font-size="14" fill="{Q["ink"]}">{label}<tspan fill="{Q["brown"]}" font-weight="600"> {sub}</tspan></text></g>'
    ring=f'<rect x="{x0-3}" y="{y-3}" width="{x1-x0+6}" height="{h+6}" fill="none" stroke="{Q["mustard"]}" stroke-width="5" rx="4"/>' if state=='here' else ''
    return body+content+plaque+ring
def shelf(x,y): return two(x,y,36,46,Q["brown"],Q["brown2"],4)+''.join(f'<rect x="{x+4+i*6}" y="{y+6}" width="5" height="14" fill="{c}"/>' for i,c in enumerate([Q["coral"],Q["navy"],Q["olive"],Q["mustard"],Q["coral"]]))+''.join(f'<rect x="{x+4+i*6}" y="{y+26}" width="5" height="14" fill="{c}"/>' for i,c in enumerate([Q["olive"],Q["mustard"],Q["navy"],Q["coral"],Q["cream"]]))
def win(x,y,night=True): return f'<rect x="{x}" y="{y}" width="20" height="30" rx="10" fill="{"#2a3a5a" if night else "#9cb8c8"}"/><rect x="{x+9}" y="{y}" width="2" height="30" fill="{Q["lav2"]}"/>'
def barrel(x,y): return two(x,y,20,26,Q["orange"],Q["orange2"],8)+f'<rect x="{x}" y="{y+8}" width="20" height="3" fill="{Q["orange2"]}"/><rect x="{x}" y="{y+16}" width="20" height="3" fill="{Q["orange2"]}"/>'
def table(x,y,w): return two(x,y,w,10,Q["brown"],Q["brown2"],4)+f'<rect x="{x+4}" y="{y+10}" width="5" height="14" fill="{Q["brown2"]}"/><rect x="{x+w-9}" y="{y+10}" width="5" height="14" fill="{Q["brown2"]}"/>'
def torch(x,y): return f'<rect x="{x}" y="{y+10}" width="4" height="10" fill="{Q["brown2"]}"/><path d="M{x+2} {y} C{x-3} {y+6} {x-1} {y+11} {x+2} {y+11} C{x+5} {y+11} {x+7} {y+6} {x+2} {y} Z" fill="{Q["mustard"]}"/>'
floors=[]
Y={'cell':560,'f1':470,'f2':380,'l3':302,'l4':224,'l5':146}
FH=86
cellar=floor_room(Y["cell"],FH,'#4a3a36','#3a2c28','#5a4038',barrel(80,Y['cell']+46)+barrel(102,Y['cell']+46)+barrel(91,Y['cell']+22)+two(250,Y['cell']+40,44,32,Q["lav"],Q["lav2"],8)+f'<path d="M262 {Y["cell"]+72} L262 {Y["cell"]+52} C262 {Y["cell"]+44} 282 {Y["cell"]+44} 282 {Y["cell"]+52} L282 {Y["cell"]+72} Z" fill="#2a1a14"/>'+torch(190,Y['cell']+30)+torch(316,Y['cell']+30),'Cellars','✓','open')
f1=floor_room(Y["f1"],FH,'#7a3a3a','#652e2e','#8a5a32',shelf(74,Y['f1']+26)+shelf(114,Y['f1']+26)+table(170,Y['f1']+50,70)+f'<circle cx="190" cy="{Y["f1"]+46}" r="5" fill="{Q["mustard"]}"/><circle cx="214" cy="{Y["f1"]+46}" r="5" fill="{Q["coral"]}"/>'+win(262,Y['f1']+30,False)+win(296,Y['f1']+30,False),'First floor','✓','open')
f2=floor_room(Y["f2"],FH,'#3a4a7a','#2f3d66','#8a5a32',f'<circle cx="110" cy="{Y["f2"]+48}" r="18" fill="{Q["coral"]}"/><circle cx="110" cy="{Y["f2"]+48}" r="10" fill="{Q["mustard"]}"/><path d="M110 {Y["f2"]+30} L110 {Y["f2"]+66} M92 {Y["f2"]+48} L128 {Y["f2"]+48}" stroke="{Q["navy2"]}" stroke-width="3"/>'+table(160,Y['f2']+54,40)+table(214,Y['f2']+54,40)+f'<rect x="270" y="{Y["f2"]+28}" width="44" height="30" rx="3" fill="{Q["cream"]}"/><ellipse cx="284" cy="{Y["f2"]+42}" rx="8" ry="5" fill="{Q["olive"]}"/><ellipse cx="302" cy="{Y["f2"]+46}" rx="6" ry="4" fill="{Q["olive"]}"/>','Second floor','0/150','here')
locks=''.join(floor_room(Y[k],70,'','','','','','','lock') for k in ('l3','l4','l5'))
castle=f'''<svg width="390" height="844" style="position:absolute;left:0;top:0">
  <circle cx="300" cy="62" r="22" fill="{Q["cream"]}"/><circle cx="310" cy="55" r="20" fill="#1e2a44"/>
  {''.join(spark(x,y,s,c) for x,y,s,c in [(140,40,7,Q["mustard"]),(200,90,5,Q["cream"]),(30,150,6,Q["pink"]),(360,170,6,Q["cream"]),(110,110,4,Q["mustard"])])}
  <!-- side towers -->
  {stonewall(18,180,40,476)}<rect x="46" y="180" width="12" height="476" fill="#978f83" opacity=".6"/><path d="M10 182 L38 120 L66 182 Z" fill="{Q["coral"]}"/><path d="M38 120 L66 182 L50 182 Z" fill="{Q["coral2"]}"/><path d="M38 120 L38 98 L56 104 L38 110" fill="{Q["mustard"]}"/>
  {stonewall(332,180,40,476)}<rect x="360" y="180" width="12" height="476" fill="#978f83" opacity=".6"/><path d="M324 182 L352 120 L380 182 Z" fill="{Q["coral"]}"/><path d="M352 120 L380 182 L364 182 Z" fill="{Q["coral2"]}"/><path d="M352 120 L352 98 L370 104 L352 110" fill="{Q["mustard"]}"/>
  {''.join(win(28,y) for y in (230,330,430,530))}{''.join(win(342,y) for y in (230,330,430,530))}
  <!-- keep frame -->
  {stonewall(50,136,290,520)}
  {''.join(f'<rect x="{50+k*36}" y="120" width="22" height="20" rx="3" fill="{Q["lav"]}"/>' for k in range(9))}
  <!-- central tower top -->
  {stonewall(160,40,70,96)}<path d="M150 44 L195 -6 L240 44 Z" fill="{Q["coral"]}"/><path d="M195 -6 L240 44 L216 44 Z" fill="{Q["coral2"]}"/><rect x="183" y="62" width="24" height="36" rx="12" fill="#3a3340"/><g transform="translate(184 70)"><path d="M6 10 L6 6 C6 0 16 0 16 6 L16 10" fill="none" stroke="{Q["lav2"]}" stroke-width="3"/><rect x="2" y="9" width="18" height="13" rx="4" fill="{Q["mustard"]}"/></g>
  {locks}{f2}{f1}{cellar}
  <!-- moat, gate, outside -->
  <rect x="0" y="656" width="390" height="30" fill="{Q["navy"]}"/><path d="M0 664 q20 -6 40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0" stroke="#4a6aa8" stroke-width="3" fill="none"/>
  <path d="M166 656 L166 612 C166 594 224 594 224 612 L224 656 Z" fill="#2a1a14"/>
  <rect x="164" y="652" width="62" height="40" fill="{Q["brown"]}"/>{''.join(f'<rect x="{164+k*10}" y="652" width="2" height="40" fill="{Q["brown2"]}"/>' for k in range(7))}
  <rect x="0" y="686" width="390" height="160" fill="{Q["olive"]}"/>
  <path d="M195 692 C180 730 220 760 190 844 L230 844 C250 770 214 730 225 692 Z" fill="{Q["cream"]}"/>
  {''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{Q["green"]}"/><circle cx="{x+r*.35}" cy="{y+r*.25}" r="{r*.6}" fill="{Q["green2"]}"/><rect x="{x-3}" y="{y+r-4}" width="6" height="12" fill="{Q["brown2"]}"/>' for x,y,r in [(40,730,22),(90,780,16),(330,740,24),(290,800,14),(360,810,12)])}
  {''.join(f'<circle cx="{x}" cy="{y}" r="4" fill="{c}"/>' for x,y,c in [(120,720,Q["pink"]),(140,760,Q["mustard"]),(260,720,Q["cream"]),(270,770,Q["pink"]),(60,810,Q["mustard"])])}
</svg>'''
plaque_out=f'<div style="position:absolute;left:104px;top:740px;padding:4px 12px;border-radius:10px;background:{Q["cream"]};font:700 14px Fredoka">Outside <span style="color:{Q["brown"]}">✓</span></div>'
b=f'''<div style="{SC}background:#1e2a44">{castle}{plaque_out}
  <div style="position:absolute;left:96px;top:14px;{TT};font-size:28px;color:{Q["cream"]}"></div>
  <div style="position:absolute;left:14px;top:20px;{TT};font-size:26px;line-height:1.05;color:{Q["cream"]}">The<br>castle</div>
  <div style="position:absolute;left:286px;top:{Y["f2"]+36}px">{sv('mouse',36)}</div>
</div>'''
boards['Castle-detailed.dc.html']=('43 · Detailed castle: a cutaway with each floor drawn',b,390)
# ---------- detailed floor plan (First floor, from above)
def fp_room(x,y,w,h,floor_svg,name,sub,state):
    lab=f'<g transform="translate({x+w/2} {y+h-16})"><rect x="{-(len(name)*4.6+len(sub)*3.6+16)}" y="-12" width="{len(name)*9.2+len(sub)*7.2+32}" height="24" rx="8" fill="{Q["cream"]}"/><text x="0" y="5" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="14" fill="{Q["ink"]}">{name}<tspan fill="{Q["brown"]}" font-weight="600"> {sub}</tspan></text></g>'
    if state=='fog':
        cid=f'fogc{x}{y}'
        return f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath><g clip-path="url(#{cid})"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#7d776e"/>'+''.join(f'<circle cx="{x+20+k*(w-40)/3}" cy="{y+h/2+((k%2)*16-8)}" r="{min(w,h)/3.2:.0f}" fill="{Q["cream2"]}" opacity=".85"/>' for k in range(4))+f'</g><text x="{x+w/2}" y="{y+h/2+10}" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="30" fill="{Q["brown"]}">?</text>'
    ring=f'<rect x="{x+3}" y="{y+3}" width="{w-6}" height="{h-6}" fill="none" stroke="{Q["mustard"]}" stroke-width="5" rx="4"/>' if state=='here' else ''
    return floor_svg+ring+lab
def planks(x,y,w,h,c,c2): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"/>'+''.join(f'<rect x="{x+k*18}" y="{y}" width="2" height="{h}" fill="{c2}"/>' for k in range(int(w//18)+1) if x+k*18<x+w)
lib=planks(30,470,150,220,'#9a6a40','#875a34')+''.join(two(36,476+k*0,34,0.1,'#000','#000') for k in [])+''.join(two(36+k*38,476,34,22,Q["brown"],Q["brown2"],3)+''.join(f'<rect x="{38+k*38+i*6}" y="479" width="5" height="16" fill="{c}"/>' for i,c in enumerate([Q["coral"],Q["navy"],Q["olive"],Q["mustard"],Q["cream"]])) for k in range(4))+f'<ellipse cx="105" cy="590" rx="52" ry="34" fill="{Q["navy"]}"/><ellipse cx="105" cy="590" rx="40" ry="24" fill="{Q["navy2"]}"/><circle cx="105" cy="584" r="18" fill="{Q["brown"]}"/><rect x="96" y="578" width="16" height="11" rx="2" fill="{Q["cream"]}"/>'+two(150,520,22,80,Q["brown"],Q["brown2"],3)
study=planks(30,160,150,290,'#a8784a','#946a40')+f'<ellipse cx="105" cy="300" rx="58" ry="44" fill="{Q["coral"]}"/><ellipse cx="105" cy="300" rx="46" ry="32" fill="{Q["coral2"]}"/>'+two(66,200,80,40,Q["brown"],Q["brown2"],5)+f'<rect x="76" y="206" width="22" height="16" rx="2" fill="{Q["cream"]}"/><circle cx="128" cy="214" r="7" fill="{Q["slate"]}"/><circle cx="128" cy="214" r="3" fill="{Q["olive"]}"/>'+two(36,170,20,90,Q["brown"],Q["brown2"],3)+f'<circle cx="150" cy="390" r="14" fill="{Q["navy"]}"/><path d="M142 386 Q150 380 158 388" stroke="{Q["olive"]}" stroke-width="5" fill="none"/>'
walls=f'''<rect x="18" y="148" width="354" height="554" rx="10" fill="{Q["lav2"]}"/>
  <rect x="30" y="160" width="330" height="530" fill="#6a645c"/>'''
inner=f'''<rect x="180" y="160" width="14" height="530" fill="{Q["lav2"]}"/><rect x="30" y="450" width="150" height="20" fill="{Q["lav2"]}"/><rect x="194" y="346" width="166" height="14" fill="{Q["lav2"]}"/><rect x="194" y="490" width="166" height="14" fill="{Q["lav2"]}"/>
  <rect x="90" y="450" width="30" height="20" fill="#9a6a40"/><rect x="180" y="268" width="14" height="30" fill="#a8784a"/>'''
fp=f'''<svg width="390" height="844" style="position:absolute;left:0;top:0">{walls}
  {fp_room(30,470,150,220,lib,'Library','✓ 30/30','done')}
  {fp_room(30,160,150,290,study,'Study','4/30','here')}
  {fp_room(194,160,166,186,'','','','fog')}{fp_room(194,360,166,130,'','','','fog')}{fp_room(194,504,166,186,'','','','fog')}
  {inner}
  <rect x="80" y="690" width="50" height="14" fill="{Q["cream2"]}"/><path d="M96 704 L105 716 L114 704 Z" fill="{Q["cream"]}"/>
</svg>'''
b=f'''<div style="{SC}background:{Q["purple"]}">{deco(390,844,5,10)}
  {pill(16,20,358,52,Q["mustard"],Q["mustard2"],'Castle',20)}
  <div style="position:absolute;left:0;right:0;top:94px;text-align:center;{TT};font-size:30px;color:{Q["cream"]}">First floor</div>
  {fp}
  <div style="position:absolute;left:128px;top:166px">{sv('mouse',36)}</div>
  {pill(16,738,164,50,Q["cream"],Q["cream2"],'Cellars',18)}{pill(210,738,164,50,Q["lav"],Q["lav2"],lock(22)+' Upstairs',18,Q["cream"])}
</div>'''
boards['Floor-detailed.dc.html']=('44 · Detailed floor plan: rooms drawn from above',b,390)
base='/home/claude/mockups/project'
for fn,(t,body,w) in boards.items():
    open(f'{base}/{fn}','w').write(HEADQ%t+body+'\n'+TAIL.replace('{"width":390,"height":844}','{"width":%d,"height":844}'%w))
c=json.load(open(f'{base}/canvas.json'))
for fn in boards: c['boards'].pop(fn,None); c['order']=[o for o in c['order'] if o!=fn]
y=max(v['y'] for v in c['boards'].values())+844+400; x=0
for fn,(t,body,w) in boards.items():
    c['boards'][fn]={'x':x,'y':y,'w':w,'h':844,'title':t}; c['order'].append(fn); x+=w+80
c['notes']['t9']={'x':0,'y':y-260,'text':'Lion options and more detailed maps','kind':'title1','maxW':2000}
json.dump(c,open(f'{base}/canvas.json','w'),ensure_ascii=False)
print('ok')
