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


#os_system='Windows'
#os_system='Linux'
os_system='Mac'

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
  if os_system=='Mac' or os_system=='Linux': cmd = ['python ' + os.path.join(cwd,'supplementary','download_daily_images_all.py')]
  if os_system=='Windows': cmd = ['python ' + os.path.join(cwd,'supplementary','download_daily_images_all_windows.py')]
  os.system(' '.join(cmd))


if run_animations:
  print(" ")
  print(" ")
  print(" ")
  print("... Running create_animations.py")
  if os_system=='Mac' or os_system=='Linux': cmd = ['python ' + os.path.join(cwd,'supplementary','create_animations.py')]
  if os_system=='Windows': cmd = ['python ' + os.path.join(cwd,'supplementary','create_animations_windows.py')]
  os.system(' '.join(cmd))


if run_processing:
  print(" ")
  print(" ")
  print(" ")
  print("... Running crop_edit_daily_images.py")
  if os_system=='Mac' or os_system=='Linux': cmd = ['python ' + os.path.join(cwd,'supplementary','crop_edit_daily_images.py')]
  if os_system=='Windows': cmd = ['python ' + os.path.join(cwd,'supplementary','crop_edit_daily_images_windows.py')]
  os.system(' '.join(cmd))
