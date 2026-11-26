# -*- coding: utf-8 -*-
"""마지막 장 · 실전 연습장 — 네 현장(추천 매장·검사실·학습 관제실·데이터 압축실). 주소 끝 #shop #clinic #train #compress"""
import os
from gen import EXTRA_CSS, AUTHOR, DATE, VER, SITE, esc, B

SCENES = [
 ('shop', '추천 매장', '3장 벡터 연산', '03_vector_ops.html#m03-angle',
  '영화 가게의 추천 담당이 되었습니다. 손님의 취향 [액션, 로맨스, 코미디]이 들어오면 상품 네 개 중 하나를 추천해요. 상품 D는 모든 점수가 큰 "대작"이라 내적으로 재면 늘 1등이 되기 쉽습니다. 방향(취향)이 가장 닮은 상품을 고르세요.'),
 ('clinic', '검사실', '7장 조건부 확률과 베이즈', '07_bayes.html#m07-medical',
  '보건소 검사실장이 되었습니다. 검사 A(민감도 99%, 거짓 양성 5%)와 검사 B(민감도 90%, 거짓 양성 1%) 중 하나를 고르고, 양성이면 같은 검사로 한 번 더 확인할지(재검사) 정합니다. "양성"이라고 알렸을 때 정말 병일 확률을 높이는 것이 목표예요.'),
 ('train', '학습 관제실', '13장 최적화', '13_optimization.html#m13-example',
  '점 (1, 2), (2, 3), (3, 5)에 직선 y = wx + b를 맞추는 모델의 학습 관제사입니다. 학습률 α와 걸음 수를 정해 경사하강을 돌려요. 정답(정규방정식)은 w = 1.5, b ≈ 0.333, 가장 작은 MSE ≈ 0.0556입니다.'),
 ('compress', '데이터 압축실', '14장 고윳값과 PCA', '14_eigen_pca.html#m14-pca',
  '특성 6개짜리 데이터를 PCA로 줄이는 압축 담당입니다. 특성끼리 정보가 겹치는 정도(상관 ρ)는 데이터가 정하고, 몇 개의 주성분 k를 남길지는 내가 정해요. 남긴 정보(설명된 분산)와 아낀 저장 공간 사이에서 균형을 찾으세요.'),
]


def build():
    tabs = ''.join(f'<button class="bt" type="button" data-tab="{k}">{n}</button>' for k, n, *_ in SCENES)
    secs = ''.join(f'''<section class="scene" id="{k}" hidden><h2><span class="hex">{i+1}</span>{n}</h2>
<div class="sit"><b>상황</b> {d}</div>
<div class="ctrlbox"><div class="env"><b>시장·데이터 조건</b><div id="{k}_env"></div></div><div class="dec"><b>내 결정</b><div id="{k}_dec"></div></div></div>
<div class="score" id="{k}_score"></div>
<div class="row2g"><canvas class="pcv" id="{k}_g1"></canvas><canvas class="pcv" id="{k}_g2"></canvas></div>
<div class="talk" id="{k}_talk"></div>
<div class="missions"><b>미션</b><ol id="{k}_mis"></ol></div>
<p class="back"><b>배운 곳 다시 보기</b> <a href="{lk}">{ch}</a></p></section>''' for i, (k, n, ch, lk, d) in enumerate(SCENES))
    T = '마지막 장 · 실전 연습장 — 수리 도감'
    D = '수리 도감 마지막 장. 추천 매장(코사인 유사도), 검사실(베이즈), 학습 관제실(경사하강), 데이터 압축실(PCA) 네 현장을 조작판·성적표·미션으로 운영하며 복습합니다.'
    H = f'''<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(T)}</title><meta name="description" content="{esc(D)}">
<meta property="og:type" content="article"><meta property="og:title" content="{esc(T)}"><meta property="og:description" content="{esc(D)}"><meta property="og:image" content="{SITE}img/og/practice.png"><meta property="og:url" content="{SITE}practice/"><meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<!--@@CSS@@-->
<style>{EXTRA_CSS}
.ptabs{{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0;position:sticky;top:52px;background:#fff;padding:8px 0;z-index:5}}
.scene{{padding:10px 0 30px}}.sit{{background:var(--panel);border-radius:12px;padding:12px 16px;margin:10px 0}}
.ctrlbox{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}.env,.dec{{border-radius:12px;padding:12px 14px}}.env{{background:var(--gfp-soft);border:1px solid #9bd0ad}}.dec{{background:var(--info-soft);border:1px solid #9db6ea}}
.env .sl label,.dec .sl label{{min-width:150px}}
.score{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:12px 0}}.score div{{border-radius:10px;padding:10px;border:1px solid var(--rule);background:#fff}}.score b{{display:block;font-size:20px}}.score span{{font-size:12.5px;color:var(--muted)}}
.score .good{{border-color:#2f9a55;background:var(--gfp-soft)}}.score .bad{{border-color:#d36a66;background:var(--eye-soft)}}
.row2g{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}.pcv{{width:100%;height:260px;border:1px solid var(--rule);border-radius:10px;background:#fff}}
.talk .say{{margin:6px 0}}.missions{{border:2px solid var(--terrain);border-radius:12px;padding:12px 16px;margin:12px 0}}.missions li{{margin:6px 0}}.missions li.ok{{color:var(--gfp);font-weight:700}}.missions li.ok::after{{content:" ✔ 통과"}}
.back{{font-size:15px}}.wrapup{{border:1px solid var(--rule);border-radius:14px;padding:16px 20px;background:var(--panel)}}
@media(max-width:760px){{.ctrlbox,.row2g{{grid-template-columns:1fr}}.score{{grid-template-columns:1fr 1fr}}}}
</style></head>
<body>
<nav class="top" aria-label="섹션 바로가기"><div class="row"><a class="logo" href="index.html">수리 <i>도감</i> 연습장</a><div class="links"><a href="#shop">추천 매장</a><a href="#clinic">검사실</a><a href="#train">학습 관제실</a><a href="#compress">압축실</a><a href="#wrap">마무리</a><a href="index.html">목차</a></div></div></nav>
<div class="cover" id="cover"><div class="frame"><img class="art" src="img/cover_practice.webp" width="1920" height="1080" alt="흰 연구실의 관제 모니터 앞에 박사·하루·초파리·주판봇이 서 있다. 칠판에 SHOP cos θ, CLINIC P(D|T), TRAIN α, PCA k=1. 16비트 픽셀아트." fetchpriority="high"><span class="cap">수리 도감 · 마지막 장</span><span class="cover-chip">실전 연습장 — 네 현장</span></div></div>
<header class="hero" id="top"><div class="wrap">
<div class="eyebrow">수리 도감 · 마지막 장 · 실전 연습장</div>
<h1>실전 연습장 — 공식으로 현장 운영하기</h1>
<p class="question">도감에서 찾은 공식, 실제 결정을 내릴 때 정말 쓸 수 있을까?</p>
<p class="lead">네 현장에서 초록 상자(조건)는 바꿔 가며 시험하고, 파란 상자(내 결정)로 운영합니다. 성적표의 숫자 넷과 그래프 두 개가 바로 반응하고, 연구소 식구 넷이 상황에 따라 한마디씩 합니다. 현장마다 미션 세 개(최적 찾기 · 함정 관찰 · 조건을 바꿔도 결론이 유지되는지)를 통과해 보세요. 주소 끝에 #shop, #clinic, #train, #compress를 붙이면 그 현장이 바로 열립니다.</p>
<p class="byline">{AUTHOR} · {DATE} · {VER}</p>
</div></header>
<main><div class="wrap">
<div class="ptabs" role="tablist">{tabs}</div>
{secs}
<section id="wrap" class="sec"><h2>마무리 — 네 현장이 함께 묻는 것</h2><div class="wrapup"><p>네 현장은 모두 "숫자 하나만 보지 말라"는 같은 질문을 합니다. 추천은 내적의 크기보다 방향을, 검사는 정확도보다 기저율을, 학습은 걸음의 크기를, 압축은 줄인 개수와 함께 남은 정보의 비율을 봐야 했어요. 계산은 프로그램이 해 주지만, 어떤 숫자를 봐야 하는지는 우리가 정합니다.</p>
<p class="muted">모형의 한계: 상품 벡터·검사 성능·데이터는 모두 교육용 예시이며, 검사는 서로 독립이라고 가정했습니다. 의료·경영·투자 판단의 근거가 아닙니다. 기록은 이 탭에만 남고 저장하지 않습니다.</p></div>
<p><a href="index.html">← 도감 목차</a> · <a href="15_quick_revision.html">15장 총정리</a></p></section>
</div></main>
<footer><div class="wrap"><p>캐릭터 이름·설정·그림은 저작권자 안상선의 허락 없이 사용할 수 없습니다.</p><p>{AUTHOR}</p></div></footer>
<script>
/*@@SPRITES@@*/
/*@@COMMON@@*/
/*@@MATHLAB@@*/
{PR_JS}
</script></body></html>'''
    open(os.path.join(B, 'practice.src.html'), 'w').write(H)


PR_JS = r'''
var PR=(function(){'use strict';
var $=U.$,$$=U.$$,f2=ML.f2,c=ML.calc,C=function(n){return U.cssv(n);};
var S={};
function say(list){return list.map(function(x,i){return U.say(x[0],x[1],x[2],i%2===1);}).join('');}
function score(id,items){$('#'+id+'_score').innerHTML=items.map(function(x){return '<div class="'+(x[2]||'')+'"><b>'+x[0]+'</b><span>'+x[1]+'</span></div>';}).join('');}
function missions(id,list){var s=S[id];$('#'+id+'_mis').innerHTML=list.map(function(m,i){if(s.touched&&m[1])s.done[i]=true;return '<li class="'+(s.done[i]?'ok':'')+'">'+m[0]+'</li>';}).join('');}
function bars(cv,labels,vals,hl,title,ref){var mx=Math.max.apply(null,vals.concat([ref||0]))*1.15||1,F=ML.frame(cv,[-0.6,vals.length-0.4],[0,mx],{sx:1,yl:title});var g=F.g;
  vals.forEach(function(v,i){g.fillStyle=i===hl?C('--c-fly'):'#9fb7c9';var x0=F.X(i-0.32),x1=F.X(i+0.32),y=F.Y(v);g.fillRect(x0,y,x1-x0,F.Y(0)-y);U.label(g,F.X(i),Math.max(y-12,14),labels[i]+' '+f2(v,2),C('--text'),'center');});
  if(ref){g.strokeStyle=C('--amber');g.setLineDash([5,4]);g.beginPath();g.moveTo(F.X(-0.6),F.Y(ref));g.lineTo(F.X(vals.length-0.4),F.Y(ref));g.stroke();g.setLineDash([]);}}
function ctl(id,html){return html;}
function bind(id,fn){var sc=id.split('_')[0];$$('#'+id+' input').forEach(function(i){i.addEventListener('input',function(){S[sc].touched=true;fn();});});}

/* 1. 추천 매장 */
var P={A:[9,1,4],B:[1,9,2],C:[2,2,9],D:[20,12,15]},PN={A:'A 액션 히어로',B:'B 러브레터',C:'C 웃긴 하루',D:'D 초대작'};
S.shop={touched:false,done:[],pick:'A',dbl:false};
function shop(){var s=S.shop,u=[ML.sv('sh_a'),ML.sv('sh_r'),ML.sv('sh_c')];['a','r','c'].forEach(function(k,i){ML.setv('sh_'+k+'_v',u[i]);});if(s.dbl)u=u.map(function(x){return 2*x;});
  var ks=Object.keys(P),cos=ks.map(function(k){return c.dot(u,P[k])/(c.norm(u)*c.norm(P[k])||1);}),dots=ks.map(function(k){return c.dot(u,P[k]);});
  var bc=ks[cos.indexOf(Math.max.apply(null,cos))],bd=ks[dots.indexOf(Math.max.apply(null,dots))],pi=ks.indexOf(s.pick),rank=cos.filter(function(v){return v>cos[pi]+1e-12;}).length+1;
  s.state={best:bc,bestDot:bd,pick:s.pick,dbl:s.dbl,cos:cos[pi]};
  score('shop',[[s.pick,'내가 추천한 상품'],[f2(cos[pi],3),'추천 상품의 코사인 유사도',rank===1?'good':'bad'],[rank+'위','코사인 순위 (4개 중)',rank===1?'good':'bad'],[bc+' / '+bd,'코사인 1위 / 내적 1위',bc!==bd?'bad':'']]);
  bars($('#shop_g1'),ks,cos,pi,'코사인 유사도');bars($('#shop_g2'),ks,dots,pi,'내적 a·b');
  $('#shop_talk').innerHTML=say([['doc','doc_judge',rank===1?'방향이 가장 닮은 상품을 골랐군요. 좋은 추천입니다.':'추천 상품의 방향이 손님 취향과 덜 닮았어요. 코사인 그래프를 다시 보세요.'],
    ['asst','asst_report','보고: 코사인 1위는 '+bc+'('+f2(Math.max.apply(null,cos),3)+'), 내적 1위는 '+bd+'('+f2(Math.max.apply(null,dots),0)+')예요.'],
    ['fly','fly_magnify',bc!==bd?'내적 1위와 코사인 1위가 다르지? 내적은 상품 점수가 큰 '+bd+'에 끌려가.':'지금은 둘이 같네. 취향을 바꿔서 갈라지는 순간을 찾아봐.'],
    ['robo','robo_calc','내적이 제일 큰 '+bd+'를 추천하면 끝 아냐?']]);
  missions('shop',[['코사인 유사도 1위 상품을 추천하기',s.pick===bc],['함정 관찰: 내적 1위와 코사인 1위가 다른 손님 취향 만들기 (그때 코사인 1위를 추천)',bc!==bd&&s.pick===bc],['조건 바꾸기: 「취향 ×2」를 켜도 같은 상품이 코사인 1위인지 확인 (켠 상태에서 1위 추천)',s.dbl&&s.pick===bc]]);}

/* 2. 검사실 */
S.clinic={touched:false,done:[],test:'A',re:false};
var TS={A:[0.99,0.05],B:[0.90,0.01]};
function clinic(){var s=S.clinic,p=ML.sv('cl_p')/100;ML.setv('cl_p_v',f2(p*100,1)+'%');var t=TS[s.test],post=c.bayes(p,t[0],t[1]),sens=t[0],fpr=t[1];
  if(s.re){post=c.bayes(post,t[0],t[1]);sens=t[0]*t[0];fpr=t[1]*t[1];}
  var N=10000,tp=N*p*sens,fp=N*(1-p)*fpr,fn=N*p-tp;s.state={p:p,test:s.test,re:s.re,post:post};
  score('clinic',[[f2(post*100,1)+'%','양성이면 실제 병일 확률',post>=0.9?'good':post<0.5?'bad':''],[f2(fp,0)+'명','1만 명 중 거짓 양성',fp>100?'bad':''],[f2(fn,0)+'명','1만 명 중 놓친 환자',fn>p*N*0.15?'bad':''],[(s.re?'재검사 · ':'한 번 · ')+'검사 '+s.test,'내 검사 설정']]);
  var F=ML.frame($('#clinic_g1'),[0,30],[0,1],{yl:'P(병|양성)',xl:'유병률 %'});ML.curve(F,function(x){var q=c.bayes(x/100,t[0],t[1]);return s.re?c.bayes(q,t[0],t[1]):q;},0.05,30,C('--info'));ML.dot(F,p*100,post,C('--c-fly'),6);
  bars($('#clinic_g2'),['진짜 양성','거짓 양성','놓친 환자'],[tp,fp,fn],-1,'1만 명당 인원');
  $('#clinic_talk').innerHTML=say([['doc','doc_judge',post>=0.9?'이 설정이면 "양성"이라는 말을 꽤 믿을 수 있어요.':'양성이라고 알려도 실제 환자가 아닌 경우가 많아요. 기저율을 보세요.'],
    ['asst','asst_report','보고: 사후확률 '+f2(post*100,1)+'%, 거짓 양성 '+f2(fp,0)+'명, 놓친 환자 '+f2(fn,0)+'명(1만 명당).'],
    ['fly','fly_magnify',s.re?'재검사는 거짓 양성을 줄이지만 놓치는 환자는 늘어. 공짜가 아니야.':'한 번 검사로는 드문 병의 양성을 다 믿기 어려워.'],
    ['robo','robo_calc','검사 A는 99% 정확하니 양성이면 99% 환자!']]);
  missions('clinic',[['유병률 2% 이하에서 양성 판정이 90% 이상 믿을 만한 설정 찾기',p<=0.02+1e-9&&post>=0.9],['함정 관찰: 유병률 1% 이하, 검사 A 한 번이면 사후확률이 20%도 안 되는 것 확인',p<=0.01+1e-9&&s.test==='A'&&!s.re&&post<0.2],['조건 바꾸기: 유병률을 10% 이상으로 올려도 재검사 설정이 90% 이상을 유지하는지 확인',p>=0.1-1e-9&&s.re&&post>=0.9]]);}

/* 3. 학습 관제실 */
S.train={touched:false,done:[]};
var TX=[1,2,3],TY=[2,3,5];
function runGD(w,b,a,n){var L=[];for(var i=0;i<=n;i++){var gw=0,gb=0,J=0;for(var k=0;k<3;k++){var e=TY[k]-(w*TX[k]+b);gw+=-2*TX[k]*e/3;gb+=-2*e/3;J+=e*e/3;}L.push(J);if(i<n){w-=a*gw;b-=a*gb;}if(!isFinite(J)||J>1e12)break;}return {w:w,b:b,L:L};}
function train(){var s=S.train,w0=ML.sv('tr_w'),a=ML.sv('tr_a'),n=ML.sv('tr_n');ML.setv('tr_w_v',f2(w0));ML.setv('tr_a_v',f2(a));ML.setv('tr_n_v',n);
  var r=runGD(w0,0,a,n),J=r.L[r.L.length-1],st=!isFinite(J)||J>100?'발산':J<=0.06?'수렴':'진행 중';s.state={w0:w0,a:a,n:n,w:r.w,b:r.b,J:J};
  score('train',[[f2(r.w,3)+' / '+f2(r.b,3),'마지막 w / b'],[isFinite(J)?f2(J,4):'폭발','마지막 MSE (최소 0.0556)',J<=0.06?'good':J>100||!isFinite(J)?'bad':''],[isFinite(r.w)?f2(Math.abs(r.w-1.5),3):'—','정답 w = 1.5와의 차이'],[st,'상태',st==='수렴'?'good':st==='발산'?'bad':'']]);
  var F=ML.frame($('#train_g1'),[0,4],[0,7],{xl:'x',yl:'y'});TX.forEach(function(x,i){ML.dot(F,x,TY[i],C('--info'),5);});if(isFinite(r.w))ML.curve(F,function(x){return r.w*x+r.b;},0,4,C('--c-fly'));ML.curve(F,function(x){return 1.5*x+1/3;},0,4,'rgba(19,115,58,.5)',1.5,[5,4]);
  var LL=r.L.map(function(v){return Math.log10(Math.max(v,1e-4));});var F2=ML.frame($('#train_g2'),[0,Math.max(1,LL.length-1)],[-2,Math.max(2,Math.min(12,Math.max.apply(null,LL)))],{xl:'걸음',yl:'log10 MSE'});ML.curve(F2,function(x){return LL[Math.min(LL.length-1,Math.round(x))];},0,LL.length-1,C('--c-fly'));
  $('#train_talk').innerHTML=say([['doc','doc_judge',st==='수렴'?'정규방정식과 같은 답에 닿았어요. 걸음 크기가 알맞았네요.':st==='발산'?'손실이 폭발했어요. 방향이 아니라 걸음 크기 문제입니다.':'아직 가는 중이에요. 걸음 수나 학습률을 조정해 보세요.'],
    ['asst','asst_report','보고: w = '+f2(r.w,3)+', b = '+f2(r.b,3)+', MSE = '+(isFinite(J)?f2(J,4):'폭발')+'.'],
    ['fly','fly_point',a>0.18?'α가 0.18을 넘으면 이 데이터에선 골짜기를 넘어가기 시작해.':'걸음이 작으면 안전하지만 오래 걸려. 손실 곡선의 기울기를 봐.'],
    ['robo','robo_calc','학습률을 최대로 올리면 제일 빨리 끝나겠지!']]);
  missions('train',[['30걸음 안에 MSE 0.06 이하 만들기',n<=30&&J<=0.06],['함정 관찰: 학습률을 키워 손실이 폭발(MSE > 100)하는 것 확인',!isFinite(J)||J>100],['조건 바꾸기: 출발점 w₀를 0이 아닌 값(|w₀| ≥ 2)으로 바꿔도 w ≈ 1.5(±0.01)에 도착',Math.abs(w0)>=2&&Math.abs(r.w-1.5)<=0.01]]);}

/* 4. 데이터 압축실 */
S.compress={touched:false,done:[]};
function eigs(rho){var l=[1+5*rho];for(var i=0;i<5;i++)l.push(1-rho);return l;}
function needK(rho){var l=eigs(rho),s=0;for(var k=1;k<=6;k++){s+=l[k-1];if(s/6>=0.9-1e-9)return k;}return 6;}
function compress(){var s=S.compress,rho=ML.sv('cp_r'),k=ML.sv('cp_k');ML.setv('cp_r_v',f2(rho,2));ML.setv('cp_k_v',k);var l=eigs(rho),cum=0,cums=[];l.forEach(function(v){cum+=v;cums.push(cum/6);});var ret=cums[k-1],nk=needK(rho);
  s.state={rho:rho,k:k,ret:ret,need:nk};
  score('compress',[[f2(ret*100,1)+'%','남긴 정보 (설명된 분산)',ret>=0.9?'good':ret<0.5?'bad':''],[f2((1-k/6)*100,0)+'%','아낀 저장 공간'],[nk+'개','90%를 남기는 최소 k'],[k+'개','내가 남긴 주성분 수',k===nk?'good':'']]);
  bars($('#compress_g1'),['PC1','PC2','PC3','PC4','PC5','PC6'],l,-1,'고윳값 (높을수록 정보 많음)');
  var F=ML.frame($('#compress_g2'),[0.5,6.5],[0,1],{sx:1,xl:'k',yl:'누적 설명 비율'});ML.curve(F,function(x){var i=Math.max(1,Math.min(6,Math.round(x)));return cums[i-1];},1,6,C('--info'));var g=F.g;g.strokeStyle=C('--amber');g.setLineDash([5,4]);g.beginPath();g.moveTo(F.X(0.5),F.Y(0.9));g.lineTo(F.X(6.5),F.Y(0.9));g.stroke();g.setLineDash([]);ML.dot(F,k,ret,C('--c-fly'),6);
  $('#compress_talk').innerHTML=say([['doc','doc_judge',ret>=0.9?'정보의 90% 이상을 남겼어요. 남긴 비율을 꼭 함께 보고하세요.':'버린 정보가 꽤 많아요. 고윳값 그래프에서 몇 개가 큰지 보세요.'],
    ['asst','asst_report','보고: 상관 ρ = '+f2(rho,2)+'에서 PC1 고윳값 '+f2(l[0],2)+', k = '+k+'이면 '+f2(ret*100,1)+'%를 남겨요.'],
    ['fly','fly_magnify',rho<0.3?'특성끼리 겹침이 적으면 PC1 하나가 할 수 있는 일이 적어. 줄이기 어려운 데이터야.':'겹침이 크면 소수의 주성분에 정보가 몰려.'],
    ['robo','robo_calc','k = 1이면 저장 공간 83% 절약! 무조건 1!']]);
  missions('compress',[['90% 이상 남기는 가장 작은 k를 고르기',k===nk],['함정 관찰: 겹침이 적을 때(ρ ≤ 0.2) k ≤ 2로 줄이면 정보가 절반도 안 남는 것 확인',rho<=0.2+1e-9&&k<=2&&ret<0.5],['조건 바꾸기: 겹침이 클 때(ρ ≥ 0.85) k = 1만으로도 90% 이상 남는지 확인',rho>=0.85-1e-9&&k===1&&ret>=0.9]]);}

function setup(){
  $('#shop_env').innerHTML=ML.slider('sh_a','손님 취향: 액션',0,10,1,5)+ML.slider('sh_r','손님 취향: 로맨스',0,10,1,1)+ML.slider('sh_c','손님 취향: 코미디',0,10,1,3)+'<div class="ctrl"><button class="bt" type="button" id="sh_dbl" aria-pressed="false">취향 ×2</button></div>';
  $('#shop_dec').innerHTML='<p style="margin:0 0 6px;font-size:14px">추천할 상품 (상품 벡터 A[9,1,4] B[1,9,2] C[2,2,9] D[20,12,15])</p><div class="ctrl" id="sh_pick"></div>';
  U.btns($('#sh_pick'),Object.keys(P).map(function(k){return [k,PN[k]];}),'A',function(v){S.shop.pick=v;S.shop.touched=true;shop();});
  $('#sh_dbl').onclick=function(){S.shop.dbl=!S.shop.dbl;S.shop.touched=true;this.setAttribute('aria-pressed',S.shop.dbl);shop();};bind('shop_env',shop);
  $('#clinic_env').innerHTML=ML.slider('cl_p','유병률 (병이 있는 비율)',0.1,30,0.1,1);
  $('#clinic_dec').innerHTML='<div class="ctrl" id="cl_t"></div><div class="ctrl"><button class="bt" type="button" id="cl_re" aria-pressed="false">양성이면 재검사</button></div>';
  U.btns($('#cl_t'),[['A','검사 A (99% · 5%)'],['B','검사 B (90% · 1%)']],'A',function(v){S.clinic.test=v;S.clinic.touched=true;clinic();});
  $('#cl_re').onclick=function(){S.clinic.re=!S.clinic.re;S.clinic.touched=true;this.setAttribute('aria-pressed',S.clinic.re);clinic();};bind('clinic_env',clinic);
  $('#train_env').innerHTML=ML.slider('tr_w','출발점 w₀ (b₀ = 0)',-4,4,0.5,0);
  $('#train_dec').innerHTML=ML.slider('tr_a','학습률 α',0.01,0.25,0.01,0.05)+ML.slider('tr_n','걸음 수',1,200,1,50);bind('train_env',train);bind('train_dec',train);
  $('#compress_env').innerHTML=ML.slider('cp_r','특성끼리 겹침 (상관 ρ)',0,0.95,0.05,0.5);
  $('#compress_dec').innerHTML=ML.slider('cp_k','남길 주성분 수 k',1,6,1,3);bind('compress_env',compress);bind('compress_dec',compress);
  shop();clinic();train();compress();}
function open(t){$$('.scene').forEach(function(s){s.hidden=s.id!==t;});$$('[data-tab]').forEach(function(b){b.setAttribute('aria-pressed',String(b.dataset.tab===t));});({shop:shop,clinic:clinic,train:train,compress:compress})[t]();}
U.fillImgs();setup();$$('[data-tab]').forEach(function(b){b.onclick=function(){history.replaceState(null,'','#'+b.dataset.tab);open(b.dataset.tab);};});
var h=(location.hash||'').slice(1);open(['shop','clinic','train','compress'].indexOf(h)>=0?h:'shop');
window.addEventListener('hashchange',function(){var t=location.hash.slice(1);if(S[t])open(t);});
var to;window.addEventListener('resize',function(){clearTimeout(to);to=setTimeout(function(){var t=($$('.scene').filter(function(s){return !s.hidden;})[0]||{}).id;if(t)open(t);},150);});
return {S:S,shop:shop,clinic:clinic,train:train,compress:compress,needK:needK,runGD:runGD,open:open};
})();
'''

