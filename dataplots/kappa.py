
import numpy as np
from scipy.interpolate import interp1d

# Define a function to get the compressibility
def deriv( x, f ):
    dx = 0.001
    return (f(x+dx) - f(x-dx))/(2.*dx)
def compressibility( mudat, ndat):
    # I want to evaluate a derivative of n^{2/3} to obtain the compressibility.
    # The evaluation should be at the points where we have data 
    n23 = ndat**(2./3.)
    mupadded  = np.concatenate(([mudat[0]-1.], mudat, [mudat[-1]+1.]))
    n23padded = np.concatenate(([n23[0]], n23, [n23[-1]]))
    n23f = interp1d( mupadded , n23padded)
    cdat = deriv( mudat, n23f)
    return cdat 
