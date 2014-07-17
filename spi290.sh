#!/bin/bash

# Optimal atom numbers 
# 200.  1.5
# 290.  1.7 
# 380.  1.79
# 470   1.84 

python spi_vs_n.py 290. 0.53 --inhomog --savedir dataplots/SPI/290/ \
    --mu 0.095 --best 0 --spiextents 20 --entextents 35 

#python spi_vs_n.py 290. 0.56 --inhomog --savedir dataplots/SPI/290/ \
#    --mu 0.095 --best 0 --spiextents 20 --entextents 35 
#
#python spi_vs_n.py 290. 0.62 --inhomog --savedir dataplots/SPI/290/ \
#    --mu 0.095 --best 0 --spiextents 23 --entextents 35 
#
#python spi_vs_n.py 290. 0.68 --inhomog --savedir dataplots/SPI/290/ \
#    --mu 0.095 --best 0 --spiextents 25 --entextents 35 
#
#python spi_vs_n.py 290. 0.80 --inhomog --savedir dataplots/SPI/290/ \
#    --mu 0.095 --best 0 --spiextents 27 --entextents 35 
#
#python spi_vs_n.py 290. 0.99 --inhomog --savedir dataplots/SPI/290/ \
#    --mu 0.095 --best 0 --spiextents 28 --entextents 35
#
#python spi_vs_n.py 290. 1.99 --inhomog --savedir dataplots/SPI/290/ \
#    --mu 0.095 --best 0 --spiextents 27 --entextents 35 


