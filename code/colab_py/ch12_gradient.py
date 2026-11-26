# 12장 편미분과 그래디언트 — 여러 방향의 기울기 — 수리 도감 코랩 실습
# 코랩: https://colab.research.google.com/github/adminmrobo/math_basic_for_ai_dictionary/blob/main/colab/ch12_gradient.ipynb
# %% 1. 편미분과 그래디언트 (sympy)
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

x, y = sp.symbols("x y")
f = x**2 * y + 3 * x * y + y**2
fx, fy = sp.diff(f, x), sp.diff(f, y)
print("∂f/∂x =", fx, "/ ∂f/∂y =", fy)
print("∇f(1, 2) =", (fx.subs({x: 1, y: 2}), fy.subs({x: 1, y: 2})))

# %% 2. 2계·혼합 편미분
g = x**2 * y + y**3
gxx, gyy = sp.diff(g, x, x), sp.diff(g, y, y)
gxy, gyx = sp.diff(g, x, y), sp.diff(g, y, x)
print("fxx =", gxx, "/ fyy =", gyy, "/ fxy =", gxy, "/ fyx =", gyx, "/ 같은가?", sp.simplify(gxy - gyx) == 0)

# %% 3. 수치 편미분으로 검산
def F(p):
    a, b = p
    return a**2 * b + 3 * a * b + b**2
def num_grad(fn, p, h=1e-5):
    p = np.array(p, dtype=float); grad = np.zeros_like(p)
    for i in range(len(p)):
        e = np.zeros_like(p); e[i] = h
        grad[i] = (fn(p + e) - fn(p - e)) / (2 * h)
    return grad
print("수치 그래디언트 (1, 2):", num_grad(F, [1, 2]).round(6))

# %% 4. 등고선과 그래디언트 화살표
X, Y = np.meshgrid(np.linspace(-3, 3, 200), np.linspace(-3, 3, 200))
plt.figure(figsize=(5.5, 5)); plt.contour(X, Y, X**2 + Y**2, levels=10, cmap="viridis")
P, Q = np.meshgrid(np.linspace(-2.5, 2.5, 7), np.linspace(-2.5, 2.5, 7))
plt.quiver(P, Q, 2 * P, 2 * Q, color="red")                     # ∇f = (2x, 2y)
plt.gca().set_aspect("equal"); plt.title("Gradient arrows are perpendicular to contours"); plt.show()

# %% 5. 접평면과 선형 근사
h2 = lambda a, b: a**2 + b**2
plane = lambda a, b: 2 * a + 4 * b - 5                          # (1, 2)에서의 접평면
print(f"(1.1, 2.1): 실제 {h2(1.1, 2.1):.4f} / 접평면 {plane(1.1, 2.1):.4f}")
print(f"(2.0, 3.0): 실제 {h2(2, 3):.4f} / 접평면 {plane(2, 3):.4f}  <- 멀어지면 어긋남")

# %% 6. 경사하강 다섯 걸음
p = np.array([1.0, 2.0]); alpha = 0.1
print("걸음 |     점        | f = x^2 + y^2")
for t in range(6):
    print(f"{t:>3}  | ({p[0]:.4f}, {p[1]:.4f}) | {h2(*p):.4f}")
    p = p - alpha * np.array([2 * p[0], 2 * p[1]])              # 그래디언트 반대로
