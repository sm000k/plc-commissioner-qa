import re

with open('docs/qa_draft_v7.md', encoding='utf-8') as f:
    lines = f.readlines()

sections = []
current_sec = None

for i, l in enumerate(lines):
    ls = l.rstrip()
    m = re.match(r'^\s{2}(\d+)\. ', ls)
    m2 = re.match(r'^## (\d+)\. ', ls)
    if m:
        sec_num = int(m.group(1))
        sections.append({'num': sec_num, 'line': i+1, 'title': ls.strip(), 'questions': []})
        current_sec = sections[-1]
    elif m2:
        sec_num = int(m2.group(1))
        sections.append({'num': sec_num, 'line': i+1, 'title': ls.strip(), 'questions': []})
        current_sec = sections[-1]
    elif ls.startswith('### ') and current_sec is not None:
        m3 = re.match(r'^### (\d+(?:\.\d+)?)\. ', ls)
        if m3:
            current_sec['questions'].append({'line': i+1, 'text': ls[:80], 'num': m3.group(1)})

for s in sections:
    print(f"SEC {s['num']} (L{s['line']}): {s['title'][:60]}")
    for q in s['questions']:
        print(f"  Q{q['num']} L{q['line']}: {q['text'][:72]}")
