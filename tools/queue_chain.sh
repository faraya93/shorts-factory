#!/bin/bash
# Run chain_render.sh for each production in turn, waiting for any running chain first (one GPU job at a time). SF_SAMPLES=64 by default (batch lens decision 2026-11-04).
# usage: nohup tools/queue_chain.sh productions/a productions/b ... &
cd "$(dirname "$0")/.."
export SF_SAMPLES=${SF_SAMPLES:-64}
while pgrep -f "tools/chain_render.sh" >/dev/null; do sleep 30; done
for p in "$@"; do
  tools/chain_render.sh "$p"
  while pgrep -f "tools/chain_render.sh" >/dev/null; do sleep 30; done
done
