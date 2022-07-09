#!/bin/sh
python3 demo_feat_lbvfr.py --ref_path $1 --dist_path $2 --ref_fps $3 --dist_fps $4 --height $5 --width $6 --bit_depth $7 --temp_filt bior22 --outfolder $8
