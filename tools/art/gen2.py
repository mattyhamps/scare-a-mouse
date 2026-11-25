import json, math
src=open('./gen.py').read()
exec(src[:src.index("boards={}")])
HEAD2=HEAD.replace('family=Fredoka:wght@500;600;700','family=Fredoka:wght@500;600;700&amp;family=MedievalSharp&amp;family=Almendra:wght@700&amp;family=IM+Fell+English+SC')
C=dict(grey='#b9b2a6',rose='#d98b8b',ochre='#d98a3a',tan=P['tan'],brown=P['brown'],gold=P['yellow'],rust=P['orange'],slate='#8f9cb8',slate2='#6f7c99',cream='#f7efdc',ink=INK)
def svg(inner,size,extra=''): return f'<svg viewBox="0 0 100 100" width="{size}" height="{size}" style="overflow:visible{extra}">{inner}</svg>'
def oeyes(x1,x2,y,rx=5,ry=6.5): return f'<ellipse cx="{x1}" cy="{y}" rx="{rx}" ry="{ry}" fill="{INK}"/><ellipse cx="{x2}" cy="{y}" rx="{rx}" ry="{ry}" fill="{INK}"/><circle cx="{x1+1.8}" cy="{y-2.4}" r="2" fill="#fff"/><circle cx="{x2+1.8}" cy="{y-2.4}" r="2" fill="#fff"/>'
cheeks=lambda x1,x2,y: f'<ellipse cx="{x1}" cy="{y}" rx="6" ry="3.5" fill="{C["rose"]}" opacity=".7"/><ellipse cx="{x2}" cy="{y}" rx="6" ry="3.5" fill="{C["rose"]}" opacity=".7"/>'
# ---------- Option A: storybook heads (round, big eyes, blush, no whiskers)
A={
'mouse': f'<circle cx="24" cy="34" r="20" fill="{C["grey"]}" {st}/><circle cx="76" cy="34" r="20" fill="{C["grey"]}" {st}/><circle cx="24" cy="34" r="11" fill="{C["rose"]}"/><circle cx="76" cy="34" r="11" fill="{C["rose"]}"/><ellipse cx="50" cy="62" rx="29" ry="26" fill="{C["grey"]}" {st}/>{oeyes(40,60,58)}{cheeks(32,68,69)}<ellipse cx="50" cy="71" rx="4.5" ry="3.5" fill="{C["rose"]}" {st}/>',
'cat': f'<path d="M20 50 L24 14 L44 34 Z" fill="{C["ochre"]}" {st}/><path d="M80 50 L76 14 L56 34 Z" fill="{C["ochre"]}" {st}/><path d="M26 42 L27 24 L37 34 Z" fill="{C["rose"]}"/><path d="M74 42 L73 24 L63 34 Z" fill="{C["rose"]}"/><ellipse cx="50" cy="58" rx="33" ry="29" fill="{C["ochre"]}" {st}/>{oeyes(39,61,56)}{cheeks(30,70,67)}<path d="M46 65 L54 65 L50 69 Z" fill="{C["rose"]}"/><path d="M44 72 Q47 75 50 71 Q53 75 56 72" fill="none" {st}/>',
'dog': f'<ellipse cx="50" cy="56" rx="31" ry="30" fill="{C["tan"]}" {st}/><path d="M24 30 C6 32 6 66 20 70 C30 62 30 40 26 30 Z" fill="{C["brown"]}" {st}/><path d="M76 30 C94 32 94 66 80 70 C70 62 70 40 74 30 Z" fill="{C["brown"]}" {st}/>{oeyes(40,60,52)}{cheeks(30,70,64)}<ellipse cx="50" cy="65" rx="8" ry="5.5" fill="{INK}"/><path d="M46 74 Q50 86 54 74 Z" fill="{C["rose"]}" {st}/>',
'bear': f'<circle cx="24" cy="28" r="14" fill="{C["brown"]}" {st}/><circle cx="76" cy="28" r="14" fill="{C["brown"]}" {st}/><circle cx="24" cy="28" r="6" fill="{C["tan"]}"/><circle cx="76" cy="28" r="6" fill="{C["tan"]}"/><circle cx="50" cy="56" r="33" fill="{C["brown"]}" {st}/><ellipse cx="50" cy="69" rx="15" ry="11" fill="{C["tan"]}" {st}/>{oeyes(38,62,51)}<ellipse cx="50" cy="64" rx="6.5" ry="4.5" fill="{INK}"/>',
'lion': ''.join(f'<ellipse cx="{50+34*math.cos(a*math.pi/5):.1f}" cy="{54+34*math.sin(a*math.pi/5):.1f}" rx="15" ry="15" fill="{C["rust"]}" {st}/>' for a in range(10)) + f'<circle cx="50" cy="54" r="34" fill="{C["rust"]}"/><circle cx="50" cy="56" r="27" fill="{C["gold"]}" {st}/><circle cx="31" cy="34" r="6" fill="{C["gold"]}" {st}/><circle cx="69" cy="34" r="6" fill="{C["gold"]}" {st}/>{oeyes(41,59,52)}{cheeks(33,67,63)}<path d="M45 61 L55 61 L50 66 Z" fill="{INK}"/>',
'elephant': f'<path d="M26 28 C0 26 2 76 28 72 C32 58 34 40 26 28 Z" fill="{C["slate2"]}" {st}/><path d="M74 28 C100 26 98 76 72 72 C68 58 66 40 74 28 Z" fill="{C["slate2"]}" {st}/><path d="M30 28 C18 32 18 62 30 64 Z" fill="{C["rose"]}" opacity=".6"/><path d="M70 28 C82 32 82 62 70 64 Z" fill="{C["rose"]}" opacity=".6"/><ellipse cx="50" cy="48" rx="26" ry="27" fill="{C["slate"]}" {st}/><path d="M43 62 C43 78 44 88 56 90 C62 90 64 84 58 82 C54 82 56 74 57 62 Z" fill="{C["slate"]}" {st}/>{oeyes(40,60,45)}{cheeks(33,67,56)}',
}
# ---------- Option B: whole animals, sitting or standing, side-ish view
B={
'mouse': f'<path d="M14 74 C2 78 2 92 18 90" fill="none" {st}/><ellipse cx="44" cy="72" rx="28" ry="18" fill="{C["grey"]}" {st}/><circle cx="70" cy="56" r="16" fill="{C["grey"]}" {st}/><circle cx="64" cy="40" r="11" fill="{C["grey"]}" {st}/><circle cx="64" cy="40" r="5.5" fill="{C["rose"]}"/><circle cx="74" cy="54" r="3.6" fill="{INK}"/><circle cx="86" cy="60" r="3.5" fill="{C["rose"]}" {st}/><path d="M34 88 L32 94 M52 88 L54 94" {st}/>',
'cat': f'<path d="M70 86 C92 86 94 64 82 60" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/><path d="M70 86 C92 86 94 64 82 60" fill="none" stroke="{C["ochre"]}" stroke-width="5" stroke-linecap="round"/><path d="M30 92 C24 70 30 50 50 48 C70 50 76 70 70 92 Z" fill="{C["ochre"]}" {st}/><path d="M34 30 L36 8 L46 20 Z M66 30 L64 8 L54 20 Z" fill="{C["ochre"]}" {st}/><circle cx="50" cy="32" r="18" fill="{C["ochre"]}" {st}/><circle cx="43" cy="31" r="3.4" fill="{INK}"/><circle cx="57" cy="31" r="3.4" fill="{INK}"/><path d="M47 38 L53 38 L50 41 Z" fill="{C["rose"]}"/><path d="M40 70 L40 92 M60 70 L60 92" {st}/>',
'dog': f'<path d="M78 66 C90 58 92 48 88 44" fill="none" {st}/><path d="M26 92 C22 72 30 56 50 56 C70 56 80 72 76 92 Z" fill="{C["tan"]}" {st}/><ellipse cx="46" cy="34" rx="20" ry="18" fill="{C["tan"]}" {st}/><path d="M28 24 C16 28 18 50 26 52 C32 46 32 32 30 24 Z" fill="{C["brown"]}" {st}/><ellipse cx="64" cy="40" rx="12" ry="9" fill="{C["tan"]}" {st}/><circle cx="74" cy="38" r="4" fill="{INK}"/><circle cx="50" cy="30" r="3.4" fill="{INK}"/><path d="M40 72 L40 92 M60 72 L60 92" {st}/>',
'bear': f'<path d="M14 74 C14 50 34 40 56 42 C76 44 84 58 82 76 L82 90 L70 90 L70 80 L34 80 L34 90 L22 90 L22 80 C16 80 14 78 14 74 Z" fill="{C["brown"]}" {st}/><circle cx="76" cy="42" r="17" fill="{C["brown"]}" {st}/><circle cx="70" cy="26" r="6" fill="{C["brown"]}" {st}/><ellipse cx="88" cy="48" rx="8" ry="6" fill="{C["tan"]}" {st}/><circle cx="94" cy="46" r="2.6" fill="{INK}"/><circle cx="78" cy="38" r="3.2" fill="{INK}"/>',
'lion': f'<path d="M10 66 C2 60 4 52 10 54" fill="none" {st}/><circle cx="8" cy="54" r="4" fill="{C["rust"]}" {st}/><path d="M14 70 C14 54 30 48 50 50 C66 52 72 60 72 72 L72 90 L62 90 L62 80 L28 80 L28 90 L18 90 L18 80 C14 80 14 76 14 70 Z" fill="{C["gold"]}" {st}/>' + ''.join(f'<circle cx="{70+18*math.cos(a*math.pi/4):.1f}" cy="{44+18*math.sin(a*math.pi/4):.1f}" r="10" fill="{C["rust"]}" {st}/>' for a in range(8)) + f'<circle cx="70" cy="44" r="18" fill="{C["rust"]}"/><circle cx="72" cy="46" r="13" fill="{C["gold"]}" {st}/><circle cx="76" cy="43" r="2.8" fill="{INK}"/><path d="M82 50 L86 48" {st}/>',
'elephant': f'<path d="M8 50 C8 30 30 24 52 28 C70 30 76 44 74 60 L74 90 L62 90 L62 74 L28 74 L28 90 L16 90 L16 70 C10 66 8 58 8 50 Z" fill="{C["slate"]}" {st}/><path d="M60 30 C82 18 98 36 92 54 C90 64 84 74 88 86 C90 92 82 94 80 88 C76 78 80 66 76 58 Z" fill="{C["slate"]}" {st}/><path d="M56 36 C44 36 40 56 52 64 C62 60 64 42 56 36 Z" fill="{C["slate2"]}" {st}/><circle cx="76" cy="40" r="3.2" fill="{INK}"/><path d="M8 50 L2 58" {st}/>',
}
# ---------- Option C: heraldic profile heads (flat, two-tone, angular, facing right like a coat of arms)
C2={
'mouse': f'<path d="M14 64 C14 40 40 34 60 44 L90 62 C92 64 90 68 86 68 L60 74 C40 80 14 80 14 64 Z" fill="{C["grey"]}" {st}/><circle cx="42" cy="34" r="16" fill="{C["grey"]}" {st}/><circle cx="42" cy="34" r="8" fill="{C["rose"]}"/><circle cx="62" cy="54" r="4" fill="{INK}"/><circle cx="90" cy="64" r="4" fill="{C["rose"]}" {st}/><path d="M78 68 L96 74 M76 70 L92 82" {st} fill="none"/>',
'cat': f'<path d="M18 80 L22 38 L32 12 L46 32 L60 30 L72 12 L78 36 L86 52 L94 60 L86 70 L70 76 L50 86 Z" fill="{C["ochre"]}" {st}/><path d="M32 22 L36 34 L42 32 Z M70 22 L68 34 L74 36 Z" fill="{C["rose"]}"/><path d="M62 48 L74 46 L70 52 Z" fill="{INK}"/><path d="M90 62 L86 66 L94 66 Z" fill="{C["rose"]}" {st}/><path d="M40 52 L52 58 M38 62 L52 64" stroke="#b5732e" stroke-width="5" stroke-linecap="round"/>',
'dog': f'<path d="M16 86 L18 46 C20 26 40 18 56 24 L70 32 L94 44 C98 48 96 56 90 58 L66 62 L52 84 Z" fill="{C["tan"]}" {st}/><path d="M36 26 C20 30 18 62 30 70 C40 62 44 40 42 28 Z" fill="{C["brown"]}" {st}/><ellipse cx="92" cy="48" rx="6" ry="5" fill="{INK}"/><path d="M58 36 L66 34 L62 40 Z" fill="{INK}"/><path d="M78 58 L86 72 L72 64 Z" fill="{C["rose"]}" {st}/>',
'bear': f'<path d="M14 84 L16 46 C18 22 46 14 62 26 L80 38 C92 40 96 48 92 56 L70 64 L56 84 Z" fill="{C["brown"]}" {st}/><circle cx="38" cy="22" r="10" fill="{C["brown"]}" {st}/><path d="M74 44 C86 44 94 48 92 56 L74 60 Z" fill="{C["tan"]}" {st}/><ellipse cx="92" cy="50" rx="5" ry="4" fill="{INK}"/><path d="M58 38 L66 36 L62 42 Z" fill="{INK}"/>',
'lion': f'<path d="M8 90 L14 60 L6 50 L18 44 L12 30 L26 30 L24 16 L38 22 L44 8 L52 20 L64 12 L66 26 L58 40 L40 50 L36 70 L46 90 Z" fill="{C["rust"]}" {st}/><path d="M40 50 L58 40 L66 26 L80 34 L94 48 C96 54 92 58 88 58 L70 62 L60 78 L46 90 L36 70 Z" fill="{C["gold"]}" {st}/><path d="M66 38 L76 38 L72 44 Z" fill="{INK}"/><ellipse cx="92" cy="50" rx="4" ry="3.5" fill="{INK}"/><path d="M74 60 L82 70 L70 64 Z" fill="{C["red"] if "red" in C else "#8e2a2f"}" {st}/>',
'elephant': f'<path d="M12 86 L14 44 C16 20 46 12 64 24 C76 32 80 44 80 56 C80 70 84 80 92 82 C96 84 94 92 88 90 C74 88 68 78 66 66 L58 86 Z" fill="{C["slate"]}" {st}/><path d="M24 30 C10 40 12 70 30 74 C42 64 44 40 36 28 Z" fill="{C["slate2"]}" {st}/><path d="M56 34 L64 32 L60 38 Z" fill="{INK}"/><path d="M66 60 L78 70" stroke="{C["cream"]}" stroke-width="6" stroke-linecap="round"/>',
}
boards={}
SC=SCREEN
def crd(ps):
    d=f'M {ps[0][0]} {ps[0][1]}'
    for i in range(len(ps)-1):
        a=ps[i-1] if i>0 else ps[i]; b=ps[i]; c=ps[i+1]; e=ps[i+2] if i+2<len(ps) else c
        d+=f' C {b[0]+(c[0]-a[0])/6:.1f} {b[1]+(c[1]-a[1])/6:.1f}, {c[0]-(e[0]-b[0])/6:.1f} {c[1]-(e[1]-b[1])/6:.1f}, {c[0]} {c[1]}'
    return d
# ---------- 24 fonts
def fontcard(top,label,fam,size1,size2,note):
    return f'''<div class="k" style="position:absolute;left:16px;right:16px;top:{top}px;height:226px;background:{P["cream"]};color:{INK};padding:14px 16px;box-sizing:border-box">
      <div style="font:700 13px Fredoka,sans-serif;color:{P["orange"]};letter-spacing:.5px">{label}</div>
      <div style="font-family:{fam};font-weight:{'700' if 'Almendra' in fam else '400'};font-size:{size1}px;line-height:1.05;margin-top:6px">Scare-a-Mouse</div>
      <div style="font-family:{fam};font-weight:{'700' if 'Almendra' in fam else '400'};font-size:{size2}px;margin-top:8px">Haystack Hop · The castle</div>
      <div style="font:600 15px/1.35 Fredoka,sans-serif;margin-top:10px">Lions scare bears. Start a chain that ends with the mouse in the hole! <span style="color:{P["brown"]}">(small text stays Fredoka)</span></div>
      <div style="position:absolute;right:12px;bottom:10px;font:600 12px Fredoka,sans-serif;color:{P["brown"]}">{note}</div></div>'''
b=f'''<div style="{SC}background:#3a2c24">
  <b style="position:absolute;left:0;right:0;top:18px;text-align:center;font:700 22px Fredoka,sans-serif;color:{P["cream"]}">Title fonts</b>
  {fontcard(62,'A · MEDIEVALSHARP',"'MedievalSharp',serif",40,24,'storybook, playful')}
  {fontcard(302,'B · ALMENDRA',"'Almendra',serif",42,25,'elegant, fairy-tale')}
  {fontcard(542,'C · IM FELL ENGLISH SC',"'IM Fell English SC',serif",36,23,'old printed book')}
  <div style="position:absolute;left:0;right:0;top:786px;text-align:center;font:600 14px Fredoka,sans-serif;color:{P["cream2"]}">Titles, room names and floor names use the title font</div>
</div>'''
boards['Med-fonts.dc.html']=('24 · Medieval: title font options',b)
# ---------- 25 win screen
N=7; cs=46; ox=(390-N*cs)//2; oy=200
cells=''.join(f'<rect x="{x*cs}" y="{y*cs}" width="{cs}" height="{cs}" fill="{P["cream"] if (x+y)%2 else P["cream2"]}"/>' for y in range(N) for x in range(N))
bd=f'<svg width="{N*cs}" height="{N*cs}" style="position:absolute;left:{ox}px;top:{oy}px;overflow:visible"><rect x="-14" y="-14" width="{N*cs+28}" height="{N*cs+28}" rx="12" fill="{P["blue"]}" {st}/>{cells}<rect x="0" y="0" width="{N*cs}" height="{N*cs}" fill="none" {st}/></svg>'
ribbon=f'<svg width="300" height="64" style="position:absolute;left:45px;top:226px;overflow:visible"><path d="M10 14 L40 14 L40 54 L22 44 L4 54 Z M290 14 L260 14 L260 54 L278 44 L296 54 Z" fill="#6e1f24" {st}/><rect x="30" y="4" width="240" height="44" rx="4" fill="{P["red"]}" {st}/></svg><b style="position:absolute;left:45px;width:300px;top:236px;text-align:center;font:700 24px Fredoka,sans-serif;color:{P["cream"]}">Mouse escaped!</b>'
b=f'''<div style="{SC}background:#3a2c24">{bd}
  <div style="position:absolute;inset:0;background:rgba(30,20,14,.62)"></div>
  <div class="k" style="position:absolute;left:30px;right:30px;top:250px;height:400px;background:{P["cream"]}"></div>
  {ribbon}
  <div style="position:absolute;left:0;right:0;top:300px;display:flex;justify-content:center;align-items:flex-end;gap:2px">{svg(A["mouse"],86)}<svg width="70" height="40" viewBox="0 0 70 40"><ellipse cx="35" cy="26" rx="32" ry="13" fill="{INK}"/></svg></div>
  <div style="position:absolute;left:0;right:0;top:404px;text-align:center;font:600 17px Fredoka,sans-serif;color:{INK}">Level 47 solved</div>
  <div class="k" style="position:absolute;left:122px;top:436px;width:146px;height:40px;border-radius:999px;background:{P["yellow"]};display:flex;align-items:center;justify-content:center;gap:6px;font:700 18px Fredoka,sans-serif;color:{INK}">+3 {icon("cheese",24)}</div>
  <div class="btn" style="left:54px;top:500px;width:282px;background:{P["grass"]};color:{P["cream"]}">Next level</div>
  <div class="btn" style="left:54px;top:566px;width:134px;background:{P["white"]};font-size:16px">All levels</div>
  <div class="btn" style="left:202px;top:566px;width:134px;background:{P["purple"]};color:{P["cream"]};font-size:16px"><svg viewBox="0 0 100 100" width="18" height="18"><path d="M48 20 L14 50 L48 80 Z M86 20 L52 50 L86 80 Z" fill="#f7efdc" stroke="#2b1d14" stroke-width="6" stroke-linejoin="round"/></svg> Replay</div>
</div>'''
boards['Med-win.dc.html']=('25 · Medieval: the win screen',b)
# ---------- 26 how to play card
chainrow=lambda: ''.join(f'<div style="display:flex;align-items:center;gap:6px;justify-content:center;margin:4px 0">{svg(A[a],46)}<b style="font:700 14px Fredoka,sans-serif;color:{P["yellow"]}">scares</b>{svg(A[b2],46)}</div>' for a,b2 in [('cat','mouse'),('dog','cat'),('bear','dog')])
b=f'''<div style="{SC}background:#3a2c24">
  <div style="position:absolute;inset:0;background:rgba(30,20,14,.45)"></div>
  <div class="k" style="position:absolute;left:24px;right:24px;top:120px;height:600px;background:{P["cream"]};color:{INK}"></div>
  <div class="k" style="position:absolute;left:48px;right:48px;top:146px;height:200px;background:{P["navy"]};display:flex;flex-direction:column;justify-content:center">{chainrow()}</div>
  <b style="position:absolute;left:40px;right:40px;top:366px;text-align:center;font:700 25px/1.15 Fredoka,sans-serif;color:{INK}">Animals scare each other</b>
  <div style="position:absolute;left:46px;right:46px;top:450px;text-align:center;font:600 16px/1.45 Fredoka,sans-serif;color:{INK}">Each animal scares just one other. A scared animal runs straight away, and it can scare the next animal on its way.</div>
  <div style="position:absolute;left:0;right:0;top:556px;display:flex;justify-content:center;gap:8px">{''.join(f'<b style="width:10px;height:10px;border-radius:50%;border:2px solid {INK};background:{P["yellow"] if k==1 else P["cream"]}"></b>' for k in range(4))}</div>
  <div class="btn" style="left:54px;top:588px;width:282px;background:{P["yellow"]}">Next</div>
  <div style="position:absolute;left:0;right:0;top:658px;text-align:center;font:600 16px Fredoka,sans-serif;color:{P["brown"]}">Skip</div>
</div>'''
boards['Med-howto.dc.html']=('26 · Medieval: a how-to-play card',b)
# ---------- 27 indoor room: Kitchens
def node(n,x,y,state):
    fill={'done':P['yellow'],'cur':P['white'],'next':P['white'],'lock':P['stone']}[state]
    ring='box-shadow:0 0 0 4px '+P['yellow']+';' if state=='cur' else ''
    tick=f'<b style="position:absolute;right:-7px;bottom:-7px;width:18px;height:18px;border:2px solid {INK};border-radius:50%;background:{P["grass"]};display:grid;place-items:center">{icon("tick",11)}</b>' if state=='done' else ''
    return f'<div style="position:absolute;left:{x-22}px;top:{y-22}px;width:44px;height:44px;box-sizing:border-box;border:2.5px solid {INK};border-radius:50%;background:{fill};display:grid;place-items:center;font:700 15px Fredoka,sans-serif;color:{INK};{ring}">{n}{tick}</div>'
pts=[(112,720),(185,690),(262,650),(290,585),(222,540),(132,505),(94,445),(152,398),(240,366),(290,302)]
road=crd([(195,860),(150,790)]+pts+[(250,240),(195,190)])
nodes=''.join(node(171+k,x,y,'done' if k<6 else 'cur' if k==6 else 'next' if k==7 else 'lock') for k,(x,y) in enumerate(pts))
def hearth(x,y): return f'<svg width="130" height="120" style="position:absolute;left:{x}px;top:{y}px;overflow:visible"><rect x="4" y="4" width="122" height="112" rx="4" fill="{P["stone"]}" {st}/><path d="M4 30 L126 30 M4 58 L126 58 M4 86 L126 86 M40 4 L40 30 M90 4 L90 30 M24 30 L24 58 M106 30 L106 58" stroke="{INK}" stroke-width="1.6"/><path d="M26 116 L26 70 C26 40 104 40 104 70 L104 116 Z" fill="#3a2418" {st}/><path d="M50 116 C46 100 56 92 60 84 C62 96 74 98 70 116 Z" fill="{P["yellow"]}" {st}/><path d="M58 116 C56 106 62 102 64 96 C66 104 72 108 68 116 Z" fill="{P["orange"]}"/><ellipse cx="65" cy="80" rx="24" ry="16" fill="#3e3a44" {st}/><path d="M44 74 L86 74" {st}/><circle cx="56" cy="58" r="6" fill="{P["cream"]}" {st} opacity=".9"/><circle cx="70" cy="50" r="5" fill="{P["cream"]}" {st} opacity=".8"/></svg>'
def table(x,y): return f'<svg width="130" height="90" style="position:absolute;left:{x}px;top:{y}px;overflow:visible"><rect x="12" y="2" width="106" height="10" rx="3" fill="{P["brown"]}" {st}/><rect x="4" y="18" width="122" height="52" rx="6" fill="#9a6338" {st}/><path d="M4 36 L126 36 M4 54 L126 54" stroke="{INK}" stroke-width="1.6"/><rect x="12" y="76" width="106" height="10" rx="3" fill="{P["brown"]}" {st}/><ellipse cx="34" cy="38" rx="14" ry="7" fill="{P["yellow"]}" {st}/><path d="M70 30 L92 30 L86 46 L76 46 Z" fill="{P["cream"]}" {st}/><path d="M96 46 L118 46 L118 30 Z" fill="{P["yellow"]}" {st}/><circle cx="56" cy="58" r="7" fill="{P["red"]}" {st}/></svg>'
def sacks(x,y): return f'<svg width="120" height="90" style="position:absolute;left:{x}px;top:{y}px;overflow:visible">' + ''.join(f'<path d="M{a} 84 C{a-8} 84 {a-10} 50 {a+6} 42 L{a+4} 34 L{a+24} 34 L{a+22} 42 C{a+38} 50 {a+36} 84 {a+28} 84 Z" fill="{P["tan"]}" {st}/><path d="M{a+4} 40 L{a+24} 40" stroke="{P["red"]}" stroke-width="3"/>' for a in (8,46,84)) + '</svg>'
def barrels(x,y): return f'<svg width="110" height="90" style="position:absolute;left:{x}px;top:{y}px;overflow:visible">' + ''.join(f'<rect x="{a}" y="{t}" width="32" height="42" rx="10" fill="#9a6338" {st}/><path d="M{a} {t+12} L{a+32} {t+12} M{a} {t+30} L{a+32} {t+30}" stroke="{INK}" stroke-width="2.4"/>' for a,t in ((8,44),(42,44),(76,44),(25,4),(59,4))) + '</svg>'
torch=lambda x,y: f'<svg width="24" height="40" style="position:absolute;left:{x}px;top:{y}px;overflow:visible"><path d="M8 18 L16 18 L14 38 L10 38 Z" fill="{P["brown"]}" {st}/><path d="M12 2 C4 10 6 18 12 18 C18 18 20 10 12 2 Z" fill="{P["yellow"]}" {st}/></svg>'
pan=lambda x,y: f'<svg width="30" height="44" style="position:absolute;left:{x}px;top:{y}px;overflow:visible"><path d="M15 0 L15 18" {st}/><circle cx="15" cy="30" r="12" fill="#3e3a44" {st}/></svg>'
b=f'''<div style="{SC}background:repeating-conic-gradient(#b5653a 0 25%,#9e5530 0 50%) 0 0/44px 44px">
  <div style="position:absolute;left:0;right:0;top:0;height:56px;display:flex;align-items:center;gap:10px;padding:0 14px;box-sizing:border-box;background:{P["yellow"]};border-bottom:2.5px solid {INK}">
    <div class="k" style="padding:4px 10px;background:{P["white"]};font:700 15px Fredoka,sans-serif;display:flex;gap:6px;align-items:center">{icon("castle",18)} Castle</div><b style="font:700 21px Fredoka,sans-serif;flex:1">Kitchens</b><b style="font:600 14px Fredoka,sans-serif">7/30</b></div>
  <div style="position:absolute;left:0;right:0;top:56px;height:150px;background:{P["stone"]};border-bottom:2.5px solid {INK}">
    <svg width="390" height="150" style="position:absolute;left:0;top:0"><path d="M0 40 L390 40 M0 80 L390 80 M0 120 L390 120 M60 0 L60 40 M160 0 L160 40 M270 0 L270 40 M110 40 L110 80 M330 40 L330 80 M30 80 L30 120 M240 80 L240 120" stroke="{INK}" stroke-width="1.4" opacity=".55"/>
    <rect x="30" y="20" width="44" height="62" rx="22" fill="{P["sky"]}" {st}/><path d="M52 20 L52 82 M30 50 L74 50" {st}/><rect x="316" y="20" width="44" height="62" rx="22" fill="{P["sky"]}" {st}/><path d="M338 20 L338 82 M316 50 L360 50" {st}/>
    <path d="M100 10 L290 10" {st}/><path d="M168 90 L168 150 L222 150 L222 90 C222 62 168 62 168 90 Z" fill="#5a3a24" {st}/><path d="M195 70 L195 150" {st}/><circle cx="206" cy="116" r="3" fill="{P["yellow"]}" {st}/></svg>
    {pan(118,10)}{pan(150,10)}{pan(236,10)}{pan(266,10)}</div>
  <div style="position:absolute;left:0;top:206px;bottom:0;width:10px;background:{P["stone2"]};border-right:2.5px solid {INK}"></div><div style="position:absolute;right:0;top:206px;bottom:0;width:10px;background:{P["stone2"]};border-left:2.5px solid {INK}"></div>
  <svg width="390" height="844" style="position:absolute;left:0;top:0"><path d="{road}" fill="none" stroke="{INK}" stroke-width="36" stroke-linecap="round"/><path d="{road}" fill="none" stroke="{P["cream"]}" stroke-width="31" stroke-linecap="round"/><path d="{road}" fill="none" stroke="{P["cream2"]}" stroke-width="3" stroke-dasharray="8 10" stroke-linecap="round"/></svg>
  {hearth(236,410)}{table(14,550)}{sacks(240,700)}{barrels(18,250)}
  {torch(12,330)}{torch(356,480)}{torch(12,640)}
  {nodes}
  <div style="position:absolute;left:78px;top:398px">{svg(A["mouse"],36)}</div>
</div>'''
boards['Med-kitchens.dc.html']=('27 · Medieval: an indoor room (Kitchens)',b)
# ---------- 28 art sheet (wide)
def row(top,label,sub,S):
    cellsr=''.join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:6px">{svg(S[k],100)}<span style="font:600 13px Fredoka,sans-serif;color:{P["cream2"]}">{k}</span></div>' for k in ['mouse','cat','dog','bear','lion','elephant'])
    return f'''<div style="position:absolute;left:24px;top:{top}px;font:700 20px Fredoka,sans-serif;color:{P["cream"]}">{label} <span style="font:600 14px Fredoka,sans-serif;color:{P["cream2"]}">{sub}</span></div>
      <div class="k" style="position:absolute;left:24px;right:24px;top:{top+34}px;height:150px;background:{P["navy"]};display:flex;justify-content:space-around;align-items:center">{cellsr}</div>'''
objs=f'''<div style="position:absolute;left:24px;top:664px;font:700 20px Fredoka,sans-serif;color:{P["cream"]}">Room objects <span style="font:600 14px Fredoka,sans-serif;color:{P["cream2"]}">same style, replacing the emoji</span></div>
  <div class="k" style="position:absolute;left:24px;right:24px;top:698px;height:130px;background:repeating-conic-gradient(#b5653a 0 25%,#9e5530 0 50%) 0 0/40px 40px;overflow:hidden"></div>'''
b=f'''<div style="width:780px;height:844px;box-sizing:border-box;position:relative;overflow:hidden;font-family:Fredoka,sans-serif;background:#3a2c24">
  <b style="position:absolute;left:24px;top:16px;font:700 24px Fredoka,sans-serif;color:{P["cream"]}">The animals: three directions</b>
  {row(56,'A · Storybook heads','round faces, big eyes, rosy cheeks',A)}
  {row(258,'B · Whole animals','sitting and standing, more character',B)}
  {row(460,'C · Heraldic','profiles like a coat of arms, more medieval',C2)}
  {objs}
  {hearth(40,704).replace('width="130" height="120"','width="104" height="96" viewBox="0 0 130 120"')}{table(170,716).replace('width="130" height="90"','width="117" height="81" viewBox="0 0 130 90"')}{sacks(310,722).replace('width="120" height="90"','width="108" height="81" viewBox="0 0 120 90"')}{barrels(440,722).replace('width="110" height="90"','width="99" height="81" viewBox="0 0 110 90"')}{torch(570,740)}{pan(610,730)}{torch(650,740)}{pan(690,730)}
</div>'''
boards['Med-art.dc.html']=('28 · Medieval: art sheet (animals A/B/C, objects)',b)
base='/home/claude/mockups/project'
for fn,(t,body) in boards.items():
    open(f'{base}/{fn}','w').write(HEAD2%t+body+'\n'+TAIL.replace('{"width":390,"height":844}','{"width":780,"height":844}' if fn=='Med-art.dc.html' else '{"width":390,"height":844}'))
c=json.load(open(f'{base}/canvas.json'))
for fn in boards: c['boards'].pop(fn,None); c['order']=[o for o in c['order'] if o!=fn]
y=max(v['y'] for k,v in c['boards'].items())+844+400
x=0
for fn in boards:
    w=780 if fn=='Med-art.dc.html' else 390
    c['boards'][fn]={'x':x,'y':y,'w':w,'h':844,'title':boards[fn][0]}; c['order'].append(fn); x+=w+80
c['notes']['t6']={'x':0,'y':y-260,'text':'Medieval style: fonts, menus, an indoor room, the art sheet','kind':'title1','maxW':2400}
json.dump(c,open(f'{base}/canvas.json','w'),ensure_ascii=False)
print('ok')
