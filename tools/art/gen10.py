import json
src=open('./gen7.py').read()
exec(src[:src.index("lsv=lambda")])
FONTS=[('Bagel Fat One','Bagel+Fat+One','400','bubbly (current mockups)'),
       ('Lilita One','Lilita+One','400','bold and friendly, a touch storybook'),
       ('MedievalSharp','MedievalSharp','400','medieval, playful'),
       ('Uncial Antiqua','Uncial+Antiqua','400','Celtic manuscript, very readable'),
       ('Macondo','Macondo','400','whimsical fairy-tale'),
       ('Almendra','Almendra:wght@700','700','elegant fairy-tale'),
       ('Pirata One','Pirata+One','400','blackletter, the most "old"'),
       ('IM Fell English SC','IM+Fell+English+SC','400','old printed book')]
fam='&amp;'.join('family='+f[1] for f in FONTS)
HEADF=HEAD.replace('family=Fredoka:wght@500;600;700','family=Fredoka:wght@500;600;700&amp;'+fam)
cards=''
for i,(name,_,w,note) in enumerate(FONTS):
    col=i%2; row=i//2; x=24+col*388; y=70+row*236
    cards+=f'''<div style="position:absolute;left:{x}px;top:{y}px;width:368px;height:216px;border-radius:22px;background:{Q["cream"]};box-shadow:0 6px 0 {Q["cream2"]};padding:14px 18px;box-sizing:border-box;color:{Q["ink"]}">
      <div style="font:700 12px Fredoka,sans-serif;color:{Q["orange"]};letter-spacing:.5px">{chr(65+i)} · {name.upper()} <span style="color:{Q["brown"]};font-weight:600;letter-spacing:0">— {note}</span></div>
      <div style="font-family:'{name}',serif;font-weight:{w};font-size:{30 if name=='Uncial Antiqua' else 40}px;line-height:1.1;margin-top:8px">Scare-a-Mouse</div>
      <div style="font-family:'{name}',serif;font-weight:{w};font-size:{18 if name=='Uncial Antiqua' else 24}px;margin-top:4px">Haystack Hop · The castle</div>
      <div style="display:flex;gap:10px;margin-top:12px;align-items:center">
        <div style="padding:6px 14px;border-radius:12px;background:{Q["coral"]};box-shadow:0 4px 0 {Q["coral2"]};font-family:'{name}',serif;font-weight:{w};font-size:{16 if name=='Uncial Antiqua' else 20}px;color:{Q["cream"]}">Mouse escaped!</div>
        <div style="font:600 13px/1.3 Fredoka,sans-serif;width:130px">Small text stays in Fredoka.</div></div></div>'''
b=f'''<div style="width:800px;height:1030px;position:relative;overflow:hidden;background:{Q["purple"]};font-family:Fredoka,sans-serif">
  <div style="position:absolute;left:24px;top:18px;font:700 26px Fredoka,sans-serif;color:{Q["cream"]}">Title fonts, in the chosen style</div>{cards}</div>'''
base='/home/claude/mockups/project'; fn='Fonts-2.dc.html'
open(f'{base}/{fn}','w').write(HEADF%'Title fonts'+b+'\n'+TAIL.replace('{"width":390,"height":844}','{"width":800,"height":1030}'))
c=json.load(open(f'{base}/canvas.json'))
c['boards'].pop(fn,None); c['order']=[o for o in c['order'] if o!=fn]
m=c['boards']['Room-detailed-meadow.dc.html']
c['boards'][fn]={'x':m['x']+m['w']+80,'y':m['y'],'w':800,'h':1030,'title':'47 · Title fonts in the chosen style'}; c['order'].append(fn)
json.dump(c,open(f'{base}/canvas.json','w'),ensure_ascii=False)
print('ok')
