# 14장 고윳값·고유벡터와 PCA — 데이터의 주축 찾기 — 수리 도감 코랩 실습
# 코랩: https://colab.research.google.com/github/adminmrobo/math_basic_for_ai_dictionary/blob/main/colab/ch14_eigen_pca.ipynb
# %% 1. 고윳값: 근의 공식 vs numpy, 그리고 검산
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.datasets import load_digits

A = np.array([[4, 1], [1, 3]], dtype=float)
lam = [(7 + np.sqrt(5)) / 2, (7 - np.sqrt(5)) / 2]
print("근의 공식 λ =", np.round(lam, 4))
vals, vecs = np.linalg.eig(A)
vals, vecs = np.real(vals), np.real(vecs)      # 버전에 따라 복소수 꼴로 나올 수 있어 실수부만 (대칭 행렬이라 실제로 실수)
print("np.linalg.eig λ =", np.round(vals, 4))
for i in range(2):
    v = vecs[:, i]
    print(f"λ={vals[i]:.4f}, v={v.round(4)}: A@v = {(A @ v).round(4)}, λv = {(vals[i] * v).round(4)}")
print("합", round(vals.sum(), 4), "= 대각합", np.trace(A), "/ 곱", round(vals.prod(), 4), "= 행렬식", round(np.linalg.det(A), 4))

# %% 2. 원을 타원으로: 고유벡터는 방향이 그대로
t = np.linspace(0, 2 * np.pi, 100); circle = np.vstack([np.cos(t), np.sin(t)])
ellipse = A @ circle
plt.figure(figsize=(5.5, 5.5)); plt.plot(*circle, "gray", label="unit circle"); plt.plot(*ellipse, "b", label="A @ circle")
for i, c in enumerate(["red", "orange"]):
    v = vecs[:, i] * vals[i]; plt.arrow(0, 0, v[0], v[1], color=c, width=0.05, length_includes_head=True)
plt.gca().set_aspect("equal"); plt.legend(); plt.title("Eigenvectors keep their direction"); plt.grid(alpha=0.3); plt.show()

# %% 3. PCA 여섯 단계를 손으로
X = np.array([[0, 0], [1, 1], [0, -1], [-1, 0]], dtype=float)
Xc = X - X.mean(axis=0)                                   # 1) 중심화 (여기서는 이미 평균 0)
S = Xc.T @ Xc / (len(X) - 1)                              # 2) 공분산 행렬
w, V = np.linalg.eigh(S)                                  # 3) 고윳값·고유벡터 (대칭 행렬용)
order = np.argsort(w)[::-1]; w, V = w[order], V[:, order] # 4) 내림차순
W = V[:, :1]                                              # 5) 상위 1개
Z = Xc @ W                                                # 6) 투영
print("공분산 행렬 =\n", S.round(4))
print("고윳값 =", w.round(4), "/ PC1 =", W.ravel().round(4), "/ 설명 비율 =", round(w[0] / w.sum(), 4))
print("투영 Z =", Z.ravel().round(4))
sk = PCA(n_components=1).fit(X)
print("sklearn 설명 비율 =", sk.explained_variance_ratio_.round(4), "/ 투영 =", sk.transform(X).ravel().round(4), "(부호는 반대일 수 있음)")

# %% 4. 비스듬한 점 구름과 주성분
rng = np.random.default_rng(5)
P = rng.multivariate_normal([0, 0], [[3, 2], [2, 2]], size=200)
pca = PCA(2).fit(P)
plt.figure(figsize=(6, 6)); plt.scatter(P[:, 0], P[:, 1], s=10, alpha=0.5, label="data")
for comp, var, c in zip(pca.components_, pca.explained_variance_, ["red", "orange"]):
    plt.arrow(0, 0, *(comp * 2 * np.sqrt(var)), color=c, width=0.06, length_includes_head=True)
proj = (P @ pca.components_[0])[:, None] * pca.components_[0]
plt.scatter(proj[:, 0], proj[:, 1], s=8, color="green", label="projected on PC1")
plt.gca().set_aspect("equal"); plt.legend(); plt.title(f"PC1 explains {pca.explained_variance_ratio_[0]:.0%}"); plt.show()

# %% 5. 손글씨 숫자 64차원 -> 2차원
digits = load_digits()
p2 = PCA(2).fit(digits.data); Z2 = p2.transform(digits.data)
print("손글씨 64차원: 상위 2개 설명 비율 =", round(p2.explained_variance_ratio_.sum(), 3),
      "/ 상위 10개 =", round(PCA(10).fit(digits.data).explained_variance_ratio_.sum(), 3))
plt.figure(figsize=(6.5, 5)); sc = plt.scatter(Z2[:, 0], Z2[:, 1], c=digits.target, cmap="tab10", s=8)
plt.colorbar(sc, label="digit"); plt.xlabel("PC1"); plt.ylabel("PC2"); plt.title("Digits (64-D) projected to 2-D"); plt.show()
