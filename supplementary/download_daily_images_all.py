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

Required packages: datetime, numpy, os, subprocess, requests, bs4, urllib.


Updates:
 - 2020-07-07: Created separate strings for downloading UWIN-CM model day 1 and day 2
 - 2020-07-12: Updated the NASA GEOS image section to call Mani's script and creates animation of NASA GEOS images. Also downloads day1, day2 model images at still_image_forecast_hr (set to 17UTC -- about mid-flight).
 - 2021-07-13: Added the NHC's tropical weather outlook for 2 and 5 days. Updated the GOES-E satellite to download the tropical atlantic region from the NOAA website. Also added the latest meteosat images to be downloaded for CV. Alan Brammer's website is no longer available -- we will reach out to see if that can be brought back.
 - 2021-07-15: Animations now span the entire model day (every other hour starting at 01 UTC), instead of only from 11UTC onward.
 - 2021-07-19: Updated availability printouts and accuracy of print statements. Created a new directory where the final figures will be moved to (figs_final). Split a section off to a new script - create animations.py. Moving switches to a new file - switches_download.txt; As images are downloaded, switches_process.txt gets written, and the crop_ reads images from there.
 - 2021-07-20: Moved archive to separate script.
 - 2021-07-26: Added total AOT and cloud fraction image downloads from NASA GEOS model.
 - 2022-07-01: Major modification for the Cabo Verde forecasting
 - 2022-07-08: ECMWF, GFS, and ICON Global forecasting models
"""


from datetime import datetime, timedelta
import numpy as np
import os
import requests
import subprocess
import time

from bs4 import BeautifulSoup
from urllib import request, error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
#(ssl package is for ICAP aerosol downlaod)


readSwitches = True
downloadImages = True

model_day1 = model_day2 = False


forecastDir = './'
saveDir = './figs/'
cropDir = './figs_cropped/'
finDir = './figs_final/'



today = datetime.today()
#today = datetime.strptime('2021-07-18', '%Y-%m-%d')
today = today.replace(hour=0, minute=0, second=0, microsecond=0)
yesterday = today - timedelta(days=1)
forecast_day1 = today + timedelta(days=1)
forecast_day2 = today + timedelta(days=2)
nFrames_uwincm = 12
still_image_forecast_hr = 16
dust_xLon = 15 # 15 degrees N
dust_xLat = 20 # 20 degrees W
nDup_frames = 3

count_good_links = 0
count_bad_links = 0

pwd = os.getcwd()
if 'supplementary' in pwd:
  fl = open('./list_of_downloaded_files.txt', 'r')
else:
  fl = open('./supplementary/list_of_downloaded_files.txt', 'r')
wanted_files = fl.readlines()
wanted_files = [line.rstrip() for line in wanted_files]
fl.close()

all_files = [fl for fl in os.listdir(saveDir)]

need_to_download = [fl for fl in all_files if fl in wanted_files]





def downloadLink(imageUrl, imageName):
  """
  downloadLink (imageUrl, imageName)

  Will attempt to download the image located at imageUrl and save it at the provided imageName. If the image is not available, it will print out the message, and set a working variable to False, to avoid further processing.

  Parameters:
  - imageUrl: the url of the image attempting to download (e.g. https:// ...)
  - imageName: the complete path and name of the saved image (e.g. ./saveDir/imagename...)
  - working: returned Boolean that will determine if further processing should be done
  """
  try:
    request.urlretrieve(imageUrl, imageName)
    working = True
  except error.HTTPError:
    print('... ... Image currently not available.')
    working = False

  return working

def write_switch(switch_name, status, fl):
  """
  write_switch(switch_name, status, fl)

  Based on what files this script is able to download, it writes the True/False switches for the cropping script.

  Parameters:
  - switch_name: name of the switch (e.g. nhc_analysis)
  - status: a list of true/false values on whether it was able to download
  - fl: open file to write into.
  """

  if sum(status) > 0:
    fl.write(switch_name + ' = True \n')
  elif sum(status) == 0:
    fl.write(switch_name + ' = False \n')


  return




if readSwitches:
  print("Reading True/False switches from switches_download.txt")
  if 'supplementary' in pwd:
    fl = open('./switches_download.txt', 'r')
  else:
    fl = open(forecastDir + '/supplementary/switches_download.txt', 'r')
  data = fl.readlines()
  fl.close()
  data = [line.rstrip() for line in data]

  switches = {}
  for line in data:
    if len(line) > 0:
      switch_name, switch_setting = line.split(' = ')

      if switch_setting == 'True':
        switches[switch_name] = True
      elif switch_setting == 'False':
        switches[switch_name] = False

  if 'supplementary' in pwd:
    fl_switch = open('./switches_process.txt', 'w')
  else:
    fl_switch = open(forecastDir + '/supplementary/switches_process.txt', 'w')


  print("Reading True/False switches complete.")


print('')
print('')
print('')
print('')
print('')

if downloadImages:
  print("Downloading images for today's forecast.")

  # NHC Analysis and Tropical Weather Outlook
  if switches['nhc_analysis']:
    print('... Downloading NHC surface analysis.')
    status = []

    url = 'https://www.nhc.noaa.gov/tafb_latest/USA_latest.gif'
    dl = downloadLink(url, saveDir + 'NHC_surface_analysis.gif')
    count_good_links += dl
    count_bad_links += (1 - dl)
    status.append(dl)

    if dl:
      print('    ... Converting .gif image to .png image.')
      cmd = ['convert',  '-coalesce', saveDir + 'NHC_surface_analysis.gif', saveDir + 'NHC_surface_analysis.png']
      subprocess.call(cmd)

    print('... Downloading NHC tropical weather 2-day outlook.')

    url = 'https://www.nhc.noaa.gov/xgtwo/two_atl_2d0.png'
    dl = downloadLink(url, saveDir + 'NHC_2day_outlook.png')
    count_good_links += dl
    count_bad_links += (1 - dl)
    status.append(dl)

    print('... Downloading NHC tropical weather 5-day outlook.')

    url = 'https://www.nhc.noaa.gov/xgtwo/two_atl_5d0.png'
    dl = downloadLink(url, saveDir + 'NHC_5day_outlook.png')
    count_good_links += dl
    count_bad_links += (1 - dl)
    status.append(dl)

    write_switch('nhc_analysis', status, fl_switch)

  # MIMIC-Total Precipitable Water
  if switches['mimic_tpw']:
    print('... Downloading MIMIC-TPW total precipitable water animation.')
    status = []

    url = 'http://tropic.ssec.wisc.edu/real-time/mtpw2/webAnims/tpw_nrl_colors/natl/mimictpw_natl_latest.gif'
    dl = downloadLink(url, saveDir + 'MIMIC-TPW_24h_animation.gif')
    count_good_links += dl
    count_bad_links += (1 - dl)
    status.append(dl)

    print('    ... Converting .gif animation to .png sequence of images.')

    if dl:
      cmd = ['convert',  '-coalesce', saveDir + 'MIMIC-TPW_24h_animation.gif', saveDir + 'MIMIC-TPW_24h_animation.png']
      subprocess.call(cmd)

      print('    ... Finding the latest image and setting it to _latest.')
      fls = [fl for fl in os.listdir(saveDir) if 'MIMIC-TPW' in fl and '.png' in fl]
      fls = [fl for fl in fls if 'MIMIC-TPW_24h_animation' in fl]
      frame_number = [int(fl.split('-')[-1][:-4]) for fl in fls]
      latest_frame = fls[0][:24] + str(max(frame_number)) + '.png'
      cmd = ['cp', saveDir+latest_frame, saveDir+'MIMIC-TPW_latest.png']
      subprocess.call(cmd)

    write_switch('mimic_tpw', status, fl_switch)

  # GOES-16 satellite imagery - Bedka group
  if switches['GOES16_sat']:
    print('... Downloading GOES16 visible satellite imagery.')
    status = []

    url = 'https://satcorps.larc.nasa.gov/prod/exp/cpex-aw-2020/satpng/g16/latest/G16.LATEST.01KM.HVIS.PNG'
    dl = downloadLink(url, saveDir + 'Goes16_VIS.png')
    count_good_links += dl
    count_bad_links += (1 - dl)
    status.append(dl)

    print('... Downloading GOES16 RGB satellite imagery.')
    url = 'https://satcorps.larc.nasa.gov/prod/exp/cpex-aw-2020/satpng/g16/latest/G16.LATEST.02KM.RGB.PNG'
    dl = downloadLink(url, saveDir + 'Goes16_RGB.png')
    count_good_links += dl
    count_bad_links += (1 - dl)
    status.append(dl)

    print('... Downloading GOES16 IRC satellite imagery.')
    url = 'https://satcorps.larc.nasa.gov/prod/exp/cpex-aw-2020/satpng/g16/latest/G16.LATEST.02KM.IRC.PNG'
    dl = downloadLink(url, saveDir + 'Goes16_IRC.png')
    count_good_links += dl
    count_bad_links += (1 - dl)
    status.append(dl)

    write_switch('GOES16_sat', status, fl_switch)

  # METEOSAT-11 satellite imagery - Bedka group
  if switches['meteosat_sat']:
    print('... Downloading Meteosat-11 visible satellite imagery.')
    status = []

    url = 'https://satcorps.larc.nasa.gov/prod/exp/cpex-aw-2020/satpng/met/latest/M11.LATEST.03KM.VIS.PNG'
    dl = downloadLink(url, saveDir + 'Meteosat11_VIS.png')
    count_good_links += dl
    count_bad_links += (1 - dl)
    status.append(dl)

    print('... Downloading Meteosat-11 IRC satellite imagery.')
    url = 'https://satcorps.larc.nasa.gov/prod/exp/cpex-aw-2020/satpng/met/latest/M11.LATEST.03KM.IRC.PNG'
    dl = downloadLink(url, saveDir + 'Meteosat11_IRC.png')
    count_good_links += dl
    count_bad_links += (1 - dl)
    status.append(dl)


    write_switch('meteosat_sat', status, fl_switch)

  # Alan Brammer's tropical wave tracking
  if switches['brammer_tropical_waves']:
    print("... Downloading AEW analysis from Alan Brammer's Website")
    status = []

    init_date = datetime.strptime('2013-01-01', '%Y-%m-%d')
    time_diff = int(np.ceil((today-init_date).total_seconds()/3600))


    url = 'http://www.atmos.albany.edu/student/abrammer/graphics/gfs_realtime/plots/prate_sf_mslp/ea_prate_sf_mslp_' + str(time_diff) + '.0.jpg'
    dl = downloadLink(url, saveDir + 'AEW_Brammer.jpg')
    if not dl:
      time_diff += 6
      url = 'http://www.atmos.albany.edu/student/abrammer/graphics/gfs_realtime/plots/prate_sf_mslp/ea_prate_sf_mslp_' + str(time_diff) + '.0.jpg'
      print('    ... Trying a different time.')
      dl = downloadLink(url, saveDir + 'AEW_Brammer.jpg')


    count_good_links += dl
    count_bad_links += (1 - dl)
    status.append(dl)

    write_switch('brammer_tropical_waves', status, fl_switch)

  # Saharan Air Layer - Split Window GOES-16
  if switches['sal_split']:
    print("... Downloading dry air and dust image from CIMSS (split window).")
    status = []

    url = 'http://tropic.ssec.wisc.edu/real-time/sal/g16split/g16split.jpg'
    dl = downloadLink(url, saveDir + 'SAL_dryAir_split.jpg')
    count_good_links += dl
    count_bad_links += (1 - dl)
    status.append(dl)

    write_switch('sal_split', status, fl_switch)


  # # # MODEL STUFF NOW - SINGLE IMAGES
  if switches['uwincm_clouds_current']:
    print("... Downloading UWINCM cloud maps at forecast making time (16Z on current day).")
    status = []
    url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/storm/pw_olr/pw_olr.storm.' +  today.strftime('%Y%m%d') + '16.jpg'
    dl = downloadLink(url, saveDir + 'uwincm_clouds_current.jpg')
    count_good_links += dl
    count_bad_links += (1 - dl)
    status.append(dl)

    write_switch('uwincm_clouds_current', status, fl_switch)

  if switches['uwincm_surfaceWind']:
    status = []
    if model_day1:
      print("... Downloading UWINCM surface wind map - single - for model day 1.")
      url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/large/windsfc/wspd.large.' +  forecast_day1.strftime('%Y%m%d') + '{:02d}'.format(still_image_forecast_hr) + '.jpg'
      dl = downloadLink(url, saveDir + 'uwincm_surfaceWind_day1.jpg')
      count_good_links += dl
      count_bad_links += (1 - dl)
      status.append(dl)

    if model_day2:
      print("... Downloading UWINCM surface wind map - single -  for model day 2.")
      url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/large/windsfc/wspd.large.' +  forecast_day2.strftime('%Y%m%d') + '{:02d}'.format(still_image_forecast_hr) + '.jpg'
      dl = downloadLink(url, saveDir + 'uwincm_surfaceWind_day2.jpg')
      count_good_links += dl
      count_bad_links += (1 - dl)
      status.append(dl)


    write_switch('uwincm_surfaceWind', status, fl_switch)

  if switches['uwincm_650mbRH']:
    status = []
    if model_day1:
      print("... Downloading UWINCM 650mb moisture map - single - for model day 1.")
      url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/large/rh650mb/650mb_rh.large.' +  forecast_day1.strftime('%Y%m%d') + '{:02d}'.format(still_image_forecast_hr) + '.jpg'
      dl = downloadLink(url, saveDir + 'uwincm_650mbRH_day1.jpg')
      count_good_links += dl
      count_bad_links += (1 - dl)
      status.append(dl)

    if model_day2:
      print("... Downloading UWINCM 650mb moisture map - single - for model day 2.")
      url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/large/rh650mb/650mb_rh.large.' +  forecast_day2.strftime('%Y%m%d') + '{:02d}'.format(still_image_forecast_hr) + '.jpg'
      dl = downloadLink(url, saveDir + 'uwincm_650mbRH_day2.jpg')
      count_good_links += dl
      count_bad_links += (1 - dl)
      status.append(dl)

    write_switch('uwincm_650mbRH', status, fl_switch)

  if switches['uwincm_clouds']:
    status = []
    if model_day1:
      print("... Downloading UWINCM cloud map - single - for model day 1.")
      url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/storm/pw_olr/pw_olr.storm.' +  forecast_day1.strftime('%Y%m%d') + '{:02d}'.format(still_image_forecast_hr) + '.jpg'
      dl = downloadLink(url, saveDir + 'uwincm_clouds_day1.jpg')
      count_good_links += dl
      count_bad_links += (1 - dl)
      status.append(dl)

    if model_day2:
      print("... Downloading UWINCM cloud map - single - for model day 2.")
      url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/storm/pw_olr/pw_olr.storm.' +  forecast_day2.strftime('%Y%m%d') + '{:02d}'.format(still_image_forecast_hr) + '.jpg'
      dl = downloadLink(url, saveDir + 'uwincm_clouds_day2.jpg')
      count_good_links += dl
      count_bad_links += (1 - dl)
      status.append(dl)

    write_switch('uwincm_clouds', status, fl_switch)

  if switches['uwincm_precipitation']:
    status = []
    if model_day1:
      print("... Downloading UWINCM precipitation map - single - for model day 1.")
      url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/storm/rr_slp/rainr.storm.' +  forecast_day1.strftime('%Y%m%d') + '{:02d}'.format(still_image_forecast_hr) + '.jpg'
      dl = downloadLink(url, saveDir + 'uwincm_precip_day1.jpg')
      count_good_links += dl
      count_bad_links += (1 - dl)
      status.append(dl)

    if model_day2:
      print("... Downloading UWINCM precipitation map - single - for model day 2.")
      url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/storm/rr_slp/rainr.storm.' +  forecast_day2.strftime('%Y%m%d') + '{:02d}'.format(still_image_forecast_hr) + '.jpg'
      dl = downloadLink(url, saveDir + 'uwincm_precip_day2.jpg')
      count_good_links += dl
      count_bad_links += (1 - dl)
      status.append(dl)

    write_switch('uwincm_precipitation', status, fl_switch)

  if switches['uwincm_boundaryLayer']:
    status = []
    if model_day1:
      print("... Downloading UWINCM boundary layer map - single - for model day 1.")
      url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/storm/blh/blh.storm.' +  forecast_day1.strftime('%Y%m%d') + '{:02d}'.format(still_image_forecast_hr) + '.jpg'
      dl = downloadLink(url, saveDir + 'uwincm_boundaryLayer_day1.jpg')
      count_good_links += dl
      count_bad_links += (1 - dl)
      status.append(dl)

    if model_day2:
      print("... Downloading UWINCM boundary layer map - single - for model day 2.")
      url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/storm/blh/blh.storm.' +  forecast_day2.strftime('%Y%m%d') + '{:02d}'.format(still_image_forecast_hr) + '.jpg'
      dl = downloadLink(url, saveDir + 'uwincm_boundaryLayer_day2.jpg')
      count_good_links += dl
      count_bad_links += (1 - dl)
      status.append(dl)

    write_switch('uwincm_boundaryLayer', status, fl_switch)

  if switches['uutah_precipitation']:
    status = []
    if model_day1:
      print("... Downloading UofUtah model precipitation map - single - for model day 1.")
      url = 'https://orca.atmos.washington.edu/model_images/atl/uutah/realtime/' + today.strftime('%Y%m%d') + '00/gfs/storm/rr_slp/slp_rain-' +  forecast_day1.strftime('%Y-%m-%d') + '_' + '{:02d}'.format(still_image_forecast_hr) + ':00:00_d02.png'
      dl = downloadLink(url, saveDir + 'uutah_precip_day1.jpg')
      count_good_links += dl
      count_bad_links += (1 - dl)
      status.append(dl)

    if model_day2:
      print("... Downloading UofUtah model precipitation map - single - for model day 2.")
      url = 'https://orca.atmos.washington.edu/model_images/atl/uutah/realtime/' + today.strftime('%Y%m%d') + '00/gfs/storm/rr_slp/slp_rain-' +  forecast_day2.strftime('%Y-%m-%d') + '_' + '{:02d}'.format(still_image_forecast_hr) + ':00:00_d02.png'
      dl = downloadLink(url, saveDir + 'uutah_precip_day2.jpg')
      count_good_links += dl
      count_bad_links += (1 - dl)
      status.append(dl)

    write_switch('uutah_precipitation', status, fl_switch)


  # # # MODEL STUFF NOW - ANIMATIONS
  if switches['uwincm_surfaceWind_animation']:
    status = []
    if model_day1:
      print("... Downloading UWINCM surface wind map - animation - for model day 1.")
      for frame in range(nFrames_uwincm):
        url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/large/windsfc/wspd.large.' +  (forecast_day1+timedelta(hours=1) + timedelta(hours=2*frame)).strftime('%Y%m%d%H') + '.jpg'
        dl = downloadLink(url, saveDir + 'uwincm_surfaceWind_day1_anim_' + '{:02d}'.format(frame) + '.jpg')
        count_good_links += dl
        count_bad_links += (1 - dl)
        status.append(dl)

    if model_day2:
      print("... Downloading UWINCM surface wind map - animation - for model day 2.")
      for frame in range(nFrames_uwincm):
        url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/large/windsfc/wspd.large.' +  (forecast_day2+timedelta(hours=1) + timedelta(hours=2*frame)).strftime('%Y%m%d%H') + '.jpg'
        dl = downloadLink(url, saveDir + 'uwincm_surfaceWind_day2_anim_' + '{:02d}'.format(frame) + '.jpg')
        count_good_links += dl
        count_bad_links += (1 - dl)
        status.append(dl)

    write_switch('uwincm_surfaceWind_animation', status, fl_switch)

  if switches['uwincm_650mbRH_animation']:
    status = []
    if model_day1:
      print("... Downloading UWINCM 650mb moisture map - animation - for model day 1.")
      for frame in range(nFrames_uwincm):
        url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/large/rh650mb/650mb_rh.large.' +  (forecast_day1+timedelta(hours=1) + timedelta(hours=2*frame)).strftime('%Y%m%d%H') + '.jpg'
        dl = downloadLink(url, saveDir + 'uwincm_650mbRH_day1_anim_' + '{:02d}'.format(frame) + '.jpg')
        count_good_links += dl
        count_bad_links += (1 - dl)
        status.append(dl)

    if model_day2:
      print("... Downloading UWINCM 650mb moisture map - animation - for model day 2.")
      for frame in range(nFrames_uwincm):
        url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/large/rh650mb/650mb_rh.large.' +  (forecast_day2+timedelta(hours=1) + timedelta(hours=2*frame)).strftime('%Y%m%d%H') + '.jpg'
        dl = downloadLink(url, saveDir + 'uwincm_650mbRH_day2_anim_' + '{:02d}'.format(frame) + '.jpg')
        count_good_links += dl
        count_bad_links += (1 - dl)
        status.append(dl)

    write_switch('uwincm_650mbRH_animation', status, fl_switch)

  if switches['uwincm_clouds_animation']:
    status = []
    if model_day1:
      print("... Downloading UWINCM cloud map - animation - for model day 1.")
      for frame in range(nFrames_uwincm):
        url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/storm/pw_olr/pw_olr.storm.' +  (forecast_day1+timedelta(hours=1) + timedelta(hours=2*frame)).strftime('%Y%m%d%H') + '.jpg'
        dl = downloadLink(url, saveDir + 'uwincm_clouds_day1_anim_' + '{:02d}'.format(frame) + '.jpg')
        count_good_links += dl
        count_bad_links += (1 - dl)
        status.append(dl)

    if model_day2:
      print("... Downloading UWINCM cloud map - animation - for model day 2.")
      for frame in range(nFrames_uwincm):
        url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/storm/pw_olr/pw_olr.storm.' +  (forecast_day2+timedelta(hours=1) + timedelta(hours=2*frame)).strftime('%Y%m%d%H') + '.jpg'
        dl = downloadLink(url, saveDir + 'uwincm_clouds_day2_anim_' + '{:02d}'.format(frame) + '.jpg')
        count_good_links += dl
        count_bad_links += (1 - dl)
        status.append(dl)

    write_switch('uwincm_clouds_animation', status, fl_switch)

  if switches['uwincm_precipitation_animation']:
    status = []
    if model_day1:
      print("... Downloading UWINCM precipitation map - animation - for model day 1.")
      for frame in range(nFrames_uwincm):
        url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/storm/rr_slp/rainr.storm.' +  (forecast_day1+timedelta(hours=1) + timedelta(hours=2*frame)).strftime('%Y%m%d%H') + '.jpg'
        dl = downloadLink(url, saveDir + 'uwincm_precip_day1_anim_' + '{:02d}'.format(frame) + '.jpg')
        count_good_links += dl
        count_bad_links += (1 - dl)
        status.append(dl)


    if model_day2:
      print("... Downloading UWINCM precipitation map - animation - for model day 2.")
      for frame in range(nFrames_uwincm):
        url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/storm/rr_slp/rainr.storm.' +  (forecast_day2+timedelta(hours=1) + timedelta(hours=2*frame)).strftime('%Y%m%d%H') + '.jpg'
        dl = downloadLink(url, saveDir + 'uwincm_precip_day2_anim_' + '{:02d}'.format(frame) + '.jpg')
        count_good_links += dl
        count_bad_links += (1 - dl)
        status.append(dl)

    write_switch('uwincm_precipitation_animation', status, fl_switch)

  if switches['uwincm_boundaryLayer_animation']:
    status = []
    if model_day1:
      print("... Downloading UWINCM boundary layer map - animation - for model day 1.")
      for frame in range(nFrames_uwincm):
        url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/storm/blh/blh.storm.' +  (forecast_day1+timedelta(hours=1) + timedelta(hours=2*frame)).strftime('%Y%m%d%H') + '.jpg'
        dl = downloadLink(url, saveDir + 'uwincm_boundaryLayer_day1_anim_' + '{:02d}'.format(frame) + '.jpg')
        count_good_links += dl
        count_bad_links += (1 - dl)
        status.append(dl)

    if model_day2:
      print("... Downloading UWINCM boundary layer map - animation - for model day 2.")
      for frame in range(nFrames_uwincm):
        url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/storm/blh/blh.storm.' +  (forecast_day2+timedelta(hours=1) + timedelta(hours=2*frame)).strftime('%Y%m%d%H') + '.jpg'
        dl = downloadLink(url, saveDir + 'uwincm_boundaryLayer_day2_anim_' + '{:02d}'.format(frame) + '.jpg')
        count_good_links += dl
        count_bad_links += (1 - dl)
        status.append(dl)

    write_switch('uwincm_boundaryLayer_animation', status, fl_switch)

  if switches['uutah_precipitation_animation']:
    status = []
    if model_day1:
      print("... Downloading UofUtah model precipitation map - animation - for model day 1.")
      for frame in range(nFrames_uwincm):
        url = 'https://orca.atmos.washington.edu/model_images/atl/uutah/realtime/' + today.strftime('%Y%m%d') + '00/gfs/storm/rr_slp/slp_rain-' +  (forecast_day1+timedelta(hours=1) + timedelta(hours=2*frame)).strftime('%Y-%m-%d_%H:%M:%S') + '_d02.png'
        dl = downloadLink(url, saveDir + 'uutah_precip_day1_anim_' + '{:02d}'.format(frame) + '.png')
        count_good_links += dl
        count_bad_links += (1 - dl)
        status.append(dl)

    if model_day2:
      print("... Downloading UofUtah model precipitation map - animation - for model day 2.")
      for frame in range(nFrames_uwincm):
        url = 'https://orca.atmos.washington.edu/model_images/atl/uutah/realtime/' + today.strftime('%Y%m%d') + '00/gfs/storm/rr_slp/slp_rain-' +  (forecast_day2+timedelta(hours=1) + timedelta(hours=2*frame)).strftime('%Y-%m-%d_%H:%M:%S') + '_d02.png'
        dl = downloadLink(url, saveDir + 'uutah_precip_day2_anim_' + '{:02d}'.format(frame) + '.png')
        count_good_links += dl
        count_bad_links += (1 - dl)
        status.append(dl)

    write_switch('uutah_precipitation_animation', status, fl_switch)

  # NOW BACK TO OBSERVATIONS - ICAP
  if switches['icap_aerosol_ensemble']:
    print("... Downloading ICAP AOT ensemble mean maps for day 3.")
    status = []

    url_base = 'https://www.nrlmry.navy.mil/aerosol/globaer/icap_01/subtropatl/' + (today-timedelta(days=1)).strftime('%Y%m%d') + '00/' + (today-timedelta(days=1)).strftime('%Y%m%d') + '00_'
    days = [4, 5]
    download_days = [((today-timedelta(days=1)) + timedelta(days=dy)).strftime('%Y%m%d%H') for dy in days]

    dTime = int((datetime.strptime(download_days[0], '%Y%m%d%H') - (today-timedelta(days=1))).total_seconds()/3600)
    url = url_base + download_days[0] + '_f' + '{:03d}'.format(dTime) + '_total_aod_550_subtropatl_icap.png'

    dl = downloadLink(url, saveDir + 'ICAP_aerosol_ensemble_' + str(dTime) + '.png')
    count_good_links += dl
    count_bad_links += (1 - dl)
    status.append(dl)


    print("... Downloading ICAP AOT ensemble mean maps for day 5.")
    dTime = int((datetime.strptime(download_days[1], '%Y%m%d%H') - (today-timedelta(days=1))).total_seconds()/3600)
    url = url_base + download_days[1] + '_f' + '{:03d}'.format(dTime) + '_total_aod_550_subtropatl_icap.png'

    dl = downloadLink(url, saveDir + 'ICAP_aerosol_ensemble_' + str(dTime) + '.png')
    count_good_links += dl
    count_bad_links += (1 - dl)
    status.append(dl)

    write_switch('icap_aerosol_ensemble', status, fl_switch)

  if switches['UTAH_dryrun']:
   var=['sfcwind','rhght650','tpw_olr','PBLH','slp_rain']
   for vv in var:
    if vv == 'PBLH' or vv == 'slp_rain':
        dd = 'd02'
    else:
        dd = 'd01'
    print("... Downloading UofUtah model "+ vv + " map - animation")
    if vv == 'slp_rain':
      for frame in range(7):
        url = 'https://home.chpc.utah.edu/~pu/cpexaw/png/' + today.strftime('%Y-%m-%d') + '_00/' + vv + '-' + (forecast_day1+timedelta(hours=3) + timedelta(hours=3*frame)).strftime('%Y-%m-%d_%H:%M:%S') + '_'+dd+'.png'
        dl = downloadLink(url, saveDir + 'uutah_'+vv+'_day1_anim_' + '{:02d}'.format(frame) + '.png')
        url = 'https://home.chpc.utah.edu/~pu/cpexaw/png/' + today.strftime('%Y-%m-%d') + '_00/' + vv + '-' + (forecast_day2+timedelta(hours=3) + timedelta(hours=3*frame)).strftime('%Y-%m-%d_%H:%M:%S') + '_'+dd+'.png'
        dl = downloadLink(url, saveDir + 'uutah_'+vv+'_day2_anim_' + '{:02d}'.format(frame) + '.png')
        count_good_links += dl
        count_bad_links += (1 - dl)
        status.append(dl)
    else:
      for frame in range(nFrames_uwincm):
        url = 'https://home.chpc.utah.edu/~pu/cpexaw/png/' + today.strftime('%Y-%m-%d') + '_00/' + vv + '-' + (forecast_day1+timedelta(hours=1) + timedelta(hours=2*frame)).strftime('%Y-%m-%d_%H:%M:%S') + '_'+dd+'.png'
        dl = downloadLink(url, saveDir + 'uutah_'+vv+'_day1_anim_' + '{:02d}'.format(frame) + '.png')
        url = 'https://home.chpc.utah.edu/~pu/cpexaw/png/' + today.strftime('%Y-%m-%d') + '_00/' + vv + '-' + (forecast_day2+timedelta(hours=1) + timedelta(hours=2*frame)).strftime('%Y-%m-%d_%H:%M:%S') + '_'+dd+'.png'
        dl = downloadLink(url, saveDir + 'uutah_'+vv+'_day2_anim_' + '{:02d}'.format(frame) + '.png')
        count_good_links += dl
        count_bad_links += (1 - dl)
        status.append(dl)
   write_switch('UTAH_dryrun', status, fl_switch)

  if switches['ECMWF_prediction']:
    ECMWF_files=[]
    for num in range(57): #57
      ECMWF_files.append('anim_'+"{:02d}".format(num)+'.png')

    var = ['mslp_wind','midRH','mslp_pwat','mslp_pcpn']
    for vv in var:
      print('... Downloading ECMWF -',vv)
      for idx, tau in enumerate(ECMWF_files):
        status = []
    #https://www.tropicaltidbits.com/analysis/models/ecmwf/2022071106/ecmwf_mslp_pwat_atl_1.png
    # -----  00Z initialization simulations
        url_base = 'https://www.tropicaltidbits.com/analysis/models/ecmwf/' + (today).strftime('%Y%m%d')+'00/ecmwf_'

        if vv == 'mslp_pcpn':
            if idx > 0: dl = downloadLink(url_base+vv+'_atl_'+str(idx)+'.png', saveDir + 'ECMWF_'+vv+'_'+ECMWF_files[idx])
        else:
            dl = downloadLink(url_base+vv+'_atl_'+str(idx+1)+'.png', saveDir + 'ECMWF_'+vv+'_'+ECMWF_files[idx])

        count_good_links += dl
        count_bad_links += (1 - dl)
        status.append(dl)
    write_switch('ECMWF_prediction', status, fl_switch)

  if switches['GFS_prediction']:
    GFS_files=[]
    for num in range(29):
      GFS_files.append('anim_'+"{:02d}".format(num)+'.png')

    var = ['mslp_wind','midRH','mslp_pwat','mslp_pcpn']
    for vv in var:
      print('... Downloading GFS -',vv)
      for idx, tau in enumerate(GFS_files):
        status = []
    # -----  00Z initialization simulations
        url_base = 'https://www.tropicaltidbits.com/analysis/models/gfs/' + (today).strftime('%Y%m%d')+'00/gfs_'

        if vv == 'mslp_pcpn':
            if idx > 0: dl = downloadLink(url_base+vv+'_atl_'+str(idx)+'.png', saveDir + 'GFS_'+vv+'_'+GFS_files[idx])
        else:
            dl = downloadLink(url_base+vv+'_atl_'+str(idx+1)+'.png', saveDir + 'GFS_'+vv+'_'+GFS_files[idx])
        count_good_links += dl
        count_bad_links += (1 - dl)
        status.append(dl)
    write_switch('GFS_prediction', status, fl_switch)

  if switches['ICON_prediction']:
    ICON_files=[]
    for num in range(29):
      ICON_files.append('anim_'+"{:02d}".format(num)+'.png')

    var = ['mslp_wind','mslp_pcpn']
    for vv in var:
      print('... Downloading ICON -',vv)
      for idx, tau in enumerate(ICON_files):
        status = []
    # -----  00Z initialization simulations
        url_base = 'https://www.tropicaltidbits.com/analysis/models/icon/' + (today).strftime('%Y%m%d')+'00/icon_'

        if vv == 'mslp_pcpn':
            if idx > 0: dl = downloadLink(url_base+vv+'_atl_'+str(idx)+'.png', saveDir + 'ICON_'+vv+'_'+ICON_files[idx])
        else:
            dl = downloadLink(url_base+vv+'_atl_'+str(idx+1)+'.png', saveDir + 'ICON_'+vv+'_'+ICON_files[idx])
        count_good_links += dl
        count_bad_links += (1 - dl)
        status.append(dl)
    write_switch('ICON_prediction', status, fl_switch)


  if switches['nasa_geos']:
    fInitialTime = today.strftime('%Y%m%d') + 'T000000'
    img_url_pattern = '/missions/static//plots/'
    req_timeout = 300 #seconds

    #=== Aerosol optical thickness config
    AOT_tau = ['000', '024', '048'] #Change tau to choose different lead hour

    AOT_url_prefix = 'https://fluid.nccs.nasa.gov/missions/chem2d_mission%2BPRDUST/?one_click=1&'
    AOT_url_suffix = '&stream=G5FPFC&level=0&region=prdust&fcst=' + fInitialTime

    AOT_img_2D_files = ['GEOS_dust_aot.png',
                        'GEOS_dust_aot_day1.png',
                        'GEOS_dust_aot_day2.png']

    AOT_img_total_files = ['GEOS_total_aot.png',
                           'GEOS_total_aot_day1.png',
                           'GEOS_total_aot_day2.png']

    AOT_img_lowcf_files = ['GEOS_lowCloudFraction.png',
                           'GEOS_lowCloudFraction_day1.png',
                           'GEOS_lowCloudFraction_day2.png']

    AOT_img_midcf_files = ['GEOS_midCloudFraction.png',
                           'GEOS_midCloudFraction_day1.png',
                           'GEOS_midCloudFraction_day2.png']

    AOT_img_highcf_files = ['GEOS_highCloudFraction.png',
                            'GEOS_highCloudFraction_day1.png',
                            'GEOS_highCloudFraction_day2.png']

    #lon cross section
    AOT_img_loncs_files = ['GEOS_dust_aot_vert_' + str(dust_xLon) + 'N.png',
                           'GEOS_dust_aot_day1_vert_' + str(dust_xLon) + 'N.png',
                           'GEOS_dust_aot_day2_vert_' + str(dust_xLon) + 'N.png']

    #lat cross section
    AOT_img_latcs_files = ['GEOS_dust_aot_vert_' + str(dust_xLat) + 'W.png',
                           'GEOS_dust_aot_day1_vert_' + str(dust_xLat) + 'W.png',
                           'GEOS_dust_aot_day2_vert_' + str(dust_xLat) + 'W.png']

    #=== 700mb wind & geopotential height config
    wind_700mb_tau = ['072', '078', '084', '090', '096', '102', '108', '114', '120', '126', '132', '138']

    wind_700mb_files = ['GEOS_700mb_outlook_anim_00.png',
                        'GEOS_700mb_outlook_anim_01.png',
                        'GEOS_700mb_outlook_anim_02.png',
                        'GEOS_700mb_outlook_anim_03.png',
                        'GEOS_700mb_outlook_anim_04.png',
                        'GEOS_700mb_outlook_anim_05.png',
                        'GEOS_700mb_outlook_anim_06.png',
                        'GEOS_700mb_outlook_anim_07.png',
                        'GEOS_700mb_outlook_anim_08.png',
                        'GEOS_700mb_outlook_anim_09.png',
                        'GEOS_700mb_outlook_anim_10.png',
                        'GEOS_700mb_outlook_anim_11.png']


    def find_geos_img_url(webpage,text_pattern,timeout):

      geos_domain = 'https://fluid.nccs.nasa.gov'
      response = request.urlopen(webpage,None,timeout)
      data = response.read()
      content = data.decode('utf8')
      parsedPage = BeautifulSoup(content,features='lxml')

      imgElms = parsedPage.findAll('img')

      img_url = -1
      for img in imgElms:
        result = str.find(img.attrs['src'],text_pattern)
        if result == 0:
          img_url = geos_domain + img.attrs['src']
          break
        elif result > 0:
          img_url  = img.attrs['src']
          break

      return img_url

    #Get AOT 2D image (dust only)
    print("... Downloading images from GEOS - Aerosol Opt. Thickness - Dust.")
    status = []

    for idx, tau in enumerate(AOT_tau):
      AOT_page = AOT_url_prefix + 'tau=' + tau + AOT_url_suffix + '&field=duaot'
      AOT_img_url = find_geos_img_url(AOT_page, img_url_pattern, req_timeout)

      dl = downloadLink(AOT_img_url, saveDir + AOT_img_2D_files[idx])
      count_good_links += dl
      count_bad_links += (1 - dl)
      status.append(dl)

    #Get AOT total image
    print("... Downloading images from GEOS - Aerosol Opt. Thickness - Total.")

    for idx, tau in enumerate(AOT_tau):
      AOT_page = AOT_url_prefix + 'tau=' + tau + AOT_url_suffix + '&field=totaot'
      AOT_img_url = find_geos_img_url(AOT_page, img_url_pattern, req_timeout)

      dl = downloadLink(AOT_img_url, saveDir + AOT_img_total_files[idx])
      count_good_links += dl
      count_bad_links += (1 - dl)
      status.append(dl)


    print("... Downloading images from GEOS - Low cloud fraction.")

    for idx, tau in enumerate(AOT_tau):
      cldfra_prefix = AOT_url_prefix.replace('chem2d_mission', 'weather_mission')
      cldfra_suffix = AOT_url_suffix
      cldfra_page = cldfra_prefix + 'tau=' + tau + cldfra_suffix + '&field=cldlow'
      cldfra_img_url = find_geos_img_url(cldfra_page, img_url_pattern, req_timeout)


      dl = downloadLink(cldfra_img_url, saveDir + AOT_img_lowcf_files[idx])
      count_good_links += dl
      count_bad_links += (1 - dl)
      status.append(dl)

    print("... Downloading images from GEOS - Middle cloud fraction.")

    for idx, tau in enumerate(AOT_tau):
      cldfra_prefix = AOT_url_prefix.replace('chem2d_mission', 'weather_mission')
      cldfra_suffix = AOT_url_suffix
      cldfra_page = cldfra_prefix + 'tau=' + tau + cldfra_suffix + '&field=cldmid'
      cldfra_img_url = find_geos_img_url(cldfra_page, img_url_pattern, req_timeout)


      dl = downloadLink(cldfra_img_url, saveDir + AOT_img_midcf_files[idx])
      count_good_links += dl
      count_bad_links += (1 - dl)
      status.append(dl)

    print("... Downloading images from GEOS - High cloud fraction.")

    for idx, tau in enumerate(AOT_tau):
      cldfra_prefix = AOT_url_prefix.replace('chem2d_mission', 'weather_mission')
      cldfra_suffix = AOT_url_suffix
      cldfra_page = cldfra_prefix + 'tau=' + tau + cldfra_suffix + '&field=cldhgh'
      cldfra_img_url = find_geos_img_url(cldfra_page, img_url_pattern, req_timeout)


      dl = downloadLink(cldfra_img_url, saveDir + AOT_img_highcf_files[idx])
      count_good_links += dl
      count_bad_links += (1 - dl)
      status.append(dl)



    #Get AOT longitudinal cross section
    print("... Downloading images from GEOS - Aerosol Opt. Thickness - Lon Cross section.")
    for idx, tau in enumerate(AOT_tau):
      AOT_page = AOT_url_prefix.replace('chem2d_mission', 'custom_mission')
      AOT_page =  AOT_page + 'tau=' + tau + AOT_url_suffix + '&field=du_w2'
      AOT_img_url = find_geos_img_url(AOT_page, img_url_pattern, req_timeout)

      dl = downloadLink(AOT_img_url, saveDir + AOT_img_loncs_files[idx])
      count_good_links += dl
      count_bad_links += (1 - dl)
      status.append(dl)

    #Get AOT latitudinal cross section image
    print("... Downloading images from GEOS - Aerosol Opt. Thickness - Lat Cross section.")
    for idx, tau in enumerate(AOT_tau):
      AOT_page = AOT_url_prefix.replace('chem2d_mission', 'custom_mission')
      AOT_page =  AOT_page + 'tau=' + tau + AOT_url_suffix + '&field=du_n1'
      AOT_img_url = find_geos_img_url(AOT_page, img_url_pattern, req_timeout)

      dl = downloadLink(AOT_img_url, saveDir + AOT_img_latcs_files[idx])
      count_good_links += dl
      count_bad_links += (1 - dl)
      status.append(dl)

    #Get 700 mb wind with geopotential heights
    print("... Downloading images from GEOS - 700 mb wind and Geopotential heights.")
    for idx, tau in enumerate(wind_700mb_tau):
      wind700mb_prefix = AOT_url_prefix.replace('chem2d_mission', 'weather_mission')
      wind700mb_suffix = AOT_url_suffix.replace('level=0','level=700')
      wind700mb_page = wind700mb_prefix + 'tau=' + tau + wind700mb_suffix + '&field=wspd'
      wind700m_img_url = find_geos_img_url(wind700mb_page, img_url_pattern, req_timeout)

      dl = downloadLink(wind700m_img_url, saveDir + wind_700mb_files[idx])
      count_good_links += dl
      count_bad_links += (1 - dl)
      status.append(dl)


    write_switch('nasa_geos', status, fl_switch)


  total_links = count_good_links + count_bad_links
  print("Downloading images for today's forecast complete.")
  print("There were a total of " + str(count_good_links) + "/" + str(total_links) + " good links (" + '{:.1f}'.format((count_good_links/total_links)*100) + '%).')
  fl_switch.close()


  time.sleep(10)
