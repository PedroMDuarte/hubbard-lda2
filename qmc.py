
"""
This file provides a way to obtain thermodynamic quantities from an 
interpolation of available QMC solutions 
"""

import numpy as np

import matplotlib.pyplot as plt
import matplotlib

from matplotlib import rc
rc('font', **{'family':'serif'})
rc('text', usetex=True)

import glob 
import os 

from scipy.spatial import Delaunay
from scipy.interpolate import CloughTocher2DInterpolator, LinearNDInterpolator
from scipy.interpolate.interpnd import _ndim_coords_from_arrays



def get_qty_mu( dat, mu, MUCOL, COL, **kwargs ): 
    # Control the interpolation between availble
    # density points here 
    #~qtyinterp = 'nearest' 
    qtyinterp = 'linear'
    msg = kwargs.get('msg', None)

    DENSCOL = 1  
    ENTRCOL = 2  
    SPICOL  = 3
    CMPRCOL = 4 

    if COL == SPICOL:
        default_minus = 1.0 
        default_plus  = 0.0  
    elif COL == ENTRCOL:
        default_minus = 0.0 
        default_plus  = 0.0  
    elif COL == DENSCOL:
        default_minus = 0.0 
        default_plus  = 2.0   
    elif COL == CMPRCOL:
        default_minus = 0.0 
        default_plus  = 0.0
    else:
        raise ValueError("Column not defined: COL = {:d}".format(COL) ) 
  

    if qtyinterp == 'nearest': 
        index = np.argmin( np.abs(dat[:, MUCOL] - mu )) 
        qtyresult = dat[index,COL] 
       
    else:
        # find the two closest chemical potentials that 
        # stride the point  
        mudat = dat[:,MUCOL]

        verbose = False

        if np.all(mu < mudat):
            qtyresult = default_minus  
 
            if COL == DENSCOL or COL == ENTRCOL:
               if verbose:
                   print "QTY=", COL,
                   print "===>>> mu={:0.2f} ".format(mu), msg 
               return 'out-of-bounds'

               #print "====>>> BE CAREFUL :  Using default density" + \
               #      " n=%.2f"%default_minus  + \
               #      " at mu={:0.2f}  ".format(mu),
               #if msg is not None:
               #    print msg 
               #raise ValueError('density error')

        elif np.all( mu > mudat):
            qtyresult = default_plus

            if COL == DENSCOL or COL == ENTRCOL:
               if verbose:
                   print "QTY=", COL,
                   print "====>>> mu={:0.2f} ".format(mu), msg 
               return 'out-of-bounds'
               #print "====>>> BE CAREFUL :  Using default density" + \
               #      " n=%.2f"%default_plus  + \
               #      " at mu={:0.2f}  ".format(mu),
               #if msg is not None:
               #    print msg 
               #raise ValueError('density error')
               return 'out-of-bounds'

        else:
            # since the mu's are ordered we can do:
            index0 = np.where( mudat <=mu )[0][-1]     
            index1 = np.where( mudat > mu )[0][0] 
           
            qty0 = dat[ index0, COL ] 
            qty1 = dat[ index1, COL ] 
    
            mu0 = dat[ index0, MUCOL ] 
            mu1 = dat[ index1, MUCOL ]
    
            qtyresult =  qty0 +  (mu-mu0) * (qty1-qty0) / (mu1-mu0)

    return qtyresult  





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


def find_closest_qmc( U=8, T=0.67, mu=4.0, **kwargs):
    """
    This function finds the closest values of U and T in the QMC data 
    that straddle the values U and T given as arguments.
    
    """

    nUs = 4 
    nTs = 3
    ALLPTS = kwargs.get('ALLPTS', False) 

    # select which quantity will be returned, options are
    # spi and entropy
    QTY = kwargs.get('QTY', 'spi' ) 
    
    #datadir = '/home/pmd/sandbox/hubbard-lda/QMC_Final/'
    #datadir = '/home/pmd/sandbox/hubbard-lda/COMBINED_Final/'

    if QTY == 'spi':
        datadir = '/home/pmd/sandbox/hubbard-lda2/COMB_Final_Spi/'
    elif QTY == 'entropy':
        datadir = '/home/pmd/sandbox/hubbard-lda2/COMB_Final_Entr/'
    elif QTY == 'density':
        datadir = '/home/pmd/sandbox/hubbard-lda2/COMB_Final_Spi/'
    elif QTY == 'kappa':
        datadir = '/home/pmd/sandbox/hubbard-lda2/COMB_Final_Spi/'
    else:
        raise ValueError('Quantity not defined:' + str(QTY) ) 
         
      
    
    fname = datadir + 'U*'
    us = [ float(u.split('/U')[-1]) for u in glob.glob(fname) ] 
    du = [ np.abs(U-u) for u in us ]
    index = np.argsort(du)

    if ALLPTS: 
        Ulist0 = range(len(index)) 
    else:
        Ulist0 = range( nUs ) 

    us = [ us[index[i]] for i in Ulist0] 
    #print us
    #print du
    #print index
    #print "Closest Us = ", us
    
    datfiles = []
    for u in us:    
    
        # For the Spi and Stheta data
        if QTY == 'spi' or QTY == 'density' or QTY == 'kappa':
            fname = datadir + 'U{U:02d}/T*dat'.format(U=int(u))
            fs = sorted(glob.glob(fname))
            Ts = [ float(f.split('T')[1].split('.dat')[0]) for f in fs ]
        elif QTY=='entropy':
            fname = datadir + 'U{U:02d}/S*dat'.format(U=int(u))
            fs = sorted(glob.glob(fname))
            Ts = [ float(f.split('S')[1].split('.dat')[0]) for f in fs ]


        Ts_g = [] ; Ts_l = []; 
        for t in Ts:
            if t > T:
                Ts_g.append(t) 
            else:
                Ts_l.append(t) 
        
        order_g = np.argsort( [ np.abs( T -t ) for t in Ts_g ] )
        order_l = np.argsort( [ np.abs( T -t ) for t in Ts_l ] )

        try:
            Tpts = [ Ts_g[ order_g[0]] , Ts_l[ order_l[0]]   ] 
        except:
            #print 
            #print "problem adding U=",u, "T=",Ts
            #print "available T data does not stride the point"
            #print "T  =", T
            #print "Ts =", Ts
            #print "will add nearest Ts nevertheless"
            Tpts = [  ] 
              
            #raise ValueError("QMC data not available.")


        dT = [ np.abs( T - t) for t in Ts ] 
        index = np.argsort(dT)
 
        if ALLPTS: 
            Tlist0 = range(len(Ts)) 
        else:
            Tlist0 = range( min(nTs , len(Ts)))
   
        for i in Tlist0:
            Tnew = Ts[index[i]] 
            if Tnew not in Tpts:
                Tpts.append(Tnew) 
        for Tpt in Tpts: 
            index = Ts.index( Tpt )  
            try:
                datfiles.append( [ fs[ index ], u, Ts[index] ] ) 
            except:
                print "problem adding U=",u, "T=",Ts
                raise
          

        # Need to make sure that selected T values stride both
        # sides of the point 
        
        #print
        #print u
        #print Ts
        #print dT
        #print index
        #print fs

#        for i in range(min(3, len(Ts))):
#            try:
#                datfiles.append( [ fs[index[i]], u, Ts[index[i]] ] ) 
#            except:
#                print "problem adding U=",u, "T=",Ts
#                raise
#        
            #datfiles.append( [ fs[index[1]], u, Ts[index[1]] ] ) 
        
    #print datfiles
    MUCOL   = 0 
    DENSCOL = 1
    ENTRCOL = 2  
    SPICOL  = 3 
    CMPRCOL = 4
  
    if QTY == 'spi':
        COL = SPICOL 
    elif QTY == 'entropy':
        COL = ENTRCOL 
    elif QTY == 'density':
        COL = DENSCOL 
    elif QTY == 'kappa':
        COL = CMPRCOL
       
 
    basedat = []
    for f in datfiles:
        # f[0] is the datafile name
        # f[1] is U
        # f[2] is T 

        radius = kwargs.get('radius', np.nan ) 
        msg = 'U={:0.2f}, T={:0.2f}'.format(U,T) + \
               ' mu={:0.2f}, r={:0.2f}, Upt={:0.3f}, Tpt={:0.3f}'.\
               format(mu, radius, f[1], f[2])
 
        try:
            dat = np.loadtxt(f[0])
            spival = get_qty_mu( dat, mu, MUCOL, COL, msg=msg )
            if spival == 'out-of-bounds':
                continue 
                #return 'out-of-bounds' 
            basedat.append( [f[1], f[2], spival] )
        except Exception as e :
            print "Failed to get data from file = ", f  

            # toggle plotting, not implemented yet: 
            #if showqtyinterp: 
            fig = plt.figure( figsize=(3.5,3.5))
            gs = matplotlib.gridspec.GridSpec( 1,1 ,\
                    left=0.15, right=0.96, bottom=0.12, top=0.88)
            ax = fig.add_subplot( gs[0] )
            ax.grid(alpha=0.5) 
            ax.plot( dat[:,MUCOL], dat[:,COL], '.-') 
            ax.axvline( mu )

            ax.text( 0.5, 1.05, msg, ha='center', va='bottom', \
                transform=ax.transAxes) 
            plt.show()
    
           
            raise e
 
        
    error = False
    try: 
        basedat =   np.array(basedat)

        Us = np.unique(basedat[:,0] )
        Ts = np.unique(basedat[:,1] ) 
        validTriang = not ( len(Us) ==1  or len(Ts) ==  1 ) 
        #print "#Us={:d}, #Ts={:d}".format( len(Us), len(Ts) )  
        #print msg 

        if validTriang: 
            points = _ndim_coords_from_arrays(( basedat[:,0] , basedat[:,1]))
            #print "Closest dat = ", basedat
            #finterp = CloughTocher2DInterpolator(points, basedat[:,2])
            finterp = LinearNDInterpolator( points, basedat[:,2] )
        else:
            raise ValueError('not enough finterp points')

    except Exception as e :
        print "QTY=%s -> Interp Error:"%QTY, msg
        print basedat
        print e
        error = True 
        #raise e  

    if error == False:
        try:
            result = finterp( U,T )
            if np.isnan(result):
                raise Exception("\n!!!! Invalid result, QTY:%s!!!!\n"%QTY)
        except Exception as e:
            if kwargs.get('error_nan', False):
                return np.nan 
            else:
                print e
                error = True

    if error == False:
        if result >= 8. and QTY == 'spi' :
            print " Obtained Spi > 8. : U={:0.2f}, T={:0.2f}, mu={:0.2f}".\
                   format( U, T, mu ),
            print "  ==> Spi={:0.2f}".format(float(result))
            error = True
        elif result >=4. and QTY == 'entropy':
            print " Obtained Ent > 4. : U={:0.2f}, T={:0.2f}, mu={:0.2f}".\
                   format( U, T, mu ), 
            print "  ==> Result={:0.2f}".format(float(result))
            error = True
        
    if error or kwargs.get('showinterp',False):

        if kwargs.get('error_nan', False):
            return np.nan 

        print "Interp points:"
        print basedat
        
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
        ax.set_title( tt + '$U/t={:.2f}$'.format(U) + \
                      ',\ \ ' + '$T/t={:.2f}$'.format(T), \
                ha='center', va='bottom', fontsize=10)
        save_err = kwargs.get('save_err',None) 
        if save_err is not None:
            print "Saving png." 
            fig.savefig( save_err, dpi=300)
        plt.show()
        if not kwargs.get('single', False):
            raise ValueError("Could not interpolate using QMC data.")
        if ALLPTS:
            if 'savepath' in kwargs.keys():
                fig.savefig( kwargs.get('savepath',None) , dpi=300) 
    
    return result

        
        
