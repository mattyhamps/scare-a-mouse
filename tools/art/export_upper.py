import json, math, random, re
g21=open('./gen21.py').read()
exec(g21[:g21.index("\nrooms={")])
CAP={}
def page2(name,count,base_n,bg,ground,wall,path,props,pts):
    CAP[name]=wall; return ''
G['page2']=page2; globals()['page2']=page2
for f in (library,study,great_hall,ballroom,gallery,chapel,passage,maproom,armory):
    try: f()
    except Exception as e: print('err',f.__name__,e)
def clean(s): return re.sub(r'\s+',' ',s).strip()
heads={k:clean(v+STEP) for k,v in CAP.items()}
PR={}
def add(name,svg,box): PR[name]=[box,clean(svg)]
# Library
for k,seed in enumerate((3,7,9,11)): add(f'bookshelf{k}',bookshelf(0,0,72,80,14,seed),(0,0,78,98))
add('armchair_navy',armchair(0,0,Q["navy"],Q["navy2"]),(0,0,54,54))
add('armchair_red',armchair(0,0),(0,0,54,54))
add('armchair_green',armchair(0,0,Q["green"],Q["green2"]),(0,0,54,54))
add('globe',globe(0,0),(0,0,42,66))
add('books',books(0,0,4),(-2,-22,40,36))
add('books3',books(0,0,3),(-2,-16,40,30))
add('reading_table',reading_table(0,0),(0,-14,62,66))
# Study
add('study_desk',f'<g><rect x="-6" y="-12" width="162" height="150" rx="10" fill="{Q["coral2"]}"/><rect x="4" y="-2" width="142" height="130" rx="6" fill="{Q["coral"]}"/></g>'+desk(0,0),(-6,-12,162,150))
add('telescope',telescope(0,0),(-8,0,58,76))
add('chair',chair(0,0),(0,0,38,48))
add('scrolls',scrolls(0,0),(0,-12,46,54))
add('drawers',drawers(0,0),(0,-16,66,88))
# Great hall
add('feast_table',feast_table(0,0,300),(-6,0,70,332))
add('bench_v',bench_v(0,0,300),(-4,0,26,312))
add('armor',armor(0,0),(-4,-18,46,104))
add('dog_bed',f'<g>{shadow(30,40,34,7)}<ellipse cx="30" cy="30" rx="30" ry="12" fill="#c99a56"/><ellipse cx="30" cy="27" rx="26" ry="10" fill="{Q["coral"]}"/></g><g transform="translate(6 -40)">{sv("dog",46)}</g>',(0,-42,62,86))
add('barrel_h',barrel(0,0,.8),(0,0,40,48))
# Ballroom
add('pillar',pillar(0,0,100),(-4,-6,52,116))
add('piano',piano(0,0),(0,0,106,114))
add('harp',harp(0,0),(0,-6,50,74))
add('punch_table',punch_table(0,0),(0,0,64,58))
add('vase_pink',vase_flowers(0,0),(0,-10,36,64))
add('vase_coral',vase_flowers(0,0,Q["coral"]),(0,-10,36,64))
add('vase_cream',vase_flowers(0,0,Q["cream"]),(0,-10,36,64))
# Gallery
add('bust',plinth(0,0,bust_top()),(-4,-14,52,94))
add('urn',plinth(0,0,urn_top()),(-4,-14,52,94))
add('ropes',ropes(0,0,3,42),(-8,0,106,46))
add('easel',easel(0,0),(0,0,54,86))
add('bench',bench(0,0),(0,0,74,36))
# Chapel
add('pew',pew(0,0,140),(0,0,146,46))
add('pew_s',pew(0,0,100),(0,0,106,46))
add('candle_stand',candle_stand(0,0),(-6,-16,44,88))
add('font',font(0,0),(0,0,54,64))
add('lectern',lectern(0,0),(0,0,42,64))
# Secret passage
add('brazier',brazier(0,0),(-8,-20,60,84))
add('glowshrooms',glowshrooms(0,0),(-10,-6,68,48))
add('puddle',puddle(0,0),(0,0,52,18))
add('key',key_item(0,0),(0,0,32,16))
add('chest',chest(0,0),(0,0,74,62))
add('rubble',rubble(0,0),(0,0,46,32))
add('rock',rock(0,0,1),(0,0,42,28))
add('barrel_p',barrel(0,0,.75),(0,0,36,44))
# Map room
add('ship_model',ship_model(0,0),(0,0,62,66))
add('chart_desk',chart_desk(0,0),(-6,0,142,88))
add('treasure_chest',chest(0,0),(0,0,74,62))
add('compass_rose',f'<g transform="translate(30 30)"><circle r="28" fill="{Q["cream"]}" opacity=".6"/><path d="M0 -26 L5 0 L0 26 L-5 0 Z" fill="{Q["coral"]}"/><path d="M-26 0 L0 5 L26 0 L0 -5 Z" fill="{DARK}" opacity=".7"/><circle r="3" fill="{Q["mustard"]}"/></g>',(0,0,60,60))
add('serpent',f'<g transform="translate(0 16)" opacity=".9">'+''.join(f'<path d="M{k*16} 0 q8 -14 16 0" fill="{Q["green"]}"/><path d="M{k*16+8} -7 q4 -2 8 7 l-8 0 Z" fill="{Q["green2"]}"/>' for k in range(3))+f'<circle cx="54" cy="-8" r="7" fill="{Q["green"]}"/><circle cx="56" cy="-10" r="1.6" fill="{DARK}"/></g>',(0,0,64,20))
add('x_mark',f'<path d="M2 2 L18 18 M18 2 L2 18" stroke="{Q["coral2"]}" stroke-width="5" stroke-linecap="round"/>',(0,0,20,20))
# Armory
add('weapon_rack',weapon_rack(0,0,70),(0,-40,70,86))
add('anvil',anvil(0,0),(0,-12,52,58))
add('target',target(0,0),(0,0,54,76))
add('arrow_barrel',arrow_barrel(0,0),(0,-26,44,74))
add('shields',shield_stand(0,0),(0,0,72,50))
d=json.load(open('../../web/src/main/webapp/room-art.json'))
d['heads'].update(heads); d['props'].update(PR)
json.dump(d,open('./room-art-full.json','w'),separators=(',',':'),ensure_ascii=False)
print({k:len(v) for k,v in heads.items()}, len(d['props']), len(json.dumps(d)))
