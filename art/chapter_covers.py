# -*- coding: utf-8 -*-
"""장 표지 15장을 승인된 목차 표지(Genspark, 연구소 식구 아홉 명이 모두 나옴)에서 만든다.
목차 표지를 480×270 격자로 줄이고 → 칠판 글씨를 장의 대표 식으로 바꾸고 → 이번 장 안내 담당에 조명(나머지는 조금 어둡게)과 화살표·이름표를 달고 → NEAREST 4배 무손실 WebP.
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
    g = base.copy()
    d = ImageDraw.Draw(g); d.fontmode = '1'
    bc = g.getpixel((118, 104))
    d.rectangle([111, 37, 367, 99], fill=bc)
    lines = board_lines(key); f = ImageFont.truetype(F, 18 if max(len(l) for l in lines) <= 16 else 15)
    for i, t in enumerate(lines):
        w = d.textlength(t, font=f); d.text(((111 + 367 - w) / 2, 41 + i * 20), t, font=f, fill=(236, 242, 230))
    cx, top, hw = POS[host]
    dark = ImageEnhance.Brightness(g).enhance(0.8)
    m = Image.new('L', g.size, 0); md = ImageDraw.Draw(m)
    md.ellipse([cx - hw - 6, top - 14, cx + hw + 6, 240], fill=255)
    out = Image.composite(g, dark, m)
    od = ImageDraw.Draw(out); od.fontmode = '1'
    tf = ImageFont.truetype(F, 10); lab = 'GUIDE'; tw = od.textlength(lab, font=tf); y = 238
    od.polygon([(cx - 5, y + 5), (cx + 5, y + 5), (cx, y - 2)], fill=(255, 205, 40), outline=(60, 40, 0))
    od.rectangle([cx - tw / 2 - 4, y + 6, cx + tw / 2 + 4, y + 19], fill=(255, 250, 225), outline=(60, 40, 0)); od.text((cx - tw / 2, y + 7), lab, font=tf, fill=(60, 40, 0))
    tf2 = ImageFont.truetype(F, 12); od.rectangle([6, 6, 18 + od.textlength(slide, font=tf2), 22], fill=(255, 255, 255), outline=(15, 127, 134)); od.text((12, 8), slide, font=tf2, fill=(15, 127, 134))
    return out
if __name__ == '__main__':
    src = Image.open(os.path.join(R, 'img', 'source', 'cover_index_genspark.png')).convert('RGB').resize((480, 270), Image.LANCZOS)
    for key, out, slide, short, sub, host, part in TOC:
        im = make(src, key, slide, host)
        big = im.resize((1920, 1080), Image.NEAREST); big.save(os.path.join(R, 'img', 'cover_%s.webp' % key), 'WEBP', lossless=True, method=6)
        big.resize((960, 540), Image.NEAREST).save(os.path.join(R, 'img', 'og', '%s.png' % key), optimize=True)
        print('cover', key, host)
