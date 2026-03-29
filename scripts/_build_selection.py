import subprocess, json, re
from pathlib import Path

result = subprocess.run(
    ['yt-dlp', '--flat-playlist', '--print', '%(id)s\t%(title)s\t%(upload_date)s',
     'https://www.youtube.com/@controlbytepl/videos'],
    capture_output=True, encoding='utf-8', errors='replace'
)
videos = []
for line in result.stdout.strip().splitlines():
    parts = line.split('\t', 2)
    if len(parts) == 3:
        videos.append({'id': parts[0].strip(), 'title': parts[1].strip(), 'date': parts[2].strip()})

EXCLUDE_KEYWORDS = [
    'beckhoff', 'codesys', 'finder', 'scada', 'inovance',
    'home assistant', 'homeassistant', 'chatgpt', 'lenze', 'opta',
    r'\bai\b', 'sztuczna inteligencja', 'machine learning',
    'wago'
]

log = json.loads(Path('transcripts/controlbyte/_log.json').read_text(encoding='utf-8'))

keep = []
skip_excluded = []
skip_done = []

for v in videos:
    t = v['title'].lower()
    if log.get(v['id'], {}).get('status') == 'ok':
        skip_done.append(v)
    elif any(re.search(kw, t) for kw in EXCLUDE_KEYWORDS):
        skip_excluded.append(v)
    else:
        keep.append(v)

print(f"=== DO POBRANIA ({len(keep)}) ===")
for v in keep:
    print(f"  [{v['date']}] {v['title']}")

print(f"\n=== JUZ POBRANE ({len(skip_done)}) ===")
for v in skip_done:
    print(f"  {v['title']}")

print(f"\n=== WYKLUCZONE TEMATYCZNIE ({len(skip_excluded)}) ===")
for v in skip_excluded:
    print(f"  {v['title']}")

sel = [v['id'] for v in keep]
Path('transcripts/controlbyte/_selection.json').write_text(
    json.dumps(sel, ensure_ascii=False), encoding='utf-8')
print(f"\nZapisano selekcje: {len(sel)} filmow -> _selection.json")
