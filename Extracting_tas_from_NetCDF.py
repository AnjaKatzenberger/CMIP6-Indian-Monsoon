#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 10:16:18 2020

@author: anjakatzenberger
"""

import netCDF4 as nc
import os

###############################################################
#        EXTRACTING TAS DATA FROM NETCDF-FILES                #
#                   Anja Katzenberger                         #
#           anja.katzenberger@pik-potsdam.de                  #
#                       18.06.2020                            #
###############################################################
# Extracting temperature data (tas) from NETCDF Format to Python

# Directories with files of interest
ssp = 'ssp585'
dir = ""

files = os.listdir(dir)


#### Extracting pr data
tas_c = []
tas_c_model = []

for file in files:
    dir_file = os.sep.join((dir, file))
    data = nc.Dataset(dir_file)

            
# combined: 1850-2100    
    if file.endswith("ymean_fldmean.nc"):
            center_model = file.split('_' + ssp)[0][3:]
            model = center_model.split('_')[2]
            tas = data['tas'][:]
            tas_c_i = []
            for i in range(len(tas)):
                tas_i = tas[i][0][0]
                tas_c_i.append(tas_i)
            tas_c.append(tas_c_i)
            tas_c_model.append(model)    
      
        
print(tas_c_model)
print(tas_c)

        
        
        
        
        
        
        
        
        
