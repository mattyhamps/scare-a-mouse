import json, math, random
G={'random':random,'math':math,'json':json}
g7=open('./gen7.py').read()
exec(g7[:g7.index("lsv=lambda")], G)      # palette, helpers, lions, two()
# chosen style: Almendra titles, oval eyes, lion B
G['TT']="font-family:'Almendra',serif;font-weight:700"
def eyes2(x1,x2,y,r=4.6): return ''.join(f'<ellipse cx="{x}" cy="{y}" rx="3.6" ry="6.2" fill="#2b1d14"/>' for x in (x1,x2))
G['eyes2']=eyes2
g4=open('./gen4.py').read(); exec(g4[g4.index("H={"):g4.index("def sv(k,size)")], G)
exec(g7[g7.index("L2=f'''"):g7.index("L3=f'''")], G)
G['H']['lion']=G['L2']
G['HEADQ']=G['HEAD'].replace('family=Fredoka:wght@500;600;700','family=Fredoka:wght@500;600;700&amp;family=Almendra:wght@700')
out={}
def run(src, a, b):
    G['boards']={}
    exec(src[a:b], G)
    for k,v in G['boards'].items(): out[k]=v
g5=open('./gen5.py').read(); run(g5, g5.index("\nboards={}\n")+1, g5.index("base='/home/claude"))
g6=open('./gen6.py').read(); run(g6, g6.index("\nboards={}\n")+1, g6.index("base='/home/claude"))
run(g7, g7.index("# ---------- detailed castle cutaway"), g7.index("# ---------- detailed floor plan"))
g9=open('./gen9.py').read(); run(g9, g9.index("rnd=random.Random(7)"), g9.index("base='/home/claude"))
# ---------- detailed Kitchens (new)
exec(open('./kitchens_body.py').read(), G)
out['K']=G['boards']['K']
pick=[('MedRetro-board.dc.html','Final-board.dc.html','F1 · Game board',390),
      ('Room-detailed-meadow.dc.html','Final-meadow.dc.html','F2 · Room map: the Meadow',390),
      ('K','Final-kitchens.dc.html','F3 · Room map: the Kitchens (indoor)',390),
      ('Castle-detailed.dc.html','Final-castle.dc.html','F4 · The castle',390),
      ('MedRetro-floor.dc.html','Final-floor.dc.html','F5 · A floor plan',390),
      ('MedRetro-win.dc.html','Final-win.dc.html','F6 · Win screen',390),
      ('MedRetro-howto.dc.html','Final-howto.dc.html','F7 · How-to-play card',390),
      ('MedRetro-sheet.dc.html','Final-sheet.dc.html','F8 · Animals, palette and objects',780)]
base='/home/claude/mockups/project'
c=json.load(open(f'{base}/canvas.json'))
y=max(v['y']+v['h'] for v in c['boards'].values())+500; x=0
for src_fn,fn,title,w in pick:
    t,body=out[src_fn][0],out[src_fn][1]
    body=body.replace('Medieval retro flat</div>','Scare-a-Mouse style</div>')
    open(f'{base}/{fn}','w').write(G['HEADQ']%title+body+'\n'+G['TAIL'].replace('{"width":390,"height":844}','{"width":%d,"height":844}'%w))
    c['boards'].pop(fn,None); c['order']=[o for o in c['order'] if o!=fn]
    c['boards'][fn]={'x':x,'y':y,'w':w,'h':844,'title':title}; c['order'].append(fn); x+=w+80
c['notes']['tF']={'x':0,'y':y-260,'text':'FINAL STYLE for approval: two-tone, medieval colours, Almendra + Fredoka','kind':'title1','maxW':3600}
json.dump(c,open(f'{base}/canvas.json','w'),ensure_ascii=False)
print('ok', [p[1] for p in pick])
