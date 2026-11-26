# -*- coding: utf-8 -*-
"""표지 17장 장면 명세 (480×270 격자). 안내 담당이 가운데, 양옆에 연구소 식구 둘, 칠판에 장의 대표 식."""
HOSTM = {'doc': 'doc_board', 'asst': 'asst_proud', 'fly': 'fly_point', 'robo': 'robo_calc', 'sia': 'sia_guide', 'moa': 'moa_sparkle', 'x1': 'x1_hint', 'x2': 'x2_hint', 'x3': 'x3_hint'}


def cv(tag, lines, host, left, right, props=(), host_y=150):
    spec = [('bg', 'lab'), ('board', 92, 20, 296, 112, lines, True), ('tag', 400, 8, tag, 'teal')]
    def up(e):
        e = list(e)
        if e[0] in ('arrow', 'line'): e[2] -= 100; e[4] -= 100
        else: e[2] -= 100
        return tuple(e)
    spec += [up(e) for e in props]
    spec += [('spr', left, 18, 168), ('spr', right, 366, 168, True), ('spr', HOSTM[host], 192, host_y)]
    return spec


COVERS = {
 'index': [('bg', 'lab'), ('board', 70, 16, 340, 118, ['f(x)  Ax=b  P(A|B)', 'σ²  ∂f/∂x  ∇f  λ', 'θ ← θ − α∇f'], True), ('tag', 6, 6, 'MATH DEX 01-15', 'teal'),
           ('spr', 'sia_smile', 0, 170), ('spr', 'moa_smile', 70, 176), ('spr', 'doc_board', 150, 156), ('spr', 'asst_smile', 240, 164), ('spr', 'robo_happy', 312, 172), ('spr', 'fly_point', 384, 168, True),
           ('spr', 'x1_hint', 412, 200, False, 0.5), ('spr', 'x2_hint', 436, 214, False, 0.5), ('spr', 'x3_hint', 456, 200, False, 0.5), ('star', 60, 150), ('star', 440, 150)],
 'ch01': cv('MATH-01', ['f(x) = 2x + 3', 'x ↦ y', 'π = 3.14…'], 'doc', 'x1_hint', 'robo_meh', [('curve', 400, 150, 60, 50, 'line', 'red', 2)]),
 'ch02': cv('MATH-02', ['a = 5', 'v = [1 2 3]', 'A = 2×3'], 'asst', 'sia_think', 'moa_report', [('matrix', 404, 150, [[1, 2, 3], [4, 5, 6]], 18)]),
 'ch03': cv('MATH-03', ['a + b', 'a·b = 32', '‖v‖ = 5'], 'fly', 'x3_hint', 'asst_spark', [('arrow', 20, 150, 70, 120, 'red'), ('arrow', 20, 150, 80, 140, 'blue')]),
 'ch04': cv('MATH-04', ['AB = [58 64]', '     [139 154]', 'AA⁻¹ = I'], 'robo', 'moa_ok', 'fly_type', [('matrix', 404, 146, [[1, 0], [0, 1]], 20)]),
 'ch05': cv('MATH-05', ['2x + 3y = 7', ' x −  y = 1', 'x=2, y=1'], 'sia', 'x2_hint', 'robo_wow', [('line', 400, 200, 470, 150, 'red', 2), ('line', 400, 160, 470, 196, 'blue', 2), ('ball', 436, 178, 4, 'green')]),
 'ch06': cv('MATH-06', ['P(E) = 3/6', '0 ≤ P ≤ 1', 'P(A∪B) = 5/6'], 'x1', 'sia_signal', 'robo_coin', [('dice', 30, 150, 3), ('dice', 410, 150, 6), ('coin', 450, 140, 'H')]),
 'ch07': cv('MATH-07', ['P(A|B) =', '  P(B|A)P(A)/P(B)', '≈ 16.7%'], 'moa', 'asst_shock', 'doc_think', []),
 'ch08': cv('MATH-08', ['x̄ = 6', 'σ = 2.83', 'IQR = 8'], 'x2', 'moa_tea', 'robo_calc', [('bars', 404, 140, 66, 50, [2, 4, 6, 5, 3, 2])]),
 'ch09': cv('MATH-09', ['N(μ, σ²)', 'Bin(n, p)', 'Poisson(λ)'], 'x3', 'fly_coffee', 'sia_smile', [('curve', 400, 140, 70, 50, 'normal', 'blue', 2, False)]),
 'ch10': cv('MATH-10', ['Cov = 1.2', 'r ≈ 0.775', '−1 ≤ r ≤ 1'], 'sia', 'x1_hint', 'asst_report', [('dots', 400, 140, 70, 55, 'pos', 12)]),
 'ch11': cv('MATH-11', ["(x²)' = 2x", 'lim h→0', '∫₀¹ x dx = ½'], 'robo', 'moa_report', 'x3_hint', [('curve', 400, 140, 70, 55, 'parab', 'red', 2)]),
 'ch12': cv('MATH-12', ['∂f/∂x  ∂f/∂y', '∇f = (2x, 2y)', 'z = 2x+4y−5'], 'asst', 'fly_magnify', 'sia_explain', [('contour', 398, 140, 74, 56, 4), ('arrow', 435, 168, 462, 150, 'red', 2)]),
 'ch13': cv('MATH-13', ['θ ← θ − α∇f', 'α = 0.1', 'argmin J(w,b)'], 'fly', 'robo_sigh', 'x2_hint', [('curve', 398, 140, 74, 56, 'parab', 'teal', 2), ('ball', 412, 158, 5, 'red')]),
 'ch14': cv('MATH-14', ['Ax = λx', 'det(A−λI) = 0', 'PC1  PC2'], 'doc', 'asst_firm', 'moa_sparkle', [('dots', 400, 140, 70, 55, 'cloud', 18), ('arrow', 410, 192, 466, 146, 'red', 2)]),
 'ch15': cv('MATH-15', ['σ(x)=1/(1+e⁻ˣ)', 'max(0, x)', 'softmax'], 'x3', 'x1_hint', 'x2_hint', [('star', 30, 140), ('star', 450, 140), ('tag', 6, 140, 'QUICK!', 'red')]),
 'practice': [('bg', 'lab'), ('board', 20, 16, 200, 100, ['SHOP  cos θ', 'CLINIC P(D|T)', 'TRAIN α', 'PCA  k=1']), ('tag', 400, 8, 'PRACTICE', 'red'),
              ('box', 250, 20, 210, 110, 'white'), ('bars', 262, 40, 80, 70, [3, 5, 2, 6, 4], 'teal'), ('curve', 360, 40, 90, 70, 'decay', 'red', 2),
              ('spr', 'doc_judge', 40, 160), ('spr', 'asst_report', 140, 168), ('spr', 'fly_type', 240, 164), ('spr', 'robo_wow', 340, 170, True)],
}
