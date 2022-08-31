"""
Author: Ajda Savarin
Created: July 04th 2020
University of Washington
asavarin@uw.edu

Author: Shun-Nan Wu
Modified: July 01 2022
University of Oklahoma
swu@ou.edu

This program is used to retrieve images for the CPEX-AW and CPEX-CV field campaign forecasting template.

Required packages: os, subprocess, time.


Updates:
 - 2022-08-27: Adopt to all operating systems
"""


from datetime import datetime, timedelta
import os

forecastDir = os.getcwd()
saveDir = os.path.join('.','figs')
cropDir = os.path.join('.','figs_cropped')
finDir = os.path.join('.','figs_final')
archiveDir = os.path.join('.','forecast_archive')

today = datetime.today()
today = today.replace(hour=0, minute=0, second=0, microsecond=0)
yesterday = today - timedelta(days=1)

print("Archiving yesterday's forecast.")

archive_forecast_directories = [directory for directory in sorted(os.listdir(archiveDir)) if os.path.isdir(os.path.join(archiveDir,directory)) and 'archive-forecast' in directory]
yesterdays_directory = 'archive-forecast_' + yesterday.strftime('%Y-%m-%d')

files_in_figs = [fl for fl in os.listdir(saveDir) if not fl.startswith('.') and 'logo_cpexcv.png' not in fl]
files_in_figs_cropped = [fl for fl in os.listdir(cropDir) if not fl.startswith('.')]
files_in_figs_final = [fl for fl in os.listdir(finDir) if not fl.startswith('.')]

if yesterdays_directory in archive_forecast_directories:
  print('... Archive directory for yesterday already exists.')
  print('    ... Checking for images.')
  files_in_yesterdays_directory = [fl for fl in os.listdir( os.path.join(archiveDir,yesterdays_directory) )]
  if len(files_in_yesterdays_directory) > 0:
    print('    ... There are already files there. Will not overwrite.')
  else:
    print('    ... Archive directory is empty. Will move in figures from ./figs_final/.')
    for fl in files_in_figs_final:
      os.rename(os.path.join(finDir,fl), os.path.join(archiveDir,yesterdays_directory,fl))

    print('    ... Removing all files in ./figs./')
    for fl in files_in_figs:
      os.remove( os.path.join(saveDir,fl) )

    print('    ... Removing all files in ./figs_cropped/.')
    for fl in files_in_figs_cropped:
      os.remove( os.path.join(cropDir,fl) )

else:
  print('... Archive directory for yesterday does not exist.')
  print('    ... Creating a new directory.')
  os.mkdir( os.path.join(archiveDir,yesterdays_directory) )

  print('    ... Move in figures from ./figs_final/')
  for fl in files_in_figs_final:
    os.rename( os.path.join(finDir,fl), os.path.join(archiveDir,yesterdays_directory,fl) )

  print('    ... Removing all files in ./figs/')
  for fl in files_in_figs:
    os.remove( os.path.join(saveDir,fl) )

  print('    ... Removing all files in ./figs_cropped/')
  for fl in files_in_figs_cropped:
    os.remove( os.path.join(cropDir,fl) )

print("Archiving yesterday's forecast complete.")
