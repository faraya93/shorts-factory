#!/bin/bash
# Overnight chain: for each production given, render every scene THROUGH the driver (hard gate check + caffeinate -dimsu inside), retry a scene once, then assemble.
# usage: tools/chain_render.sh productions/pilot/a productions/pilot/b ...   (log: output/chain-<name>.log)
cd "$(dirname "$0")/.."
for prod in "$@"; do
  name=$(basename "$prod"); log=output/chain-$name.log
  n=$(.venv/bin/python -c "import json,sys;print(len(json.load(open('$prod/scenes.json'))['scenes']))")
  echo "$(date +%T) START $name ($n scenes)" | tee -a "$log"
  .venv/bin/python factory/gate.py run "$prod" >> "$log" 2>&1 || { echo "$(date +%T) GATE BLOCKED $name, production skipped" | tee -a "$log"; continue; }
  for i in $(seq 1 "$n"); do
    [ -f "$prod/clips/scene-$(printf %02d $i).mp4" ] && { echo "scene $i exists, skipped" >> "$log"; continue; }
    for try in 1 2; do
      .venv/bin/python factory/code3d_render.py "$prod" "$i" --mode final >> "$log" 2>&1 && break
      echo "scene $i attempt $try FAILED" >> "$log"
    done
  done
  .venv/bin/python factory/editor.py "$prod" >> "$log" 2>&1
  echo "$(date +%T) DONE $name" | tee -a "$log"
done
