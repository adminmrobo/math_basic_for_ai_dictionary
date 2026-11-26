#!/bin/sh
# 금지 단어 검사 — 결과물 전체에서 0건이어야 한다: sh code/check_words.sh
cd "$(dirname "$0")/.." || exit 1
bad=0
for w in 칸 사다리 관통 장부 수포자 통포자 supoja 포기한 쉽죠 당연히 기초인데 중학생도 "고등학생 눈높이" "중·고등학생 눈높이"; do
  n=$(cat ./*.html practice/*.html docs/*.md docs/genspark/*.md README.md build/content/*.py build/*.py build/mathlab.js colab/*.ipynb 2>/dev/null | grep -o "$w" | wc -l)
  [ "$n" -ne 0 ] && { echo "BAD $w: $n"; bad=1; }
done
[ $bad -eq 0 ] && echo "금지 단어 0건"
exit $bad
