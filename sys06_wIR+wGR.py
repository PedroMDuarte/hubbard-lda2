
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
import pickle
 
import spi_vs_n 
from colorChooser import rgb_to_hex, cmapCycle



 
savedir = 'dataplots/SYS/06_wIR+wGR/' 
if not os.path.exists(savedir):
    os.makedirs(savedir) 
if not os.path.exists(savedir + 'Inhomog'):
    os.makedirs(savedir + 'Inhomog')

Tstardict = { 0.53:0.46, 0.55:0.48, 0.57:0.50, 0.61:0.54, 0.68:0.60 }

aS = 290.0 
spiexts = [ 20., 21.0, 22., 22.5, 23.0] 

for ii,Tspi in enumerate([0.53, 0.55, 0.57, 0.61, 0.68]):
#    if ii != 2: continue 
    if ii != 4: continue
    for mu, Tnlce, ext, yscale, spiextmult in [\
          ( 0.229, 0.035, 26.0, 0.85, 0.85), \
          ( 0.180, 0.035, 27.0, 0.90, 0.90), \
          ( 0.143, 0.035, 28.0, 0.94, 0.94), \
          ( 0.095, 0.035, 30.0, 1.00, 1.00), \
          ( 0.028, 0.035, 31.0, 1.10, 1.10), \
          (-0.026, 0.035, 32.0, 1.20, 1.20), \
        ]: 

               
        spiext = spiextmult * spiexts[ii]
        wIR = 47. * yscale 
        wGR = (47./1.175) * yscale  
        #print 
        #print "yscale = ", yscale
        #print "spiext = ", spiext
        #continue
  
        key = '{:0.3f}yscale_{:0.3f}T'.format( yscale, Tstardict[Tspi] ) 
       
        figfname = savedir + 'Inhomog/' + key + '.png' 
        figfname2 = savedir +  key + '.png' 
    
        finegrid = False 
        spis = spi_vs_n.Spi_vs_N( aS=aS, Spi_inhomog=True, Tspi=Tspi, \
              savedir=savedir, mulist = [mu],  bestForce=0, \
              spiextents=spiext, entextents=35.,\
              finegrid=finegrid, \
              # Kwargs follow 
              params_T = Tnlce, \
              params_extents = ext, \
              params_figfname = figfname, \
              params_wIR=wIR ,\
              params_wGR=wGR ,\
              figfname2 = figfname2
     
            )
        
        fname = savedir +  key + '.pck' 
        pickle.dump( spis, open( fname, "wb" ) )        
                
            
