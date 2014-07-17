
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
import pickle
 
import spi_vs_n 
from colorChooser import rgb_to_hex, cmapCycle


savedir = 'dataplots/EXP/' 
if not os.path.exists(savedir):
    os.makedirs(savedir) 
if not os.path.exists(savedir + 'Inhomog'):
    os.makedirs(savedir + 'Inhomog') 

for aS,mu,spiext in [ (200, 0.12, 20.), (290,0.095,20.),\
               (380, 0.05,19.2), (470,-0.01,17.0) ]:

    finegrid = True 
    spis = spi_vs_n.Spi_vs_N( aS=aS, Spi_inhomog=True, Tspi=0.53, \
          savedir=savedir,\
          mulist = [mu],  bestForce=0, spiextents=spiext, entextents=17.,\
          finegrid=finegrid )
    
    fname = savedir + 'aS{:03d}_mu{:0.2f}.pck'.format(aS,mu) 
    pickle.dump( spis, open( fname, "wb" ) )        
            
            
