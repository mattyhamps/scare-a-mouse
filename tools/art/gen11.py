import json
src=open('./gen7.py').read()
exec(src[:src.index("lsv=lambda")])
BODY=[('Fredoka','Fredoka:wght@500;600;700','rounded, soft (current)'),('Nunito','Nunito:wght@600;700;800','rounded but calmer'),('Alegreya Sans','Alegreya+Sans:wght@500;700;800','humanist, made to pair with calligraphic fonts'),('Alegreya','Alegreya:wght@500;700;800','storybook serif'),('Andika','Andika:wght@400;700','designed for easy reading by kids')]
fam='&amp;'.join('family='+b[1] for b in BODY)+'&amp;family=Almendra:wght@700'
HEADB=HEAD.replace('family=Fredoka:wght@500;600;700',fam)
T="font-family:'Almendra',serif;font-weight:700"
cards=''
for i,(name,_,note) in enumerate(BODY):
    y=66+i*196; F=f"font-family:'{name}',sans-serif"
    nums=''.join(f'<div style="width:38px;height:38px;border-radius:50%;background:{bg};box-shadow:0 3px 0 {sh};display:grid;place-items:center;{F};font-weight:700;font-size:15px">{n}</div>' for n,bg,sh in [(21,Q["mustard"],Q["mustard2"]),(22,Q["mustard"],Q["mustard2"]),(26,Q["cream"],Q["cream2"]),(27,Q["lav"],Q["lav2"])])
    cards+=f'''<div style="position:absolute;left:24px;top:{y}px;width:752px;height:180px;border-radius:22px;background:{Q["purple"]};box-shadow:inset 0 0 0 2px #5a4034">
      <div style="position:absolute;left:18px;top:12px;font:700 12px Fredoka,sans-serif;color:{Q["mustard"]};letter-spacing:.4px">{chr(49+i)} · {name.upper()} <span style="color:{Q["cream2"]};font-weight:600;letter-spacing:0">— {note}</span></div>
      <div style="position:absolute;left:18px;top:34px;{T};font-size:28px;color:{Q["cream"]}">Haystack Hop</div>
      <div style="position:absolute;left:210px;top:38px;padding:3px 12px;border-radius:12px;background:{Q["mustard"]};box-shadow:0 3px 0 {Q["mustard2"]};{F};font-weight:700;font-size:15px">Level 47</div>
      <div style="position:absolute;left:18px;top:80px;width:330px;padding:10px 12px;border-radius:14px;background:{Q["cream"]};box-shadow:0 4px 0 {Q["cream2"]};{F};font-weight:600;font-size:15px;line-height:1.35;color:{Q["ink"]}">Lions scare bears. Start a chain that ends with the mouse in the hole!</div>
      <div style="position:absolute;left:380px;top:36px;display:flex;gap:10px">{nums}</div>
      <div style="position:absolute;left:380px;top:92px;display:flex;gap:10px">
        <div style="padding:10px 14px;border-radius:14px;background:{Q["cream"]};box-shadow:0 4px 0 {Q["cream2"]};{F};font-weight:700;font-size:16px">Hint · 1</div>
        <div style="padding:10px 14px;border-radius:14px;background:{Q["pink"]};box-shadow:0 4px 0 {Q["pink2"]};{F};font-weight:700;font-size:16px">Reset</div>
        <div style="padding:10px 18px;border-radius:14px;background:{Q["coral"]};box-shadow:0 4px 0 {Q["coral2"]};{T};font-size:20px;color:{Q["cream"]}">Go!</div>
        <div style="{F};font-weight:600;font-size:13px;color:{Q["cream2"]};width:90px;line-height:1.25">Level 47 solved · +3 cheese</div></div></div>'''
b=f'''<div style="width:800px;height:1060px;position:relative;overflow:hidden;background:#3a2a22;font-family:Fredoka,sans-serif">
  <div style="position:absolute;left:24px;top:18px;font:700 24px Fredoka,sans-serif;color:{Q["cream"]}">Small text with Almendra titles</div>{cards}</div>'''
base='/home/claude/mockups/project'; fn='Body-fonts.dc.html'
open(f'{base}/{fn}','w').write(HEADB%'Small text fonts'+b+'\n'+TAIL.replace('{"width":390,"height":844}','{"width":800,"height":1060}'))
c=json.load(open(f'{base}/canvas.json'))
c['boards'].pop(fn,None); c['order']=[o for o in c['order'] if o!=fn]
f2=c['boards']['Fonts-2.dc.html']
c['boards'][fn]={'x':f2['x']+f2['w']+80,'y':f2['y'],'w':800,'h':1060,'title':'48 · Small-text fonts with Almendra titles'}; c['order'].append(fn)
json.dump(c,open(f'{base}/canvas.json','w'),ensure_ascii=False)
print('ok')
