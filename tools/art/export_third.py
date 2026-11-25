# Adds the Third floor's drawings (gen22.py, then gen23.py) to the game's room-art.json.
# Run from this folder: python3 gen22.py && python3 gen23.py && python3 export_third.py
import json
F = '../../web/src/main/webapp/room-art.json'
d = json.load(open(F))
a = json.load(open('third_floor_art.json'))
b = json.load(open('third_floor_art2.json'))
props = dict(a['props'])
props['guard_stool'] = props.pop('stool')   # 'stool' and 'tub' are the Kitchens' pieces
props['bath_tub'] = props.pop('tub')
props.update(b['props'])
for k in ('block_tower', 'blocks_s', 'pinwheel', 'spin_top', 'fan', 'petals', 'perfume',
          'blocks_fun', 'blocks_eek', 'blocks_yay', 'blocks_toy', 'stool_unused'):
    props.pop(k, None)
heads = dict(a['heads']); heads.update(b['heads'])
d['heads'].update(heads); d['props'].update(props)
json.dump(d, open(F, 'w'), separators=(',', ':'), ensure_ascii=False)
print('room-art.json updated:', len(d['heads']), 'walls,', len(d['props']), 'pieces')
