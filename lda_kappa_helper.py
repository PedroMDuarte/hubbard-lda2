
import numpy as np
import matplotlib 

import scubic
import lda

from scipy.interpolate import interp1d

import logging
# create logger 
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler()) 
#logger.disabled = True

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
    extents = kwargs.pop('params_extents', 31.)
    direc   = '111'
    mu0     = 'halfMott'
    muBrent = kwargs.pop('params_muBrent',(-0.2,0.3)) 
    muBrentShift = kwargs.pop('params_muBrentShift', 0.)



    aS     = kwargs.pop('params_aS', 300.) 
    muPlus = kwargs.pop('params_muPlus', 0.00 )
    Natoms = kwargs.pop('params_Natoms', None)
    

    select = 'nlce'
    #print 
    #print "muPlus = ", muPlus
    pot = scubic.sc(allIR=s, allGR=g, allIRw=wIR, allGRw=wGR)

    Tlist = kwargs.pop('Tlist', [0.036])
    outdict = {} 
    for Tval in Tlist:
        logger.warning('working on Tval = {:0.4f}'.format(Tval) )
        if Natoms is None:
            lda0 = lda.lda(potential = pot, Temperature=Tval, a_s=aS, \
                           override_npoints = 240,\
                           extents=extents, \
                           globalMu=mu0, halfMottPlus=muPlus,\
                           verbose=False, \
                           select = select,\
                           ignoreExtents=False, ignoreSlopeErrors=True, \
                           ignoreMuThreshold=True)
        else:
            lda0 = lda.lda(potential = pot, Temperature=Tval, a_s=aS, \
                           override_npoints = 240,\
                           extents=extents, \
                           Natoms = Natoms,\
                           muBrent=muBrent, muBrentShift=muBrentShift,\
                           verbose=False, \
                           select = select,\
                           ignoreExtents=False, ignoreSlopeErrors=True, \
                           ignoreMuThreshold=True)
    
        r111, n111 = lda0.getDensity( lda0.globalMu, lda0.T)  
        localMu_t = lda0.get_localMu_t( lda0.globalMu )
    
        localMu_t_f = extrap1d( interp1d( r111, localMu_t ) )
        dmu_dr = deriv( rpoints, localMu_t_f )
        dmu_dr111 = deriv( r111, localMu_t_f ) 
    
        t0 = lda0.tunneling_111.min()
        # Need to also get the value of T/t0 and the overall S/N 
        _spibulk, _spi, _r111, _n111, _U111, _t111, _entrbulk, _entr111,\
        _lda_num, _density111, _k111, _k111htse_list = \
            lda0.getBulkSpi(Tspi=Tval/t0, inhomog=True, \
               spiextents=extents, entextents=extents, do_k111=True) 
    
        Tdict = {
                   'r111':r111 ,\
                   'n111':n111 ,\
                   'Ut111':lda0.onsite_111 / lda0.tunneling_111 ,\
                   'localMu_t':localMu_t ,\
                   'dmu_dr': dmu_dr ,\
                   'dmu_dr111': dmu_dr111 ,\
                   'num':lda0.Number,\
                   'T/t0': Tval/t0 ,\
                   'S/N':_entrbulk ,\
                          } 
        outdict[ Tval ] = Tdict

    return outdict 
