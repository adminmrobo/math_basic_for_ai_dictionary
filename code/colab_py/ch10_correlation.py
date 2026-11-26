# 10장 상관과 공분산 — 함께 움직이는 정도 — 수리 도감 코랩 실습
# 코랩: https://colab.research.google.com/github/adminmrobo/math_basic_for_ai_dictionary/blob/main/colab/ch10_correlation.ipynb
# %% 1. 공분산과 상관계수: 직접 vs numpy
import numpy as np
import matplotlib.pyplot as plt

X = np.array([1, 2, 3, 4, 5], dtype=float); Y = np.array([2, 4, 5, 4, 5], dtype=float)
mx, my = X.mean(), Y.mean()
cov = sum((x - mx) * (y - my) for x, y in zip(X, Y)) / len(X)
sx = np.sqrt(sum((x - mx) ** 2 for x in X) / len(X)); sy = np.sqrt(sum((y - my) ** 2 for y in Y) / len(Y))
r = cov / (sx * sy)
print(f"평균 x={mx}, y={my} / 공분산 = {cov} / σx = {sx:.3f}, σy = {sy:.3f} / r = {r:.4f}")
print("np.cov(ddof=0) =", np.cov(X, Y, ddof=0)[0, 1], "/ np.cov 기본(ddof=1) =", np.cov(X, Y)[0, 1], "(n-1로 나눔)")
print("np.corrcoef =", round(np.corrcoef(X, Y)[0, 1], 4))

# %% 2. 단위를 바꾸면?
print("배율 |   공분산 | 상관계수")
for k in [1, 10, 1000]:
    print(f"{k:>4} | {np.cov(X, Y * k, ddof=0)[0, 1]:>8.1f} | {np.corrcoef(X, Y * k)[0, 1]:.4f}")

# %% 3. 여러 상관의 산점도
rng = np.random.default_rng(0)
fig, axes = plt.subplots(2, 2, figsize=(8, 7))
for ax, target in zip(axes.ravel(), [0.95, -0.9, 0.0, 0.4]):
    a, b = rng.normal(size=100), rng.normal(size=100)
    x, y = a, target * a + np.sqrt(1 - target ** 2) * b
    ax.scatter(x, y, s=12); ax.set_title(f"r = {np.corrcoef(x, y)[0, 1]:.2f}")
plt.tight_layout(); plt.show()

# %% 4. 곡선 관계는 r = 0일 수 있다
xs = np.linspace(-3, 3, 61); ys = xs ** 2
print("y = x^2 의 상관계수 =", round(np.corrcoef(xs, ys)[0, 1], 6))
plt.scatter(xs, ys, s=10); plt.title("y = x^2 : strong relation, r = 0"); plt.show()

# %% 5. 튀는 점 하나의 힘
x5, y5 = np.append(X, 6), np.append(Y, 0)
print(f"점 (6, 0) 하나를 넣으면 r: {np.corrcoef(X, Y)[0, 1]:.3f} -> {np.corrcoef(x5, y5)[0, 1]:.3f}")
