#!/bin/bash

# Optimal atom numbers 
# 200.  1.5
# 290.  1.7 
# 380.  1.79
# 470   1.84 

python spi_vs_n.py 200. 0.50 --inhomog --savedir dataplots/SPI/200/ \
    --mu  0.12  --best 0 --spiextents 19.  --entextents 30

python spi_vs_n.py 200. 0.51 --inhomog --savedir dataplots/SPI/200/ \
    --mu  0.12  --best 0 --spiextents 18.5  --entextents 30

python spi_vs_n.py 200. 0.53 --inhomog --savedir dataplots/SPI/200/ \
    --mu  0.12  --best 0 --spiextents 19  --entextents 30

python spi_vs_n.py 200. 0.56 --inhomog --savedir dataplots/SPI/200/ \
    --mu  0.12  --best 0 --spiextents 19  --entextents 30

python spi_vs_n.py 200. 0.62 --inhomog --savedir dataplots/SPI/200/ \
    --mu  0.12  --best 0 --spiextents 23  --entextents 30

python spi_vs_n.py 200. 0.68 --inhomog --savedir dataplots/SPI/200/ \
    --mu  0.12  --best 0 --spiextents 25  --entextents 30

python spi_vs_n.py 200. 0.80 --inhomog --savedir dataplots/SPI/200/ \
    --mu  0.12  --best 0 --spiextents 27  --entextents 30

python spi_vs_n.py 200. 0.99 --inhomog --savedir dataplots/SPI/200/ \
    --mu  0.12  --best 0 --spiextents 27  --entextents 30 

python spi_vs_n.py 200. 1.99 --inhomog --savedir dataplots/SPI/200/ \
    --mu  0.12  --best 0 --spiextents 27  --entextents 30 

