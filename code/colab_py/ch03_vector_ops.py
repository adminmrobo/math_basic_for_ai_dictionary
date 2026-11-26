# 03장 벡터 연산 — 더하기·내적·길이·각도 — 수리 도감 코랩 실습
# 코랩: https://colab.research.google.com/github/adminmrobo/math_basic_for_ai_dictionary/blob/main/colab/ch03_vector_ops.ipynb
# %% 1. 기본 연산
import numpy as np
import matplotlib.pyplot as plt

a = np.array([1, 2, 3]); b = np.array([4, 5, 6])
print("a + b =", a + b)
print("a - b =", a - b)
print("3 * a =", 3 * a)
print("내적 a·b =", np.dot(a, b))
print("노름 ||a|| =", round(np.linalg.norm(a), 3), "/ ||b|| =", round(np.linalg.norm(b), 3))

# %% 2. 내적을 손으로(반복문) 계산해 비교
s = 0
for x, y in zip(a, b):
    s += x * y          # 같은 자리끼리 곱해서 더하기
print("반복문 내적 =", s, "/ np.dot과 같은가?", s == np.dot(a, b))

# %% 3. 두 벡터 사이 각도
def angle_deg(u, v):
    cos = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
    return np.degrees(np.arccos(np.clip(cos, -1, 1))), cos

for u, v in [([1, 0], [0, 1]), ([1, 2, 3], [4, 5, 6]), ([1, 1], [-1, -1]), ([3, 4], [30, 40])]:
    deg, cos = angle_deg(np.array(u), np.array(v))
    print(f"{u} vs {v}: cos = {cos:.3f}, 각도 = {deg:.1f}도")

# %% 4. 화살표 그림
p, q = np.array([3, 1]), np.array([1, 3])
plt.figure(figsize=(5, 5))
plt.quiver([0, 0, 0], [0, 0, 0], [p[0], q[0], (p+q)[0]], [p[1], q[1], (p+q)[1]],
           color=["red", "blue", "green"], angles="xy", scale_units="xy", scale=1)
plt.quiver(p[0], p[1], q[0], q[1], color="blue", alpha=0.4, angles="xy", scale_units="xy", scale=1)
plt.xlim(0, 5); plt.ylim(0, 5); plt.gca().set_aspect("equal"); plt.grid(alpha=0.3)
plt.title("a (red) + b (blue) = a+b (green)"); plt.show()

# %% 5. 코사인 유사도로 영화 추천
user = np.array([5, 1, 3])                     # [액션, 로맨스, 코미디]
movies = {"Action Hero": np.array([9, 1, 4]), "Love Letter": np.array([1, 9, 2]), "Funny Day": np.array([2, 2, 9])}
def cos_sim(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
scores = {name: cos_sim(user, vec) for name, vec in movies.items()}
for name, s in sorted(scores.items(), key=lambda t: -t[1]):
    print(f"{name:12s} 코사인 유사도 = {s:.3f}")
print("추천:", max(scores, key=scores.get))
print("영화 벡터를 10배로 늘려도 같은가?", np.isclose(cos_sim(user, movies["Action Hero"] * 10), scores["Action Hero"]))
