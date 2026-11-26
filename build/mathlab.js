/* mathlab.js — 수리 도감 실험실 모듈 (장마다 하나, 외부 라이브러리 없음)
   ML.mountAll()이 [data-w] 패널을 찾아 W[이름](패널)을 부른다. 계산 함수는 ML.calc로 내보내 code/check_numbers.js가 검산한다. */
var ML=(function(){
'use strict';
var $=U.$,$$=U.$$,fmt=U.fmt,cssv=U.cssv,clamp=U.clamp;
function C(n){return cssv(n)||'#333';}
function f2(x,d){if(!isFinite(x))return '—';d=d==null?2:d;var s=(+x).toFixed(d);if(d>0)s=s.replace(/\.?0+$/,'');return s==='-0'?'0':s;}
function el(h){var d=document.createElement('div');d.innerHTML=h;return d.firstElementChild;}
function slider(id,lab,min,max,step,val){return '<div class="sl"><label for="'+id+'">'+lab+'</label><input type="range" id="'+id+'" min="'+min+'" max="'+max+'" step="'+step+'" value="'+val+'"><span class="val" id="'+id+'_v"></span></div>';}
function rd(items){return '<div class="rd">'+items.map(function(x){return '<div><b id="'+x[0]+'">—</b><span>'+x[1]+'</span></div>';}).join('')+'</div>';}
function sv(id){return parseFloat($('#'+id).value);}
function setv(id,t){var e=$('#'+id);if(e)e.innerHTML=t;}
function bind(root,fn){$$('input,select,textarea',root).forEach(function(i){i.addEventListener('input',fn);});}
function bbar(host,list,cur,on){U.btns(host,list,cur,on);}
/* 좌표 틀: 값 범위를 화면으로 */
function frame(cv,xr,yr,o){o=o||{};var S=U.setup(cv),g=S.g,w=S.w,h=S.h,L=o.L||40,Rr=12,T=12,Bm=o.B||28;
  var X=function(x){return L+(x-xr[0])/(xr[1]-xr[0])*(w-L-Rr);},Y=function(y){return h-Bm-(y-yr[0])/(yr[1]-yr[0])*(h-T-Bm);};
  var ix=function(px){return xr[0]+(px-L)/(w-L-Rr)*(xr[1]-xr[0]);},iy=function(py){return yr[0]+(h-Bm-py)/(h-T-Bm)*(yr[1]-yr[0]);};
  g.strokeStyle='rgba(22,33,43,.07)';g.lineWidth=1;var sx=o.sx||niceStep(xr),sy=o.sy||niceStep(yr);
  g.beginPath();for(var x=Math.ceil(xr[0]/sx)*sx;x<=xr[1]+1e-9;x+=sx){g.moveTo(X(x),T);g.lineTo(X(x),h-Bm);}for(var y=Math.ceil(yr[0]/sy)*sy;y<=yr[1]+1e-9;y+=sy){g.moveTo(L,Y(y));g.lineTo(w-Rr,Y(y));}g.stroke();
  g.strokeStyle='rgba(22,33,43,.55)';g.lineWidth=1.3;g.beginPath();var y0=clamp(Y(0),T,h-Bm),x0=clamp(X(0),L,w-Rr);g.moveTo(L,y0);g.lineTo(w-Rr,y0);g.moveTo(x0,T);g.lineTo(x0,h-Bm);g.stroke();
  g.fillStyle=C('--muted');g.font='11px '+C('--font');g.textAlign='center';g.textBaseline='top';
  for(x=Math.ceil(xr[0]/sx)*sx;x<=xr[1]+1e-9;x+=sx)g.fillText(f2(x,2),X(x),h-Bm+6);
  g.textAlign='right';g.textBaseline='middle';for(y=Math.ceil(yr[0]/sy)*sy;y<=yr[1]+1e-9;y+=sy)g.fillText(f2(y,2),L-5,Y(y));
  if(o.xl){g.textAlign='right';g.textBaseline='bottom';g.fillText(o.xl,w-Rr,h-Bm-3);}if(o.yl){g.textAlign='left';g.textBaseline='top';g.fillText(o.yl,L+4,T);}
  return {g:g,w:w,h:h,X:X,Y:Y,ix:ix,iy:iy,T:T,Bm:Bm,L:L};}
function niceStep(r){var s=(r[1]-r[0])/8,p=Math.pow(10,Math.floor(Math.log10(s))),m=s/p;return (m<1.5?1:m<3.5?2:m<7.5?5:10)*p;}
function curve(F,fn,a,b,col,wd,dash){var g=F.g;g.save();g.strokeStyle=col;g.lineWidth=wd||2.2;if(dash)g.setLineDash(dash);g.beginPath();var pen=false,N=300;
  for(var i=0;i<=N;i++){var x=a+(b-a)*i/N,y=fn(x);if(!isFinite(y)||Math.abs(F.Y(y))>1e5){pen=false;continue;}var px=F.X(x),py=F.Y(y);if(!pen){g.moveTo(px,py);pen=true;}else g.lineTo(px,py);}g.stroke();g.restore();}
function dot(F,x,y,col,r){var g=F.g;g.beginPath();g.arc(F.X(x),F.Y(y),r||4.5,0,7);g.fillStyle=col;g.fill();g.strokeStyle='#fff';g.lineWidth=1.5;g.stroke();}
function arrowV(F,x0,y0,x1,y1,col,wd){U.arrow2(F.g,F.X(x0),F.Y(y0),F.X(x1),F.Y(y1),col,wd||2.5);}
function txt(F,x,y,t,col,al){U.label(F.g,F.X(x),F.Y(y),t,col||C('--text'),al||'left');}
function rng(seed){var s=seed>>>0||1;return function(){s=(s*1664525+1013904223)>>>0;return s/4294967296;};}
function gauss(r){var u=r()||1e-9,v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}

/* ── 계산 (검산 대상) ── */
var calc={
  dot:function(a,b){var s=0;for(var i=0;i<a.length;i++)s+=a[i]*b[i];return s;},
  norm:function(a){return Math.sqrt(calc.dot(a,a));},
  angle:function(a,b){return Math.acos(clamp(calc.dot(a,b)/(calc.norm(a)*calc.norm(b)),-1,1))*180/Math.PI;},
  matmul:function(A,B){return A.map(function(r){return B[0].map(function(_,j){var s=0;for(var k=0;k<r.length;k++)s+=r[k]*B[k][j];return s;});});},
  det2:function(a,b,c,d){return a*d-b*c;},
  solve2:function(a1,b1,c1,a2,b2,c2){var D=a1*b2-b1*a2;if(Math.abs(D)<1e-12){var cons=Math.abs(a1*c2-a2*c1)<1e-12&&Math.abs(b1*c2-b2*c1)<1e-12;return {type:cons?'inf':'none',D:0};}
    return {type:'one',D:D,x:(c1*b2-b1*c2)/D,y:(a1*c2-c1*a2)/D,Dx:c1*b2-b1*c2,Dy:a1*c2-c1*a2};},
  bayes:function(p,sens,fpr){var t=sens*p+fpr*(1-p);return sens*p/t;},
  mean:function(a){return a.reduce(function(s,x){return s+x;},0)/a.length;},
  median:function(a){var s=a.slice().sort(function(x,y){return x-y;}),n=s.length;return n%2?s[(n-1)/2]:(s[n/2-1]+s[n/2])/2;},
  quart:function(a){var s=a.slice().sort(function(x,y){return x-y;}),n=s.length,h=Math.floor(n/2);var lo=s.slice(0,h),hi=s.slice(n%2?h+1:h);return [calc.median(lo),calc.median(s),calc.median(hi)];},
  varp:function(a){var m=calc.mean(a);return a.reduce(function(s,x){return s+(x-m)*(x-m);},0)/a.length;},
  mode:function(a){var c={},best=0,m=[];a.forEach(function(x){c[x]=(c[x]||0)+1;});Object.keys(c).forEach(function(k){if(c[k]>best){best=c[k];m=[+k];}else if(c[k]===best)m.push(+k);});return best<2?null:m;},
  comb:function(n,k){var r=1;for(var i=1;i<=k;i++)r=r*(n-k+i)/i;return r;},
  binom:function(n,p,k){return calc.comb(n,k)*Math.pow(p,k)*Math.pow(1-p,n-k);},
  fact:function(k){var r=1;for(var i=2;i<=k;i++)r*=i;return r;},
  poisson:function(l,k){return Math.exp(-l)*Math.pow(l,k)/calc.fact(k);},
  npdf:function(x,m,s){return Math.exp(-(x-m)*(x-m)/(2*s*s))/(s*Math.sqrt(2*Math.PI));},
  ncdf:function(z){var t=1/(1+0.2316419*Math.abs(z)),d=0.3989423*Math.exp(-z*z/2),p=d*t*(0.3193815+t*(-0.3565638+t*(1.781478+t*(-1.821256+t*1.330274))));return z>0?1-p:p;},
  cov:function(x,y){var mx=calc.mean(x),my=calc.mean(y),s=0;for(var i=0;i<x.length;i++)s+=(x[i]-mx)*(y[i]-my);return s/x.length;},
  corr:function(x,y){return calc.cov(x,y)/Math.sqrt(calc.varp(x)*calc.varp(y));},
  eig2:function(a,b,d){var tr=a+d,dt=a*d-b*b,disc=Math.sqrt(Math.max(0,tr*tr/4-dt)),l1=tr/2+disc,l2=tr/2-disc;
    var v1=Math.abs(b)>1e-12?[b,l1-a]:(a>=d?[1,0]:[0,1]);var n=Math.hypot(v1[0],v1[1]);v1=[v1[0]/n,v1[1]/n];return {l1:l1,l2:l2,v1:v1,v2:[-v1[1],v1[0]]};},
  gd:function(th,a,n){var p=[th];for(var i=0;i<n;i++){th=th-a*2*th;p.push(th);}return p;}
};

var W={};
/* 01 함수 그리기 */
W.func=function(P){P.innerHTML='<div class="ptitle">함수 기계 — 입력 x를 넣으면 출력 y가 나온다</div><div class="ctrl" id="fn_b"></div>'+slider('fn_a','a (기울기·폭)',-3,3,0.5,2)+slider('fn_c','b (위아래 이동)',-5,5,1,3)+
  '<div class="row2"><canvas class="cv" id="fn_cv" aria-label="함수 그래프"></canvas><div><table class="mt" id="fn_tb"></table><div class="msg" id="fn_m"></div></div></div>';
  var kind='lin',K=[['lin','일차 ax + b'],['quad','이차 ax² + b'],['sqrt','제곱근 a√x + b'],['sin','삼각 a·sin x + b'],['exp','지수 a·eˣ + b']];
  function f(x){var a=sv('fn_a'),b=sv('fn_c');return kind==='lin'?a*x+b:kind==='quad'?a*x*x+b:kind==='sqrt'?(x<0?NaN:a*Math.sqrt(x)+b):kind==='sin'?a*Math.sin(x)+b:a*Math.exp(x)+b;}
  function draw(){setv('fn_a_v',f2(sv('fn_a')));setv('fn_c_v',f2(sv('fn_c')));var F=frame($('#fn_cv'),[-4,4],[-10,10],{xl:'x',yl:'y'});curve(F,f,-4,4,C('--c-fly'));
    var rows='<tr><td><b>x</b></td><td><b>f(x)</b></td></tr>';[-2,-1,0,1,2].forEach(function(x){var y=f(x);rows+='<tr><td>'+x+'</td><td>'+(isNaN(y)?'없음':f2(y,3))+'</td></tr>';if(!isNaN(y)&&Math.abs(y)<=10)dot(F,x,y,C('--c-fly'));});$('#fn_tb').innerHTML=rows;
    var m={lin:'일차함수는 x가 1 늘 때마다 y가 a만큼 늘어요. a=2, b=3이면 원자료의 f(x) = 2x + 3과 같습니다.',quad:'이차함수는 a가 양수면 아래로 볼록한 그릇, 음수면 뒤집힌 그릇이에요. 손실 함수가 이런 그릇 모양입니다.',
      sqrt:'√x는 음수를 넣을 수 없어요. 그래서 정의역(넣을 수 있는 x)은 x ≥ 0, 표에서 x = −2, −1은 "없음"입니다.',sin:'sin은 오르내림이 되풀이되는 비선형 함수예요. 계절·하루 주기 데이터에 씁니다.',exp:'eˣ는 x가 조금 늘어도 y가 빠르게 커져요. a가 양수면 출력은 늘 b보다 큽니다(치역 y > b).'}[kind];setv('fn_m',m);}
  bbar($('#fn_b'),K,kind,function(v){kind=v;draw();});bind(P,draw);U.reg($('#fn_cv'),function(dt){if(!dt)draw();});draw();};

/* 02 행렬 모양 */
W.shape=function(P){P.innerHTML='<div class="ptitle">표를 행렬로 — 행은 표본, 열은 특성</div>'+slider('sh_m','행의 수 m (표본)',1,5,1,2)+slider('sh_n','열의 수 n (특성)',1,5,1,3)+
  '<div class="ctrl"><button class="bt" type="button" id="sh_t" aria-pressed="false">전치 Aᵀ 보기</button><button class="bt" type="button" id="sh_i" aria-pressed="false">단위행렬로 채우기</button></div><div class="row2"><div><table class="mt" id="sh_tb"></table><div class="msg" id="sh_info">표 속 숫자 하나를 눌러 보세요.</div></div><div class="msg" id="sh_m"></div></div>';
  var tr=false,idm=false,pick=null;
  function draw(){var m=sv('sh_m'),n=sv('sh_n');setv('sh_m_v',m);setv('sh_n_v',n);var R=tr?n:m,Cc=tr?m:n,h='';
    for(var i=1;i<=R;i++){h+='<tr>';for(var j=1;j<=Cc;j++){var oi=tr?j:i,oj=tr?i:j,v=idm?(oi===oj?1:0):(oi-1)*n+oj;h+='<td tabindex="0" data-i="'+i+'" data-j="'+j+'" class="'+(pick&&pick[0]===i&&pick[1]===j?'hl':'')+'">'+v+'</td>';}h+='</tr>';}
    $('#sh_tb').innerHTML=h;$$('#sh_tb td').forEach(function(td){td.onclick=td.onfocus=function(){pick=[+td.dataset.i,+td.dataset.j];setv('sh_info','<b>'+(tr?'Aᵀ':'A')+'<sub>'+pick[0]+pick[1]+'</sub> = '+td.textContent+'</b> — '+pick[0]+'행 '+pick[1]+'열에 있는 수'+(tr?' (원래 A에서는 '+pick[1]+'행 '+pick[0]+'열)':''));$$('#sh_tb td').forEach(function(x){x.classList.toggle('hl',x===td);});};});
    var kinds=[];if(R===1)kinds.push('행 행렬');if(Cc===1)kinds.push('열 행렬');if(R===Cc)kinds.push('정사각 행렬');if(idm&&R===Cc)kinds.push('단위행렬 I');if(idm&&R!==Cc)kinds.push('(정사각이 아니라 단위행렬이 아님)');
    setv('sh_m','<b>'+R+' × '+Cc+' 행렬</b> — 숫자 '+(R*Cc)+'개.<br>'+(tr?'전치하면 행과 열이 바뀌어 '+m+' × '+n+'이 '+n+' × '+m+'이 됩니다.':'데이터로 읽으면 표본(사람·물건) '+m+'개, 특성(키·몸무게…) '+n+'개짜리 표예요.')+'<br>이름: '+(kinds.join(', ')||'일반 직사각 행렬'));}
  $('#sh_t').onclick=function(){tr=!tr;this.setAttribute('aria-pressed',tr);pick=null;draw();};$('#sh_i').onclick=function(){idm=!idm;this.setAttribute('aria-pressed',idm);draw();};bind(P,function(){pick=null;draw();});draw();};

/* 03 벡터 연산 */
W.vec=function(P){P.innerHTML='<div class="ptitle">화살표 두 개 — 더하기·빼기·늘이기·내적·각도</div><div class="ctrl" id="vc_b"></div>'+slider('vc_ax','a의 x',-5,5,1,3)+slider('vc_ay','a의 y',-5,5,1,1)+slider('vc_bx','b의 x',-5,5,1,1)+slider('vc_by','b의 y',-5,5,1,3)+slider('vc_k','k (스칼라)',-2,3,0.5,2)+
  '<div class="row2"><canvas class="cv tall" id="vc_cv" aria-label="벡터 그림"></canvas><div>'+rd([['vc_r1','결과 벡터'],['vc_dot','내적 a·b'],['vc_na','길이 ‖a‖'],['vc_nb','길이 ‖b‖'],['vc_cos','cos θ'],['vc_th','사이각 θ']])+'<div class="msg" id="vc_m"></div></div></div>';
  var op='add';
  function draw(){['ax','ay','bx','by','k'].forEach(function(k){setv('vc_'+k+'_v',f2(sv('vc_'+k)));});var a=[sv('vc_ax'),sv('vc_ay')],b=[sv('vc_bx'),sv('vc_by')],k=sv('vc_k');
    var F=frame($('#vc_cv'),[-10,10],[-10,10],{sx:2,sy:2});var ca=C('--c-fly'),cb=C('--info'),cr=C('--gfp');
    arrowV(F,0,0,a[0],a[1],ca);txt(F,a[0],a[1],'a',ca);if(op!=='k'){arrowV(F,0,0,b[0],b[1],cb);txt(F,b[0],b[1],'b',cb);}var r;
    if(op==='add'){r=[a[0]+b[0],a[1]+b[1]];F.g.setLineDash([4,4]);arrowV(F,a[0],a[1],r[0],r[1],cb,1.5);F.g.setLineDash([]);arrowV(F,0,0,r[0],r[1],cr,3);txt(F,r[0],r[1],'a+b',cr);setv('vc_r1','['+r+']');setv('vc_m','덧셈은 같은 자리끼리: ['+a[0]+'+'+b[0]+', '+a[1]+'+'+b[1]+'] = ['+r+']. 그림으로는 a 끝에 b를 이어 붙인 곳.');}
    else if(op==='sub'){r=[a[0]-b[0],a[1]-b[1]];arrowV(F,b[0],b[1],a[0],a[1],cr,3);txt(F,(a[0]+b[0])/2,(a[1]+b[1])/2,'a−b',cr);setv('vc_r1','['+r+']');setv('vc_m','뺄셈 a − b = ['+r+']는 "b 끝에서 a 끝으로 가는 화살표"예요. 길이 '+f2(calc.norm(r))+'가 곧 두 점 사이 거리.');}
    else if(op==='k'){r=[k*a[0],k*a[1]];arrowV(F,0,0,r[0],r[1],cr,3);txt(F,r[0]*0.6,r[1]*0.6,k+'a',cr);setv('vc_r1','['+r.map(function(x){return f2(x);})+']');setv('vc_m',k<0?'k가 음수면 방향이 반대로 뒤집혀요.':'k = '+k+'배: 방향은 그대로, 길이만 '+Math.abs(k)+'배('+f2(calc.norm(a))+' → '+f2(calc.norm(r))+').');}
    else{setv('vc_r1','—');var th=calc.angle(a,b);setv('vc_m',Math.abs(calc.dot(a,b))<1e-9?'내적 0 → 두 화살표가 직각(수직)이에요. AI에서는 "서로 전혀 닮지 않음".':calc.dot(a,b)>0?'내적이 양수 → 사이각이 90°보다 작아요. 비슷한 쪽을 가리킵니다.':'내적이 음수 → 사이각이 90°보다 커요. 반대쪽을 가리킵니다.');
      var t1=Math.atan2(a[1],a[0]),t2=Math.atan2(b[1],b[0]);F.g.beginPath();F.g.strokeStyle=C('--amber');F.g.lineWidth=2;var rr=28,s=t1,e=t2;var d=((e-s+3*Math.PI)%(2*Math.PI))-Math.PI;F.g.arc(F.X(0),F.Y(0),rr,-s,-(s+d),d>0);F.g.stroke();}
    var na=calc.norm(a),nb=calc.norm(b),dp=calc.dot(a,b);setv('vc_dot',dp);setv('vc_na',f2(na));setv('vc_nb',f2(nb));setv('vc_cos',na&&nb?f2(dp/(na*nb),3):'—');setv('vc_th',na&&nb?f2(calc.angle(a,b),1)+'°':'—');}
  bbar($('#vc_b'),[['add','더하기 a+b'],['sub','빼기 a−b'],['k','스칼라배 k·a'],['dot','내적·각도']],op,function(v){op=v;draw();});bind(P,draw);U.reg($('#vc_cv'),function(dt){if(!dt)draw();});draw();};

/* 04 행렬곱 */
W.matmul=function(P){P.innerHTML='<div class="ptitle">행렬곱 — 결과의 숫자 하나를 눌러 어디서 왔는지 보기</div><p>A(2×3)의 <b>행 하나</b>와 B(3×2)의 <b>열 하나</b>를 짝지어 곱하고 더하면 결과 숫자 하나가 됩니다. 숫자 상자를 고쳐도 됩니다.</p>'+
  '<div class="row2"><div><b>A</b><table class="mt" id="mm_a"></table><b>B</b><table class="mt" id="mm_b"></table></div><div><b>A × B (2×2)</b><table class="mt" id="mm_c"></table><div class="msg step" id="mm_s"></div></div></div>'+
  '<div class="ptitle" style="margin-top:14px">모양 검사기 — 곱할 수 있을까?</div>'+slider('mm_m','앞 행렬 행 m',1,5,1,2)+slider('mm_k1','앞 행렬 열 k',1,5,1,3)+slider('mm_k2','뒤 행렬 행 k′',1,5,1,3)+slider('mm_n','뒤 행렬 열 n',1,5,1,2)+'<div class="msg" id="mm_chk"></div>';
  var A=[[1,2,3],[4,5,6]],Bm=[[7,8],[9,10],[11,12]],sel=[0,0];
  function tbl(id,M,nm){$('#'+id).innerHTML=M.map(function(r,i){return '<tr>'+r.map(function(v,j){return '<td><input type="text" inputmode="numeric" data-m="'+nm+'" data-i="'+i+'" data-j="'+j+'" value="'+v+'" style="width:3em;border:0;text-align:center;background:transparent;font:inherit"></td>';}).join('')+'</tr>';}).join('');}
  function draw(){var Cm=calc.matmul(A,Bm);$('#mm_c').innerHTML=Cm.map(function(r,i){return '<tr>'+r.map(function(v,j){return '<td tabindex="0" data-i="'+i+'" data-j="'+j+'" class="'+(sel[0]===i&&sel[1]===j?'hl':'')+'" style="cursor:pointer">'+v+'</td>';}).join('')+'</tr>';}).join('');
    $$('#mm_c td').forEach(function(td){td.onclick=td.onfocus=function(){sel=[+td.dataset.i,+td.dataset.j];draw();};});
    $$('#mm_a tr').forEach(function(tr,i){$$('td',tr).forEach(function(td){td.classList.toggle('hl',i===sel[0]);});});$$('#mm_b tr').forEach(function(tr){$$('td',tr).forEach(function(td,j){td.classList.toggle('hl2',j===sel[1]);});});
    var i=sel[0],j=sel[1],parts=A[i].map(function(v,k){return v+'×'+Bm[k][j];});setv('mm_s','A의 '+(i+1)+'행 · B의 '+(j+1)+'열<br>'+parts.join(' + ')+' = '+A[i].map(function(v,k){return v*Bm[k][j];}).join(' + ')+' = <b>'+Cm[i][j]+'</b>');
    var m=sv('mm_m'),k1=sv('mm_k1'),k2=sv('mm_k2'),n=sv('mm_n');['m','k1','k2','n'].forEach(function(x){setv('mm_'+x+'_v',sv('mm_'+x));});
    setv('mm_chk',k1===k2?'('+m+'×'+k1+') × ('+k2+'×'+n+') → <b>곱할 수 있어요. 결과는 '+m+'×'+n+'</b>. 가운데 두 수('+k1+'와 '+k2+')가 같아야 짝이 맞습니다.':'('+m+'×'+k1+') × ('+k2+'×'+n+') → <b>곱할 수 없어요.</b> 앞 행렬의 열 수 '+k1+'과 뒤 행렬의 행 수 '+k2+'가 달라 행·열 짝이 남거나 모자랍니다.');}
  tbl('mm_a',A,'A');tbl('mm_b',Bm,'B');$$('#mm_a input,#mm_b input').forEach(function(inp){inp.addEventListener('input',function(){var v=parseFloat(inp.value);if(!isFinite(v))return;(inp.dataset.m==='A'?A:Bm)[+inp.dataset.i][+inp.dataset.j]=v;draw();});});
  $$('input[type=range]',P).forEach(function(i){i.addEventListener('input',draw);});draw();};

/* 05 연립방정식 */
W.sys=function(P){P.innerHTML='<div class="ptitle">두 직선이 만나는 곳 = 연립방정식의 해</div><div class="ctrl" id="sy_b"></div><p class="muted" style="font-size:14px">식 ①: a₁x + b₁y = c₁ · 식 ②: a₂x + b₂y = c₂</p>'+
  slider('sy_a1','a₁',-5,5,1,2)+slider('sy_b1','b₁',-5,5,1,3)+slider('sy_c1','c₁',-10,10,1,7)+slider('sy_a2','a₂',-5,5,1,1)+slider('sy_b2','b₂',-5,5,1,-1)+slider('sy_c2','c₂',-10,10,1,1)+
  '<div class="row2"><canvas class="cv tall" id="sy_cv" aria-label="두 직선"></canvas><div>'+rd([['sy_d','det(A) = a₁b₂ − b₁a₂'],['sy_x','x'],['sy_y','y'],['sy_t','해의 종류']])+'<div class="msg" id="sy_m"></div></div></div>';
  var PR={orig:[2,3,7,1,-1,1],inf:[1,1,2,2,2,4],none:[1,1,2,1,1,3]};
  function draw(){var v=['a1','b1','c1','a2','b2','c2'].map(function(k){setv('sy_'+k+'_v',sv('sy_'+k));return sv('sy_'+k);});var F=frame($('#sy_cv'),[-6,6],[-6,6],{sx:1,sy:1});
    function line(a,b,c,col){if(Math.abs(b)>1e-9)curve(F,function(x){return (c-a*x)/b;},-6,6,col,2.5);else if(Math.abs(a)>1e-9){F.g.strokeStyle=col;F.g.lineWidth=2.5;F.g.beginPath();F.g.moveTo(F.X(c/a),F.Y(-6));F.g.lineTo(F.X(c/a),F.Y(6));F.g.stroke();}}
    line(v[0],v[1],v[2],C('--c-fly'));line(v[3],v[4],v[5],C('--info'));var s=calc.solve2.apply(null,v);setv('sy_d',f2(calc.det2(v[0],v[1],v[3],v[4])));
    if(s.type==='one'){dot(F,s.x,s.y,C('--gfp'),6);setv('sy_x',f2(s.x,3));setv('sy_y',f2(s.y,3));setv('sy_t','해가 하나');setv('sy_m','두 직선이 한 점 ('+f2(s.x,3)+', '+f2(s.y,3)+')에서 만나요. 크라메르 공식: x = det(Aₓ)/det(A) = '+f2(s.Dx)+'/'+f2(s.D)+', y = '+f2(s.Dy)+'/'+f2(s.D)+'.');}
    else{setv('sy_x','—');setv('sy_y','—');setv('sy_t',s.type==='inf'?'해가 무수히 많음':'해가 없음');setv('sy_m',s.type==='inf'?'두 식이 사실은 같은 직선이에요(한 식이 다른 식의 몇 배). 겹친 모든 점이 해입니다.':'det(A) = 0이고 두 직선이 평행이에요. 만나는 점이 없으니 해가 없습니다.');}}
  bbar($('#sy_b'),[['orig','원자료 예 (2x+3y=7, x−y=1)'],['inf','겹치는 두 직선'],['none','평행한 두 직선']],'orig',function(k){['a1','b1','c1','a2','b2','c2'].forEach(function(id,i){$('#sy_'+id).value=PR[k][i];});draw();});
  bind(P,draw);U.reg($('#sy_cv'),function(dt){if(!dt)draw();});draw();};

/* 06 주사위 */
W.dice=function(P){P.innerHTML='<div class="ptitle">주사위 실험실 — 이론 확률과 실제로 던진 비율</div><div class="ctrl" id="dc_e"></div><div class="ctrl"><button class="bt primary" type="button" data-n="10">10번 던지기</button><button class="bt" type="button" data-n="100">100번</button><button class="bt" type="button" data-n="1000">1000번</button><button class="bt" type="button" id="dc_r">처음부터</button></div>'+
  '<div class="row2"><canvas class="cv" id="dc_cv" aria-label="눈별 횟수"></canvas><div>'+rd([['dc_th','이론 확률 P(E)'],['dc_em','실제 비율'],['dc_n','던진 횟수'],['dc_hit','사건이 일어난 횟수']])+'<div class="msg" id="dc_m"></div></div></div>';
  var cnt=[0,0,0,0,0,0],ev='even',r=rng(7);
  var E={even:[[2,4,6],'짝수 {2, 4, 6}'],low:[[1,2,3],'4 미만 {1, 2, 3}'],or:[[1,2,3,4,6],'짝수 또는 4 미만 (A∪B)'],and:[[2],'짝수이면서 4 미만 (A∩B)'],not:[[1,3,5],'짝수가 아님 (여사건)']};
  function draw(){var S=E[ev][0],n=cnt.reduce(function(a,b){return a+b;},0),hit=S.reduce(function(s,f){return s+cnt[f-1];},0);var F=frame($('#dc_cv'),[0.5,6.5],[0,Math.max(5,Math.max.apply(null,cnt)*1.15)],{sx:1,xl:'눈'});
    for(var f=1;f<=6;f++){var on=S.indexOf(f)>=0;F.g.fillStyle=on?C('--terrain'):'#c9d3dc';var x0=F.X(f-0.35),x1=F.X(f+0.35),y=F.Y(cnt[f-1]);F.g.fillRect(x0,y,x1-x0,F.Y(0)-y);}
    if(n){F.g.strokeStyle=C('--amber');F.g.setLineDash([5,4]);F.g.beginPath();F.g.moveTo(F.X(0.5),F.Y(n/6));F.g.lineTo(F.X(6.5),F.Y(n/6));F.g.stroke();F.g.setLineDash([]);}
    setv('dc_th',S.length+'/6 = '+f2(S.length/6,3));setv('dc_em',n?f2(hit/n,3):'—');setv('dc_n',n);setv('dc_hit',hit);
    setv('dc_m','사건 E = '+E[ev][1]+'. '+(n<30?'적게 던지면 비율이 들쭉날쭉해요. 더 던져 보세요.':'던질수록 실제 비율이 이론값 '+f2(S.length/6,3)+'에 가까워집니다(차이 '+f2(Math.abs(hit/n-S.length/6),3)+'). 점선은 눈마다 기대 횟수 n/6.'));}
  bbar($('#dc_e'),Object.keys(E).map(function(k){return [k,E[k][1]];}),ev,function(v){ev=v;draw();});
  $$('[data-n]',P).forEach(function(b){b.onclick=function(){for(var i=0;i<+b.dataset.n;i++)cnt[Math.floor(r()*6)]++;draw();};});$('#dc_r').onclick=function(){cnt=[0,0,0,0,0,0];draw();};U.reg($('#dc_cv'),function(dt){if(!dt)draw();});draw();};

/* 07 베이즈 */
W.bayes=function(P){P.innerHTML='<div class="ptitle">1000명 검사장 — 양성이 나왔을 때 진짜 병이 있을 확률</div>'+slider('by_p','병이 있는 비율 (사전확률)',0.1,20,0.1,1)+slider('by_s','민감도 (병이 있으면 양성)',50,99.9,0.1,99)+slider('by_f','거짓 양성률 (병이 없는데 양성)',0.1,20,0.1,5)+
  '<div class="row2"><canvas class="cv tall" id="by_cv" aria-label="1000명 그림"></canvas><div>'+rd([['by_tp','진짜 양성 (병 O·양성)'],['by_fp','거짓 양성 (병 X·양성)'],['by_post','P(병 | 양성) 사후확률'],['by_pos','양성 전체']])+'<div class="msg" id="by_m"></div></div></div>';
  function draw(){var p=sv('by_p')/100,s=sv('by_s')/100,f=sv('by_f')/100;setv('by_p_v',f2(p*100,1)+'%');setv('by_s_v',f2(s*100,1)+'%');setv('by_f_v',f2(f*100,1)+'%');
    var N=1000,D=Math.round(N*p),tp=Math.round(D*s),fn=D-tp,fp=Math.round((N-D)*f),tn=N-D-fp,post=calc.bayes(p,s,f);
    var S=U.setup($('#by_cv')),g=S.g,cols=40,rows=25,cw=S.w/cols,ch=S.h/rows,sz=Math.min(cw,ch)*0.72,k=0;var kinds=[[tp,C('--c-fly')],[fn,'#f2b8b5'],[fp,C('--amber')],[tn,'#d6dde4']];
    kinds.forEach(function(kk){for(var i=0;i<kk[0];i++,k++){var x=(k%cols)*cw+cw/2,y=Math.floor(k/cols)*ch+ch/2;g.fillStyle=kk[1];g.beginPath();g.arc(x,y-sz*0.18,sz*0.22,0,7);g.fill();g.fillRect(x-sz*0.25,y+sz*0.05,sz*0.5,sz*0.35);}});
    setv('by_tp',tp+'명');setv('by_fp',fp+'명');setv('by_post',f2(post*100,1)+'%');setv('by_pos',(tp+fp)+'명');
    setv('by_m','빨강 = 병이 있고 양성('+tp+'), 연분홍 = 병이 있는데 음성('+fn+'), 주황 = 병이 없는데 양성('+fp+'), 회색 = 나머지('+tn+').<br>양성 '+(tp+fp)+'명 가운데 진짜 환자는 '+tp+'명 → 약 <b>'+f2(post*100,1)+'%</b>. '+(post<0.5?'병이 드물면 정확한 검사도 양성의 대부분이 거짓 양성이에요.':'병이 흔해지거나 거짓 양성률이 줄면 양성을 더 믿을 수 있어요.'));}
  bind(P,draw);U.reg($('#by_cv'),function(dt){if(!dt)draw();});draw();};

/* 08 기술통계 */
W.stats=function(P){P.innerHTML='<div class="ptitle">숫자 묶음 요약기 — 가운데와 퍼짐</div><div class="ctrl" id="st_b"></div><label for="st_in" style="font-size:14px">숫자를 쉼표로 넣으세요</label><input type="text" id="st_in" value="2, 4, 6, 8, 10">'+
  '<div class="row2"><canvas class="cv" id="st_cv" aria-label="점 그림과 상자 그림"></canvas><div>'+rd([['st_mean','평균'],['st_med','중앙값'],['st_mode','최빈값'],['st_rng','범위'],['st_var','분산 σ²'],['st_sd','표준편차 σ'],['st_q','Q1 · Q3'],['st_iqr','IQR']])+'</div></div><div class="msg" id="st_m"></div>';
  var PR={a:'2, 4, 6, 8, 10',b:'1, 2, 2, 3, 100',c:'1, 2, 4, 6, 8, 10, 12',d:'5, 5, 5, 5, 5'};
  function draw(){var a=$('#st_in').value.split(/[,\s]+/).map(parseFloat).filter(isFinite);if(a.length<2){setv('st_m','숫자를 두 개 이상 넣어 주세요.');return;}
    var m=calc.mean(a),md=calc.median(a),mo=calc.mode(a),v=calc.varp(a),q=calc.quart(a),mn=Math.min.apply(null,a),mx=Math.max.apply(null,a);
    setv('st_mean',f2(m,3));setv('st_med',f2(md,3));setv('st_mode',mo?mo.join(', '):'없음');setv('st_rng',f2(mx-mn,3));setv('st_var',f2(v,3));setv('st_sd',f2(Math.sqrt(v),3));setv('st_q',f2(q[0],2)+' · '+f2(q[2],2));setv('st_iqr',f2(q[2]-q[0],3));
    var pad=(mx-mn)*0.08||1,F=frame($('#st_cv'),[mn-pad,mx+pad],[0,4],{sy:10,B:28});var g=F.g,seen={};
    a.forEach(function(x){seen[x]=(seen[x]||0)+1;dot(F,x,2.6+0.32*(seen[x]-1),C('--info'),5);});
    var y0=F.Y(1.4),y1=F.Y(0.6);g.strokeStyle=C('--text');g.lineWidth=1.6;g.fillStyle='rgba(15,127,134,.15)';g.fillRect(F.X(q[0]),y0,F.X(q[2])-F.X(q[0]),y1-y0);g.strokeRect(F.X(q[0]),y0,F.X(q[2])-F.X(q[0]),y1-y0);
    g.beginPath();g.moveTo(F.X(q[1]),y0);g.lineTo(F.X(q[1]),y1);g.moveTo(F.X(mn),(y0+y1)/2);g.lineTo(F.X(q[0]),(y0+y1)/2);g.moveTo(F.X(q[2]),(y0+y1)/2);g.lineTo(F.X(mx),(y0+y1)/2);g.stroke();
    g.strokeStyle=C('--c-fly');g.setLineDash([5,4]);g.beginPath();g.moveTo(F.X(m),F.Y(3.9));g.lineTo(F.X(m),F.Y(0.2));g.stroke();g.setLineDash([]);U.label(g,F.X(m),F.Y(3.85),'평균',C('--c-fly'),'center');
    setv('st_m',Math.abs(m-md)>(mx-mn)*0.15?'평균('+f2(m,2)+')이 중앙값('+f2(md,2)+')에서 멀리 끌려갔어요. 큰 값 하나(이상치)가 평균을 잡아당긴 거예요. 이럴 땐 중앙값이 "보통"을 더 잘 말합니다.':'평균('+f2(m,2)+')과 중앙값('+f2(md,2)+')이 가까워요. 한쪽으로 쏠리지 않은 묶음입니다. 아래 상자 그림의 상자가 가운데 절반(Q1~Q3)이에요.');}
  bbar($('#st_b'),[['a','원자료 2,4,6,8,10'],['b','이상치 1,2,2,3,100'],['c','사분위 예 1~12'],['d','모두 같은 5']],'a',function(k){$('#st_in').value=PR[k];draw();});
  bind(P,draw);U.reg($('#st_cv'),function(dt){if(!dt)draw();});draw();};

/* 09 확률분포 */
W.dist=function(P){P.innerHTML='<div class="ptitle">분포 진열장 — 모양을 바꾸며 확률 읽기</div><div class="ctrl" id="ds_b"></div>'+slider('ds_p1','',0,1,0.01,0.5)+slider('ds_p2','',1,20,1,5)+slider('ds_q','',0,20,1,2)+
  '<canvas class="cv tall" id="ds_cv" aria-label="분포 그래프"></canvas><div class="msg" id="ds_m"></div>';
  var kind='binom';var CFG={bern:{p1:['p (성공 확률)',0,1,0.05,0.6],p2:null,q:null},binom:{p1:['p (성공 확률)',0,1,0.05,0.5],p2:['n (시행 횟수)',1,20,1,5],q:['k (성공 횟수)',0,20,1,2]},
    pois:{p1:['λ (평균 횟수)',0.5,10,0.5,3],p2:null,q:['k (일어난 횟수)',0,15,1,2]},norm:{p1:['μ (평균)',150,190,1,170],p2:['σ (표준편차)',2,20,1,10],q:['x 이상일 확률의 x',140,200,1,180]},
    unif:{p1:['a (시작)',0,5,1,0],p2:['b (끝)',6,20,1,10],q:['구간 [2, x]의 x',2,20,1,8]},expo:{p1:['λ (비율)',0.1,2,0.1,0.5],p2:null,q:['x보다 오래 걸릴 확률의 x',0,10,0.5,3]}};
  function setup(){var c=CFG[kind];[['ds_p1',c.p1],['ds_p2',c.p2],['ds_q',c.q]].forEach(function(z){var row=$('#'+z[0]).parentNode;if(!z[1]){row.style.display='none';return;}row.style.display='';row.querySelector('label').textContent=z[1][0];var i=$('#'+z[0]);i.min=z[1][1];i.max=z[1][2];i.step=z[1][3];i.value=z[1][4];});draw();}
  function draw(){var c=CFG[kind],p1=sv('ds_p1'),p2=sv('ds_p2'),q=sv('ds_q'),F,msg;setv('ds_p1_v',f2(p1));setv('ds_p2_v',f2(p2));setv('ds_q_v',f2(q));
    function bars(ks,pf,hl){var mx=0;ks.forEach(function(k){mx=Math.max(mx,pf(k));});F=frame($('#ds_cv'),[ks[0]-0.6,ks[ks.length-1]+0.6],[0,mx*1.2||1],{sx:ks.length>12?2:1});ks.forEach(function(k){F.g.fillStyle=hl(k)?C('--c-fly'):'#9fb7c9';var x0=F.X(k-0.35),x1=F.X(k+0.35),y=F.Y(pf(k));F.g.fillRect(x0,y,x1-x0,F.Y(0)-y);});}
    if(kind==='bern'){bars([0,1],function(k){return k?p1:1-p1;},function(k){return k===1;});msg='베르누이: 한 번 던져 성공(1) 또는 실패(0). P(X=1) = '+f2(p1,2)+', P(X=0) = '+f2(1-p1,2)+'.';}
    else if(kind==='binom'){var n=p2,k=Math.min(q,n);var ks=[];for(var i=0;i<=n;i++)ks.push(i);bars(ks,function(k){return calc.binom(n,p1,k);},function(x){return x===k;});msg='이항: '+n+'번 중 성공 '+k+'번일 확률 = C('+n+','+k+')·'+f2(p1)+'^'+k+'·'+f2(1-p1)+'^'+(n-k)+' = <b>'+f2(calc.binom(n,p1,k),4)+'</b>. 평균 np = '+f2(n*p1,2)+'.';}
    else if(kind==='pois'){ks=[];for(i=0;i<=15;i++)ks.push(i);bars(ks,function(k){return calc.poisson(p1,k);},function(x){return x===q;});msg='포아송: 평균 λ = '+f2(p1)+'번 일어나는 시간에 딱 '+q+'번일 확률 = e^−λ·λ^k/k! = <b>'+f2(calc.poisson(p1,q),4)+'</b>.';}
    else if(kind==='norm'){F=frame($('#ds_cv'),[p1-4*p2,p1+4*p2],[0,calc.npdf(p1,p1,p2)*1.2],{xl:'키 (cm)'});var g=F.g;g.fillStyle='rgba(201,48,48,.22)';g.beginPath();g.moveTo(F.X(q),F.Y(0));for(var x=q;x<=p1+4*p2;x+=p2/20)g.lineTo(F.X(x),F.Y(calc.npdf(x,p1,p2)));g.lineTo(F.X(p1+4*p2),F.Y(0));g.fill();
      curve(F,function(x){return calc.npdf(x,p1,p2);},p1-4*p2,p1+4*p2,C('--info'));var z=(q-p1)/p2;msg='정규: 평균 '+p1+', 표준편차 '+p2+'. x = '+q+'은 평균에서 표준편차 '+f2(z,2)+'개만큼 떨어진 곳(z = '+f2(z,2)+'). 이보다 클 확률(빨간 넓이) ≈ <b>'+f2(1-calc.ncdf(z),3)+'</b>.';}
    else if(kind==='unif'){var a=p1,b=p2,h=1/(b-a);F=frame($('#ds_cv'),[a-1,b+1],[0,h*1.6]);F.g.fillStyle='rgba(201,48,48,.22)';var lo=Math.max(a,2),hi=Math.min(q,b);if(hi>lo)F.g.fillRect(F.X(lo),F.Y(h),F.X(hi)-F.X(lo),F.Y(0)-F.Y(h));F.g.strokeStyle=C('--info');F.g.lineWidth=2.5;F.g.strokeRect(F.X(a),F.Y(h),F.X(b)-F.X(a),F.Y(0)-F.Y(h));
      msg='균등: '+a+'부터 '+b+' 사이 어디나 똑같이 그럴듯해요. 높이 1/(b−a) = '+f2(h,3)+'. P(2 ≤ X ≤ '+q+') = (길이 '+f2(Math.max(0,hi-lo))+') ÷ '+(b-a)+' = <b>'+f2(Math.max(0,hi-lo)*h,3)+'</b>.';}
    else{F=frame($('#ds_cv'),[0,10],[0,p1*1.2],{xl:'기다리는 시간'});g=F.g;g.fillStyle='rgba(201,48,48,.22)';g.beginPath();g.moveTo(F.X(q),F.Y(0));for(x=q;x<=10;x+=0.05)g.lineTo(F.X(x),F.Y(p1*Math.exp(-p1*x)));g.lineTo(F.X(10),F.Y(0));g.fill();curve(F,function(x){return p1*Math.exp(-p1*x);},0,10,C('--info'));
      msg='지수: 다음 일이 일어날 때까지 기다리는 시간. 평균 1/λ = '+f2(1/p1,2)+'. '+q+'보다 오래 기다릴 확률 = e^(−λx) = <b>'+f2(Math.exp(-p1*q),4)+'</b>.';}
    setv('ds_m',msg);}
  bbar($('#ds_b'),[['bern','베르누이'],['binom','이항'],['pois','포아송'],['norm','정규'],['unif','균등'],['expo','지수']],kind,function(v){kind=v;setup();});bind(P,draw);U.reg($('#ds_cv'),function(dt){if(!dt)draw();});setup();};

/* 10 상관 */
W.corr=function(P){P.innerHTML='<div class="ptitle">점 구름 — 함께 움직이는 정도를 숫자 하나로</div><div class="ctrl" id="cr_b"></div>'+slider('cr_r','관계의 세기 (만들 때 쓴 값)',-1,1,0.05,0.8)+slider('cr_s','단위 배율 (Y를 cm→mm처럼 키우기)',1,10,1,1)+
  '<div class="ctrl"><button class="bt" type="button" id="cr_o" aria-pressed="false">튀는 점 하나 넣기</button></div><div class="row2"><canvas class="cv tall" id="cr_cv" aria-label="산점도"></canvas><div>'+rd([['cr_cov','공분산 Cov(X,Y)'],['cr_rv','상관계수 r'],['cr_sx','σX'],['cr_sy','σY']])+'<div class="msg" id="cr_m"></div></div></div>';
  var mode='gen',out=false;
  function pts(){if(mode==='orig')return [[1,2,3,4,5],[2,4,5,4,5]];var r=rng(11),x=[],y=[],t=sv('cr_r');for(var i=0;i<40;i++){var a=gauss(r),b=gauss(r);x.push(5+1.6*a);y.push(5+1.6*(t*a+Math.sqrt(1-t*t)*b));}return [x,y];}
  function draw(){var d=pts(),x=d[0].slice(),y=d[1].slice(),s=sv('cr_s');setv('cr_r_v',f2(sv('cr_r')));setv('cr_s_v','×'+s);if(out){x.push(mode==='orig'?6:9.5);y.push(mode==='orig'?0:0.5);}y=y.map(function(v){return v*s;});
    var mx=calc.mean(x),my=calc.mean(y),F=frame($('#cr_cv'),[0,10],[0,10*s],{xl:'X',yl:'Y'}),g=F.g;g.fillStyle='rgba(19,115,58,.07)';g.fillRect(F.X(mx),F.T,F.w,F.Y(my)-F.T);g.fillRect(F.L,F.Y(my),F.X(mx)-F.L,F.h-F.Bm-F.Y(my));
    g.strokeStyle='rgba(22,33,43,.35)';g.setLineDash([4,4]);g.beginPath();g.moveTo(F.X(mx),F.T);g.lineTo(F.X(mx),F.h-F.Bm);g.moveTo(F.L,F.Y(my));g.lineTo(F.w,F.Y(my));g.stroke();g.setLineDash([]);
    for(var i=0;i<x.length;i++){var pr=(x[i]-mx)*(y[i]-my);dot(F,x[i],y[i],pr>=0?C('--gfp'):C('--c-fly'),out&&i===x.length-1?7:4.5);}
    var cv=calc.cov(x,y),r=calc.corr(x,y);setv('cr_cov',f2(cv,3));setv('cr_rv',f2(r,3));setv('cr_sx',f2(Math.sqrt(calc.varp(x)),3));setv('cr_sy',f2(Math.sqrt(calc.varp(y)),3));
    setv('cr_m','초록 점 = (x−평균)×(y−평균)이 양수(오른쪽 위·왼쪽 아래), 빨강 = 음수. 공분산은 이 곱들의 평균이에요.<br>'+(s>1?'단위 배율을 '+s+'배 하자 공분산은 '+s+'배로 커졌지만 r은 그대로 '+f2(r,3)+' — r은 단위가 없어요.':(out?'튀는 점 하나가 r을 크게 흔들었어요. 산점도를 꼭 같이 보세요.':(Math.abs(r)>0.7?'|r|이 1에 가까워 직선 관계가 강해요.':Math.abs(r)<0.2?'r이 0 가까이 — 직선 관계가 거의 없어요(다른 모양의 관계는 있을 수도).':'중간 정도의 관계예요.'))));}
  bbar($('#cr_b'),[['gen','점 40개 만들기'],['orig','원자료 5점 (r ≈ 0.775)']],mode,function(v){mode=v;draw();});$('#cr_o').onclick=function(){out=!out;this.setAttribute('aria-pressed',out);draw();};bind(P,draw);U.reg($('#cr_cv'),function(dt){if(!dt)draw();});draw();};

/* 11 미분 */
W.deriv=function(P){P.innerHTML='<div class="ptitle">할선이 접선이 되는 순간 — h를 0으로</div><div class="ctrl" id="dv_b"></div>'+slider('dv_x','점 x₀',-2,2,0.1,1)+slider('dv_h','h (두 점 사이 간격)',-3,0.3,0.1,0)+
  '<div class="row2"><canvas class="cv tall" id="dv_cv" aria-label="할선과 접선"></canvas><div>'+rd([['dv_sec','할선 기울기 [f(x₀+h) − f(x₀)]/h'],['dv_tan','미분값 f′(x₀)'],['dv_err','차이'],['dv_hv','h']])+'<div class="msg" id="dv_m"></div></div></div>';
  var kind='sq',FN={sq:[function(x){return x*x;},function(x){return 2*x;},'x²','2x'],cu:[function(x){return x*x*x;},function(x){return 3*x*x;},'x³','3x²'],sin:[Math.sin,Math.cos,'sin x','cos x'],exp:[Math.exp,Math.exp,'eˣ','eˣ']};
  function draw(){var f=FN[kind],x0=sv('dv_x'),h=Math.pow(10,sv('dv_h'));setv('dv_x_v',f2(x0));setv('dv_h_v',f2(h,4));var F=frame($('#dv_cv'),[-3,3],[-4,8],{sx:1,sy:2});curve(F,f[0],-3,3,C('--info'));
    var y0=f[0](x0),y1=f[0](x0+h),sec=(y1-y0)/h,tan=f[1](x0);curve(F,function(x){return y0+sec*(x-x0);},-3,3,C('--amber'),2,[6,4]);curve(F,function(x){return y0+tan*(x-x0);},-3,3,C('--c-fly'),2);dot(F,x0,y0,C('--c-fly'),5.5);dot(F,x0+h,y1,C('--amber'),5);
    setv('dv_sec',f2(sec,4));setv('dv_tan',f2(tan,4));setv('dv_err',f2(Math.abs(sec-tan),4));setv('dv_hv',f2(h,4));setv('dv_m','f(x) = '+f[2]+', 도함수 f′(x) = '+f[3]+'. 주황 점선(할선)은 두 점을 잇는 선, 빨간 선(접선)은 한 점에서 스치는 선이에요. h를 줄이면 할선 기울기 '+f2(sec,3)+'가 미분값 '+f2(tan,3)+'로 다가갑니다. 이것이 극한 h → 0.');}
  bbar($('#dv_b'),[['sq','x²'],['cu','x³'],['sin','sin x'],['exp','eˣ']],kind,function(v){kind=v;draw();});bind(P,draw);U.reg($('#dv_cv'),function(dt){if(!dt)draw();});draw();};

/* 12 그래디언트 */
W.grad=function(P){P.innerHTML='<div class="ptitle">등고선 지도 위의 화살표 — 지도를 눌러 점을 옮기세요</div><div class="ctrl" id="gr_b"></div>'+
  '<div class="row2"><canvas class="cv tall" id="gr_cv" aria-label="등고선과 그래디언트" tabindex="0"></canvas><div>'+rd([['gr_p','점 (x, y)'],['gr_f','높이 f(x, y)'],['gr_fx','∂f/∂x'],['gr_fy','∂f/∂y'],['gr_n','‖∇f‖ 가파름']])+'<div class="msg" id="gr_m"></div></div></div>';
  var kind='bowl',pt=[1,2],FN={bowl:[function(x,y){return x*x+y*y;},function(x,y){return [2*x,2*y];},'x² + y²'],
    mix:[function(x,y){return x*x*y+3*x*y+y*y;},function(x,y){return [2*x*y+3*y,x*x+3*x+2*y];},'x²y + 3xy + y²'],wave:[function(x,y){return Math.sin(x)+Math.cos(y);},function(x,y){return [Math.cos(x),-Math.sin(y)];},'sin x + cos y']};
  function draw(){var f=FN[kind],F=frame($('#gr_cv'),[-3,3],[-3,3],{sx:1,sy:1}),g=F.g,lo=Infinity,hi=-Infinity,N=60,i,j;for(i=0;i<=N;i++)for(j=0;j<=N;j++){var v=f[0](-3+6*i/N,-3+6*j/N);lo=Math.min(lo,v);hi=Math.max(hi,v);}
    var cw=(F.X(3)-F.X(-3))/N,chh=(F.Y(-3)-F.Y(3))/N;for(i=0;i<N;i++)for(j=0;j<N;j++){var t=(f[0](-3+6*(i+.5)/N,-3+6*(j+.5)/N)-lo)/(hi-lo);g.fillStyle='rgba('+Math.round(40+200*t)+','+Math.round(120+60*(1-t))+','+Math.round(200-150*t)+',0.28)';g.fillRect(F.X(-3)+i*cw,F.Y(-3)-(j+1)*chh,cw+0.5,chh+0.5);}
    var gv=f[1](pt[0],pt[1]),n=Math.hypot(gv[0],gv[1]),sc=n>0?Math.min(1.4,n*0.25)/n:0;dot(F,pt[0],pt[1],C('--text'),5);arrowV(F,pt[0],pt[1],pt[0]+gv[0]*sc,pt[1]+gv[1]*sc,C('--c-fly'),3);arrowV(F,pt[0],pt[1],pt[0]-gv[0]*sc,pt[1]-gv[1]*sc,C('--gfp'),2.2);
    setv('gr_p','('+f2(pt[0])+', '+f2(pt[1])+')');setv('gr_f',f2(f[0](pt[0],pt[1]),3));setv('gr_fx',f2(gv[0],3));setv('gr_fy',f2(gv[1],3));setv('gr_n',f2(n,3));
    setv('gr_m','f(x, y) = '+f[2]+'. 빨간 화살표 ∇f = ('+f2(gv[0],2)+', '+f2(gv[1],2)+')는 가장 가파르게 오르는 방향, 초록 화살표는 그 반대인 가장 빠른 내리막(경사하강이 가는 쪽)이에요. 진한 색일수록 높은 곳.');}
  function pick(e){var r=$('#gr_cv').getBoundingClientRect(),F=frame($('#gr_cv'),[-3,3],[-3,3],{sx:1,sy:1});pt=[clamp(F.ix(e.clientX-r.left),-3,3),clamp(F.iy(e.clientY-r.top),-3,3)];pt=[Math.round(pt[0]*10)/10,Math.round(pt[1]*10)/10];draw();}
  $('#gr_cv').addEventListener('pointerdown',pick);$('#gr_cv').addEventListener('keydown',function(e){var d={ArrowLeft:[-.1,0],ArrowRight:[.1,0],ArrowUp:[0,.1],ArrowDown:[0,-.1]}[e.key];if(d){e.preventDefault();pt=[clamp(+(pt[0]+d[0]).toFixed(1),-3,3),clamp(+(pt[1]+d[1]).toFixed(1),-3,3)];draw();}});
  bbar($('#gr_b'),[['bowl','그릇 x²+y²'],['mix','원자료 x²y+3xy+y²'],['wave','물결 sin x+cos y']],kind,function(v){kind=v;draw();});U.reg($('#gr_cv'),function(dt){if(!dt)draw();});draw();};

/* 13 경사하강 */
W.gd=function(P){P.innerHTML='<div class="ptitle">그릇 바닥 찾기 — 학습률 α에 따라 걸음이 달라진다</div>'+slider('gd_a','학습률 α',0.02,1.1,0.02,0.1)+slider('gd_t','출발점 θ₀',-5,5,0.5,4)+slider('gd_n','걸음 수',1,40,1,15)+
  '<div class="row2"><canvas class="cv" id="gd_cv" aria-label="f(θ)=θ² 위의 걸음"></canvas><canvas class="cv" id="gd_cv2" aria-label="걸음마다 손실"></canvas></div>'+rd([['gd_last','마지막 θ'],['gd_loss','마지막 손실 θ²'],['gd_ratio','한 걸음마다 θ에 곱해지는 수 (1−2α)'],['gd_st','상태']])+'<div class="msg" id="gd_m"></div>';
  function draw(){var a=sv('gd_a'),t=sv('gd_t'),n=sv('gd_n');setv('gd_a_v',f2(a));setv('gd_t_v',f2(t));setv('gd_n_v',n);var p=calc.gd(t,a,n),F=frame($('#gd_cv'),[-6,6],[0,36],{sx:2,sy:6,xl:'θ',yl:'f(θ)=θ²'});curve(F,function(x){return x*x;},-6,6,C('--info'));
    var g=F.g;g.strokeStyle=C('--c-fly');g.lineWidth=1.6;g.beginPath();p.forEach(function(th,i){var x=clamp(th,-6,6),y=Math.min(th*th,36);if(i)g.lineTo(F.X(x),F.Y(y));else g.moveTo(F.X(x),F.Y(y));});g.stroke();p.forEach(function(th,i){if(Math.abs(th)<=6)dot(F,th,th*th,i===0?C('--amber'):i===p.length-1?C('--gfp'):C('--c-fly'),i===0||i===p.length-1?5.5:3.5);});
    var L=p.map(function(x){return x*x;}),mxL=Math.min(Math.max.apply(null,L),1e4),F2=frame($('#gd_cv2'),[0,n],[0,mxL*1.1||1],{xl:'걸음',yl:'손실'});curve(F2,function(x){var i=Math.round(x);return L[clamp(i,0,n)];},0,n,C('--c-fly'));
    var r=1-2*a,last=p[p.length-1],st=Math.abs(r)>=1?(Math.abs(r)===1?'제자리 왕복':'발산'):(r<0?'지그재그로 수렴':'수렴');setv('gd_last',f2(last,4));setv('gd_loss',f2(last*last,4));setv('gd_ratio',f2(r,2));setv('gd_st',st);
    setv('gd_m',{'수렴':'α = '+a+': 걸음마다 θ가 '+f2(r,2)+'배로 줄어 바닥(0)에 다가가요. '+(a<0.05?'너무 작으면 바닥까지 한참 걸립니다.':''),'지그재그로 수렴':'α가 0.5보다 커서 바닥을 넘어 반대편에 착지하지만, 넘는 폭이 줄어 결국 바닥에 닿아요.','제자리 왕복':'α = 1: θ가 '+t+'과 '+(-t)+' 사이를 영원히 오가요.','발산':'α가 1보다 커서 걸음마다 바닥에서 더 멀어져요(손실 폭발). 학습률이 너무 클 때 생기는 일.'}[st]);}
  bind(P,draw);U.reg($('#gd_cv'),function(dt){if(!dt)draw();});draw();};

/* 14 고유벡터·PCA */
W.pca=function(P){P.innerHTML='<div class="ptitle">데이터의 주축 찾기 — 공분산 행렬의 고유벡터</div><div class="ctrl" id="pc_b"></div><div id="pc_c1">'+slider('pc_ang','점 구름의 기울기 (°)',-80,80,5,40)+slider('pc_sp','길쭉함 (긴 축 ÷ 짧은 축)',1,6,0.5,3)+
  '<div class="ctrl"><button class="bt" type="button" id="pc_pj" aria-pressed="false">PC1 위로 내려 찍기 (2차원 → 1차원)</button></div></div><div id="pc_c2" style="display:none">'+slider('pc_a','a',0,5,0.5,4)+slider('pc_bb','b (= c)',-3,3,0.5,1)+slider('pc_d','d',0,5,0.5,3)+'</div>'+
  '<div class="row2"><canvas class="cv tall" id="pc_cv" aria-label="점 구름과 주성분"></canvas><div>'+rd([['pc_l1','λ₁ (큰 고윳값)'],['pc_l2','λ₂'],['pc_ex','PC1이 설명하는 몫'],['pc_v1','고유벡터 v₁']])+'<div class="msg" id="pc_m"></div></div></div>';
  var mode='data',proj=false;
  function draw(){var F=frame($('#pc_cv'),[-6,6],[-6,6],{sx:2,sy:2}),g=F.g,E;
    if(mode==='data'){var an=sv('pc_ang')*Math.PI/180,sp=sv('pc_sp'),r=rng(5),X=[],Y=[];setv('pc_ang_v',sv('pc_ang')+'°');setv('pc_sp_v',f2(sp));
      for(var i=0;i<80;i++){var u=gauss(r)*1.2*Math.sqrt(sp),v=gauss(r)*1.2/Math.sqrt(sp);X.push(u*Math.cos(an)-v*Math.sin(an));Y.push(u*Math.sin(an)+v*Math.cos(an));}
      var mx=calc.mean(X),my=calc.mean(Y);X=X.map(function(x){return x-mx;});Y=Y.map(function(y){return y-my;});var a=calc.varp(X),b=calc.cov(X,Y),d=calc.varp(Y);E=calc.eig2(a,b,d);
      for(i=0;i<X.length;i++){if(proj){var t=X[i]*E.v1[0]+Y[i]*E.v1[1];g.strokeStyle='rgba(22,33,43,.18)';g.beginPath();g.moveTo(F.X(X[i]),F.Y(Y[i]));g.lineTo(F.X(t*E.v1[0]),F.Y(t*E.v1[1]));g.stroke();dot(F,t*E.v1[0],t*E.v1[1],C('--gfp'),3.5);}dot(F,X[i],Y[i],proj?'rgba(30,85,200,.35)':C('--info'),3.5);}
      setv('pc_m','공분산 행렬 Σ = [['+f2(a,2)+', '+f2(b,2)+'], ['+f2(b,2)+', '+f2(d,2)+']]. 빨간 화살표(PC1)가 점이 가장 넓게 퍼진 방향, 주황(PC2)이 그와 직각이에요. '+(proj?'초록 점은 PC1 한 줄로 내려 찍은 모습 — 숫자 두 개를 하나로 줄였는데 퍼짐의 '+f2(100*E.l1/(E.l1+E.l2),1)+'%가 남았어요.':'버튼을 눌러 2차원을 1차원으로 줄여 보세요.'));}
    else{var A=[sv('pc_a'),sv('pc_bb'),sv('pc_d')];['a','bb','d'].forEach(function(k){setv('pc_'+k+'_v',f2(sv('pc_'+k)));});E=calc.eig2(A[0],A[1],A[2]);
      g.strokeStyle='rgba(22,33,43,.35)';g.beginPath();for(var k=0;k<=100;k++){var th=2*Math.PI*k/100;if(k)g.lineTo(F.X(Math.cos(th)),F.Y(Math.sin(th)));else g.moveTo(F.X(1),F.Y(0));}g.stroke();
      g.strokeStyle=C('--info');g.lineWidth=2;g.beginPath();for(k=0;k<=100;k++){th=2*Math.PI*k/100;var x=Math.cos(th),y=Math.sin(th),px=A[0]*x+A[1]*y,py=A[1]*x+A[2]*y;if(k)g.lineTo(F.X(px),F.Y(py));else g.moveTo(F.X(px),F.Y(py));}g.stroke();
      setv('pc_m','회색 원(길이 1인 화살표 모두)을 A = [['+A[0]+', '+A[1]+'], ['+A[1]+', '+A[2]+']]로 보내면 파란 타원이 돼요. 대부분의 화살표는 방향이 꺾이지만, 고유벡터 방향만은 방향이 그대로이고 길이만 λ배가 됩니다(Ax = λx). '+(A[0]===4&&A[1]===1&&A[2]===3?'원자료 예: λ = (7 ± √5)/2 ≈ 4.618, 2.382.':''));}
    var s1=Math.sqrt(Math.max(E.l1,0)),s2=Math.sqrt(Math.max(E.l2,0)),k1=mode==='data'?2*s1:E.l1,k2=mode==='data'?2*s2:E.l2;arrowV(F,0,0,E.v1[0]*k1,E.v1[1]*k1,C('--c-fly'),3);arrowV(F,0,0,E.v2[0]*k2,E.v2[1]*k2,C('--amber'),3);
    txt(F,E.v1[0]*k1,E.v1[1]*k1,'v₁',C('--c-fly'));txt(F,E.v2[0]*k2,E.v2[1]*k2,'v₂',C('--amber'));
    setv('pc_l1',f2(E.l1,3));setv('pc_l2',f2(E.l2,3));setv('pc_ex',E.l1+E.l2>0?f2(100*E.l1/(E.l1+E.l2),1)+'%':'—');setv('pc_v1','('+f2(E.v1[0],3)+', '+f2(E.v1[1],3)+')');}
  bbar($('#pc_b'),[['data','데이터 점 구름 (PCA)'],['mat','행렬 A로 원 늘이기 (고유벡터)']],mode,function(v){mode=v;$('#pc_c1').style.display=v==='data'?'':'none';$('#pc_c2').style.display=v==='mat'?'':'none';draw();});
  $('#pc_pj').onclick=function(){proj=!proj;this.setAttribute('aria-pressed',proj);draw();};bind(P,draw);U.reg($('#pc_cv'),function(dt){if(!dt)draw();});draw();};

/* 15 공식 도감 검색 */
var FORM=[['01','함수','y = f(x)','입력 x 하나에 출력 y 하나','01_math_basics.html#m01-function'],['01','일차함수','f(x) = ax + b','기울기 a, 절편 b','01_math_basics.html#m01-types'],['01','정의역·치역','√x: x ≥ 0, y ≥ 0','넣을 수 있는 값·나올 수 있는 값','01_math_basics.html#m01-domain'],
  ['02','행렬 크기','m × n','행 m개, 열 n개','02_linear_algebra.html#m02-dim'],['02','전치','(Aᵀ)ᵢⱼ = Aⱼᵢ','행과 열 바꾸기','02_linear_algebra.html#m02-notation'],['02','데이터 행렬','X ∈ ℝ^(m×n)','행 = 표본, 열 = 특성','02_linear_algebra.html#m02-data'],
  ['03','벡터 덧셈','a + b = [a₁+b₁, …]','같은 자리끼리','03_vector_ops.html#m03-add'],['03','내적','a·b = a₁b₁ + … + aₙbₙ','닮음을 재는 숫자 하나','03_vector_ops.html#m03-dot'],['03','노름(L2)','‖v‖ = √(v₁² + … + vₙ²)','화살표 길이','03_vector_ops.html#m03-norm'],['03','코사인 유사도','cos θ = a·b / (‖a‖‖b‖)','방향이 닮은 정도','03_vector_ops.html#m03-angle'],
  ['04','행렬곱','(AB)ᵢⱼ = Σₖ AᵢₖBₖⱼ','행 × 열','04_matrix_ops.html#m04-mul'],['04','역행렬(2×2)','A⁻¹ = 1/(ad−bc)·[[d, −b], [−c, a]]','ad − bc ≠ 0일 때만','04_matrix_ops.html#m04-inv'],['04','단위행렬','AI = IA = A','곱해도 그대로','04_matrix_ops.html#m04-identity'],
  ['05','행렬 방정식','Ax = b','계수 × 미지수 = 상수','05_linear_systems.html#m05-matrix'],['05','역행렬 풀이','x = A⁻¹b','det A ≠ 0일 때','05_linear_systems.html#m05-inverse'],['05','크라메르 공식','x = det(Aₓ)/det(A)','열 바꿔 끼운 행렬식','05_linear_systems.html#m05-cramer'],['05','정규방정식','β = (XᵀX)⁻¹Xᵀy','선형 회귀의 답','05_linear_systems.html#m05-regression'],
  ['06','확률 범위','0 ≤ P(E) ≤ 1','0 불가능, 1 확실','06_probability.html#m06-what'],['06','고전적 확률','P(E) = 유리한 경우 ÷ 전체 경우','모든 결과가 똑같이 그럴듯할 때','06_probability.html#m06-classic'],['06','여사건','P(Eᶜ) = 1 − P(E)','일어나지 않을 확률','06_probability.html#m06-complement'],['06','덧셈 법칙','P(A∪B) = P(A) + P(B) − P(A∩B)','겹친 곳 한 번 빼기','06_probability.html#m06-union'],['06','곱셈 법칙(독립)','P(A∩B) = P(A)P(B)','서로 영향 없을 때','06_probability.html#m06-mult'],
  ['07','조건부 확률','P(A|B) = P(A∩B)/P(B)','B가 일어났다는 조건에서 A','07_bayes.html#m07-formula'],['07','베이즈 정리','P(A|B) = P(B|A)P(A)/P(B)','새 증거로 믿음 고치기','07_bayes.html#m07-bayes'],
  ['08','평균','x̄ = Σxᵢ / n','다 더해 개수로 나누기','08_statistics.html#m08-center'],['08','분산(모집단)','σ² = Σ(xᵢ−μ)² / n','평균에서 떨어진 정도의 제곱 평균','08_statistics.html#m08-spread'],['08','표본분산','s² = Σ(xᵢ−x̄)² / (n−1)','표본으로 모집단 추정','15_quick_revision.html#m15-stat'],['08','IQR','IQR = Q3 − Q1','가운데 절반의 폭','08_statistics.html#m08-quartile'],
  ['09','베르누이','P(X=x) = pˣ(1−p)¹⁻ˣ','한 번 시행','09_distributions.html#m09-bern'],['09','이항','P(X=k) = C(n,k)pᵏ(1−p)ⁿ⁻ᵏ','n번 중 k번 성공','09_distributions.html#m09-binom'],['09','포아송','P(X=k) = e^−λ λᵏ / k!','정해진 시간에 일어난 횟수','09_distributions.html#m09-pois'],['09','정규','f(x) = e^(−(x−μ)²/2σ²) / (σ√2π)','종 모양','09_distributions.html#m09-normal'],['09','지수','f(x) = λe^(−λx)','기다리는 시간','09_distributions.html#m09-expo'],
  ['10','공분산','Cov(X,Y) = Σ(xᵢ−x̄)(yᵢ−ȳ) / n','함께 움직이는 방향','10_correlation.html#m10-cov'],['10','상관계수','r = Cov(X,Y) / (σXσY)','−1 ≤ r ≤ 1, 단위 없음','10_correlation.html#m10-corr'],
  ['11','미분의 정의','f′(x) = lim(h→0) [f(x+h) − f(x)]/h','순간 기울기','11_calculus.html#m11-deriv'],['11','거듭제곱 미분','(xⁿ)′ = nxⁿ⁻¹','지수를 앞으로, 하나 줄이기','11_calculus.html#m11-table'],['11','연쇄 법칙','(f(g(x)))′ = f′(g(x))·g′(x)','겉 미분 × 속 미분','11_calculus.html#m11-rules'],['11','정적분','∫ₐᵇ f(x)dx = F(b) − F(a)','곡선 아래 넓이','11_calculus.html#m11-definite'],
  ['12','편미분','∂f/∂x','다른 변수는 고정','12_gradient.html#m12-what'],['12','그래디언트','∇f = (∂f/∂x₁, …, ∂f/∂xₙ)','가장 가파른 오르막','12_gradient.html#m12-grad'],['12','접평면','z = f(a,b) + fₓ(x−a) + f_y(y−b)','한 점에서의 평평한 근사','12_gradient.html#m12-tangent'],
  ['13','최적화','θ* = argmin f(θ)','손실이 가장 작은 θ','13_optimization.html#m13-what'],['13','경사하강','θ_new = θ_old − α∇f(θ)','내리막으로 한 걸음','13_optimization.html#m13-gd'],['13','MSE 손실','J = (1/m) Σ(yᵢ − ŷᵢ)²','오차 제곱 평균','13_optimization.html#m13-example'],
  ['14','고윳값 식','Ax = λx','방향은 그대로, 길이만 λ배','14_eigen_pca.html#m14-what'],['14','특성방정식','det(A − λI) = 0','λ 찾는 식','14_eigen_pca.html#m14-find'],['14','대각합·행렬식','tr A = Σλᵢ, det A = Πλᵢ','고윳값으로 검산','14_eigen_pca.html#m14-props'],['14','PCA 변환','Z = X_centered · W','주성분으로 옮기기','14_eigen_pca.html#m14-pca'],
  ['15','시그모이드','σ(x) = 1/(1+e⁻ˣ)','0~1 확률로 바꾸기','15_quick_revision.html#m15-func'],['15','ReLU','f(x) = max(0, x)','음수는 0으로','15_quick_revision.html#m15-func'],['15','소프트맥스','σ(zᵢ) = e^zᵢ / Σe^zⱼ','점수를 확률 분포로','15_quick_revision.html#m15-func'],['15','교차 엔트로피','J = −(1/m)Σ[y log ŷ + (1−y)log(1−ŷ)]','분류의 손실','15_quick_revision.html#m15-func'],['15','헤세 행렬','Hᵢⱼ = ∂²f/∂xᵢ∂xⱼ','굽은 정도(2차 미분)','15_quick_revision.html#m15-opt']];
W.revise=function(P){P.innerHTML='<div class="ptitle">공식 도감 — '+FORM.length+'개 공식을 이름·기호·뜻으로 찾기</div><input type="text" id="rv_q" placeholder="예: 내적, 분산, λ, 미분, 확률" aria-label="공식 찾기"><div class="ctrl" style="margin-top:8px"><button class="bt primary" type="button" id="rv_card">공식 카드 뽑기</button><button class="bt" type="button" id="rv_show">답 보기</button><span id="rv_cnt" class="muted" style="font-size:14px"></span></div><div class="msg" id="rv_c">카드를 뽑으면 이름만 보입니다. 식을 떠올려 본 뒤 "답 보기"를 누르세요.</div><div class="tblwrap"><table class="cmp" id="rv_tb"></table></div>';
  var cur=null,r=rng(3);function draw(){var q=$('#rv_q').value.trim().toLowerCase(),rows=FORM.filter(function(f){return !q||f.join(' ').toLowerCase().indexOf(q)>=0;});setv('rv_cnt',rows.length+'개');
    $('#rv_tb').innerHTML='<thead><tr><th>장</th><th>이름</th><th>식</th><th>뜻</th></tr></thead><tbody>'+rows.map(function(f){return '<tr><td>'+f[0]+'</td><td><a href="'+f[4]+'">'+f[1]+'</a></td><td style="white-space:nowrap">'+f[2]+'</td><td>'+f[3]+'</td></tr>';}).join('')+'</tbody>';}
  $('#rv_card').onclick=function(){cur=FORM[Math.floor(r()*FORM.length)];setv('rv_c','<b>'+cur[1]+'</b> ('+cur[0]+'장) — 식을 떠올려 보세요.');};$('#rv_show').onclick=function(){if(cur)setv('rv_c','<b>'+cur[1]+'</b>: '+cur[2]+' — '+cur[3]+' <a href="'+cur[4]+'">도감에서 보기</a>');};
  $('#rv_q').addEventListener('input',draw);draw();};

function mountAll(){$$('[data-w]').forEach(function(p){var f=W[p.dataset.w];if(f)try{f(p);}catch(e){p.innerHTML='<p class="msg">실험판을 여는 중 문제가 생겼어요: '+U.esc(e.message)+'</p>';if(window.console)console.error(e);}});}
function copyButtons(){$$('button.cpy').forEach(function(b){b.onclick=function(){var t=$('#'+b.dataset.copy).innerText;function ok(){b.textContent='복사됨';setTimeout(function(){b.textContent='복사';},1500);}
  if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(t).then(ok,function(){fallback(t);ok();});else{fallback(t);ok();}};});
  function fallback(t){var ta=document.createElement('textarea');ta.value=t;document.body.appendChild(ta);ta.select();try{document.execCommand('copy');}catch(e){}ta.remove();}}
return {W:W,calc:calc,FORM:FORM,mountAll:mountAll,copyButtons:copyButtons,f2:f2,frame:frame,curve:curve,dot:dot,arrowV:arrowV,txt:txt,slider:slider,rd:rd,setv:setv,sv:sv};
})();
if(typeof module!=='undefined')module.exports=ML;
