#!/usr/bin/env bash

mkdir -p ./download

cat targets.txt | xargs -I {} wget -P download/ "https://dude.docking.org//targets/{}/{}.tar.gz"

