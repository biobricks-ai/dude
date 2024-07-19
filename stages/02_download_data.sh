#!/usr/bin/env bash

mkdir -p ./download

while read -r first second third; do
    wget "$first" "$second" "$third"
    wait
done < links.txt
