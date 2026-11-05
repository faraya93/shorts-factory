#!/bin/bash
# usage: tools/look.sh <production> <scene> <frame,frame,...> <out.png>   draft stills + contact sheet in one go
cd "$(dirname "$0")/.."
.venv/bin/python tools/draft_still.py "$1" "$2" "$3" | tail -4 | cut -c1-300
files=""; for f in ${3//,/ }; do files="$files $1/build/stills/s$(printf %02d $2)/still-$(printf %04d $f).png"; done
.venv/bin/python tools/contact_sheet.py "$4" $files
