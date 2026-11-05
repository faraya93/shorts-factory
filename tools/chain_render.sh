#!/bin/bash
# Overnight chain: for each production given, render every scene THROUGH the driver (hard gate check + caffeinate -dimsu inside), retry a scene once, then assemble.
# usage: tools/chain_render.sh productions/pilot/a productions/pilot/b ...   (log: output/chain-<name>.log)
cd "$(dirname "$0")/.."
for prod in "$@"; do
  name=$(basename "$prod"); log=output/chain-$name.log
  n=$(.venv/bin/python -c "import json,sys;print(len(json.load(open('$prod/scenes.json'))['scenes']))")
  echo "$(date +%T) START $name ($n scenes)" | tee -a "$log"
  .venv/bin/python factory/gate.py run "$prod" >> "$log" 2>&1 || { echo "$(date +%T) GATE BLOCKED $name, production skipped" | tee -a "$log"; continue; }
  failed=""; retried=""; rm -f "$prod/build/render-failures.txt"
  for i in $(seq 1 "$n"); do
    [ -f "$prod/clips/scene-$(printf %02d $i).mp4" ] && { echo "scene $i exists, skipped" >> "$log"; continue; }
    ok=0
    for try in 1 2; do
      .venv/bin/python factory/code3d_render.py "$prod" "$i" --mode final >> "$log" 2>&1 && { ok=1; break; }
      echo "scene $i attempt $try FAILED" >> "$log"
      [ $try = 1 ] && retried="$retried $i"
    done
    [ $ok = 1 ] || failed="$failed $i"
  done
  # A failed sub-step must never pass silently (2026-11-04): a scene that failed both attempts, or a missing clip, makes the production INCOMPLETE, not DONE.
  for i in $(seq 1 "$n"); do [ -f "$prod/clips/scene-$(printf %02d $i).mp4" ] || case " $failed " in *" $i "*) ;; *) failed="$failed $i";; esac; done
  if [ -n "$failed" ]; then
    mkdir -p "$prod/build"; echo "scenes failed after 2 attempts:$failed" > "$prod/build/render-failures.txt"
    echo "$(date +%T) INCOMPLETE $name (scenes failed:$failed; editor not run, see $log)" | tee -a "$log"; continue
  fi
  .venv/bin/python factory/editor.py "$prod" >> "$log" 2>&1 || { echo "$(date +%T) INCOMPLETE $name (editor failed, see $log)" | tee -a "$log"; continue; }
  [ -n "$retried" ] && echo "$(date +%T) DONE $name (WARNING: first attempt failed for scenes:$retried, recovered on retry, see $log)" | tee -a "$log" || echo "$(date +%T) DONE $name" | tee -a "$log"
done
