#!/bin/sh
ffmpeg -i $1 -ss $2 -t $3 -vcodec copy -an -y ${4}
