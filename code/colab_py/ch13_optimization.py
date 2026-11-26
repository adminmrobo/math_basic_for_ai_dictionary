# 13장 최적화 — 경사하강과 학습률 — 수리 도감 코랩 실습
# 코랩: https://colab.research.google.com/github/adminmrobo/math_basic_for_ai_dictionary/blob/main/colab/ch13_optimization.ipynb
# %% 1. 학습률에 따른 경사하강 (f = θ^2)
import numpy as np
import matplotlib.pyplot as plt

def gd_path(theta, alpha, steps):
    path = [theta]
    for _ in range(steps):
        theta = theta - alpha * 2 * theta       # ∇f = 2θ
        path.append(theta)
    return np.array(path)

for a in [0.01, 0.1, 0.7, 1.0, 1.1]:
    p = gd_path(4.0, a, 20); r = 1 - 2 * a
    kind = "발산" if abs(r) > 1 else "제자리 왕복" if abs(r) == 1 else ("지그재그 수렴" if r < 0 else "수렴")
    print(f"α={a:<5} 공비 {r:+.2f} -> 20걸음 뒤 θ = {p[-1]:+.4g} ({kind})")
    plt.plot(p ** 2 + 1e-12, label=f"alpha={a}")
plt.yscale("log"); plt.xlabel("step"); plt.ylabel("loss"); plt.legend(); plt.title("Learning rate matters"); plt.show()

# %% 2. 선형 회귀를 경사하강으로 (5장과 같은 데이터)
x = np.array([1, 2, 3.0]); y = np.array([2, 3, 5.0])
def grads(w, b):
    err = y - (w * x + b)
    return -2 * np.mean(x * err), -2 * np.mean(err), np.mean(err ** 2)
w = b = 0.0
for t in range(5000):
    gw, gb, J = grads(w, b)
    w, b = w - 0.05 * gw, b - 0.05 * gb
    if t in (0, 10, 100, 1000, 4999):
        print(f"걸음 {t:>4}: w = {w:.4f}, b = {b:.4f}, MSE = {J:.5f}")
X = np.column_stack([np.ones_like(x), x])
print("정규방정식 답:", np.linalg.solve(X.T @ X, X.T @ y).round(4), "(b, w)")

# %% 3. 배치 vs SGD vs 미니배치
rng = np.random.default_rng(0)
xd = rng.uniform(0, 2, 1000); yd = 3 * xd + 2 + rng.normal(0, 0.5, 1000)
def train(batch, epochs=20, lr=0.05):
    w = b = 0.0; hist = []
    for _ in range(epochs):
        idx = rng.permutation(len(xd))
        for s in range(0, len(xd), batch):
            j = idx[s:s + batch]; err = yd[j] - (w * xd[j] + b)
            w += lr * 2 * np.mean(xd[j] * err); b += lr * 2 * np.mean(err)
        hist.append(np.mean((yd - (w * xd + b)) ** 2))
    return w, b, hist
for name, bs in [("batch", 1000), ("SGD", 1), ("mini-batch 32", 32)]:
    w_, b_, h = train(bs)
    print(f"{name:14s}: w = {w_:.3f}, b = {b_:.3f}, 마지막 MSE = {h[-1]:.4f}")
    plt.plot(h, label=name)
plt.xlabel("epoch"); plt.ylabel("MSE"); plt.legend(); plt.title("Batch vs SGD vs mini-batch"); plt.show()

# %% 4. 좁고 긴 그릇에서 GD vs 모멘텀 vs Adam
f = lambda p: p[0] ** 2 + 10 * p[1] ** 2
g = lambda p: np.array([2 * p[0], 20 * p[1]])
def run(method, lr, steps=300):
    p = np.array([5.0, 1.0]); v = np.zeros(2); m = np.zeros(2); s = np.zeros(2)
    for t in range(1, steps + 1):
        gr = g(p)
        if method == "GD":
            p = p - lr * gr
        elif method == "Momentum":
            v = 0.9 * v + gr; p = p - lr * v
        else:  # Adam
            m = 0.9 * m + 0.1 * gr; s = 0.999 * s + 0.001 * gr ** 2
            mh, sh = m / (1 - 0.9 ** t), s / (1 - 0.999 ** t)
            p = p - lr * mh / (np.sqrt(sh) + 1e-8)
        if f(p) < 1e-6:
            return t
    return steps
for meth, lr in [("GD", 0.01), ("Momentum", 0.01), ("Adam", 0.1)]:
    print(f"{meth:8s} (lr={lr}): 손실 < 0.000001 까지 {run(meth, lr, 3000)}걸음")
print("GD를 lr=0.09로 잘 맞추면:", run("GD", 0.09), "걸음 -> 학습률을 잘 고르면 기본 GD도 빠르다.")
print("개선판의 장점: 학습률을 덜 까다롭게 골라도 잘 움직인다(같은 lr=0.01에서 모멘텀이 약 3배 빠름).")
