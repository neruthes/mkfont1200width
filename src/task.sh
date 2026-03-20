#!/bin/bash

INPUT_FONT=$1
OUTPUT_FONT="Resized_${INPUT_FONT}"

if [ -z "$1" ]; then
    echo "Usage: ./resize.sh font.ttf"
    exit 1
fi

echo "Processing $INPUT_FONT..."

# Run FontForge with the Python script
fontforge -script resize_cjk.py "$INPUT_FONT" "$OUTPUT_FONT"

echo "Done! Saved as $OUTPUT_FONT"
