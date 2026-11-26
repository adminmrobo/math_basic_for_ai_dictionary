# 05장 연립일차방정식 — Ax = b와 선형 회귀 — 수리 도감 코랩 실습
# 코랩: https://colab.research.google.com/github/adminmrobo/math_basic_for_ai_dictionary/blob/main/colab/ch05_linear_systems.ipynb
# %% 1. Ax = b를 세 가지로 풀기
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

A = np.array([[2, 3], [1, -1]], dtype=float); b = np.array([7, 1], dtype=float)
print("(a) A^-1 b      =", np.linalg.inv(A) @ b)
print("(b) solve(A, b) =", np.linalg.solve(A, b))
detA = np.linalg.det(A)
Ax = A.copy(); Ax[:, 0] = b          # x 열을 b로
Ay = A.copy(); Ay[:, 1] = b          # y 열을 b로
print(f"(c) 크라메르: det A = {detA:.0f}, x = {np.linalg.det(Ax):.0f}/{detA:.0f} = {np.linalg.det(Ax)/detA:.0f}, y = {np.linalg.det(Ay)/detA:.0f}")

# %% 2. 해의 종류 판정
def kind(a1, b1, c1, a2, b2, c2):
    D = a1 * b2 - b1 * a2
    if abs(D) > 1e-12:
        return f"해가 하나 (det = {D})"
    same = abs(a1 * c2 - a2 * c1) < 1e-12 and abs(b1 * c2 - b2 * c1) < 1e-12
    return "해가 무수히 많음 (det = 0, 겹침)" if same else "해가 없음 (det = 0, 평행)"

cases = {"unique": (2, 3, 7, 1, -1, 1), "infinite": (1, 1, 2, 2, 2, 4), "none": (1, 1, 2, 1, 1, 3)}
for name, c in cases.items():
    print(f"{name:9s} {c} -> {kind(*c)}")

# %% 3. 세 경우를 그림으로
xs = np.linspace(-1, 4, 50)
fig, axes = plt.subplots(1, 3, figsize=(12, 3.6))
for ax, (name, (a1, b1, c1, a2, b2, c2)) in zip(axes, cases.items()):
    ax.plot(xs, (c1 - a1 * xs) / b1, "r", lw=2, label="eq 1")
    ax.plot(xs, (c2 - a2 * xs) / b2, "b--", lw=2, label="eq 2")
    ax.set_title(name); ax.set_ylim(-3, 5); ax.grid(alpha=0.3); ax.legend()
plt.tight_layout(); plt.show()

# %% 4. 정규방정식으로 선형 회귀
x = np.array([1, 2, 3], dtype=float); y = np.array([2, 3, 5], dtype=float)
X = np.column_stack([np.ones_like(x), x])        # 설계 행렬: [1, x]
XtX, Xty = X.T @ X, X.T @ y
print("X^T X =\n", XtX, "\nX^T y =", Xty)
beta = np.linalg.inv(XtX) @ Xty
print(f"정규방정식: beta0 = {beta[0]:.3f}, beta1 = {beta[1]:.3f}")
lr = LinearRegression().fit(x.reshape(-1, 1), y)
print(f"sklearn   : beta0 = {lr.intercept_:.3f}, beta1 = {lr.coef_[0]:.3f}")
print("각 점의 오차(정답 - 예측):", (y - X @ beta).round(3))
plt.scatter(x, y, s=60, label="data"); plt.plot(xs, beta[0] + beta[1] * xs, "g", label="y = 0.333 + 1.5x")
plt.legend(); plt.grid(alpha=0.3); plt.title("Least squares line"); plt.show()
