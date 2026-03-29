import re
import shutil

src = 'docs/qa_draft_v7.md'
shutil.copy(src, src + '.bak')

with open(src, encoding='utf-8') as f:
    lines = f.readlines()

current_sec = None
out = []

for line in lines:
    ls = line.rstrip('\n')

    # Detect section header (both styles)
    m = re.match(r'^\s{2}(\d+)\. ', ls)
    m2 = re.match(r'^## (\d+)\. ', ls)
    if m:
        current_sec = int(m.group(1))
        out.append(line)
        continue
    elif m2:
        current_sec = int(m2.group(1))
        out.append(line)
        continue

    # Rewrite ### N. or ### N.M. question headers only (not other ### lines)
    if ls.startswith('### ') and current_sec is not None:
        # Match ### followed by a plain number (possibly already X.Y)
        m3 = re.match(r'^(### )(\d+)\. (.+)$', ls)
        if m3:
            prefix, q_num, rest = m3.group(1), m3.group(2), m3.group(3)
            new_line = f"{prefix}{current_sec}.{q_num}. {rest}\n"
            out.append(new_line)
            continue

    out.append(line)

with open(src, 'w', encoding='utf-8') as f:
    f.writelines(out)

print("Done. Backup: docs/qa_draft_v7.md.bak")
# Verify: show first few renumbered headers
with open(src, encoding='utf-8') as f:
    for i, l in enumerate(f):
        if l.startswith('### ') and re.match(r'^### \d+\.\d+\.', l):
            print(f"L{i+1}: {l.rstrip()[:80]}")
