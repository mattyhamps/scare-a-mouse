# Adds the Royal floor's drawings (gen25.py) to the game's room-art.json.
# Run from this folder: python3 gen25.py && python3 export_royal.py
import json
F = '../../web/src/main/webapp/room-art.json'
d = json.load(open(F, encoding='utf-8'))
a = json.load(open('royal_floor_art.json', encoding='utf-8'))
d['heads'].update(a['heads']); d['props'].update(a['props'])
for gone in ('shoes_s', 'parasol_stand'): d['props'].pop(gone, None)   # replaced by bigger pieces
json.dump(d, open(F, 'w', encoding='utf-8'), separators=(',', ':'), ensure_ascii=False)
print('room-art.json updated:', len(d['heads']), 'walls,', len(d['props']), 'pieces')
