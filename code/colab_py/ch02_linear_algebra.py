# 02장 선형대수 기초 — 스칼라·벡터·행렬 — 수리 도감 코랩 실습
# 코랩: https://colab.research.google.com/github/adminmrobo/math_basic_for_ai_dictionary/blob/main/colab/ch02_linear_algebra.ipynb
# %% 1. 스칼라·벡터·행렬 만들기
import numpy as np
import pandas as pd

a = 5                                   # 스칼라: 숫자 하나
v = np.array([1, 2, 3])                 # 벡터: 한 줄
A = np.array([[1, 2, 3],
              [4, 5, 6]])               # 행렬: 행 2개 x 열 3개
print("스칼라 a =", a, "/ ndim =", np.ndim(a))
print("벡터 v =", v, "/ shape =", v.shape)
print("행렬 A =\n", A, "\nshape =", A.shape, "(행, 열)")

# %% 2. 주소로 꺼내기: 수학의 A_23 = 파이썬의 A[1, 2] (0부터 센다)
print("A_23 (2행 3열) =", A[1, 2])
print("첫째 행 =", A[0], "/ 둘째 열 =", A[:, 1])

# %% 3. 행렬의 종류
kinds = {
    "행 행렬 (1x3)": np.array([[1, 2, 3]]),
    "열 행렬 (3x1)": np.array([[1], [2], [3]]),
    "정사각 행렬": np.array([[1, 2], [3, 4]]),
    "대각 행렬": np.diag([5, 8]),
    "단위행렬 I": np.eye(2, dtype=int),
    "영행렬 O": np.zeros((2, 2), dtype=int),
}
for name, M in kinds.items():
    print(f"{name}: shape={M.shape}\n{M}")

# %% 4. 전치: 행과 열 바꾸기
print("A.T =\n", A.T, "\nshape:", A.shape, "->", A.T.shape)

# %% 5. 데이터를 행렬로: 행 = 표본, 열 = 특성
df = pd.DataFrame({"Height": [1.2, 0.7, 1.5], "Weight": [3.4, 2.1, 3.0], "Age": [0.5, 1.8, 2.2]},
                  index=["student1", "student2", "student3"])
print(df)
X = df.values
print("X.shape =", X.shape, "-> 표본", X.shape[0], "개, 특성", X.shape[1], "개")
print("둘째 학생 =", X[1], "/ Age 열 =", X[:, 2])
