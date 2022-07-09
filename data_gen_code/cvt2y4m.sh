#!/bin/sh
ffmpeg -y -f rawvideo -vcodec rawvideo -s $4 -r $3 -pix_fmt yuv420p -i $1 -an $2  -nostdin -loglevel panic
