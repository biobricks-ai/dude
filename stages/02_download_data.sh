#!/usr/bin/env bash

# TODO Only downloading *.ism files for now.

mkdir -p ./download

cat list/target_links.txt | xargs -I {} wget -P download/  -nH --cut-dirs=2 -r -l 1 -A '*.ism' 'https://dude.docking.org/targets/{}'
