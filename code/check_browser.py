# 브라우저 점검: 콘솔 오류 0, 390·1280px 가로 넘침 0, 빈 캐릭터 그림 0, 스크린샷
# python3 code/check_browser.py [파일 ...]
import sys, os, asyncio, json
from playwright.async_api import async_playwright
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = sys.argv[1:] or ['index.html'] + [l['out'] for l in json.load(open(os.path.join(R, 'build', 'pages.json'))) if l['key'].startswith('ch')] + ['practice/index.html']
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        bad = 0
        for f in FILES:
            fp = os.path.join(R, f)
            if not os.path.exists(fp): continue
            for W in (1280, 390):
                pg = await b.new_page(viewport={'width': W, 'height': 900})
                errs = []
                pg.on('pageerror', lambda e: errs.append(str(e)))
                pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' and 'fonts.g' not in m.text and 'ERR_' not in m.text else None)
                await pg.goto('file://' + fp); await pg.wait_for_timeout(900)
                r = await pg.evaluate('''()=>{const W=document.documentElement.clientWidth;const over=[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.right>W+1&&!e.closest('pre,.links,.tblwrap,.eq,.glog,#kg,#export,nav,.kgx')}).slice(0,5).map(e=>e.tagName+'.'+e.className+' '+Math.round(e.getBoundingClientRect().right));
                  const empty=[...document.querySelectorAll('img')].filter(i=>!i.getAttribute('src')).length;
                  return {sw:document.documentElement.scrollWidth,W,over,empty}}''')
                ok = not errs and r['sw'] <= W + 1 and r['empty'] == 0
                bad += 0 if ok else 1
                print(('OK ' if ok else 'BAD'), f, W, json.dumps(r, ensure_ascii=False), errs[:3])
                if W == 1280:
                    os.makedirs('/tmp/shots', exist_ok=True)
                    await pg.screenshot(path='/tmp/shots/' + f.replace('/', '_') + '.png', full_page=False)
                await pg.close()
        await b.close(); sys.exit(1 if bad else 0)
asyncio.run(main())
