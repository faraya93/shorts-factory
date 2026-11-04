#!/bin/bash
# usage: tools/stills_sheet.sh <production> <scene id> <out.png> frame1 frame2 ...   (draft stills + contact sheet in one go; CPU=1 uses CPU Cycles while a final render runs)
prod=$1; n=$2; out=$3; shift 3; frames=$(IFS=,; echo "$*")
cd "$(dirname "$0")/.."
.venv/bin/python tools/draft_still.py "$prod" "$n" "$frames" ${CPU:+--cpu} > /dev/null || exit 1
tools/sheet.sh "$prod/build/stills/s$(printf %02d $n)" "$out" "$@"
