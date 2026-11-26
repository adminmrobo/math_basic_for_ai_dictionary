# 내부 링크 검사: 모든 페이지의 a[href="파일#앵커"]가 실제 파일·id를 가리키는지 (스크립트 속 공식 도감 링크 포함)
import os, re, glob, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages = glob.glob(os.path.join(R, '*.html')) + glob.glob(os.path.join(R, 'practice', '*.html'))
ids = {os.path.relpath(p, R): set(re.findall(r'id="([^"]+)"', open(p).read())) for p in pages}
bad = 0
for p in pages:
    rel = os.path.relpath(p, R); base = os.path.dirname(rel)
    H = open(p).read()
    hrefs = re.findall(r'href="([^"]+)"', H) + ([] if rel.startswith('practice') else re.findall(r"'([0-9]{2}_[a-z_]+\.html#[a-z0-9-]+)'", H) + re.findall(r'"([0-9]{2}_[a-z_]+\.html#[a-z0-9-]+)"', H))
    for h in set(hrefs):
        if h.startswith(('http', 'mailto', 'data:', 'javascript')) or "'" in h or '+' in h: continue
        f, _, a = h.partition('#')
        tgt = os.path.normpath(os.path.join(base, f)) if f else rel
        if f and not os.path.exists(os.path.join(R, tgt)): print('없는 파일', rel, h); bad += 1; continue
        if a and tgt in ids and a not in ids[tgt] and a not in ('kg', 'export'):
            print('없는 앵커', rel, h); bad += 1
print('링크 검사', '통과' if not bad else f'실패 {bad}'); sys.exit(1 if bad else 0)
