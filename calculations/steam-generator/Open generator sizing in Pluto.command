#!/bin/zsh
set -e
worksheet_dir="$(cd -- "$(dirname -- "$0")" && pwd)"
if [[ -x "$HOME/.juliaup/bin/julia" ]]; then
    worksheet_julia="$HOME/.juliaup/bin/julia"
else
    worksheet_julia="$(command -v julia || true)"
fi
if [[ -z "$worksheet_julia" ]]; then
    print 'Julia was not found. Install Julia, then run this launcher again.'
    read 'reply?Press Return to close.'
    exit 1
fi
print 'Starting your generator-sizing notebook in Pluto.'
print 'Keep this Terminal window open while using it. Press Control-C here when finished.'
"$worksheet_julia" --startup-file=no --project="$worksheet_dir/pluto-environment" -e 'using Pkg; Pkg.instantiate(); using Pluto; Pluto.run(notebook=ARGS[1])' "$worksheet_dir/Generator sizing - Pluto.jl"
