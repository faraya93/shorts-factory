#!/bin/bash
# usage: tools/proof_sheet.sh <out.png> <stem> [<stem>...]   contact sheet of proof stills (270 px tiles) so a session looks at ONE image instead of one per still
out=$1; shift; args=(); n=0; d=$(dirname "$0")/../productions/_lab/proofs-b5/build/stills
for s in "$@"; do ffmpeg -y -v error -i "$d/$s/still-0010.png" -vf scale=270:-1 "$d/$s/sm.png"; args+=(-i "$d/$s/sm.png"); n=$((n+1)); done
ffmpeg -y -v error "${args[@]}" -filter_complex hstack=$n "$out"
