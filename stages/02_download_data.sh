#!/usr/bin/env bash

mkdir -p ./download

while read -r first; do
    bash "$first"
    wait
done < links.txt
