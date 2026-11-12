#!/bin/bash
# usage: tools/proof_read.sh <production> <proof id>:<stem> [<proof id>:<stem> ...]   read each proof still with three isolated readers and record it in proofs.json (block B5); prints guesses, confidences and PASS/FAIL
cd "$(dirname "$0")/.." || exit 1
prod=$1; shift
for pair in "$@"; do
  id=${pair%%:*}; stem=${pair##*:}
  echo "== $id ($stem)"
  .venv/bin/python tools/blind_read.py "productions/_lab/proofs-b5/build/stills/$stem/still-0010.png" --record proof "$prod" "$id" 2>&1 | .venv/bin/python -c "
import sys, json
t = sys.stdin.read().strip().splitlines()
try:
    print([(x['guess'][:90], x['confidence']) for x in json.loads(t[0])])
except Exception:
    print('\n'.join(t))
print(t[-1])"
done
