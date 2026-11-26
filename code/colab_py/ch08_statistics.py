# 08장 통계 기초 — 평균·분산·사분위 — 수리 도감 코랩 실습
# 코랩: https://colab.research.google.com/github/adminmrobo/math_basic_for_ai_dictionary/blob/main/colab/ch08_statistics.ipynb
# %% 1. 가운데와 퍼짐: 손으로 vs numpy
import numpy as np
import matplotlib.pyplot as plt

x = [2, 4, 6, 8, 10]
n = len(x)
mean = sum(x) / n
var_pop = sum((v - mean) ** 2 for v in x) / n          # 모집단 분산 (n으로 나눔)
var_smp = sum((v - mean) ** 2 for v in x) / (n - 1)    # 표본 분산 (n-1로 나눔)
print("평균", mean, "/ 중앙값", np.median(x), "/ 범위", max(x) - min(x))
print("분산(n)", var_pop, "= np.var", np.var(x), "/ 표준편차", round(var_pop ** 0.5, 3))
print("분산(n-1)", var_smp, "= np.var(ddof=1)", np.var(x, ddof=1))

# %% 2. 이상치가 평균을 끌어당긴다
y = np.array([1, 2, 2, 3, 100])
print("평균", y.mean(), "/ 중앙값", np.median(y))
print("100을 빼면 평균", y[y < 100].mean(), "/ 중앙값", np.median(y[y < 100]))

# %% 3. 사분위수 (원자료 방식: 가운데 값을 빼고 반으로)
def quartiles(data):
    s = sorted(data); m = len(s); h = m // 2
    lower, upper = s[:h], s[h + 1:] if m % 2 else s[h:]
    return np.median(lower), np.median(s), np.median(upper)

z = [1, 2, 4, 6, 8, 10, 12]
q1, q2, q3 = quartiles(z)
print("원자료 방식 Q1, Q2, Q3 =", q1, q2, q3, "/ IQR =", q3 - q1)
print("numpy.percentile 25, 50, 75 =", np.percentile(z, [25, 50, 75]), "(계산 방식이 달라 값이 다를 수 있음)")

# %% 4. IQR 규칙으로 이상치 찾기 (여기서는 numpy.percentile 방식의 사분위수 사용)
def outliers(data):
    q1, q3 = np.percentile(data, [25, 75]); iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return [int(v) for v in data if v < lo or v > hi], (float(lo), float(hi))
found, (lo, hi) = outliers([1, 2, 2, 3, 100])
print("이상치:", found, f"/ 정상 범위 {lo} ~ {hi}")

# %% 5. 히스토그램과 상자 그림
rng = np.random.default_rng(1)
scores = rng.normal(70, 10, 200)
fig, ax = plt.subplots(1, 2, figsize=(10, 3.5))
ax[0].hist(scores, bins=15, color="teal", edgecolor="white"); ax[0].set_title("Histogram"); ax[0].set_xlabel("score")
ax[1].boxplot(scores); ax[1].set_title("Box plot")
plt.tight_layout(); plt.show()

# %% 6. 표준화: 단위가 다른 특성을 같은 크기로
h = np.array([160, 165, 170, 175, 180.0]); w = np.array([50, 58, 61, 70, 76.0])
zh, zw = (h - h.mean()) / h.std(), (w - w.mean()) / w.std()
print("키 z:", zh.round(2), "/ 평균", round(zh.mean(), 10), "표준편차", round(zh.std(), 3))
print("몸무게 z:", zw.round(2), "/ 평균", round(zw.mean(), 10), "표준편차", round(zw.std(), 3))
