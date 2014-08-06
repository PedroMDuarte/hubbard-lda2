
import numpy as np
import matplotlib.pyplot as plt
import matplotlib 

import scubic
import lda

from scipy.interpolate import interp1d


def deriv( x, f ):
    """ 
    This function is used to take a derivative
    """ 
    dx = 0.001
    return (f(x+dx) - f(x-dx))/(2.*dx)

def extrap1d( f ):
    """ 
    This function is used to extend the 1d interpolator 
    returned by interp1d, such that it extrapolates linearly
    for some small range outside of the data range. 
    """ 
    xs = f.x 
    ys = f.y 
  
    dx = 0.001 

    mStart = ( f(xs[0] + dx ) - f(xs[0]) ) / dx  
    mEnd   = ( f(xs[-1]) - f(xs[-1] - dx) ) / dx  

    def f2(x):
        'vectorized piecewise function for extrapolation'
        return np.piecewise(x, [x < xs[0], (x>=xs[0]) & (x<=xs[-1]), x > xs[-1]], \
              [\
               lambda x: f(xs[0]) + mStart * (x-xs[0]), \
               lambda x: f(x), \
               lambda x: f(xs[-1]) + mEnd * (x-xs[-1]), \
            ])
    return f2
        
    
    
    
from colorChooser import rgb_to_hex, cmapCycle

    
def dmu_dr( rpoints, **kwargs ):
    s       = kwargs.pop('params_s', 7.) 
    g       = kwargs.pop('params_g', 3.666)
    wIR     = kwargs.pop('params_wIR', 47.) 
    wGR     = kwargs.pop('params_wGR', 47./1.175) 
    T       = kwargs.pop('params_T', 0.036) 
    extents = kwargs.pop('params_extents', 31.)
    direc   = '111'
    mu0     = 'halfMott'

    aS     = kwargs.pop('params_aS', 300.) 
    muPlus = kwargs.pop('params_muPlus', 0.00 ) 

    select = 'nlce'

    print 
    print "muPlus = ", muPlus
    pot = scubic.sc(allIR=s, allGR=g, allIRw=wIR, allGRw=wGR)


    lda0 = lda.lda(potential = pot, Temperature=T, a_s=aS, \
                   override_npoints = 240,\
                   extents=extents, \
                   globalMu=mu0, halfMottPlus=muPlus,\
                   verbose=True, \
                   select = select,\
                   ignoreExtents=False, ignoreSlopeErrors=True, \
                   ignoreMuThreshold=True)

    r111, n111 = lda0.getDensity( lda0.globalMu, lda0.T)  
    localMu_t = lda0.get_localMu_t( lda0.globalMu )

    localMu_t_f = extrap1d( interp1d( r111, localMu_t ) )
    dmu_dr = deriv( rpoints, localMu_t_f )

     

    outdict = {
               'r111':r111,\
               'n111':n111,\
               'localMu_t':localMu_t,\
               'dmu_dr': dmu_dr,\
                      } 
    return outdict  

