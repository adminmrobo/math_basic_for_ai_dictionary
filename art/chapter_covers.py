# -*- coding: utf-8 -*-
"""장 표지 15장을 승인된 목차 표지(Genspark, 연구소 식구 아홉 명이 모두 나옴)에서 만든다.
목차 표지(1920×1080)의 칠판 글씨를 장의 대표 식으로 바꾸고 → 이번 장 안내 담당에 조명(나머지는 조금 어둡게)과 GUIDE 이름표를 달고 → LANCZOS 1600×900 WebP(220 KB 이하, 기본 스킬 18-15-2 v1.19).
쓰는 법: python3 art/chapter_covers.py  (원본: img/source/cover_index_genspark.png)"""
import os, sys, json
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
A = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(A)
sys.path.insert(0, A); sys.path.insert(0, os.path.join(R, 'build'))
import covers
from gen import TOC
F = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
# 480×270 격자에서 식구 위치: (가운데 x, 머리 위 y, 조명 반폭)
POS = {'fly': (50, 118, 28), 'asst': (100, 118, 25), 'robo': (153, 116, 30), 'doc': (215, 96, 30), 'moa': (267, 110, 26), 'sia': (312, 110, 26),
       'x1': (357, 134, 25), 'x2': (405, 138, 24), 'x3': (452, 132, 24)}
def board_lines(key):
    for e in covers.COVERS[key]:
        if e[0] == 'board' and len(e) > 5: return e[5]
def make(base, key, slide, host):
    """base: 1920×1080 원본. 글씨·이름표는 480×270 격자 층에 그려 4배로 얹고(픽셀 글씨), 조명은 원본 해상도에서."""
    W, H = base.size; k = W // 480
    g = base.copy(); d = ImageDraw.Draw(g)
    bc = g.getpixel((118 * k, 104 * k))
    d.rectangle([111 * k, 37 * k, 367 * k, 99 * k], fill=bc)
    lay = Image.new('RGBA', (480, 270), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay); ld.fontmode = '1'
    lines = board_lines(key); f = ImageFont.truetype(F, 18 if max(len(l) for l in lines) <= 16 else 15)
    for i, t in enumerate(lines):
        w = ld.textlength(t, font=f); ld.text(((111 + 367 - w) / 2, 41 + i * 20), t, font=f, fill=(236, 242, 230, 255))
    g.alpha_composite(lay.resize((W, H), Image.NEAREST)) if g.mode == 'RGBA' else g.paste(lay.resize((W, H), Image.NEAREST), (0, 0), lay.resize((W, H), Image.NEAREST))
    cx, top, hw = POS[host]
    dark = ImageEnhance.Brightness(g).enhance(0.8)
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).ellipse([(cx - hw - 6) * k, (top - 14) * k, (cx + hw + 6) * k, 240 * k], fill=255)
    out = Image.composite(g, dark, m)
    tl = Image.new('RGBA', (480, 270), (0, 0, 0, 0)); od = ImageDraw.Draw(tl); od.fontmode = '1'
    tf = ImageFont.truetype(F, 10); lab = 'GUIDE'; tw = od.textlength(lab, font=tf); y = 238
    od.polygon([(cx - 5, y + 5), (cx + 5, y + 5), (cx, y - 2)], fill=(255, 205, 40, 255), outline=(60, 40, 0, 255))
    od.rectangle([cx - tw / 2 - 4, y + 6, cx + tw / 2 + 4, y + 19], fill=(255, 250, 225, 255), outline=(60, 40, 0, 255)); od.text((cx - tw / 2, y + 7), lab, font=tf, fill=(60, 40, 0, 255))
    tf2 = ImageFont.truetype(F, 12); od.rectangle([6, 6, 18 + od.textlength(slide, font=tf2), 22], fill=(255, 255, 255, 255), outline=(15, 127, 134, 255)); od.text((12, 8), slide, font=tf2, fill=(15, 127, 134, 255))
    big = tl.resize((W, H), Image.NEAREST); out.paste(big, (0, 0), big)
    return out
def save_cover(im, name):
    """기본 스킬 18-15-2 v1.19: 고해상도 픽셀아트 표지는 LANCZOS 1600×900 WebP(220 KB 이하), 공유 미리보기 960×540."""
    c = im.convert('RGB').resize((1600, 900), Image.LANCZOS)
    for q in (86, 80, 74, 68):
        c.save(os.path.join(R, 'img', 'cover_%s.webp' % name), 'WEBP', quality=q, method=6)
        if os.path.getsize(os.path.join(R, 'img', 'cover_%s.webp' % name)) <= 220 * 1024: break
    im.convert('RGB').resize((960, 540), Image.LANCZOS).save(os.path.join(R, 'img', 'og', '%s.png' % name), optimize=True)
if __name__ == '__main__':
    for name in ('index', 'practice'):
        save_cover(Image.open(os.path.join(R, 'img', 'source', 'cover_%s_genspark.png' % name)), name); print('cover', name)
    src = Image.open(os.path.join(R, 'img', 'source', 'cover_index_genspark.png')).convert('RGB').resize((1920, 1080), Image.LANCZOS)
    for key, out, slide, short, sub, host, part in TOC:
        save_cover(make(src, key, slide, host), key); print('cover', key, host, os.path.getsize(os.path.join(R, 'img', 'cover_%s.webp' % key)) // 1024, 'KB')
