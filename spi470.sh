#!/bin/bash

# Optimal atom numbers 
# 200.  1.5
# 290.  1.7 
# 380.  1.79
# 470   1.84 

python spi_vs_n.py 470. 0.50 --inhomog --savedir dataplots/SPI/470/ \
    --mu -0.01 --best 0 --spiextents 15.5 --entextents 35

python spi_vs_n.py 470. 0.53 --inhomog --savedir dataplots/SPI/470/ \
    --mu -0.01 --best 0 --spiextents 17 --entextents 35

python spi_vs_n.py 470. 0.56 --inhomog --savedir dataplots/SPI/470/ \
    --mu -0.01 --best 0 --spiextents 18 --entextents 35

python spi_vs_n.py 470. 0.62 --inhomog --savedir dataplots/SPI/470/ \
    --mu -0.01 --best 0 --spiextents 20 --entextents 35

python spi_vs_n.py 470. 0.68 --inhomog --savedir dataplots/SPI/470/ \
   --mu  -0.01 --best 0 --spiextents 25 --entextents 35

python spi_vs_n.py 470. 0.80 --inhomog --savedir dataplots/SPI/470/ \
    --mu -0.01 --best 0 --spiextents 27 --entextents 35

python spi_vs_n.py 470. 0.99 --inhomog --savedir dataplots/SPI/470/ \
    --mu -0.01 --best 0 --spiextents 27 --entextents 35

python spi_vs_n.py 470. 1.99 --inhomog --savedir dataplots/SPI/470/ \
    --mu -0.01 --best 0 --spiextents 27 --entextents 35

