# 01장 수학 기초 — 변수·식·함수 — 수리 도감 코랩 실습
# 코랩: https://colab.research.google.com/github/adminmrobo/math_basic_for_ai_dictionary/blob/main/colab/ch01_math_basics.ipynb
# %% 1. 함수 f(x) = 2x + 3과 값 표
import numpy as np
import matplotlib.pyplot as plt

def f(x):
    """입력 x를 두 배 하고 3을 더해 내보내는 함수"""
    return 2 * x + 3

print("x  | f(x) = 2x + 3")
for x in [-2, -1, 0, 1, 2]:
    print(f"{x:>2} | {f(x):>3}")

# %% 2. ML에서 흔한 함수 네 종류 그리기
xs = np.linspace(-3, 3, 200)
funcs = {
    "Linear: 2x + 3": 2 * xs + 3,
    "Quadratic: x^2": xs ** 2,
    "Polynomial: 0.1x^3 - x": 0.1 * xs ** 3 - xs,
    "Non-linear: sin(x), e^x": None,
}
fig, axes = plt.subplots(2, 2, figsize=(9, 6))
for ax, (name, ys) in zip(axes.ravel(), funcs.items()):
    if ys is None:
        ax.plot(xs, np.sin(xs), label="sin(x)")
        ax.plot(xs, np.exp(xs) / 5, label="e^x / 5")
        ax.legend()
    else:
        ax.plot(xs, ys)
    ax.axhline(0, color="gray", lw=0.8); ax.axvline(0, color="gray", lw=0.8)
    ax.set_title(name)
plt.tight_layout(); plt.show()

# %% 3. 정의역 검사: sqrt(x)는 x >= 0에서만
def safe_sqrt(x):
    if x < 0:
        return f"{x}은(는) 정의역 밖 (x >= 0 이어야 함)"
    return np.sqrt(x)

for x in [0, 4, 9, -4]:
    print("sqrt(", x, ") ->", safe_sqrt(x))
with np.errstate(invalid="ignore"):
    print("numpy.sqrt(-4) 그대로 계산하면:", np.sqrt(-4.0))   # nan = 숫자가 아님

# %% 4. 방정식 2x + 3 = 11 풀고 확인하기
x_sol = (11 - 3) / 2
print("해 x =", x_sol, "/ 대입 확인 2x+3 =", f(x_sol), "->", f(x_sol) == 11)

# %% 5. 상수 pi와 e
print("pi =", round(np.pi, 4), "/ e =", round(np.e, 3))
for r in [1, 2]:
    print(f"반지름 {r}인 원의 둘레 2*pi*r = {2 * np.pi * r:.3f}")
print("배운 점: 1) 함수는 입력 하나에 출력 하나  2) 정의역 밖 입력은 nan  3) 상수는 그대로, 변수만 바뀐다")
