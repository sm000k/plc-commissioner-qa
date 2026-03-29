import subprocess, sys, time, re
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi

result = subprocess.run(
    ['yt-dlp','--flat-playlist','--playlist-end','5',
     '--print','%(id)s|%(title)s|%(upload_date)s',
     'https://www.youtube.com/@controlbytepl/videos'],
    capture_output=True, encoding='utf-8', errors='replace'
)
videos = []
for line in result.stdout.strip().splitlines():
    p = line.split('|', 2)
    if len(p) == 3:
        videos.append({'id': p[0], 'title': p[1], 'date': p[2]})

print(f'Znaleziono filmow: {len(videos)}')
OUT = Path('transcripts/controlbyte')
OUT.mkdir(parents=True, exist_ok=True)
api = YouTubeTranscriptApi()

for v in videos:
    try:
        tl = api.list(v['id'])
        t = list(tl)[0]
        data = t.fetch()
        text = ' '.join(seg.text for seg in data)
        safe = re.sub(r'[<>:"/\\|?*]', '', v['title'])[:80]
        fname = OUT / f"{v['date']}_{safe}.txt"
        fname.write_text(f"# {v['title']}\n# {v['id']}\n\n{text}", encoding='utf-8')
        print(f"OK [{t.language_code}]: {fname.name}")
    except Exception as e:
        print(f"BRAK: {v['title']} -- {e}")
    time.sleep(0.3)

print('DONE')
