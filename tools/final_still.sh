#!/bin/bash
# usage: tools/final_still.sh <production> <scene id> <frames,comma> [samples=32] [extra blender args...]   (Cycles stills of one scene, under caffeinate; -> <production>/build/stills-final/sNN)
prod=$1; n=$2; frames=$3; samples=${4:-32}; shift 4 2>/dev/null
cd "$(dirname "$0")/.."
prefix=$(.venv/bin/python -c "import json;c=json.load(open('$prod/scenes.json'));print(c.get('scene_script_prefix','scene'))")
look=$(.venv/bin/python -c "import json;c=json.load(open('$prod/scenes.json'));print(c.get('identity_preset',''))")
ident=$(.venv/bin/python -c "import sys;sys.path.insert(0,'factory');import identity;from pathlib import Path;print(identity.export_json(production=Path('$prod').resolve()))")
mp3="$prod/audio/scene-$(printf %02d $n).mp3"
slot=300; [ -f "$mp3" ] && slot=$(.venv/bin/python -c "import subprocess,math;d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','$mp3'],capture_output=True,text=True).stdout);print(math.ceil(d*30-1e-6))")
out="$prod/build/stills-final/s$(printf %02d $n)"
t0=$(date +%s)
caffeinate -dimsu blender -b --python code3d/scenes/${prefix}_$(printf %02d $n).py -- production=$PWD/$prod mode=final slot=$slot samples=$samples stills=$frames out=$PWD/$out identity=$ident look=$look "$@" 2>&1 | grep -E "Traceback|Error|error|render profile" | head -20
echo "done in $(( $(date +%s)-t0 )) s -> $out"
