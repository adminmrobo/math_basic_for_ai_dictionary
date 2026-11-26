# 07장 조건부 확률과 베이즈 — 새 정보로 고치는 믿음 — 수리 도감 코랩 실습
# 코랩: https://colab.research.google.com/github/adminmrobo/math_basic_for_ai_dictionary/blob/main/colab/ch07_bayes.ipynb
# %% 1. 베이즈 정리 함수
import numpy as np
import matplotlib.pyplot as plt

def bayes(prior, sens, fpr):
    """P(병|양성) = P(양성|병)P(병) / P(양성)"""
    evidence = sens * prior + fpr * (1 - prior)     # 전확률: 양성이 나오는 모든 길
    return sens * prior / evidence

p = bayes(0.01, 0.99, 0.05)
print(f"P(병|양성) = 0.0099 / (0.0099 + 0.0495) = {p:.4f}  (약 {p*100:.1f}%)")

# %% 2. 가상 인구로 확인
rng = np.random.default_rng(7)
for N in [1000, 1_000_000]:
    sick = rng.random(N) < 0.01
    positive = np.where(sick, rng.random(N) < 0.99, rng.random(N) < 0.05)
    tp, fp = np.sum(sick & positive), np.sum(~sick & positive)
    fn, tn = np.sum(sick & ~positive), np.sum(~sick & ~positive)
    print(f"N={N:>9,}: 진양성 {tp}, 거짓양성 {fp}, 거짓음성 {fn}, 진음성 {tn} -> 양성 중 환자 비율 {tp/(tp+fp):.3f}")

# %% 3. 유병률에 따라 달라지는 사후확률
priors = np.linspace(0.001, 0.5, 300)
plt.plot(priors * 100, [bayes(q, 0.99, 0.05) for q in priors])
plt.axvline(1, color="gray", ls=":"); plt.xlabel("prevalence (%)"); plt.ylabel("P(disease | positive)")
plt.title("Same test, different base rates"); plt.grid(alpha=0.3); plt.show()

# %% 4. 베이즈 갱신: 사후확률이 다음 사전확률
belief = 0.01
for k in range(1, 4):
    belief = bayes(belief, 0.99, 0.05)
    print(f"양성 {k}번 뒤: P(병) = {belief:.3f}")

# %% 5. 비복원 추출: 빨강 5, 파랑 3
bag = np.array(["R"] * 5 + ["B"] * 3)
first_red = second_red_too = 0
for _ in range(100000):
    draw = rng.choice(bag, size=2, replace=False)
    if draw[0] == "R":
        first_red += 1
        second_red_too += draw[1] == "R"
print(f"P(둘째 빨강 | 첫째 빨강) ≈ {second_red_too/first_red:.3f} (이론 4/7 = {4/7:.3f})")
