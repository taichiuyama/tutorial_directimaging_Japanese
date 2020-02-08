#! /usr/bin/env python

# interface module to run contrat_pr and investigate the noise profile as a function of radius from the star

# Procedure written by Masayuki Kuzuhara (Tokyo Tech)
# modification record: March 3 2013
# modification record: June 16 2015
# modification record: March 01 2016 to implement sigma cliping option
# last update March 13, 2016 to write calculation width in final output

# usage: python contrast.py fits_file_for_contrast_measure FWHM start_radius max_radius step (mask_position_txt_file; option)

# mask position should be fits/IDL coordinate system.

######## give the mask size and center of image ########### 
######## that you'd like to investigate        ###########

mask_size = 5.6*2
#center = 1000
#center = 1433


##### Sigma clipping #####################
#If you do not use sigma_clip, please describe 
# sigma_clip = None
# sigma_clip = 5.  (+5 sigma pixels are excluded in calculations)

sigma_clip = 5.

#############################

from contrast_pr import *
import sys
from astropy.io import fits
import csv
from csv import *
from numpy import *

openfile = str(sys.argv[1])
FWHM = float(sys.argv[2])
start_r = float(sys.argv[3])
rmax = float(sys.argv[4])
step = float(sys.argv[5])
mode = 'entire'

data = fits.open(openfile)


######### treatment of mask #############
#########################################

if len(sys.argv) == 7:

 maskdata = str(sys.argv[6])
 openmask = open(maskdata,"r")

 mask_posi = []

 for row in csv.reader(openmask, delimiter=" "):

  mask_posi.append([float(row[0]),float(row[1])])

###### mask size from command line #######

if len(sys.argv) == 8:

     if "*" in sys.argv[7]:

        mask_size = float(sys.argv[7].split("*")[0]) * float(sys.argv[7].split("*")[1])

     else:

        mask_size = float(sys.argv[7])

else:

     pass

########################################

scidata=data[0].data
header_primary = fits.getheader(openfile)
size=float(header_primary['NAXIS1'])

try:
    center
except NameError:
    center = size//2

#center = size/2

try: 
 test = mask_posi
 print '#using mask and position number = ',len(mask_posi)
 
 for oo in range(len(mask_posi)):

  mask_x = float(mask_posi[oo][0])
  mask_y = float(mask_posi[oo][1])

  print '#mask position', mask_x, mask_y

  mask_size=float(mask_size)

  scidata[mask_y-mask_size:mask_y+mask_size,mask_x-mask_size:mask_x+mask_size] = float(nan)

except NameError:
 pass


center_x=center; center_y=center

print '#x and y center', center_x, center_y

print '#width in calculation', FWHM 

print '#Radius,  ', 'anulus radius median,  ', 'Mean,  ',  'Standard Deviation'

if sigma_clip is None:
 
   sigma_clip = None

else:

   print '#using '+str(sigma_clip)+"sigma clipping"   
   sigma_clip = float(sigma_clip)

contrast_pr(scidata,FWHM,rmax,center_x,center_y,start_r=start_r,mode=mode,step=step,cliping=sigma_clip)
