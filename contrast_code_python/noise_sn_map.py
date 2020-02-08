import sys
import numpy as np
from numpy import linspace
from astropy.io import fits
import scipy.interpolate
from scipy.interpolate import UnivariateSpline
from math import sqrt

#### make noise-map frame from data file of noises ######
#### In input file, noise should be on the 4th column ###

def noise_interp(im, sep, noise):

   s = scipy.interpolate.interp1d(sep,noise,kind='linear',bounds_error=False)

   x = np.arange(0,im.shape[1],1)
   y = np.arange(0,im.shape[0],1)

   x, y = np.meshgrid(x, y)
   xcenter = im.shape[1]//2
   ycenter = im.shape[0]//2

   r = np.sqrt((x-xcenter)**2+(y-ycenter)**2)

   smoothed_data = np.array([sep, s(sep) ])

   noise_map = s(r.reshape(-1)).reshape(r.shape)

   return noise_map
   
def snmap(im, noise):  

    sn = im / noise

    fits.writeto('snmap.fits', sn, overwrite=True)

if __name__ == "__main__":

   if len(sys.argv) == 1:
     print 'usage'
     print 'python noise_sn_map.py convolved_image noise.dat'

   im = fits.open(sys.argv[1])[0].data ## convolved image

   #### noise data should be on the 4th column ###
   noise_data = np.loadtxt(sys.argv[2], usecols=(0,3), dtype=str)
   
   sep = np.array(noise_data[:,0], dtype=float)
   oned_noise = np.array(noise_data[:,1], dtype=str)
   
   ####### remove nan ############ 
   nan_sep = np.where(oned_noise != 'all_nan')
   oned_noise = oned_noise[nan_sep]
   sep = sep[nan_sep]
   ###############################

   oned_noise = np.array(oned_noise, dtype=float)
   
   noise = noise_interp(im, sep, oned_noise)
 
   fits.writeto('noise_map.fits', noise, overwrite=True)
 
   snmap(im, noise)
