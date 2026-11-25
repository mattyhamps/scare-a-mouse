import json, math
INK='#2b1d14'; SW=2.6
P=dict(cream='#f1e3c2',cream2='#e3cfa0',sky='#8fb3c9',grass='#6f8f45',grass2='#4f7337',yellow='#d9a43a',orange='#b5622a',red='#8e2a2f',pink='#c9a24a',purple='#2f4f8f',blue='#5a3a24',stone='#a39c8f',stone2='#857e72',navy='#1e2a44',brown='#7a4b2a',tan='#cfae78',white='#f7efdc',grey='#b9b2a6')
st=f'stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round" stroke-linecap="round"'
def eyes(x1,x2,y,r=5): return f'<circle cx="{x1}" cy="{y}" r="{r}" fill="{INK}"/><circle cx="{x2}" cy="{y}" r="{r}" fill="{INK}"/><circle cx="{x1+1.6}" cy="{y-1.8}" r="1.6" fill="#fff"/><circle cx="{x2+1.6}" cy="{y-1.8}" r="1.6" fill="#fff"/>'
ANIMAL={
'mouse': f'<circle cx="26" cy="30" r="17" fill="{P["grey"]}" {st}/><circle cx="74" cy="30" r="17" fill="{P["grey"]}" {st}/><circle cx="26" cy="30" r="8" fill="#d98b8b"/><circle cx="74" cy="30" r="8" fill="#d98b8b"/><ellipse cx="50" cy="60" rx="30" ry="27" fill="{P["grey"]}" {st}/>{eyes(40,60,55)}<circle cx="50" cy="70" r="5" fill="#d98b8b" {st}/><path d="M30 68 L12 64 M30 73 L12 76 M70 68 L88 64 M70 73 L88 76" {st} fill="none"/>',
'cat': f'<path d="M18 46 L22 12 L42 30 Z" fill="#d98a3a" {st}/><path d="M82 46 L78 12 L58 30 Z" fill="#d98a3a" {st}/><ellipse cx="50" cy="56" rx="34" ry="30" fill="#d98a3a" {st}/><path d="M40 30 L44 40 M50 28 L50 40 M60 30 L56 40" {st} fill="none"/>{eyes(38,62,54)}<path d="M45 64 L55 64 L50 70 Z" fill="#d98b8b" {st}/><path d="M28 66 L10 62 M28 71 L10 74 M72 66 L90 62 M72 71 L90 74" {st} fill="none"/>',
'dog': f'<ellipse cx="50" cy="54" rx="32" ry="31" fill="{P["tan"]}" {st}/><path d="M22 30 C8 34 6 62 18 66 C26 60 26 40 24 30 Z" fill="{P["brown"]}" {st}/><path d="M78 30 C92 34 94 62 82 66 C74 60 74 40 76 30 Z" fill="{P["brown"]}" {st}/><ellipse cx="62" cy="44" rx="10" ry="9" fill="{P["brown"]}"/>{eyes(40,62,50)}<ellipse cx="50" cy="66" rx="9" ry="6" fill="{INK}"/><path d="M50 72 L50 78 M42 78 Q50 84 58 78" {st} fill="none"/><path d="M46 80 Q50 92 54 80" fill="{P["red"]}" {st}/>',
'bear': f'<circle cx="24" cy="26" r="13" fill="{P["brown"]}" {st}/><circle cx="76" cy="26" r="13" fill="{P["brown"]}" {st}/><circle cx="50" cy="55" r="34" fill="{P["brown"]}" {st}/><ellipse cx="50" cy="68" rx="16" ry="12" fill="{P["tan"]}" {st}/>{eyes(37,63,50)}<ellipse cx="50" cy="63" rx="7" ry="5" fill="{INK}"/><path d="M50 68 L50 74 M44 75 Q50 79 56 75" {st} fill="none"/>',
'lion': f'<circle cx="50" cy="52" r="44" fill="{P["orange"]}" {st}/>' + ''.join(f'<circle cx="{50+40*__import__("math").cos(a*0.5236):.1f}" cy="{52+40*__import__("math").sin(a*0.5236):.1f}" r="10" fill="{P["orange"]}" {st}/>' for a in range(12)) + f'<circle cx="50" cy="52" r="40" fill="{P["orange"]}"/><circle cx="50" cy="54" r="28" fill="{P["yellow"]}" {st}/>{eyes(40,60,50)}<path d="M44 60 L56 60 L50 66 Z" fill="{INK}"/><path d="M50 66 L50 71 M44 72 Q50 76 56 72" {st} fill="none"/>',
'elephant': f'<path d="M24 26 C2 28 2 72 26 70 C30 56 32 38 24 26 Z" fill="#6f7c99" {st}/><path d="M76 26 C98 28 98 72 74 70 C70 56 68 38 76 26 Z" fill="#6f7c99" {st}/><ellipse cx="50" cy="48" rx="28" ry="28" fill="#8f9cb8" {st}/><path d="M44 62 C44 80 40 88 30 90 C28 92 30 96 34 95 C50 92 56 80 56 62 Z" fill="#8f9cb8" {st}/>{eyes(40,60,44)}<path d="M36 60 L30 70 M64 60 L70 70" stroke="#fff" stroke-width="5" stroke-linecap="round"/>',
}
# STORYBOOK: use the storybook heads (with the extra detail, variation 1) for the outlined style too
_g2=open('./gen2.py').read(); _g3=open('./gen3.py').read()
exec(_g2[_g2.index("C=dict("):_g2.index("# ---------- Option A")])
exec(_g3[_g3.index("thin=f'stroke"):_g3.index("VAR=[")])
ANIMAL.update(heads('big'))
def icon(k, size=22):
    I={'lock':f'<rect x="20" y="44" width="60" height="44" rx="8" fill="{P["yellow"]}" {st}/><path d="M32 44 L32 32 C32 12 68 12 68 32 L68 44" fill="none" {st}/><circle cx="50" cy="64" r="6" fill="{INK}"/>',
       'cheese':f'<path d="M10 70 L90 70 L90 40 L10 70 Z" fill="{P["yellow"]}" {st}/><path d="M10 70 L90 40 L60 20 Z" fill="#e8c56a" {st}/><circle cx="58" cy="58" r="5" fill="#b58a2a"/><circle cx="76" cy="52" r="4" fill="#b58a2a"/>',
       'castle':f'<path d="M14 88 L14 30 L26 30 L26 40 L38 40 L38 30 L62 30 L62 40 L74 40 L74 30 L86 30 L86 88 Z" fill="{P["stone"]}" {st}/><path d="M40 88 L40 64 C40 52 60 52 60 64 L60 88" fill="{P["brown"]}" {st}/>',
       'book':f'<path d="M14 24 L50 32 L86 24 L86 80 L50 88 L14 80 Z" fill="{P["white"]}" {st}/><path d="M50 32 L50 88" {st}/><path d="M14 24 L14 80" stroke="{P["red"]}" stroke-width="8"/>',
       'quill':f'<path d="M80 12 C40 20 24 50 22 82 C46 70 70 46 80 12 Z" fill="{P["white"]}" {st}/><path d="M22 82 L14 92 M30 70 L60 34" {st} fill="none"/>',
       'down':f'<path d="M50 14 L50 80 M24 56 L50 82 L76 56" fill="none" {st} stroke-width="10"/>',
       'note':f'<path d="M36 76 L36 22 L76 14 L76 66" fill="none" {st} stroke-width="8"/><ellipse cx="28" cy="78" rx="12" ry="9" fill="{INK}"/><ellipse cx="68" cy="68" rx="12" ry="9" fill="{INK}"/>',
       'tick':f'<path d="M18 52 L40 74 L82 28" fill="none" {st} stroke-width="12"/>'}
    return f'<svg viewBox="0 0 100 100" width="{size}" height="{size}" style="vertical-align:middle;overflow:visible">{I[k]}</svg>'
def animal(k, size, x=None, y=None, extra=''):
    pos = f'position:absolute;left:{x}px;top:{y}px;' if x is not None else ''
    return f'<svg viewBox="0 0 100 100" width="{size}" height="{size}" style="{pos}overflow:visible{extra}">{ANIMAL[k]}</svg>'
HEAD='''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>%s</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&amp;display=swap">
<style>
body{margin:0}
.k{border:2.5px solid #2b1d14;border-radius:10px}
.btn{position:absolute;height:52px;box-sizing:border-box;border:2.5px solid #2b1d14;border-radius:10px;display:flex;align-items:center;justify-content:center;gap:6px;white-space:nowrap;font:700 19px Fredoka,sans-serif;color:#2b1d14;box-shadow:0 3px 0 #2b1d14}
@keyframes bob{0%%,100%%{transform:translateY(0)}50%%{transform:translateY(-5px)}}
</style>
</helmet>
'''
TAIL='''</x-dc>
<script type="text/x-dc" data-dc-script data-props='{"$preview":{"width":390,"height":844}}'>
class Component extends DCLogic {
  renderVals() { return {}; }
}
</script>
</body>
</html>
'''
SCREEN=f'width:390px;height:844px;box-sizing:border-box;position:relative;overflow:hidden;font-family:Fredoka,system-ui,sans-serif;color:{INK};'
boards={}
# ---- 1. Game board
N=7; cs=46; ox=(390-N*cs)//2; oy=258
cells=''
walls={(4,2),(1,5)}
for y in range(N):
  for x in range(N):
    cells+=f'<rect x="{x*cs}" y="{y*cs}" width="{cs}" height="{cs}" fill="{P["cream"] if (x+y)%2 else P["cream2"]}"/>'
    if (x,y) in walls:
      cells+=f'<rect x="{x*cs+3}" y="{y*cs+3}" width="{cs-6}" height="{cs-6}" rx="8" fill="{P["stone2"]}" {st}/>'
hole=(0,3)
cells+=f'<ellipse cx="{hole[0]*cs+cs/2}" cy="{hole[1]*cs+cs/2+2}" rx="17" ry="13" fill="{INK}"/>'
board_svg=f'<svg width="{N*cs}" height="{N*cs}" style="position:absolute;left:{ox}px;top:{oy}px;overflow:visible"><rect x="-14" y="-14" width="{N*cs+28}" height="{N*cs+28}" rx="16" fill="{P["blue"]}" {st}/><g>{cells}</g><rect x="0" y="0" width="{N*cs}" height="{N*cs}" fill="none" {st}/></svg>'
pieces=[('mouse',3,3),('cat',5,4),('dog',2,1),('bear',5,1)]
ani=''.join(animal(k,cs-4,ox+x*cs+2,oy+y*cs+2) for k,x,y in pieces)
# placed elephant ghost + highlight
ani+=f'<div style="position:absolute;left:{ox+6*cs}px;top:{oy+4*cs}px;width:{cs}px;height:{cs}px;box-sizing:border-box;border:2.5px dashed {INK};border-radius:10px;background:{P["yellow"]}"></div>'
chain=''.join(animal(k,26)+('<b style="font:700 16px Fredoka,sans-serif">›</b>' if i<5 else '') for i,k in enumerate(['mouse','cat','dog','bear','lion','elephant']))
b=f'''<div style="{SCREEN}background:#3a2c24;color:#f1e3c2">
  <div style="position:absolute;left:16px;right:16px;top:20px;display:flex;align-items:center;gap:8px">
    {animal('mouse',34)}<b style="font:700 20px Fredoka,sans-serif;flex:1;white-space:nowrap">Scare-a-Mouse</b>
    <div class="k" style="width:44px;height:40px;display:grid;place-items:center;background:{P["white"]}">{icon("note",22)}</div>
    <div class="k" style="height:40px;padding:0 12px;display:grid;place-items:center;color:#2b1d14;background:{P["yellow"]};font:700 16px Fredoka,sans-serif;white-space:nowrap">Level 47 ▾</div>
  </div>
  <div style="position:absolute;left:16px;right:16px;top:78px;display:flex;align-items:center;justify-content:space-between">
    <b style="font:700 24px Fredoka,sans-serif;color:#f1e3c2">Haystack Hop</b>
    <div class="k" style="padding:2px 12px;border-radius:999px;color:#2b1d14;background:{P["yellow"]};font:700 16px Fredoka,sans-serif">{icon("cheese",20)} 12</div>
  </div>
  <div class="k" style="position:absolute;left:16px;right:16px;top:120px;padding:10px 14px;color:#2b1d14;background:{P["white"]};font:600 16px/1.3 Fredoka,sans-serif">Lions scare bears. Start a chain that ends with the mouse in the hole!</div>
  <div class="k" style="position:absolute;left:16px;right:16px;top:186px;height:44px;display:flex;align-items:center;justify-content:center;gap:4px;color:#2b1d14;background:{P["cream"]}">{chain}</div>
  {board_svg}{ani}
  <div class="k" style="position:absolute;left:16px;right:16px;top:632px;height:74px;display:flex;align-items:center;gap:12px;padding:0 14px;color:#2b1d14;background:{P["white"]}">
    <b style="font:600 15px Fredoka,sans-serif;width:60px;line-height:1.1">Your animals</b>
    <div class="k" style="width:58px;height:58px;display:grid;place-items:center;background:{P["yellow"]};box-shadow:0 3px 0 {INK}">{animal('elephant',46)}</div>
    <div class="k" style="width:58px;height:58px;display:grid;place-items:center;background:{P["cream"]}">{animal('lion',44)}</div>
  </div>
  <div class="btn" style="left:16px;top:728px;width:108px;background:{P["white"]}">Hint · 1 {icon("cheese",20)}</div>
  <div class="btn" style="left:138px;top:728px;width:100px;background:{P["pink"]}">Reset</div>
  <div class="btn" style="left:252px;top:728px;width:122px;background:{P["grass"]}">Go!</div>
</div>'''
boards['Flat-board.dc.html']=('20 · Flat style: the game board',b)
# ---- 2. Room map (Meadow)
def node(n,x,y,state):
    fill={'done':P['yellow'],'cur':P['white'],'next':P['white'],'lock':P['stone']}[state]
    ring='box-shadow:0 0 0 4px '+P['yellow']+';' if state=='cur' else ''
    tick=f'<b style="position:absolute;right:-8px;bottom:-8px;width:20px;height:20px;border:2px solid {INK};border-radius:50%;background:{P["grass"]};font:700 12px Fredoka,sans-serif;display:grid;place-items:center">✓</b>' if state=='done' else ''
    return f'<div style="position:absolute;left:{x-23}px;top:{y-23}px;width:46px;height:46px;box-sizing:border-box;border:2.5px solid {INK};border-radius:50%;background:{fill};display:grid;place-items:center;font:700 16px Fredoka,sans-serif;{ring}">{n}{tick}</div>'
pts=[(110,700),(180,665),(255,625),(290,560),(225,512),(140,478),(92,420),(150,372),(235,340),(290,282)]
def crd(ps):
    d=f'M {ps[0][0]} {ps[0][1]}'
    for i in range(len(ps)-1):
        a=ps[i-1] if i>0 else ps[i]; b=ps[i]; c=ps[i+1]; e=ps[i+2] if i+2<len(ps) else c
        d+=f' C {b[0]+(c[0]-a[0])/6:.1f} {b[1]+(c[1]-a[1])/6:.1f}, {c[0]-(e[0]-b[0])/6:.1f} {c[1]-(e[1]-b[1])/6:.1f}, {c[0]} {c[1]}'
    return d
road=crd([(195,860),(150,780)]+pts+[(240,220),(195,170)])
nodes=''.join(node(21+k,x,y,'done' if k<5 else 'cur' if k==5 else 'next' if k==6 else 'lock') for k,(x,y) in enumerate(pts))
tree=lambda x,y: f'<svg width="90" height="100" style="position:absolute;left:{x}px;top:{y}px;overflow:visible"><rect x="38" y="52" width="14" height="40" rx="4" fill="{P["brown"]}" {st}/><circle cx="45" cy="38" r="34" fill="{P["grass2"]}" {st}/><circle cx="30" cy="30" r="7" fill="{P["red"]}" {st}/><circle cx="58" cy="44" r="7" fill="{P["red"]}" {st}/><circle cx="50" cy="20" r="7" fill="{P["red"]}" {st}/></svg>'
pond=f'<svg width="130" height="80" style="position:absolute;left:220px;top:400px;overflow:visible"><ellipse cx="65" cy="40" rx="60" ry="32" fill="{P["sky"]}" {st}/><path d="M40 40 Q50 34 60 40" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round"/><ellipse cx="88" cy="30" rx="14" ry="9" fill="{P["grass"]}" {st}/></svg>'
flowers=''.join(f'<svg width="26" height="26" style="position:absolute;left:{x}px;top:{y}px;overflow:visible"><circle cx="13" cy="13" r="10" fill="{c}" {st}/><circle cx="13" cy="13" r="4" fill="{P["yellow"]}"/></svg>' for x,y,c in [(30,560,P['pink']),(60,585,P['white']),(330,650,P['pink']),(300,690,P['purple']),(40,330,P['white']),(340,220,P['pink'])])
picnic=f'<svg width="110" height="70" style="position:absolute;left:24px;top:220px;overflow:visible"><rect x="6" y="6" width="96" height="56" rx="6" fill="{P["red"]}" {st} transform="rotate(-6 55 35)"/><path d="M20 10 L20 60 M44 8 L44 62 M68 6 L68 60 M8 26 L100 20 M8 44 L100 40" stroke="#fff" stroke-width="5" transform="rotate(-6 55 35)"/></svg>'
b=f'''<div style="{SCREEN}background:{P["grass"]}">
  <div style="position:absolute;left:0;right:0;top:0;height:60px;display:flex;align-items:center;gap:10px;padding:0 14px;box-sizing:border-box;background:{P["yellow"]};border-bottom:2.5px solid {INK}">
    <div class="k" style="padding:4px 12px;background:{P["white"]};font:700 16px Fredoka,sans-serif">{icon("castle",20)} Castle</div><b style="font:700 22px Fredoka,sans-serif;flex:1">Meadow</b><b style="font:600 15px Fredoka,sans-serif">5/20</b></div>
  <div style="position:absolute;left:0;right:0;top:60px;height:120px;background:{P["sky"]};border-bottom:2.5px solid {INK}">
    <svg width="390" height="120" style="position:absolute;left:0;top:0"><circle cx="340" cy="30" r="20" fill="{P["yellow"]}" {st}/><path d="M-10 120 Q90 40 190 120 Z" fill="{P["grass2"]}" {st}/><path d="M150 120 Q270 50 400 120 Z" fill="{P["grass2"]}" {st}/><rect x="168" y="44" width="54" height="76" rx="27" fill="{P["brown"]}" {st}/><path d="M195 46 L195 120" {st}/></svg></div>
  <svg width="390" height="844" style="position:absolute;left:0;top:0"><path d="{road}" fill="none" stroke="{INK}" stroke-width="36" stroke-linecap="round"/><path d="{road}" fill="none" stroke="{P["tan"]}" stroke-width="32" stroke-linecap="round"/></svg>
  {tree(290,690)}{tree(4,520)}{pond}{flowers}{picnic}{nodes}
  <div style="position:absolute;left:123px;top:432px;animation:bob 1.2s ease-in-out infinite">{animal('mouse',34)}</div>
</div>'''
boards['Flat-room.dc.html']=('21 · Flat style: a room map (Meadow)',b)
# ---- 3. Castle overview
def band(top,label,color,state,sub=''):
    if state=='lock':
        return f'<div class="k" style="position:absolute;left:48px;right:48px;top:{top}px;height:54px;background:{P["stone2"]};display:flex;align-items:center;justify-content:center;font:700 18px Fredoka,sans-serif;color:{INK}">'+icon('lock',26)+'</div>'
    glow=f'box-shadow:0 0 0 4px {P["yellow"]};' if state=='here' else ''
    return f'<div class="k" style="position:absolute;left:48px;right:48px;top:{top}px;height:54px;background:{color};display:flex;align-items:center;gap:10px;padding:0 12px;{glow}"><b style="font:700 18px Fredoka,sans-serif;flex:1;color:#f7efdc">{label}</b><span style="font:600 14px Fredoka,sans-serif;color:#f7efdc">{sub}</span></div>'
b=f'''<div style="{SCREEN}background:{P["navy"]}">
  <svg width="390" height="844" style="position:absolute;left:0;top:0">
    <circle cx="60" cy="70" r="24" fill="{P["yellow"]}" {st}/>
    <path d="M5 40 L12 47 M330 60 L336 66 M200 30 L206 36" stroke="{P["yellow"]}" stroke-width="4" stroke-linecap="round"/>
    <rect x="250" y="70" width="80" height="120" fill="{P["stone"]}" {st}/><path d="M240 72 L290 22 L340 72 Z" fill="{P["red"]}" {st}/>
    <rect x="30" y="150" width="330" height="520" fill="{P["stone"]}" {st}/>
    <path d="M30 150 L30 130 L60 130 L60 150 M90 150 L90 130 L120 130 L120 150 M150 150 L150 130 L180 130 L180 150 M210 150 L210 130 L240 130 L240 150 M270 150 L270 130 L300 130 L300 150 M330 150 L330 130 L360 130 L360 150" fill="{P["stone"]}" {st}/>
    <rect x="0" y="670" width="390" height="30" fill="{P["sky"]}" {st}/><rect x="0" y="700" width="390" height="144" fill="{P["grass"]}" {st}/>
    <rect x="165" y="660" width="60" height="50" fill="{P["brown"]}" {st}/>
    <path d="M290 22 L290 4 L312 10 L290 16" fill="{P["pink"]}" {st}/>
  </svg>
  <b style="position:absolute;left:100px;top:52px;font:700 26px Fredoka,sans-serif;color:#fff">The castle</b>
  <div class="k" style="position:absolute;left:258px;top:110px;width:64px;height:60px;background:{P["stone2"]};display:grid;place-items:center">{icon("lock",26)}</div>
  {band(170,'','', 'lock')}{band(234,'','','lock')}{band(298,'','','lock')}{band(362,'','','lock')}
  {band(426,'Second floor',P['purple'],'open','0/150')}
  {band(490,'First floor',P['orange'],'open',icon('tick',18))}
  {band(580,'Cellars',P['pink'],'open',icon('tick',18))}
  {band(740,'Outside',P['grass2'],'here',icon('tick',18))}
  <div style="position:absolute;left:300px;top:404px;animation:bob 1.2s ease-in-out infinite">{animal('mouse',34)}</div>
</div>'''
b=b.replace(f"{band(740,'Outside',P['grass2'],'here',icon('tick',18))}",f"{band(740,'Outside',P['grass2'],'open',icon('tick',18))}").replace(f"{band(426,'Second floor',P['purple'],'open','0/150')}",f"{band(426,'Second floor',P['purple'],'here','0/150')}")
boards['Flat-castle.dc.html']=('22 · Flat style: the whole castle',b)
# ---- 4. Floor plan
def room(x,y,w,h,name,col,state,ic=''):
    if state=='fog':
        return f'<div class="k" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;background:{P["stone2"]};display:grid;place-items:center;font:700 26px Fredoka,sans-serif;color:#fff">?</div>'
    glow=f'box-shadow:0 0 0 4px {P["yellow"]};' if state=='here' else ''
    return f'<div class="k" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;background:{col};display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;color:#f7efdc;{glow}">{icon(ic,30)}<b style="font:700 17px Fredoka,sans-serif">{name}</b><span style="font:600 13px Fredoka,sans-serif">{icon('tick',14)+' 30/30' if state=='done' else '4/30'}</span></div>'
b=f'''<div style="{SCREEN}background:#3a2c24;color:#f1e3c2">
  <div style="position:absolute;left:16px;right:16px;top:20px;display:flex;gap:10px">
    <div class="btn" style="position:relative;flex:1;background:{P["yellow"]}">{icon("castle",24)}&nbsp;Castle</div></div>
  <b style="position:absolute;left:0;right:0;top:92px;text-align:center;font:700 26px Fredoka,sans-serif;color:#f1e3c2">First floor</b>
  <div class="k" style="position:absolute;left:16px;right:16px;top:140px;height:560px;background:{P["cream"]}"></div>
  <svg width="390" height="844" style="position:absolute;left:0;top:0"><path d="M100 600 L100 290 L260 290 L260 420 L260 530" fill="none" stroke="{INK}" stroke-width="15" stroke-linecap="round" stroke-linejoin="round"/><path d="M100 600 L100 290 L260 290 L260 420 L260 530" fill="none" stroke="{P["tan"]}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></svg>
  {room(32,470,140,210,'Library',P['purple'],'done','book')}
  {room(32,164,140,280,'Study',P['orange'],'here','quill')}
  {room(196,164,162,180,'Great hall','', 'fog')}
  {room(196,362,162,120,'Ballroom','','fog')}
  {room(196,500,162,180,'Gallery','','fog')}
  <div style="position:absolute;left:136px;top:170px;animation:bob 1.2s ease-in-out infinite">{animal('mouse',30)}</div>
  <div class="btn" style="left:16px;top:722px;width:160px;background:{P["white"]}">{icon("down",20)}&nbsp;Cellars</div>
  <div class="btn" style="left:214px;top:722px;width:160px;background:{P["stone2"]}">{icon("lock",20)}&nbsp;Upstairs</div>
</div>'''
boards['Flat-floor.dc.html']=('23 · Flat style: a floor plan',b)
import os
base='/home/claude/mockups/project'
for fn,(t,body) in boards.items():
    open(f'{base}/{fn}','w').write(HEAD%t+body+'\n'+TAIL)
c=json.load(open(f'{base}/canvas.json'))
y=max(v['y'] for v in c['boards'].values())+844+400
for k,fn in enumerate(boards):
    old=c['boards'].get(fn)
    c['boards'][fn]=dict(old, title=boards[fn][0]) if old else {'x':470*k,'y':y,'w':390,'h':844,'title':boards[fn][0]}
    if fn not in c['order']: c['order'].append(fn)
c['notes'].setdefault('t5',{'x':0,'y':y-260,'text':'Flat style: thin outlines, medieval colours','kind':'title1','maxW':1800})
json.dump(c,open(f'{base}/canvas.json','w'),ensure_ascii=False)
print('ok', list(boards))
