# SSIM AND PSNR

Extracts SSIM and PSNR for videos using ffmpeg and daala.

The daala version is more reliable because ffmpeg sometimes errors out. 

In order to run this code, first install Daala: https://xiph.org/daala/. Ensure pull request 233 (https://github.com/xiph/daala/pull/233) is merged so that y4m files are read correctly. 

Modify the paths to videos and daala in extract_ssim_and_psnr_daala.py
