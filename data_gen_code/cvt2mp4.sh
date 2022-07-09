#!/bin/sh
ffmpeg -i $1 -vcodec copy -an $2
