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
#today = datetime.strptime('2021-07-18', '%Y-%m-%d')
today = today.replace(hour=0, minute=0, second=0, microsecond=0)
yesterday = today - timedelta(days=1)
forecast_day1 = today + timedelta(days=1)
forecast_day2 = today + timedelta(days=2)
nFrames_uwincm = 12
still_image_forecast_hr = 16
dust_xLon = 15 # 20 degrees N
dust_xLat = 60 # 60 degrees W
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
