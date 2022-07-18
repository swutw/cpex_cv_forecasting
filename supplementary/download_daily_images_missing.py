"""
Author: Ajda Savarin
Created: July 04th 2020
University of Washington
asavarin@uw.edu

This program is used to retrieve images for the CPEX-AW field campaign forecasting template.

Required packages: datetime, numpy, os, subprocess, requests, bs4, urllib.


Updates:
 - 2020-07-07: Created separate strings for downloading UWIN-CM model day 1 and day 2
 - 2020-07-12: Updated the NASA GEOS image section to call Mani's script and creates animation of NASA GEOS images. Also downloads day1, day2 model images at still_image_forecast_hr (set to 17UTC -- about mid-flight).
 - 2021-07-13: Added the NHC's tropical weather outlook for 2 and 5 days. Updated the GOES-E satellite to download the tropical atlantic region from the NOAA website. Also added the latest meteosat images to be downloaded for CV. Alan Brammer's website is no longer available -- we will reach out to see if that can be brought back.
 - 2021-07-15: Animations now span the entire model day (every other hour starting at 01 UTC), instead of only from 11UTC onward.
 - 2021-07-19: Updated availability printouts and accuracy of print statements. Created a new directory where the final figures will be moved to (figs_final). Split a section off to a new script - create animations.py. Moving switches to a new file - switches_download.txt; As images are downloaded, switches_process.txt gets written, and the crop_ reads images from there.
 - 2021-07-20: Moved archive to separate script. Downloads only the missing images.
 - 2021-07-26: Added total AOT and cloud fraction image downloads from NASA GEOS model.
"""


from datetime import datetime, timedelta
import numpy as np
import os
import requests
import subprocess
import time

from bs4 import BeautifulSoup
from urllib import request, error



readSwitches = True
downloadImages = True

model_day1 = model_day2 = True


forecastDir = './'
saveDir = './figs/'
cropDir = './figs_cropped/'
finDir = './figs_final/'



today = datetime.today()
today = today.replace(hour=0, minute=0, second=0, microsecond=0)
yesterday = today - timedelta(days=1)
forecast_day1 = today + timedelta(days=1)
forecast_day2 = today + timedelta(days=2)
nFrames_uwincm = 12
still_image_forecast_hr = 16
dust_xLon = 15 # 15 degrees N
dust_xLat = 20 # 60 degrees W
nDup_frames = 3



fl = open('./supplementary/list_of_downloaded_files.txt', 'r')
wanted_files = fl.readlines()
wanted_files = [line.rstrip() for line in wanted_files]
fl.close()

present_files = [fl for fl in os.listdir(saveDir) if fl in wanted_files]

need_to_download = [fl for fl in wanted_files if not fl in present_files]

total_links = len(wanted_files)


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
    print('    ... ' + imageName[7:] + ' downloaded.')
    working = True
  except error.HTTPError:
    print('... ... ' + imageName[7:] + ' currently not available.')
    working = False

  return working

def write_switch(switch_name, fl):
  """
  write_switch(switch_name, fl)

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

def check_if_missing(imageUrl, imageName, imageDir=saveDir):
  """
  check_if_missing(imageName, imageDir=saveDir)

  Checks whether an image has already been downloaded or not.

  If yes, doesn't do anything.
  If no, it downloads the image (if available).

  Parameters:
  - imageUrl: url of the image to be downloaded if needed
  - imageName: name of the image
  - imageDir: directory where image is saved
  """
  if os.path.isfile(imageDir+imageName):
    existed_before = True
  else:
    dl = downloadLink(imageUrl, imageDir+imageName)
    existed_before = False

  return existed_before


if readSwitches:
  print("Reading True/False switches from switches_download.txt")
  fl = open(forecastDir + 'supplementary/switches_download.txt', 'r')
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


  print("Reading True/False switches complete.")

  print('')
  print('')
  print('')
  print('')
  print('')


switch_dict = {'mimic_tpw': ['MIMIC-TPW_24h_animation.gif'],
               'nhc_analysis': ['NHC_surface_analysis.gif', 'NHC_2day_outlook.png', 'NHC_5day_outlook.png'],
               'GOES16_sat': ['Goes16_VIS.png', 'Goes16_RGB.png', 'Goes16_IRC.png'],
               'meteosat_sat': ['Meteosat11_VIS.png', 'Meteosat11_IRC.png'],
               'brammer_tropical_waves': ['AEW_Brammer.jpg'],
               'sal_split': ['SAL_dryAir_split.jpg'],
               'uwincm_clouds_current': ['uwincm_clouds_current.jpg'],
               'uwincm_surfaceWind': ['uwincm_surfaceWind_day1.jpg', 'uwincm_surfaceWind_day2.jpg'],
               'uwincm_650mbRH': ['uwincm_650mbRH_day1.jpg', 'uwincm_650mbRH_day2.jpg'],
               'uwincm_clouds': ['uwincm_clouds_day1.jpg', 'uwincm_clouds_day2.jpg'],
               'uwincm_precipitation': ['uwincm_precip_day1.jpg', 'uwincm_precip_day2.jpg'],
               'uwincm_boundaryLayer': ['uwincm_boundaryLayer_day1.jpg', 'uwincm_boundaryLayer_day2.jpg'],
               'uutah_precipitation': ['uutah_precip_day1.jpg', 'uutah_precip_day2.jpg'],
               'uwincm_surfaceWind_animation': ['uwincm_surfaceWind_day1_anim_00.jpg', 'uwincm_surfaceWind_day1_anim_01.jpg', 'uwincm_surfaceWind_day1_anim_02.jpg', 'uwincm_surfaceWind_day1_anim_03.jpg', 'uwincm_surfaceWind_day1_anim_04.jpg', 'uwincm_surfaceWind_day1_anim_05.jpg', 'uwincm_surfaceWind_day1_anim_06.jpg', 'uwincm_surfaceWind_day1_anim_07.jpg', 'uwincm_surfaceWind_day1_anim_08.jpg', 'uwincm_surfaceWind_day1_anim_09.jpg', 'uwincm_surfaceWind_day1_anim_10.jpg', 'uwincm_surfaceWind_day1_anim_11.jpg', 'uwincm_surfaceWind_day2_anim_00.jpg', 'uwincm_surfaceWind_day2_anim_01.jpg', 'uwincm_surfaceWind_day2_anim_02.jpg', 'uwincm_surfaceWind_day2_anim_03.jpg', 'uwincm_surfaceWind_day2_anim_04.jpg', 'uwincm_surfaceWind_day2_anim_05.jpg', 'uwincm_surfaceWind_day2_anim_06.jpg', 'uwincm_surfaceWind_day2_anim_07.jpg', 'uwincm_surfaceWind_day2_anim_08.jpg', 'uwincm_surfaceWind_day2_anim_09.jpg', 'uwincm_surfaceWind_day2_anim_10.jpg', 'uwincm_surfaceWind_day2_anim_11.jpg'],
               'uwincm_650mbRH_animation': ['uwincm_650mbRH_day1_anim_00.jpg', 'uwincm_650mbRH_day1_anim_01.jpg', 'uwincm_650mbRH_day1_anim_02.jpg', 'uwincm_650mbRH_day1_anim_03.jpg', 'uwincm_650mbRH_day1_anim_04.jpg', 'uwincm_650mbRH_day1_anim_05.jpg', 'uwincm_650mbRH_day1_anim_06.jpg', 'uwincm_650mbRH_day1_anim_07.jpg', 'uwincm_650mbRH_day1_anim_08.jpg', 'uwincm_650mbRH_day1_anim_09.jpg', 'uwincm_650mbRH_day1_anim_10.jpg', 'uwincm_650mbRH_day1_anim_11.jpg', 'uwincm_650mbRH_day2_anim_00.jpg', 'uwincm_650mbRH_day2_anim_01.jpg', 'uwincm_650mbRH_day2_anim_02.jpg', 'uwincm_650mbRH_day2_anim_03.jpg', 'uwincm_650mbRH_day2_anim_04.jpg', 'uwincm_650mbRH_day2_anim_05.jpg', 'uwincm_650mbRH_day2_anim_06.jpg', 'uwincm_650mbRH_day2_anim_07.jpg', 'uwincm_650mbRH_day2_anim_08.jpg', 'uwincm_650mbRH_day2_anim_09.jpg', 'uwincm_650mbRH_day2_anim_10.jpg', 'uwincm_650mbRH_day2_anim_11.jpg'],
               'uwincm_clouds_animation': ['uwincm_clouds_day1_anim_00.jpg', 'uwincm_clouds_day1_anim_01.jpg', 'uwincm_clouds_day1_anim_02.jpg', 'uwincm_clouds_day1_anim_03.jpg', 'uwincm_clouds_day1_anim_04.jpg', 'uwincm_clouds_day1_anim_05.jpg', 'uwincm_clouds_day1_anim_06.jpg', 'uwincm_clouds_day1_anim_07.jpg', 'uwincm_clouds_day1_anim_08.jpg', 'uwincm_clouds_day1_anim_09.jpg', 'uwincm_clouds_day1_anim_10.jpg', 'uwincm_clouds_day1_anim_11.jpg', 'uwincm_clouds_day2_anim_00.jpg', 'uwincm_clouds_day2_anim_01.jpg', 'uwincm_clouds_day2_anim_02.jpg', 'uwincm_clouds_day2_anim_03.jpg', 'uwincm_clouds_day2_anim_04.jpg', 'uwincm_clouds_day2_anim_05.jpg', 'uwincm_clouds_day2_anim_06.jpg', 'uwincm_clouds_day2_anim_07.jpg', 'uwincm_clouds_day2_anim_08.jpg', 'uwincm_clouds_day2_anim_09.jpg', 'uwincm_clouds_day2_anim_10.jpg', 'uwincm_clouds_day2_anim_11.jpg'],
               'uwincm_precipitation_animation': ['uwincm_precip_day1_anim_00.jpg', 'uwincm_precip_day1_anim_01.jpg', 'uwincm_precip_day1_anim_02.jpg', 'uwincm_precip_day1_anim_03.jpg', 'uwincm_precip_day1_anim_04.jpg', 'uwincm_precip_day1_anim_05.jpg', 'uwincm_precip_day1_anim_06.jpg', 'uwincm_precip_day1_anim_07.jpg', 'uwincm_precip_day1_anim_08.jpg', 'uwincm_precip_day1_anim_09.jpg', 'uwincm_precip_day1_anim_10.jpg', 'uwincm_precip_day1_anim_11.jpg', 'uwincm_precip_day2_anim_00.jpg', 'uwincm_precip_day2_anim_01.jpg', 'uwincm_precip_day2_anim_02.jpg', 'uwincm_precip_day2_anim_03.jpg', 'uwincm_precip_day2_anim_04.jpg', 'uwincm_precip_day2_anim_05.jpg', 'uwincm_precip_day2_anim_06.jpg', 'uwincm_precip_day2_anim_07.jpg', 'uwincm_precip_day2_anim_08.jpg', 'uwincm_precip_day2_anim_09.jpg', 'uwincm_precip_day2_anim_10.jpg', 'uwincm_precip_day2_anim_11.jpg'],
               'uwincm_boundaryLayer_animation': ['uwincm_boundaryLayer_day1_anim_00.jpg', 'uwincm_boundaryLayer_day1_anim_01.jpg', 'uwincm_boundaryLayer_day1_anim_02.jpg', 'uwincm_boundaryLayer_day1_anim_03.jpg', 'uwincm_boundaryLayer_day1_anim_04.jpg', 'uwincm_boundaryLayer_day1_anim_05.jpg', 'uwincm_boundaryLayer_day1_anim_06.jpg', 'uwincm_boundaryLayer_day1_anim_07.jpg', 'uwincm_boundaryLayer_day1_anim_08.jpg', 'uwincm_boundaryLayer_day1_anim_09.jpg', 'uwincm_boundaryLayer_day1_anim_10.jpg', 'uwincm_boundaryLayer_day1_anim_11.jpg', 'uwincm_boundaryLayer_day2_anim_00.jpg', 'uwincm_boundaryLayer_day2_anim_01.jpg', 'uwincm_boundaryLayer_day2_anim_02.jpg', 'uwincm_boundaryLayer_day2_anim_03.jpg', 'uwincm_boundaryLayer_day2_anim_04.jpg', 'uwincm_boundaryLayer_day2_anim_05.jpg', 'uwincm_boundaryLayer_day2_anim_06.jpg', 'uwincm_boundaryLayer_day2_anim_07.jpg', 'uwincm_boundaryLayer_day2_anim_08.jpg', 'uwincm_boundaryLayer_day2_anim_09.jpg', 'uwincm_boundaryLayer_day2_anim_10.jpg', 'uwincm_boundaryLayer_day2_anim_11.jpg'],
               'uutah_precipitation_animation': ['uutah_precip_day1_anim_00.jpg', 'uutah_precip_day1_anim_01.jpg', 'uutah_precip_day1_anim_02.jpg', 'uutah_precip_day1_anim_03.jpg', 'uutah_precip_day1_anim_04.jpg', 'uutah_precip_day1_anim_05.jpg', 'uutah_precip_day1_anim_06.jpg', 'uutah_precip_day1_anim_07.jpg', 'uutah_precip_day1_anim_08.jpg', 'uutah_precip_day1_anim_09.jpg', 'uutah_precip_day1_anim_10.jpg', 'uutah_precip_day1_anim_11.jpg', 'uutah_precip_day2_anim_00.jpg', 'uutah_precip_day2_anim_01.jpg', 'uutah_precip_day2_anim_02.jpg', 'uutah_precip_day2_anim_03.jpg', 'uutah_precip_day2_anim_04.jpg', 'uutah_precip_day2_anim_05.jpg', 'uutah_precip_day2_anim_06.jpg', 'uutah_precip_day2_anim_07.jpg', 'uutah_precip_day2_anim_08.jpg', 'uutah_precip_day2_anim_09.jpg', 'uutah_precip_day2_anim_10.jpg', 'uutah_precip_day2_anim_11.jpg'],
               'icap_aerosol_ensemble': ['ICAP_aerosol_ensemble_72.png', 'ICAP_aerosol_ensemble_120.png'],
               'nasa_geos': ['GEOS_dust_aot.png', 'GEOS_dust_aot_day1.png', 'GEOS_dust_aot_day2.png', 'GEOS_dust_aot_vert_' + str(dust_xLon) + 'N.png', 'GEOS_dust_aot_day1_vert_' + str(dust_xLon) + 'N.png', 'GEOS_dust_aot_day2_vert_' + str(dust_xLon) + 'N.png', 'GEOS_dust_aot_vert_' + str(dust_xLat) + 'W.png', 'GEOS_dust_aot_day1_vert_' + str(dust_xLat) + 'W.png', 'GEOS_dust_aot_day2_vert_' + str(dust_xLat) + 'W.png', 'GEOS_700mb_outlook_anim_00.png', 'GEOS_700mb_outlook_anim_01.png', 'GEOS_700mb_outlook_anim_02.png', 'GEOS_700mb_outlook_anim_03.png', 'GEOS_700mb_outlook_anim_04.png', 'GEOS_700mb_outlook_anim_05.png', 'GEOS_700mb_outlook_anim_06.png', 'GEOS_700mb_outlook_anim_07.png', 'GEOS_700mb_outlook_anim_08.png', 'GEOS_700mb_outlook_anim_09.png', 'GEOS_700mb_outlook_anim_10.png', 'GEOS_700mb_outlook_anim_11.png'],
               'ECMWF_prediction': ['ECMWF_mslp_pcpn_anim_00.png','ECMWF_mslp_pcpn_anim_01.png'],
               'UTAH_dryrun': ['uutah_slp_rain_day1_anim_00.png','uutah_slp_rain_day2_anim_00.png','uutah_tpw_olr_day1_anim_00.png','uutah_tpw_olr_day2_anim_00.png'],
               'GFS_prediction': ['GFS_midRH_anim_00.png','GFS_midRH_anim_01.png','GFS_midRH_anim_02.png'],
               'ICON_prediction': ['ICON_mslp_wind_anim_00.png','ICON_mslp_wind_anim_01.png','ICON_mslp_wind_anim_02.png']}

switch_key_list = list(switch_dict.keys())
switch_val_list = list(switch_dict.values())





print("Downloading images for today's forecast.")



for fle in need_to_download:
  for val in switch_val_list:
    if fle in val:
      fl_val = val

  switch_index = switch_key_list[switch_val_list.index(fl_val)]

  # NHC Analysis and Tropical Weather Outlook
  if switches['nhc_analysis'] and switch_index == 'nhc_analysis':

    if fle == 'NHC_surface_analysis.gif':
      url = 'https://www.nhc.noaa.gov/tafb_latest/USA_latest.gif'
      eb = check_if_missing(url, 'NHC_surface_analysis.gif')


      if not eb:
        cmd = ['convert',  '-coalesce', saveDir + 'NHC_surface_analysis.gif', saveDir + 'NHC_surface_analysis.png']
        subprocess.call(cmd)

    if fle == 'NHC_2day_outlook.png':
      url = 'https://www.nhc.noaa.gov/xgtwo/two_atl_2d0.png'
      _ = check_if_missing(url, 'NHC_2day_outlook.png')


    if fle == 'NHC_2day_outlook.png':
      url = 'https://www.nhc.noaa.gov/xgtwo/two_atl_5d0.png'
      _ = check_if_missing(url, 'NHC_5day_outlook.png')


  # MIMIC-Total Precipitable Water
  if switches['mimic_tpw'] and switch_index == 'mimic_tpw':

    if fle ==  'MIMIC-TPW_24h_animation.gif':
      url = 'http://tropic.ssec.wisc.edu/real-time/mtpw2/webAnims/tpw_nrl_colors/natl/mimictpw_natl_latest.gif'
      eb = check_if_missing(url, 'MIMIC-TPW_24h_animation.gif')


      if not eb:
        cmd = ['convert',  '-coalesce', saveDir + 'MIMIC-TPW_24h_animation.gif', saveDir + 'MIMIC-TPW_24h_animation.png']
        subprocess.call(cmd)

        print('    ... Finding the latest image and setting it to _latest.')
        fls = [fl for fl in os.listdir(saveDir) if 'MIMIC-TPW' in fl and '.png' in fl]
        fls = [fl for fl in fls if 'MIMIC-TPW_24h_animation' in fl]
        frame_number = [int(fl.split('-')[-1][:-4]) for fl in fls]
        latest_frame = fls[0][:24] + str(max(frame_number)) + '.png'
        cmd = ['cp', saveDir+latest_frame, saveDir+'MIMIC-TPW_latest.png']
        subprocess.call(cmd)


  # GOES-16 satellite imagery - Bedka group
  if switches['GOES16_sat'] and switch_index == 'GOES16_sat':

    if fle == 'Goes16_VIS.png':
      url = 'https://satcorps.larc.nasa.gov/prod/exp/cpex-aw-2020/satpng/g16/latest/G16.LATEST.01KM.HVIS.PNG'
      _ = check_if_missing(url, 'Goes16_VIS.png')

    if fle == 'Goes16_RGB.png':
      url = 'https://satcorps.larc.nasa.gov/prod/exp/cpex-aw-2020/satpng/g16/latest/G16.LATEST.02KM.RGB.PNG'
      _ = check_if_missing(url, 'Goes16_RGB.png')

    if fle == 'Goes16_IRC.png':
      url = 'https://satcorps.larc.nasa.gov/prod/exp/cpex-aw-2020/satpng/g16/latest/G16.LATEST.02KM.IRC.PNG'
      _ = check_if_missing(url, 'Goes16_IRC.png')


  # METEOSAT-11 satellite imagery - Bedka group
  if switches['meteosat_sat'] and switch_index == 'meteosat_sat':

    if fle == 'Meteosat11_VIS.png':
      url = 'https://satcorps.larc.nasa.gov/prod/exp/cpex-aw-2020/satpng/met/latest/M11.LATEST.03KM.VIS.PNG'
      _ = check_if_missing(url, 'Meteosat11_VIS.png')


    if fle == 'Meteosat11_IRC.png':
      url = 'https://satcorps.larc.nasa.gov/prod/exp/cpex-aw-2020/satpng/met/latest/M11.LATEST.03KM.IRC.PNG'
      _ = check_if_missing(url, 'Meteosat11_IRC.png')


  # Alan Brammer's tropical wave tracking
  if switches['brammer_tropical_waves'] and switch_index == 'brammer_tropical_waves':

    if fle == 'AEW_Brammer.jpg':
      init_date = datetime.strptime('2013-01-01', '%Y-%m-%d')
      time_diff = int(np.ceil((today-init_date).total_seconds()/3600))

      url = 'http://www.atmos.albany.edu/student/abrammer/graphics/gfs_realtime/plots/prate_sf_mslp/ea_prate_sf_mslp_' + str(time_diff) + '.0.jpg'
      dl = downloadLink(url, saveDir + 'AEW_Brammer.jpg')

      if not dl:
        time_diff += 6
        url = 'http://www.atmos.albany.edu/student/abrammer/graphics/gfs_realtime/plots/prate_sf_mslp/ea_prate_sf_mslp_' + str(time_diff) + '.0.jpg'
        print('    ... Trying a different time.')
        dl = downloadLink(url, saveDir + 'AEW_Brammer.jpg')



    if not dl:
      time_diff += 6
      url = 'http://www.atmos.albany.edu/student/abrammer/graphics/gfs_realtime/plots/prate_sf_mslp/ea_prate_sf_mslp_' + str(time_diff) + '.0.jpg'
      print('    ... Trying a different time.')
      dl = downloadLink(url, saveDir + 'AEW_Brammer.jpg')


      url = 'http://www.atmos.albany.edu/student/abrammer/graphics/gfs_realtime/plots/prate_sf_mslp/ea_prate_sf_mslp_' + str(time_diff) + '.0.jpg'
      _ = check_if_missing(url, 'AEW_Brammer.jpg')






  # Saharan Air Layer - Split Window GOES-16
  if switches['sal_split'] and switch_index == 'sal_split':

    if fle == 'SAL_dryAir_split.jpg':
      url = 'http://tropic.ssec.wisc.edu/real-time/sal/g16split/g16split.jpg'
      _ = check_if_missing(url, 'SAL_dryAir_split.jpg')



  # # # MODEL STUFF NOW - SINGLE IMAGES
  if switches['uwincm_clouds_current'] and switch_index == 'uwincm_clouds_current':

    if fle == 'uwincm_clouds_current.jpg':
      url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/storm/pw_olr/pw_olr.storm.' +  today.strftime('%Y%m%d') + '16.jpg'
      _ = check_if_missing(url, 'uwincm_clouds_current.jpg')


  if switches['uwincm_surfaceWind'] and switch_index == 'uwincm_surfaceWind':

    if fle == 'uwincm_surfaceWind_day1.jpg':
      if model_day1:
        url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/large/windsfc/wspd.large.' +  forecast_day1.strftime('%Y%m%d') + '{:02d}'.format(still_image_forecast_hr) + '.jpg'
        _ = check_if_missing(url, 'uwincm_surfaceWind_day1.jpg')

    if fle == 'uwincm_surfaceWind_day1.jpg':
      if model_day2:
        url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/large/windsfc/wspd.large.' +  forecast_day2.strftime('%Y%m%d') + '{:02d}'.format(still_image_forecast_hr) + '.jpg'
        _ = check_if_missing(url, 'uwincm_surfaceWind_day2.jpg')


  if switches['uwincm_650mbRH'] and switch_index == 'uwincm_650mbRH':

    if fle == 'uwincm_650mbRH_day1.jpg':
      if model_day1:
        url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/large/rh650mb/650mb_rh.large.' +  forecast_day1.strftime('%Y%m%d') + '{:02d}'.format(still_image_forecast_hr) + '.jpg'
        _ = check_if_missing(url, 'uwincm_650mbRH_day1.jpg')

    if fle == 'uwincm_650mbRH_day2.jpg':
      if model_day2:
        url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/large/rh650mb/650mb_rh.large.' +  forecast_day2.strftime('%Y%m%d') + '{:02d}'.format(still_image_forecast_hr) + '.jpg'
        _ = check_if_missing(url, 'uwincm_650mbRH_day2.jpg')


  if switches['uwincm_clouds'] and switch_index == 'uwincm_clouds':

    if fle == 'uwincm_clouds_day1.jpg':
      if model_day1:
        url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/storm/pw_olr/pw_olr.storm.' +  forecast_day1.strftime('%Y%m%d') + '{:02d}'.format(still_image_forecast_hr) + '.jpg'
        _ = check_if_missing(url, 'uwincm_clouds_day1.jpg')


    if fle == 'uwincm_clouds_day2.jpg':
      if model_day2:
        url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/storm/pw_olr/pw_olr.storm.' +  forecast_day2.strftime('%Y%m%d') + '{:02d}'.format(still_image_forecast_hr) + '.jpg'
        _ = check_if_missing(url, 'uwincm_clouds_day2.jpg')


  if switches['uwincm_precipitation'] and switch_index == 'uwincm_precipitation':

    if fle == 'uwincm_precip_day1.jpg':
      if model_day1:
        url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/storm/rr_slp/rainr.storm.' +  forecast_day1.strftime('%Y%m%d') + '{:02d}'.format(still_image_forecast_hr) + '.jpg'
        _ = check_if_missing(url, 'uwincm_precip_day1.jpg')


    if fle == 'uwincm_precip_day2.jpg':
      if model_day2:
        url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/storm/rr_slp/rainr.storm.' +  forecast_day2.strftime('%Y%m%d') + '{:02d}'.format(still_image_forecast_hr) + '.jpg'
        _ = check_if_missing(url, 'uwincm_precip_day2.jpg')


  if switches['uwincm_boundaryLayer'] and switch_index == 'uwincm_boundaryLayer':

    if fle == 'uwincm_boundaryLayer_day1.jpg':
      if model_day1:
        url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/storm/blh/blh.storm.' +  forecast_day1.strftime('%Y%m%d') + '{:02d}'.format(still_image_forecast_hr) + '.jpg'
        _ = check_if_missing(url, 'uwincm_boundaryLayer_day1.jpg')


    if fle == 'uwincm_boundaryLayer_day1.jpg':
      if model_day2:
        url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/storm/blh/blh.storm.' +  forecast_day2.strftime('%Y%m%d') + '{:02d}'.format(still_image_forecast_hr) + '.jpg'
        _ = check_if_missing(url, 'uwincm_boundaryLayer_day2.jpg')


  if switches['uutah_precipitation'] and switch_index == 'uutah_precipitation':

    if fle == 'uutah_precip_day1.jpg':
      if model_day1:
        url = 'https://orca.atmos.washington.edu/model_images/atl/uutah/realtime/' + today.strftime('%Y%m%d') + '00/gfs/storm/rr_slp/slp_rain-' +  forecast_day1.strftime('%Y-%m-%d') + '_' + '{:02d}'.format(still_image_forecast_hr) + ':00:00_d02.png'
        _ = check_if_missing(url, 'uutah_precip_day1.jpg')


    if fle == 'uutah_precip_day1.jpg':
      if model_day2:
        url = 'https://orca.atmos.washington.edu/model_images/atl/uutah/realtime/' + today.strftime('%Y%m%d') + '00/gfs/storm/rr_slp/slp_rain-' +  forecast_day2.strftime('%Y-%m-%d') + '_' + '{:02d}'.format(still_image_forecast_hr) + ':00:00_d02.png'
        _ = check_if_missing(url, 'uutah_precip_day2.jpg')



  # # # MODEL STUFF NOW - ANIMATIONS
  if switches['uwincm_surfaceWind_animation'] and switch_index == 'uwincm_surfaceWind_animation':

    if 'uwincm_surfaceWind_day1_anim_' in fle:
      if model_day1:
        for frame in range(nFrames_uwincm):
          url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/large/windsfc/wspd.large.' +  (forecast_day1+timedelta(hours=1) + timedelta(hours=2*frame)).strftime('%Y%m%d%H') + '.jpg'
          fName = 'uwincm_surfaceWind_day1_anim_' + '{:02d}'.format(frame) + '.jpg'
          if fName == fle:
            _ = check_if_missing(url, fName)

    if 'uwincm_surfaceWind_day2_anim_' in fle:
      if model_day2:
        for frame in range(nFrames_uwincm):
          url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/large/windsfc/wspd.large.' +  (forecast_day2+timedelta(hours=1) + timedelta(hours=2*frame)).strftime('%Y%m%d%H') + '.jpg'
          fName = 'uwincm_surfaceWind_day2_anim_' + '{:02d}'.format(frame) + '.jpg'
          if fName == fle:
            _ = check_if_missing(url, fName)


  if switches['uwincm_650mbRH_animation'] and switch_index == 'uwincm_650mbRH_animation':

    if 'uwincm_650mbRH_day1_anim_' in fle:
      if model_day1:
        for frame in range(nFrames_uwincm):
          url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/large/rh650mb/650mb_rh.large.' +  (forecast_day1+timedelta(hours=1) + timedelta(hours=2*frame)).strftime('%Y%m%d%H') + '.jpg'
          fName = 'uwincm_650mbRH_day1_anim_' + '{:02d}'.format(frame) + '.jpg'
          if fName == fle:
            _ = check_if_missing(url, fName)

    if 'uwincm_650mbRH_day2_anim_' in fle:
      if model_day2:
        for frame in range(nFrames_uwincm):
          url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/large/rh650mb/650mb_rh.large.' +  (forecast_day2+timedelta(hours=1) + timedelta(hours=2*frame)).strftime('%Y%m%d%H') + '.jpg'
          fName = 'uwincm_650mbRH_day2_anim_' + '{:02d}'.format(frame) + '.jpg'
          if fName == fle:
            _ = check_if_missing(url, fName)


  if switches['uwincm_clouds_animation'] and switch_index == 'uwincm_clouds_animation':

    if 'uwincm_clouds_day1_anim_' in fle:
      if model_day1:
        for frame in range(nFrames_uwincm):
          url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/storm/pw_olr/pw_olr.storm.' +  (forecast_day1+timedelta(hours=1) + timedelta(hours=2*frame)).strftime('%Y%m%d%H') + '.jpg'
          fName = 'uwincm_clouds_day1_anim_' + '{:02d}'.format(frame) + '.jpg'
          if fName == fle:
            _ = check_if_missing(url, fName)

    if 'uwincm_clouds_day2_anim_' in fle:
      if model_day2:
        for frame in range(nFrames_uwincm):
          url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/storm/pw_olr/pw_olr.storm.' +  (forecast_day2+timedelta(hours=1) + timedelta(hours=2*frame)).strftime('%Y%m%d%H') + '.jpg'
          fName = 'uwincm_clouds_day2_anim_' + '{:02d}'.format(frame) + '.jpg'
          if fName == fle:
            _ = check_if_missing(url, fName)

  if switches['uwincm_precipitation_animation'] and switch_index == 'uwincm_precipitation_animation':

    if 'uwincm_precip_day1_anim_' in fle:
      if model_day1:
        for frame in range(nFrames_uwincm):
          url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/storm/rr_slp/rainr.storm.' +  (forecast_day1+timedelta(hours=1) + timedelta(hours=2*frame)).strftime('%Y%m%d%H') + '.jpg'
          fName = 'uwincm_precip_day1_anim_' + '{:02d}'.format(frame) + '.jpg'
          if fName == fle:
            _ = check_if_missing(url, fName)


    if 'uwincm_precip_day2_anim_' in fle:
      if model_day2:
        for frame in range(nFrames_uwincm):
          url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/storm/rr_slp/rainr.storm.' +  (forecast_day2+timedelta(hours=1) + timedelta(hours=2*frame)).strftime('%Y%m%d%H') + '.jpg'
          fName = 'uwincm_precip_day2_anim_' + '{:02d}'.format(frame) + '.jpg'
          if fName == fle:
            _ = check_if_missing(url, fName)


  if switches['uwincm_boundaryLayer_animation'] and switch_index == 'uwincm_boundaryLayer_animation':

    if 'uwincm_boundaryLayer_day1_anim_' in fle:
      if model_day1:
        for frame in range(nFrames_uwincm):
          url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/storm/blh/blh.storm.' +  (forecast_day1+timedelta(hours=1) + timedelta(hours=2*frame)).strftime('%Y%m%d%H') + '.jpg'
          fName = 'uwincm_boundaryLayer_day1_anim_' + '{:02d}'.format(frame) + '.jpg'
          if fName == fle:
            _ = check_if_missing(url, fName)

    if 'uwincm_boundaryLayer_day2_anim_' in fle:
      if model_day2:
        for frame in range(nFrames_uwincm):
          url = 'https://orca.atmos.washington.edu/model_images/atl/umcm_wmh/realtime/' + today.strftime('%Y%m%d') + '00/ecmwf/storm/blh/blh.storm.' +  (forecast_day2+timedelta(hours=1) + timedelta(hours=2*frame)).strftime('%Y%m%d%H') + '.jpg'
          fName = 'uwincm_boundaryLayer_day2_anim_' + '{:02d}'.format(frame) + '.jpg'
          if fName == fle:
            _ = check_if_missing(url, fName)


  if switches['uutah_precipitation_animation'] and switch_index == 'uutah_precipitation_animation':

    if 'uutah_precip_day1_anim_' in fle:
      if model_day1:
        for frame in range(nFrames_uwincm):
          url = 'https://orca.atmos.washington.edu/model_images/atl/uutah/realtime/' + today.strftime('%Y%m%d') + '00/gfs/storm/rr_slp/slp_rain-' +  (forecast_day1+timedelta(hours=1) + timedelta(hours=2*frame)).strftime('%Y-%m-%d_%H:%M:%S') + '_d02.png'
          fName = 'uutah_precip_day1_anim_' + '{:02d}'.format(frame) + '.png'
          if fName == fle:
            _ = check_if_missing(url, fName)

    if 'uutah_precip_day1_anim_' in fle:
      if model_day2:
        for frame in range(nFrames_uwincm):
          url = 'https://orca.atmos.washington.edu/model_images/atl/uutah/realtime/' + today.strftime('%Y%m%d') + '00/gfs/storm/rr_slp/slp_rain-' +  (forecast_day2+timedelta(hours=1) + timedelta(hours=2*frame)).strftime('%Y-%m-%d_%H:%M:%S') + '_d02.png'
          fName = 'uutah_precip_day2_anim_' + '{:02d}'.format(frame) + '.png'
          if fName == fle:
            _ = check_if_missing(url, fName)



  # NOW BACK TO OBSERVATIONS - ICAP
  if switches['icap_aerosol_ensemble'] and switch_index == 'icap_aerosol_ensemble':

    if 'ICAP_aerosol_ensemble_' in fle:
      url_base = 'https://www.nrlmry.navy.mil/aerosol/globaer/icap_01/subtropatl/' + (today-timedelta(days=1)).strftime('%Y%m%d') + '00/' + (today-timedelta(days=1)).strftime('%Y%m%d') + '00_'
      days = [4, 5]
      download_days = [((today-timedelta(days=1)) + timedelta(days=dy)).strftime('%Y%m%d%H') for dy in days]

      dTime = int((datetime.strptime(download_days[0], '%Y%m%d%H') - (today-timedelta(days=1))).total_seconds()/3600)
      url = url_base + download_days[0] + '_f' + '{:03d}'.format(dTime) + '_total_aod_550_subtropatl_icap.png'

      _ = check_if_missing(url, 'ICAP_aerosol_ensemble_' + str(dTime) + '.png')



      dTime = int((datetime.strptime(download_days[1], '%Y%m%d%H') - (today-timedelta(days=1))).total_seconds()/3600)
      url = url_base + download_days[1] + '_f' + '{:03d}'.format(dTime) + '_total_aod_550_subtropatl_icap.png'

      _ = check_if_missing(url, 'ICAP_aerosol_ensemble_' + str(dTime) + '.png')


  if switches['nasa_geos'] and switch_index == 'nasa_geos':

    if 'GEOS_' in fle:
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

      #Get AOT 2D image

      for idx, tau in enumerate(AOT_tau):
        AOT_page = AOT_url_prefix + 'tau=' + tau + AOT_url_suffix + '&field=duaot'
        AOT_img_url = find_geos_img_url(AOT_page, img_url_pattern, req_timeout)

        _ = check_if_missing(AOT_img_url, AOT_img_2D_files[idx])


      for idx, tau in enumerate(AOT_tau):
        AOT_page = AOT_url_prefix + 'tau=' + tau + AOT_url_suffix + '&field=totaot'
        AOT_img_url = find_geos_img_url(AOT_page, img_url_pattern, req_timeout)

        _ = check_if_missing(AOT_img_url, AOT_img_total_files[idx])


      for idx, tau in enumerate(AOT_tau):
        cldfra_prefix = AOT_url_prefix.replace('chem2d_mission', 'weather_mission')
        cldfra_suffix = AOT_url_suffix
        cldfra_page = cldfra_prefix + 'tau=' + tau + cldfra_suffix + '&field=cldlow'
        cldfra_img_url = find_geos_img_url(cldfra_page, img_url_pattern, req_timeout)

        _ = check_if_missing(cldfra_img_url, AOT_img_lowcf_files[idx])


      for idx, tau in enumerate(AOT_tau):
        cldfra_prefix = AOT_url_prefix.replace('chem2d_mission', 'weather_mission')
        cldfra_suffix = AOT_url_suffix
        cldfra_page = cldfra_prefix + 'tau=' + tau + cldfra_suffix + '&field=cldmid'
        cldfra_img_url = find_geos_img_url(cldfra_page, img_url_pattern, req_timeout)

        _ = check_if_missing(cldfra_img_url, AOT_img_midcf_files[idx])


      for idx, tau in enumerate(AOT_tau):
        cldfra_prefix = AOT_url_prefix.replace('chem2d_mission', 'weather_mission')
        cldfra_suffix = AOT_url_suffix
        cldfra_page = cldfra_prefix + 'tau=' + tau + cldfra_suffix + '&field=cldhgh'
        cldfra_img_url = find_geos_img_url(cldfra_page, img_url_pattern, req_timeout)

        _ = check_if_missing(cldfra_img_url, AOT_img_highcf_files[idx])



      #Get AOT longitudinal cross section
      for idx, tau in enumerate(AOT_tau):
        AOT_page = AOT_url_prefix.replace('chem2d_mission', 'custom_mission')
        AOT_page =  AOT_page + 'tau=' + tau + AOT_url_suffix + '&field=du_w2'
        AOT_img_url = find_geos_img_url(AOT_page, img_url_pattern, req_timeout)

        _ = check_if_missing(AOT_img_url, AOT_img_loncs_files[idx])



      #Get AOT latitudinal cross section image
      for idx, tau in enumerate(AOT_tau):
        AOT_page = AOT_url_prefix.replace('chem2d_mission', 'custom_mission')
        AOT_page =  AOT_page + 'tau=' + tau + AOT_url_suffix + '&field=du_n3'
        AOT_img_url = find_geos_img_url(AOT_page, img_url_pattern, req_timeout)

        _ = check_if_missing(AOT_img_url, AOT_img_latcs_files[idx])


      #Get 700 mb wind with geopotential heights
      for idx, tau in enumerate(wind_700mb_tau):
        wind700mb_prefix = AOT_url_prefix.replace('chem2d_mission', 'weather_mission')
        wind700mb_suffix = AOT_url_suffix.replace('level=0','level=700')
        wind700mb_page = wind700mb_prefix + 'tau=' + tau + wind700mb_suffix + '&field=wspd'
        wind700m_img_url = find_geos_img_url(wind700mb_page, img_url_pattern, req_timeout)

        _ = check_if_missing(wind700m_img_url, wind_700mb_files[idx])


new_present_files = [fl for fl in os.listdir(saveDir) if fl in wanted_files]

fl_switch = open(forecastDir + './supplementary/switches_process.txt', 'w')
# set all switches for completed or partly-completed to true
for sw in switch_key_list:
  fls = switch_dict[sw]
  fls_present = [fl for fl in fls if fl in present_files]
  print(sw,fls,fls_present)
  if len(fls_present) > 0:
    status = [True]
    write_switch(sw, fl_switch)
  else:
    status = [False]
    write_switch(sw, fl_switch)
fl_switch.close()

nGood_links = len(new_present_files)

print("Downloading missing images for today's forecast complete.")
print("There were a total of " + str(nGood_links) + "/" + str(total_links) + " good links (" + '{:.1f}'.format((nGood_links/total_links)*100) + '%).')
