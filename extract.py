import re, sys

SECTION = "Software Engineering Internship Roles"

html = open('r.md', encoding='utf-8').read()

# Slice out only the target section: from its ## heading to the next ## heading.
heads = [(m.start(), m.group(0)) for m in re.finditer(r'(?m)^[ \t]*##[ \t]+.*$', html)]
start = next((i for i, (_, t) in enumerate(heads) if SECTION in t), None)
if start is None:
    sys.stderr.write("FATAL: section heading not found; parser needs updating\n")
    sys.exit(1)
begin = heads[start][0]
end = heads[start + 1][0] if start + 1 < len(heads) else len(html)
section = html[begin:end]

rows = re.findall(r'<tr>(.*?)</tr>', section, re.S)
out, last = [], '?'
for r in rows:
    tds = re.findall(r'<td>(.*?)</td>', r, re.S)
    if len(tds) < 4:
        continue
    m = re.search(r'simplify\.jobs/c/[^"]*"[^>]*>([^<]+)</a>', tds[0])
    company = m.group(1).strip() if m else re.sub(r'<[^>]+>', '', tds[0]).strip()
    if company in ('↳', '&#8627;', ''):
        company = last
    else:
        last = company
    role = re.sub(r'<[^>]+>', '', tds[1]).strip()
    loc = ' '.join(re.sub(r'<[^>]+>', ' ', tds[2]).split())
    lm = re.search(r'href="(https?://(?!simplify\.jobs)[^"]+)"', tds[3])
    link = lm.group(1).split('?')[0] if lm else ''
    out.append(f"{company} | {role} | {loc} | {link}")

if not out:
    sys.stderr.write("FATAL: section found but zero rows parsed; markup changed\n")
    sys.exit(1)

print('\n'.join(sorted(set(out))))
