"""
Author: Ajda Savarin
Created: July 04th 2020
University of Washington
asavarin@uw.edu

Re-run the code for downloading and processing observed satellite imagery.

"""


from datetime import datetime, timedelta
import numpy as np
import os
import requests
import subprocess
import time

from bs4 import BeautifulSoup
from urllib import request, error


moveOriginalImages = True
downloadImages = True
moveFinalImages = True


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
dust_xLat = 20 # 20 degrees W
nDup_frames = 3




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


if moveOriginalImages:
  print('Copying original downloaded images into ./figs_final/*backup.')


  list_of_images = ['NHC_surface_analysis.png',
                    'MIMIC-TPW_latest.png',
                    'Goes16_Meteosat11_IRC.png',
                    'SAL_dryAir_split.jpg',
                    'ICAP_aerosol_ensemble_96.png',
                    'ICAP_aerosol_ensemble_120.png']


  for fl in list_of_images:
    pref = fl[:-4]
    ins = '_backup_'
    num = 0
    suf = fl[-4:]

    fl_tmp = pref + ins + '{:02d}'.format(num) + suf

    if os.path.isfile(finDir+fl):
      while os.path.isfile(finDir+fl_tmp):
        num+=1
        fl_tmp = pref + ins + '{:02d}'.format(num) + suf


      os.system('cp ' + finDir+fl + ' ' + finDir+fl_tmp)
    else:
      print('... ... ' + fl + ' not present and cannot be copied over.')



switches = {'nhc_analysis': True,
            'mimic_tpw': True,
            'GOES16_sat': True,
            'meteosat_sat': True,
            'sal_split': True,
            'icap_aerosol_ensemble': True}

if downloadImages:
  all_files = sorted([el for el in os.listdir(saveDir)])
  current_files = sorted([el for el in all_files if 'MIMIC-TPW' in el])
  for fl in current_files:
    os.remove(saveDir+fl)
  #all_files = sorted([el for el in os.listdir(saveDir)])
  print("Downloading latest satellite imagery for today's forecast.")

  # NHC Analysis and Tropical Weather Outlook
  if switches['nhc_analysis']:
    print('... Downloading and processing NHC surface analysis.')

    url = 'https://www.nhc.noaa.gov/tafb_latest/USA_latest.gif'
    dl = downloadLink(url, saveDir + 'NHC_surface_analysis.gif')

    if dl:
      cmd = ['convert',  '-coalesce', saveDir + 'NHC_surface_analysis.gif', saveDir + 'NHC_surface_analysis.png']
      subprocess.call(cmd)

    current_files = [el for el in all_files if 'NHC_surface_analysis.png' in el]
    marker_radius = 5
    for fl in current_files:
      cmd = ['convert', saveDir+fl, '-crop', '1268x648+1100+350', '+repage', cropDir+fl]
      subprocess.call(cmd)

      xPt, yPt = 370, 430
      cmd = ['convert', cropDir+fl, '-fill', 'red', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)

      xPt, yPt = 952, 445
      cmd = ['convert', cropDir+fl, '-fill', 'red', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)


  # MIMIC-Total Precipitable Water
  if switches['mimic_tpw']:
    print('... Downloading and processing MIMIC-TPW animation.')

    url = 'http://tropic.ssec.wisc.edu/real-time/mtpw2/webAnims/tpw_nrl_colors/natl/mimictpw_natl_latest.gif'
    dl = downloadLink(url, saveDir + 'MIMIC-TPW_24h_animation.gif')


    if dl:
      cmd = ['convert',  '-coalesce', saveDir + 'MIMIC-TPW_24h_animation.gif', saveDir + 'MIMIC-TPW_24h_animation.png']
      subprocess.call(cmd)

      fls = [fl for fl in os.listdir(saveDir) if 'MIMIC-TPW' in fl and '.png' in fl]
      fls = [fl for fl in fls if 'MIMIC-TPW_24h_animation' in fl]
      frame_number = [int(fl.split('-')[-1][:-4]) for fl in fls]
      latest_frame = fls[0][:24] + str(max(frame_number)) + '.png'
      cmd = ['cp', saveDir+latest_frame, saveDir+'MIMIC-TPW_latest.png']
      subprocess.call(cmd)



    current_files = sorted([el for el in all_files if 'MIMIC-TPW' in el])

    marker_radius = 4
    for fl in current_files:
      cmd = ['convert', saveDir+fl, '-crop', '990x452+8+18', '+repage', cropDir+fl]
      subprocess.call(cmd)


      xPt, yPt = 367, 305
      cmd = ['convert', cropDir+fl, '-fill', 'white', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)


      xPt, yPt = 665, 323
      cmd = ['convert', cropDir+fl, '-fill', 'white', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)

    current_files_subset = [el for el in current_files if 'animation-' in el]
    frame_number = [int(el.split('-')[-1].split('.')[0]) for el in current_files_subset]
    for num, fl in enumerate(current_files_subset):
      os.rename(cropDir+fl, cropDir+fl[:24]+'{:02d}'.format(frame_number[num])+fl[-4:])

  # GOES-16 satellite imagery - Bedka group
  if switches['GOES16_sat']:
    print('... Downloading and processing GOES-16 imagery.')

    url = 'https://satcorps.larc.nasa.gov/prod/exp/cpex-aw-2020/satpng/g16/latest/G16.LATEST.01KM.HVIS.PNG'
    dl = downloadLink(url, saveDir + 'Goes16_VIS.png')


    print('... Downloading GOES16 RGB satellite imagery.')
    url = 'https://satcorps.larc.nasa.gov/prod/exp/cpex-aw-2020/satpng/g16/latest/G16.LATEST.02KM.RGB.PNG'
    dl = downloadLink(url, saveDir + 'Goes16_RGB.png')


    print('... Downloading GOES16 IRC satellite imagery.')
    url = 'https://satcorps.larc.nasa.gov/prod/exp/cpex-aw-2020/satpng/g16/latest/G16.LATEST.02KM.IRC.PNG'
    dl = downloadLink(url, saveDir + 'Goes16_IRC.png')

    current_files = sorted([el for el in all_files if 'Goes16' in el])

    marker_radius = 8
    xPt, yPt = 480, 808
    for fl in current_files:
      if ('IRC' or 'RGB') in fl:
        xPt, yPt = 508, 860
        cmd = ['convert', saveDir+fl, '-crop', '2000x2000+0+0', '+repage', cropDir+fl]
        subprocess.call(cmd)

        cmd = ['convert', cropDir+fl, '-fill', 'magenta', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
        subprocess.call(cmd)

      elif 'VIS' in fl:
        xPt, yPt = 940, 1560
        cmd = ['convert', saveDir+fl, '-crop', '3712x3700+0+0', '+repage', cropDir+fl]
        subprocess.call(cmd)

        cmd = ['convert', cropDir+fl, '-fill', 'magenta', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius*2) + ',' + str(yPt+marker_radius*2), cropDir+fl]
        subprocess.call(cmd)

      if 'IRC' in fl:

        cmd = ['convert', cropDir+fl, '-resize', '2100x2000', '-background', 'white', '-gravity', 'west', '-extent', '2100x2000', cropDir+fl]
        subprocess.call(cmd)
        # this will add a  color scale

        xPtT, yPtT = 2000, 1775
        cmd = ['convert', cropDir+fl, '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), '-110', cropDir+fl]
        subprocess.call(cmd)
        xPtT, yPtT = 2000, 1577
        cmd = ['convert', cropDir+fl, '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), '-90', cropDir+fl]
        subprocess.call(cmd)
        xPtT, yPtT = 2000, 1395
        cmd = ['convert', cropDir+fl, '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), '-70', cropDir+fl]
        subprocess.call(cmd)
        xPtT, yPtT = 2000, 1215
        cmd = ['convert', cropDir+fl, '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), '-50', cropDir+fl]
        subprocess.call(cmd)
        xPtT, yPtT = 2000, 1035
        cmd = ['convert', cropDir+fl, '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), '-30', cropDir+fl]
        subprocess.call(cmd)
        xPtT, yPtT = 2000, 855
        cmd = ['convert', cropDir+fl, '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), '-10', cropDir+fl]
        subprocess.call(cmd)
        xPtT, yPtT = 2000, 675
        cmd = ['convert', cropDir+fl, '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), ' 10', cropDir+fl]
        subprocess.call(cmd)
        xPtT, yPtT = 2000, 495
        cmd = ['convert', cropDir+fl, '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), ' 30', cropDir+fl]
        subprocess.call(cmd)
        xPtT, yPtT = 2000, 315
        cmd = ['convert', cropDir+fl, '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), ' 50', cropDir+fl]
        subprocess.call(cmd)
        xPtT, yPtT = 2000, 245
        cmd = ['convert', cropDir+fl, '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), 'ºC', cropDir+fl]
        subprocess.call(cmd)


  # METEOSAT-11 satellite imagery - Bedka group
  if switches['meteosat_sat']:
    print('... Downloading and processing Meteosat-11 imagery.')

    url = 'https://satcorps.larc.nasa.gov/prod/exp/cpex-aw-2020/satpng/met/latest/M11.LATEST.03KM.VIS.PNG'
    dl = downloadLink(url, saveDir + 'Meteosat11_VIS.png')

    print('... Downloading Meteosat-11 IRC satellite imagery.')
    url = 'https://satcorps.larc.nasa.gov/prod/exp/cpex-aw-2020/satpng/met/latest/M11.LATEST.03KM.IRC.PNG'
    dl = downloadLink(url, saveDir + 'Meteosat11_IRC.png')

    current_files = sorted([el for el in all_files if 'Meteosat' in el])

    marker_radius = 12
    #xPt, yPt = 600, 675
    xPt, yPt = 850, 910
    for fl in current_files:
      subprocess.call(cmd)
      cmd = ['convert', saveDir+fl, '-crop', '3000x2000+0+0', '+repage', cropDir+fl]
      subprocess.call(cmd)

      cmd = ['convert', cropDir+fl, '-fill', 'magenta', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)

      if 'IRC' in fl:
        print('      ... Color IR - adding Celsius color scale on side.')
        #cmd = []
        cmd = ['convert', cropDir+fl, '-resize', '3100x2000', '-background', 'white', '-gravity', 'west', '-extent', '3100x2000', cropDir+fl]
        subprocess.call(cmd)
        # this will add a  color scale

        xPtT, yPtT = 3000, 1775
        cmd = ['convert', cropDir+fl, '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), '-110', cropDir+fl]
        subprocess.call(cmd)
        xPtT, yPtT = 3000, 1577
        cmd = ['convert', cropDir+fl, '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), '-90', cropDir+fl]
        subprocess.call(cmd)
        xPtT, yPtT = 3000, 1395
        cmd = ['convert', cropDir+fl, '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), '-70', cropDir+fl]
        subprocess.call(cmd)
        xPtT, yPtT = 3000, 1215
        cmd = ['convert', cropDir+fl, '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), '-50', cropDir+fl]
        subprocess.call(cmd)
        xPtT, yPtT = 3000, 1035
        cmd = ['convert', cropDir+fl, '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), '-30', cropDir+fl]
        subprocess.call(cmd)
        xPtT, yPtT = 3000, 855
        cmd = ['convert', cropDir+fl, '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), '-10', cropDir+fl]
        subprocess.call(cmd)
        xPtT, yPtT = 3000, 675
        cmd = ['convert', cropDir+fl, '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), ' 10', cropDir+fl]
        subprocess.call(cmd)
        xPtT, yPtT = 3000, 495
        cmd = ['convert', cropDir+fl, '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), ' 30', cropDir+fl]
        subprocess.call(cmd)
        xPtT, yPtT = 3000, 315
        cmd = ['convert', cropDir+fl, '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), ' 50', cropDir+fl]
        subprocess.call(cmd)
        xPtT, yPtT = 3000, 245
        cmd = ['convert', cropDir+fl, '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), 'ºC', cropDir+fl]
        subprocess.call(cmd)


  if switches['meteosat_sat'] and switches['GOES16_sat']:
    current_files_met = sorted([el for el in all_files if 'Meteosat' in el])
    current_files_goes = sorted([el for el in all_files if 'Goes16' in el])


    # for IRC image:
    fileName = 'Goes16_Meteosat11_IRC.png'
    currentInd_met = current_files_met.index([fl for fl in current_files_met if '_IRC.' in fl][0])
    currentInd_goes = current_files_goes.index([fl for fl in current_files_goes if '_IRC.' in fl][0])

    # 1. crop off the color bar off of GOES16
    cmd = ['convert', cropDir+current_files_goes[currentInd_goes], '-crop', '1750x2000+0+0', '+repage', cropDir+'temp1.png']
    subprocess.call(cmd)

    # 2. merge met file with goes file
    cmd = ['convert', cropDir+'temp1.png', cropDir+current_files_met[currentInd_met], '+append', '+repage', cropDir+fileName]
    subprocess.call(cmd)


    current_fls = [fl for fl in os.listdir(cropDir) if 'temp' in fl and '.png' in fl]
    for fl in current_fls:
      cmd = ['rm', cropDir+fl]
      subprocess.call(cmd)


  # Saharan Air Layer - Split Window GOES-16
  if switches['sal_split']:
    print('... Downloading and processing split window imagery from CIMSS.')

    url = 'http://tropic.ssec.wisc.edu/real-time/sal/g16split/g16split.jpg'
    dl = downloadLink(url, saveDir + 'SAL_dryAir_split.jpg')

    current_files = [el for el in all_files if 'SAL_dryAir_split' in el]

    marker_radius = 6
    for fl in current_files:
      cmd = ['convert', saveDir+fl, '-crop', '1312x780+230+0', '+repage', cropDir+fl]
      subprocess.call(cmd)

      xPt, yPt = 405, 468
      cmd = ['convert', cropDir+fl, '-fill', 'white', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)

      xPt, yPt = 1120, 488
      cmd = ['convert', cropDir+fl, '-fill', 'white', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)

      # # # crop off the color bar
      cmd = ['convert', saveDir+fl, '-crop', '682x38+430+782', '+repage', cropDir+fl[:-4]+'_cbar'+fl[-4:]]
      subprocess.call(cmd)

      # # # resize color bar
      cmd = ['convert', cropDir+fl[:-4]+'_cbar'+fl[-4:], '-resize', '1312x73', '+repage', cropDir+fl[:-4]+'_cbar'+fl[-4:]]
      subprocess.call(cmd)

      print('      ... Adding a larger version of the color bar.')
      # # # join original image and larger color bar together
      cmd = ['convert', cropDir+fl, cropDir+fl[:-4]+'_cbar'+fl[-4:], '-append', cropDir+fl]
      subprocess.call(cmd)


  # ICAP Aerosol Ensemble
  if switches['icap_aerosol_ensemble']:
    print('... Downloading and processing ICAP aerosol ensemble imagery.')

    url_base = 'https://www.nrlmry.navy.mil/aerosol/globaer/icap_01/subtropatl/' + (today-timedelta(days=1)).strftime('%Y%m%d') + '00/' + (today-timedelta(days=1)).strftime('%Y%m%d') + '00_'
    days = [4, 5]
    download_days = [((today-timedelta(days=1)) + timedelta(days=dy)).strftime('%Y%m%d%H') for dy in days]

    dTime = int((datetime.strptime(download_days[0], '%Y%m%d%H') - (today-timedelta(days=1))).total_seconds()/3600)
    url = url_base + download_days[0] + '_f' + '{:03d}'.format(dTime) + '_total_aod_550_subtropatl_icap.png'

    dl = downloadLink(url, saveDir + 'ICAP_aerosol_ensemble_' + str(dTime) + '.png')



    dTime = int((datetime.strptime(download_days[1], '%Y%m%d%H') - (today-timedelta(days=1))).total_seconds()/3600)
    url = url_base + download_days[1] + '_f' + '{:03d}'.format(dTime) + '_total_aod_550_subtropatl_icap.png'

    dl = downloadLink(url, saveDir + 'ICAP_aerosol_ensemble_' + str(dTime) + '.png')

    current_files = sorted([el for el in all_files if 'ICAP' in el])

    marker_radius = 4
    for fl in current_files:
      cmd = ['convert', saveDir+fl, '-crop', '825x530+80+85', '+repage', cropDir+fl]
      subprocess.call(cmd)


      xPt, yPt = 243, 318
      cmd = ['convert', cropDir+fl, '-fill', 'red', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)

      xPt, yPt = 490, 334
      cmd = ['convert', cropDir+fl, '-fill', 'red', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)


if moveFinalImages:
  print('Moving final images and animations to ./figs_final.')


  list_of_images = ['NHC_surface_analysis.png',
                    'MIMIC-TPW_latest.png',
                    'Goes16_Meteosat11_IRC.png',
                    'SAL_dryAir_split.jpg',
                    'ICAP_aerosol_ensemble_96.png',
                    'ICAP_aerosol_ensemble_120.png']


  for fl in list_of_images:
    if os.path.isfile(cropDir+fl):
      os.system('cp ' + cropDir+fl + ' ' + finDir+fl)
    else:
      print('... ... ' + fl + ' not present and cannot be copied over.')
