# 화면 확인: python3 code/shot.py 파일 너비 선택자...  → /tmp/shots/*.png, 콘솔 오류 출력
import sys, os, asyncio
from playwright.async_api import async_playwright
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
async def main():
    f, W, sels = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
    os.makedirs('/tmp/shots', exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = await b.new_page(viewport={'width': W, 'height': 900}); errs = []
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('file://' + os.path.join(R, f)); await pg.wait_for_timeout(900)
        for s in sels:
            el = await pg.query_selector(s)
            if not el: print('missing', s); continue
            await el.scroll_into_view_if_needed(); await pg.wait_for_timeout(300)
            out = '/tmp/shots/%s_%d_%s.png' % (os.path.basename(f).replace('.html', ''), W, s.strip('#.').replace(' ', '_')[:20])
            await el.screenshot(path=out); print(out)
        print('errors:', [e for e in errs if 'fonts.g' not in e][:5])
        await b.close()
asyncio.run(main())
