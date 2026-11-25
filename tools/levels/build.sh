#!/bin/bash
# Builds levels FROM..TO in order (LevelsCli make --write), one at a time, after a quick dry run.
#   tools/levels/build.sh FROM TO            run from the repo root, after: mvn -q -pl levels -am package -DskipTests
# First it runs `LevelsCli probe FROM TO`: if any recipe is slow it stops, so you can change that recipe
# (for example move a turn tile to another level) before the long build. Then it builds each level; when
# a level repeats another puzzle or can't be built in time it tries another seed, and after two failed
# tries it stops and says which level, rather than grinding on. Progress goes to tools/levels/build.log.
# Set SKIP_PROBE=1 to resume a build without the dry run.
set -o pipefail   # so a failed dry run stops the build even though its output goes through tee
from=$1; to=$2
[ -z "$to" ] && { echo "Usage: tools/levels/build.sh FROM TO"; exit 2; }
log=tools/levels/build.log
sep=':'; case "$(uname -s)" in MINGW*|MSYS*|CYGWIN*) sep=';' ;; esac
cli() { java -cp "engine/target/classes${sep}levels/target/classes" io.github.mattyhamps.scareamouse.levels.LevelsCli "$@"; }
if [ -z "$SKIP_PROBE" ]; then
  echo "Dry run of $from-$to..." | tee -a "$log"
  cli probe "$from" "$to" --timeout 30 | tee -a "$log" || { echo "Change the slow recipes above, then run again." | tee -a "$log"; exit 1; }
fi
for n in $(seq "$from" "$to"); do
  ok=0
  for s in 0 1; do
    seed=$(( n * 1000 + s * 7919 ))
    start=$(date +%s)
    out=$(cli make "$n" --candidates 3 --balance 10 --seed "$seed" --timeout 180 --write 2>&1); rc=$?
    echo "[$n seed $seed rc $rc $(( $(date +%s) - start ))s] $(echo "$out" | grep -E 'Built|No level|same puzzle|Exception' | head -2 | tr '\n' ' ')" | tee -a "$log"
    if [ $rc -eq 0 ]; then ok=1; break; fi
  done
  if [ $ok -eq 0 ]; then echo "STOPPED at level $n: two tries failed. Change its recipe or try --seed by hand." | tee -a "$log"; exit 1; fi
done
echo "Built $from-$to." | tee -a "$log"
