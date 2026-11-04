#!/bin/bash
# usage: tools/gate_all.sh prod1 prod2 ...   runs the composition gate for each, prints the BLOCK lines (log: output/gate-all.log)
cd "$(dirname "$0")/.."
for p in "$@"; do
  .venv/bin/python factory/gate.py run "$p" | tail -1 | tee -a output/gate-all.log
  grep -n "BLOCK" "$p/build/gate/gate.md" | tee -a output/gate-all.log
done
