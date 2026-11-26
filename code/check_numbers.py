# 숫자 검산: 도감 항목·실험실·그림·AI 판단 코너에 적은 모든 예시 숫자를 다시 계산한다.
# python3 code/check_numbers.py   (마지막에 실험실 계산 모듈 build/mathlab.js의 calc도 node로 검산)
import math, os, subprocess, json
import numpy as np
from fractions import Fraction as Fr
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
n = 0
def ok(cond, msg):
    global n
    assert cond, msg
    n += 1
near = lambda a, b, t=5e-4: abs(a - b) <= t
# 01
f = lambda x: 2 * x + 3
ok([f(x) for x in [-2, -1, 0, 1, 2]] == [-1, 1, 3, 5, 7], '01 표'); ok((11 - 3) / 2 == 4, '01 방정식')
ok(near(2 * math.pi, 6.283) and near(4 * math.pi, 12.566), '01 원 둘레'); ok(near(math.e ** 2, 7.389), '01 e^2')
# 02·03
ok(np.array([[1, 2, 3], [4, 5, 6]])[1, 2] == 6, '02 A23')
a, b = np.array([1, 2, 3]), np.array([4, 5, 6])
ok(a @ b == 32 and near(np.linalg.norm(a), 3.742) and near(np.linalg.norm(b), 8.775), '03 내적·노름')
ok(near(math.degrees(math.acos(32 / (math.sqrt(14) * math.sqrt(77)))), 12.9, 0.05), '03 각도 12.9')
ok(near(math.degrees(math.acos(6 / 10)), 53.13, 0.01), '03 [3,1],[1,3]')
ok(near(math.hypot(99, 198), 221.4, 0.05), '03 거리 221.4'); ok(near(math.sqrt(24), 4.90, 0.005), '03 [4,2,2]')
ok(np.linalg.norm([2, 3, 6]) == 7 and np.linalg.norm([1, 2, 2]) == 3, '03 노름 7, 3')
# 04
A = np.array([[1, 2, 3], [4, 5, 6]]); B = np.array([[7, 8], [9, 10], [11, 12]])
ok((A @ B).tolist() == [[58, 64], [139, 154]], '04 AB'); ok((B @ A).tolist() == [[39, 54, 69], [49, 68, 87], [59, 82, 105]], '04 BA')
ok(np.allclose(np.linalg.inv([[2, 1], [1, 2]]), np.array([[2, -1], [-1, 2]]) / 3), '04 역행렬')
ok((np.array([[1, 2, 3], [4, 5, 6]]) + np.array([[3, 1, 0], [1, 2, 4]])).tolist() == [[4, 3, 3], [5, 7, 10]], '04 덧셈')
# 05
ok(np.allclose(np.linalg.solve([[2, 3], [1, -1]], [7, 1]), [2, 1]), '05 해'); ok(near(np.linalg.det([[7, 3], [1, -1]]), -10) and near(np.linalg.det([[2, 7], [1, 1]]), -5), '05 크라메르')
X = np.array([[1, 1], [1, 2], [1, 3.]]); y = np.array([2, 3, 5.]); beta = np.linalg.solve(X.T @ X, X.T @ y)
ok(near(beta[0], 1 / 3) and near(beta[1], 1.5), '05 회귀'); ok(np.allclose(y - X @ beta, [1 / 6, -1 / 3, 1 / 6]), '05 잔차')
# 06
S = set(range(1, 7)); P = lambda E: Fr(len(E), 6)
ok(P({1, 2, 3} | {2, 4, 6}) == Fr(5, 6), '06 합사건'); ok(near(1 - (5 / 6) ** 2, 0.306), '06 적어도 한 번 6'); ok(Fr(4, 12) == Fr(1, 3), '06 킹')
# 07
bayes = lambda p, s, f: s * p / (s * p + f * (1 - p))
ok(near(bayes(.01, .99, .05), .1667), '07 의료'); ok(near(bayes(bayes(.01, .99, .05), .99, .05), .798), '07 두 번')
ok(near(bayes(.1, .8, .05), .64), '07 스팸'); ok(near(.15 / .45, 1 / 3) and near(4 / 7, .571), '07 예')
ok(near(5 / 8 * 4 / 7, .357), '07 둘 다 빨강')
# 08
d = [2, 4, 6, 8, 10]
ok(np.var(d) == 8 and np.var(d, ddof=1) == 10 and near(np.std(d), 2.828), '08 분산'); ok(np.mean([1, 2, 2, 3, 100]) == 21.6, '08 이상치 평균')
ok(near(np.std([68, 70, 72, 69, 71, 70]), 1.29, .01) and near(np.std([100, 40, 95, 45, 90, 50]), 25.3, .05), '08 그림 2')
# 09
ok(near(math.comb(5, 2) * .5 ** 5, .3125), '09 이항'); ok(near(math.exp(-3) * 9 / 2, .2240), '09 포아송')
ok(near(math.exp(-1.5), .2231), '09 지수'); ok(near(math.exp(-3) * 27 / 6, .224) and near(math.exp(-3) * 243 / 120, .1008), '09 그림 포아송')
ok(near(1 - sum(math.exp(-3) * 3 ** k / math.factorial(k) for k in range(5)), .1847), '09 5통 이상'); ok(near(1 - .99 ** 100, .634), '09 뽑기')
Phi = lambda z: .5 * (1 + math.erf(z / math.sqrt(2)))
ok(near(1 - Phi(1), .1587) and near(1 - Phi(2), .0228) and near(1 - Phi(3), .00135, 5e-5), '09 정규 꼬리')
# 10
x5, y5 = np.array([1, 2, 3, 4, 5.]), np.array([2, 4, 5, 4, 5.])
ok(near(np.cov(x5, y5, ddof=0)[0, 1], 1.2) and near(np.corrcoef(x5, y5)[0, 1], .7746), '10 공분산·상관'); ok(near(np.cov(x5, y5)[0, 1], 1.5), '10 ddof=1')
# 11
ok(near(((1.1) ** 2 - 1) / .1, 2.1) and near((2 ** 2 - 1) / 1, 3), '11 할선'); ok(near(2 * (math.pi / 2), math.pi), '11 AI 판단'); ok(near(8 / 3, 2.667), '11 적분')
# 12
fx = lambda x, y: 2 * x * y + 3 * y; fy = lambda x, y: x * x + 3 * x + 2 * y
ok((fx(1, 2), fy(1, 2)) == (10, 8) and near(math.hypot(10, 8), 12.8, .05), '12 그래디언트'); ok(near(1.1 ** 2 + 2.1 ** 2, 5.62) and near(2 * 1.1 + 4 * 2.1 - 5, 5.6), '12 접평면')
ok(np.allclose(np.array([1, 2.]) - .1 * np.array([2, 4.]), [.8, 1.6]), '12 한 걸음')
# 13
ok(near(4 * .8 ** 15, .1407) and near(4 * .98 ** 15, 2.954), '13 학습률 표')
# 14
ev = np.linalg.eigvalsh([[4, 1], [1, 3]]); ok(np.allclose(sorted(ev), [(7 - 5 ** .5) / 2, (7 + 5 ** .5) / 2]), '14 고윳값')
Xp = np.array([[0, 0], [1, 1], [0, -1], [-1, 0.]]); Sg = Xp.T @ Xp / 3; ok(np.allclose(np.linalg.eigvalsh(Sg), [1 / 3, 1]), '14 PCA 예'); ok(near(1 / (4 / 3), .75), '14 75%')
ok(np.allclose(Xp @ (np.array([1, 1]) / 2 ** .5), [0, 1.4142, -.7071, -.7071], atol=1e-4), '14 투영')
# 15
Xq = np.array([[2, 0], [0, 1], [1, 1.]]); Xc = Xq - Xq.mean(0); w = np.linalg.eigvalsh(Xc.T @ Xc / 2)[::-1]
ok(near(w[0], 1.268) and near(w[1], .066, 1e-3) and near(w[0] / w.sum(), .951), '15 PCA')
sm = np.exp([2, 1, 0]) / np.exp([2, 1, 0]).sum(); ok(np.allclose(sm, [.665, .245, .090], atol=1e-3), '15 소프트맥스')
ok(near(1 / (1 + math.exp(-2)), .881) and near(-math.log(.9), .105) and near(-math.log(.1), 2.303), '15 함수')
ok((2 * 1 + 3, 1 + 6) == (5, 7), '15 편미분 예')
# 실전 연습장
ok(near(bayes(.02, .9, .01), .647) and bayes(bayes(.02, .9, .01), .9, .01) >= .9 and bayes(bayes(.02, .99, .05), .99, .05) < .9, '연습장 검사실')
print(f'파이썬 검산 {n}개 통과')
js = r'''
global.U={$:()=>null,$$:()=>[],fmt:x=>x,cssv:()=>'#000',clamp:(v,a,b)=>Math.min(b,Math.max(a,v))};
const ML=require(process.argv[1]);const c=ML.calc,near=(a,b,t)=>Math.abs(a-b)<=(t||5e-4);let k=0;const ok=(x,m)=>{if(!x)throw new Error(m);k++;};
ok(c.dot([1,2,3],[4,5,6])===32,'dot');ok(near(c.angle([3,1],[1,3]),53.13,0.01),'angle');ok(JSON.stringify(c.matmul([[1,2,3],[4,5,6]],[[7,8],[9,10],[11,12]]))==='[[58,64],[139,154]]','matmul');
const s=c.solve2(2,3,7,1,-1,1);ok(s.x===2&&s.y===1,'solve');ok(c.solve2(1,1,2,2,2,4).type==='inf'&&c.solve2(1,1,2,1,1,3).type==='none','types');
ok(near(c.bayes(.01,.99,.05),.1667),'bayes');ok(c.varp([2,4,6,8,10])===8&&c.median([1,2,2,3,100])===2,'stats');ok(JSON.stringify(c.quart([1,2,4,6,8,10,12]))==='[2,6,10]','quart');
ok(near(c.binom(5,.5,2),.3125)&&near(c.poisson(3,2),.224),'dist');ok(near(1-c.ncdf(1),.1587,1e-3),'ncdf');ok(near(c.cov([1,2,3,4,5],[2,4,5,4,5]),1.2)&&near(c.corr([1,2,3,4,5],[2,4,5,4,5]),.7746),'corr');
const e=c.eig2(4,1,3);ok(near(e.l1,4.618)&&near(e.l2,2.382)&&near(e.v1[0],.8507),'eig');const g=c.gd(4,.1,15);ok(near(g[15],.1407),'gd');ok(ML.FORM.length===54,'form 54');
console.log('실험실 계산 모듈 검산 '+k+'개 통과');'''
p = subprocess.run(['node', '-e', js, os.path.join(R, 'build', 'mathlab.js')], capture_output=True, text=True)
print(p.stdout.strip() or p.stderr[-800:]); assert p.returncode == 0
