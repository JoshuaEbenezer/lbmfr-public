# Data Generation

This folder contains code used to generate the videos for the video quality study.


## Encoding and cutting
The videos were generated using the Elemental encoder. After generation, the videos were converted to the y4m format. The timestamps at which the videos were to be cut were identified and converted to the corresponding frame numbers. The y4m videos were then cut with frame-level accuracy. The cut videos were then displayed to subjects.

## Hashing

When videos were displayed to the subjects, the video player would briefly display the video name. If the original video name had been displayed, it might have given subjects a clue about the quality. Hence, all the videos were hashed and the hashed videos were played instead of the original.

## Groups

There are 750 videos generated from 30 contents in this study. 95 subjects participated in the study. They were divided into three groups of approximately 30 subjects each and each group watched exactly 250 videos of exactly 10 contents each.  

## Display order

In order to remove content bias, the videos' display order was completely randomized. Videos of the same content were not allowed to be adjacent. For Group 1, the videos were distributed across two sessions. For Groups 2 and 3, videos of the same content were shown in the same session. We found no differences between the two methods in terms of inter-subject agreement/correlation.
 
## Display hardware

The videos were displayed on LG C9 55 inch OLED TVs through HDMI 2.2 cables to Alienware M15 R4 laptops.

## Display software 

The scores were collected automatically through a slider interface that could be controlled with a mouse. The software was created using the psychopy library in python and the videos were played using Potlplayer.

## Steps to generate videos (after encoding)

1. Generate y4m files - cvt_all_mp42y4m.py
2. Cut y4m files using frame numbers - cut_y4m_videos.py and cut_source_y4m_videos.py
3. Convert video names to hashes and store a hashed copy of the database - generate_hash.py
4. Divide the hashed copy into the 3 groups - divide_vids_into_groups.py
5. Randomize the videos within each group for each subject and output lists - randomize_groups.py
6. Change paths in psychopy to point to the appropriate lists and the hashed videos  

## Generating motion interpolated and frame duplicated SFR videos

Use increase_fps_of_dis_vids.py to achieve this. The variable "frame_duplicate" should be True for frame duplication, and False for motion interpolation. Check all paths carefully.

## Generating downsampled versions of source videos

Refer to source code of ST GREED for this. Available at algo_code/stgreed/
