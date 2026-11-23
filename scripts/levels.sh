#!/usr/bin/env bash
# Level tools. Examples:
#   ./scripts/levels.sh audit                 check every level against its rules
#   ./scripts/levels.sh check 30              explain one level
#   ./scripts/levels.sh make 30 --write       generate a new level 30 and save it to data/levels.json
set -euo pipefail
cd "$(dirname "$0")/.."
mvn -q -B -pl levels -am -DskipTests package
exec java -cp engine/target/classes:levels/target/classes io.github.mattyhamps.scareamouse.levels.LevelsCli "$@"
