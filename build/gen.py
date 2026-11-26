# -*- coding: utf-8 -*-
"""수리 도감 — 페이지 원본(*.src.html) 생성기.
장마다 build/content/chNN.py가 CH 사전을 내고, 이 파일이 같은 틀
(표지 → 히어로 → 3줄 → 안내 담당 → 큰 그림 → 도감 항목 → 웃는 그림 → 실험실 → AI 판단 → 코랩 실습실 → 정리 → 아웃트로)으로 엮는다.
그다음 node build/build.js가 CSS·캐릭터·모듈·지식 색인을 붙여 완성 HTML을 만든다.
코랩 노트북(colab/*.ipynb)과 파이썬 파일(code/colab_py/*.py)도 여기서 만든다."""
import json, os, importlib, sys, html
B = os.path.dirname(os.path.abspath(__file__))
R = os.path.dirname(B)
sys.path.insert(0, os.path.join(B, 'content'))
SITE = 'https://adminmrobo.github.io/math_basic_for_ai_dictionary/'
REPO = 'adminmrobo/math_basic_for_ai_dictionary'
AUTHOR = '글 · 안상선 ((주)M-Robo 대표) · <a href="https://adminmrobo.github.io/who_am_i/who_am_i.html">저자 소개</a>'
SERIES = '수리 도감 — 인공지능을 위한 수리적 기초'
DATE = '2026-11-26'
VER = 'v1.0'
KEYS = ['ch%02d' % i for i in range(1, 16)]

NAME = {'doc': '박사', 'asst': '조교 하루', 'fly': '조교 초파리', 'robo': '조교 주판봇', 'sia': '시아', 'moa': '모아', 'x1': 'X1', 'x2': 'X2', 'x3': 'X3'}
MOOD = {'doc': 'doc_board', 'asst': 'asst_smile', 'fly': 'fly_point', 'robo': 'robo_calc', 'sia': 'sia_smile', 'moa': 'moa_smile', 'x1': 'x1_hint', 'x2': 'x2_hint', 'x3': 'x3_hint'}
CAST = [
    ('doc', 'doc_board', '박사', '연구소 책임자. 장마다 상황 질문으로 문을 열고 해석 문장으로 닫아요.'),
    ('asst', 'asst_smile', '조교 하루', '수식 담당. 기호 하나씩 읽는 법과 뜻부터 풀어 줘요.'),
    ('fly', 'fly_point', '조교 초파리', '실험 담당. "이걸 눌러 봐"로 실험판을 열고, 답이 그럴듯한지 의심해요.'),
    ('robo', 'robo_calc', '조교 주판봇', '계산 담당. 1초 만에 답을 내지만 가끔 너무 빨라요. AI 판단 코너의 단골.'),
    ('sia', 'sia_smile', '시아', '직관파 연구원. 비유부터 꺼내 "그러니까 이런 거죠?"라고 물어요.'),
    ('moa', 'moa_smile', '모아', '꼼꼼파 연구원. "그건 언제나 그래요?" 하고 조건과 예외를 물어요.'),
    ('x1', 'x1_hint', 'X1', '막내 연구원. 손을 번쩍 들고 엉뚱한 질문을 해요.'),
    ('x2', 'x2_hint', 'X2', '막내 연구원. 필기를 가장 열심히 해요.'),
    ('x3', 'x3_hint', 'X3', '막내 연구원. 게임과 퀴즈 시간에 가장 신나요.'),
]
# 열다섯 장의 자리 (목차·큰 그림·이전/다음 링크가 함께 쓴다)
TOC = [
    ('ch01', '01_math_basics.html', 'MATH-01', '수학 기초', '변수·식·함수', 'doc', '기초'),
    ('ch02', '02_linear_algebra.html', 'MATH-02', '선형대수 기초', '스칼라·벡터·행렬', 'asst', '선형대수'),
    ('ch03', '03_vector_ops.html', 'MATH-03', '벡터 연산', '더하기·내적·길이·각도', 'fly', '선형대수'),
    ('ch04', '04_matrix_ops.html', 'MATH-04', '행렬 연산', '곱셈·전치·역행렬', 'robo', '선형대수'),
    ('ch05', '05_linear_systems.html', 'MATH-05', '연립일차방정식', 'Ax = b와 회귀', 'sia', '선형대수'),
    ('ch06', '06_probability.html', 'MATH-06', '확률 기초', '사건·덧셈·곱셈', 'x1', '확률·통계'),
    ('ch07', '07_bayes.html', 'MATH-07', '조건부 확률과 베이즈', '새 정보로 고치는 믿음', 'moa', '확률·통계'),
    ('ch08', '08_statistics.html', 'MATH-08', '통계 기초', '평균·분산·사분위', 'x2', '확률·통계'),
    ('ch09', '09_distributions.html', 'MATH-09', '확률분포', '이항·포아송·정규', 'x3', '확률·통계'),
    ('ch10', '10_correlation.html', 'MATH-10', '상관과 공분산', '함께 움직이는 정도', 'sia', '확률·통계'),
    ('ch11', '11_calculus.html', 'MATH-11', '미적분 기초', '극한·미분·적분', 'robo', '미적분·최적화'),
    ('ch12', '12_gradient.html', 'MATH-12', '편미분과 그래디언트', '여러 방향의 기울기', 'asst', '미적분·최적화'),
    ('ch13', '13_optimization.html', 'MATH-13', '최적화', '경사하강과 학습률', 'fly', '미적분·최적화'),
    ('ch14', '14_eigen_pca.html', 'MATH-14', '고윳값·고유벡터와 PCA', '데이터의 주축 찾기', 'doc', '응용'),
    ('ch15', '15_quick_revision.html', 'MATH-15', '총정리', '공식 도감과 실전 예제', 'x3', '총정리'),
]
TOCD = {t[0]: t for t in TOC}
# 같은 원자료를 이야기(생선 가게 AI 모델)로 풀어 쓴 자매 시리즈 「인공지능을 위한 수학」의 같은 주제 방
MFA = 'https://adminmrobo.github.io/math_for_ai_lab/'
SIS = {'ch01': ('index.html#c01', '1부 1장 함수'), 'ch02': ('index.html#c02', '1부 2장 행렬'), 'ch03': ('index.html#c03', '1부 3장 벡터 연산'), 'ch04': ('index.html#c04', '1부 4장 행렬 연산'),
       'ch05': ('index.html#c05', '1부 5장 연립방정식'), 'ch06': ('part2.html#c09', '2부 9장 확률 기초'), 'ch07': ('part2.html#c10', '2부 10장 조건부 확률·베이즈'), 'ch08': ('part2.html#c06', '2부 6장 통계 기초'),
       'ch09': ('part2.html#c11', '2부 11장 확률분포'), 'ch10': ('part2.html#c07', '2부 7장 상관·공분산'), 'ch11': ('part3.html#c13', '3부 13장 미적분 기초'), 'ch12': ('part3.html#c14', '3부 14장 편미분·그래디언트'),
       'ch13': ('part3.html#c15', '3부 15장 최적화'), 'ch14': ('part2.html#c08', '2부 8장 고유값·PCA'), 'ch15': ('index.html', '1~3부 전체')}


def esc(s):
    return html.escape(str(s), quote=True)


def dlg_html(key):
    return f'<div data-dlg="{key}"></div>'


def entry(e, no):
    tries = ''.join(f'<li>{t}</li>' for t in e['tryl'])
    rows = ''.join(f'<tr><td class="m">{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in e.get('eq', []))
    eq = (f'<details class="eqx"><summary>식으로 보면 (몰라도 됩니다)</summary><table class="ez-tb"><thead><tr><th>식 조각</th><th>읽는 법</th><th>뜻</th></tr></thead><tbody>{rows}</tbody></table></details>' if rows else '')
    warn = f'<p class="dexwarn"><b>헷갈리기 쉬운 점</b> {e["warn"]}</p>' if e.get('warn') else ''
    return (f'<article class="dex" id="{e["id"]}" data-dex="{esc(e["ko"])}">'
            f'<header><span class="dexno">{no}</span><h3>{e["ko"]} <small>{e["en"]}</small></h3></header>'
            f'<p class="one">{e["one"]}</p>'
            f'<div class="dexgrid"><div class="dw"><b>말로 먼저</b> {e["words"]}</div>'
            f'<div class="try"><b>숫자로 한 번 해 보기</b><ol>{tries}</ol></div></div>'
            f'<div class="pair"><div><div class="tl">학교 수학으로 보면</div>{e["school"]}</div><div><div class="tr">AI에서는</div>{e["ai"]}</div></div>'
            f'{warn}{eq}</article>')


def why_box(w):
    return ('<details class="ez-why" open><summary>왜 이 방법을 쓰나</summary><ol>'
            f'<li>문제: {w["problem"]}</li><li>앞 방법의 한계: {w["limit"]}</li><li><b>이 방법의 해법: {w["solve"]}</b></li></ol>'
            f'<p class="ez-easy"><b>쉽게 말하면</b> {w["easy"]}</p></details>')


def math_box(m):
    who = m.get('who', 'sia')
    rows = ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in m['rows'])
    tries = ''.join(f'<li>{t}</li>' for t in m['tries'])
    return ('<div class="ez-math"><div class="ez-t">연구원이 묻고, 조교 하루가 풀어 봅니다</div>'
            f'<div class="ez-q"><img data-mood="{m.get("qmood", MOOD[who])}" alt="" aria-hidden="true"><p><b style="display:block;font-size:12.5px;color:var(--muted)">{NAME[who]}</b>{m["q"]}</p></div>'
            f'<p><b>말로 먼저</b> {m["words"]}</p>'
            f'<p><b>학교 수학으로 보면</b> {m["school"]}</p>'
            f'<div class="try" style="background:#fff;border:1px dashed #e8b67a;border-radius:10px;padding:10px 14px"><b>숫자로 한 번 해 보기</b><ol style="margin:6px 0 0;padding-left:22px">{tries}</ol></div>'
            '<details class="eqx"><summary>식으로 보면 (몰라도 됩니다)</summary>'
            f'<table class="ez-tb"><thead><tr><th>식 조각</th><th>읽는 법</th><th>뜻</th></tr></thead><tbody>{rows}</tbody></table></details>'
            f'<div class="ez-q ez-c"><img data-mood="{m.get("cmood", "asst_spark")}" alt="" aria-hidden="true"><p><b style="display:block;font-size:12.5px;color:var(--muted)">조교 하루</b>{m["comment"]}</p></div></div>')


def ai_box(a):
    qs = ''.join(f'<li>{q}</li>' for q in a['checks'])
    return (f'<div class="aibox" id="ai"><div class="aihead"><span class="aitag">AI 판단 코너</span>{a["title"]}</div>'
            f'<div data-dlg="ai_d"></div>'
            f'<p>박사는 늘 두 가지를 묻습니다. "가정이 맞나? 숫자가 그럴듯한가?"</p><ol>{qs}</ol>'
            f'<details class="eqx"><summary>확인해 보기 (먼저 스스로 따져 본 뒤 펼치세요)</summary><p class="aiverdict">{a["verdict"]}</p>'
            f'<div data-dlg="ai_e"></div></details></div>')


def toon(t, key, i):
    lines = ''.join(f'<div class="tline"><img data-mood="{m}" alt="" aria-hidden="true"><p><b>{NAME[w]}</b> {s}</p></div>' for w, m, s in t['lines'])
    ab = 'ab'[i]
    return (f'<figure class="toon" id="toon{i+1}"><div class="tframe"><img src="img/toon/{key}_{ab}.webp" width="1200" height="800" loading="lazy" alt="{esc(t["alt"])}"></div>'
            f'<figcaption><b class="ttl">웃는 그림 {i+1} · {t["title"]}</b>{lines}'
            f'{"<p class=tpoint><b>그림 속 수학</b> " + t["point"] + "</p>" if t.get("point") else ""}</figcaption></figure>')


def colab(C):
    key = C['key']
    nb = f'colab/{key}_{C["slug"]}.ipynb'
    url = f'https://colab.research.google.com/github/{REPO}/blob/main/{nb}'
    code = esc(C['code'].strip('\n'))
    prompt = esc(C['prompt'].strip('\n'))
    out = esc(C.get('_output', '').rstrip())
    tasks = ''.join(f'<li>{t}</li>' for t in C['tasks'])
    return f'''<section class="sec" id="colab" aria-labelledby="h-colab"><div class="wrap">
<h2 id="h-colab"><span class="hex">실습</span>코랩 실습실 — 배운 것을 직접 돌려 보기</h2>
<p>두 가지 방법이 있어요. ① 생성 AI에게 프롬프트를 주고 코드를 만들게 해 보기, ② 연구소가 미리 만들어 검사까지 마친 코드를 돌려 보기. 둘을 나란히 돌려 결과를 비교하면, AI가 낸 코드를 믿어도 되는지 스스로 판단하는 연습이 됩니다.</p>
<div data-dlg="colab"></div>
<div class="labbox"><div class="labh"><span class="lno">①</span> 생성 AI로 실습하기 — 코랩 파이썬 프롬프트</div>
<p>구글 코랩(Colab)의 Gemini 창이나 ChatGPT·Claude 같은 생성 AI에 아래 글을 그대로 붙여 넣으세요. AI가 만든 코드를 코랩 셀에 붙여 넣고 실행합니다.</p>
<div class="codewrap"><button type="button" class="cpy" data-copy="p-{key}">복사</button><pre class="prompt" id="p-{key}">{prompt}</pre></div></div>
<div class="labbox"><div class="labh"><span class="lno">②</span> 실제로 돌아가는 코드 — 파이썬 · 코랩</div>
<p>연구소가 직접 실행해 결과를 확인한 코드입니다. 버튼 하나로 코랩에서 바로 열 수 있어요(구글 계정만 있으면 설치할 것이 없습니다).</p>
<p class="colabbtns"><a class="bt primary" href="{url}" target="_blank" rel="noopener">코랩에서 열기</a> <a class="bt" href="code/colab_py/{key}_{C["slug"]}.py" download>.py 내려받기</a> <a class="bt" href="{nb}" download>.ipynb 내려받기</a></p>
<details class="fold"><summary>코드 펼치기 (몰라도 됩니다 · {C["code"].count(chr(10))}줄)</summary><div class="codewrap"><button type="button" class="cpy" data-copy="c-{key}">복사</button><pre class="code" id="c-{key}"><code>{code}</code></pre></div></details>
<details class="fold"><summary>실행하면 이렇게 나옵니다 (연구소에서 돌린 결과)</summary><pre class="out">{out}</pre><p class="muted" style="font-size:13px">그래프 창은 코랩 화면에 함께 나타납니다. 무작위 실험이 있는 코드는 seed를 고정해 같은 숫자가 나오게 했어요.</p></details></div>
<div class="labbox"><div class="labh"><span class="lno">③</span> 비교 과제 — AI 코드와 연구소 코드 맞대 보기</div><ol>{tasks}</ol></div>
</div></section>'''


def chapter(C):
    key = C['key']
    k, out, slide, short, sub, host, part = TOCD[key]
    C['out'] = out
    idx = KEYS.index(key)
    prev = TOC[idx - 1] if idx > 0 else None
    nxt = TOC[idx + 1] if idx < len(TOC) - 1 else None
    nav = [('#dex', '도감 항목'), ('#lab', '실험실'), ('#ai', 'AI 판단'), ('#colab', '코랩 실습'), ('#sum', '정리'), ('#kg', '색인')]
    navh = ''.join(f'<a href="{h}">{t}</a>' for h, t in nav) + (f'<a href="{nxt[1]}">{nxt[2][-2:]}장 →</a>' if nxt else '<a href="practice/index.html">연습장 →</a>')
    ents = C['entries']
    half = (len(ents) + 1) // 2
    dex1 = '\n'.join(entry(e, f'{C["no"]:02d}-{i+1:02d}') for i, e in enumerate(ents[:half]))
    dex2 = '\n'.join(entry(e, f'{C["no"]:02d}-{i+1+half:02d}') for i, e in enumerate(ents[half:]))
    dexidx = ''.join(f'<a href="#{e["id"]}">{e["ko"]}</a>' for e in ents)
    plain = ''.join(f'<li><b>{a}</b> {b}</li>' for a, b in C['plain'])
    abbr = ''.join(f'<div><b>{a}</b> <span>{b}</span> — {c}</div>' for a, b, c in C['abbr'])
    cast = ''.join(f'<div class="castc{" host" if kk == host else ""}" style="--cc:var(--c-{("x" if kk.startswith("x") else kk)})"><img data-mood="{m}" alt="" aria-hidden="true"><div><b>{n}{" · 이번 장 안내" if kk == host else ""}</b><p>{d}</p></div></div>' for kk, m, n, d in CAST)
    chain = '<i>→</i>'.join(f'<span class="{"on" if t[0] == key else ""}">{t[2][-2:]} {t[3]}</span>' for t in TOC[max(0, idx - 2): idx + 3])
    kpis = (f'<div class="kpi m"><b>{len(ents)}개</b><span>도감 항목 (슬라이드 {slide}의 모든 상자)</span></div>'
            f'<div class="kpi g"><b>1개</b><span>직접 움직이는 실험실</span></div>'
            f'<div class="kpi a"><b>2 + 2</b><span>웃는 그림 둘, 코랩 실습 둘(AI 프롬프트·실제 코드)</span></div>'
            f'<div class="kpi r"><b>{len(C["quiz"])}문제</b><span>확인 퀴즈</span></div>')
    L = C['lab']
    summ = ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in C['summary'])
    gloss = ''.join(f'<div><b>{e["ko"]}</b> = {e["one"]}</div>' for e in ents)
    lims = ''.join(f'<li>{x}</li>' for x in C['limits'])
    diffs = ''.join(f'<li>{x}</li>' for x in C.get('diffs', [])) or '<li>원자료의 값과 식은 모두 검산했고, 바꾼 곳이 없습니다.</li>'
    nx = []
    if prev: nx.append((prev[1], f'← {prev[2][-2:]}장 {prev[3]}', prev[4]))
    nx.append(('index.html', '도감 목차', '열다섯 장과 항목 찾기'))
    if nxt: nx.append((nxt[1], f'{nxt[2][-2:]}장 {nxt[3]} →', nxt[4]))
    else: nx.append(('practice/index.html', '마지막 장 · 실전 연습장 →', '네 현장에서 배운 것 쓰기'))
    nexth = ''.join(f'<a href="{h}"><b>{t}</b><br>{d}</a>' for h, t, d in nx)
    toons = [toon(t, key, i) for i, t in enumerate(C['toons'])]
    T = f'{C["no"]:02d}장 {C["title"]} | 수리 도감 — 인공지능을 위한 수리적 기초'
    D = C['desc']
    og = SITE + 'img/og/' + key + '.png'
    gl = {e['ko']: [e['ko'], e['en'], e['one']] for e in ents}
    gl.update(C.get('gloss', {}))
    quiz = {'q': C['quiz']}
    H = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(T)}</title>
<meta name="description" content="{esc(D)}">
<meta property="og:type" content="article"><meta property="og:title" content="{esc(T)}"><meta property="og:description" content="{esc(D)}">
<meta property="og:image" content="{og}"><meta property="og:url" content="{SITE}{out}"><meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<!--@@CSS@@-->
<style>{EXTRA_CSS}</style>
</head>
<body>
<nav class="top" aria-label="섹션 바로가기"><div class="row">
  <a class="logo" href="index.html">수리 <i>도감</i> {C["no"]:02d}</a>
  <div class="links">{navh}</div>
</div></nav>
<div class="cover" id="cover"><div class="frame"><img class="art" src="img/cover_{key}.webp" width="1920" height="1080" alt="{esc(C["cover_alt"])}" fetchpriority="high"><span class="cap">수리 도감 · {slide}</span><span class="cover-chip">{C["no"]:02d}장 {C["title"]} · 안내 {NAME[host]}</span></div></div>
<header class="hero" id="top"><div class="wrap">
  <div class="eyebrow">수리 도감 · 인공지능을 위한 수리적 기초 · {part} · 원자료 {slide} <span class="diff">이번 장 안내: {NAME[host]}</span></div>
  <h1>{C["no"]:02d}장 {C["title"]}</h1>
  <p class="question">{C["question"]}</p>
  <p class="lead">{C["lead"]}</p>
  <p class="byline">{AUTHOR} · {DATE} · {VER}</p>
  <div class="start"><b>처음이라면</b> {C["start"]}</div>
  <div class="kpis" aria-label="숫자 요약">{kpis}</div>
</div></header>
<main>
<section class="sec" id="plain" aria-labelledby="h-plain"><div class="wrap"><h2 id="h-plain">처음 오신 분께 — 이 장을 3줄로</h2><ol class="plain3">{plain}</ol>
<p class="plain-note">코드와 수식을 몰라도 됩니다. 항목마다 "말로 먼저"와 "숫자로 한 번 해 보기"가 먼저 나오고, 식은 "식으로 보면"을 펼칠 때만 나옵니다. 여기서 한 번 멈춰도 괜찮아요.</p>
<details class="abbr"><summary>기호·영어 약어 풀이 ({len(C["abbr"])}개)</summary><div class="abbr-list">{abbr}</div></details></div></section>
<section class="sec" id="cast" aria-labelledby="h-cast" style="padding:18px 0 0;border:0"><div class="wrap"><h3 id="h-cast">연구소 식구 — 열다섯 장을 돌아가며 안내합니다</h3>
<div class="cast" style="grid-template-columns:repeat(auto-fit,minmax(230px,1fr))">{cast}</div></div></section>
<section class="sec" id="open" aria-labelledby="h-open"><div class="wrap">
<h2 id="h-open"><span class="hex">{C["no"]:02d}</span>{C["open_title"]}</h2>
<div class="hostcard" style="--cc:var(--c-{("x" if host.startswith("x") else host)})"><img data-mood="{MOOD[host]}" alt="" aria-hidden="true"><div><b>이번 장 안내 · {NAME[host]}</b><p>{C["host_why"]}</p></div></div>
<div data-dlg="open"></div>
<div class="chain">{chain}</div>
<p class="where"><b>도감 속 자리</b> {C["where"]}</p>
<div class="sis"><img data-mood="asst_report" alt="" aria-hidden="true"><p><b>조교 하루의 길 안내</b> 같은 주제를 생선 가게 AI 모델 이야기로 차례차례 따라가고 싶다면 「인공지능을 위한 수학」 <a href="{MFA}{SIS[key][0]}">{SIS[key][1]}</a>을 함께 보세요. 이야기로 흐름을 잡고, 이 도감으로 낱말을 찾아보는 식으로 쓰면 좋아요.</p></div>
{toons[0]}
</div></section>
<section class="sec" id="dex" aria-labelledby="h-dex"><div class="wrap">
<h2 id="h-dex"><span class="hex">도감</span>도감 항목 — {len(ents)}개</h2>
<p>슬라이드 {slide}의 상자를 하나도 빼지 않고 항목으로 옮겼습니다. 이름표를 눌러 바로 가세요.</p>
<div class="dexidx">{dexidx}</div>
{dex1}
<div data-dlg="mid"></div>
{dex2}
</div></section>
<section class="sec" id="lab" aria-labelledby="h-lab"><div class="wrap">
<h2 id="h-lab"><span class="hex">실험</span>{L["title"]}</h2>
<div data-dlg="lab_o"></div>
<div class="easy">{why_box(L["why"])}{math_box(L["math"])}</div>
<div class="dialog lvtalk" data-dlg="lab_t"></div>
<div class="panel" id="w-{key}" data-w="{L["widget"]}"></div>
<div class="say" data-who="doc"><img class="who" data-mood="doc_judge" alt="" aria-hidden="true"><div><b class="name">박사의 정리</b><p>{L["doc"]}</p></div></div>
<div class="lim"><b>이 실험의 한계</b> {L["limit"]}</div>
{toons[1]}
{ai_box(C["ai"])}
<h3 id="quiz">확인 퀴즈</h3>
<div class="quiz" data-quiz="q"></div>
</div></section>
{colab(C)}
<section class="sec" id="sum" aria-labelledby="h-sum"><div class="wrap">
<h2 id="h-sum">정리 — {C["sum_title"]}</h2>
<div class="tblwrap"><table class="cmp"><thead><tr><th>질문</th><th>답 한 줄</th></tr></thead><tbody>{summ}</tbody></table></div>
<h3>용어 대응 카드</h3><div class="gloss">{gloss}</div>
<h3>원자료와 다르게 쓴 곳</h3><ul>{diffs}</ul>
<h3>비유와 예시의 한계</h3><ul>{lims}</ul>
<div class="next">{nexth}</div>
</div></section>
<section class="sec" id="outro" aria-labelledby="h-outro"><div class="wrap"><h2 id="h-outro">아웃트로 — 다음 장으로</h2><div data-dlg="outro"></div></div></section>
</main>
<footer><div class="wrap">
<h3>출처</h3>
<table><thead><tr><th>#</th><th>자료</th><th>이 페이지에서 쓴 곳</th></tr></thead><tbody><tr><td>[1]</td><td>연구소 수학 노트 {slide} 「{C["en"]}」 (인포그래픽 한 장)</td><td>도감 항목 전부, 예시 숫자</td></tr>{C.get("refs_html","")}</tbody></table>
<h3>예시값·설명용 모형인 것</h3><ul><li>항목의 숫자 예시는 설명용이며 연구소가 검산했습니다(code/check_numbers.py).</li><li>코랩 코드는 교육용 예제이며 실제 서비스에 그대로 쓰는 코드가 아닙니다.</li></ul>
<p>캐릭터 이름·설정·그림은 저작권자 안상선의 허락 없이 사용할 수 없습니다.</p>
<p>{AUTHOR} · <a href="index.html">수리 도감 목차</a> · 자매편 <a href="https://adminmrobo.github.io/hello_space_lab/index.html">좌표 첫걸음</a> · <a href="https://adminmrobo.github.io/optimization_3d_map/first_step_0.html">최적화 첫걸음</a></p>
</div></footer>
<script>
/*@@SPRITES@@*/
/*@@COMMON@@*/
/*@@MATHLAB@@*/
(function(){{
'use strict';
U.dialogues({json.dumps(C["dlg"], ensure_ascii=False)});
U.fillImgs();
ML.mountAll();
ML.copyButtons();
U.Gloss({json.dumps(gl, ensure_ascii=False)},{json.dumps([e["ko"] for e in ents[:6]], ensure_ascii=False)});
U.Study({{quiz:{json.dumps(quiz, ensure_ascii=False)}}});
U.start();
}})();
</script>
</body>
</html>
'''
    open(os.path.join(B, key + '.src.html'), 'w').write(H)
    return H


EXTRA_CSS = '''
.tl,.tr{font-weight:700;font-size:13.5px;margin-bottom:4px}.tl{color:var(--amber)}.tr{color:var(--terrain)}
.hex{display:inline-grid;place-items:center;min-width:44px;height:34px;padding:0 10px;margin-right:10px;border-radius:8px;background:var(--terrain);color:#fff;font-size:17px;vertical-align:4px}
.sec{padding:40px 0;border-top:1px solid var(--rule)}
.cast{display:grid;gap:10px}.castc{display:flex;gap:10px;align-items:center;background:var(--panel);border:1px solid var(--rule);border-left:4px solid var(--cc);border-radius:10px;padding:8px 10px}
.castc.host{background:#fff;box-shadow:0 0 0 2px var(--cc)}
.castc img{width:60px;height:60px;flex:none}.castc p{margin:0;font-size:13.5px;color:var(--muted);line-height:1.55}
.cover img.art{image-rendering:pixelated;image-rendering:crisp-edges}
.diff{display:inline-block;border:1px solid var(--c-asst);color:var(--c-asst);border-radius:999px;padding:0 10px;font-size:12.5px;margin-left:6px}
.hostcard{display:flex;gap:14px;align-items:center;border:2px solid var(--cc);border-radius:14px;padding:12px 16px;margin:10px 0 16px;background:#fff}
.hostcard img{width:84px;height:84px;flex:none}.hostcard p{margin:4px 0 0;color:var(--muted)}
.chain span.on{background:var(--terrain);color:#fff;border-color:var(--terrain)}
.where{background:var(--panel);border-radius:10px;padding:10px 14px}
.sis{display:flex;gap:12px;align-items:center;border:1px solid var(--c-asst);border-radius:12px;padding:10px 14px;margin:10px 0;background:#fff7fb}.sis img{width:56px;height:56px;flex:none}.sis p{margin:0}
.dexidx{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 18px}.dexidx a{border:1px solid var(--rule);border-radius:999px;padding:3px 12px;font-size:14px;text-decoration:none;background:var(--panel)}
.dexidx a:hover{border-color:var(--terrain)}
.dex{border:1px solid var(--rule);border-top:4px solid var(--terrain);border-radius:14px;padding:16px 20px 12px;margin:0 0 22px;background:#fff;scroll-margin-top:70px}
.dex header{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap}.dex h3{margin:0;font-size:21px}.dex h3 small{font-size:14px;color:var(--muted);font-weight:500}
.dexno{font:700 13px/1 var(--font);color:#fff;background:var(--c-x);border-radius:6px;padding:4px 8px}
.dex .one{font-size:17px;font-weight:600;color:var(--terrain);margin:8px 0 10px}
.dexgrid{display:grid;grid-template-columns:1.2fr 1fr;gap:14px;margin-bottom:10px}
.dexgrid .dw{line-height:1.8}.dexgrid .try{background:var(--amber-soft);border:1px dashed #e8b67a;border-radius:10px;padding:10px 14px}.dexgrid .try ol{margin:6px 0 0;padding-left:22px}
.dexwarn{background:var(--eye-soft);border-radius:8px;padding:8px 12px;font-size:15px}
@media(max-width:760px){.dexgrid{grid-template-columns:1fr}}
.toon{margin:26px auto;max-width:820px;border:1px solid var(--rule);border-radius:14px;overflow:hidden;background:#fff}
.toon .tframe{background:#fff;border-bottom:1px solid var(--rule)}.toon img{display:block;width:100%;height:auto;image-rendering:pixelated;image-rendering:crisp-edges}
.toon figcaption{padding:12px 16px}.toon .ttl{display:block;margin-bottom:8px;color:var(--amber)}
.tline{display:flex;gap:10px;align-items:center;margin:6px 0}.tline img{width:40px;height:40px;flex:none;border-radius:8px;border:1px solid var(--rule)}.tline p{margin:0}
.tpoint{margin:10px 0 0;background:var(--panel);border-radius:8px;padding:8px 12px;font-size:15px}
.labbox{border:1px solid var(--rule);border-radius:14px;padding:14px 18px;margin:16px 0;background:#fff}
.labh{font-weight:700;font-size:17px;margin-bottom:6px}.lno{display:inline-grid;place-items:center;width:28px;height:28px;border-radius:50%;background:var(--terrain);color:#fff;margin-right:6px}
.codewrap{position:relative}.cpy{position:absolute;right:8px;top:8px;font:600 12.5px var(--font);border:1px solid var(--rule);background:#fff;border-radius:8px;padding:3px 10px;cursor:pointer}
pre.prompt,pre.code,pre.out{white-space:pre-wrap;word-break:break-word;background:#f7f9fb;border:1px solid var(--rule);border-radius:10px;padding:14px 16px;font:13.5px/1.65 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;max-height:520px;overflow:auto;margin:8px 0}
pre.prompt{background:#fbf8ff;border-color:#d9c8f0;font-family:var(--font);font-size:14.5px}
pre.out{background:#0f1720;color:#d8e6f0}
.colabbtns{display:flex;flex-wrap:wrap;gap:8px}.colabbtns a.bt{text-decoration:none}
.panel .row2{display:grid;grid-template-columns:1fr 1fr;gap:14px}@media(max-width:760px){.panel .row2{grid-template-columns:1fr}}
.panel .cv{width:100%;height:300px;display:block;border:1px solid var(--rule);border-radius:10px;background:#fff;touch-action:none}
.panel .cv.tall{height:360px}
.panel .rd{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:8px;margin:10px 0}
.panel .rd div{background:var(--panel);border-radius:10px;padding:8px 10px}.panel .rd b{display:block;font-size:19px}.panel .rd span{font-size:12.5px;color:var(--muted)}
.panel .sl{display:flex;align-items:center;gap:10px;margin:6px 0;flex-wrap:wrap}.panel .sl label{min-width:140px;font-size:14.5px}.panel .sl input[type=range]{flex:1;min-width:140px}
.panel .msg{background:#f4fbfb;border:1px dashed var(--terrain);border-radius:10px;padding:10px 14px;margin:8px 0;font-size:15px}
.panel textarea,.panel input[type=text]{width:100%;font:15px var(--font);padding:8px 10px;border:1px solid var(--rule);border-radius:8px}
.panel table.mt{border-collapse:collapse;margin:6px 0}.panel table.mt td{border:1px solid var(--rule);min-width:44px;text-align:center;padding:4px 6px;font-variant-numeric:tabular-nums}
.panel table.mt td.hl{background:var(--amber-soft);font-weight:700}.panel table.mt td.hl2{background:var(--info-soft);font-weight:700}
.panel .step{font-variant-numeric:tabular-nums}
.ptitle{font-weight:700;margin-bottom:6px}
'''


# ── 코랩 노트북·파이썬 파일 ──
def notebook(C):
    key, slug = C['key'], C['slug']
    title = f'{C["no"]:02d}장 {C["title"]} — 수리 도감 코랩 실습'
    cells = [
        {'cell_type': 'markdown', 'metadata': {}, 'source': [
            f'# {title}\n', '\n',
            f'원자료: 연구소 수학 노트 {TOCD[key][2]} 「{C["en"]}」 · 해설 페이지: {SITE}{TOCD[key][1]}\n', '\n',
            '위에서부터 셀을 차례로 실행하세요(Shift + Enter). 그래프는 영어 글자로 그렸습니다(코랩에 한글 글꼴을 따로 깔지 않아도 되게).\n', '\n',
            '글 · 안상선 ((주)M-Robo 대표)\n']},
    ]
    parts = [p.strip('\n') for p in C['code'].split('\n# %%')]
    for i, p in enumerate(parts):
        src = p if i == 0 else '# %%' + p
        lines = src.split('\n')
        title_line = lines[0].replace('# %%', '').strip() if lines[0].startswith('# %%') else ''
        body = '\n'.join(lines[1:] if title_line or lines[0].startswith('# %%') else lines).strip('\n')
        if title_line:
            cells.append({'cell_type': 'markdown', 'metadata': {}, 'source': ['## ' + title_line + '\n']})
        cells.append({'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': [l + '\n' for l in body.split('\n')][:-1] + [body.split('\n')[-1]]})
    cells.append({'cell_type': 'markdown', 'metadata': {}, 'source': ['## 생성 AI 실습 프롬프트\n', '\n', '아래 글을 코랩의 Gemini 창(또는 다른 생성 AI)에 붙여 넣고, 만들어진 코드를 위 코드의 결과와 비교해 보세요.\n', '\n', '```text\n'] + [l + '\n' for l in C['prompt'].strip('\n').split('\n')] + ['```\n']})
    nb = {'cells': cells, 'metadata': {'colab': {'provenance': [], 'name': f'{key}_{slug}.ipynb'}, 'kernelspec': {'name': 'python3', 'display_name': 'Python 3'}, 'language_info': {'name': 'python'}},
          'nbformat': 4, 'nbformat_minor': 0}
    json.dump(nb, open(os.path.join(R, 'colab', f'{key}_{slug}.ipynb'), 'w'), ensure_ascii=False, indent=1)
    os.makedirs(os.path.join(R, 'code', 'colab_py'), exist_ok=True)
    open(os.path.join(R, 'code', 'colab_py', f'{key}_{slug}.py'), 'w').write(f'# {title}\n# 코랩: https://colab.research.google.com/github/{REPO}/blob/main/colab/{key}_{slug}.ipynb\n' + C['code'].strip('\n') + '\n')


def load(key):
    m = importlib.import_module(key)
    C = m.CH
    C['key'] = key
    C['no'] = int(key[2:])
    outf = os.path.join(R, 'code', 'outputs', key + '.txt')
    C['_output'] = open(outf).read() if os.path.exists(outf) else '(아직 실행 기록이 없습니다)'
    return C


if __name__ == '__main__':
    keys = sys.argv[1:] or KEYS
    for k in keys:
        if k in ('index', 'practice'):
            m = importlib.import_module(k + '_page'); m.build(); print('src', k); continue
        C = load(k)
        chapter(C)
        notebook(C)
        print('src', k)
