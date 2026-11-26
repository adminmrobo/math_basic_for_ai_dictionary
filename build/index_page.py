# -*- coding: utf-8 -*-
"""목차 — 수리 도감: 인공지능을 위한 수리적 기초 (도감 검색 + 열다섯 장 + 하루의 길 안내)"""
import os, json, re
from gen import EXTRA_CSS, AUTHOR, DATE, VER, SITE, esc, B, CAST, TOC, NAME, MOOD, load, MFA

PARTS = [('기초', '숫자와 함수의 첫 단어'), ('선형대수', '데이터를 담고 한꺼번에 계산하기'), ('확률·통계', '불확실함을 숫자로 재기'), ('미적분·최적화', '손실을 조금씩 줄이기'), ('응용', '정보가 몰린 방향 찾기'), ('총정리', '한 쪽으로 보는 열네 장')]
strip = lambda s: re.sub(r'<[^>]+>', '', s)


def build():
    allent, cards_by_part = [], {p: [] for p, _ in PARTS}
    for key, out, slide, short, sub, host, part in TOC:
        C = load(key)
        for e in C['entries']:
            allent.append([C['no'], out + '#' + e['id'], strip(e['ko']), e['en'], strip(e['one'])])
        n = len(C['entries'])
        cards_by_part[part].append(f'''<a class="ccard" href="{out}"><img class="cthumb" src="img/og/{key}.png" width="960" height="540" loading="lazy" alt=""><div><span class="cno">{slide}</span> <span class="chost"><img data-mood="{MOOD[host]}" alt="" aria-hidden="true">안내 {NAME[host]}</span><h3>{C["no"]:02d}장 {short}</h3><p>{sub} · 항목 {n}개</p><p class="cq">{C["question"]}</p></div></a>''')
    parts = ''.join(f'<h3 class="parth">{p} <small>{d}</small></h3><div class="cgrid">{"".join(cards_by_part[p])}</div>' for p, d in PARTS)
    cast = ''.join(f'<div class="castc" style="--cc:var(--c-{("x" if k.startswith("x") else k)})"><img data-mood="{m}" alt="" aria-hidden="true"><div><b>{n}</b><p>{d}</p></div></div>' for k, m, n, d in CAST)
    rota = ''.join(f'<span><img data-mood="{MOOD[h]}" alt="" aria-hidden="true">{s[-2:]} {NAME[h]}</span>' for k, o, s, sh, su, h, p in TOC)
    T = '수리 도감 — 인공지능을 위한 수리적 기초 | 연구소 식구가 돌아가며 안내하는 열다섯 장'
    D = '수리 도감. 인공지능에 쓰이는 수학(함수, 벡터·행렬, 연립방정식, 확률·베이즈, 통계·분포·상관, 미분·그래디언트·최적화, 고윳값·PCA)을 열다섯 장 ' + str(len(allent)) + '개 항목으로 찾아보는 도감. 장마다 웃는 그림 둘, 실험실, 코랩 실습(생성 AI 프롬프트와 실제 코드).'
    H = f'''<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(T)}</title><meta name="description" content="{esc(D)}">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(T)}"><meta property="og:description" content="{esc(D)}"><meta property="og:image" content="{SITE}img/og/index.png"><meta property="og:url" content="{SITE}"><meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<!--@@CSS@@-->
<style>{EXTRA_CSS}
.cgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px;margin:10px 0 22px}}
.ccard{{display:flex;flex-direction:column;background:var(--panel);border:1px solid var(--rule);border-radius:14px;overflow:hidden;text-decoration:none;color:var(--text)}}
.ccard:hover{{border-color:var(--terrain)}}.ccard>div{{padding:12px 16px}}.ccard h3{{margin:6px 0 4px;font-size:18px}}.ccard p{{margin:0 0 6px;font-size:14.5px;color:var(--muted)}}
.cthumb{{width:100%;height:auto;display:block;image-rendering:pixelated;border-bottom:1px solid var(--rule)}}.cno{{font-weight:700;color:var(--terrain)}}.cq{{font-size:13.5px!important}}
.chost{{display:inline-flex;align-items:center;gap:4px;font-size:13px;color:var(--muted)}}.chost img{{width:24px;height:24px;border-radius:6px}}
.parth{{margin:26px 0 4px;font-size:20px}}.parth small{{font-size:14px;color:var(--muted);font-weight:500}}
.rota{{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0}}.rota span{{display:inline-flex;align-items:center;gap:4px;border:1px solid var(--rule);border-radius:999px;padding:2px 10px 2px 3px;font-size:13.5px;background:#fff}}.rota img{{width:26px;height:26px;border-radius:50%}}
#dexq{{width:100%;font:17px var(--font);padding:12px 14px;border:2px solid var(--terrain);border-radius:12px}}
#dexres{{list-style:none;padding:0;margin:10px 0;max-height:520px;overflow:auto;border:1px solid var(--rule);border-radius:12px}}
#dexres li{{border-bottom:1px solid var(--rule);padding:8px 14px}}#dexres li:last-child{{border:0}}#dexres a{{font-weight:700;text-decoration:none}}#dexres small{{color:var(--muted)}}#dexres .n{{display:inline-block;min-width:30px;color:#fff;background:var(--c-x);border-radius:6px;text-align:center;font-size:12.5px;margin-right:8px}}
#dexres p{{margin:2px 0 0;font-size:14px;color:var(--muted)}}
.qchips{{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}}.qchips button{{font:14px var(--font);border:1px solid var(--rule);background:var(--panel);border-radius:999px;padding:3px 12px;cursor:pointer}}
.guide{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:14px 0}}.guide>div{{border:1px solid var(--rule);border-radius:12px;padding:14px 18px;background:#fff}}.guide b.q{{display:block;font-size:19px;color:var(--terrain);margin-bottom:4px}}
.harubox{{display:flex;gap:14px;align-items:flex-start;border:2px solid var(--c-asst);border-radius:14px;padding:14px 18px;background:#fff7fb;margin:16px 0}}.harubox img{{width:84px;height:84px;flex:none}}.harubox p{{margin:4px 0}}
.harubox .bt{{text-decoration:none;display:inline-block;margin-top:6px}}
@media(max-width:760px){{.guide{{grid-template-columns:1fr}}.harubox{{flex-direction:column}}}}
</style></head>
<body>
<nav class="top" aria-label="섹션 바로가기"><div class="row"><a class="logo" href="index.html">수리 <i>도감</i></a><div class="links"><a href="#search">도감 검색</a><a href="#before">먼저 볼 곳</a><a href="#toc">열다섯 장</a><a href="#family">연구소 식구</a><a href="#how">쓰는 법</a><a href="practice/index.html">실전 연습장</a><a href="#kg">색인</a></div></div></nav>
<div class="cover" id="cover"><div class="frame"><img class="art" src="img/cover_index.webp" width="1920" height="1080" alt="흰 연구실. 칠판에 f(x), Ax=b, P(A|B), σ², ∂f/∂x, ∇f, λ, θ ← θ − α∇f가 적혀 있고, 가운데 박사가 지휘봉으로 칠판을 가리킨다. 초파리·하루·주판봇·모아·시아·X1·X2·X3까지 연구소 식구 아홉 명이 모두 나란히 서 있고, 오른쪽 책장에 두꺼운 책이 꽂혀 있다. 16비트 픽셀아트." fetchpriority="high"><span class="cap">수리 도감 · MATH-01 ~ 15</span><span class="cover-chip">인공지능을 위한 수리적 기초</span></div></div>
<header class="hero" id="top"><div class="wrap">
<div class="eyebrow">수리 도감 · 연구소 식구가 돌아가며 안내하는 열다섯 장 · 좌표 첫걸음의 이웃</div>
<h1>인공지능을 위한 수리적 기초</h1>
<p class="question">AI 책에서 막힌 그 기호, 그 공식 — 어디서 왔고 무엇을 재는지 도감처럼 찾아보세요.</p>
<p class="lead">인공지능에 쓰이는 수학을 열다섯 장, <b>{len(allent)}개 항목</b>으로 정리한 도감입니다. 함수에서 시작해 벡터·행렬, 연립방정식, 확률과 베이즈, 통계·분포·상관, 미분·그래디언트·경사하강을 지나 고윳값과 PCA까지 갑니다. 항목마다 "말로 먼저 → 숫자로 한 번 해 보기 → 학교 수학으로 보면 → AI에서는" 순서로 쓰여 있고, 장마다 <b>웃는 그림 둘</b>, 직접 움직이는 <b>실험실</b>, <b>코랩 실습</b>(생성 AI에게 줄 프롬프트와 연구소가 검사한 실제 코드)이 있습니다.</p>
<p class="byline">{AUTHOR} · {DATE} · {VER}</p>
<div class="start"><b>처음이라면</b> 아래 「도감 검색」에 궁금한 낱말을 넣거나, 01장에서 시작해 차례로 읽으세요. 한 장은 20~40분 분량이고, 코드와 수식을 몰라도 됩니다. 고등학교 1학년 수학(일차·이차함수, 확률의 기초)이면 출발하기에 충분해요.</div>
<div class="kpis"><div class="kpi m"><b>15장</b><span>원자료 수학 노트 MATH-01 ~ 15 전부</span></div><div class="kpi g"><b>{len(allent)}개</b><span>찾아볼 수 있는 도감 항목</span></div><div class="kpi a"><b>30장</b><span>장마다 둘, 웃는 픽셀 그림</span></div><div class="kpi r"><b>15 + 15</b><span>코랩 노트북과 생성 AI 프롬프트</span></div></div>
</div></header>
<main>
<section class="sec" id="search"><div class="wrap"><h2><span class="hex">검색</span>도감 검색 — 낱말 하나로 찾기</h2>
<p>이름(한글·영어)이나 뜻으로 찾습니다. 결과를 누르면 그 장의 항목으로 바로 갑니다.</p>
<input type="search" id="dexq" placeholder="예: 내적, 역행렬, 베이즈, 표준편차, gradient, PCA" aria-label="도감 검색">
<div class="qchips" id="qchips"></div>
<ul id="dexres" aria-live="polite"></ul>
</div></section>
<section class="sec" id="before"><div class="wrap"><h2><span class="hex">안내</span>먼저 볼 곳 — 조교 하루의 길 안내</h2>
<div class="harubox"><img data-mood="asst_report" alt="" aria-hidden="true"><div><b style="color:var(--c-asst)">조교 하루</b>
<p>인공지능을 위한 수학의 기본 내용을 <b>이야기로 먼저</b> 보고 싶다면, 이 도감보다 <b>「인공지능을 위한 수학 — 숫자로 담고, 한 번에 풀기」</b>를 먼저 추천해요. 생선 가게 AI 모델 하나를 처음부터 끝까지 만들면서, 공식 하나하나가 모델의 어느 부품이 되는지 차례로 따라가거든요.</p>
<p>그 이야기로 흐름을 잡은 뒤, 읽다가 막히는 낱말을 이 도감에서 찾아보는 식으로 함께 쓰면 가장 좋아요. 도감의 장마다 그 시리즈의 같은 주제 방으로 가는 길도 달아 두었어요.</p>
<a class="bt primary" href="{MFA}">인공지능을 위한 수학 1부부터 보기 →</a> <a class="bt" href="{MFA}part2.html">2부 데이터·불확실성</a> <a class="bt" href="{MFA}part3.html">3부 조금씩 고치며 배우기</a></div></div>
<div class="guide"><div><b class="q">이야기로 따라가기</b><p><a href="{MFA}">인공지능을 위한 수학</a> — 생선 가게 모델 하나로 공식 12장을 엮은 연구실 해설(1~3부).</p></div><div><b class="q">낱말로 찾아보기</b><p>수리 도감 (이 사이트) — 같은 범위의 공식을 항목별로 펼치고, 실험실·코랩 실습을 붙인 사전.</p></div></div>
<p class="muted" style="font-size:14.5px">좌표와 최적화를 그림으로 먼저 보고 싶다면 이웃 시리즈 <a href="https://adminmrobo.github.io/hello_space_lab/index.html">좌표 첫걸음 — 나는 어디에 있는가?</a>와 <a href="https://adminmrobo.github.io/optimization_3d_map/first_step_0.html">최적화 첫걸음</a>도 함께 보세요. 이 도감의 장 구성과 강의실 형식은 좌표 첫걸음을 본보기로 삼았습니다.</p>
</div></section>
<section class="sec" id="toc"><div class="wrap"><h2><span class="hex">목차</span>열다섯 장</h2>
<div class="chain"><span>기초</span><i>→</i><span>선형대수 (담기)</span><i>→</i><span>확률·통계 (재기)</span><i>→</i><span>미적분·최적화 (고치기)</span><i>→</i><span>응용 (줄이기)</span><i>→</i><span>총정리</span><i>→</i><span>실전 연습장</span></div>
{parts}
<h3 class="parth">마지막 장 <small>배운 것으로 현장 운영하기</small></h3><div class="cgrid"><a class="ccard" href="practice/index.html"><img class="cthumb" src="img/og/practice.png" width="960" height="540" loading="lazy" alt=""><div><span class="cno">PRACTICE</span><h3>실전 연습장 — 네 현장</h3><p>추천 매장(코사인 유사도) · 검사실(베이즈) · 학습 관제실(경사하강) · 데이터 압축실(PCA). 미션 12개.</p></div></a></div>
</div></section>
<section class="sec" id="family"><div class="wrap"><h2><span class="hex">식구</span>연구소 식구 — 돌아가며 안내합니다</h2>
<p>장이 많은 만큼 연구소 식구 모두가 번갈아 한 장씩 안내를 맡았습니다. 막내 X1·X2·X3도 각자 장을 맡고, 마지막 총정리는 셋이 함께 엽니다. 계산 담당 주판봇은 1초 만에 답을 내지만 가끔 너무 빨라서, 장마다 <b>AI 판단 코너</b>에서 "이 답 믿어도 될까?"를 함께 따져 봅니다.</p>
<div class="rota">{rota}</div>
<div class="cast" style="grid-template-columns:repeat(auto-fit,minmax(230px,1fr))">{cast}</div></div></section>
<section class="sec" id="how"><div class="wrap"><h2><span class="hex">쓰는 법</span>한 장은 이렇게 생겼어요</h2>
<ol><li><b>안내 담당의 상황 질문</b>으로 문을 엽니다.</li><li><b>도감 항목</b> — 원자료 슬라이드의 상자를 하나도 빼지 않고 항목으로. 말로 먼저, 숫자로 한 번, 학교 수학, AI에서는, 식은 접어서.</li><li><b>웃는 그림 둘</b> — 개념이 틀리는 순간을 연구소 식구들이 몸으로 보여 줍니다.</li><li><b>실험실</b> — 슬라이더와 버튼으로 직접 움직이는 계산기·그래프.</li><li><b>AI 판단 코너</b> — 주판봇이 너무 빨리 낸 답에서 틀린 곳을 찾습니다.</li><li><b>코랩 실습실</b> — ① 생성 AI에게 줄 프롬프트 ② 연구소가 실행해 검사한 파이썬 코드(코랩에서 바로 열기) ③ 둘을 맞대 보는 비교 과제.</li></ol>
<p>원자료와 값이나 설명을 다르게 쓴 곳은 장마다 「원자료와 다르게 쓴 곳」에 밝혔습니다. 모든 예시 숫자는 code/check_numbers.py로, 모든 코랩 코드는 실제로 실행해(code/run_colab.py) 확인했습니다.</p>
</div></section>
</main>
<footer><div class="wrap"><p>원자료: 연구소 수학 노트 인포그래픽 MATH-01 ~ MATH-15. 캐릭터 이름·설정·그림은 저작권자 안상선의 허락 없이 사용할 수 없습니다.</p><p>{AUTHOR} · 이웃 시리즈 <a href="{MFA}">인공지능을 위한 수학</a> · <a href="https://adminmrobo.github.io/hello_space_lab/index.html">좌표 첫걸음</a> · <a href="https://adminmrobo.github.io/optimization_3d_map/first_step_0.html">최적화 첫걸음</a></p></div></footer>
<script>
/*@@SPRITES@@*/
/*@@COMMON@@*/
/*@@MATHLAB@@*/
(function(){{'use strict';U.fillImgs();
var D={json.dumps(allent, ensure_ascii=False)};
var q=U.$('#dexq'),res=U.$('#dexres');
function norm(s){{return String(s).toLowerCase().replace(/\\s+/g,'');}}
function show(){{var t=norm(q.value),list=D.filter(function(d){{return !t||norm(d[2]+d[3]+d[4]).indexOf(t)>=0;}});
res.innerHTML=list.slice(0,80).map(function(d){{return '<li><span class="n">'+(d[0]<10?'0':'')+d[0]+'</span><a href="'+d[1]+'">'+U.esc(d[2])+'</a> <small>'+U.esc(d[3])+'</small><p>'+U.esc(d[4])+'</p></li>';}}).join('')||'<li>찾는 낱말이 없어요. 다른 말(영어 이름, 뜻)로 찾아보세요.</li>';}}
q.addEventListener('input',show);
['함수','행렬','내적','역행렬','베이즈','표준편차','정규','상관','미분','그래디언트','학습률','PCA','소프트맥스'].forEach(function(w){{var b=document.createElement('button');b.type='button';b.textContent=w;b.onclick=function(){{q.value=w;show();}};U.$('#qchips').appendChild(b);}});
show();U.start();}})();
</script></body></html>'''
    open(os.path.join(B, 'index.src.html'), 'w').write(H)
