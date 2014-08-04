
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
import pickle
 
import spi_vs_n 
from colorChooser import rgb_to_hex, cmapCycle



 
savedir = 'dataplots/SYS/05_wGR/' 
if not os.path.exists(savedir):
    os.makedirs(savedir) 
if not os.path.exists(savedir + 'Inhomog'):
    os.makedirs(savedir + 'Inhomog')

Tstardict = { 0.53:0.46, 0.55:0.48, 0.57:0.50, 0.61:0.54, 0.68:0.60 }

aS = 290.0 
spiexts = [ 20., 21.0, 22., 22.5, 23.0 ] 

for ii,Tspi in enumerate([0.53, 0.55, 0.57, 0.61, 0.68]):
#    if ii > 0: continue 
    if ii != 4: continue
    for mu, Tnlce, ext, wGR, spiextmult in [\
          (-0.2155, 0.035, 30.7, 44./1.175, 1.00), \
          (-0.109, 0.035, 30.5, 45./1.175, 1.00), \
          ( -0.004, 0.035, 30.0, 46./1.175, 1.00), \
          ( 0.095, 0.035, 30.0, 47./1.175, 1.00), \
          (+0.185, 0.035, 30.0, 48./1.175, 1.00), \
          (+0.265, 0.035, 30.0, 49./1.175, 1.00), \
          (+0.401, 0.035, 30.0, 51./1.175, 1.00), \
        ]: 

        spiext = spiextmult * spiexts[ii] 
  
        key = '{:0.3f}wGR_{:0.3f}T'.format( wGR, Tstardict[Tspi] ) 
       
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
              params_wGR=wGR ,\
              figfname2 = figfname2
     
            )
        
        fname = savedir +  key + '.pck' 
        pickle.dump( spis, open( fname, "wb" ) )        
                
            
