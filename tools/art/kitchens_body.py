rk=random.Random(11)
def kpot(x,y,s=1): return f'<g transform="translate({x} {y}) scale({s})"><rect x="13" y="0" width="4" height="16" fill="{Q["ink"]}"/><circle cx="15" cy="28" r="13" fill="#4a4652"/><path d="M15 15 A13 13 0 0 1 28 28 A13 13 0 0 1 20 40 A13 13 0 0 0 23 28 Z" fill="#35323c"/></g>'
def herbs(x,y): return f'<g transform="translate({x} {y})"><rect x="0" y="0" width="70" height="4" fill="{Q["brown2"]}"/>' + ''.join(f'<rect x="{6+k*16}" y="4" width="2" height="8" fill="{Q["brown2"]}"/><path d="M{1+k*16} 12 L{13+k*16} 12 L{7+k*16} 32 Z" fill="{c}"/><path d="M{7+k*16} 12 L{13+k*16} 12 L{7+k*16} 32 Z" fill="{c2}"/>' for k,(c,c2) in enumerate([(Q["green"],Q["green2"]),(Q["cream"],Q["cream2"]),(Q["coral"],Q["coral2"]),(Q["olive"],Q["olive2"])])) + '</g>'
def window(x,y): return f'<g transform="translate({x} {y})"><rect x="-4" y="-4" width="52" height="74" rx="26" fill="{Q["lav2"]}"/><rect x="0" y="0" width="44" height="66" rx="22" fill="#9cb8c8"/><path d="M22 0 A22 22 0 0 1 44 22 L44 66 L30 66 L30 10 Z" fill="#86a5b8"/><rect x="20" y="0" width="4" height="66" fill="{Q["lav2"]}"/><rect x="0" y="30" width="44" height="4" fill="{Q["lav2"]}"/><rect x="-6" y="62" width="56" height="8" rx="4" fill="{Q["brown"]}"/></g>'
def bigshelf(x,y):
    g=f'<g transform="translate({x} {y})"><rect x="0" y="0" width="96" height="70" rx="6" fill="{Q["brown"]}"/><rect x="70" y="0" width="26" height="70" rx="6" fill="{Q["brown2"]}"/><rect x="6" y="6" width="84" height="26" fill="#5a3a24"/><rect x="6" y="38" width="84" height="26" fill="#5a3a24"/>'
    for i,(c,c2,w,h) in enumerate([(Q["cream"],Q["cream2"],14,20),(Q["coral"],Q["coral2"],12,16),(Q["mustard"],Q["mustard2"],16,18),(Q["green"],Q["green2"],12,22),(Q["navy"],Q["navy2"],14,16)]):
        g+=f'<rect x="{8+i*17}" y="{32-h}" width="{w}" height="{h}" rx="4" fill="{c}"/><rect x="{8+i*17+w/2}" y="{32-h}" width="{w/2}" height="{h}" rx="3" fill="{c2}"/>'
    g+=f'<ellipse cx="24" cy="58" rx="14" ry="6" fill="{Q["mustard"]}"/><rect x="44" y="44" width="16" height="20" rx="3" fill="{Q["cream"]}"/><rect x="66" y="48" width="18" height="16" rx="8" fill="{Q["orange"]}"/>'
    return g+'</g>'
def hearthD(x,y):
    return f'''<g transform="translate({x} {y})"><rect x="0" y="0" width="140" height="132" rx="12" fill="{Q["lav"]}"/><rect x="104" y="0" width="36" height="132" rx="12" fill="{Q["lav2"]}"/>
      {''.join(f'<rect x="{6+(r%2)*14+k*34}" y="{6+r*20}" width="28" height="14" rx="3" fill="#978f83" opacity=".55"/>' for r in range(2) for k in range(4) if 6+(r%2)*14+k*34<128)}
      <rect x="-6" y="44" width="152" height="12" rx="4" fill="{Q["brown"]}"/><rect x="-6" y="52" width="152" height="4" fill="{Q["brown2"]}"/>
      <path d="M24 132 L24 84 C24 62 116 62 116 84 L116 132 Z" fill="#2e1c14"/>
      <path d="M40 132 L100 132 L96 124 L44 124 Z" fill="#4a3226"/>
      <path d="M52 124 C48 108 60 98 66 88 C68 102 82 106 76 124 Z" fill="{Q["mustard"]}"/><path d="M62 124 C60 114 66 108 68 102 C72 110 76 116 72 124 Z" fill="{Q["coral"]}"/><path d="M78 124 C76 114 84 108 86 104 C88 112 92 116 88 124 Z" fill="{Q["mustard"]}"/>
      <rect x="68" y="62" width="4" height="18" fill="{Q["ink"]}"/><ellipse cx="70" cy="94" rx="28" ry="18" fill="#4a4652"/><path d="M70 76 A28 18 0 0 1 98 94 A28 18 0 0 1 78 111 A28 18 0 0 0 88 94 Z" fill="#35323c"/><ellipse cx="70" cy="80" rx="24" ry="5" fill="{Q["olive"]}"/>
      <g transform="translate(6 20)">{''.join(f'<rect x="{k*22}" y="{10-h}" width="14" height="{h}" rx="5" fill="{c}"/>' for k,(c,h) in enumerate([(Q["cream"],16),(Q["mustard"],12),(Q["coral"],14),(Q["navy"],10),(Q["cream2"],18),(Q["olive"],12)]))}</g>
      <ellipse cx="62" cy="60" rx="8" ry="5" fill="{Q["cream"]}" opacity=".85"/><ellipse cx="74" cy="50" rx="6" ry="4" fill="{Q["cream"]}" opacity=".6"/></g>'''
def tableD(x,y):
    return f'''<g transform="translate({x} {y})"><rect x="10" y="0" width="120" height="12" rx="6" fill="{Q["brown2"]}"/><rect x="0" y="18" width="140" height="66" rx="12" fill="{Q["brown"]}"/><rect x="0" y="66" width="140" height="18" rx="9" fill="{Q["brown2"]}"/>
      <path d="M0 40 L140 40 M0 58 L140 58" stroke="{Q["brown2"]}" stroke-width="2"/><rect x="10" y="90" width="120" height="12" rx="6" fill="{Q["brown2"]}"/>
      <ellipse cx="28" cy="38" rx="17" ry="9" fill="{Q["mustard"]}"/><path d="M14 36 L42 36" stroke="{Q["mustard2"]}" stroke-width="2"/><path d="M60 26 L88 26 L82 44 L66 44 Z" fill="{Q["cream"]}"/><path d="M74 26 L88 26 L82 44 L74 44 Z" fill="{Q["cream2"]}"/>
      <path d="M98 52 L126 52 L126 30 Z" fill="{Q["mustard"]}"/><path d="M110 52 L126 52 L126 30 Z" fill="{Q["mustard2"]}"/><circle cx="114" cy="46" r="3" fill="{Q["mustard2"]}"/>
      <circle cx="46" cy="62" r="8" fill="{Q["coral"]}"/><circle cx="47.5" cy="60.5" r="2.4" fill="{Q["pink"]}"/><circle cx="62" cy="64" r="7" fill="{Q["coral2"]}"/>
      <ellipse cx="96" cy="68" rx="14" ry="5" fill="{Q["cream"]}"/><path d="M84 68 Q90 58 96 66 Q102 58 108 68" fill="{Q["tan"]}"/></g>'''
def sacksD(x,y): return f'<g transform="translate({x} {y})">' + ''.join(f'<path d="M{a} 88 C{a-8} 88 {a-10} 52 {a+6} 44 L{a+4} 34 L{a+26} 34 L{a+24} 44 C{a+40} 52 {a+38} 88 {a+30} 88 Z" fill="{Q["tan"]}"/><path d="M{a+18} 48 C{a+34} 56 {a+34} 86 {a+30} 88 L{a+16} 88 C{a+24} 76 {a+24} 58 {a+18} 48 Z" fill="{Q["tan2"]}"/><rect x="{a+4}" y="40" width="22" height="5" rx="2" fill="{Q["coral"]}"/><text x="{a+15}" y="72" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="8" fill="{Q["brown2"]}">{t}</text>' for a,t in ((8,'FLOUR'),(46,'OATS'),(84,'SALT'))) + f'<ellipse cx="22" cy="92" rx="10" ry="4" fill="{Q["cream"]}"/></g>'
def barrelsD(x,y): return f'<g transform="translate({x} {y})">' + ''.join(f'<rect x="{a}" y="{t}" width="34" height="44" rx="13" fill="{Q["orange"]}"/><rect x="{a+18}" y="{t}" width="16" height="44" rx="8" fill="{Q["orange2"]}"/><rect x="{a}" y="{t+11}" width="34" height="5" fill="{Q["orange2"]}"/><rect x="{a}" y="{t+28}" width="34" height="5" fill="{Q["orange2"]}"/><ellipse cx="{a+17}" cy="{t+3}" rx="13" ry="3" fill="{Q["orange2"]}"/>' for a,t in ((8,48),(44,48),(80,48),(26,6),(62,6))) + f'<rect x="96" y="22" width="22" height="22" rx="4" fill="{Q["tan"]}"/><rect x="107" y="22" width="11" height="22" rx="3" fill="{Q["tan2"]}"/></g>'
def torchD(x,y): return f'<g transform="translate({x} {y})"><rect x="0" y="22" width="14" height="6" rx="2" fill="{Q["lav2"]}"/><rect x="5" y="16" width="6" height="22" rx="2" fill="{Q["brown2"]}"/><path d="M8 0 C0 8 2 16 8 16 C14 16 16 8 8 0 Z" fill="{Q["mustard"]}"/><path d="M8 6 C5 10 6 14 8 14 C10 14 11 10 8 6 Z" fill="{Q["coral"]}"/></g>'
def rugD(x,y): return f'<g transform="translate({x} {y})"><rect x="0" y="0" width="120" height="70" rx="10" fill="{Q["navy"]}"/><rect x="8" y="8" width="104" height="54" rx="6" fill="{Q["navy2"]}"/><rect x="18" y="18" width="84" height="34" rx="4" fill="{Q["coral"]}"/><path d="M60 22 L74 35 L60 48 L46 35 Z" fill="{Q["mustard"]}"/>' + ''.join(f'<rect x="{6+k*12}" y="-6" width="3" height="6" fill="{Q["cream2"]}"/><rect x="{6+k*12}" y="70" width="3" height="6" fill="{Q["cream2"]}"/>' for k in range(10)) + '</g>'
def catbed(x,y): return f'<g transform="translate({x} {y})"><ellipse cx="34" cy="30" rx="34" ry="16" fill="{Q["tan2"]}"/><ellipse cx="34" cy="26" rx="30" ry="12" fill="{Q["tan"]}"/><ellipse cx="34" cy="24" rx="20" ry="8" fill="{Q["coral"]}"/></g>'
tiles=''.join(f'<rect x="{c*44}" y="{r*44}" width="44" height="44" fill="{"#b5653a" if (r+c)%2 else "#a35a33"}"/>' + (f'<path d="M{c*44+8} {r*44+8} l6 0" stroke="#c4744a" stroke-width="2"/>' if rk.random()<.25 else '') for r in range(20) for c in range(9))
KH=f"""<rect x="0" y="0" width="390" height="214" fill="{Q["lav"]}"/>{''.join(f'<rect x="{(r%2)*20+k*40-10}" y="{r*22+4}" width="34" height="16" rx="3" fill="#978f83" opacity=".5"/>' for r in range(9) for k in range(11))}<rect x="0" y="200" width="390" height="14" fill="{Q["lav2"]}"/>
  {window(24,70)}{window(322,70)}{herbs(92,64)}{herbs(228,64)}
  <rect x="96" y="20" width="198" height="5" rx="2" fill="{Q["brown2"]}"/>{kpot(112,24)}{kpot(146,24,.9)}{kpot(228,24,.9)}{kpot(260,24)}
  <path d="M164 214 L164 150 C164 118 226 118 226 150 L226 214 Z" fill="{Q["brown"]}"/><path d="M195 122 C214 124 226 136 226 150 L226 214 L195 214 Z" fill="{Q["brown2"]}"/><rect x="164" y="160" width="62" height="5" fill="{Q["brown2"]}"/><rect x="164" y="188" width="62" height="5" fill="{Q["brown2"]}"/><circle cx="210" cy="176" r="4" fill="{Q["mustard"]}"/>"""
b=f'''<div style="{SC}background:#a35a33">
  <svg width="390" height="844" style="position:absolute;left:0;top:0">{tiles}{KH}
    <rect x="0" y="214" width="12" height="630" fill="{Q["lav2"]}"/><rect x="378" y="214" width="12" height="630" fill="{Q["lav2"]}"/>
    {rugD(150,740)}
    <path d="{road}" fill="none" stroke="{Q["cream2"]}" stroke-width="44" stroke-linecap="round" transform="translate(0 4)"/><path d="{road}" fill="none" stroke="{Q["cream"]}" stroke-width="42" stroke-linecap="round"/><path d="{road}" fill="none" stroke="#f6ecd4" stroke-width="16" stroke-linecap="round"/>
    {hearthD(236,392)}{tableD(14,552)}{sacksD(250,686)}{barrelsD(14,236)}{bigshelf(286,230)}{catbed(24,450)}
    {torchD(14,330)}{torchD(362,540)}{torchD(14,680)}
  </svg>
  <div style="position:absolute;left:0;right:0;top:0;height:56px;background:{Q["purple"]};z-index:4">
    {pill(14,8,98,40,Q["mustard"],Q["mustard2"],'Castle',16)}<div style="position:absolute;left:126px;top:12px;{TT};font-size:24px;color:{Q["cream"]}">Kitchens</div><b style="position:absolute;right:16px;top:18px;font:700 15px Fredoka,sans-serif;color:{Q["cream"]}">7/30</b></div>
  {nodes(171)}
  <div style="position:absolute;left:122px;top:430px;z-index:4">{sv('mouse',36)}</div>
  <div style="position:absolute;left:40px;top:446px;z-index:2">{sv('cat',34)}</div>
</div>'''
boards['K']=('Kitchens',b)
