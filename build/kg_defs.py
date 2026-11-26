# -*- coding: utf-8 -*-
"""지식 색인·참고문헌·페이지 서지 → build/kg/kg_{key}.json · refs_{key}.json · meta_{key}.json
장마다 도감 항목(개념), 실험실(시뮬레이션), 웃는 그림(비유), AI 판단 코너(질문), 한계를 노드로 만든다."""
import json, os, sys, re
B = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, B); sys.path.insert(0, os.path.join(B, 'content'))
from gen import load, TOC, TOCD, SITE, KEYS, MFA, SIS
os.makedirs(os.path.join(B, 'kg'), exist_ok=True)
TYPE_PREFIX = {'Concept': 'concept', 'Analogy': 'analogy', 'Simulation': 'sim', 'Limitation': 'limitation', 'Question': 'question', 'Method': 'method', 'Claim': 'claim'}
strip = lambda s: re.sub(r'<[^>]+>', '', s)


def nid(t, s): return 'lab:%s/%s' % (TYPE_PREFIX[t], s)


def node(t, s, ko, en, page, anc, d):
    return {'id': nid(t, s), 'type': t, 'label': {'ko': ko, 'en': en}, 'page': page, 'anchor': anc, 'level': 1, 'status': 'known', 'confidence': 'high',
            'coverage': 'explained', 'family': 'math-for-ai', 'domain': ['math', 'ai'], 'match': [], 'definition': {'ko': strip(d)}}


def refs_for(key):
    out = [{'id': 'ahn_math_for_ai', 'type': 'webpage', 'title': '인공지능을 위한 수학 — 공식 12장이 모델 하나가 되기까지', 'author': [{'family': '안', 'given': '상선'}], 'issued': {'date-parts': [[2026]]},
            'URL': MFA + (SIS[key][0] if key in SIS else ''), 'lab': {'work': 'lab:work/ahn_math_for_ai', 'role': 'background', 'supports': [], 'locs': [], 'verified': {'title': True, 'author': True, 'year': True, 'url': True},
            'checkedBy': '연구실 저장소에서 직접 확인 (2026-11-26)', 'note': '같은 원자료를 이야기로 풀어 쓴 자매 시리즈'}},
           {'id': 'ahn_hello_space', 'type': 'webpage', 'title': '나는 어디에 있는가? — 좌표계로 본 매핑 (좌표 첫걸음)', 'author': [{'family': '안', 'given': '상선'}], 'issued': {'date-parts': [[2026]]},
            'URL': 'https://adminmrobo.github.io/hello_space_lab/', 'lab': {'work': 'lab:work/ahn_hello_space', 'role': 'background', 'supports': [], 'locs': [], 'verified': {'title': True, 'author': True, 'year': True, 'url': True},
            'checkedBy': '연구실 저장소에서 직접 확인 (2026-11-26)', 'note': '구성·난이도의 본보기가 된 자매편'}}]
    return out


def meta_for(key, title, out, about):
    return {'title': title, 'series': '수리 도감 — 인공지능을 위한 수리적 기초', 'number': key, 'creator': [{'name': '안상선', 'role': 'author', 'affiliation': '(주)M-Robo'}],
            'contributor': [{'name': 'AI 보조 제작', 'role': 'assistant'}], 'date': '2026-11-26', 'version': '1.0', 'language': ['ko'], 'license': '',
            'url': SITE + out, 'about': about[:4], 'basedOn': ['ahn_math_for_ai', 'ahn_hello_space'], 'educationalLevel': '입문', 'learningResourceType': 'interactive explainer', 'registry': 'KG_00_registry 0.2',
            'suggestedCitation': '안상선 (2026). %s. 수리 도감 — 인공지능을 위한 수리적 기초, v1.0.' % title}


def save(key, kg, refs, meta):
    for nm, obj in (('kg', kg), ('refs', refs), ('meta', meta)):
        json.dump(obj, open(os.path.join(B, 'kg', '%s_%s.json' % (nm, key)), 'w'), ensure_ascii=False, indent=1)


def chapter(key):
    C = load(key)
    out = TOCD[key][1]; page = out.replace('.html', '')
    nodes, edges = [], []
    ids = []
    for e in C['entries']:
        s = e['id']; ids.append(s)
        nodes.append(node('Concept', s, strip(e['ko']), e['en'], page, '#' + s, e['one']))
    for a, b in zip(ids, ids[1:]):
        edges.append({'s': nid('Concept', a), 'p': 'lab:prerequisiteOf', 'o': nid('Concept', b), 'anchor': '#' + b, 'confidence': 'medium'})
    L = C['lab']; sim = key + '-lab'
    nodes.append(node('Simulation', sim, L['title'].split(' — ')[0], 'Interactive lab ' + key, page, '#lab', L['doc']))
    main = ids[min(len(ids) - 1, len(ids) // 2)]
    edges.append({'s': nid('Concept', main), 'p': 'lab:demonstratedBy', 'o': nid('Simulation', sim), 'anchor': '#lab', 'confidence': 'high'})
    for i, t in enumerate(C['toons']):
        s = '%s-toon%d' % (key, i + 1)
        nodes.append(node('Analogy', s, t['title'], 'Cartoon %d' % (i + 1), page, '#toon%d' % (i + 1), t.get('point', t['title'])))
        edges.append({'s': nid('Analogy', s), 'p': 'lab:analogyOf', 'o': nid('Concept', ids[0 if i == 0 else -1] if len(ids) < 3 else ids[1 + i * (len(ids) // 2 - 1)]), 'anchor': '#toon%d' % (i + 1), 'confidence': 'medium'})
    q = key + '-ai'
    nodes.append(node('Question', q, C['ai']['title'], 'AI check ' + key, page, '#ai', C['ai']['verdict']))
    edges.append({'s': nid('Concept', main), 'p': 'lab:relatedTo', 'o': nid('Question', q), 'anchor': '#ai', 'confidence': 'medium'})
    lim = key + '-limit'
    nodes.append(node('Limitation', lim, '이 장의 한계', 'Limitation ' + key, page, '#sum', C['limits'][0]))
    edges.append({'s': nid('Concept', ids[0]), 'p': 'lab:hasLimitation', 'o': nid('Limitation', lim), 'anchor': '#sum', 'confidence': 'medium'})
    kg = {'version': '1.3', 'page': page, 'nodes': nodes, 'edges': edges}
    title = '%02d장 %s' % (C['no'], C['title'])
    save(key, kg, refs_for(key), meta_for(key, title, out, [n['id'] for n in nodes if n['type'] == 'Concept']))


def simple(key, out, title, items):
    page = out.replace('.html', '').replace('/index', '')
    nodes = [node(t, s, ko, en, page, anc, d) for t, s, ko, en, anc, d in items]
    edges = [{'s': nodes[0]['id'], 'p': 'lab:relatedTo', 'o': n['id'], 'anchor': n['anchor'], 'confidence': 'medium'} for n in nodes[1:]]
    save(key, {'version': '1.3', 'page': page, 'nodes': nodes, 'edges': edges}, refs_for('ch15'), meta_for(key, title, out, [nodes[0]['id']]))


if __name__ == '__main__':
    ks = sys.argv[1:] or KEYS + ['index', 'practice']
    for k in ks:
        if k == 'index':
            simple('index', 'index.html', '수리 도감 — 인공지능을 위한 수리적 기초 (목차)', [
                ('Concept', 'math-for-ai', '인공지능을 위한 수리적 기초', 'Mathematical foundations for AI', '#toc', '선형대수·확률·통계·미적분·최적화 다섯 분야를 열다섯 장 도감으로.'),
                ('Concept', 'linear-algebra', '선형대수', 'Linear algebra', '#toc', '2~5장: 스칼라·벡터·행렬, 벡터·행렬 연산, 연립방정식.'),
                ('Concept', 'prob-stats', '확률·통계', 'Probability & statistics', '#toc', '6~10장: 확률, 베이즈, 기술통계, 확률분포, 상관.'),
                ('Concept', 'calc-opt', '미적분·최적화', 'Calculus & optimization', '#toc', '11~13장: 미분, 그래디언트, 경사하강.'),
                ('Method', 'dex-search', '도감 검색', 'Dictionary search', '#search', '항목 이름·영어·뜻으로 열다섯 장의 항목을 찾는다.')])
        elif k == 'practice':
            simple('practice', 'practice/index.html', '마지막 장 · 실전 연습장 — 수리 도감', [
                ('Simulation', 'practice', '실전 연습장', 'Practice floor', '#top', '추천 매장·검사실·학습 관제실·데이터 압축실 네 현장에서 도감의 공식을 쓴다.'),
                ('Simulation', 'shop', '추천 매장', 'Recommendation shop', '#shop', '코사인 유사도로 상품 추천(3장).'),
                ('Simulation', 'clinic', '검사실', 'Test clinic', '#clinic', '베이즈 정리로 양성 판정 해석(7장).'),
                ('Simulation', 'train', '학습 관제실', 'Training control', '#train', '경사하강과 학습률(13장).'),
                ('Simulation', 'compress', '데이터 압축실', 'Compression room', '#compress', 'PCA로 차원 줄이기(14장).')])
        else:
            chapter(k)
        print('kg', k)
