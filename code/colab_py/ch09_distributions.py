# 09장 확률분포 — 이항·포아송·정규 — 수리 도감 코랩 실습
# 코랩: https://colab.research.google.com/github/adminmrobo/math_basic_for_ai_dictionary/blob/main/colab/ch09_distributions.ipynb
# %% 1. 다섯 가지 확률: 공식 vs scipy
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

binom_formula = math.comb(5, 2) * 0.5**2 * 0.5**3
pois_formula = math.exp(-3) * 3**2 / math.factorial(2)
print(f"이항 P(X=2)      : 공식 {binom_formula:.4f} / scipy {stats.binom.pmf(2, 5, 0.5):.4f}")
print(f"포아송 P(X=2)    : 공식 {pois_formula:.4f} / scipy {stats.poisson.pmf(2, 3):.4f}")
print(f"균등 P(2<=X<=8)  : 공식 {(8-2)/(10-0):.4f} / scipy {stats.uniform(0, 10).cdf(8) - stats.uniform(0, 10).cdf(2):.4f}")
print(f"지수 P(X>3)      : 공식 {math.exp(-0.5*3):.4f} / scipy {stats.expon(scale=1/0.5).sf(3):.4f}  (scale = 1/λ)")
print(f"정규 P(X>180)    : scipy {stats.norm(170, 10).sf(180):.4f}  (z = 1)")
print(f"베르누이 P(X=1)  : {stats.bernoulli(0.6).pmf(1):.1f}")

# %% 2. 여섯 분포의 모양
fig, ax = plt.subplots(2, 3, figsize=(12, 6))
ax[0, 0].bar([0, 1], stats.bernoulli(0.6).pmf([0, 1]), color=["pink", "skyblue"]); ax[0, 0].set_title("Bernoulli p=0.6")
k = np.arange(0, 6); ax[0, 1].bar(k, stats.binom.pmf(k, 5, 0.5)); ax[0, 1].set_title("Binomial n=5, p=0.5")
k = np.arange(0, 11); ax[0, 2].bar(k, stats.poisson.pmf(k, 3), color="pink"); ax[0, 2].set_title("Poisson lambda=3")
x = np.linspace(130, 210, 300); ax[1, 0].plot(x, stats.norm(170, 10).pdf(x)); ax[1, 0].set_title("Normal mu=170, sigma=10")
x = np.linspace(-2, 12, 300); ax[1, 1].plot(x, stats.uniform(0, 10).pdf(x)); ax[1, 1].set_title("Uniform U(0,10)")
x = np.linspace(0, 10, 300); ax[1, 2].plot(x, stats.expon(scale=2).pdf(x), "r"); ax[1, 2].set_title("Exponential lambda=0.5")
plt.tight_layout(); plt.show()

# %% 3. 68-95-99.7 규칙
for s in [1, 2, 3]:
    print(f"평균 ± {s}σ 안: {stats.norm.cdf(s) - stats.norm.cdf(-s):.4f}")
print(f"키 200cm 초과(z=3): {stats.norm(170, 10).sf(200):.4f}")

# %% 4. 시뮬레이션 vs 이론 (이항 n=5, p=0.5)
rng = np.random.default_rng(3)
samples = rng.binomial(5, 0.5, size=100000)
print(" k | 실제 비율 | 이론 확률")
for kk in range(6):
    print(f" {kk} |  {np.mean(samples == kk):.4f}   |  {stats.binom.pmf(kk, 5, 0.5):.4f}")
