#! /usr/bin/env python
# Procedure written by Masayuki Kuzuhara (Tokyo Tech)
# email: m.kuzuhara@nao.ac.jp
# last update:  March 20, 2016
# You can freely use this software without MK's permission and adding MK to your co-author list.  However, please don't re-distribute this to others. Also, please use this, sharing risks.

# modified to match py27 by TU 
# 2019 Feb

'''

usage:  

1)
> python circ_conv.py XXXX.fits aperture_diameter

2)  Before doing convlution, the input image is normalized by TIME.

> python circ_conv.py XXXX.fits aperture_diameter TIME

'''

###### import used modules ##########

import numpy as np
import scipy.signal as scisig
from astropy.io import fits
import sys
#####################################


def make_aperture(diameter):

    if round(diameter) % 2 == 0:

       add_size = 3

    else:
     
       add_size = 4  

    print 'aperture diameter = %s (pix)' %(int(round(diameter)))

    kernel = np.ones((int(round(diameter))+add_size,int(round(diameter))+add_size))
    
    x_part = np.arange(0,np.shape(kernel)[0],1) - np.shape(kernel)[0]//2
    y_part = np.arange(0,np.shape(kernel)[1],1) - np.shape(kernel)[1]//2

    x, y = np.meshgrid(x_part, y_part)

    r = np.sqrt(x**2+y**2)

    used_elements = np.where(r>diameter/2.)
    
    kernel[used_elements] = 0  ### elements of r>diameter/2 is set to be zero

    return kernel

def circ_conv(im, kernel, exptime):

    nan_el = np.where(im != im)

    im[nan_el] = 0.

    if exptime is not None:

       im = im / exptime 

    convolved = scisig.convolve2d(im, kernel, boundary='symm', mode='same')

    return convolved

def work(input_file, app_di, exptime=None):

    im = fits.open(input_file)[0].data # convolved image
    hd = fits.open(input_file)[0].header # and its header

    kernel = make_aperture(app_di) # make convolution kernel

    output = circ_conv(im, kernel, exptime) # make convolved image
   
    hd.set("normtime", str(exptime), 'normalized by this value')
    hd.set("convD", str(app_di), 'convolution with this diameter aperture')

    fits.writeto('conv_D'+str(app_di)+"_"+input_file, output, hd) # output

#### operation part ########
if __name__ == "__main__":

    input_file = sys.argv[1]
    app_di = float(sys.argv[2]) # aperture diameter

    if len(sys.argv) == 4:

       exptime = float(sys.argv[3])

    else:

       exptime = None

    work(input_file, app_di, exptime)
