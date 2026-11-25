import urllib.parse, json
W='#c58a55'; W1='#a06a3e'; W2='#7d5030'; P='#f1e3c2'; P2='#e0cb9c'
T={}
# kitchen counter: butcher-block top, cupboard front with a handle
T['counter']=f'''<rect x="1" y="1" width="46" height="46" rx="5" fill="{W1}"/><rect x="1" y="1" width="46" height="17" rx="5" fill="#e6c79a"/><rect x="1" y="13" width="46" height="5" fill="#cfa877"/>
<path d="M12 1 L12 18 M24 1 L24 18 M36 1 L36 18" stroke="#cfa877" stroke-width="1.6"/><rect x="5" y="22" width="18" height="21" rx="2" fill="{W}"/><rect x="25" y="22" width="18" height="21" rx="2" fill="{W}"/><rect x="38" y="22" width="5" height="21" fill="{W1}"/><rect x="18" y="22" width="5" height="21" fill="{W1}"/>
<circle cx="20" cy="32" r="1.8" fill="#d9a43a"/><circle cx="28" cy="32" r="1.8" fill="#d9a43a"/>'''
# bookshelf: a wooden case with two rows of coloured spines
cols=['#a8353a','#2f4f8f','#d9a43a','#3f6b3a','#7a4a7a','#b5622a','#f1e3c2']
sp=''.join(f'<rect x="{5+i*5.4:.1f}" y="{6 if i%3 else 8}" width="4.6" height="{15 if i%3 else 13}" fill="{cols[i%7]}"/>' for i in range(7))
sp+=''.join(f'<rect x="{5+i*5.4:.1f}" y="{27 if i%2 else 29}" width="4.6" height="{15 if i%2 else 13}" fill="{cols[(i+3)%7]}"/>' for i in range(7))
T['shelf']=f'<rect x="1" y="1" width="46" height="46" rx="4" fill="{W2}"/><rect x="4" y="4" width="40" height="40" fill="#3a2418"/>{sp}<rect x="4" y="21" width="40" height="4" fill="{W1}"/><rect x="4" y="42" width="40" height="3" fill="{W1}"/><rect x="40" y="4" width="4" height="40" fill="#5a3a24"/>'
# banquet table from above: oak planks with a plate and a cup
T['table']=f'<rect x="1" y="1" width="46" height="46" rx="5" fill="{W1}"/><rect x="1" y="1" width="46" height="42" rx="5" fill="{W}"/><path d="M1 15 L47 15 M1 29 L47 29" stroke="{W1}" stroke-width="1.6"/><ellipse cx="22" cy="22" rx="11" ry="10" fill="{P}"/><ellipse cx="22" cy="22" rx="6.5" ry="6" fill="{P2}"/><rect x="34" y="9" width="7" height="9" rx="2" fill="#a39c8f"/><ellipse cx="37.5" cy="9.5" rx="3.5" ry="1.6" fill="#a8353a"/>'
# marble pillar from above: square base, round column, gold ring
T['pillar']=f'<rect x="1" y="1" width="46" height="46" rx="4" fill="#8f817d"/><rect x="1" y="1" width="46" height="42" rx="4" fill="#a99a96"/><circle cx="24" cy="22" r="16" fill="#efe6e3"/><path d="M24 6 A16 16 0 0 1 24 38 A16 16 0 0 0 30 22 A16 16 0 0 0 24 6 Z" fill="#d6c8c4"/><circle cx="24" cy="22" r="11" fill="none" stroke="#d9a43a" stroke-width="2"/>'
# chapel pew: a backrest along the top and the seat below, with a red cushion
T['pew']=f'<rect x="1" y="1" width="46" height="46" rx="5" fill="{W2}"/><rect x="1" y="1" width="46" height="13" rx="4" fill="{W1}"/><rect x="1" y="11" width="46" height="4" fill="{W2}"/><rect x="2" y="17" width="44" height="26" rx="3" fill="{W}"/><rect x="6" y="24" width="36" height="9" rx="3" fill="#842629"/><rect x="6" y="24" width="36" height="4" rx="2" fill="#a8353a"/>'
# rough rock
T['rock']='<path d="M4 42 Q1 22 12 10 Q24 2 36 8 Q46 16 45 30 Q44 44 30 46 Q14 47 4 42 Z" fill="#a39c8f"/><path d="M36 8 Q46 16 45 30 Q44 44 30 46 Q22 46 18 44 Q36 38 38 24 Q38 14 36 8 Z" fill="#857e72"/><path d="M12 18 Q18 11 26 12" stroke="#bdb6a9" stroke-width="3.4" fill="none" stroke-linecap="round"/><path d="M10 34 l6 -3" stroke="#857e72" stroke-width="2" stroke-linecap="round"/>'
# map table: a wooden table with a chart on it
T['maptable']=f'<rect x="1" y="1" width="46" height="46" rx="5" fill="{W1}"/><rect x="1" y="1" width="46" height="42" rx="5" fill="{W}"/><g transform="rotate(-6 24 22)"><rect x="8" y="8" width="32" height="28" rx="2" fill="{P}"/><path d="M12 26 q6 -10 12 -2 q6 6 12 -6" stroke="#b39260" stroke-width="2" fill="none"/><path d="M14 14 l4 4 M18 14 l-4 4" stroke="#a8353a" stroke-width="2"/><path d="M28 22 l3 3 l-3 3 l-3 -3 Z" fill="#7a9a4a"/></g>'
# weapon rack: a wooden frame holding three blades
bl=''.join(f'<rect x="{x}" y="5" width="4" height="34" fill="#c4c1cc"/><rect x="{x+2}" y="5" width="2" height="34" fill="#9a97a4"/><path d="M{x} 5 L{x+2} 1 L{x+4} 5 Z" fill="#c4c1cc"/><rect x="{x-2}" y="30" width="8" height="3" fill="#d9a43a"/>' for x in (10,22,34))
T['rack']=f'<rect x="1" y="1" width="46" height="46" rx="4" fill="#3e3a48"/>{bl}<rect x="2" y="8" width="44" height="5" rx="2" fill="{W1}"/><rect x="2" y="38" width="44" height="7" rx="2" fill="{W1}"/><rect x="2" y="42" width="44" height="3" fill="{W2}"/>'
# gallery statue: a bust on a stone plinth
T['statue']='<rect x="5" y="26" width="38" height="20" rx="2" fill="#a99a96"/><rect x="33" y="26" width="10" height="20" fill="#8f817d"/><rect x="2" y="22" width="44" height="7" rx="2" fill="#c4b6b2"/><path d="M12 24 Q14 15 24 14 Q34 15 36 24 Z" fill="#efe6e3"/><path d="M24 14 Q34 15 36 24 L28 24 Q30 18 24 14 Z" fill="#d6c8c4"/><ellipse cx="24" cy="9" rx="6.5" ry="7.5" fill="#efe6e3"/><path d="M24 1.5 A6.5 7.5 0 0 1 24 16.5 A6.5 7.5 0 0 0 26.5 9 A6.5 7.5 0 0 0 24 1.5 Z" fill="#d6c8c4"/>'
out={k:'url("data:image/svg+xml,'+urllib.parse.quote(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">{v}</svg>'.replace('\n',''),safe=":/=,() ")+'")' for k,v in T.items()}
json.dump(out,open('./walltiles.json','w'))
print({k:len(v) for k,v in out.items()})
