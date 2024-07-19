#!/usr/bin/env bash

mkdir -p ./download

while read -r first; do
    wget -P download/ "$first" &
    wait
done < links.txt
