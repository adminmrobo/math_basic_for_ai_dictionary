# 04장 행렬 연산 — 곱셈·전치·역행렬 — 수리 도감 코랩 실습
# 코랩: https://colab.research.google.com/github/adminmrobo/math_basic_for_ai_dictionary/blob/main/colab/ch04_matrix_ops.ipynb
# %% 1. 행렬곱과 그 속의 내적
import numpy as np

A = np.array([[1, 2, 3], [4, 5, 6]])          # 2 x 3
B = np.array([[7, 8], [9, 10], [11, 12]])     # 3 x 2
C = A @ B                                      # 2 x 2
print("A @ B =\n", C)
for i in range(A.shape[0]):
    for j in range(B.shape[1]):
        parts = " + ".join(f"{A[i,k]}x{B[k,j]}" for k in range(A.shape[1]))
        print(f"C[{i+1}{j+1}] = {parts} = {C[i, j]}")

# %% 2. 순서를 바꾸면? (AB != BA)
print("B @ A 크기:", (B @ A).shape, "/ A @ B 크기:", C.shape)
print("B @ A =\n", B @ A)

# %% 3. 크기가 맞지 않으면 오류
try:
    A @ A
except ValueError as e:
    print("A @ A 오류:", str(e)[:60], "...")
    print("-> 앞 행렬의 열 수(3)와 뒤 행렬의 행 수(2)가 달라 곱할 수 없어요.")

# %% 4. 덧셈·뺄셈·전치
P = np.array([[3, 1, 0], [1, 2, 4]])
print("A + P =\n", A + P)
print("[[5,4],[3,2]] - [[1,1],[1,1]] =\n", np.array([[5, 4], [3, 2]]) - np.ones((2, 2), dtype=int))
print("A.T =\n", A.T, " shape", A.T.shape)

# %% 5. 역행렬: 공식으로 직접, 그리고 numpy로
M = np.array([[2, 1], [1, 2]])
a, b, c, d = M.ravel()
det = a * d - b * c
M_inv = (1 / det) * np.array([[d, -b], [-c, a]])
print("det =", det, "\n공식 역행렬 =\n", M_inv.round(4))
print("np.linalg.inv와 같은가?", np.allclose(M_inv, np.linalg.inv(M)))
print("M @ M_inv =\n", (M @ M_inv).round(10), "-> 단위행렬?", np.allclose(M @ M_inv, np.eye(2)))

# %% 6. 역행렬이 없는 행렬
S = np.array([[1, 2], [2, 4]])
print("det(S) =", round(np.linalg.det(S), 10))
try:
    np.linalg.inv(S)
except np.linalg.LinAlgError as e:
    print("역행렬 없음:", e, "-> 둘째 행이 첫째 행의 2배")

# %% 7. 신경망 한 층처럼: 데이터 5개 x 특성 3개 @ 가중치 3 x 2
rng = np.random.default_rng(0)
X = rng.normal(size=(5, 3)); W = rng.normal(size=(3, 2))
print("X", X.shape, "@ W", W.shape, "=", (X @ W).shape)
print("단위행렬 곱: A @ I3 == A ?", np.array_equal(A @ np.eye(3, dtype=int), A))
