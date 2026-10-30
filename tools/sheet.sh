#!/bin/bash
# usage: tools/sheet.sh <stills dir> out.png frame1 frame2 ...   (contact sheet of draft stills, 270 px wide tiles)
d=$1; out=$2; shift 2; args=(); n=0
for f in "$@"; do ffmpeg -y -v error -i "$d/still-$(printf %04d $f).png" -vf scale=270:-1 "$d/sm-$f.png"; args+=(-i "$d/sm-$f.png"); n=$((n+1)); done
ffmpeg -y -v error "${args[@]}" -filter_complex hstack=$n "$out"
