import json, math, random, re
g19=open('./gen19.py').read()
exec(g19[:g19.index("\nrooms={")])
CAP={}
def page2(name,count,base_n,bg,ground,wall,path,props,pts):
    CAP[name]=wall; return ''
G['page2']=page2
globals()['page2']=page2
for f in (meadow4,orchard4,stables4,moat4,gate4):
    try: f()
    except Exception as e: print('err',f.__name__,e)
# Meadow's head is SKY (+STEP); page2 got SKY as wall already.
heads={k:(v+STEP) for k,v in CAP.items()}
def clean(s): return re.sub(r'\s+',' ',s).strip()
# props drawn at the origin, with their box (x, y, w, h) relative to the origin, shadow included
PR={}
def add(name,svg,box): PR[name]=[box,clean(svg)]
add('tree_apple',tree3(0,0,.85,True),(0,-6,84,104))
add('tree',tree3(0,0,.8,False),(0,-6,80,96))
add('pear_tree',pear_tree(0,0,.75),(0,-6,76,90))
add('bush_pink',bush3(0,0,.8,Q["pink"]),(0,0,50,34))
add('bush_cream',bush3(0,0,.8,Q["cream"]),(0,0,50,34))
add('blanket',blanket(0,0),(-4,-6,120,80))
add('mushrooms',mush3(0,0,Q["coral"],Q["coral2"]),(0,0,50,34))
add('pond',pond3(0,0),(-6,0,136,84))
add('rock',rock(0,0,.8),(0,0,36,24))
add('skep',skep(0,0),(-12,-10,76,96))
add('flowers_pink',flower_patch(0,0,Q["pink"],Q["pink2"]),(-6,-4,46,30))
add('flowers_cream',flower_patch(0,0,Q["cream"],Q["cream2"]),(-6,-4,46,30))
add('flowers_blue',flower_patch(0,0,Q["navy"],Q["navy2"]),(-6,-4,46,30))
add('fence',fence3(0,0,3),(-6,0,96,46))
add('hay',hay(0,0),(0,0,76,54))
add('signpost',signpost(0,0),(-4,0,56,64))
add('apple_crate',apple_crate(0,0),(0,0,52,48))
add('pear_crate',apple_crate(0,0,(Q["mustard"],Q["mustard2"])),(0,0,52,48))
add('ladder',ladder3(0,0,58,12),(-4,0,34,64))
add('cart_apples',cart(0,0),(0,0,140,82))
add('cart_hay',cart(0,0,'hay'),(0,0,140,82))
add('well',well(0,0),(-6,-22,82,92))
add('stall',horse_stall(0,0),(-6,-4,110,92))
add('bale',square_bale(0,0,.8),(0,0,48,34))
add('pitchfork',pitchfork(0,0),(-4,0,34,80))
add('trough',trough(0,0),(0,0,84,44))
add('chicken',chicken(0,0),(0,-6,32,30))
add('hen',chicken(0,0,'#c9783a','#a65e2a'),(0,-6,32,30))
add('bucket',bucket(0,0),(0,0,30,36))
add('sack',sack(0,0),(0,0,46,58))
add('sack_gold',sack(0,0,Q["mustard"],.9),(0,0,42,52))
add('reeds',reeds3(0,0,.8),(0,0,42,38))
add('lily',lily(0,0),(0,0,26,16))
add('lily_plain',lily(0,0,.8,False),(0,0,22,14))
add('frog',frog(0,0),(0,0,22,18))
add('fish',fish(0,0),(0,0,22,8))
add('rowboat',rowboat(0,0),(0,-10,100,54))
add('island_reeds',bank(0,0,110,70)+reeds3(30,8,.8),(0,0,110,76))
add('island_bush',bank(0,0,130,76)+bush3(40,16,.7,Q["pink"])+rock(18,30,.6),(0,0,130,82))
add('tent_red',tent(0,0,Q["coral"],Q["coral2"]),(-4,-14,96,80))
add('tent_blue',tent(0,0,Q["navy"],Q["navy2"]),(-4,-14,96,80))
add('campfire',campfire(0,0),(0,-6,48,40))
add('shields',shield_stand(0,0),(0,0,72,50))
add('barrel',barrel(0,0,.8),(0,0,40,48))
add('pine',pine(0,0,.8),(0,-2,50,80))
add('butterfly_pink',butterfly(0,0,Q["pink"],Q["pink2"]),(-10,-10,20,20))
add('butterfly_cream',butterfly(0,0,Q["cream"],Q["cream2"]),(-10,-10,20,20))
add('tuft',tuft3(0,0),(0,-4,18,14))
out={'heads':{k:clean(v) for k,v in heads.items()},'props':PR}
json.dump(out,open('./outside_art.json','w'))
print({k:len(v) for k,v in out['heads'].items()}, len(PR), sum(len(v[1]) for v in PR.values()))
