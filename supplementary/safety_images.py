from PIL import Image
import os
import subprocess
import time




dir_file = './Davis_2022090112'
dir_save = './figs_safety'
dat ='2022090112'


# For creating gif
var=['RH650mb_V650mb','V10m']
for vv in var:
# Day 1
    images=[]
    for num in range(37,37+24,2):
        images.append(Image.open( os.path.join(dir_file,vv+'_'+dat+'_fcst_'+"{:02d}".format(num)+'hr.png') ))
    for rep in range(3):
        images.append(Image.open( os.path.join(dir_file,vv+'_'+dat+'_fcst_'+"{:02d}".format(num)+'hr.png') ))
        images[0].save( os.path.join(dir_save,vv+'_day1.gif'), save_all=True, append_images=images[1:], optimize=False, duration=500, loop=0)
# Day 2
    images=[]
    for num in range(61,61+24,2):
        images.append(Image.open( os.path.join(dir_file,vv+'_'+dat+'_fcst_'+"{:02d}".format(num)+'hr.png') ))
    for rep in range(3):
        images.append(Image.open( os.path.join(dir_file,vv+'_'+dat+'_fcst_'+"{:02d}".format(num)+'hr.png') ))
        images[0].save( os.path.join(dir_save,vv+'_day2.gif'), save_all=True, append_images=images[1:], optimize=False, duration=500, loop=0)


var=['TPW_OLR','PBLH','SLP_Rainrate']
for vv in var:
# Day 1
    images=[]
    for num in range(37,37+24,2):
        images.append(Image.open( os.path.join(dir_file,vv+'_'+dat+'_fcst_'+"{:02d}".format(num)+'hr.d02.png') ))
    for rep in range(3):
        images.append(Image.open( os.path.join(dir_file,vv+'_'+dat+'_fcst_'+"{:02d}".format(num)+'hr.d02.png') ))
        images[0].save( os.path.join(dir_save,vv+'_day1.gif'), save_all=True, append_images=images[1:], optimize=False, duration=500, loop=0)
# Day 2
    images=[]
    for num in range(61,61+24,2):
        images.append(Image.open( os.path.join(dir_file,vv+'_'+dat+'_fcst_'+"{:02d}".format(num)+'hr.d02.png') ))
    for rep in range(3):
        images.append(Image.open( os.path.join(dir_file,vv+'_'+dat+'_fcst_'+"{:02d}".format(num)+'hr.d02.png') ))
        images[0].save( os.path.join(dir_save,vv+'_day2.gif'), save_all=True, append_images=images[1:], optimize=False, duration=500, loop=0)


# for creating Videos

import cv2
import os

image_folder = dir_file
var='SLP_Rainrate'
video_name = os.path.join(dir_save,var+'.mp4')

imag = [img for img in sorted(os.listdir(image_folder)) if var in img]
images = [img for img in imag if 'd02' in img]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape
fps = 5

self_fourcc = cv2.VideoWriter_fourcc(*'MP4V')
video = cv2.VideoWriter(video_name, self_fourcc, fps, (width,height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()
