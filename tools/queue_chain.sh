#!/bin/bash
# THE render queue (merged 2026-11-08, render_queue.sh is now a shim). One chain at a time and one Blender at a time are enforced by the locks in tools/blender_run.py. SF_SAMPLES=64 by default (batch lens decision 2026-11-04).
# usage: nohup tools/queue_chain.sh productions/<ch>/a productions/<ch>/b ... &
#        nohup tools/queue_chain.sh --watch &     reads output/queue.txt (one path per line); a production that blocks is logged and skipped; stops after ~3 h idle or when output/queue.stop exists
cd "$(dirname "$0")/.."
export SF_SAMPLES=${SF_SAMPLES:-64}
if [ "$1" != "--watch" ]; then
  for p in "$@"; do tools/chain_render.sh "$p"; done
  exit 0
fi
touch output/queue.txt; idle=0
while true; do
  [ -f output/queue.stop ] && { echo "$(date +%T) queue stopped" >> output/queue.log; exit 0; }
  next=$(head -n1 output/queue.txt)
  if [ -z "$next" ]; then idle=$((idle+1)); [ $idle -gt 360 ] && exit 0; sleep 30; continue; fi
  idle=0; sed -i.bak '1d' output/queue.txt; rm -f output/queue.txt.bak
  echo "$(date +%T) queue: $next" >> output/queue.log
  tools/chain_render.sh "$next" >> output/queue.log 2>&1
done
