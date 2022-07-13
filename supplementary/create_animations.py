"""
Author: Ajda Savarin
Created: July 19th 2021
University of Washington
asavarin@uw.edu

This program is used to create base animations for the CPEX-AW Forecasting team.

Required packages: os, subprocess, time.


NOTE: Read through the True/False switches at the top of the script to make sure the ones you want are selected.

Updates:
 -
"""


import os
import subprocess
import time
from PIL import Image


readSwitches = True
createAnimations = True

model_day1 = model_day2 = True





nDup_frames = 3

forecastDir = './'
saveDir = './figs/'
cropDir = './figs_cropped/'
finDir = './figs_final/'

fl = open('./supplementary/list_of_downloaded_files.txt', 'r')
wanted_files = fl.readlines()
wanted_files = [line.rstrip() for line in wanted_files]
fl.close()

present_files = [fl for fl in os.listdir(saveDir)]
present_files_animation = [fl for fl in present_files if '_anim_' in fl]


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

  time.sleep(10)

print('')
print('')
print('')
print('')
print('')


if createAnimations:
  print('Creating model output animations.')


  if switches['uwincm_surfaceWind_animation']:
    current_fls = [fl for fl in present_files_animation if 'uwincm_surfaceWind_day1_anim_' in fl]
    if len(current_fls) == 12:
      if model_day1:
        print('... UWINCM surface winds - model day 1')
        animationSteps(saveDir, 'uwincm_surfaceWind_day1_anim_', 'uwincm_surfaceWind_day1_movie.gif')

    current_fls = [fl for fl in present_files_animation if 'uwincm_surfaceWind_day2_anim_' in fl]
    if len(current_fls) == 12:
      if model_day2:
        print('... UWINCM surface winds - model day 2')
        animationSteps(saveDir, 'uwincm_surfaceWind_day2_anim_', 'uwincm_surfaceWind_day2_movie.gif')


  if switches['uwincm_650mbRH_animation']:
    current_fls = [fl for fl in present_files_animation if 'uwincm_650mbRH_day1_anim_' in fl]
    if len(current_fls) == 12:
      if model_day1:
        print('... UWINCM 650mb moisture - model day 1')
        animationSteps(saveDir, 'uwincm_650mbRH_day1_anim_', 'uwincm_650mbRH_day1_movie.gif')

    current_fls = [fl for fl in present_files_animation if 'uwincm_650mbRH_day2_anim_' in fl]
    if len(current_fls) == 12:
      if model_day2:
        print('... UWINCM 650mb moisture - model day 2')
        animationSteps(saveDir, 'uwincm_650mbRH_day2_anim_', 'uwincm_650mbRH_day2_movie.gif')


  if switches['uwincm_clouds_animation']:
    current_fls = [fl for fl in present_files_animation if 'uwincm_clouds_day1_anim_' in fl]
    if len(current_fls) == 12:
      if model_day1:
        print('... UWINCM clouds - model day 1')
        animationSteps(saveDir, 'uwincm_clouds_day1_anim_', 'uwincm_clouds_day1_movie.gif')

    current_fls = [fl for fl in present_files_animation if 'uwincm_clouds_day2_anim_' in fl]
    if len(current_fls) == 12:
      if model_day2:
        print('... UWINCM clouds - model day 2')
        animationSteps(saveDir, 'uwincm_clouds_day2_anim_', 'uwincm_clouds_day2_movie.gif')


  if switches['uwincm_precipitation_animation']:
    current_fls = [fl for fl in present_files_animation if 'uwincm_precip_day1_anim_' in fl]
    if len(current_fls) == 12:
      if model_day1:
        print('... UWINCM precipitation - model day 1')
        animationSteps(saveDir, 'uwincm_precip_day1_anim_', 'uwincm_precip_day1_movie.gif')

    current_fls = [fl for fl in present_files_animation if 'uwincm_precip_day2_anim_' in fl]
    if len(current_fls) == 12:
      if model_day2:
        print('... UWINCM precipitation - model day 2')
        animationSteps(saveDir, 'uwincm_precip_day2_anim_', 'uwincm_precip_day2_movie.gif')


  if switches['uwincm_boundaryLayer_animation']:
    current_fls = [fl for fl in present_files_animation if 'uwincm_boundaryLayer_day1_anim_' in fl]
    if len(current_fls) == 12:
      if model_day1:
        print('... UWINCM boundary layer - model day 1')
        animationSteps(saveDir, 'uwincm_boundaryLayer_day1_anim_', 'uwincm_boundaryLayer_day1_movie.gif')

    current_fls = [fl for fl in present_files_animation if 'uwincm_boundaryLayer_day2_anim_' in fl]
    if len(current_fls) == 12:
      if model_day2:
        print('... UWINCM boundary layer - model day 2')
        animationSteps(saveDir, 'uwincm_boundaryLayer_day2_anim_', 'uwincm_boundaryLayer_day2_movie.gif')


  if switches['uutah_precipitation_animation']:
    current_fls = [fl for fl in present_files_animation if 'uutah_precip_day1_anim_' in fl]
    if len(current_fls) == 12:
      if model_day1:
        print('... UofUtah precipitation - model day 1')
        animationSteps(saveDir, 'uutah_precip_day1_anim_', 'uutah_precip_day1_movie.gif')

    current_fls = [fl for fl in present_files_animation if 'uutah_precip_day2_anim_' in fl]
    if len(current_fls) == 12:
      if model_day2:
        print('... UofUtah precipitation - model day 2')
        animationSteps(saveDir, 'uutah_precip_day2_anim_', 'uutah_precip_day2_movie.gif')


  if switches['nasa_geos']:
    print('... NASA GEOS 700mb winds')
    current_fls = [fl for fl in present_files_animation if 'GEOS_700mb_outlook_anim_' in fl]
    if len(current_fls) == 12:
      animationSteps(saveDir, 'GEOS_700mb_outlook_anim_', 'GEOS_700mb_outlook_movie.gif')


  if switches['ECMWF_prediction']:
      var=['ECMWF_mslp_wind', 'ECMWF_midRH', 'ECMWF_mslp_pwat', 'ECMWF_mslp_pcpn']
      for vv in var:
          images=[]
          if vv=='ECMWF_mslp_pcpn':
              cmd=['cp', './figs/ECMWF_mslp_pcpn_anim_01.png', './figs/ECMWF_mslp_pcpn_anim_00.png']
              subprocess.call(cmd)
          for num in range(0,8):
              images.append(Image.open('./figs/'+vv+'_anim_'+"{:02d}".format(num)+'.png'))
          for rep in range(2):
              images.append(Image.open('./figs/'+vv+'_anim_'+"{:02d}".format(num)+'.png'))
          images[0].save('./figs/'+vv+'_day0.gif', save_all=True, append_images=images[1:], optimize=False, duration=500, loop=0)

          images=[]
          for num in range(0+8,8+8):
              images.append(Image.open('./figs/'+vv+'_anim_'+"{:02d}".format(num)+'.png'))
          for rep in range(2):
              images.append(Image.open('./figs/'+vv+'_anim_'+"{:02d}".format(num)+'.png'))
          images[0].save('./figs/'+vv+'_day1.gif', save_all=True, append_images=images[1:], optimize=False, duration=500, loop=0)

          images=[]
          for num in range(0+16,8+16):
              images.append(Image.open('./figs/'+vv+'_anim_'+"{:02d}".format(num)+'.png'))
          for rep in range(2):
              images.append(Image.open('./figs/'+vv+'_anim_'+"{:02d}".format(num)+'.png'))
          images[0].save('./figs/'+vv+'_day2.gif', save_all=True, append_images=images[1:], optimize=False, duration=500, loop=0)

  if switches['GFS_prediction']:
      var=['GFS_mslp_wind', 'GFS_midRH', 'GFS_mslp_pwat', 'GFS_mslp_pcpn']
      for vv in var:
          if vv=='GFS_mslp_pcpn':
              cmd=['cp', './figs/GFS_mslp_pcpn_anim_01.png', './figs/GFS_mslp_pcpn_anim_00.png']
              subprocess.call(cmd)
          images=[]
          for num in range(0,4):
              images.append(Image.open('./figs/'+vv+'_anim_'+"{:02d}".format(num)+'.png'))
          for rep in range(2):
              images.append(Image.open('./figs/'+vv+'_anim_'+"{:02d}".format(num)+'.png'))
          images[0].save('./figs/'+vv+'_day0.gif', save_all=True, append_images=images[1:], optimize=False, duration=500, loop=0)

          images=[]
          for num in range(0+4,4+4):
              images.append(Image.open('./figs/'+vv+'_anim_'+"{:02d}".format(num)+'.png'))
          for rep in range(2):
              images.append(Image.open('./figs/'+vv+'_anim_'+"{:02d}".format(num)+'.png'))
          images[0].save('./figs/'+vv+'_day1.gif', save_all=True, append_images=images[1:], optimize=False, duration=500, loop=0)

          images=[]
          for num in range(0+8,4+8):
              images.append(Image.open('./figs/'+vv+'_anim_'+"{:02d}".format(num)+'.png'))
          for rep in range(2):
              images.append(Image.open('./figs/'+vv+'_anim_'+"{:02d}".format(num)+'.png'))
          images[0].save('./figs/'+vv+'_day2.gif', save_all=True, append_images=images[1:], optimize=False, duration=500, loop=0)

  if switches['ICON_prediction']:
      var=['iCON_mslp_wind', 'ICON_mslp_pcpn']
      for vv in var:
          images=[]
          if vv=='ICON_mslp_pcpn':
              cmd=['cp', './figs/ICON_mslp_pcpn_anim_01.png', './figs/ICON_mslp_pcpn_anim_00.png']
              subprocess.call(cmd)
          for num in range(0,8):
              images.append(Image.open('./figs/'+vv+'_anim_'+"{:02d}".format(num)+'.png'))
          for rep in range(2):
              images.append(Image.open('./figs/'+vv+'_anim_'+"{:02d}".format(num)+'.png'))
          images[0].save('./figs/'+vv+'_day0.gif', save_all=True, append_images=images[1:], optimize=False, duration=500, loop=0)

          images=[]
          for num in range(0+8,8+8):
              images.append(Image.open('./figs/'+vv+'_anim_'+"{:02d}".format(num)+'.png'))
          for rep in range(2):
              images.append(Image.open('./figs/'+vv+'_anim_'+"{:02d}".format(num)+'.png'))
          images[0].save('./figs/'+vv+'_day1.gif', save_all=True, append_images=images[1:], optimize=False, duration=500, loop=0)

          images=[]
          for num in range(0+16,8+16):
              images.append(Image.open('./figs/'+vv+'_anim_'+"{:02d}".format(num)+'.png'))
          for rep in range(2):
              images.append(Image.open('./figs/'+vv+'_anim_'+"{:02d}".format(num)+'.png'))
          images[0].save('./figs/'+vv+'_day2.gif', save_all=True, append_images=images[1:], optimize=False, duration=500, loop=0)

  print('Creating model output animations complete.')
