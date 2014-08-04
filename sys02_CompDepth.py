
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
import pickle
 
import spi_vs_n 
from colorChooser import rgb_to_hex, cmapCycle



 
savedir = 'dataplots/SYS/02_CompDepth/' 
if not os.path.exists(savedir):
    os.makedirs(savedir) 
if not os.path.exists(savedir + 'Inhomog'):
    os.makedirs(savedir + 'Inhomog')

Tstardict = { 0.53:0.46, 0.55:0.48, 0.57:0.50, 0.61:0.54, 0.68:0.60 }

aS = 290.0 
spiexts = [ 20., 21.0, 22., 22.5, 23.0] 

for ii,Tspi in enumerate([0.53, 0.55, 0.57, 0.61, 0.68]):
#    if ii > 0: continue
#    if ii != 4: continue 
    spiext = spiexts[ii]  
    for mu, Tnlce, ext, g in [\
#          (+0.229, 0.036, 30., 3.466), \
          (+0.198, 0.035, 30., 3.516), \
#          ( 0.164, 0.035, 30., 3.566), \
#          ( 0.095, 0.035, 30., 3.666), \
#          ( 0.022, 0.035, 30., 3.766), \
#          (-0.053, 0.034, 30., 3.866), \
        ]: 
    
        key = '{:0.3f}g_{:0.3f}T'.format( g, Tstardict[Tspi] ) 
       
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
              params_g=g ,\
              figfname2 = figfname2
     
            )
        
        fname = savedir +  key + '.pck' 
        pickle.dump( spis, open( fname, "wb" ) )        
                
            
