# 실전 연습장 미션 판정 검사: 조작 전에는 통과 표시가 없고, 정답 조작을 흉내 내면 미션이 통과로 바뀌는지 확인
# python3 code/check_missions.py
import os, sys, asyncio
from playwright.async_api import async_playwright
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "([id,v])=>{const e=document.getElementById(id);e.value=v;e.dispatchEvent(new Event('input'));}"
CASES = [  # (장면, [(동작, 값)...], 통과해야 할 미션 번호)
 ('shop', [('click', '#sh_pick button:nth-child(1)')], 0),
 ('shop', [('set', 'sh_a', 5), ('set', 'sh_r', 1), ('set', 'sh_c', 3), ('click', '#sh_pick button:nth-child(1)')], 1),
 ('shop', [('click', '#sh_dbl'), ('click', '#sh_pick button:nth-child(1)')], 2),
 ('clinic', [('set', 'cl_p', 2), ('click', '#cl_t button:nth-child(2)'), ('click', '#cl_re')], 0),
 ('clinic', [('set', 'cl_p', 1)], 1),
 ('clinic', [('set', 'cl_p', 10), ('click', '#cl_re')], 2),
 ('train', [('set', 'tr_a', 0.1), ('set', 'tr_n', 20)], 0),
 ('train', [('set', 'tr_a', 0.25), ('set', 'tr_n', 200)], 1),
 ('train', [('set', 'tr_w', -4), ('set', 'tr_a', 0.15), ('set', 'tr_n', 200)], 2),
 ('compress', [('set', 'cp_r', 0.5), ('set', 'cp_k', 5)], 0),
 ('compress', [('set', 'cp_r', 0.1), ('set', 'cp_k', 2)], 1),
 ('compress', [('set', 'cp_r', 0.9), ('set', 'cp_k', 1)], 2),
]
async def main():
    bad = 0
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        for scene, acts, want in CASES:
            pg = await b.new_page(viewport={'width': 1280, 'height': 900})
            await pg.goto('file://' + os.path.join(R, 'practice', 'index.html') + '#' + scene); await pg.wait_for_timeout(500)
            before = await pg.evaluate(f"document.querySelectorAll('#{scene}_mis li.ok').length")
            for a in acts:
                if a[0] == 'set': await pg.evaluate(SET, [a[1], a[2]])
                else: await pg.click(a[1])
            await pg.wait_for_timeout(150)
            got = await pg.evaluate(f"[...document.querySelectorAll('#{scene}_mis li')].map(l=>l.classList.contains('ok'))")
            ok = before == 0 and got[want]
            bad += 0 if ok else 1
            print('OK ' if ok else 'BAD', scene, '미션', want + 1, '조작 전 통과', before, '→', got)
            await pg.close()
        await b.close()
    print('미션 판정 검사', '통과' if not bad else f'실패 {bad}')
    sys.exit(1 if bad else 0)
asyncio.run(main())
