import json, math, random, re
g19=open('./gen19.py').read()
exec(g19[:g19.index("\nrooms={")])
CAP={}
def page2(name,count,base_n,bg,ground,wall,path,props,pts):
    CAP[name]=wall; return ''
G['page2']=page2; globals()['page2']=page2
storeroom3(); wine3(); dungeon4()
def clean(s): return re.sub(r'\s+',' ',s).strip()
heads={k:clean(v+STEP) for k,v in CAP.items()}
g14=open('./gen14.py').read()
exec(g14[g14.index('# ----- floor'):g14.index('PATH=')])
heads['Kitchens']=clean(WALL+STEP)
PR={}
def add(name,svg,box): PR[name]=[box,clean(svg)]
# Storeroom
add('crate',crate_closed(0,0,44),(0,0,50,58))
add('crate_big',crate_closed(0,0,52),(0,0,58,58))
add('barrel_s',barrel(0,0,.75),(0,0,36,44))
add('sack',sack(0,0),(0,0,46,58))
add('sack_gold',sack(0,0,Q["mustard"],.9),(0,0,42,52))
add('rope',rope(0,0),(0,0,52,28))
add('chest',chest(0,0),(0,0,74,62))
add('cheese_stack',cheese_stack(0,0),(-6,-8,82,56))
# Wine cellar
add('tun',tun(0,0,.9),(0,0,108,84))
add('rack',rack(0,0,72,16,54),(0,0,80,76))
add('candle_table',candle_table(0,0),(0,-12,54,62))
add('grapes',grapes(0,0),(0,-4,46,42))
add('grape_crate',crate(0,0,'cabbage').replace(Q["green"],'#5e3460').replace(Q["green2"],'#4a2850').replace('#8fb85a','#7a4a7a'),(0,0,72,62))
add('wine_rug',f'<g><rect x="0" y="4" width="200" height="130" rx="8" fill="#2a140a" opacity=".2"/><rect x="0" y="0" width="200" height="130" rx="8" fill="{Q["navy"]}"/><rect x="10" y="10" width="180" height="110" rx="5" fill="{Q["navy2"]}"/><rect x="22" y="22" width="156" height="86" rx="4" fill="#5e3460"/><path d="M100 30 L150 65 L100 100 L50 65 Z" fill="{Q["mustard"]}" opacity=".85"/></g>'+f'<g transform="translate(74 30)">{candle_table(0,0)}</g>',(0,0,200,136))
# Dungeon
add('bench',bench(0,0),(0,0,74,36))
add('bucket',bucket(0,0),(0,0,30,36))
add('crate_s',crate_closed(0,0,44),(0,0,50,58))
add('cell_lion',cell3(0,0,176,104,'lion'),(-6,-16,188,128))
add('cell_bear',cell3(0,0,164,100,'bear'),(-6,-16,176,124))
add('rubble',rubble(0,0),(0,0,46,32))
add('ball_chain',ball_chain(0,0),(0,0,44,30))
# Kitchens
add('barrel_k',barrel(0,0),(0,0,48,58))
add('keg',keg(0,0),(0,0,64,48))
add('kitchen_table',table(0,0),(-6,0,138,96))
add('stool',stool(0,0),(0,0,34,40))
add('cat_bed',basket_bed(0,0)+f'<g transform="translate(20 -16)">{sv("cat",40)}</g>',(0,-16,82,68))
add('flour_spill',spill(0,0),(-16,-6,46,12))
add('crate_cabbage',crate(0,0,'cabbage'),(0,0,72,62))
add('crate_carrot',crate(0,0,'carrot'),(0,0,72,62))
add('tub',tub(0,0),(0,0,76,58))
add('logs',logs(0,0),(0,0,82,62))
add('sconce',sconce(0,0),(0,-10,14,46))
d=json.load(open('../../web/src/main/webapp/room-art.json'))
d['heads'].update(heads); d['props'].update(PR)
json.dump(d,open('../../web/src/main/webapp/room-art.json','w'),separators=(',',':'),ensure_ascii=False)
print({k:len(v) for k,v in heads.items()}, len(d['props']))
