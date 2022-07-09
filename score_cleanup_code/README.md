# Source code for cleaning up scores from the study

The final set of scores used for this study were sureal scores (https://github.com/Netflix/sureal). See the folder `sureal` for details. Final scores are in `sureal/lbmfr_sureal_scores.csv`.

Note that there are different ways of finding MOS: averaging of raw scores and averaging of Z scores. Please be aware of the differences.

Towards the end of the project we found that raw averaging of MOS scores is more reliable than Z score averaging. To do raw averaging,
1. keep_first_score.py - keeps only unique scores
2. mos_zscore_conversion.py - converts MOS to session-wise Z scores per subject, per video
3. average_subject_rawavg.py - find MOS by averaging raw scores across subjects for each video 
4. create_dmos_from_raw_avg_mos.py - find DMOS by subtracting MOS of reference from MOS of distorted video

Please refer to the jupyter notebook 'score_cleanup.ipynb' for a walkthrough of the process of score cleanup when Z scores are used.

The sequence in which python scripts are to be run (if you don't want to use jupyter) are (for Z scores, NOT raw averaging):

1. keep_first_score.py - keeps only unique scores
2. mos_zscore_conversion.py - converts MOS to session-wise Z scores per subject, per video
3. average_subject_zscores.py - find MOS by averaging Z scores across subjects for each video 
4. create_dmos_from_mos.py - find DMOS by subtracting MOS of reference from MOS of distorted video

