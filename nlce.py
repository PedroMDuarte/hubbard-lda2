
"""
This file provides a way to obtain thermodynamic quantities from an 
interpolation of available NLCE solutions 
"""

import numpy as np

import matplotlib.pyplot as plt
import matplotlib
from matplotlib import rc
rc('font', **{'family':'serif'})
rc('text', usetex=True)

from scipy.spatial import Delaunay
from scipy.interpolate import CloughTocher2DInterpolator, LinearNDInterpolator
from scipy.interpolate.interpnd import _ndim_coords_from_arrays



def find_closest_nlce( U=8, T=0.67, mu=4., qty='dens', **kwargs):
    """
    This function finds the closest values of U and T in the NLCE data 
    that straddle the values U and T given as arguments.
    
    This case is a little bit easier than the QMC data because here 
    pretty much everything is available, so we can directly get the 
    closest four (U,T) points to get the triangulation 
    """
    
    Ustep = 2. 
    Ua = Ustep*(U/Ustep - (U%Ustep)/Ustep)
    Ub = Ua + 2. 
    
    #print "U in ", Ua, Ub
    
    
    # The T points are not uniformly spaced so we find the two closest ones
    Ts = np.array([0.4, 0.5, 0.64, 0.72, 0.84, 0.9, 1.0, 1.2, \
                   1.4, 1.6, 1.8, 2.0, 2.2, 2.4])
    
    diff = T-Ts

    error = False

    if np.all( diff < 0 ):
        print "Available temperatures do not make it this low:"
        print " T = ", T
        error = True  

    if not error:    
        order_pos =  np.argsort(np.abs( diff[diff>0] ))
        order_neg =  np.argsort(np.abs( diff[diff<0] ))
        Tpts = sorted( [  Ts[diff>0][ order_pos[0] ] ,  Ts[diff<0][ order_neg[0]] ] )  
    else:
        order = np.argsort( np.abs( diff ) ) 
        Tpts = sorted( [ Ts[order[0]], Ts[order[1]], Ts[order[2]] ] ) 
        #Ta = min(Ts[order[0]], Ts[order[1]])
        #Tb = max(Ts[order[0]], Ts[order[1]])
        #print "T in ", Ta, Tb
    
    datadir = '/home/pmd/sandbox/hubbard-lda2/'
    datfiles = []
    for Uval in [Ua,Ub]:
        for Tval in Tpts:
            fname =  datadir + \
                'NLCE8_Final/U{:02d}/T{:0.2f}.dat'.format(int(Uval),Tval)
            datfiles.append([ fname, Uval, Tval ])
            
    if qty == 'dens':
        COL = 1 
    elif qty == 'entr':
        COL = 2 
    elif qty == 'spi':
        COL = 3 
    else:
        raise "Qty not defined:", qty
            
    MUCOL = 0 
    basedat = [] 

    qtyinterp = kwargs.get( 'qtyinterp', 'nearest' ) 

    for f in datfiles:
        try:
            dat = np.loadtxt(f[0])
            if qtyinterp == 'nearest': 
                index = np.argmin( np.abs(dat[:, MUCOL] - mu )) 
                basedat.append( [f[1], f[2], dat[index, COL]] )
            else:
                # find the two closest chemical potentials that 
                # stride the point  
                mudat = dat[:,MUCOL] 

                # since the mu's are ordered we can do:
                index0 = np.where( mudat <=mu )[0][-1]     
                index1 = np.where( mudat > mu )[0][0] 
               
                qty0 = dat[ index0, COL ] 
                qty1 = dat[ index1, COL ] 
   
                mu0 = dat[ index0, MUCOL ] 
                mu1 = dat[ index1, MUCOL ]

                qtyresult =  qty0 +  (mu-mu0) * (qty1-qty0) / (mu1-mu0) 
                basedat.append( [f[1], f[2], qtyresult] )

                # not implemented yet: 
                #if showqtyinterp: 
                #    fig = plt.figure( figsize=(3.5,3.5))
                #    gs = matplotlib.gridspec.GridSpec( 1,1 ,\
                #            left=0.15, right=0.96, bottom=0.12, top=0.88)
                #    ax = fig.add_subplot( gs[0] )
                #    ax.grid(alpha=0.5)

                #print
                #print " mu = ", mu 
                #print "index0 = ", index0
                #print "index1 = ", index1
                #print "Doing linear interpolation for the qty"
                #print " mu0 = ", mu0 
                #print " mu1 = ", mu1 
                #print "qty0 = ", qty0 
                #print "qty1 = ", qty1
                #print "qtyresult = ", qtyresult

                
        except Exception as e:
            print "Failed to get data from file = ", f
            raise e 
        
    basedat =   np.array(basedat)
    #print "Closest dat = ", basedat
    points = _ndim_coords_from_arrays(( basedat[:,0] , basedat[:,1]))
    
    
    
    #finterp = CloughTocher2DInterpolator(points, basedat[:,2])
    finterp = LinearNDInterpolator( points, basedat[:,2] )
    
    
    try:
        result = finterp( U,T )
        if np.isnan(result):
            raise Exception("!!!! Invalid result !!!!\n")
    except Exception as e:
        print e
        error = True
        
    if error or kwargs.get('showinterp',False):
        #print "Interp points:"
        #print basedat
        
        tri = Delaunay(points)
        fig = plt.figure( figsize=(3.5,3.5))
        gs = matplotlib.gridspec.GridSpec( 1,1 ,\
                left=0.15, right=0.96, bottom=0.12, top=0.88)
        ax = fig.add_subplot( gs[0] )
        ax.grid(alpha=0.5)
        ax.triplot(points[:,0], points[:,1], tri.simplices.copy())
        ax.plot(points[:,0], points[:,1], 'o')
        ax.plot( U, T, 'o', ms=6., color='red')
        xlim = ax.get_xlim()
        dx = (xlim[1]-xlim[0])/10.
        ax.set_xlim( xlim[0]-dx, xlim[1]+dx )
        ylim = ax.get_ylim()
        dy = (ylim[1]-ylim[0])/10.
        ax.set_ylim( ylim[0]-dy, ylim[1]+dy )
        ax.set_xlabel('$U/t$')
        ax.set_ylabel('$T/t$',rotation=0,labelpad=8)
        
        tt = kwargs.get('title_text','')
        ax.set_title( tt + '$U/t={:.2f}$'.format(U) + ',\ \ ' + '$T/t={:.2f}$'.format(T), \
                ha='center', va='bottom', fontsize=10)
        save_err = kwargs.get('save_err',None) 
        if save_err is not None:
            print "Saving png." 
            fig.savefig( save_err, dpi=300)
        plt.show()
    
    return result


QTYINTERP = 'linear' 

def nlce_dens( T, t, mu, U, ignoreLowT=False, verbose=True):
    U_ = U/t 
    T_ = T/t 
    mu_ = mu/t   

    result = np.empty_like(mu) 
    for i in range( len(mu_)):
        result[i] = find_closest_nlce( U=U_[i], T=T_[i], mu=mu_[i], \
                     qty='dens',  qtyinterp=QTYINTERP  ) 
    return result     
 
def nlce_entr( T, t, mu, U, ignoreLowT=False, verbose=True):
    U_ = U/t 
    T_ = T/t 
    mu_ = mu/t   

    result = np.empty_like(mu) 
    for i in range( len(mu_)):
        result[i] = find_closest_nlce( U=U_[i], T=T_[i], mu=mu_[i], \
                     qty='entr', qtyinterp=QTYINTERP ) 
    return result     

def nlce_spi( T, t, mu, U, ignoreLowT=False, verbose=True):
    U_ = U/t 
    T_ = T/t 
    mu_ = mu/t   

    result = np.empty_like(mu) 
    for i in range( len(mu_)):
        result[i] = find_closest_nlce( U=U_[i], T=T_[i], mu=mu_[i], \
                     qty='spi', qtyinterp=QTYINTERP ) 
    return result     

