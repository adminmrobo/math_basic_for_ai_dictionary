# 15장 총정리 — 공식 도감과 실전 예제 — 수리 도감 코랩 실습
# 코랩: https://colab.research.google.com/github/adminmrobo/math_basic_for_ai_dictionary/blob/main/colab/ch15_quick_revision.ipynb
# %% 1. 공식을 함수로, 도감 예시로 검산
import numpy as np
import matplotlib.pyplot as plt

dot = lambda a, b: sum(x * y for x, y in zip(a, b))
norm = lambda v: dot(v, v) ** 0.5
det2 = lambda M: M[0][0] * M[1][1] - M[0][1] * M[1][0]
mean = lambda xs: sum(xs) / len(xs)
var_s = lambda xs: sum((x - mean(xs)) ** 2 for x in xs) / (len(xs) - 1)      # 표본분산
cov = lambda xs, ys: sum((x - mean(xs)) * (y - mean(ys)) for x, y in zip(xs, ys)) / len(xs)
corr = lambda xs, ys: cov(xs, ys) / ((cov(xs, xs) ** 0.5) * (cov(ys, ys) ** 0.5))
bayes = lambda p, sens, fpr: sens * p / (sens * p + fpr * (1 - p))

assert dot([1, 2, 3], [4, 5, 6]) == 32
assert norm([3, 4]) == 5
assert (np.array([[1, 2, 3], [4, 5, 6]]) @ np.array([[7, 8], [9, 10], [11, 12]])).tolist() == [[58, 64], [139, 154]]
assert det2([[2, 1], [1, 2]]) == 3
assert mean([2, 4, 6, 8, 10]) == 6 and var_s([2, 4, 6, 8, 10]) == 10
X, Y = [1, 2, 3, 4, 5], [2, 4, 5, 4, 5]
assert round(cov(X, Y), 3) == 1.2 and round(corr(X, Y), 3) == 0.775
assert round(bayes(0.01, 0.99, 0.05), 3) == 0.167
print("공식 검산 9개 모두 통과")

# %% 2. 활성화 함수와 소프트맥스
sigmoid = lambda x: 1 / (1 + np.exp(-x))
relu = lambda x: np.maximum(0, x)
def softmax(z):
    z = np.asarray(z, dtype=float); e = np.exp(z - z.max())     # 최댓값을 빼서 overflow 방지
    return e / e.sum()
xs = np.linspace(-5, 5, 200)
fig, ax = plt.subplots(1, 3, figsize=(12, 3.2))
for a, (name, ys) in zip(ax, [("Sigmoid", sigmoid(xs)), ("Tanh", np.tanh(xs)), ("ReLU", relu(xs))]):
    a.plot(xs, ys); a.axhline(0, color="gray", lw=0.6); a.set_title(name); a.grid(alpha=0.3)
plt.tight_layout(); plt.show()
print("σ(0) =", sigmoid(0), "/ σ(2) =", round(sigmoid(2), 3), "/ ReLU(-3), ReLU(2) =", relu(-3), relu(2))
s = softmax([2, 1, 0]); print("softmax([2,1,0]) =", s.round(3), "합 =", round(s.sum(), 6))
print("softmax([1000, 1001]) =", softmax([1000, 1001]).round(3), "(큰 수도 안전)")

# %% 3. 손실 함수
mse = lambda y, yh: np.mean((np.asarray(y) - np.asarray(yh)) ** 2)
def bce(y, yh, eps=1e-12):
    y, yh = np.asarray(y, float), np.clip(np.asarray(yh, float), eps, 1 - eps)
    return -np.mean(y * np.log(yh) + (1 - y) * np.log(1 - yh))
print("MSE([2,3,5], [1.833,3.333,4.833]) =", round(mse([2, 3, 5], [1.833, 3.333, 4.833]), 4))
print("정답 1, 예측 0.9 -> 교차 엔트로피", round(bce([1], [0.9]), 3), "/ 예측 0.1 ->", round(bce([1], [0.1]), 3))

# %% 4. 실전 예제 세 개
p = np.array([1.0, 2.0]); p_new = p - 0.1 * 2 * p
print("(a) 경사하강 한 걸음:", p, "->", p_new)
vals, vecs = np.linalg.eigh(np.array([[2, 1], [1, 2]], dtype=float))
print("(b) 고윳값:", vals[::-1], "/ 고유벡터(열):\n", vecs[:, ::-1].round(4))
Xp = np.array([[2, 0], [0, 1], [1, 1]], dtype=float); Xc = Xp - Xp.mean(axis=0)
S = Xc.T @ Xc / (len(Xp) - 1); w, V = np.linalg.eigh(S); w = w[::-1]
print("(c) 평균", Xp.mean(axis=0).round(3), "/ 공분산\n", S.round(3), "\n    고윳값", w.round(3), "/ PC1 설명 비율", round(w[0] / w.sum(), 3))

# %% 5. 공식 카드 복습 퀴즈 (코랩에서 Enter로 넘기기)
cards = {"내적": "a·b = Σ aᵢbᵢ", "베이즈": "P(A|B) = P(B|A)P(A)/P(B)", "표본분산": "s² = Σ(xᵢ−x̄)²/(n−1)",
         "상관계수": "r = Cov/(σxσy)", "경사하강": "θ ← θ − α∇f(θ)", "고윳값": "det(A − λI) = 0", "시그모이드": "1/(1+e⁻ˣ)"}
def quiz(n=3, interactive=False, seed=0):
    rng = np.random.default_rng(seed)
    for name in rng.choice(list(cards), size=n, replace=False):
        if interactive:
            input(f"[{name}] 식을 떠올린 뒤 Enter > ")
        print(f"{name}: {cards[name]}")
quiz(3)   # 코랩에서는 quiz(5, interactive=True)로 바꿔 보세요
