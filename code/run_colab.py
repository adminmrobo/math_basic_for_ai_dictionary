# 코랩 코드 실제 실행 검사: python3 code/run_colab.py [ch01 ...]
# 장마다 build/content/chNN.py의 code를 새 파이썬으로 실행(MPLBACKEND=Agg, 그림 창 대신 파일)하고, 출력을 code/outputs/chNN.txt에 남긴다.
import sys, os, subprocess, importlib, tempfile
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(R, 'build', 'content'))
keys = sys.argv[1:] or ['ch%02d' % i for i in range(1, 16)]
bad = 0
for k in keys:
    code = importlib.import_module(k).CH['code']
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, k + '.py'); open(f, 'w').write(code)
        env = dict(os.environ, MPLBACKEND='Agg', PYTHONHASHSEED='0')
        p = subprocess.run([sys.executable, '-I', f], cwd=d, capture_output=True, text=True, env=env, timeout=300)
    out = p.stdout
    open(os.path.join(R, 'code', 'outputs', k + '.txt'), 'w').write(out)
    ok = p.returncode == 0 and 'Traceback' not in p.stderr
    warn = [l for l in p.stderr.splitlines() if l.strip() and 'Warning' in l]
    print(k, 'OK' if ok else 'FAIL', '%d줄' % len(out.splitlines()), ('경고 %d' % len(warn)) if warn else '')
    if not ok: bad = 1; print(p.stderr[-1500:])
sys.exit(bad)
