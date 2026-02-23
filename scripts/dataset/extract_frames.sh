#!/bin/bash

STEP=5

extract_folder () {
    INPUT_DIR=$1
    OUTPUT_DIR=$2

    for VIDEO in "$INPUT_DIR"/*; do
        BASENAME=$(basename "$VIDEO")
        NAME="${BASENAME%.*}"

        echo "Extraction from $BASENAME"

        mkdir -p "$OUTPUT_DIR/$NAME"

        ffmpeg -hide_banner -loglevel error \
        -i "$VIDEO" \
        -vf "fps=1/$STEP,scale=trunc(iw/2)*2:trunc(ih/2)*2,format=rgb24" \
        -q:v 2 \
        "$OUTPUT_DIR/$NAME/${NAME}_frame_%04d.jpg"

        echo "OK → $NAME"
    done
}

extract_folder "data/raw/youtube" "data/interim/frames/youtube"
extract_folder "data/raw/personal" "data/interim/frames/personal"

echo "Extraction done."