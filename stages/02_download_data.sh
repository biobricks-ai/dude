#!/usr/bin/env bash

mkdir -p ./download

while read -r first second third fourth; do
    wget "$first" "$second" "$third" "$fourth"
    wait
done < links.txt
