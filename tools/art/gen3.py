import json, math
src=open('./gen2.py').read()
exec(src[:src.index("\nboards={}\nSC=SCREEN")])
thin=f'stroke="{INK}" stroke-width="1.8" stroke-linecap="round" fill="none"'
def EYES(style,x1,x2,y):
    if style=='big':
        return ''.join(f'<ellipse cx="{x}" cy="{y}" rx="6.2" ry="7.6" fill="{INK}"/><circle cx="{x+2}" cy="{y-2.8}" r="2.4" fill="#fff"/><circle cx="{x-2}" cy="{y+3}" r="1.1" fill="#fff"/>' for x in (x1,x2))
    if style=='dot':
        return ''.join(f'<circle cx="{x}" cy="{y}" r="3.8" fill="{INK}"/><circle cx="{x+1.2}" cy="{y-1.3}" r="1.2" fill="#fff"/>' for x in (x1,x2)) + f'<path d="M{x1-6} {y-9} Q{x1} {y-12} {x1+5} {y-9} M{x2-5} {y-9} Q{x2} {y-12} {x2+6} {y-9}" {thin} stroke-width="2.4"/>'
    if style=='button':
        return ''.join(f'<circle cx="{x}" cy="{y}" r="7.4" fill="#fff" {st}/><circle cx="{x+1}" cy="{y+0.5}" r="4" fill="{INK}"/><circle cx="{x+2.2}" cy="{y-1}" r="1.3" fill="#fff"/>' for x in (x1,x2))
def wh(x,y,side):  # three whiskers
    s=1 if side>0 else -1
    return f'<path d="M{x} {y-3} L{x+16*s} {y-7} M{x} {y} L{x+18*s} {y} M{x} {y+3} L{x+16*s} {y+7}" {thin}/>'
def heads(es):
    C_=C
    return {
'mouse': f'<circle cx="24" cy="34" r="20" fill="{C_["grey"]}" {st}/><circle cx="76" cy="34" r="20" fill="{C_["grey"]}" {st}/><circle cx="24" cy="35" r="11" fill="{C_["rose"]}"/><circle cx="76" cy="35" r="11" fill="{C_["rose"]}"/><path d="M18 30 Q24 26 30 31 M70 31 Q76 26 82 30" {thin}/>'
         f'<ellipse cx="50" cy="62" rx="29" ry="26" fill="{C_["grey"]}" {st}/><path d="M44 37 Q46 32 50 36 Q53 31 56 37" {thin} stroke-width="2.2"/><ellipse cx="50" cy="74" rx="12" ry="7" fill="#d4cec4"/>{EYES(es,40,60,57)}{cheeks(31,69,68)}<ellipse cx="50" cy="70" rx="4.5" ry="3.5" fill="{C_["rose"]}" {st}/>{wh(36,73,-1)}{wh(64,73,1)}<path d="M47 79 L47 83 L53 83 L53 79" fill="#fff" {thin}/>',
'cat': f'<path d="M20 50 L24 14 L44 34 Z" fill="{C_["ochre"]}" {st}/><path d="M80 50 L76 14 L56 34 Z" fill="{C_["ochre"]}" {st}/><path d="M26 42 L27 24 L37 34 Z" fill="{C_["rose"]}"/><path d="M74 42 L73 24 L63 34 Z" fill="{C_["rose"]}"/><path d="M28 30 L31 36 M72 30 L69 36" {thin}/>'
       f'<ellipse cx="50" cy="58" rx="33" ry="29" fill="{C_["ochre"]}" {st}/><path d="M42 32 L44 40 M50 30 L50 40 M58 32 L56 40" stroke="#a8621e" stroke-width="3" stroke-linecap="round"/><path d="M18 56 L26 57 M19 63 L27 62 M82 56 L74 57 M81 63 L73 62" stroke="#a8621e" stroke-width="3" stroke-linecap="round"/>'
       f'<path d="M38 66 Q50 58 62 66 Q62 80 50 82 Q38 80 38 66 Z" fill="#f2d3a0"/>{EYES(es,39,61,55)}{cheeks(30,70,67)}<path d="M46 64 L54 64 L50 68 Z" fill="{C_["rose"]}" {st}/><path d="M44 72 Q47 75 50 71 Q53 75 56 72" {thin} stroke-width="2.2"/>{wh(36,68,-1)}{wh(64,68,1)}',
'dog': f'<ellipse cx="50" cy="56" rx="31" ry="30" fill="{C_["tan"]}" {st}/><path d="M57 30 C70 26 80 38 74 50 C66 50 58 42 57 30 Z" fill="{C_["brown"]}"/><path d="M24 30 C6 32 6 66 20 70 C30 62 30 40 26 30 Z" fill="{C_["brown"]}" {st}/><path d="M76 30 C94 32 94 66 80 70 C70 62 70 40 74 30 Z" fill="{C_["brown"]}" {st}/><path d="M14 44 Q16 54 18 62 M86 44 Q84 54 82 62" {thin}/>'
       f'<path d="M45 24 Q48 19 50 24 Q52 18 55 24" {thin} stroke-width="2.2"/><ellipse cx="50" cy="70" rx="16" ry="12" fill="#f2dcb2"/>{EYES(es,40,60,51)}{cheeks(30,70,63)}<ellipse cx="50" cy="64" rx="8" ry="5.5" fill="{INK}"/><circle cx="48" cy="62.5" r="1.6" fill="#fff"/><circle cx="41" cy="72" r="1.2" fill="{INK}"/><circle cx="44" cy="75" r="1.2" fill="{INK}"/><circle cx="59" cy="72" r="1.2" fill="{INK}"/><circle cx="56" cy="75" r="1.2" fill="{INK}"/><path d="M50 69 L50 74 M44 75 Q50 79 56 75" {thin} stroke-width="2.2"/><path d="M47 77 Q50 88 53 77 Z" fill="{C_["rose"]}" {st}/>',
'bear': f'<circle cx="24" cy="28" r="14" fill="{C_["brown"]}" {st}/><circle cx="76" cy="28" r="14" fill="{C_["brown"]}" {st}/><circle cx="24" cy="29" r="6.5" fill="{C_["tan"]}"/><circle cx="76" cy="29" r="6.5" fill="{C_["tan"]}"/><circle cx="50" cy="56" r="33" fill="{C_["brown"]}" {st}/>'
        f'<path d="M42 25 L45 20 L48 25 L51 19 L54 25 L57 21 L58 26" {thin} stroke-width="2.2"/><path d="M22 52 Q20 58 22 64 M78 52 Q80 58 78 64" {thin}/><ellipse cx="50" cy="69" rx="16" ry="12" fill="{C_["tan"]}" {st}/>{EYES(es,38,62,50)}<ellipse cx="50" cy="63.5" rx="7" ry="5" fill="{INK}"/><circle cx="48" cy="62" r="1.6" fill="#fff"/><path d="M50 68 L50 73 M44 74 Q50 78 56 74" {thin} stroke-width="2.2"/>{cheeks(28,72,61)}',
'lion': ''.join(f'<ellipse cx="{50+34*math.cos(a*math.pi/5):.1f}" cy="{54+34*math.sin(a*math.pi/5):.1f}" rx="15" ry="15" fill="{C_["rust"]}" {st}/>' for a in range(10))
        + f'<circle cx="50" cy="54" r="34" fill="{C_["rust"]}"/>' + ''.join(f'<path d="M{50+30*math.cos(a*math.pi/5+0.3):.1f} {54+30*math.sin(a*math.pi/5+0.3):.1f} L{50+42*math.cos(a*math.pi/5+0.3):.1f} {54+42*math.sin(a*math.pi/5+0.3):.1f}" stroke="#8a4518" stroke-width="2.4" stroke-linecap="round"/>' for a in range(10))
        + f'<circle cx="50" cy="56" r="27" fill="{C_["gold"]}" {st}/><path d="M46 31 Q50 26 54 31" {thin} stroke-width="2.4"/><circle cx="31" cy="34" r="6" fill="{C_["gold"]}" {st}/><circle cx="69" cy="34" r="6" fill="{C_["gold"]}" {st}/><path d="M38 62 Q50 56 62 62 Q62 76 50 78 Q38 76 38 62 Z" fill="#f2d79a"/>{EYES(es,41,59,51)}{cheeks(33,67,62)}<path d="M45 60 L55 60 L50 65 Z" fill="{INK}"/><path d="M50 65 L50 69 M45 70 Q50 73 55 70" {thin} stroke-width="2.2"/><circle cx="42" cy="68" r="1.1" fill="{INK}"/><circle cx="44" cy="71" r="1.1" fill="{INK}"/><circle cx="58" cy="68" r="1.1" fill="{INK}"/><circle cx="56" cy="71" r="1.1" fill="{INK}"/>',
'elephant': f'<path d="M26 28 C0 26 2 76 28 72 C32 58 34 40 26 28 Z" fill="{C_["slate2"]}" {st}/><path d="M74 28 C100 26 98 76 72 72 C68 58 66 40 74 28 Z" fill="{C_["slate2"]}" {st}/><path d="M30 28 C18 32 18 62 30 64 Z" fill="{C_["rose"]}" opacity=".6"/><path d="M70 28 C82 32 82 62 70 64 Z" fill="{C_["rose"]}" opacity=".6"/><path d="M14 44 Q20 48 18 56 M86 44 Q80 48 82 56" {thin}/>'
            f'<ellipse cx="50" cy="48" rx="26" ry="27" fill="{C_["slate"]}" {st}/><path d="M46 22 L45 16 M50 21 L50 14 M54 22 L55 16" {thin} stroke-width="2.2"/><path d="M43 62 C43 78 44 88 56 90 C62 90 64 84 58 82 C54 82 56 74 57 62 Z" fill="{C_["slate"]}" {st}/><path d="M44 68 L56 68 M44 74 L56 74 M46 80 L57 80" {thin}/>{EYES(es,40,60,44)}{cheeks(33,67,55)}<path d="M40 60 Q38 66 34 68 M60 60 Q62 66 66 68" stroke="#f7efdc" stroke-width="4" stroke-linecap="round"/>',
}
VAR=[('1 · Big shiny eyes','round heads, large glossy eyes','big','scale(1,1)'),
     ('2 · Dot eyes and brows','small eyes with eyebrows, a bit taller and more grown-up','dot','translate(50 50) scale(.95 1.05) translate(-50 -50)'),
     ('3 · Button eyes, chunky','white button eyes, wider squat heads','button','translate(50 50) scale(1.07 .94) translate(-50 -50)')]
def sv(inner,size,tf): return f'<svg viewBox="0 0 100 100" width="{size}" height="{size}" style="overflow:visible"><g transform="{tf}">{inner}</g></svg>'
rows=''
for k,(label,sub,es,tf) in enumerate(VAR):
    H=heads(es); top=56+k*250
    big=''.join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:4px">{sv(H[a],78,tf)}<span style="font:600 12px Fredoka,sans-serif;color:{P["cream2"]}">{a}</span></div>' for a in ['mouse','cat','dog','bear','lion','elephant'])
    small=''.join(f'<div style="width:46px;height:46px;background:{P["cream"] if j%2 else P["cream2"]};display:grid;place-items:center">{sv(H[a],40,tf)}</div>' for j,a in enumerate(['mouse','cat','dog','bear','lion','elephant']))
    rows+=f'''<div style="position:absolute;left:24px;top:{top}px;font:700 19px Fredoka,sans-serif;color:{P["cream"]}">{label} <span style="font:600 13px Fredoka,sans-serif;color:{P["cream2"]}">{sub}</span></div>
      <div class="k" style="position:absolute;left:24px;width:540px;top:{top+32}px;height:180px;background:{P["navy"]};display:flex;justify-content:space-around;align-items:center">{big}</div>
      <div style="position:absolute;left:584px;top:{top+32}px;font:600 12px Fredoka,sans-serif;color:{P["cream2"]}">at board size</div>
      <div class="k" style="position:absolute;left:584px;top:{top+54}px;width:{46*3}px;height:{46*2}px;overflow:hidden;display:flex;flex-wrap:wrap;background:{P["cream"]}">{small}</div>'''
b=f'''<div style="width:780px;height:844px;box-sizing:border-box;position:relative;overflow:hidden;font-family:Fredoka,sans-serif;background:#3a2c24">
  <b style="position:absolute;left:24px;top:16px;font:700 24px Fredoka,sans-serif;color:{P["cream"]}">Storybook heads, more detail: three variations</b>{rows}
  <div style="position:absolute;left:24px;right:24px;top:804px;font:600 13px Fredoka,sans-serif;color:{P["cream2"]}">New details on all three: whiskers, fur tufts, cat stripes, a dog spot and freckles, mane strands, trunk wrinkles and ear lines.</div>
</div>'''
base='/home/claude/mockups/project'; fn='Med-heads.dc.html'
open(f'{base}/{fn}','w').write(HEAD2%'Storybook heads: variations'+b+'\n'+TAIL.replace('{"width":390,"height":844}','{"width":780,"height":844}'))
c=json.load(open(f'{base}/canvas.json'))
c['boards'].pop(fn,None); c['order']=[o for o in c['order'] if o!=fn]
art=c['boards']['Med-art.dc.html']
c['boards'][fn]={'x':art['x']+art['w']+80,'y':art['y'],'w':780,'h':844,'title':'29 · Storybook heads, more detail: 3 variations'}; c['order'].append(fn)
json.dump(c,open(f'{base}/canvas.json','w'),ensure_ascii=False)
print('ok')
