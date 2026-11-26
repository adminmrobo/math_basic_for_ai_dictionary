# 11장 미적분 기초 — 극한·미분·적분 — 수리 도감 코랩 실습
# 코랩: https://colab.research.google.com/github/adminmrobo/math_basic_for_ai_dictionary/blob/main/colab/ch11_calculus.ipynb
# %% 1. 할선 기울기 -> 미분 (극한)
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

f = lambda x: x ** 2
print("    h     | 할선 기울기 [f(1+h)-f(1)]/h")
for h in [1, 0.1, 0.01, 0.001, 0.0001]:
    print(f"{h:>9} | {(f(1 + h) - f(1)) / h:.6f}")

# %% 2. sympy로 기호 미분
x = sp.symbols("x")
exprs = [x**3, sp.sin(x), sp.exp(x), sp.log(x), x**2 * sp.sin(x), (3*x + 1)**5, (x**2 + 1) / (x - 1)]
for e in exprs:
    d = sp.simplify(sp.diff(e, x))
    print(f"({e})' = {sp.factor(d) if e == (x**2 + 1) / (x - 1) else d}")

# %% 3. 수치 미분으로 검산 (gradient check)
def numeric_derivative(fn, x0, h=1e-5):
    return (fn(x0 + h) - fn(x0 - h)) / (2 * h)     # 가운데 차분: 더 정확
g = lambda t: t ** 2 * np.sin(t)
x0 = np.pi / 2
exact = float(sp.diff(x**2 * sp.sin(x), x).subs(x, sp.pi / 2))
print(f"x = pi/2: 기호 미분 {exact:.6f} / 수치 미분 {numeric_derivative(g, x0):.6f}")
print("주판봇의 답 2x*cos(x) =", round(2 * x0 * np.cos(x0), 6), "-> 틀림")

# %% 4. 할선과 접선 그림
xs = np.linspace(-0.5, 2.5, 200)
plt.plot(xs, f(xs), label="f(x) = x^2")
for h, c in [(1, "orange"), (0.5, "gold")]:
    s = (f(1 + h) - f(1)) / h
    plt.plot(xs, f(1) + s * (xs - 1), "--", color=c, label=f"secant h={h} (slope {s:.2f})")
plt.plot(xs, f(1) + 2 * (xs - 1), "r", label="tangent (slope 2)")
plt.scatter([1], [1], color="red", zorder=3); plt.ylim(-1, 6); plt.legend(); plt.grid(alpha=0.3); plt.show()

# %% 5. 적분: 기호 vs 리만 합
print("∫x^2 dx =", sp.integrate(x**2, x), "+ C")
print("∫_0^1 x dx =", sp.integrate(x, (x, 0, 1)))
n = 1000; dx = 1 / n; mids = (np.arange(n) + 0.5) * dx
print(f"리만 합(사각형 {n}개) = {np.sum(mids * dx):.6f}")
