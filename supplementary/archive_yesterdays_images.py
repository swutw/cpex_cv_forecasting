"""
Author: Ajda Savarin
Created: July 20th 2021
University of Washington
asavarin@uw.edu

This program is used to check if an archive folder for yesterday has already been created.

If yes, it does not do anything (it won't overwrite an archive).

If no, it will move all images from ./figs_final/ to the archive folder, then remove the images in ./figs/, ./figs_cropped/, and ./figs_final.

Required packages: os, datetime.

"""
from datetime import datetime, timedelta
import os

forecastDir = './'
saveDir = './figs/'
cropDir = './figs_cropped/'
finDir = './figs_final/'
archiveDir = './forecast_archive/'

today = datetime.today()
today = today.replace(hour=0, minute=0, second=0, microsecond=0)
yesterday = today - timedelta(days=1)

print("Archiving yesterday's forecast.")

archive_forecast_directories = [directory for directory in sorted(os.listdir(archiveDir)) if os.path.isdir(archiveDir+directory) and 'archive-forecast' in directory]
yesterdays_directory = 'archive-forecast_' + yesterday.strftime('%Y-%m-%d')

files_in_figs = [fl for fl in os.listdir(saveDir) if not fl.startswith('.') and 'logo_cpexcv.png' not in fl]
files_in_figs_cropped = [fl for fl in os.listdir(cropDir) if not fl.startswith('.')]
files_in_figs_final = [fl for fl in os.listdir(finDir) if not fl.startswith('.')]

if yesterdays_directory in archive_forecast_directories:
  print('... Archive directory for yesterday already exists.')
  print('    ... Checking for images.')
  files_in_yesterdays_directory = [fl for fl in os.listdir(archiveDir+yesterdays_directory)]
  if len(files_in_yesterdays_directory) > 0:
    print('    ... There are already files there. Will not overwrite.')
  else:
    print('    ... Archive directory is empty. Will move in figures from ./figs_final/.')
    for fl in files_in_figs_final:
      os.rename(finDir+fl, archiveDir+yesterdays_directory+'/'+fl)

    print('    ... Removing all files in ./figs./')
    for fl in files_in_figs:
      os.remove(saveDir+fl)

    print('    ... Removing all files in ./figs_cropped/.')
    for fl in files_in_figs_cropped:
      os.remove(cropDir+fl)

else:
  print('... Archive directory for yesterday does not exist.')
  print('    ... Creating a new directory.')
  os.mkdir(archiveDir + yesterdays_directory)

  print('    ... Move in figures from ./figs_final/')
  for fl in files_in_figs_final:
    os.rename(finDir+fl, archiveDir+yesterdays_directory+'/'+fl)

  print('    ... Removing all files in ./figs/')
  for fl in files_in_figs:
    os.remove(saveDir+fl)

  print('    ... Removing all files in ./figs_cropped/')
  for fl in files_in_figs_cropped:
    os.remove(cropDir+fl)

print("Archiving yesterday's forecast complete.")
