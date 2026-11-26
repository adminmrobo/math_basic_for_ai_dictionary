# 그림 지시문 문서 만들기: python3 code/make_docs.py → docs/IMAGE_PROMPTS.md
# 표지 17장(1920×1080, 480×270 격자)·웃는 그림 30장(1200×800, 600×400 격자)의 생성 AI 지시문을 장 내용에서 모은다.
import os, sys, importlib
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(R, 'build')); sys.path.insert(0, os.path.join(R, 'build', 'content'))
from gen import TOC, NAME, cover_alt
STYLE = ('16-bit RPG pixel art, crisp hard pixel edges, limited palette, bright daytime laboratory with a WHITE background and light grey checker floor, '
         'chibi characters from the attached character sheet (keep faces, hair and clothes exactly), no text except the short math formulas given, no logos, no watermark.')
L = ['# 그림 지시문 — 수리 도감', '', '지금 저장소의 표지·웃는 그림은 연구소 캐릭터 팩(96px)과 픽셀 도형으로 조립한 **임시 그림**입니다(art/scenes.py).',
     '아래 지시문으로 생성 도구(Genspark 등)에서 그린 뒤, 원래 격자(표지 480×270, 웃는 그림 600×400)로 줄여 NEAREST 정수배(표지 ×4, 웃는 그림 ×2)로 키운 **무손실 WebP**로 같은 파일 이름에 덮어쓰면 됩니다.', '',
     '- 첨부: 캐릭터 기본 그림(박사·하루·초파리·주판봇·시아·모아·X1~X3) — github.com/adminmrobo/fruitfly-lab-expressions',
     '- 순서: 목차 표지를 먼저 받아 그림체를 확인 → 나머지에 그 표지를 참고 그림으로 함께 올리기', '- 공통 스타일: `' + STYLE + '`', '- 금지: 그림 속 긴 한글 문장(말풍선 대사는 페이지의 HTML이 맡음)', '']
L += ['## 표지 (img/cover_*.webp, 16:9)', '', '| 파일 | 지시문 |', '|---|---|',
      '| cover_index.webp | White lab, big blackboard with "f(x)  Ax=b  P(A|B)  σ²  ∂f/∂x  ∇f  λ  θ ← θ − α∇f", all nine lab members lined up in front (Doctor center). |',
      '| cover_practice.webp | Control room with monitors showing bar charts and a loss curve, blackboard "SHOP cos θ / CLINIC P(D|T) / TRAIN α / PCA k=1", all nine lab members gathered, Doctor in front center. |']
for key, out, slide, short, sub, host, part in TOC:
    C = importlib.import_module(key).CH
    L.append(f'| cover_{key}.webp | {slide} {short} — 연구소 식구 아홉 명이 모두 모인 장면, 안내 {NAME[host]}가 맨 앞 가운데. {cover_alt(key)} 칠판 식과 소품: {C["cover_alt"]} |')
L += ['', '## 웃는 그림 (img/toon/*_a.webp, *_b.webp, 3:2)', '']
for key, out, slide, short, sub, host, part in TOC:
    C = importlib.import_module(key).CH
    L.append(f'### {slide} {short}')
    for i, t in enumerate(C['toons']):
        L.append(f'- **{key}_{"ab"[i]}.webp · {t["title"]}** — {t["alt"]}')
    L.append('')
open(os.path.join(R, 'docs', 'IMAGE_PROMPTS.md'), 'w').write('\n'.join(L) + '\n')
print('docs/IMAGE_PROMPTS.md', len(L), '줄')
