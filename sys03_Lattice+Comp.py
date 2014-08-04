
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
import pickle
 
import spi_vs_n 
from colorChooser import rgb_to_hex, cmapCycle



 
savedir = 'dataplots/SYS/03_Lattice+Comp/' 
if not os.path.exists(savedir):
    os.makedirs(savedir) 
if not os.path.exists(savedir + 'Inhomog'):
    os.makedirs(savedir + 'Inhomog')

Tstardict = { 0.53:0.46, 0.55:0.48, 0.57:0.50, 0.61:0.54, 0.68:0.60 }

aS = 290.0 
spiexts = [ 20., 21.0, 22., 22.5, 23.0] 

for ii,Tspi in enumerate([0.53, 0.55, 0.57, 0.61, 0.68]):
#    if ii > 0: continue
    if ii != 4: continue 
    for mu, Tnlce, ext, ymult, spiextmult in [\
          (-0.001, 0.035, 27.0, 0.88, 1.0), \
          (+0.018, 0.036, 28.5, 0.90, 1.0), \
          (+0.059, 0.035, 29.2, 0.95, 1.0), \
          ( 0.095, 0.035, 30., 1.0, 1.0), \
          ( 0.130, 0.035, 30., 1.05, 0.96), \
          (+0.164, 0.035, 30., 1.1, 0.92), \
          (+0.197, 0.035, 30., 1.15, 0.85), \
        ]: 

        spiext = spiextmult * spiexts[ii]
  
        s = ymult * 7. 
        g = ymult * 3.666
    
        key = '{:0.3f}ymult_{:0.3f}T'.format( ymult, Tstardict[Tspi] ) 
       
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
              params_s=s ,\
              params_g=g ,\
              figfname2 = figfname2
     
            )
        
        fname = savedir +  key + '.pck' 
        pickle.dump( spis, open( fname, "wb" ) )        
                
            
