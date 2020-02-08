#! /usr/bin/env python

# calculation of mean and standard deviation in anuli
# Authored by Masayuki Kuzuhara (email: m.kuzuhara@geo.titech.ac.jp)
# Redistribution of this code is not permitted
# Please use this sharing your own risk
# modification record: 31 Oct 2010
# modification record: 21 Aug 2014 for speed up
# modification record: 16 June, 2015 for clarification
# last updte: 29 Feb, 2016 for clarification 

'''
This code gives you the measured noises as a function of radius from the center.
The input parameters are following:

    1 -- scidata:  image fits file
    2 -- FWHM:     width of anulus at which noise is estimated
    3 -- center_x:   stellar center x
    4 -- center_y:   stellar center y
    5 -- start_r: start point for contrast calculation
    6 -- step (option): step number for contrast anulus
    7 -- mode (option):  currently, only "entire" mode can be selected
        using "entire" mode allows you to calculate the noise function 
        for the entere image area
    8 -- cliping (option): If you want to remove outliers greather \\
            than +XX sigma (you can set XX), use this option

'''

from astropy.io import fits
import sys
import getopt
import numpy as np
from numpy import *
from array import *
import scipy.stats as stats

def contrast_pr(scidata,FWHM,u,center_x,center_y,start_r=0,step=None, mode=None, cliping=None):

    xc=center_y;  yc=center_y
    FWHM = float(FWHM)
    u = float(u)

    if step is None:

       step = FWHM/2.0

    xarray = np.arange(0,np.shape(scidata)[1],1)
    yarray = np.arange(0,np.shape(scidata)[0],1)

    x, y = np.meshgrid(xarray, yarray) 
    theta = np.arctan2(x-xc,y-yc)*180./np.pi
    radius = np.sqrt((x-xc)**2+(y-yc)**2)


    ######### below, noise is caclulated   ################# 

    if not mode:

       ###### for single anulus #############
      
       calc_index = np.where( (radius <= float(u)+float(FWHM/2.0)) \
               & (radius >= float(u)-float(FWHM/2.0)))

      
       new_radius = radius[calc_index]
       calc = scidata[calc_index]

       ####### remove nan ############
       nanindex = np.where(calc != calc)
       calc = np.delete(calc, nanindex)
       ###############################

       if cliping is not None: 

          calc = stats.sigmaclip(calc, 100.*cliping, cliping)[0] 
          
       return u, np.median(new_radius), \
                     np.median(calc, ddof=1), \
                     np.std(calc, ddof=1)    

       #######################################

    ######### contract calculations on entrire region #########     

    elif mode == 'entire':
  
       radii = np.arange(start_r, float(u) + step, step) ### radius at which 
                                                   ### the noise is measured

       for i in range(len(radii)):

           if (radii[i] - FWHM/2.0) > 0:

               calc_index = np.where( (radius <= radii[i]+float(FWHM/2.0)) \
                 & (radius >= radii[i]-float(FWHM/2.0)))

               new_radius = radius[calc_index]
               calc = scidata[calc_index]

               except_nan_index = np.where(calc == calc)

               if len(except_nan_index[0]) > 1:

                  ####### remove nan ############
                  nanindex = np.where(calc != calc)
                  calc = np.delete(calc, nanindex)
                  ###############################

                  if cliping is not None: 

                     calc = stats.sigmaclip(calc, 100.*cliping, cliping)[0]

                  print radii[i], \
                    np.median(new_radius), \
                    np.median(calc), \
                    np.std(calc,ddof=1)
            
               else:

                  print radii[i], \
                    np.median(new_radius), \
                    'all_nan', \
                    'all_nan'
 
      ###################################################################  

if __name__ == "__main__":

  # sys.argv[2] is anulus width 
  # sys.argv[3] is the maximum radius
  # sys.argv[4] is step of calculations
  # if you prefer to use sigma cliping, 

  scidata = fits.open(sys.argv[1])[0].data ### data

  center_x = np.shape(scidata)[0]//2
  center_y = np.shape(scidata)[1]//2

  if len(sys.argv) >=5:

     contrast_pr(scidata, sys.argv[2], sys.argv[3], \
             center_x, center_y, step=float(sys.argv[4]),mode='entire') 
  
  else:
 
  # sys.argv[3] is the anulus radius

     rst = contrast_pr(scidata, sys.argv[2], sys.argv[3], center_x, center_y)
     
     print "radius, mean, noise" 

     print rst[0], rst[2], rst[3]

