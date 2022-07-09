#!/bin/sh
ffmpeg -i $1 -f rawvideo -vcodec rawvideo -s 3840x2160 -r $4 -pix_fmt yuv420p -i $2 -lavfi ssim="stats_file=$3" -f null - 
