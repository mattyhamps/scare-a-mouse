import json, math
src=open('./gen7.py').read()
pre=src[:src.index("lsv=lambda")]
VARS={
 'arcs':("1 · Happy closed eyes","curved lines, calm and friendly",lambda x1,x2,y,r=4.6: ''.join(f'<path d="M{x-6} {y+1} Q{x} {y-7} {x+6} {y+1}" fill="none" stroke="#2b1d14" stroke-width="3.2" stroke-linecap="round"/>' for x in (x1,x2))),
 'ovals':("2 · Soft ovals, no shine","taller flat eyes, no highlight dots",lambda x1,x2,y,r=4.6: ''.join(f'<ellipse cx="{x}" cy="{y}" rx="3.6" ry="6.2" fill="#2b1d14"/>' for x in (x1,x2))),
 'whites':("3 · Eyes with whites","a cream eye with a dark pupil looking sideways",lambda x1,x2,y,r=4.6: ''.join(f'<ellipse cx="{x}" cy="{y}" rx="6.4" ry="7.2" fill="#f7efdc"/><circle cx="{x+1.8}" cy="{y+0.6}" r="3.4" fill="#2b1d14"/>' for x in (x1,x2))),
}
rows=''; top=70
for key,(label,sub,fn) in VARS.items():
    ns={}
    exec(pre.replace("def eyes2(x1,x2,y,r=4.6):","def _old_eyes2(x1,x2,y,r=4.6):"), ns) if False else None
    g={}
    code=pre
    exec(code,g)
    g['eyes2']=fn
    # rebuild heads + lion B with new eyes
    s6=open('./gen4.py').read(); hs=s6[s6.index("H={"):s6.index("def sv(k,size)")]
    exec(hs,g)
    s7=open('./gen7.py').read(); l2=s7[s7.index("L2=f'''"):s7.index("L3=f'''")]
    exec(l2,g)
    Hh=g['H']; Hh['lion']=g['L2']
    cells=''.join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:4px"><svg viewBox="0 0 100 100" width="92" height="92" style="overflow:visible">{Hh[k]}</svg><span style="font:600 12px Fredoka;color:#e0cb9c">{k}</span></div>' for k in ['mouse','cat','dog','bear','lion','elephant'])
    small=''.join(f'<div style="width:46px;height:46px;background:{"#f1e3c2" if j%2 else "#e0cb9c"};display:grid;place-items:center"><svg viewBox="0 0 100 100" width="40" height="40" style="overflow:visible">{Hh[k]}</svg></div>' for j,k in enumerate(['mouse','cat','dog','bear','lion','elephant']))
    rows+=f'''<div style="position:absolute;left:24px;top:{top}px;font:700 20px Fredoka,sans-serif;color:#f1e3c2">{label} <span style="font:600 14px Fredoka;color:#e0cb9c">{sub}</span></div>
      <div style="position:absolute;left:24px;top:{top+34}px;width:600px;height:170px;border-radius:22px;background:#857e72;display:flex;align-items:center;justify-content:space-around">{cells}</div>
      <div style="position:absolute;left:640px;top:{top+34}px;width:138px;height:92px;border-radius:12px;overflow:hidden;display:flex;flex-wrap:wrap">{small}</div>'''
    top+=250
g0={}; exec(pre,g0)
b=f'''<div style="width:800px;height:844px;position:relative;overflow:hidden;background:#4a3328;font-family:Fredoka,sans-serif">
  <div style="position:absolute;left:24px;top:18px;font:700 26px Fredoka,sans-serif;color:#f1e3c2">Eyes without the beady look (lion B)</div>{rows}</div>'''
base='/home/claude/mockups/project'; fn='Eyes-options.dc.html'
open(f'{base}/{fn}','w').write(g0['HEADQ']%'Eye options'+b+'\n'+g0['TAIL'].replace('{"width":390,"height":844}','{"width":800,"height":844}'))
c=json.load(open(f'{base}/canvas.json'))
c['boards'].pop(fn,None); c['order']=[o for o in c['order'] if o!=fn]
fl=c['boards']['Floor-detailed.dc.html']
c['boards'][fn]={'x':fl['x']+fl['w']+80,'y':fl['y'],'w':800,'h':844,'title':'45 · Eye options (no beady eyes), lion B'}; c['order'].append(fn)
json.dump(c,open(f'{base}/canvas.json','w'),ensure_ascii=False)
print('ok')
