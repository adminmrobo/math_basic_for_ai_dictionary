# -*- coding: utf-8 -*-
"""픽셀 장면 엔진 — 표지(480×270 격자 → 4배 1920×1080)와 웃는 그림(600×400 격자 → 2배 1200×800).
모든 도형은 계단 현상을 살린 무(無)안티앨리어싱으로 격자에 그리고, NEAREST 정수배로만 키워 무손실 WebP로 저장한다.
캐릭터는 연구소 캐릭터 팩(fruitfly-lab-expressions 96px)을 그대로 붙인다.
쓰는 법: python3 art/scenes.py            (모든 장)
         python3 art/scenes.py ch01 ch02  (일부)"""
import os, sys, re, io, base64, math, json
from PIL import Image, ImageDraw, ImageFont
A = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(A)
sys.path.insert(0, os.path.join(R, 'build')); sys.path.insert(0, os.path.join(R, 'build', 'content'))
FONT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', 10)
FONT2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', 16)
FONT3 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', 24)
INK = (27, 36, 48); WHITE = (255, 255, 255)
PAL = {'red': (201, 48, 48), 'blue': (30, 85, 200), 'green': (19, 115, 58), 'teal': (15, 127, 134), 'amber': (214, 132, 20), 'purple': (122, 63, 214), 'pink': (196, 42, 110),
       'gray': (150, 160, 170), 'chalk': (240, 244, 236), 'yellow': (245, 200, 60), 'ink': INK, 'white': WHITE, 'sky': (190, 222, 245), 'grass': (120, 180, 90)}


def col(c):
    return PAL.get(c, c) if isinstance(c, str) else c


# ── 캐릭터 팩 ──
def load_sprites():
    s = open(os.path.join(R, 'build', 'sprites96.js')).read()
    raw = dict(re.findall(r'"([a-z0-9_]+)":"data:image/webp;base64,([^"]+)"', s))
    alias = dict(re.findall(r'"([a-z0-9]+_[a-z]+)":\s*"([a-z0-9]+_e[0-9]+)"', s))
    out = {}
    for k, v in raw.items():
        im = Image.open(io.BytesIO(base64.b64decode(v))).convert('RGBA')
        a = im.split()[3].point(lambda p: 255 if p > 110 else 0)
        im.putalpha(a); out[k] = im
    for k, v in alias.items():
        if v in out: out[k] = out[v]
    return out


SPR = load_sprites()


class Scene:
    def __init__(self, W, H):
        self.W, self.H = W, H
        self.im = Image.new('RGB', (W, H), WHITE)
        self.d = ImageDraw.Draw(self.im); self.d.fontmode = '1'

    # 배경
    def bg(self, kind='lab'):
        d, W, H = self.d, self.W, self.H
        fy = int(H * (0.84 if W == 600 else 0.78))
        if kind == 'sky':
            d.rectangle([0, 0, W, fy], fill=(214, 236, 250))
            for x, y in ((W * .15, H * .12), (W * .7, H * .18)):
                for dx, dy, r in ((0, 0, 14), (14, 4, 11), (-13, 5, 10)):
                    d.ellipse([x + dx - r, y + dy - r * .6, x + dx + r, y + dy + r * .6], fill=WHITE)
            d.rectangle([0, fy, W, H], fill=(150, 200, 110))
            for x in range(0, W, 8): d.point((x + (x // 8 % 2) * 3, fy + 4), fill=(110, 165, 85))
            return
        d.rectangle([0, 0, W, fy], fill=(247, 249, 251))
        for x in range(0, W, 60): d.line([x, 0, x, fy], fill=(236, 240, 244))
        for x in range(30, W, 120):
            d.rectangle([x - 6, 0, x + 6, 5], fill=(200, 206, 212)); d.rectangle([x - 4, 6, x + 4, 9], fill=(255, 244, 200))
        d.rectangle([0, fy - 4, W, fy], fill=(214, 220, 226))
        t = 20 if W > 500 else 16
        for y in range(fy, H, t // 2):
            for x in range(0, W, t):
                c = (232, 236, 240) if ((x // t) + (y // (t // 2))) % 2 == 0 else (222, 228, 233)
                d.rectangle([x, y, x + t, y + t // 2], fill=c)
        if kind == 'window':
            x0 = W - 110; d.rectangle([x0, 30, x0 + 80, 120], fill=(205, 230, 248), outline=(180, 190, 200), width=3); d.line([x0 + 40, 30, x0 + 40, 120], fill=(180, 190, 200), width=2)

    def board(self, x, y, w, h, lines, big=False):
        d = self.d
        d.rectangle([x - 4, y - 4, x + w + 4, y + h + 4], fill=(108, 78, 52)); d.rectangle([x, y, x + w, y + h], fill=(47, 93, 80))
        for i in range(0, w, 7): d.point((x + i, y + 2 + (i * 7) % 5), fill=(60, 108, 92))
        d.rectangle([x + 6, y + h + 4, x + 40, y + h + 7], fill=(230, 230, 230))
        f = FONT3 if big else FONT2
        lh = 28 if big else 19
        for i, t in enumerate(lines):
            d.text((x + 10, y + 8 + i * lh), t, font=f, fill=PAL['chalk'])

    def spr(self, mood, x, y, flip=False, scale=1):
        im = SPR[mood]
        if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
        if scale < 1:   # 줄일 때는 부드럽게 줄인 뒤 투명도를 다시 0/255로 (가장자리 픽셀 경계 유지)
            im = im.resize((int(96 * scale), int(96 * scale)), Image.LANCZOS)
            im.putalpha(im.split()[3].point(lambda v: 255 if v > 110 else 0))
        elif scale != 1: im = im.resize((int(96 * scale), int(96 * scale)), Image.NEAREST)
        if self.W == 600 and y >= 150 and scale == 1: y = int(self.H * 0.84) - 92   # 웃는 그림: 캐릭터는 바닥선에 선다
        self.im.paste(im, (int(x), int(y)), im)

    def text(self, x, y, t, c='ink', size=1):
        f = {1: FONT, 2: FONT2, 3: FONT3}[size]
        self.d.text((x, y), t, font=f, fill=col(c))

    def tag(self, x, y, t, c='ink'):
        w = int(self.d.textlength(t, font=FONT)) + 8
        self.d.rectangle([x, y, x + w, y + 14], fill=(255, 250, 225), outline=col(c)); self.d.text((x + 4, y + 1), t, font=FONT, fill=col(c))

    def bubble(self, x, y, t, tail='l'):
        f = FONT2; w = int(self.d.textlength(t, font=f)) + 16; h = 26
        d = self.d
        d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=INK, width=2)
        tx = x + 14 if tail == 'l' else x + w - 22
        d.polygon([(tx, y + h), (tx + 8, y + h), (tx + (-6 if tail == 'l' else 14), y + h + 12)], fill=WHITE, outline=INK)
        d.line([tx + 1, y + h - 1, tx + 7, y + h - 1], fill=WHITE, width=2)
        d.text((x + 8, y + 4), t, font=f, fill=INK)

    def box(self, x, y, w, h, fill='white', outline='ink', width=2):
        self.d.rectangle([x, y, x + w, y + h], fill=col(fill), outline=col(outline), width=width)

    def line(self, x1, y1, x2, y2, c='ink', w=2):
        self.d.line([x1, y1, x2, y2], fill=col(c), width=w)

    def arrow(self, x1, y1, x2, y2, c='red', w=3):
        c = col(c); self.d.line([x1, y1, x2, y2], fill=c, width=w)
        a = math.atan2(y2 - y1, x2 - x1); L = 10
        p1 = (x2 - L * math.cos(a - .45), y2 - L * math.sin(a - .45)); p2 = (x2 - L * math.cos(a + .45), y2 - L * math.sin(a + .45))
        self.d.polygon([(x2, y2), p1, p2], fill=c)

    def star(self, x, y, c='yellow'):
        c = col(c)
        for dx, dy in ((0, -6), (0, 6), (-6, 0), (6, 0)): self.d.line([x, y, x + dx, y + dy], fill=c, width=2)
        self.d.rectangle([x - 1, y - 1, x + 1, y + 1], fill=WHITE)

    def sweat(self, x, y):
        self.d.polygon([(x, y), (x - 5, y + 9), (x + 5, y + 9)], fill=(120, 190, 240)); self.d.ellipse([x - 5, y + 5, x + 5, y + 14], fill=(120, 190, 240))

    def question(self, x, y, c='purple'):
        self.d.text((x, y), '?', font=FONT3, fill=col(c))

    def dice(self, x, y, n, s=26):
        d = self.d; d.rectangle([x, y, x + s, y + s], fill=WHITE, outline=INK, width=2)
        P = {1: [(.5, .5)], 2: [(.25, .25), (.75, .75)], 3: [(.25, .25), (.5, .5), (.75, .75)], 4: [(.25, .25), (.75, .25), (.25, .75), (.75, .75)],
             5: [(.25, .25), (.75, .25), (.5, .5), (.25, .75), (.75, .75)], 6: [(.25, .22), (.75, .22), (.25, .5), (.75, .5), (.25, .78), (.75, .78)]}[n]
        for px, py in P:
            cx, cy = x + px * s, y + py * s; r = s * .08 + 1
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PAL['red'] if n == 1 else INK)

    def coin(self, x, y, t='H', r=14):
        self.d.ellipse([x - r, y - r, x + r, y + r], fill=(240, 196, 70), outline=(150, 110, 20), width=2); self.d.text((x - 4, y - 7), t, font=FONT2, fill=(120, 80, 10))

    def bars(self, x, y, w, h, vals, c='teal', hl=None):
        m = max(vals) or 1; n = len(vals); bw = w / n
        self.d.line([x, y + h, x + w, y + h], fill=INK, width=2)
        for i, v in enumerate(vals):
            bh = h * v / m; cc = col('red') if hl is not None and i in hl else col(c)
            self.d.rectangle([x + i * bw + 2, y + h - bh, x + (i + 1) * bw - 2, y + h - 1], fill=cc, outline=INK)

    def curve(self, x, y, w, h, kind, c='blue', wd=3, axes=True):
        if axes:
            self.d.line([x, y + h, x + w, y + h], fill=INK, width=2); self.d.line([x, y, x, y + h], fill=INK, width=2)
        pts = []
        for i in range(0, 101):
            t = i / 100
            v = {'normal': math.exp(-((t - .5) ** 2) / .02), 'parab': 1 - (2 * t - 1) ** 2 * -1 if False else (2 * t - 1) ** 2, 'exp': (math.exp(3 * t) - 1) / (math.e ** 3 - 1),
                 'decay': math.exp(-4 * t), 'sin': .5 + .45 * math.sin(t * 4 * math.pi), 'line': t, 'sqrt': math.sqrt(t), 'wave': .5 + .3 * math.sin(t * 6) + .15 * t,
                 'zigzag': .5 + .45 * (1 if (i // 12) % 2 else -1) * (1 - t)}[kind]
            pts.append((x + t * w, y + h - v * h * .92))
        self.d.line(pts, fill=col(c), width=wd)

    def matrix(self, x, y, rows, cell=22, hl=None, c='ink'):
        d = self.d; R, Cn = len(rows), len(rows[0])
        H = R * cell; W = Cn * cell
        for xx, s in ((x - 4, 1), (x + W + 4, -1)):
            d.line([xx, y - 2, xx, y + H + 2], fill=INK, width=2); d.line([xx, y - 2, xx + 5 * s, y - 2], fill=INK, width=2); d.line([xx, y + H + 2, xx + 5 * s, y + H + 2], fill=INK, width=2)
        for i, r in enumerate(rows):
            for j, v in enumerate(r):
                if hl and (i, j) in hl: d.rectangle([x + j * cell + 1, y + i * cell + 1, x + (j + 1) * cell - 1, y + (i + 1) * cell - 1], fill=(255, 226, 170))
                t = str(v); tw = d.textlength(t, font=FONT2)
                d.text((x + j * cell + (cell - tw) / 2, y + i * cell + 2), t, font=FONT2, fill=col(c))

    def dots(self, x, y, w, h, kind='pos', n=16, c='blue', seed=3):
        import random
        rnd = random.Random(seed)
        for i in range(n):
            t = rnd.random(); e = rnd.gauss(0, .12)
            v = {'pos': t + e, 'neg': 1 - t + e, 'none': rnd.random(), 'cloud': .5 + (t - .5) * .8 + e}[kind]
            v = min(max(v, 0), 1); cx, cy = x + t * w, y + h - v * h
            self.d.rectangle([cx - 3, cy - 3, cx + 3, cy + 3], fill=col(c), outline=INK)

    def ball(self, x, y, r=8, c='red'):
        self.d.ellipse([x - r, y - r, x + r, y + r], fill=col(c), outline=INK, width=2); self.d.rectangle([x - r // 2, y - r // 2, x - r // 2 + 2, y - r // 2 + 2], fill=WHITE)

    def contour(self, x, y, w, h, n=5, c='teal'):
        for i in range(n, 0, -1):
            rx, ry = w / 2 * i / n, h / 2 * i / n
            self.d.ellipse([x + w / 2 - rx, y + h / 2 - ry, x + w / 2 + rx, y + h / 2 + ry], outline=col(c), width=2)

    def venn(self, x, y, r=40):
        d = self.d
        d.ellipse([x - r, y - r, x + r, y + r], outline=PAL['blue'], width=3); d.ellipse([x + r * .9 - r, y - r, x + r * .9 + r, y + r], outline=PAL['red'], width=3)
        d.text((x - r * .55, y - 8), 'A', font=FONT2, fill=PAL['blue']); d.text((x + r * 1.15, y - 8), 'B', font=FONT2, fill=PAL['red'])

    def person(self, x, y, c='gray'):
        c = col(c); self.d.rectangle([x + 2, y, x + 7, y + 5], fill=c); self.d.rectangle([x, y + 6, x + 9, y + 14], fill=c)

    def crowd(self, x, y, cols, rows, colors):
        k = 0
        for r in range(rows):
            for cc in range(cols):
                self.person(x + cc * 12, y + r * 18, colors[k] if k < len(colors) else 'gray'); k += 1

    def rack(self, x, y, labels):
        d = self.d; w = 40 * len(labels) + 20
        d.line([x, y, x + w, y], fill=INK, width=3); d.line([x + 4, y, x + 4, y + 150], fill=INK, width=3); d.line([x + w - 4, y, x + w - 4, y + 150], fill=INK, width=3)
        for i, t in enumerate(labels):
            sx = x + 14 + i * 40; d.line([sx + 14, y, sx + 14, y + 8], fill=INK)
            d.polygon([(sx, y + 10), (sx + 28, y + 10), (sx + 32, y + 22), (sx + 26, y + 22), (sx + 26, y + 52), (sx + 2, y + 52), (sx + 2, y + 22), (sx - 4, y + 22)],
                      fill=[PAL['blue'], PAL['pink'], PAL['green'], PAL['amber']][i % 4], outline=INK)
            d.text((sx + 4, y + 28), t, font=FONT2, fill=WHITE)

    def vending(self, x, y, sign):
        d = self.d
        d.rectangle([x, y, x + 130, y + 230], fill=(200, 60, 60), outline=INK, width=3); d.rectangle([x + 10, y + 34, x + 90, y + 170], fill=(220, 240, 250), outline=INK, width=2)
        for r in range(3):
            for c in range(3): d.rectangle([x + 18 + c * 24, y + 44 + r * 40, x + 34 + c * 24, y + 72 + r * 40], fill=[PAL['blue'], PAL['yellow'], PAL['green']][(r + c) % 3], outline=INK)
        for i in range(4): d.rectangle([x + 100, y + 44 + i * 26, x + 120, y + 62 + i * 26], fill=WHITE, outline=INK); d.text((x + 106, y + 46 + i * 26), str(i + 1), font=FONT, fill=INK)
        d.rectangle([x + 20, y + 186, x + 110, y + 210], fill=(40, 40, 40))
        d.rectangle([x - 6, y - 26, x + 136, y - 2], fill=WHITE, outline=INK, width=2); d.text((x + 4, y - 22), sign, font=FONT2, fill=INK)

    def can(self, x, y, t):
        self.d.rectangle([x, y, x + 22, y + 34], fill=PAL['yellow'], outline=INK, width=2); self.d.text((x + 6, y + 9), t, font=FONT2, fill=INK)

    def save(self, path, scale):
        big = self.im.resize((self.W * scale, self.H * scale), Image.NEAREST)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        big.save(path, 'WEBP', lossless=True, quality=100, method=6)
        return big


def run(scene, spec):
    for el in spec:
        k, a = el[0], el[1:]
        if k == 'bg': scene.bg(*a)
        elif k == 'tree': tree(scene, *a)
        else: getattr(scene, k)(*a)


def tree(s, x, y):
    s.box(x, y + 40, 40, 20, 'white'); s.text(x + 4, y + 44, 'Start')
    for i, (lab, yy) in enumerate((('A', y), ('~A', y + 80))):
        s.line(x + 40, y + 50, x + 90, yy + 10, 'ink', 2); s.ball(x + 100, yy + 10, 10, 'sky'); s.text(x + 94 if i == 0 else x + 90, yy + 4, lab)
        for j, (b, y2) in enumerate((('B', yy - 12), ('~B', yy + 30))):
            s.line(x + 110, yy + 10, x + 150, y2 + 6, 'ink', 2); s.box(x + 150, y2, 50, 14, 'white', 'ink', 1); s.text(x + 154, y2 + 1, (lab + '∩' + b)[:6])


if __name__ == '__main__':
    import importlib
    from gen import TOC
    keys = sys.argv[1:] or [t[0] for t in TOC] + ['index', 'practice']
    covers = importlib.import_module('covers')
    for k in keys:
        if k in covers.COVERS:
            s = Scene(480, 270); run(s, covers.COVERS[k]); big = s.save(os.path.join(R, 'img', 'cover_%s.webp' % k), 4)
            big.resize((960, 540), Image.NEAREST).save(os.path.join(R, 'img', 'og', '%s.png' % k), optimize=True)
        if k.startswith('ch'):
            C = importlib.import_module(k).CH
            for i, t in enumerate(C['toons']):
                s = Scene(600, 400); run(s, t['scene']); s.save(os.path.join(R, 'img', 'toon', '%s_%s.webp' % (k, 'ab'[i])), 2)
        print('art', k)
