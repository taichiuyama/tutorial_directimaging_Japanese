# made by TU; 2017 Jul
# modified for VAMPIRES contrast limit
# basically no ND filter and exp time is not normalized (same exposure time as science images)

import numpy as np
import sys

def calc_contrast(file1,counts_unsat): #file1 = noise profile
 out1 = open("contrast.dat","w")

 # target information (optional)
 if len(sys.argv) == 4:
  mag_star = float(sys.argv[2])
  distance = float(sys.argv[3]) #in pc
  out2 = open("abs_magnitude.dat","w")
 else:
  print 'only contrast limits will be calculated; converting absolute magnitude requires distance and magnitude of the central star'

 # Kuzuhara-san's code uses all_nan, which is not readable in this code
 noise_data = np.loadtxt(file1,dtype=str)
 change_nan = np.where(noise_data=='all_nan')
 noise_data[change_nan] = np.nan

 #VAMPIRES-Halpha observation may or may not use ADI
 try:
  file2 = open('partial_subloci.dat',"r")
  selfsub_data = np.loadtxt(file2,dtype=float)
 except IOError:
  pass

 for i in range(len(noise_data)):

  r = noise_data[i][0]
  noise = float(noise_data[i][3])
  try:
   selfsub = selfsub_data[i][1]
  except NameError:
   selfsub = 1.

 # calculating 5 sigma detection limits
  contrast = 5.0*noise/(counts_unsat*selfsub)
  print >> out1, '%s %le' %(r,contrast)
  try:
   magnitude = mag_star - 2.5*np.log10(contrast) - 5.0*np.log10(distance/10.0)
   print >> out2, '%s %lf' %(r, magnitude)
  except NameError:
   pass

 out1.close()
 try:
  out2.close()
 except NameError:
  pass


if __name__ == "__main__":

 if len(sys.argv) == 1:
  print 'usage'
  print 'python detection_limit.py noise.dat counts_unsat mag_star(optional) distance(pc: optional)'
  sys.exit()

 # unsat frame information
 counts_unsat = float(sys.argv[2])

 # file set
 file1 = open(sys.argv[1],"r")

 calc_contrast(file1,counts_unsat)
