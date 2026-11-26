# Genspark 요청 꾸러미 만들기: python3 code/make_genspark.py
# → docs/genspark/GENSPARK_PROMPTS.md (붙여 넣을 지시문, 묶음별) + docs/genspark/refs.zip (캐릭터 참고 그림·지금의 임시 그림)
import os, sys, importlib, zipfile, glob
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(R, 'build')); sys.path.insert(0, os.path.join(R, 'build', 'content')); sys.path.insert(0, os.path.join(R, 'art'))
from gen import TOC, NAME
import covers
CHAR = {'doc': '박사(뾰족한 흑백 머리, 안경, 흰 가운과 검은 조끼)', 'asst': '조교 하루(분홍 머리 양쪽 똬리, 남색 앞머리 줄, 연보라 후드 위 흰 가운)', 'fly': '조교 초파리(사람 크기 초파리, 빨간 겹눈, 파란 헬멧, 투명 날개, 흰 가운)',
        'robo': '조교 주판봇(베이지색 네모 모니터 머리에 초록 화면 얼굴, 주판을 든 궤도 로봇)', 'sia': '시아(긴 검은 머리, 검은 원피스와 흰 앞치마)', 'moa': '모아(긴 밝은 갈색 머리, 머리띠, 갈색 카디건과 빨간 리본)',
        'x1': 'X1(검은 실루엣, 분홍 리본 포니테일)', 'x2': 'X2(검은 실루엣, 베레모와 동그란 청록 안경)', 'x3': 'X3(검은 실루엣, 고양이 귀 후드와 노란 방울)'}
ALL = '·'.join(CHAR[k].split('(')[0] for k in CHAR)
STYLE = ('스타일: 16비트 RPG 픽셀아트, 또렷한 픽셀 경계(안티에일리어싱 없음), 제한된 색, 밝은 낮의 흰 연구실(흰 벽·연회색 체크 바닥), '
         '첨부한 캐릭터 그림의 얼굴·머리·옷을 그대로 유지, 칠판의 짧은 수식 말고는 글자·로고·워터마크 없음.')
def board(key):
    for e in covers.COVERS[key]:
        if e[0] == 'board': return ' / '.join(e[5]) if len(e) > 5 else ''
    return ''
L = ['# Genspark 그림 요청 꾸러미 — 수리 도감', '',
     '## 쓰는 법', '1. Genspark 이미지 생성 창에 `refs.zip` 안의 캐릭터 참고 그림을 먼저 올립니다(characters/ 폴더 9장 + intro/ 6장).',
     '2. **묶음 0**(카드 단체 그림·목차 표지)부터 받아 그림체를 확인한 뒤, 그 목차 표지를 참고 그림으로 함께 올리고 나머지 묶음을 요청합니다.',
     '3. 한 번에 한 묶음(3~5장)씩, 같은 비율끼리 요청합니다. 각 지시문 앞에 아래 「공통 스타일」을 붙여 넣으세요.',
     '4. 받은 그림을 **저장 이름 그대로** 저장소 `img/genspark_in/`(카드 그림은 ahnboat_lab_cover_status의 `thumbs/chars/atlas/`)에 올려 주시면, 원래 격자로 줄여 정수배 무손실 WebP로 바꿔 반영합니다.', '',
     '## 공통 스타일 (모든 지시문 앞에)', '```text', STYLE, '```', '',
     '## 캐릭터 안내 (지시문에 이름이 나오면 이 모습)', ''] + [f'- {v}' for v in CHAR.values()] + ['']
L += ['## 묶음 0 — 먼저 받을 두 장', '',
      '### G00 · ahnboat.xyz 카드 단체 그림 → `crew_intro.png` (가로 2.7 : 세로 1, 배경 투명)', '```text',
      f'배경이 완전히 투명한 PNG 스프라이트, 가로로 긴 단체 그림(약 1300×480). 연구소 식구 아홉 명({ALL})이 모두 함께 커다랗게 펼쳐진 두꺼운 "도감" 책 주위에 모여 있다. '
      '책 펼친 면에는 픽셀로 그린 작은 그래프들(직선, 종 모양 곡선, 화살표, 행렬 격자)이 보인다. 박사는 앞줄 왼쪽에서 책을 가리키고, 하루·시아·모아는 뒷줄에서 책을 들여다보며 웃고, '
      '주판봇과 초파리는 앞줄 가운데, X1·X2·X3는 앞줄 오른쪽에서 책을 함께 받쳐 든다. 아홉 명 모두 몸 전체가 보이고 발끝이 아래 가장자리에 닿는다. 그림자·바닥·배경 없음.', '```',
      '- 비교용: 지금 카드에 걸린 임시 그림 `refs.zip/now/crew_intro_now.webp`', '',
      '### G01 · 목차 표지 → `cover_index.png` (16:9)', '```text',
      '16:9 표지. 흰 연구실 큰 칠판에 "f(x)  Ax=b  P(A|B)  σ²  ∂f/∂x  ∇f  λ  θ ← θ − α∇f"가 적혀 있다. 칠판 앞에 연구소 식구 아홉 명이 모두 나란히 서서 정면을 본다. '
      '박사가 가운데에서 지휘봉으로 칠판을 가리키고, 칠판 옆 책장에는 "도감"처럼 두꺼운 책 열다섯 권이 꽂혀 있다.', '```', '']
groups = [TOC[0:4], TOC[4:8], TOC[8:12], TOC[12:15]]
for gi, g in enumerate(groups):
    L += [f'## 묶음 {gi + 1} — 장 표지 (16:9){" + 실전 연습장" if gi == 3 else ""}', '']
    for key, out, slide, short, sub, host, part in g:
        others = '·'.join(CHAR[k].split('(')[0] for k in CHAR if k != host)
        L += [f'### {slide} · {short} → `cover_{key}.png`', '```text',
              f'16:9 표지. 흰 연구실 칠판에 "{board(key)}"가 적혀 있다. 연구소 식구 아홉 명이 모두 모여 있다: 이번 장 안내인 {CHAR[host]}가 맨 앞 가운데에 크게 서서 칠판을 소개하고, '
              f'나머지 여덟 명({others})은 뒷줄에 한 줄로 서서 함께 칠판을 본다. 장의 주제({sub})를 떠올리게 하는 작은 소품을 칠판 옆에 둔다.', '```']
    if gi == 3:
        L += ['### 마지막 장 · 실전 연습장 → `cover_practice.png`', '```text',
              '16:9 표지. 흰 연구실의 관제 모니터 벽(막대그래프, 내려가는 손실 곡선, 점 구름)과 칠판 "SHOP cos θ / CLINIC P(D|T) / TRAIN α / PCA k=1". 연구소 식구 아홉 명이 모두 모여 있고, 박사가 맨 앞 가운데에서 판정하는 손짓을, 나머지는 뒷줄에서 모니터를 본다.', '```']
    L.append('')
toons = []
for key, out, slide, short, sub, host, part in TOC:
    C = importlib.import_module(key).CH
    for i, t in enumerate(C['toons']): toons.append((slide, key, 'ab'[i], t))
for bi in range(0, len(toons), 4):
    L += [f'## 묶음 {5 + bi // 4} — 웃는 그림 (3:2)', '']
    for slide, key, ab, t in toons[bi:bi + 4]:
        L += [f'### {slide} · {t["title"]} → `{key}_{ab}.png`', '```text',
              f'3:2 한 컷 만화(말풍선 없이, 표정과 몸짓으로 웃기게). {t["alt"]} 그림 속 수학 포인트: {t.get("point", "")}', '```']
    L.append('')
L += ['## 저장 이름 체크리스트', '', '- [ ] crew_intro.png', '- [ ] cover_index.png'] + [f'- [ ] cover_{k}.png' for k, *_ in TOC] + ['- [ ] cover_practice.png'] + [f'- [ ] {k}_{ab}.png' for s, k, ab, t in toons]
open(os.path.join(R, 'docs', 'genspark', 'GENSPARK_PROMPTS.md'), 'w').write('\n'.join(L) + '\n')
CS = '/home/claude/ahnboat_lab_cover_status/thumbs/chars/atlas'
z = zipfile.ZipFile(os.path.join(R, 'docs', 'genspark', 'refs.zip'), 'w', zipfile.ZIP_DEFLATED)
for f in sorted(glob.glob(CS + '/*_intro.webp')):
    if 'crew' in f: z.write(f, 'now/crew_intro_now.webp')
    else: z.write(f, 'intro/' + os.path.basename(f))
spr = os.path.join('/home/claude/work/spr')
for k, e in [('doc', 'doc_e08'), ('asst', 'asst_e13'), ('fly', 'fly_e08'), ('robo', 'robo_e13'), ('sia', 'sia_e13'), ('moa', 'moa_e13'), ('x1', 'x1_e13'), ('x2', 'x2_e13'), ('x3', 'x3_e13')]:
    z.write(os.path.join(spr, e + '.png'), f'characters/{k}.png')
for f in ['img/cover_index.webp', 'img/cover_ch01.webp', 'img/toon/ch01_a.webp']:
    z.write(os.path.join(R, f), 'now/' + os.path.basename(f))
z.close()
print(len(L), '줄 ·', 2 + 16 + len(toons), '장')
