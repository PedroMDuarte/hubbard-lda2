
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
import pickle
 
import spi_vs_n 
from colorChooser import rgb_to_hex, cmapCycle



 
savedir = 'dataplots/SYS/04_wIR/' 
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
    for mu, Tnlce, ext, wIR, spiextmult in [\
          ( 0.518, 0.035, 28.0, 43., 0.9), \
          ( 0.310, 0.035, 29.0, 45., 0.95), \
          ( 0.183, 0.035, 29.6, 46.2, 0.98), \
          ( 0.139, 0.035, 29.8, 46.6, 0.99), \
          ( 0.095, 0.035, 30.0, 47., 1.00), \
          ( 0.040, 0.035, 30.2, 47.5, 1.02), \
          ( -0.015, 0.035, 30.5, 48., 1.03), \
          (-0.123, 0.035, 31.0, 49., 1.05), \
          (-0.295, 0.035, 32.0, 51., 1.00), \
        ]: 

        spiext = spiextmult * spiexts[ii]  
  
        key = '{:0.3f}wIR_{:0.3f}T'.format( wIR, Tstardict[Tspi] ) 
       
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
              figfname2 = figfname2
     
            )
        
        fname = savedir +  key + '.pck' 
        pickle.dump( spis, open( fname, "wb" ) )        
                
            
