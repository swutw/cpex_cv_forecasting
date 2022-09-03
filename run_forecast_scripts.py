"""
Author: Shun-Nan Wu
Created: Aug. 27 2022
University of Oklahoma
swu@ou.edu

This python script will combine a bunch of steps (true/false switches) in creating the forecast template.
Things you will need to change after downloading this to your computer:
  - change true/false switches according to what you want executed
  - change true/false switched_download.txt according to what you want to download
"""

import os
import subprocess


change_work_dir=True
run_archive=True
run_download=True
run_animations=True
run_processing=True

cwd = os.getcwd()

if change_work_dir:
  print(" ")
  print(" ")
  print(" ")
  print("... Changing working directory to CPEX forecast template.")
  cmd = ['cd ' + cwd]
  os.system(' '.join(cmd))


if run_archive:
  print(" ")
  print(" ")
  print(" ")
  print("... Archiving yesterday's imagery.")
  cmd = ['python ' + os.path.join(cwd,'supplementary','archive_yesterdays_images.py')]
  os.system(' '.join(cmd))


if run_download:
  print(" ")
  print(" ")
  print(" ")
  print("... Running download_daily_images_all.py")
  cmd = ['python ' + os.path.join(cwd,'supplementary','download_daily_images_all.py')]
  os.system(' '.join(cmd))


if run_animations:
  print(" ")
  print(" ")
  print(" ")
  print("... Running create_animations.py")
  cmd = ['python ' + os.path.join(cwd,'supplementary','create_animations.py')]
  os.system(' '.join(cmd))


if run_processing:
  print(" ")
  print(" ")
  print(" ")
  print("... Running crop_edit_daily_images.py")
  cmd = ['python ' + os.path.join(cwd,'supplementary','crop_edit_daily_images.py')]
  os.system(' '.join(cmd))
