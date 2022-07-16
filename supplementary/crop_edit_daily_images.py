"""
Author: Ajda Savarin
Created: July 12th 2020
University of Washington
asavarin@uw.edu

This program is used to crop images downloaded with download_daily_images and draw the Sal Island marker on them.

Required packages: os, subprocess, time.


NOTE: Read through the True/False switches at the top of the script to make sure the ones you want are selected.

Updates:
 - 2021-07-13: For satellite imagery, included Meteosat, GOES-16 cropped to St. Croix, and the Tropical Atlantic GOES-16. Also added the NHC tropical weather outlook figures for 2 and  5 days ahead. Included marked locations for both Sal Island and St Croix where applicable.
 - 2021-07-15: Trimmed the new CPEX-AW 2021 logo. Merged the Meteosat-11 and GOES-16 satellite imagery for a view of the Tropical Atlantic.
 - 2021-07-26: Added total AOT to files moved to ./figs_final/.
"""
import os
import subprocess
import time


clearDirectory = True # remove existing files
readSwitches = True
processImages = True
joinSlideAnimations = True
moveFinalImages = True

model_day1 = model_day2 = True

forecastDir = './'
saveDir = './figs/'
cropDir = './figs_cropped/'
finDir = './figs_final/'




nDup_frames = 3


def persistLastImage(fileDir, imageNameRoot, nDup=3):
  """
  persistLastImage(fileDir, imageNameRoot, nDup)

  Will copy the last image in the series nDup times, so it persists a bit longer in animation.

  Parameters:
  - fileDir: the directory where the files are saved
  - imageNameRoot: the complete root of the animation images (e.g. uwincm_anim_day1_)
  - nDup: number of times the last image is duplicated
  """

  fls = sorted([el for el in os.listdir(fileDir) if imageNameRoot in el])
  if len(fls) > 0:
    working = True
    frame_num = [int(el[-6:-4]) for el in fls]
    for fl in range(nDup):
      cmd = ['cp', fileDir+imageNameRoot+'{:02d}'.format(frame_num[-1])+fls[-1][-4:], fileDir+imageNameRoot+'{:02d}'.format(frame_num[-1]+fl+1)+fls[-1][-4:]]

      subprocess.call(cmd)
  else:
    working = False

  return working


def createAnimation(fileDir, imageNameRoot, outName, delay=50, loop=0):
  """
  createAnimation(fileDir, imageNameRoot, delay=50, loop=0, outName)

  Will create a .gif animation of the provided images and save it.

  Parameters:
  - fileDir: the directory where the files are saved
  - imageNameRoot: the complete root of the animation images (e.g. uwincm_anim_day1_)
  - outName: the name of the output file (e.g. something.gif)
  - delay: delay in ms
  - loop: 0 means repeating
  """
  cmd = ['convert', '-delay', str(delay), fileDir+imageNameRoot+'*', '-loop', str(loop), '+repage', fileDir+outName]
  subprocess.call(cmd)

  return


def animationSteps(fileDir, imageNameRoot, outName):
  """
  animationSteps(fileDir, imageNameRoot, outName)

  Sequentially calls persistLastImage, then createAnimation (if possible), to output an animation.

  Parameters:
  - fileDir: the directory where the files are saved
  - imageNameRoot: the complete root of the animation images (e.g. uwincm_anim_day1_)
  - outName: the name of the output file (e.g. something.gif)
  """

  dl = persistLastImage(fileDir, imageNameRoot)

  if dl:
    createAnimation(fileDir, imageNameRoot, outName)
  else:
    print('... ... Missing images - cannot create animation')

  return





if clearDirectory:
  print('Removing existing files.')
  existing_files = [el for el in sorted(os.listdir(cropDir)) if 'logo_cpexaw.png' not in el]
  for fl in existing_files:
    os.remove(cropDir+fl)

  print('Copying over CPEX-AW logo.')
  fls = os.listdir(saveDir)
  cmd = ['cp', saveDir+'logo_cpexaw.png', cropDir+'logo_cpexaw.png']
  subprocess.call(cmd)
  cmd = ['convert', cropDir+'logo_cpexaw.png', '-trim',  '-border',  '0',  '+repage', cropDir+'logo_cpexaw.png']
  subprocess.call(cmd)
  print('Removing existing files complete.')

  time.sleep(10)

print('')
print('')
print('')
print('')
print('')


if readSwitches:
  print("Reading True/False switches from switches_process.txt")
  fl = open(forecastDir + './supplementary/switches_process.txt', 'r')
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

if processImages:
  all_files = sorted([el for el in os.listdir(saveDir)])
  print('Processing images.')

  if switches['UTAH_dryrun']:
    print('... UTAH precipitation and ECMWF precipitation - model day 1.')
    fls_left = sorted([el for el in os.listdir(saveDir) if 'ECMWF_mslp_pcpn_day1_anim' in el])
    fls_right = sorted([el for el in os.listdir(saveDir) if 'uutah_slp_rain_day1_anim' in el])
    if len(fls_left) <= len(fls_right):
      for num, fl in enumerate(fls_left):
        cmd = ['convert', '+append', saveDir+fl, saveDir+fls_right[num], cropDir+'UtahEcmwf_joint_precip_day1_anim_' + '{:02d}'.format(num) + '.jpg']
        subprocess.call(cmd)
    else:
      print('... ... The numbers of images for fields do not match.')


    animationSteps(cropDir, 'UtahEcmwf_joint_precip_day1_anim_', 'UtahEcmwf_joint_precip_day1_movie.gif')

    print('... UTAH precipitation and ECMWF precipitation - model day 2.')
    fls_left = sorted([el for el in os.listdir(saveDir) if 'ECMWF_mslp_pcpn_day2_anim' in el])
    fls_right = sorted([el for el in os.listdir(saveDir) if 'uutah_slp_rain_day2_anim' in el])
    if len(fls_left) <= len(fls_right):
      for num, fl in enumerate(fls_left):
        cmd = ['convert', '+append', saveDir+fl, saveDir+fls_right[num], cropDir+'UtahEcmwf_joint_precip_day2_anim_' + '{:02d}'.format(num) + '.jpg']
        subprocess.call(cmd)
    else:
      print('... ... The numbers of images for fields do not match.')


    animationSteps(cropDir, 'UtahEcmwf_joint_precip_day2_anim_', 'UtahEcmwf_joint_precip_day2_movie.gif')


  if switches['nhc_analysis']:
    print('... NHC analysis - cropping image and adding St.Croix and Sal locations.')
    current_files = [el for el in all_files if 'NHC_surface_analysis.png' in el]

    marker_radius = 5
    for fl in current_files:
      cmd = ['convert', saveDir+fl, '-crop', '1268x648+1100+350', '+repage', cropDir+fl]
      subprocess.call(cmd)

      #xPt, yPt = 952, 445
      xPt, yPt = 370, 430
      cmd = ['convert', cropDir+fl, '-fill', 'red', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)

      xPt, yPt = 952, 445
      cmd = ['convert', cropDir+fl, '-fill', 'red', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)

    current_files = [el for el in all_files if 'NHC_' in el and 'surface_analysis' not in el]

    marker_radius = 5
    for fl in current_files:
      cmd = ['convert', saveDir+fl, '-crop', '900x665+0+0', '+repage', cropDir+fl]
      subprocess.call(cmd)

      xPt, yPt = 380, 433
      cmd = ['convert', cropDir+fl, '-fill', 'blue', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)

      xPt, yPt = 775, 445
      cmd = ['convert', cropDir+fl, '-fill', 'blue', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)


  if switches['mimic_tpw']:
    print('... MIMIC-TPW - cropping image and adding St.Croix and Sal locations.')
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


  if switches['meteosat_sat']:
    print('... Meteosat-11 - cropping image, adding Sal location, and adding a Celsius IR scale.')
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



  if switches['GOES16_sat']:
    print('... GOES-16 - cropping image, adding St. Croix location, and adding a Celsius IR scale.')
    current_files = sorted([el for el in all_files if 'Goes16' in el])

    marker_radius = 12
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
        print('      ... Color IR - adding Celsius color scale on side.')
        #cmd = []
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


  if switches['brammer_tropical_waves']:
    print('   ... Tropical wave analysis - cropping image and adding St.Croix amd Sal locations.')
    current_files = [el for el in all_files if 'Brammer' in el]

    marker_radius = 4
    for fl in current_files:
      cmd = ['convert', saveDir+fl, '-crop', '990x388+10+0', '+repage', cropDir+fl]
      subprocess.call(cmd)

      xPt, yPt = 662, 243
      cmd = ['convert', cropDir+fl, '-fill', 'red', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)

      xPt, yPt = 295, 237
      cmd = ['convert', cropDir+fl, '-fill', 'red', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)



  if switches['sal_split']:
    print('   ... SAL dust split image - cropping image and adding St.Croix location.')
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


  if switches['uwincm_clouds_animation'] or switches['uwincm_clouds_current'] or switches['uwincm_clouds']:
    print('   ... UWIN-CM - clouds and TPW - cropping image and adding St.Croix and Sal locations.')
    current_files = sorted([el for el in all_files if 'uwincm_clouds' in el])

    marker_radius = 5
    for fl in current_files:
      cmd = ['convert', saveDir+fl, '-crop', '740x400+25+125', '+repage', cropDir+fl]
      subprocess.call(cmd)

      # st croix
      #largeD02
      #xPt, yPt = 120, 165
      #smallerD02 - 08-19
      xPt, yPt = 303, 165
      cmd = ['convert', cropDir+fl, '-fill', 'white', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)

      # cape verde
      #largeD02
#       xPt, yPt = 615, 180
#       #smallerD02 - 08-19
#       xPt, yPt = 615, 180
#       cmd = ['convert', cropDir+fl, '-fill', 'white', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
#       subprocess.call(cmd)


  if switches['uwincm_precipitation'] or switches['uwincm_precipitation_animation']:
    print('   ... UWIN-CM - precipitation - cropping image and adding St.Croix and Sal locations.')
    current_files = sorted([el for el in all_files if 'uwincm_precip' in el])

    marker_radius = 5

    for fl in current_files:
      cmd = ['convert', saveDir+fl, '-crop', '740x400+25+125', '+repage', cropDir+fl]
      subprocess.call(cmd)

      # st croix
      #xPt, yPt = 117, 230
      #xPt, yPt = 120, 195
      #xPt, yPt = 120, 165
      #smallerD02 - 08-19
      xPt, yPt = 303, 165
      cmd = ['convert', cropDir+fl, '-fill', 'black', '-stroke', 'red', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)

      # cape verde
      #xPt, yPt = 612, 243
      #xPt, yPt = 615, 210
#       xPt, yPt = 615, 180
#       cmd = ['convert', cropDir+fl, '-fill', 'black', '-stroke', 'red', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
#       subprocess.call(cmd)


  if switches['uutah_precipitation'] or switches['uutah_precipitation_animation']:
    print('   ... Unversity of Utah - precipitation - cropping image and adding St.Croix location.')
    current_files = sorted([el for el in all_files if 'uutah_precip' in el])

    marker_radius = 5
    xPt, yPt = 177, 150
    for fl in current_files:
      cmd = ['convert', saveDir+fl, '-crop', '980x700+0+0', '+repage', cropDir+fl]
      subprocess.call(cmd)


      cmd = ['convert', cropDir+fl, '-fill', 'black', '-stroke', 'red', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)


  if switches['uwincm_boundaryLayer'] or switches['uwincm_boundaryLayer_animation']:
    print('   ... UWIN-CM - boundary layer - cropping image and adding St.Croix and Sal locations.')
    current_files = sorted([el for el in all_files if 'uwincm_boundaryLayer' in el])

    marker_radius = 5
    for fl in current_files:
      cmd = ['convert', saveDir+fl, '-crop', '740x400+25+125', '+repage', cropDir+fl]
      subprocess.call(cmd)


      #xPt, yPt = 117, 230
      #xPt, yPt = 120, 195
      #xPt, yPt = 120, 165
      #smallerD02 - 08-19
      xPt, yPt = 303, 165
      cmd = ['convert', cropDir+fl, '-fill', 'red', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)

      # cape verde
      #xPt, yPt = 612, 243
      #xPt, yPt = 615, 210
#       xPt, yPt = 615, 180
#       cmd = ['convert', cropDir+fl, '-fill', 'red', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
#       subprocess.call(cmd)


  if switches['uwincm_surfaceWind'] or switches['uwincm_surfaceWind_animation']:
    print('   ... UWIN-CM - surface winds - cropping image and adding St.Croix and Sal locations.')
    current_files = sorted([el for el in all_files if ('uwincm_surfaceWind' in el)])

    marker_radius = 4
    for fl in current_files:
      cmd = ['convert', saveDir+fl, '-crop', '725x489+35+52', '+repage', cropDir+fl]
      subprocess.call(cmd)

      #xPt, yPt = 240, 300
      xPt, yPt = 265, 280
      cmd = ['convert', cropDir+fl, '-fill', 'white', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)

      # cape verde
      #xPt, yPt = 595, 310
      xPt, yPt = 567, 288
      cmd = ['convert', cropDir+fl, '-fill', 'white', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)


  if switches['uwincm_650mbRH'] or switches['uwincm_650mbRH_animation']:
    print('   ... UWIN-CM - 650mb RH - cropping image and adding St.Croix and Sal locations.')
    current_files = sorted([el for el in all_files if 'uwincm_650mbRH' in el])

    marker_radius = 4
    for fl in current_files:
      cmd = ['convert', saveDir+fl, '-crop', '725x489+35+52', '+repage', cropDir+fl]
      subprocess.call(cmd)

      #xPt, yPt = 240, 300
      xPt, yPt = 265, 280
      cmd = ['convert', cropDir+fl, '-fill', 'red', '-stroke', 'white', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)

      # cape verde
      #xPt, yPt = 595, 310
      xPt, yPt = 567, 288
      cmd = ['convert', cropDir+fl, '-fill', 'red', '-stroke', 'white', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)


  if switches['icap_aerosol_ensemble']:
    print('   ... ICAP aerosol ensemble - cropping image and adding St.Croix and Sal locations.')
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


  if switches['nasa_geos']:
    print('   ... NASA GEOS images - cropping image and adding St. Croix and Sal locations.')
    current_files = sorted([el for el in all_files if 'GEOS_700mb_outlook' in el])

    marker_radius = 5
    for fl in current_files:
      cmd = ['convert', saveDir+fl, '-crop', '984x688+0+80', '+repage', cropDir+fl]
      subprocess.call(cmd)


      xPt, yPt = 360, 325
      cmd = ['convert', cropDir+fl, '-fill', 'red', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)

      xPt, yPt = 685, 335
      cmd = ['convert', cropDir+fl, '-fill', 'red', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)


    current_files = sorted([el for el in all_files if ('GEOS_dust' in el) and ('vert' not in el)])

    marker_radius = 5
    for fl in current_files:
      cmd = ['convert', saveDir+fl, '-crop', '984x688+0+80', '+repage', cropDir+fl]
      subprocess.call(cmd)

      xPt, yPt = 360, 325
      cmd = ['convert', cropDir+fl, '-fill', 'white', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)

      xPt, yPt = 685, 335
      cmd = ['convert', cropDir+fl, '-fill', 'white', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)


    current_files = sorted([el for el in all_files if ('GEOS_dust' in el) and ('N.png' in el)])

    marker_radius = 8
    xPt, yPt = 385, 619
    for fl in current_files:
      cmd = ['convert', saveDir+fl, '-crop', '1021x654+2+57', '+repage', cropDir+fl]
      subprocess.call(cmd)


      xPt, yPt = 385, 619
      cmd = ['convert', cropDir+fl, '-fill', 'white', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)

      xPt, yPt = 750, 619
      cmd = ['convert', cropDir+fl, '-fill', 'white', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)


    current_files = sorted([el for el in all_files if ('GEOS_dust' in el) and ('W.png' in el)])

    marker_radius = 8
    for fl in current_files:
      cmd = ['convert', saveDir+fl, '-crop', '1019x681+0+57', '+repage', cropDir+fl]
      subprocess.call(cmd)


      xPt, yPt = 510, 619
      cmd = ['convert', cropDir+fl, '-fill', 'white', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)


    current_files = sorted([el for el in all_files if ('GEOS_total_aot' in el)])

    marker_radius = 5
    for fl in current_files:
      cmd = ['convert', saveDir+fl, '-crop', '984x688+0+80', '+repage', cropDir+fl]
      subprocess.call(cmd)

      xPt, yPt = 360, 325
      cmd = ['convert', cropDir+fl, '-fill', 'blue', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)

      xPt, yPt = 685, 335
      cmd = ['convert', cropDir+fl, '-fill', 'blue', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)

    current_files = sorted([el for el in all_files if ('GEOS_' in el) and ('CloudFraction' in el)])

    marker_radius = 5
    for fl in current_files:
      cmd = ['convert', saveDir+fl, '-crop', '984x688+0+80', '+repage', cropDir+fl]
      subprocess.call(cmd)

      xPt, yPt = 360, 325
      cmd = ['convert', cropDir+fl, '-fill', 'red', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)

      xPt, yPt = 685, 335
      cmd = ['convert', cropDir+fl, '-fill', 'red', '-stroke', 'black', '-draw', 'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius), cropDir+fl]
      subprocess.call(cmd)



  print('Processing images complete.')
  time.sleep(10)

print('')
print('')
print('')
print('')
print('')



if joinSlideAnimations:
  print('Creating joint animations.')

  if switches['uwincm_surfaceWind_animation'] and switches['uwincm_650mbRH_animation']:

    if model_day1:
      print('... UWINCM Surface winds and 650 mb RH - model day 1.')

      fls_left = sorted([el for el in os.listdir(cropDir) if 'uwincm_surfaceWind_day1_anim' in el])
      fls_right = sorted([el for el in os.listdir(cropDir) if 'uwincm_650mbRH_day1_anim' in el])
      if len(fls_left) <= len(fls_right):
        for num, fl in enumerate(fls_left):
          cmd = ['convert', '+append', cropDir+fl, cropDir+fls_right[num], cropDir+'uwincm_joint_surfaceWind_650mbRH_day1_anim_' + '{:02d}'.format(num) + '.jpg']
          subprocess.call(cmd)
      else:
        print('... ... The numbers of images for fields do not match.')


      animationSteps(cropDir, 'uwincm_joint_surfaceWind_650mbRH_day1_anim_', 'uwincm_joint_surfaceWind_650mbRH_day1_movie.gif')


    if model_day2:
      print('... UWINCM Surface winds and 650 mb RH - model day 2.')

      fls_left = sorted([el for el in os.listdir(cropDir) if 'uwincm_surfaceWind_day2_anim' in el])
      fls_right = sorted([el for el in os.listdir(cropDir) if 'uwincm_650mbRH_day2_anim' in el])
      if len(fls_left) <= len(fls_right):
        for num, fl in enumerate(fls_left):
          cmd = ['convert', '+append', cropDir+fl, cropDir+fls_right[num], cropDir+'uwincm_joint_surfaceWind_650mbRH_day2_anim_' + '{:02d}'.format(num) + '.jpg']
          subprocess.call(cmd)
      else:
        print('... ... The numbers of images for fields do not match.')


      animationSteps(cropDir, 'uwincm_joint_surfaceWind_650mbRH_day2_anim_', 'uwincm_joint_surfaceWind_650mbRH_day2_movie.gif')


  if switches['uwincm_clouds_animation'] and switches['uwincm_boundaryLayer_animation']:

    if model_day1:
      print('... UWINCM clouds and boundary layer - model day 1.')
      fls_left = sorted([el for el in os.listdir(cropDir) if 'uwincm_clouds_day1_anim' in el])
      fls_right = sorted([el for el in os.listdir(cropDir) if 'uwincm_boundaryLayer_day1_anim' in el])
      if len(fls_left) <= len(fls_right):
        for num, fl in enumerate(fls_left):
          cmd = ['convert', '+append', cropDir+fl, cropDir+fls_right[num], cropDir+'uwincm_joint_clouds_boundaryLayer_day1_anim_' + '{:02d}'.format(num) + '.jpg']
          subprocess.call(cmd)
      else:
        print('... ... The numbers of images for fields do not match.')


      animationSteps(cropDir, 'uwincm_joint_clouds_boundaryLayer_day1_anim_', 'uwincm_joint_clouds_boundaryLayer_day1_movie.gif')


    if model_day2:
      print('... UWINCM clouds and boundary layer - model day 2.')
      fls_left = sorted([el for el in os.listdir(cropDir) if 'uwincm_clouds_day2_anim' in el])
      fls_right = sorted([el for el in os.listdir(cropDir) if 'uwincm_boundaryLayer_day2_anim' in el])
      if len(fls_left) <= len(fls_right):
        for num, fl in enumerate(fls_left):
          cmd = ['convert', '+append', cropDir+fl, cropDir+fls_right[num], cropDir+'uwincm_joint_clouds_boundaryLayer_day2_anim_' + '{:02d}'.format(num) + '.jpg']
          subprocess.call(cmd)
      else:
        print('... ... The numbers of images for fields do not match.')


      animationSteps(cropDir, 'uwincm_joint_clouds_boundaryLayer_day2_anim_', 'uwincm_joint_clouds_boundaryLayer_day2_movie.gif')


  if switches['uwincm_precipitation_animation'] and switches['uutah_precipitation_animation']:

    if model_day1:
      print('... UWINCM precipitation and U of Utah precipitation - model day 1.')
      fls_left = sorted([el for el in os.listdir(cropDir) if 'uwincm_precip_day1_anim' in el])
      fls_right = sorted([el for el in os.listdir(cropDir) if 'uutah_precip_day1_anim' in el])
      if len(fls_left) <= len(fls_right):
        for num, fl in enumerate(fls_left):
          cmd = ['convert', '+append', cropDir+fl, cropDir+fls_right[num], cropDir+'uwincm_joint_precip_day1_anim_' + '{:02d}'.format(num) + '.jpg']
          subprocess.call(cmd)
      else:
        print('... ... The numbers of images for fields do not match.')


      animationSteps(cropDir, 'uwincm_joint_precip_day1_anim_', 'uwincm_joint_precip_day1_movie.gif')

    if model_day2:
      print('... UWINCM precipitation and U of Utah precipitation - model day 2.')
      fls_left = sorted([el for el in os.listdir(cropDir) if 'uwincm_precip_day2_anim' in el])
      fls_right = sorted([el for el in os.listdir(cropDir) if 'uutah_precip_day2_anim' in el])
      if len(fls_left) <= len(fls_right):
        for num, fl in enumerate(fls_left):
          cmd = ['convert', '+append', cropDir+fl, cropDir+fls_right[num], cropDir+'uwincm_joint_precip_day2_anim_' + '{:02d}'.format(num) + '.jpg']
          subprocess.call(cmd)
      else:
        print('... ... The numbers of images for fields do not match.')


      animationSteps(cropDir, 'uwincm_joint_precip_day2_anim_', 'uwincm_joint_precip_day2_movie.gif')

    if switch['UTAH_dryrun']:
      print('... UTAH precipitation and ECMWF precipitation - model day 1.')
      fls_left = sorted([el for el in os.listdir(saveDir) if 'uutah_slp_rain_day1_anim' in el])
      fls_right = sorted([el for el in os.listdir(saveDir) if 'ECMWF_mslp_pcpn_day1_anim' in el])
      if len(fls_left) <= len(fls_right):
        for num, fl in enumerate(fls_left):
          cmd = ['convert', '+append', saveDir+fl, saveDir+fls_right[num], cropDir+'UtahEcmwf_joint_precip_day2_anim_' + '{:02d}'.format(num) + '.jpg']
          subprocess.call(cmd)
      else:
        print('... ... The numbers of images for fields do not match.')


      animationSteps(cropDir, 'UtahEcmwf_joint_precip_day2_anim_', 'UtahEcmwf_joint_precip_day2_movie.gif')





  moving_files=[      'ECMWF_mslp_pcpn_day1.gif',
                      'ECMWF_mslp_pcpn_day2.gif',
                      'ECMWF_mslp_wind_day1.gif',
                      'ECMWF_mslp_wind_day2.gif',
                      'ECMWF_mslp_pwat_day1.gif',
                      'ECMWF_mslp_pwat_day2.gif',
                      'ECMWF_midRH_day1.gif',
                      'ECMWF_midRH_day2.gif',
                      'ICON_mslp_pcpn_day1.gif',
                      'ICON_mslp_pcpn_day2.gif',
                      'uutah_sfcwind_day1_movie.gif',
                      'uutah_sfcwind_day2_movie.gif',
                      'uutah_tpw_olr_day1_movie.gif',
                      'uutah_tpw_olr_day2_movie.gif',
                      'uutah_slp_rain_day1_movie.gif',
                      'uutah_slp_rain_day2_movie.gif',
                      'uutah_rhght650_day1_movie.gif',
                      'uutah_rhght650_day2_movie.gif',
                      'uutah_PBLH_day1_movie.gif',
                      'uutah_PBLH_day2_movie.gif'
                      ]
  for ff in moving_files:
    cmd = ['cp', saveDir+ff, cropDir+'.']
    subprocess.call(cmd)

  print('Creating joint animations complete.')


  time.sleep(10)

print('')
print('')
print('')
print('')
print('')

if moveFinalImages:
  print('Moving final images and animations to ./figs_final.')


  list_of_images = ['logo_cpexaw.png',
                    'NHC_surface_analysis.png',
                    'MIMIC-TPW_latest.png',
                    'uwincm_clouds_current.jpg',
                    'AEW_Brammer.jpg',
                    'Goes16_Meteosat11_IRC.png',
                    'SAL_dryAir_split.jpg',
                    'GEOS_dust_aot.png',
                    'NHC_2day_outlook.png',
                    'NHC_5day_outlook.png',
                    'uwincm_joint_surfaceWind_650mbRH_day1_movie.gif',
                    'uwincm_joint_clouds_boundaryLayer_day1_movie.gif',
                    'uwincm_joint_precip_day1_movie.gif',
                    'uwincm_joint_surfaceWind_650mbRH_day2_movie.gif',
                    'uwincm_joint_clouds_boundaryLayer_day2_movie.gif',
                    'uwincm_joint_precip_day2_movie.gif',
                    'GEOS_dust_aot_vert_15N.png',
                    'GEOS_dust_aot_vert_20W.png',
                    'GEOS_dust_aot_day1.png',
                    'GEOS_dust_aot_day1_vert_15N.png',
                    'GEOS_dust_aot_day1_vert_20W.png',
                    'GEOS_dust_aot_day2.png',
                    'GEOS_dust_aot_day2_vert_15N.png',
                    'GEOS_dust_aot_day2_vert_20W.png',
                    'GEOS_total_aot.png',
                    'GEOS_total_aot_day1.png',
                    'GEOS_total_aot_day2.png',
                    'GEOS_lowCloudFraction_day1.png',
                    'GEOS_lowCloudFraction_day2.png',
                    'GEOS_midCloudFraction_day1.png',
                    'GEOS_midCloudFraction_day2.png',
                    'GEOS_highCloudFraction_day1.png',
                    'GEOS_highCloudFraction_day2.png',
                    'ICAP_aerosol_ensemble_96.png',
                    'ICAP_aerosol_ensemble_120.png',
                    'GEOS_700mb_outlook_movie.gif',
                    'ECMWF_mslp_pcpn_day1.gif',
                    'ECMWF_mslp_pcpn_day2.gif',
                    'ICON_mslp_pcpn_day1.gif',
                    'ICON_mslp_pcpn_day2.gif',
                    'UtahEcmwf_joint_precip_day1_movie.gif',
                    'UtahEcmwf_joint_precip_day2_movie.gif',
                    'uutah_sfcwind_day1_movie.gif',
                    'uutah_sfcwind_day2_movie.gif',
                    'uutah_tpw_olr_day1_movie.gif',
                    'uutah_tpw_olr_day2_movie.gif',
                    'uutah_slp_rain_day1_movie.gif',
                    'uutah_slp_rain_day2_movie.gif',
                    'uutah_rhght650_day1_movie.gif',
                    'uutah_rhght650_day2_movie.gif',
                    'uutah_PBLH_day1_movie.gif',
                    'uutah_PBLH_day2_movie.gif'
                    ]

    # additional images, when they become available:
    # 'AEW_Brammer.jpg'

  for fl in list_of_images:
    if os.path.isfile(cropDir+fl):
      os.system('cp ' + cropDir+fl + ' ' + finDir+fl)
    else:
      print('... ... ' + fl + ' not present and cannot be copied over.')


  print('Moving final images and animations complete.')
  time.sleep(10)
