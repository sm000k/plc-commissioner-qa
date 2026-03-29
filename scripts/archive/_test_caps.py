import requests, json, re

VIDEO_ID = 'hlRvFncPqmI'
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept-Language': 'pl,en-US;q=0.9,en;q=0.8',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
})

# Get video page
page_url = f'https://www.youtube.com/watch?v={VIDEO_ID}'
r = session.get(page_url, timeout=15)
print('Page status:', r.status_code)
print('Cookies set:', list(session.cookies.keys())[:5])

# Find caption tracks in page source
m = re.search(r'"captionTracks":\[(.+?)\]', r.text)
if m:
    caps_json = '[' + m.group(1) + ']'
    caps = json.loads(caps_json)
    for c in caps:
        lang = c.get('languageCode', '')
        base_url = c.get('baseUrl', '')
        kind = c.get('kind', '')
        print(f'  Caption: {lang} ({kind}) -> {base_url[:100]}...')
        if 'pl' in lang:
            # Try downloading the caption
            cap_url = base_url + '&fmt=json3'
            r2 = session.get(cap_url, timeout=15)
            print(f'  Download status: {r2.status_code}, size: {len(r2.content)} bytes')
            if r2.status_code == 200:
                data = r2.json()
                events = data.get('events', [])
                words = []
                for evt in events:
                    for seg in evt.get('segs', []):
                        w = seg.get('utf8', '').strip()
                        if w and w != '\n':
                            words.append(w)
                text = ' '.join(words)
                print(f'  Transcript preview: {text[:200]}')
else:
    print('No captionTracks found in page source')
    # Print first 200 chars around "caption" to debug
    idx = r.text.find('caption')
    if idx > 0:
        print('Context:', r.text[idx:idx+200])
