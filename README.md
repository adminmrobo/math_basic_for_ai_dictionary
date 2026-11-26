# 수리 도감 — 인공지능을 위한 수리적 기초

인공지능에 쓰이는 수학을 **열다섯 장, 125개 항목**으로 찾아보는 도감입니다. 연구소 수학 노트 인포그래픽 **MATH-01 ~ MATH-15** 전부를 바탕으로, 장마다 연구소 식구(박사·하루·초파리·주판봇·시아·모아·X1·X2·X3)가 돌아가며 안내합니다. 구성과 난이도는 자매편 [좌표 첫걸음](https://adminmrobo.github.io/hello_space_lab/index.html)을 본보기로, 고등학교 1학년 수학으로 출발할 수 있게 썼습니다.

- 사이트: https://adminmrobo.github.io/math_basic_for_ai_dictionary/
- 글 · 안상선 ((주)M-Robo 대표) · [저자 소개](https://adminmrobo.github.io/who_am_i/who_am_i.html)
- 기본 내용을 이야기로 먼저 보려면: [인공지능을 위한 수학 — 숫자로 담고, 한 번에 풀기](https://adminmrobo.github.io/math_for_ai_lab/) (목차에서 조교 하루가 추천)

## 장마다 들어 있는 것
1. 안내 담당의 상황 질문과 「처음 오신 분께 — 3줄」
2. **도감 항목** — 원자료 슬라이드의 상자를 빠짐없이: 말로 먼저 · 숫자로 한 번 해 보기 · 학교 수학으로 보면 · AI에서는 · (접는) 식
3. **웃는 그림 2장** (16비트 픽셀풍, 지금은 임시 그림 — `docs/IMAGE_PROMPTS.md`)
4. **실험실** — 직접 움직이는 계산기·그래프 1개, 왜 이 방법 / 하루의 수식 상자, 박사의 정리
5. **AI 판단 코너** — 주판봇의 성급한 답에서 틀린 곳 찾기, 확인 퀴즈
6. **코랩 실습실** — ① 생성 AI 실습 프롬프트(복사) ② 실제 구현 코드(코랩에서 열기, .py/.ipynb) ③ 실행 결과 ④ 비교 과제
7. 정리 · 용어 카드 · 원자료와 다르게 쓴 곳 · 한계 · 지식 색인(#kg)·온톨로지 꾸러미(#export)

## 열다섯 장
| 원자료 | 파일 | 안내 | 제목 | 항목 | 웃는 그림 | 코랩 |
|---|---|---|---|---|---|---|
| MATH-01 | `01_math_basics.html` | 박사 | 수학 기초 — 변수·식·함수 | 8 | 변수의 옷장, 상수의 고집 / 고장 난 자판기는 함수가 아니다 | `colab/ch01_math_basics.ipynb` |
| MATH-02 | `02_linear_algebra.html` | 조교 하루 | 선형대수 기초 — 스칼라·벡터·행렬 | 9 | 전치당한 X2 / 단위행렬은 거울 | `colab/ch02_linear_algebra.ipynb` |
| MATH-03 | `03_vector_ops.html` | 조교 초파리 | 벡터 연산 — 더하기·내적·길이·각도 | 8 | 각도 90°의 냉전 / 길이 자랑 대회 | `colab/ch03_vector_ops.ipynb` |
| MATH-04 | `04_matrix_ops.html` | 조교 주판봇 | 행렬 연산 — 곱셈·전치·역행렬 | 8 | AB ≠ BA 소동 / 행렬식 0의 저주 | `colab/ch04_matrix_ops.ipynb` |
| MATH-05 | `05_linear_systems.html` | 시아 | 연립일차방정식 — Ax = b와 선형 회귀 | 7 | 평행선의 짝사랑 / 쌍둥이 방정식 | `colab/ch05_linear_systems.ipynb` |
| MATH-06 | `06_probability.html` | X1 | 확률 기초 — 사건·덧셈·곱셈 | 8 | 세 번 연속 홀수 사건 / 두 번 센 2번 눈 | `colab/ch06_probability.ipynb` |
| MATH-07 | `07_bayes.html` | 모아 | 조건부 확률과 베이즈 — 새 정보로 고치는 믿음 | 8 | 99% 검사의 배신 / 증거를 먹고 자라는 믿음 | `colab/ch07_bayes.ipynb` |
| MATH-08 | `08_statistics.html` | X2 | 통계 기초 — 평균·분산·사분위 | 8 | 평균을 끌고 간 100점 / 평균은 같은데 반 분위기는 정반대 | `colab/ch08_statistics.ipynb` |
| MATH-09 | `09_distributions.html` | X3 | 확률분포 — 이항·포아송·정규 | 9 | 콜센터의 포아송 예언 / 종 모양 줄서기 | `colab/ch09_distributions.ipynb` |
| MATH-10 | `10_correlation.html` | 시아 | 상관과 공분산 — 함께 움직이는 정도 | 8 | 아이스크림과 상어 / r = 0의 함정 | `colab/ch10_correlation.ipynb` |
| MATH-11 | `11_calculus.html` | 조교 주판봇 | 미적분 기초 — 극한·미분·적분 | 9 | h를 줄이는 다이어트 / 연쇄 법칙 기차 | `colab/ch11_calculus.ipynb` |
| MATH-12 | `12_gradient.html` | 조교 하루 | 편미분과 그래디언트 — 여러 방향의 기울기 | 8 | 안개 속 하산 작전 / y는 잠깐 얼음! | `colab/ch12_gradient.ipynb` |
| MATH-13 | `13_optimization.html` | 조교 초파리 | 최적화 — 경사하강과 학습률 | 8 | 학습률 1.1의 롤러코스터 / α = 0.0001의 달팽이 | `colab/ch13_optimization.ipynb` |
| MATH-14 | `14_eigen_pca.html` | 박사 | 고윳값·고유벡터와 PCA — 데이터의 주축 찾기 | 8 | 고집 센 화살표 / 납작해진 점 구름 | `colab/ch14_eigen_pca.ipynb` |
| MATH-15 | `15_quick_revision.html` | X3 | 총정리 — 공식 도감과 실전 예제 | 11 | X 삼총사의 공식 줄다리기 / ReLU 문지기 | `colab/ch15_quick_revision.ipynb` |
| — | `index.html` | 하루(길 안내) | 목차 · 도감 검색 · 먼저 볼 곳 | 125 | — | — |
| — | `practice/index.html` | 넷 | 마지막 장 · 실전 연습장 (`#shop` `#clinic` `#train` `#compress`, 미션 12개) | — | — | — |

## 폴더
```
.
├─ index.html · 01~15_*.html · practice/index.html   완성 페이지 (build/에서 만듦)
├─ build/
│  ├─ content/ch01.py ~ ch15.py   장마다 항목·대사·실험·그림 장면·퀴즈·프롬프트·코드 (내용의 원본)
│  ├─ gen.py                      같은 틀로 *.src.html 생성 + colab/*.ipynb, code/colab_py/*.py 생성
│  ├─ index_page.py · practice_page.py   목차(도감 검색)·실전 연습장
│  ├─ mathlab.js                  실험실 15종 + 계산 모듈(ML.calc) + 공식 도감 54개
│  ├─ kg_defs.py                  지식 색인·서지 → build/kg/
│  ├─ common.css · common.js · sprites96.js · kgx.js · backbone.json   공용 디자인·캐릭터 팩·색인 모듈 (hello_space_lab에서)
│  └─ build.js                    조립
├─ art/scenes.py · covers.py      픽셀 장면 엔진 (표지: 식구 아홉 명이 모두 모이고 안내 담당이 맨 앞, 480×270 ×4, 웃는 그림 600×400 ×2, 무손실 WebP)
├─ colab/                         코랩 노트북 15개
├─ code/
│  ├─ colab_py/                   같은 코드의 .py
│  ├─ outputs/                    코드를 실제로 돌린 출력 (페이지 「실행하면 이렇게 나옵니다」)
│  ├─ run_colab.py                15개 코드 실제 실행 검사
│  ├─ check_numbers.py            예시 숫자 55개 + 실험실 계산 14개 검산
│  ├─ check_missions.py           실전 연습장 미션 12개 판정 검사(조작 전 통과 0)
│  ├─ check_browser.py            390·1280px 가로 넘침·콘솔 오류·빈 그림 검사
│  ├─ check_links.py · check_words.sh   내부 링크·금지 단어 검사
│  └─ make_docs.py · shot.py
├─ docs/PLAN.md · IMAGE_PROMPTS.md · AHNBOAT_CARD.md
└─ img/  표지 17장, toon/ 웃는 그림 30장, og/ 공유 미리보기 960×540
```

다시 만들기: `python3 code/run_colab.py && python3 build/gen.py && python3 build/gen.py index practice && python3 build/kg_defs.py && python3 art/scenes.py && node build/build.js`
검사: `python3 code/check_numbers.py && python3 code/check_missions.py && python3 code/check_browser.py && python3 code/check_links.py && sh code/check_words.sh`

## 저작권
원자료는 연구소 수학 노트 인포그래픽(MATH-01~15)입니다. 캐릭터 이름·설정·그림은 저작권자 안상선의 허락 없이 사용할 수 없습니다. 숫자 예시는 설명용이며 의료·경영·투자 판단의 근거가 아닙니다.
