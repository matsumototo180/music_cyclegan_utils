#!/bin/bash

# 引数で指定したディレクトリ内のwavファイルすべてをCQT画像と位相行列に変換したものを出力する

files="$1*.wav"
for filepath in $files; do
    python generateCQTImage.py -i $filepath -o $2
done
