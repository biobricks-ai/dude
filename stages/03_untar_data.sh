#!/bin/bash

mkdir -p extract/

# Directory containing files
directory="download"

find "$directory" -type f -name "*.tar.gz" | xargs -I {} sh -c '
    # Extract filename without extension
    filename=$(basename "{}" .tar.gz)

    # Extract .tar.gz file
    tar -xzvf "{}" -C extract

    # Find the extracted .tar.gz file and unzip if there are .zip files inside
    find extract -type f -name "*.zip" | xargs -I {} unzip -d extract "{}"
'
