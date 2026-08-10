import re
html = open('r.md', encoding='utf-8').read()
rows = re.findall(r'<tr>(.*?)</tr>', html, re.S)
out, last = [], '?'
for r in rows:
    tds = re.findall(r'<td>(.*?)</td>', r, re.S)
    if len(tds) < 4: continue
    m = re.search(r'simplify\.jobs/c/[^"]*"[^>]*>([^<]+)</a>', tds[0])
    company = m.group(1).strip() if m else re.sub(r'<[^>]+>','',tds[0]).strip()
    if company in ('↳',''): company = last
    else: last = company
    role = re.sub(r'<[^>]+>','',tds[1]).strip()
    loc  = ' '.join(re.sub(r'<[^>]+>',' ',tds[2]).split())
    lm = re.search(r'href="(https?://(?!simplify\.jobs)[^"]+)"', tds[3])
    link = lm.group(1).split('?')[0] if lm else ''
    out.append(f"{company} | {role} | {loc} | {link}")
print('\n'.join(sorted(set(out))))
