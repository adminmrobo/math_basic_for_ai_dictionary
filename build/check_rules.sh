#!/bin/sh
# 기본 스킬 규칙 점검 — 매번 되풀이되던 문제를 빌드 뒤 자동으로 잡는다.
cd "$(dirname "$0")/.."; bad=0
for f in index.html [0-9]*.html practice/index.html; do
  grep -q '<!-- px-fix v1 -->' "$f" || { echo "px-fix 없음: $f"; bad=1; }
  grep -q '조수</div>' "$f" && { echo "꾸러미 조수 글자 상자: $f"; bad=1; }
  grep -o 'image-rendering:pixelated[^"]*' "$f" | grep -qv 'important' && { echo "pixelated 직접 지정: $f"; bad=1; }
done
cmp -s build/kgx.js ../adminmrobo/ahnboat_lab_explainer/packs/task/onto-retrofit/tools/kgx.js 2>/dev/null || [ ! -d ../adminmrobo ] || { echo "kgx.js가 정본 팩과 다름"; bad=1; }
[ $bad = 0 ] && echo "규칙 점검 통과"; exit $bad
