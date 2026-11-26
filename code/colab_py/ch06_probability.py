# 06장 확률 기초 — 사건·덧셈·곱셈 — 수리 도감 코랩 실습
# 코랩: https://colab.research.google.com/github/adminmrobo/math_basic_for_ai_dictionary/blob/main/colab/ch06_probability.ipynb
# %% 1. 집합으로 고전적 확률 계산
from fractions import Fraction
import numpy as np
import matplotlib.pyplot as plt

S = {1, 2, 3, 4, 5, 6}
A = {1, 2, 3}          # 4 미만
B = {2, 4, 6}          # 짝수
P = lambda E: Fraction(len(E), len(S))
print("P(A) =", P(A), "/ P(B) =", P(B), "/ P(A∩B) =", P(A & B))
print("P(A∪B) =", P(A | B), "= P(A)+P(B)-P(A∩B) =", P(A) + P(B) - P(A & B))
print("P(B의 여사건) =", 1 - P(B))

# %% 2. 많이 던질수록 이론값에 가까워진다
rng = np.random.default_rng(42)
for n in [10, 100, 1000, 100000]:
    rolls = rng.integers(1, 7, size=n)
    print(f"{n:>6}번 던짐: 짝수 비율 = {np.mean(rolls % 2 == 0):.4f}")
rolls = rng.integers(1, 7, size=5000)
running = np.cumsum(rolls % 2 == 0) / np.arange(1, 5001)
plt.plot(running); plt.axhline(0.5, color="red", ls="--")
plt.xscale("log"); plt.xlabel("number of rolls"); plt.ylabel("ratio of even"); plt.title("Law of large numbers"); plt.show()

# %% 3. 동전 두 번: 곱셈 법칙과 여사건
coins = rng.integers(0, 2, size=(100000, 2))      # 1 = 앞면
both = np.mean(coins.sum(axis=1) == 2)
atleast = np.mean(coins.sum(axis=1) >= 1)
print(f"두 번 다 앞면: {both:.3f} (이론 1/4 = 0.25)")
print(f"적어도 한 번 앞면: {atleast:.3f} (이론 1 - 1/4 = 0.75)")

# %% 4. 조건부 확률: 그림 카드 중 킹
ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
deck = [(r, s) for r in ranks for s in "SHDC"]
face = [c for c in deck if c[0] in "JQK"]
king_in_face = [c for c in face if c[0] == "K"]
print("카드", len(deck), "장 / 그림 카드", len(face), "장 / 그중 킹", len(king_in_face), "장")
print("P(킹 | 그림 카드) =", Fraction(len(king_in_face), len(face)))
