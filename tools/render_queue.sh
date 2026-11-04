#!/bin/bash
# Sequential render queue (2026-11-03 batch): reads productions from output/queue.txt (one path per line), runs tools/chain_render.sh on each (gate + all scenes + editor),
# one at a time, waiting while another chain is running. A production that blocks is logged and skipped. Stops after ~3 h with an empty queue or when output/queue.stop exists.
cd "$(dirname "$0")/.."
touch output/queue.txt; idle=0
while true; do
  [ -f output/queue.stop ] && { echo "$(date +%T) queue stopped" >> output/queue.log; exit 0; }
  if pgrep -f "chain_render" > /dev/null; then sleep 30; continue; fi
  next=$(head -n1 output/queue.txt)
  if [ -z "$next" ]; then idle=$((idle+1)); [ $idle -gt 360 ] && exit 0; sleep 30; continue; fi
  idle=0; sed -i.bak '1d' output/queue.txt; rm -f output/queue.txt.bak
  echo "$(date +%T) queue: $next" >> output/queue.log
  tools/chain_render2.sh "$next" >> output/queue.log 2>&1
done
