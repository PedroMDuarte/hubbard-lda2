
import numpy as np
import matplotlib.pyplot as plt
import matplotlib 

import scubic
import lda
    
from colorChooser import rgb_to_hex, cmapCycle

def Spi_vs_N( aS=200., Spi_inhomog=False, Tspi=0.9, \
              savedir='dataplots/VaryN_Spi', \
              mulist =[-0.15, -0.075, 0., 0.10, 0.18], 
              bestForce = -1 ,
              spiextents = 25., 
              entextents = 25., 
              finegrid = False, 
              ):

    s       = 7.
    g       = 3.666
    wIR     = 47.
    wGR     = 47./1.175
    T       = 0.035
    extents = 30.
    direc   = '111'
    mu0     = 'halfMott'

    spis = [] 
    select = 'nlce'

    for tag, muPlus in enumerate(mulist):
        print 
        print "muPlus = ", muPlus
        pot = scubic.sc(allIR=s, allGR=g, allIRw=wIR, allGRw=wGR)

        lda0 = lda.lda(potential = pot, Temperature=T, a_s=aS, \
                       extents=extents, \
                       globalMu=mu0, halfMottPlus=muPlus,\
                       verbose=True, \
                       select = select,\
                       ignoreExtents=False, ignoreSlopeErrors=True, \
                       ignoreMuThreshold=True)

        spibulk, spi, r111, n111, U111, t111, entrbulk, entr111,\
        lda_num, density111  = \
            lda0.getBulkSpi(Tspi=Tspi, inhomog=Spi_inhomog, \
               spiextents=spiextents, entextents=entextents)
    
        if finegrid: 
            r111_fine, spi111_fine, n111_fine = \
                lda0.getSpiFineGrid( Tspi=Tspi, numpoints=320,\
                    inhomog=Spi_inhomog, spiextents=spiextents, \
                    entextents=entextents )
        else:
            r111_fine, spi111_fine, n111_fine = None, None, None


        spis.append( {'SpiBulk':spibulk,\
                      'spi111':spi,\
                      'r111':r111,\
                      'n111':n111,\
                      'U111':U111,\
                      't111':t111,\
                      'entrbulk':entrbulk,\
                      'entr111':entr111,\
                      'Number':lda0.Number,\
                      'ldanum':lda_num,\
                      # dens111 is the one obtained from QMC
                      'dens111':density111,\
                      'Tn':T,\
                      'Tspi':Tspi,\
                      'aS':aS,\
                      'savedir':savedir,\
                      'r111_fine':r111_fine,\
                      'spi111_fine':spi111_fine,\
                      'n111_fine':n111_fine,\
                      } ) 

        # Figure to check inhomogeneity
        fig111, binresult, peak_dens, radius1e, peak_t, output = \
            lda.CheckInhomog( lda0, closefig = True, n_ylim=(-0.1,2.0) ) ;

        figfname = savedir + 'Inhomog/{:0.3f}gr_{:03d}_{}_T{:0.4f}Er.png'.\
                   format(g,tag,select,T)

        fig111.savefig(figfname, dpi=300)

    plot_spis( spis, inhomog=Spi_inhomog, bestForce=bestForce)
    
    return spis[bestForce] 



def plot_spis( spis,  inhomog=False, bestForce = -1):
    """ This function makes a nice plot of the results of 
    the studies of Spi_vs_n""" 

    from matplotlib import rc
    rc('font', **{'family':'serif'})
    rc('text', usetex=True)

    fig = plt.figure(figsize=(9.,5.8))
    gs = matplotlib.gridspec.GridSpec(3,4,\
            wspace=0.45, hspace=0.15,\
            left=0.07, right=0.96, bottom=0.08, top=0.9)

    

    axn = fig.add_subplot( gs[0,0])
    axSpi = fig.add_subplot( gs[0,1]) 
    axEnt = fig.add_subplot( gs[0,2])
    axEntP = fig.add_subplot( gs[2,2])

    axVol  = fig.add_subplot( gs[1,0] ) 
    axVolSpi = fig.add_subplot( gs[1,1] ) 
    axVolEnt = fig.add_subplot( gs[1,2] ) 


    axT = fig.add_subplot( gs[2,0])
    axU = fig.add_subplot( gs[2,1])

    axSpiB = fig.add_subplot(gs[0,3])
    axEntB = fig.add_subplot(gs[1,3])
    axFrac = fig.add_subplot(gs[2,3])


    savedir = spis[0]['savedir']
    aS = spis[0]['aS']
    U0 = spis[0]['U111'].max()
    T0 = spis[0]['Tspi']
    t0 = spis[0]['t111'].min()
    T0dens = spis[0]['Tn']/t0 
    
    titletext = r'$\mathrm{{density\ at\ }} [T/t]_{{0}}={:0.2f}$\, \ \ \ '\
               .format(T0dens)
    titletext += r'$S_{{\pi}}\ \mathrm{{at}}\ \ [U/t]_{{0}}={:0.1f}\ , \  \ $'\
                 .format(U0) + \
                 r'$[T/t]_{{0}}={:0.2f}\ \ $'.format(T0) 

    #if inhomog:
    #    titletext = titletext + r'$\mathrm{{Inhomogeneous}}$'
    
    fig.text(0.5, 0.98, titletext, ha='center', va='top', fontsize=13) 


    spiBs = []
    for spi in spis:
        spiBs.append( spi['SpiBulk'] ) 
    best = np.argmax( spiBs ) 

    if bestForce != -1:
        best = bestForce

    print 
    print "Best result =", best
        

    results = [] 
    for ii, spi in enumerate(spis):

        try:
            color = cmapCycle( matplotlib.cm.jet, float(ii), \
                    lbound=0, ubound=float(len(spis)-1))
        except:
            color = 'blue'
  
        spiB = spi['SpiBulk']
        spi0 = spi['spi111'].max()
        entB = spi['entrbulk'] 

        # effective contributing fraction
        x = (spiB - 1.)/(spi0-1.)


        t0 = spi['t111'].min()
        #print "T (density) = ", spi['Tn']/t0
        Tspi = spi['Tspi']

        lw =1.5 
        axn.plot(spi['r111'], spi['n111'], color=color, lw=lw,\
            label='{:0.1f}'.format(spi['Number']/1e5))
            #label='{:0.1f}({:0.1f})'.format(spi['Number']/1e5, spi['ldanum']/1e5))

        axn.plot(spi['r111'], spi['dens111'], 'o', color=color, lw=lw, \
            ms=3., alpha=0.3 ) 

        axSpi.plot(spi['r111'], spi['spi111'], color=color, lw=lw)
        axEnt.plot(spi['r111'], spi['entr111'], color=color, lw=lw)
        axEntP.plot(spi['r111'], spi['entr111']/spi['dens111'], color=color, lw=lw)

        axVol.plot(spi['r111'], \
            4.*np.pi * np.power( spi['r111'],2) * spi['n111'] / 1e3 ,\
                   color=color, lw=lw)

        axVolSpi.plot(spi['r111'], \
            4.*np.pi * np.power( spi['r111'],2) * spi['spi111'] \
                      * spi['n111'] / 1e3 ,\
              color=color, lw=lw)

        axVolEnt.plot(spi['r111'], \
            4.*np.pi * np.power( spi['r111'],2) * spi['entr111'] / 1e3,\
              color=color, lw=lw)
         

        axT.plot( spi['r111'], Tspi * t0 / spi['t111'], color='black', lw=lw  )
        axU.plot( spi['r111'], spi['U111'], color='black', lw=lw )

        pos = spi['r111'] > 0 
        indmax =  np.argmax( spi['spi111'][pos]  ) 
        rmax = spi['r111'][pos][indmax] 
        tbest = spi['t111'][pos][indmax] 
        Tbest = Tspi * t0 / tbest 
        Ubest = spi['U111'][pos][indmax]
        results.append( [spi['Number']/1e5, spiB, x*100., entB, tbest, Tbest, Ubest] )

        # Find the max of spi 
        if ii == best:
            axSpi.axvline( rmax, color=color, alpha=0.7  ) 
            axn.axvline( rmax, color=color, alpha=0.7  ) 
            axT.axvline( rmax, color=color, alpha=0.7  ) 
            axU.axvline( rmax, color=color, alpha=0.7 )

            axT.text( 0.95, 0.95,  '$[T/t]^{{*}}={:0.2f}$'.format(Tbest),\
                      ha='right', va='top', color='black',\
                      transform = axT.transAxes, fontsize=10, 
                      bbox= {'boxstyle':'round', 'facecolor':'white'}) 
            axU.text( 0.95, 0.95,  '$[U/t]^{{*}}={:0.1f}$'.format(Ubest),\
                      ha='right', va='top', color='black',\
                      transform = axU.transAxes, fontsize=10, 
                      bbox= {'boxstyle':'round', 'facecolor':'white'}) 
 

    results = np.array(results)
    

    fname = savedir + 'aS{:03d}_U{:02d}_Tspi{:0.2f}.dat'.format( int(aS), int(U0), T0 ) 
    np.savetxt( fname, results, fmt='%.4g',\
     header= '# N/1e5  Spi  Frac  S/N  t*  T/t*  U*/t* ' )

    legend = axn.legend(title='$N/10^{5}$',bbox_to_anchor=(1.02,1.02), \
           loc='upper right', numpoints=1, \
           prop={'size':6}, handlelength=1.1, handletextpad=0.5)

    plt.setp(legend.get_title(),fontsize=6.5) 
 
    axSpiB.plot( results[:,0], results[:,1],'.-', color='black')
    axFrac.plot( results[:,0], results[:,2],'.-', color='black')
    axEntB.plot( results[:,0], results[:,3],'.-', color='black')

    axn.set_ylabel('$n$', rotation=0, labelpad=12, fontsize=13)
    axT.set_ylabel('$T/t$', rotation=0, labelpad=12, fontsize=13)
    axU.set_ylabel('$U/t$', rotation=0, labelpad=12, fontsize=13)
    axSpi.set_ylabel(r'$\frac{S_{\pi}}{n}$', rotation=0, labelpad=12, \
                     fontsize=13)

    axEnt.set_ylabel(r'$s$', rotation=0, labelpad=12, fontsize=13)
    axEntP.set_ylabel(r'$\frac{s}{n}$', rotation=0, labelpad=12, fontsize=14)
    axVol.set_ylabel(r'$(4\pi r^{2}) n $', rotation=90) 
    axVolSpi.set_ylabel(r'$(4\pi r^{2}) S_{\pi} $', rotation=90) 
    axVolEnt.set_ylabel(r'$(4\pi r^{2}) s $', rotation=90)


    def scale_text(ax):
        ax.text( 0.0, 1.0, r'$\times 10^{3}$', ha='left', va='bottom',\
             transform = ax.transAxes, fontsize=9) 
    for axV in [axVol, axVolSpi, axVolEnt]:
        scale_text(axV) 
    


    axSpiB.set_ylabel(r'$\bar{S}_{\pi}$', rotation=0, labelpad=12, \
                     fontsize=13)
    axEntB.set_ylabel(r'$\frac{S}{N}$', rotation=0, labelpad=12, \
                     fontsize=13)
    axFrac.set_ylabel('Effective fraction (\%)', fontsize=10)

    axFrac.set_xlabel('$N/10^{5}$')
   
    x1 = 29. 
    axn.set_xlim(0.,x1)
    axT.set_xlim(0.,x1)
    axU.set_xlim(0.,x1)
    axSpi.set_xlim(0.,x1) 

    axT.set_ylim(0.3, 1.00)
    axU.set_ylim(0., 20.00)
    axSpi.set_ylim(0.5, 6.0) 

    axSpiB.set_xlim(0., 3.5)
    axFrac.set_xlim(0., 3.5)
    axSpiB.set_ylim(0.8,2.5)
    axFrac.set_ylim(0., 65.) 

    axEnt.set_xlim(0., x1) 
    axEntP.set_xlim(0., x1) 
    axVol.set_xlim(0., x1)
    axVolSpi.set_xlim(0., x1)
    axVolEnt.set_xlim(0., x1)  
    axEntB.set_xlim( 0., 3.5  )

    axEnt.set_ylim(0., 1.0) 
    axEntP.set_ylim(0.,4.0) 
    axVol.set_ylim(0., 3.0)
    axVolSpi.set_ylim(0., 15.)
    axVolEnt.set_ylim(0., 4.0)  
    axEntB.set_ylim( 0., 2.0  )
   

    for ax in [axVol, axVolSpi, axVolEnt, axEntB, axU, axT]:
        ax.yaxis.set_major_locator( matplotlib.ticker.MaxNLocator(5) ) 

    for ax in [axSpiB, axFrac]:
        ax.xaxis.set_major_locator( matplotlib.ticker.MaxNLocator(5) ) 

    for ax in [axn, axSpi, axEnt, axVol, axVolSpi,  axVolEnt, axSpiB, axEntB]:
        ax.xaxis.set_ticklabels([])
    for ax in [axT, axU, axEntP]:
        ax.set_xlabel('$r_{111}\ (\mu\mathrm{m})$')


    for ax in [axn, axSpi, axT, axU, axSpiB, axFrac, \
             axEnt, axEntP, axVol, axVolEnt, axVolSpi, axEntB]:
        ax.grid(alpha=0.3)

    if inhomog:
        inhomog_tag = 'inhomog'
    else:
        inhomog_tag = '' 
    fig.savefig( savedir + 'Tn{:0.2f}_U{:04.1f}_T{:0.2f}'.\
                 format(T0dens,U0,T0) + inhomog_tag +'.png', dpi=300)


import os
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser('spi_vs_n.py')
    parser.add_argument('SCATTLEN', action="store", type=float, \
        help='Scattering length') 
    parser.add_argument('TSPI', action="store", type=float, \
        help='The value of [T/t]_0 used for Spi')
    parser.add_argument('--inhomog', action="store_true", \
        help='Whether or not to use inhomogeneous U/t and T/t in Spi') 
    parser.add_argument('--savedir', action="store", type=str, \
        help='Directory to put the results')
    parser.add_argument('--mu', nargs='+', type=float, \
        help='List of chemical potentials to consider') 
    parser.add_argument('--best', action='store', type=int, default=-1,\
        help='Selects which of the mus to highlight in the plot')
    parser.add_argument('--spiextents', action='store', type=float, default=25.,\
        help='Sets the extents over which to calculate Spi')
    parser.add_argument('--entextents', action='store', type=float, default=25.,\
        help='Sets the extents over which to calculate Entropy')

    args = parser.parse_args()

    print args  

    if not os.path.exists(args.savedir):
        os.makedirs(args.savedir) 
    if not os.path.exists(args.savedir + 'Inhomog'):
        os.makedirs(args.savedir + 'Inhomog') 


    #Spi_inhomog = False
    #aS      = 200. 
    #Ts      = 0.9 
    Spi_vs_N( aS=args.SCATTLEN, \
              Spi_inhomog=args.inhomog, \
              Tspi = args.TSPI,\
              savedir = args.savedir,\
              mulist = args.mu,\
              bestForce = args.best,\
              spiextents = args.spiextents,\
              entextents = args.entextents
             ) 
