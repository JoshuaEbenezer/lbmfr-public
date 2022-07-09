#!/bin/sh
vmaf -r $1 -d $2 -w 3840 -h 2160 -p 420 -b 8 --model path='/home/ubuntu/vmaf/model/vmaf_4k_v0.6.1.json' -o $3 --json --threads 80
