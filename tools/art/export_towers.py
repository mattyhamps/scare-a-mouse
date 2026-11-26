# Adds the Towers and roof's drawings (gen26.py) to the game's room-art.json.
# Run from this folder: python3 gen26.py && python3 export_towers.py
import json
F = '../../web/src/main/webapp/room-art.json'
d = json.load(open(F, encoding='utf-8'))
a = json.load(open('towers_art.json', encoding='utf-8'))
d['heads'].update(a['heads']); d['props'].update(a['props'])
json.dump(d, open(F, 'w', encoding='utf-8'), separators=(',', ':'), ensure_ascii=False)
print('room-art.json updated:', len(d['heads']), 'walls,', len(d['props']), 'pieces')
