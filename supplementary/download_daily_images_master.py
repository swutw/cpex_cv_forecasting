"""
Author: Ajda Savarin
Created: July 20th 2021
University of Washington
asavarin@uw.edu

This program is used to decide if all, or only missing images will be downloaded.

It will download ALL files if:
 - there is only the logo file in ./figs (everything is missing).
 - all the files are present in ./figs (update all images).

Otherwise, it will only download the missing files.


Required packages: os.



"""
import os

forecastDir = './'
saveDir = './figs/'
cropDir = './figs_cropped/'
finDir = './figs_final/'



fl = open('./supplementary/list_of_downloaded_files.txt', 'r')
wanted_files = fl.readlines()
wanted_files = [line.rstrip() for line in wanted_files]
fl.close()

present_files = [fl for fl in os.listdir(saveDir) if fl in wanted_files]

need_to_download = [fl for fl in wanted_files if not fl in present_files]

print('Downloading ALL images.')
os.system('python ./supplementary/download_daily_images_all.py')

#if len(present_files) == 0 or len(need_to_download) <= 1:
#  print('Downloading ALL images.')
#  os.system('python ./supplementary/download_daily_images_all.py')
#
#else:
#  print('Downloading MISSING images.')
#  os.system('python ./supplementary/download_daily_images_missing.py')
