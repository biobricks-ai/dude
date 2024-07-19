#!/usr/bin/env bash

mkdir -p ./download

cat list/target_links.txt | xargs -I {} wget -P download/ "https://dude.docking.org//targets/{}/{}.tar.gz"

