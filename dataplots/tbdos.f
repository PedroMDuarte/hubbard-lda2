c File tbdos.f
       subroutine tbdos(dos,e, n, d)
       double precision e
       integer n
       double precision d 
       double precision dos
       double precision ki  
       double precision kj
       double precision kk
       double precision ee 
cf2py  intent(in) :: e
cf2py  intent(in) :: n
cf2py  intent(in) :: d
cf2py  intent(out) :: dos
       parameter (PI=4.D0*DATAN(1.D0))

       dos = 0 
       do 10 i=0, n/2 + MOD(n,2) -1 
           do 20 j=0, n/2 + MOD(n,2) -1 
               do 30 k=0, n/2 + MOD(n,2) -1
                   ki = 2.*PI / n * i
                   kj = 2.*PI / n * j
                   kk = 2.*PI / n * k
                   ee = (e + DCOS(ki) + DCOS(kj) + DCOS(kk))**2.
                   dos = dos + d / (PI * ( ee + d**2. ))
c                    d/( np.pi*( (e+np.cos(kx)+np.cos(ky)+np.cos(kz))**2. + d**2.))
30             continue
20         continue
10     continue
       dos = 2.*dos / (n/2.)**3
       end