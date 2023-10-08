#!/bin/bash

videos=`ls -1 originals/*.mp4`

rm -rf *.mp4

for video in $videos
do
    ffmpeg -i $video -c:v libx264 -crf 23 -c:a aac -strict experimental -b:a 128k $(basename -- "$video")
done