import json, math
src=open('./gen.py').read()
exec(src[:src.index("SCREEN=")])
Q=dict(purple='#9b7bbf',lav='#b49ad0',lav2='#8a69b0',mustard='#f0b43c',mustard2='#d9952a',orange='#e8913a',orange2='#cf7428',coral='#e8553e',coral2='#c9432f',pink='#f29a9a',pink2='#de8282',cream='#f6ead2',cream2='#e8d6b4',olive='#b8c24a',olive2='#9aa53a',green='#2f8a6a',green2='#24705a',navy='#3a3f9e',navy2='#2d3180',ink='#2d2a4a',grey='#c9c2d6',grey2='#ab a3bd'.replace(' ',''),brown='#b8754a',brown2='#99603a',tan='#efc596',tan2='#d9a877',slate='#8fa0d8',slate2='#7385c4')
def eyes2(x1,x2,y,r=4.6): return ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{Q["ink"]}"/><circle cx="{x+1.5}" cy="{y-1.6}" r="1.5" fill="#fff"/>' for x in (x1,x2))
def blush(x1,x2,y): return f'<ellipse cx="{x1}" cy="{y}" rx="6" ry="3.6" fill="{Q["pink"]}"/><ellipse cx="{x2}" cy="{y}" rx="6" ry="3.6" fill="{Q["pink"]}"/>'
def spark(x,y,s,c):  # 4-point sparkle
    return f'<path d="M{x} {y-s} Q{x+s*.18} {y-s*.18} {x+s} {y} Q{x+s*.18} {y+s*.18} {x} {y+s} Q{x-s*.18} {y+s*.18} {x-s} {y} Q{x-s*.18} {y-s*.18} {x} {y-s} Z" fill="{c}"/>'
def star8(x,y,s,c):
    pts=' '.join(f'{x+(s if k%2==0 else s*.38)*math.cos(k*math.pi/4-math.pi/2):.1f},{y+(s if k%2==0 else s*.38)*math.sin(k*math.pi/4-math.pi/2):.1f}' for k in range(8))
    return f'<polygon points="{pts}" fill="{c}"/>'
# heads: two-tone flat, no outlines (shade = a darker shape on the lower-right)
H={
'mouse': f'<circle cx="24" cy="34" r="20" fill="{Q["grey"]}"/><circle cx="76" cy="34" r="20" fill="{Q["grey2"]}"/><circle cx="25" cy="35" r="11" fill="{Q["pink"]}"/><circle cx="75" cy="35" r="11" fill="{Q["pink2"]}"/><ellipse cx="50" cy="62" rx="29" ry="26" fill="{Q["grey"]}"/><path d="M79 62 A29 26 0 0 1 50 88 A29 26 0 0 0 72 62 Z" fill="{Q["grey2"]}"/><ellipse cx="50" cy="74" rx="13" ry="8" fill="{Q["cream"]}"/>{eyes2(40,60,57)}{blush(31,69,68)}<ellipse cx="50" cy="70" rx="5" ry="3.8" fill="{Q["coral"]}"/>',
'cat': f'<path d="M20 50 L24 12 L46 34 Z" fill="{Q["orange"]}"/><path d="M80 50 L76 12 L54 34 Z" fill="{Q["orange2"]}"/><path d="M27 42 L28 24 L38 34 Z" fill="{Q["pink"]}"/><path d="M73 42 L72 24 L62 34 Z" fill="{Q["pink2"]}"/><ellipse cx="50" cy="58" rx="33" ry="29" fill="{Q["orange"]}"/><path d="M83 58 A33 29 0 0 1 50 87 A33 29 0 0 0 76 58 Z" fill="{Q["orange2"]}"/><path d="M44 30 L46 40 M50 29 L50 40 M56 30 L54 40" stroke="{Q["orange2"]}" stroke-width="3.4" stroke-linecap="round"/><path d="M36 66 Q50 58 64 66 Q64 82 50 84 Q36 82 36 66 Z" fill="{Q["cream"]}"/>{eyes2(39,61,55)}{blush(29,71,66)}<path d="M46 64 L54 64 L50 68 Z" fill="{Q["coral"]}"/>',
'dog': f'<ellipse cx="50" cy="56" rx="31" ry="30" fill="{Q["tan"]}"/><path d="M81 56 A31 30 0 0 1 50 86 A31 30 0 0 0 74 56 Z" fill="{Q["tan2"]}"/><path d="M58 28 C72 24 80 38 74 50 C66 50 58 42 58 28 Z" fill="{Q["brown"]}"/><path d="M24 30 C6 32 6 66 20 70 C30 62 30 40 26 30 Z" fill="{Q["brown"]}"/><path d="M76 30 C94 32 94 66 80 70 C70 62 70 40 74 30 Z" fill="{Q["brown2"]}"/><ellipse cx="50" cy="70" rx="16" ry="12" fill="{Q["cream"]}"/>{eyes2(40,60,51)}{blush(30,70,63)}<ellipse cx="50" cy="64" rx="8" ry="5.5" fill="{Q["ink"]}"/><path d="M46 74 Q50 88 54 74 Z" fill="{Q["coral"]}"/>',
'bear': f'<circle cx="24" cy="28" r="14" fill="{Q["brown"]}"/><circle cx="76" cy="28" r="14" fill="{Q["brown2"]}"/><circle cx="24" cy="29" r="6.5" fill="{Q["tan"]}"/><circle cx="76" cy="29" r="6.5" fill="{Q["tan2"]}"/><circle cx="50" cy="56" r="33" fill="{Q["brown"]}"/><path d="M83 56 A33 33 0 0 1 50 89 A33 33 0 0 0 76 56 Z" fill="{Q["brown2"]}"/><ellipse cx="50" cy="69" rx="16" ry="12" fill="{Q["tan"]}"/>{eyes2(38,62,50)}<ellipse cx="50" cy="64" rx="7" ry="5" fill="{Q["ink"]}"/>{blush(28,72,61)}',
'lion': ''.join(f'<ellipse cx="{50+34*math.cos(a*math.pi/5):.1f}" cy="{54+34*math.sin(a*math.pi/5):.1f}" rx="15" ry="15" fill="{Q["orange2"] if a in (0,1,2,9) else Q["orange"]}"/>' for a in range(10)) + f'<circle cx="50" cy="54" r="34" fill="{Q["orange"]}"/><circle cx="50" cy="56" r="27" fill="{Q["mustard"]}"/><path d="M77 56 A27 27 0 0 1 50 83 A27 27 0 0 0 71 56 Z" fill="{Q["mustard2"]}"/><circle cx="31" cy="34" r="6" fill="{Q["mustard"]}"/><circle cx="69" cy="34" r="6" fill="{Q["mustard2"]}"/><path d="M38 62 Q50 56 62 62 Q62 76 50 78 Q38 76 38 62 Z" fill="{Q["cream"]}"/>{eyes2(41,59,51)}{blush(33,67,62)}<path d="M45 60 L55 60 L50 65 Z" fill="{Q["coral"]}"/>',
'elephant': f'<path d="M26 28 C0 26 2 76 28 72 C32 58 34 40 26 28 Z" fill="{Q["slate"]}"/><path d="M74 28 C100 26 98 76 72 72 C68 58 66 40 74 28 Z" fill="{Q["slate2"]}"/><path d="M28 32 C14 36 16 62 28 64 Z" fill="{Q["pink"]}"/><path d="M72 32 C86 36 84 62 72 64 Z" fill="{Q["pink2"]}"/><ellipse cx="50" cy="48" rx="26" ry="27" fill="{Q["slate"]}"/><path d="M76 48 A26 27 0 0 1 56 74 L58 62 C66 60 70 54 70 48 Z" fill="{Q["slate2"]}"/><path d="M43 62 C43 78 44 88 56 90 C62 90 64 84 58 82 C54 82 56 74 57 62 Z" fill="{Q["slate"]}"/><path d="M52 62 C52 76 54 84 58 86 C62 88 64 84 58 82 C54 82 56 74 57 62 Z" fill="{Q["slate2"]}"/>{eyes2(40,60,45)}{blush(33,67,56)}<path d="M40 60 Q38 66 34 68 M60 60 Q62 66 66 68" stroke="{Q["cream"]}" stroke-width="4.5" stroke-linecap="round"/>',
}
def sv(k,size): return f'<svg viewBox="0 0 100 100" width="{size}" height="{size}" style="overflow:visible">{H[k]}</svg>'
deco=lambda W,Hh,seed,n=22: f'<svg width="{W}" height="{Hh}" style="position:absolute;left:0;top:0">' + ''.join((spark if k%2 else star8)(((seed*37+k*97)%W),((seed*53+k*61)%Hh),5+(k*7)%9,[Q["pink"],Q["mustard"],Q["cream"],Q["lav"]][k%4]) for k in range(n)) + '</svg>'
HEADQ=HEAD.replace('family=Fredoka:wght@500;600;700','family=Fredoka:wght@500;600;700&amp;family=Bagel+Fat+One')
TT="font-family:'Bagel Fat One',Fredoka,sans-serif"
SC='width:390px;height:844px;box-sizing:border-box;position:relative;overflow:hidden;font-family:Fredoka,sans-serif;color:'+Q['ink']+';'
def pill(x,y,w,h,bg,sh,txt,fs=19,col=None):
    col=col or Q['ink']
    return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:16px;background:{bg};box-shadow:0 5px 0 {sh};display:flex;align-items:center;justify-content:center;gap:6px;font:700 {fs}px Fredoka,sans-serif;color:{col}">{txt}</div>'
boards={}
# ---- 30 animals sheet
cells=''.join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:6px">{sv(k,96)}<span style="font:600 13px Fredoka,sans-serif;color:{Q["cream"]}">{k}</span></div>' for k in ['mouse','cat','dog','bear','lion','elephant'])
small=''.join(f'<div style="width:50px;height:50px;background:{Q["cream"] if j%2 else Q["cream2"]};display:grid;place-items:center">{sv(k,42)}</div>' for j,k in enumerate(['mouse','cat','dog','bear','lion','elephant']))
b=f'''<div style="width:780px;height:844px;position:relative;overflow:hidden;background:{Q["purple"]};font-family:Fredoka,sans-serif">{deco(780,844,3,40)}
  <div style="position:absolute;left:30px;top:26px;{TT};font-size:40px;color:{Q["cream"]}">Retro flat</div>
  <div style="position:absolute;left:30px;top:80px;font:600 16px Fredoka,sans-serif;color:{Q["cream"]}">No outlines. Each shape is one flat colour plus a darker shade of the same colour on one side.</div>
  <div style="position:absolute;left:30px;right:30px;top:130px;height:200px;border-radius:24px;background:{Q["lav2"]};display:flex;justify-content:space-around;align-items:center">{cells}</div>
  <div style="position:absolute;left:30px;top:356px;font:700 16px Fredoka,sans-serif;color:{Q["cream"]}">At board size</div>
  <div style="position:absolute;left:30px;top:384px;width:150px;height:100px;border-radius:12px;overflow:hidden;display:flex;flex-wrap:wrap">{small}</div>
  <div style="position:absolute;left:220px;top:356px;font:700 16px Fredoka,sans-serif;color:{Q["cream"]}">Palette</div>
  <div style="position:absolute;left:220px;top:384px;display:flex;gap:10px;flex-wrap:wrap;width:520px">{''.join(f'<div style="width:56px;height:56px;border-radius:14px;background:{c};box-shadow:0 4px 0 rgba(0,0,0,.15)"></div>' for c in [Q["purple"],Q["lav"],Q["mustard"],Q["orange"],Q["coral"],Q["pink"],Q["cream"],Q["olive"],Q["green"],Q["navy"]])}</div>
  <div style="position:absolute;left:30px;top:520px;font:700 16px Fredoka,sans-serif;color:{Q["cream"]}">Objects and buttons</div>
  <svg width="720" height="260" style="position:absolute;left:30px;top:552px">
    <rect x="0" y="40" width="130" height="90" rx="12" fill="{Q["olive"]}"/><rect x="0" y="110" width="130" height="20" rx="8" fill="{Q["olive2"]}"/><path d="M30 130 L30 70 Q65 30 100 70 L100 130 Z" fill="{Q["navy2"]}"/><path d="M52 130 Q48 110 62 96 Q66 112 76 114 Q80 124 72 130 Z" fill="{Q["mustard"]}"/>
    <g transform="translate(160 40)"><rect x="0" y="20" width="44" height="60" rx="16" fill="{Q["orange"]}"/><rect x="24" y="20" width="20" height="60" rx="10" fill="{Q["orange2"]}"/><rect x="0" y="36" width="44" height="6" fill="{Q["orange2"]}"/><rect x="0" y="60" width="44" height="6" fill="{Q["orange2"]}"/><rect x="52" y="20" width="44" height="60" rx="16" fill="{Q["orange"]}"/><rect x="76" y="20" width="20" height="60" rx="10" fill="{Q["orange2"]}"/><rect x="52" y="36" width="44" height="6" fill="{Q["orange2"]}"/><rect x="52" y="60" width="44" height="6" fill="{Q["orange2"]}"/></g>
    <g transform="translate(290 30)"><rect x="0" y="0" width="100" height="100" rx="12" fill="{Q["cream"]}"/><rect x="0" y="70" width="100" height="30" rx="10" fill="{Q["cream2"]}"/><circle cx="50" cy="40" r="22" fill="{Q["coral"]}"/><circle cx="50" cy="40" r="10" fill="{Q["mustard"]}"/></g>
    <g transform="translate(420 40)"><path d="M10 80 L50 10 L90 80 Z" fill="{Q["mustard"]}"/><path d="M50 10 L90 80 L60 80 Z" fill="{Q["mustard2"]}"/><circle cx="40" cy="58" r="7" fill="{Q["mustard2"]}"/><circle cx="58" cy="44" r="5" fill="{Q["mustard2"]}"/></g>
    <g transform="translate(540 50)"><rect x="0" y="0" width="150" height="56" rx="18" fill="{Q["coral2"]}"/><rect x="0" y="0" width="150" height="48" rx="18" fill="{Q["coral"]}"/><text x="75" y="33" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="22" fill="{Q["cream"]}">Go!</text></g>
  </svg>
</div>'''
boards['Retro-sheet.dc.html']=('30 · Retro flat: animals, palette and objects',b)
# ---- 31 board screen
N=7; cs=46; ox=(390-N*cs)//2; oy=254
cells=''.join(f'<rect x="{x*cs}" y="{y*cs}" width="{cs}" height="{cs}" fill="{Q["cream"] if (x+y)%2 else Q["cream2"]}"/>' for y in range(N) for x in range(N))
walls=''.join(f'<rect x="{x*cs+4}" y="{y*cs+4}" width="{cs-8}" height="{cs-8}" rx="10" fill="{Q["lav"]}"/><rect x="{x*cs+4}" y="{y*cs+cs-16}" width="{cs-8}" height="12" rx="6" fill="{Q["lav2"]}"/>' for x,y in [(4,2),(1,5)])
bd=f'<svg width="{N*cs}" height="{N*cs}" style="position:absolute;left:{ox}px;top:{oy}px;overflow:visible"><rect x="-12" y="-10" width="{N*cs+24}" height="{N*cs+26}" rx="22" fill="{Q["navy2"]}"/><rect x="-12" y="-12" width="{N*cs+24}" height="{N*cs+22}" rx="22" fill="{Q["navy"]}"/><g><clipPath id="cl"><rect x="0" y="0" width="{N*cs}" height="{N*cs}" rx="12"/></clipPath><g clip-path="url(#cl)">{cells}</g></g>{walls}<ellipse cx="{cs/2}" cy="{3*cs+cs/2+2}" rx="16" ry="12" fill="{Q["ink"]}"/></svg>'
ani=''.join(f'<div style="position:absolute;left:{ox+x*cs+3}px;top:{oy+y*cs+3}px">{sv(k,cs-6)}</div>' for k,x,y in [('mouse',3,3),('cat',5,4),('dog',2,1),('bear',5,1)])
ani+=f'<div style="position:absolute;left:{ox+6*cs+3}px;top:{oy+4*cs+3}px;width:{cs-6}px;height:{cs-6}px;border-radius:12px;background:{Q["mustard"]};opacity:.75"></div>'
chain=''.join(sv(k,28)+(f'<b style="color:{Q["coral"]};font:700 16px Fredoka">›</b>' if i<5 else '') for i,k in enumerate(['mouse','cat','dog','bear','lion','elephant']))
cheese=f'<svg viewBox="0 0 100 100" width="22" height="22"><path d="M8 74 L92 74 L92 40 Z" fill="{Q["mustard"]}"/><path d="M8 74 L92 40 L62 20 Z" fill="#f7cd6a"/><circle cx="62" cy="60" r="6" fill="{Q["mustard2"]}"/></svg>'
b=f'''<div style="{SC}background:{Q["purple"]}">{deco(390,844,7,26)}
  <div style="position:absolute;left:16px;right:16px;top:22px;display:flex;align-items:center;gap:8px">{sv('mouse',36)}<div style="{TT};font-size:24px;color:{Q["cream"]};flex:1;white-space:nowrap">Scare-a-Mouse</div>
    <div style="height:40px;padding:0 12px;border-radius:14px;background:{Q["mustard"]};box-shadow:0 4px 0 {Q["mustard2"]};display:grid;place-items:center;font:700 16px Fredoka,sans-serif;white-space:nowrap">Level 47</div></div>
  <div style="position:absolute;left:16px;right:16px;top:80px;display:flex;align-items:center;justify-content:space-between"><div style="{TT};font-size:24px;color:{Q["cream"]}">Haystack Hop</div>
    <div style="padding:3px 12px;border-radius:999px;background:{Q["cream"]};display:flex;align-items:center;gap:4px;font:700 16px Fredoka,sans-serif">{cheese} 12</div></div>
  <div style="position:absolute;left:16px;right:16px;top:124px;padding:12px 14px;border-radius:18px;background:{Q["cream"]};box-shadow:0 5px 0 {Q["cream2"]};font:600 16px/1.3 Fredoka,sans-serif">Lions scare bears. Start a chain that ends with the mouse in the hole!</div>
  <div style="position:absolute;left:16px;right:16px;top:196px;height:40px;border-radius:14px;background:{Q["lav2"]};display:flex;align-items:center;justify-content:center;gap:4px">{chain}</div>
  {bd}{ani}
  <div style="position:absolute;left:16px;right:16px;top:640px;height:76px;border-radius:18px;background:{Q["cream"]};box-shadow:0 5px 0 {Q["cream2"]};display:flex;align-items:center;gap:12px;padding:0 14px">
    <b style="font:600 15px Fredoka,sans-serif;width:60px;line-height:1.1">Your animals</b>
    <div style="width:58px;height:58px;border-radius:16px;background:{Q["mustard"]};box-shadow:0 4px 0 {Q["mustard2"]};display:grid;place-items:center">{sv('elephant',46)}</div>
    <div style="width:58px;height:58px;border-radius:16px;background:{Q["cream2"]};display:grid;place-items:center">{sv('lion',46)}</div></div>
  {pill(16,738,112,52,Q["cream"],Q["cream2"],'Hint · 1 '+cheese,17)}{pill(140,738,100,52,Q["pink"],Q["pink2"],'Reset',18)}{pill(252,738,122,52,Q["coral"],Q["coral2"],'Go!',20,Q["cream"])}
</div>'''
boards['Retro-board.dc.html']=('31 · Retro flat: the game board',b)
# ---- 32 room map (Meadow)
def node(n,x,y,state):
    bg={'done':Q['mustard'],'cur':Q['cream'],'next':Q['cream'],'lock':Q['lav']}[state]
    sh={'done':Q['mustard2'],'cur':Q['cream2'],'next':Q['cream2'],'lock':Q['lav2']}[state]
    ring=f'box-shadow:0 4px 0 {sh},0 0 0 6px {Q["coral"]};' if state=='cur' else f'box-shadow:0 4px 0 {sh};'
    tick=f'<b style="position:absolute;right:-6px;bottom:-6px;width:18px;height:18px;border-radius:50%;background:{Q["green"]};color:#fff;font:700 11px Fredoka;display:grid;place-items:center">✓</b>' if state=='done' else ''
    return f'<div style="position:absolute;left:{x-22}px;top:{y-22}px;width:44px;height:44px;border-radius:50%;background:{bg};{ring}display:grid;place-items:center;font:700 16px Fredoka,sans-serif;color:{Q["ink"]}">{n}{tick}</div>'
def crd(ps):
    d=f'M {ps[0][0]} {ps[0][1]}'
    for i in range(len(ps)-1):
        a=ps[i-1] if i>0 else ps[i]; bb=ps[i]; c=ps[i+1]; e=ps[i+2] if i+2<len(ps) else c
        d+=f' C {bb[0]+(c[0]-a[0])/6:.1f} {bb[1]+(c[1]-a[1])/6:.1f}, {c[0]-(e[0]-bb[0])/6:.1f} {c[1]-(e[1]-bb[1])/6:.1f}, {c[0]} {c[1]}'
    return d
pts=[(110,700),(180,665),(255,625),(290,560),(225,512),(140,478),(92,420),(150,372),(235,340),(290,282)]
road=crd([(195,860),(150,780)]+pts+[(240,220),(195,170)])
nodes=''.join(node(21+k,x,y,'done' if k<5 else 'cur' if k==5 else 'next' if k==6 else 'lock') for k,(x,y) in enumerate(pts))
tree=lambda x,y: f'<svg width="90" height="110" style="position:absolute;left:{x}px;top:{y}px"><rect x="38" y="56" width="16" height="44" rx="6" fill="{Q["brown"]}"/><rect x="46" y="56" width="8" height="44" rx="4" fill="{Q["brown2"]}"/><circle cx="46" cy="40" r="36" fill="{Q["green"]}"/><path d="M82 40 A36 36 0 0 1 46 76 A36 36 0 0 0 74 40 Z" fill="{Q["green2"]}"/><circle cx="32" cy="30" r="7" fill="{Q["coral"]}"/><circle cx="60" cy="46" r="7" fill="{Q["coral"]}"/><circle cx="50" cy="20" r="7" fill="{Q["coral"]}"/></svg>'
mush=lambda x,y,c,c2: f'<svg width="50" height="50" style="position:absolute;left:{x}px;top:{y}px"><rect x="18" y="26" width="14" height="20" rx="6" fill="{Q["cream"]}"/><path d="M4 30 Q25 -4 46 30 Z" fill="{c}"/><path d="M30 6 Q44 14 46 30 L34 30 Z" fill="{c2}"/><circle cx="18" cy="20" r="4" fill="{Q["cream"]}"/><circle cx="32" cy="14" r="3" fill="{Q["cream"]}"/></svg>'
pond=f'<svg width="130" height="80" style="position:absolute;left:222px;top:400px"><ellipse cx="65" cy="44" rx="60" ry="30" fill="{Q["navy2"]}"/><ellipse cx="65" cy="40" rx="60" ry="30" fill="{Q["slate"]}"/><path d="M36 40 Q48 34 60 40" stroke="{Q["cream"]}" stroke-width="4" fill="none" stroke-linecap="round"/><ellipse cx="90" cy="32" rx="14" ry="8" fill="{Q["olive"]}"/></svg>'
picnic=f'<svg width="110" height="74" style="position:absolute;left:22px;top:218px"><g transform="rotate(-6 55 37)"><rect x="6" y="10" width="96" height="58" rx="8" fill="{Q["coral2"]}"/><rect x="6" y="6" width="96" height="56" rx="8" fill="{Q["coral"]}"/><path d="M30 6 L30 62 M54 6 L54 62 M78 6 L78 62 M6 24 L102 24 M6 44 L102 44" stroke="{Q["cream"]}" stroke-width="6"/></g></svg>'
b=f'''<div style="{SC}background:{Q["olive"]}">
  <svg width="390" height="844" style="position:absolute;left:0;top:0">{''.join(f'<path d="M{(k*53)%380} {200+(k*89)%620} l4 -9 l4 9" stroke="{Q["olive2"]}" stroke-width="3" fill="none" stroke-linecap="round"/>' for k in range(40))}</svg>
  <div style="position:absolute;left:0;right:0;top:0;height:60px;display:flex;align-items:center;gap:10px;padding:0 14px;box-sizing:border-box;background:{Q["purple"]}">
    {pill(14,10,98,40,Q["mustard"],Q["mustard2"],'Castle',16)}<div style="position:absolute;left:126px;top:14px;{TT};font-size:24px;color:{Q["cream"]}">Meadow</div><b style="position:absolute;right:16px;top:20px;font:700 15px Fredoka,sans-serif;color:{Q["cream"]}">5/20</b></div>
  <div style="position:absolute;left:0;right:0;top:60px;height:120px;background:{Q["pink"]};overflow:hidden">
    <svg width="390" height="120"><circle cx="330" cy="40" r="22" fill="{Q["mustard"]}"/><path d="M40 40 q14 -16 28 0 q14 -10 22 6 h-54 z" fill="{Q["cream"]}"/><path d="M-10 120 Q90 40 190 120 Z" fill="{Q["green"]}"/><path d="M150 120 Q270 50 400 120 Z" fill="{Q["green2"]}"/><path d="M168 120 L168 72 Q195 40 222 72 L222 120 Z" fill="{Q["navy"]}"/><path d="M195 52 Q222 58 222 72 L222 120 L195 120 Z" fill="{Q["navy2"]}"/></svg></div>
  <svg width="390" height="844" style="position:absolute;left:0;top:0"><path d="{road}" fill="none" stroke="{Q["mustard2"]}" stroke-width="40" stroke-linecap="round" transform="translate(0 4)"/><path d="{road}" fill="none" stroke="{Q["cream"]}" stroke-width="38" stroke-linecap="round"/></svg>
  {tree(290,690)}{tree(4,520)}{pond}{picnic}{mush(330,240,Q["coral"],Q["coral2"])}{mush(30,330,Q["mustard"],Q["mustard2"])}{mush(310,760,Q["pink"],Q["pink2"])}
  <svg width="390" height="844" style="position:absolute;left:0;top:0">{spark(60,610,8,Q["cream"])}{spark(350,620,6,Q["mustard"])}{star8(200,780,9,Q["pink"])}{spark(150,250,7,Q["cream"])}</svg>
  {nodes}
  <div style="position:absolute;left:122px;top:430px">{sv('mouse',36)}</div>
</div>'''
boards['Retro-room.dc.html']=('32 · Retro flat: a room map (Meadow)',b)
# ---- 33 castle
def band(top,label,bg,sh,state,sub=''):
    if state=='lock':
        return f'<div style="position:absolute;left:52px;right:52px;top:{top}px;height:52px;border-radius:16px;background:{Q["lav2"]};display:grid;place-items:center;color:{Q["lav"]};font:700 22px Fredoka">?</div>'
    ring=f'box-shadow:0 5px 0 {sh},0 0 0 6px {Q["mustard"]};' if state=='here' else f'box-shadow:0 5px 0 {sh};'
    return f'<div style="position:absolute;left:52px;right:52px;top:{top}px;height:52px;border-radius:16px;background:{bg};{ring}display:flex;align-items:center;padding:0 14px;gap:8px"><b style="font:700 18px Fredoka,sans-serif;flex:1;color:{Q["cream"]}">{label}</b><span style="font:700 14px Fredoka,sans-serif;color:{Q["cream"]}">{sub}</span></div>'
b=f'''<div style="{SC}background:{Q["navy"]}">{deco(390,300,11,20)}
  <svg width="390" height="844" style="position:absolute;left:0;top:0">
    <circle cx="66" cy="74" r="26" fill="{Q["cream"]}"/><circle cx="76" cy="66" r="24" fill="{Q["navy"]}"/>
    <rect x="252" y="70" width="80" height="120" rx="10" fill="{Q["lav"]}"/><rect x="300" y="70" width="32" height="120" rx="10" fill="{Q["lav2"]}"/><path d="M240 76 L292 20 L344 76 Z" fill="{Q["coral"]}"/><path d="M292 20 L344 76 L310 76 Z" fill="{Q["coral2"]}"/>
    <rect x="34" y="140" width="322" height="530" rx="18" fill="{Q["lav"]}"/><rect x="300" y="140" width="56" height="530" rx="18" fill="{Q["lav2"]}"/>
    {''.join(f'<rect x="{34+k*56}" y="118" width="34" height="34" rx="8" fill="{Q["lav"]}"/>' for k in range(6))}
    <rect x="0" y="672" width="390" height="34" fill="{Q["slate"]}"/><rect x="0" y="706" width="390" height="140" fill="{Q["olive"]}"/>
    <rect x="166" y="660" width="58" height="52" rx="10" fill="{Q["brown"]}"/>
    <path d="M292 20 L292 0 L316 6 L292 12" fill="{Q["mustard"]}"/>
  </svg>
  <div style="position:absolute;left:104px;top:56px;{TT};font-size:30px;color:{Q["cream"]}">The castle</div>
  {band(170,'','','','lock')}{band(234,'','','','lock')}{band(298,'','','','lock')}{band(362,'','','','lock')}
  {band(428,'Second floor',Q['coral'],Q['coral2'],'here','0/150')}
  {band(494,'First floor',Q['orange'],Q['orange2'],'open','✓')}
  {band(584,'Cellars',Q['green'],Q['green2'],'open','✓')}
  {band(744,'Outside',Q['olive2'],Q['green2'],'open','✓')}
  <div style="position:absolute;left:298px;top:398px">{sv('mouse',36)}</div>
</div>'''
boards['Retro-castle.dc.html']=('33 · Retro flat: the whole castle',b)
base='/home/claude/mockups/project'
for fn,(t,body) in boards.items():
    open(f'{base}/{fn}','w').write(HEADQ%t+body+'\n'+TAIL.replace('{"width":390,"height":844}','{"width":780,"height":844}' if 'sheet' in fn else '{"width":390,"height":844}'))
c=json.load(open(f'{base}/canvas.json'))
for fn in boards: c['boards'].pop(fn,None); c['order']=[o for o in c['order'] if o!=fn]
y=max(v['y'] for v in c['boards'].values())+844+400; x=0
for fn in boards:
    w=780 if 'sheet' in fn else 390
    c['boards'][fn]={'x':x,'y':y,'w':w,'h':844,'title':boards[fn][0]}; c['order'].append(fn); x+=w+80
c['notes']['t7']={'x':0,'y':y-260,'text':'Retro flat (your second reference): no outlines, two-tone shading','kind':'title1','maxW':2200}
json.dump(c,open(f'{base}/canvas.json','w'),ensure_ascii=False)
print('ok')
